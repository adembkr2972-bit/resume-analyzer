from docx import Document


def create_cover_letter(letter):

    document = Document()

    document.add_heading(
        "Cover Letter",
        level=1
    )

    document.add_paragraph(letter)

    path = "generated/cover_letter.docx"

    document.save(path)

    return path