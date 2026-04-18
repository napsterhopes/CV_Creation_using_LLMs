"""
CS01 - CV Creation using LLMs
main.py: Entry point for the automated CV creation pipeline.

Two LLMs are used:
  LLM 1 — Google Gemini 1.5 Flash: extracts structured data from raw profile text
  LLM 2 — Ollama (Llama 3 / Gemma 3): generates polished, ATS-friendly CV content

Usage:
    python main.py --input profile.txt --output my_cv.docx --api-key YOUR_KEY
    python main.py --input profile.pdf --job-desc job.txt --ollama-model gemma3

Environment variable:
    GOOGLE_API_KEY: can be used instead of --api-key
"""

import argparse
import os
import sys

import google.generativeai as genai

from extractor import read_input_file, extract_structured_profile
from generator import generate_cv_content
from formatter import format_cv_to_docx


def parse_args():
    """Define and parse command-line arguments for the CV creation pipeline."""
    parser = argparse.ArgumentParser(
        description="CV Creation using LLMs — CS01 Capstone Project"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input profile file (.txt or .pdf)",
    )
    parser.add_argument(
        "--output", default="output_cv.docx",
        help="Output CV filename (default: output_cv.docx)",
    )
    parser.add_argument(
        "--api-key",
        help="Google Gemini API key (or set GOOGLE_API_KEY env var)",
    )
    parser.add_argument(
        "--ollama-model", default="llama3",
        help="Local Ollama model name for generation (default: llama3)",
    )
    parser.add_argument(
        "--job-desc",
        help="Optional path to a job description file for targeted CV tailoring",
    )
    return parser.parse_args()


def main():
    """
    Orchestrate the full CV creation pipeline:
      1. Read raw input profile (TXT or PDF)
      2. Extract structured data using Gemini (LLM 1)
      3. Generate polished CV content using Ollama (LLM 2)
      4. Format and save as a DOCX file
    """
    args = parse_args()

    # Resolve Gemini API key from argument or environment variable
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: Gemini API key required. Use --api-key or set GOOGLE_API_KEY.")
        sys.exit(1)

    # Validate that the input file exists
    if not os.path.exists(args.input):
        print(f"ERROR: Input file '{args.input}' not found.")
        sys.exit(1)

    # Configure Gemini client (LLM 1)
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    print("\n=== CV Creation Pipeline (CS01) ===")
    print(f"  Input          : {args.input}")
    print(f"  Output         : {args.output}")
    print(f"  LLM 1 (extract): Gemini 1.5 Flash")
    print(f"  LLM 2 (generate): Ollama / {args.ollama_model}")

    # ------------------------------------------------------------------ #
    # Step 1: Read the raw input profile file
    # ------------------------------------------------------------------ #
    print("\n[Step 1] Reading input profile...")
    raw_text = read_input_file(args.input)
    print(f"  Loaded {len(raw_text)} characters from '{args.input}'.")

    # ------------------------------------------------------------------ #
    # Step 2: Extract structured profile using Gemini (LLM 1)
    # ------------------------------------------------------------------ #
    print("\n[Step 2] Extracting structured profile with Gemini (LLM 1)...")
    profile = extract_structured_profile(raw_text, gemini_model)
    print(f"  Profile extracted for: {profile.get('name', 'Unknown')}")
    print(f"  Skills found        : {len(profile.get('skills', []))}")
    print(f"  Experience entries  : {len(profile.get('experience', []))}")
    print(f"  Education entries   : {len(profile.get('education', []))}")

    # ------------------------------------------------------------------ #
    # Step 3: Generate polished CV content using Ollama (LLM 2)
    # ------------------------------------------------------------------ #
    print(f"\n[Step 3] Generating CV content with Ollama '{args.ollama_model}' (LLM 2)...")
    job_desc_text = None
    if args.job_desc:
        if os.path.exists(args.job_desc):
            with open(args.job_desc, "r", encoding="utf-8") as f:
                job_desc_text = f.read().strip()
            print(f"  Job description loaded: {args.job_desc}")
        else:
            print(f"  Warning: Job description file '{args.job_desc}' not found. Skipping.")

    cv_content = generate_cv_content(profile, args.ollama_model, job_desc_text)
    print("  CV content generation complete.")

    # ------------------------------------------------------------------ #
    # Step 4: Format and save the CV as a DOCX file
    # ------------------------------------------------------------------ #
    print(f"\n[Step 4] Formatting and saving CV to '{args.output}'...")
    format_cv_to_docx(cv_content, args.output)

    print(f"\n=== Done! CV saved to: {args.output} ===\n")


if __name__ == "__main__":
    main()
