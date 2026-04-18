"""
CS01 - CV Creation using LLMs
extractor.py: Reads raw user profile files (TXT or PDF) and uses
Gemini (LLM 1) to extract structured profile data as JSON.
"""

import json
import pdfplumber
import google.generativeai as genai


def read_input_file(file_path: str) -> str:
    """
    Read content from a plain text file or a PDF file.
    For PDFs, extract text from all pages using pdfplumber.
    Returns the full text as a string.
    """
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()


def extract_structured_profile(raw_text: str, model) -> dict:
    """
    Use Gemini (LLM 1) to extract structured profile information from raw
    unstructured text. Prompts the model to return a strict JSON object
    with all key CV fields.

    Args:
        raw_text: Raw profile text (from TXT or PDF).
        model: Configured Gemini GenerativeModel instance.

    Returns:
        A dictionary with keys: name, email, phone, summary, education,
        experience, skills, achievements, projects.
    """
    prompt = f"""You are a professional CV parser. Extract structured information
from the following user profile text.

Return ONLY a valid JSON object with exactly these keys:
- "name": full name (string)
- "email": email address (string)
- "phone": phone number (string)
- "summary": 2-3 sentence professional summary (string)
- "education": list of objects, each with "degree", "institution", "year", "gpa"
- "experience": list of objects, each with "title", "company", "duration",
  "responsibilities" (list of strings)
- "skills": list of skill strings
- "achievements": list of achievement strings
- "projects": list of objects, each with "name", "description",
  "technologies" (list of strings)

If a field is not present, use "" for strings and [] for lists.

User profile text:
---
{raw_text}
---
Return ONLY the JSON object. No markdown, no code fences, no explanation.
"""

    response = model.generate_content(prompt)
    response_text = response.text.strip()

    # Strip markdown code fences if the model added them
    if "```" in response_text:
        lines = response_text.split("\n")
        cleaned = [ln for ln in lines if not ln.strip().startswith("```")]
        response_text = "\n".join(cleaned).strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Graceful fallback: return a minimal usable structure
        print("  Warning: Could not parse JSON from Gemini response. Using fallback.")
        return {
            "name": "Candidate",
            "email": "",
            "phone": "",
            "summary": raw_text[:400],
            "education": [],
            "experience": [],
            "skills": [],
            "achievements": [],
            "projects": [],
        }
