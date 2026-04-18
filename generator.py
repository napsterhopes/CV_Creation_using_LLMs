"""
CS01 - CV Creation using LLMs
generator.py: Uses Ollama (LLM 2) to generate polished, ATS-friendly CV
content from the structured profile extracted by Gemini (LLM 1).
"""

import ollama


def generate_cv_content(profile: dict, model_name: str = "llama3",
                        job_desc: str = None) -> dict:
    """
    Use Ollama (LLM 2) to generate polished CV sections from structured data.

    Applies prompt engineering to produce ATS-optimized, action-verb-led content.
    If a job description is provided, the CV is tailored to match its requirements.

    Args:
        profile: Structured profile dict from extract_structured_profile().
        model_name: Name of the Ollama model to use (e.g. "llama3", "gemma3").
        job_desc: Optional job description text for targeted tailoring.

    Returns:
        A dict with enhanced CV sections ready to be passed to the formatter.
    """
    # Build an optional job-targeting context string
    job_context = ""
    if job_desc:
        job_context = (
            f"\n\nTarget Job Description:\n{job_desc}\n\n"
            "Tailor all content to highlight alignment with this role."
        )

    # Compact profile summary for use inside prompts
    edu_str = "; ".join(
        f"{e.get('degree')} at {e.get('institution')} ({e.get('year')})"
        for e in profile.get("education", [])
    )
    skills_list = ", ".join(profile.get("skills", []))

    # Step A: Generate an enhanced professional summary
    summary = _call_ollama(
        model_name,
        f"Write a compelling 3-sentence professional summary for a CV. "
        f"Be concise, impactful, and keyword-rich for ATS systems.{job_context}\n\n"
        f"Person: {profile.get('name')}\n"
        f"Education: {edu_str}\n"
        f"Skills: {skills_list}\n"
        f"Existing summary: {profile.get('summary', '')}\n\n"
        "Return ONLY the summary paragraph, no labels or extra text.",
    )

    # Step B: Generate a categorized skills section
    skills_section = _call_ollama(
        model_name,
        f"Organize these skills into 2-4 categories for a CV skills section "
        f"(e.g. Languages, Frameworks, Tools, Soft Skills).{job_context}\n\n"
        f"Skills: {skills_list}\n\n"
        "Return plain text with category labels on their own lines followed by "
        "comma-separated skills. No bullet points.",
    )

    # Step C: Rewrite each experience entry with strong action-verb bullet points
    enhanced_experience = []
    for exp in profile.get("experience", []):
        raw_bullets = "; ".join(exp.get("responsibilities", []))
        enhanced_bullets = _call_ollama(
            model_name,
            f"Rewrite these job responsibilities as 3-4 powerful, action-verb led "
            f"CV bullet points. Quantify impact where you can infer it.{job_context}\n\n"
            f"Role: {exp.get('title')} at {exp.get('company')}\n"
            f"Responsibilities: {raw_bullets}\n\n"
            "Return ONLY the bullet points, one per line, each starting with a dash '-'.",
        )
        enhanced_experience.append({**exp, "enhanced_bullets": enhanced_bullets})

    return {
        "name": profile.get("name", ""),
        "email": profile.get("email", ""),
        "phone": profile.get("phone", ""),
        "summary": summary if summary else profile.get("summary", ""),
        "skills_section": skills_section if skills_section else skills_list,
        "education": profile.get("education", []),
        "experience": enhanced_experience,
        "achievements": profile.get("achievements", []),
        "projects": profile.get("projects", []),
    }


def _call_ollama(model_name: str, prompt: str) -> str:
    """
    Send a single prompt to the Ollama local model and return the response text.
    Handles connection failures gracefully so the pipeline can continue.
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"  Warning: Ollama ({model_name}) call failed — {e}")
        return ""
