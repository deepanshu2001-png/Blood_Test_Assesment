import os
from dotenv import load_dotenv
import fitz
from PyPDF2 import PdfReader



from blood_analyst_crew.crew import HealthAdvisorCrew

 
def extract_text_from_pdf(pdf_path, pages_to_extract):
    raw_text = ''
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in pages_to_extract:
            page = reader.pages[page_num - 1]  # Adjust for 0-based index
            content = page.extract_text()
            if content:
                raw_text += content
    return raw_text


def run():

    pdf = 'C:/Users/deepa/Downloads/blood_report.pdf'
    pages_to_extract = [1, 3]
    extracted_text = extract_text_from_pdf(pdf, pages_to_extract)
    print("Extracted Text:", extracted_text)  # Debugging

    inputs = {
        'blood_report_text': extracted_text  # Use the extracted text
    }
    HealthAdvisorCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()