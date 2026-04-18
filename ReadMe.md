# CV Creation using LLMs

---

## Objective
Design and develop a capstone project on "CV Creation using LLMs" to showcase how modern open-source models can automate the creation of CV from information provided by user or some documents.

---

## Required Models
* **Gemma 3 1B via Ollama:** Lightweight, open-source LLM ideal for local, privacy-centric deployment that efficiently handles resume tailoring and document generation tasks.
* **Llama 2 or LlamaIndex:** Versatile frameworks for LLM-based document applications, enabling easy integration and information extraction.
* **ResumeLM:** An open-source AI-powered resume builder that is tailored for ATS-optimized CVs using open models, and supports local setup for privacy.
* **LangChain:** Useful for orchestrating different LLM pipeline stages from extraction to evaluation across various models.

---

## Step by Step Instructions

### 1. Project Setup
* Select an open-source LLM (e.g., Gemma via Ollama or LlamaIndex).
* Set up a local environment with required dependencies: Python, relevant LLM backends (Ollama, Transformers), and document parsing libraries (e.g., pdfplumber for PDF extraction).
* Clone and adapt an open-source repository as a starting point, such as ResumeLM.

### 2. Resume Data Extraction
* Implement a component to convert user CVs from PDF/Word to structured text (or JSON).
* Use the LLM to extract key resume information: personal details, education, work history, skills, achievements, and projects.
* **Typical Prompt:** "Extract the following fields from this resume: name, contact, education, experience, skills, achievements."

### 3. Job Description Parsing
* Accept user-provided job descriptions (copy-pasted or scraped text).
* Use the LLM to extract requirements, responsibilities, and keywords from the job posting.
* Store this as a structured object (JSON) for downstream use.

### 4. Resume Tailoring and Generation
* Summarize or reorganize the candidate's experience to align with job requirements using prompt engineering.
* **Generation Process:**
    * **Step 1:** LLM reviews extracted user info and target job keywords.
    * **Step 2:** LLM synthesizes or rewrites sections, ensuring personalized and keyword-rich content.
* Output a ready-to-use DOCX or PDF using template engines and document conversion tools (e.g., Pandoc).

### 5. User Review and Iterative Revision
* Allow the user to edit generated content, then use the LLM to refine sections as needed (especially for missing keywords or achievements).
* Provide real-time feedback on ATS compatibility and keyword optimization.
