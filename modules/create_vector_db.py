# Install required packages if you haven't already
# pip install langchain-google-genai faiss-cpu langchain-community

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Set your Google API key as environment variable
# export GOOGLE_API_KEY="your-google-api-key"
# or set it in Python:
# os.environ["GOOGLE_API_KEY"] = "your-google-api-key"

# 1. Load PDF documents (one Document per page)
file_path = "your_file.pdf"  # Replace with your PDF file path
loader = PyPDFLoader(file_path)
documents = loader.load()

# 2. Split documents into smaller chunks for better embedding granularity
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)

# 3. Initialize Google Generative AI Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# 4. Create a FAISS vector store from the split documents and embeddings
vector_store = FAISS.from_documents(split_docs, embeddings)

# Save the FAISS index locally for later use
vector_store.save_local("faiss_index")

# To load the index later:
# vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
