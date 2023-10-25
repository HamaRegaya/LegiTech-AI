from flask import Flask, render_template, request, jsonify ,send_from_directory
import fitz

import openai
from nltk.tokenize import sent_tokenize
from io import StringIO
import json
import time
from array import array
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
import os
import openai
from dotenv import load_dotenv
import base64
load_dotenv()
from io import BytesIO
openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = "a41984e997a74b999e979b08007ec70a"

ENDPOINT = "https://francecentral.api.cognitive.microsoft.com/"
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/back")
def back():
    return render_template("index_back.html")

@app.route("/Writinglawyer")
def Writinglawyer():
    return render_template("Writinglawyer.html")

@app.route("/generate_text", methods=["POST"])
def generate_text():
    try:
        image = request.files["image"]
        if image:
            img_stream = BytesIO(image.read()) # Read the uploaded file as bytes
            img_data = base64.b64encode(img_stream.getvalue()).decode('utf-8')
            read_response = computervision_client.read_in_stream(img_stream, language='en', raw=True)
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            if read_result.status == OperationStatusCodes.succeeded:
                extracted_text = ''  # Create a variable to store the extracted text
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        extracted_text += line.text + ' '
            # You can return the extracted text and any other data you want to the template
            return render_template("Writinglawyer.html", generated_text=extracted_text,imgg=img_data)

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/correct_text", methods=["POST"])
def correct_text():
    user_input = request.form["user_input"]
    text="test"

    # Use the user_input as input for ChatGPT
    messages = [
    {
        "role": "user",
        "content": user_input
    },
    {
        "role": "assistant",
        "content": "You will be provied with lawyers students essay and  give them feedback and a grade. Please use this format for feedback:\n\nGrade: [Your grade, like A, B, or C]\nStrengths: [Highlight what you did really well, such as how you structured your paragraph, used Critical Thinking,Originality and Plagiarism and Proper Grammar and Style]\nAreas for Improvement: [Tell us where you think you can make it even better]\n\n"
    }
]


    try:
        # Make the OpenAI chat completion request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        assistant_reply = response.choices[0].message["content"]
        print(assistant_reply)

        # Split the response into lines
        lines = assistant_reply.split('\n')

        # Initialize variables to store the grade, strengths, and areas for improvement
        grade = ""
        strengths = ""
        areas_for_improvement = ""

        current_section = None

                # Iterate through the lines to categorize them into grade, strengths, and areas for improvement
        for line in lines:
                if line.startswith("Grade:"):
                    current_section = "Grade"
                    grade += line + '\n'
                elif line.startswith("Strengths:"):
                    current_section = "Strengths"
                    strength_points = line.split("\n")
                    strengths += '\n'.join(point.strip() for point in strength_points if point.strip()) + '\n'
                elif line.startswith("Areas for Improvement:"):
                    current_section = "Areas for Improvement"
                    improvement_points = line.split("\n")
                    areas_for_improvement += '\n'.join(point.strip() for point in improvement_points if point.strip()) + '\n'
                else:
                    if current_section == "Grade":
                        grade += line + '\n'
                    elif current_section == "Strengths":
                        strengths += line + '\n'
                    elif current_section == "Areas for Improvement":
                        areas_for_improvement += line + '\n'
        pros = strengths
        cons=areas_for_improvement  # Replace with the actual areas for improvement

    except Exception as e:
        return f"Error generating assistant reply: {str(e)}"






    # Render the HTML template with the variables
    return render_template("Writinglawyer.html", grade=grade, pros=pros, cons=cons, user_input=user_input,text=text)

def read_pdf(filename):
    context = ''
  
    # Open the PDF file
    with fitz.open(filename) as pdf_file:
    
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count
        
        # Loop through each page in the PDF file
        for page_num in range(num_pages):
          
            # Get the current page
            page = pdf_file[page_num]
          
            # Get the text from the current page
            page_text = page.get_text()
          
            # Append the text to context
            context += page_text
    return context

@app.route("/chat")
def chatv1():
    return render_template('chat.html')


document = None  # Initialize the global variable

@app.route("/get", methods=["GET", "POST"])
def chat():
    global document  # Access the global variable
    msg = request.form["msg"]
    prompt = msg
    
    if document is not None:
        return summarize(document, prompt)
    else:
        return "No document uploaded."

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' in request.files:
        pdf_file = request.files['pdf_file']
        if pdf_file.filename != '':
            # Save the uploaded PDF to a folder
            pdf_path = os.path.join('static', pdf_file.filename)
            pdf_file.save(pdf_path)
            
            # Read the PDF and store its content in the global variable
            global document
            document = read_pdf(pdf_path)
            
            return render_template('chat.html', output=pdf_file.filename)

    return render_template('chat.html', output="No file uploaded")


#########################################




def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = os.getenv("OPENAI_API_KEY")



def split_text(text, chunk_size=5000):
    """
    Splits the given text into chunks of approximately the specified chunk size.
    
    Args:
    text (str): The text to split.
    
    chunk_size (int): The desired size of each chunk (in characters).
    
    Returns:
    List[str]: A list of chunks, each of approximately the specified chunk size.
    """
    
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk.getvalue():
        chunks.append(current_chunk.getvalue())
    return chunks

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.5, top_p=0.3, tokens=1000):
    try:
        response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        top_p=top_p,
        max_tokens=tokens
        )
        return response.choices[0].text.strip()
    except Exception as oops:
        return "GPT-3 error: %s" % oops

def summarize(document,prompt):
    # Calling the split function to split text
    chunks = split_text(document)
  
    summaries = []
    for chunk in chunks:
        # prompt = 'Please what are the  Services in the following document: \n'
        summary = gpt3_completion(prompt + chunk)

        if summary.startswith('GPT-3 error:'):
            continue

        summaries.append(summary)
    return '\n'.join(summaries)

# Read the PDF file


# # Call the summarize function with the document as input
# result = summarize(document)
# print(result)  # Print or use the result as needed



if __name__ == '__main__':
    app.run(debug=True)
