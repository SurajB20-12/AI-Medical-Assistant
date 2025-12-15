import os,time 
from pathlib import Path
from dotenv import load_dotenv
import pinecone
from tqdm.auto import tqdm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone,ServerlessSpec
from pydantic import SecretStr

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")

PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="medical-index"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY or ""

#store uploaded doc in directory
UPLOAD_DIR='./uploaded_docs'
os.makedirs(UPLOAD_DIR,exist_ok=True)

#initialize pinecone instance
pc=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(
  cloud="aws",
  region=PINECONE_ENV
)

#check is index exists
existing_indexes= [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
  pc.create_index(
    name=PINECONE_INDEX_NAME,
    dimension=768,
    metric="dotproduct",
    spec=spec

  )
  while True:
        desc = pc.describe_index(PINECONE_INDEX_NAME)
        if desc.status and desc.status.get("ready"):
            break
        time.sleep(1)

index=pc.Index(PINECONE_INDEX_NAME)

def load_vectorstore(uploaded_doc):
  embed_model=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
  file_path=[]

  for file in uploaded_doc:
    path=Path(UPLOAD_DIR)/file.filename
    with open(path,"wb") as f:
      f.write(file.file.read())
    file_path.append(str(path))

  for file_path in file_path:
    loader=PyPDFLoader(file_path)
    documents=loader.load()

    spiltter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks=spiltter.split_documents(documents)

    text=[chunk.page_content for chunk in chunks]
    metadatas=[chunk.metadata for chunk in chunks]

    ids=[f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

    print(f"Embedding {len(text)} chunks")
    embeddings=embed_model.embed_documents(text)

    print("Uploading to Pinecone...") 

    vectors=list(zip(ids,embeddings,metadatas))
    with tqdm(total=len(embeddings),desc="Upserting in pinecone") as progress:
       index.upsert(vectors=vectors)
       progress.update(len(embeddings))

    print(f"Completed uploading vectors for {file_path}")




