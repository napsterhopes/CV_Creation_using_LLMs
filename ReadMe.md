# [cite_start]CV Creation using LLMs (Capstone_Project-CS[01]) [cite: 1]

---

## Objective
[cite_start]Design and develop a capstone project on "CV Creation using LLMs" to showcase how modern open-source models can automate the creation of CV from information provided by user or some documents[cite: 2].

---

## Required Models
* [cite_start]**Gemma 3 1B via Ollama:** Lightweight, open-source LLM ideal for local, privacy-centric deployment that efficiently handles resume tailoring and document generation tasks[cite: 6].
* [cite_start]**Llama 2 or LlamaIndex:** Versatile frameworks for LLM-based document applications, enabling easy integration and information extraction[cite: 7].
* [cite_start]**ResumeLM:** An open-source AI-powered resume builder that is tailored for ATS-optimized CVs using open models, and supports local setup for privacy[cite: 8].
* [cite_start]**LangChain:** Useful for orchestrating different LLM pipeline stages from extraction to evaluation across various models[cite: 9].

---

## Step by Step Instructions

### 1. Project Setup
* [cite_start]Select an open-source LLM (e.g., Gemma via Ollama or LlamaIndex)[cite: 12].
* [cite_start]Set up a local environment with required dependencies: Python, relevant LLM backends (Ollama, Transformers), and document parsing libraries (e.g., pdfplumber for PDF extraction)[cite: 13, 14].
* [cite_start]Clone and adapt an open-source repository as a starting point, such as ResumeLM[cite: 15].

### 2. Resume Data Extraction
* [cite_start]Implement a component to convert user CVs from PDF/Word to structured text (or JSON)[cite: 17].
* [cite_start]Use the LLM to extract key resume information: personal details, education, work history, skills, achievements, and projects[cite: 18].
* [cite_start]**Typical Prompt:** "Extract the following fields from this resume: name, contact, education, experience, skills, achievements." [cite: 19]

### 3. Job Description Parsing
* [cite_start]Accept user-provided job descriptions (copy-pasted or scraped text)[cite: 21].
* [cite_start]Use the LLM to extract requirements, responsibilities, and keywords from the job posting[cite: 22].
* [cite_start]Store this as a structured object (JSON) for downstream use[cite: 23].

### 4. Resume Tailoring and Generation
* [cite_start]Summarize or reorganize the candidate's experience to align with job requirements using prompt engineering[cite: 25].
* **Generation Process:**
    * [cite_start]**Step 1:** LLM reviews extracted user info and target job keywords[cite: 27].
    * [cite_start]**Step 2:** LLM synthesizes or rewrites sections, ensuring personalized and keyword-rich content[cite: 28].
* [cite_start]Output a ready-to-use DOCX or PDF using template engines and document conversion tools (e.g., Pandoc)[cite: 29].

### 5. User Review and Iterative Revision
* [cite_start]Allow the user to edit generated content, then use the LLM to refine sections as needed (especially for missing keywords or achievements)[cite: 31].
* [cite_start]Provide real-time feedback on ATS compatibility and keyword optimization[cite: 32].