import PyPDF2

def extract_text(file):
    """
    Extracts text from a PDF file uploaded via Streamlit.
    Returns raw string content.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text.strip()
    except Exception as e:
        return f"[ERROR extracting text: {e}]"
