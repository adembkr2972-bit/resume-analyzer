from docx import Document
from docx.shared import Pt
from services.resume_parser import parse_resume


def create_resume_doc(text):

    data = parse_resume(text)

    doc = Document()

    title = doc.add_heading("Professional Resume", 0)
    title.style.font.size = Pt(24)

    def add_section(title, content):

        if content.strip():

            doc.add_heading(title, level=1)

            for line in content.split("\n"):

                if line.strip():

                    doc.add_paragraph(
                        line,
                        style="List Bullet"
                    )

    add_section(
        "Professional Summary",
        data["summary"]
    )

    add_section(
        "Experience",
        data["experience"]
    )

    add_section(
        "Education",
        data["education"]
    )

    add_section(
        "Skills",
        data["skills"]
    )

    add_section(
        "Projects",
        data["projects"]
    )

    add_section(
        "Languages",
        data["languages"]
    )

    add_section(
        "Certifications",
        data["certifications"]
    )

    path = "generated/Optimized_Resume.docx"

    doc.save(path)

    return path