import os

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from utils.pdf_utils import extract_pdf_content
from langchain_community.embeddings import OpenAIEmbeddings
# Initialize the embedding model

load_dotenv()
# Initialize the embedding model
file = r"../ftp_india/FTP2023_Chapter10.pdf"

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

file_text = extract_pdf_content(file)
print(file_text)

vector_db = Chroma(collection_name="pdf_documents", embedding_function=embeddings, persist_directory="chroma_db")

ftp_document = Document(page_content=file_text, metadata={"source": "FTP2023_Chapter10.pdf"})
hsn_code_document = Document(page_content="HSN Code: 93061000 is of Grenade and comes under SCOMET", metadata={"source": "HSN_CODE"})
vector_db.add_documents([hsn_code_document, ftp_document])
# vector_db.persist()
print("Document inserted into Chroma vector database successfully.")
print(vector_db.get()['ids'])