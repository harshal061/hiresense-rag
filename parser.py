import pdfplumber
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text
def clean_text(text):
    # lowercase
    text = text.lower()
    
    # remove extra spaces
    text = " ".join(text.split())
    
    return text