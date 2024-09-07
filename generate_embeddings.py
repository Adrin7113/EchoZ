import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Directory to check for uploaded files
uploaded_files_dir = './uploaded_files'

# Get list of PDF files in the directory
pdf_files = [f for f in os.listdir(uploaded_files_dir) if f.endswith('.pdf')]

# Initialize loaders only if there are PDF files
loaders = [PyPDFLoader(os.path.join(uploaded_files_dir, pdf_file))
           for pdf_file in pdf_files]

docs = []

if loaders:
    for file in loaders:
        docs.extend(file.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(docs)
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

    vectorstore = Chroma.from_documents(
        docs, embedding_function, persist_directory="./chroma_db_nccn")

    print(vectorstore._collection.count())
else:
    print("No PDF files found in the uploaded_files directory.")
