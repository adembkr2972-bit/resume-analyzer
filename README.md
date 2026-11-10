# Resume Analyzer

> Portfolio README draft based on the local app and service code. Setup has not yet been verified from a clean environment.

This Streamlit prototype accepts a PDF resume and a job description, extracts resume text, and displays structured AI-generated feedback. The interface includes an ATS-style dashboard, strengths and weaknesses, missing-skill and keyword lists, suggested edits, an optimized resume view, cover-letter and interview-question sections, and DOCX downloads.

## Implementation

- Streamlit provides the upload and review interface.
- PyPDF2 extracts text from uploaded PDFs.
- A Pydantic response schema defines the structured analysis fields.
- The API path sends the resume text and job description in a prompt to Google's Gemini service.
- Resume rendering and document-generation helpers produce downloadable documents.

## Privacy and responsible use

Resume files contain personal information. In the API path, extracted resume text and the job description are sent to Gemini. Do not deploy this app for real resumes until the interface explains that data flow, users have an informed choice, and storage/session handling has been reviewed. Never include real resumes, generated resumes, `.env` files, or API keys in this repository.

The current response schema includes a Yes/No `hiring_decision`. That output is not validated as a fair or job-related selection method. It should not be used to make employment decisions; consider removing it from a public demo. Treat all generated scores, edits, skills, and interview suggestions as unverified suggestions for human review.

## Local development

The project includes a `requirements.txt` and a virtual environment, but the dependency list and imported Gemini SDK need to be aligned before publishing setup instructions. A local `.env` exists in the source folder; it was not copied. The staged copy also omits `sample_data/sample_result.json` until it is confirmed synthetic, so the default development-mode analysis will need a safe sample or an adjusted dev path. Use a documented `.env.example` containing variable names only, and load credentials from the user's environment.

Once the clean public copy is reviewed, document the exact commands to create a virtual environment, install dependencies, set `GEMINI_API_KEY`, and launch Streamlit. Confirm whether the default development mode uses only the bundled sample response, and verify that the sample response contains no personal information before including it.

## Review items before publication

- Add a `.gitignore` for virtual environments, `.env`, generated documents, uploaded resumes, and local outputs.
- Confirm and pin the Gemini SDK dependency that matches the `google.genai` import.
- Review `services/ai.py`'s production-mode conditional (`false` should be Python's `False`) and test it without a real API key.
- Replace the network-calling `test_models.py` script with automated tests that do not list live API models or require credentials.
- Add privacy, retention, and third-party AI service disclosures before considering any hosted version.
- Verify that all sample files are synthetic and that no generated DOCX contains personal data.

## License

Choose a license only after confirming the code and all included assets may be shared. Do not include generated resumes or real candidate data as examples.
