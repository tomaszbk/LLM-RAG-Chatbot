def test_pdf_reader():
    from pypdf import PdfReader

    file = "tests/pdf_test.pdf"
    with open(file, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    print(text)
