
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def parse_my_resume(text=None):
    # Given the manual details, we can return them directly
    # If text parsing becomes necessary in the future, this function can be expanded
    return {
        'name': 'Daniel Garcia',
        'profession': 'Machine Learning Engineer',
        'location': 'Wallington, NJ',
        'phone': '973.934.7491',
        'email': 'dangarcia31538@gmail.com',
        'linkedin': 'linkedin.com/in/daniel--garcia'
    }

def get_resume_details():
    # For now, we're using the manually provided details
    # Uncomment the below lines if you wish to extract text from a PDF and parse it
    # text = extract_text_from_pdf("path_to_your_pdf.pdf")
    # details = parse_my_resume(text)
    details = parse_my_resume()
    return details

def test_extraction():
    details = get_resume_details()
    for key, value in details.items():
        print(f"{key.capitalize()}: {value}")

if __name__ == "__main__":
    test_extraction()

