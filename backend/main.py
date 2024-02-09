import json
from fastapi import FastAPI, File, UploadFile
from typing import Union, Optional, List, Dict
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
import tempfile
from extractor import DataExtractor

client = OpenAI(api_key="your api key here")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List of allowed origins (React app URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryItem(BaseModel):
    message: str



class Messages:
    def __init__(self):
        self.memory: list = []

    def add_message(self, role:str, msg:QueryItem):
        self.memory.append({role:msg.message})
    
    def delete_last_message(self):
        if self.memory:
            self.memory.pop()
        else:
            raise IndexError("No message to delete.")
    
    def reset_messages(self):
        self.memory = []


def read_single_pdf(upload_file):
    output = []
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Save uploaded file to a temporary file
            content = upload_file.read()  
            temp_file.write(content)
            temp_file_path = temp_file.name  
            pdf_reader = PdfReader(temp_file_path)
            num_pages = len(pdf_reader.pages)
            for i in range(num_pages):
                page = pdf_reader.pages[i]
                output.append(page.extract_text())

    except Exception as e:
        print("Error reading file")
    return str(" ".join(output))


def get_completion_from_openai(query: str):
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ])
    response = completion.choices[0].message.content
    return response
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
def read_item(query: QueryItem):
    print(query.message)
    response: QueryItem = get_completion_from_openai(query.message)
    return {"response":response}

@app.post("/resume_process/")
async def resume_pdf_to_text(file: UploadFile = File(...)):
    data = read_single_pdf(file.file)
    phone_number = DataExtractor(data).extract_phone_numbers()
    email = DataExtractor(data).extract_emails()
    links = DataExtractor(data).extract_links()
    # links_ext = DataExtractor(data).extract_links_extended()
    names = DataExtractor(data).extract_names()
    entities = DataExtractor(data).extract_entities()
    exprience = DataExtractor(data).extract_experience()
    return {"parsed_resume": [names[0],email,phone_number]}
