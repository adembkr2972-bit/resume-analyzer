import re


def parse_resume(text):

    sections = {
        "header": "",
        "summary": "",
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "languages": "",
        "certifications": ""
    }

    current = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        if "professional summary" in lower:
            current = "summary"
            continue

        elif "experience" in lower:
            current = "experience"
            continue

        elif "education" in lower:
            current = "education"
            continue

        elif "skills" in lower:
            current = "skills"
            continue

        elif "projects" in lower:
            current = "projects"
            continue

        elif "languages" in lower:
            current = "languages"
            continue

        elif "certifications" in lower:
            current = "certifications"
            continue

        if current:

            sections[current] += line + "\n"

    return sections