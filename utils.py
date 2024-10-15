import requests
import PyPDF2
import io
from dotenv import load_dotenv
import os
import google.generativeai as genai


# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API with the key from environment variables
api = os.environ['API']
genai.configure(api_key=api)

# Define the Gemini model
model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')

def summarize_text_with_gemini(text):
    """
    Function to generate a detailed summary of the given text using the Gemini model.
    Emphasizes the abstract, conclusion, and other key points like applications,
    advantages, disadvantages, technical highlights, future directions, and results.
    """
    # Define the pre-prompt structure for a detailed summary
    preprompt = f"""Prompt: For the below-provided text, give a detailed summary with an emphasis on the abstract and conclusion. Additionally, cover the following key areas:
    
Main Focus of the Paper: Provide a summary of the abstract, highlighting the key contributions and innovations of the research.
Applications: Summarize the real-world applications or potential use cases of the technology or research presented in the paper.
Advantages: Highlight the main benefits and strengths of the proposed solution or technology.
Disadvantages: Summarize any limitations, challenges, or drawbacks mentioned in the paper.
Technical Highlights: Summarize the important methodologies, architectures, or algorithms used.
Future Directions: Provide insights into the future research goals or possible extensions of the work.
Results: Provide a summary of the key results and metrics achieved in the research.
Conclusion: Emphasize the final results achieved, as well as any concluding remarks from the paper.

'{text}'"""
    
    # Generate content using the model
    response = model.generate_content(preprompt)
    story = response.text
    return story 

def extract_text_from_pdf(url):
    """
    Function to download and extract text from a PDF file available at the given URL.
    """
    try:
        # Step 1: Download the PDF file
        response = requests.get(url)
        if response.status_code == 200:
            # Step 2: Read the PDF from the downloaded content
            pdf_file = io.BytesIO(response.content)
            reader = PyPDF2.PdfReader(pdf_file)
            
            # Step 3: Extract text from all pages of the PDF
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            
            # Return the extracted text
            return text
        else:
            print("Failed to download the PDF file. Please check the URL.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

