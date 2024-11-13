# import os

# import faiss

# load environment variable - saved project root folder
# import os
# from dotenv import load_dotenv
# env_path = os.path.join(os.path.dirname(__file__), '..' , '..', ".env")
# load_dotenv(dotenv_path = env_path)
# os.environ['AZURE_OPENAI_API_KEY'] = os.getenv('AZURE_OPENAI_API_KEY')
# os.environ['AZURE_OPENAI_ENDPOINT'] = os.getenv('AZURE_OPENAI_ENDPOINT')

os.environ["AZURE_OPENAI_API_KEY"] = "1b31fc4eb58c4879960c46f697d72af6"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://genai-openai-quantifai.openai.azure.com/"


from langchain_openai import AzureOpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from bs4 import BeautifulSoup
import glob
from langchain_core.documents import Document

import faiss
from langchain.document_loaders import PyPDFLoader
from langchain_community.docstore.in_memory import InMemoryDocstore

import pathlib

#########################################################################
### env

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large"
)

global sec_filling_db
global research_db
global news_db
global test


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Get text
    text = soup.get_text(separator='\n')
    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def html_load(html_file):

    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    text_content = extract_text_from_html(html_content)
    docs = [
            Document(
                metadata={"source": html_file},
                page_content=text_content,
            )
    ]
    return docs


def create_vector_database(file_path: str, format: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    FAISS_mr = FAISS_manager(embedding=embeddings)

    files_list = glob.glob(f"{file_path}/*.{format}")
    for file in files_list:
        if format == 'pdf':
            loader=PyPDFLoader(file)
            docs=loader.load()
        elif format == 'html':
            docs = html_load(file)
        else:
            raise ValueError(f"format: {format} not supported, now only supports 'pdf' and 'html'")

        documents = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, separators=["\n","\n\n"], chunk_overlap=chunk_overlap
        ).split_documents(docs)

        FAISS_mr.add_documents(documents=documents)

    return FAISS_mr


def initialize_vector_store(file_mapping: dict):
    global sec_filling_db
    global research_db
    global news_db

    cwd = pathlib.Path.cwd()
    faiss_db_path = f"{cwd}/../../faiss-db/"

    if file_mapping:
        sec_filling_db = create_vector_database(file_mapping['sec_filling'], format='pdf')
        research_db = create_vector_database(file_mapping['research_report'], format='pdf')
        news_db = create_vector_database(file_mapping['news'], format='html')

        # save the files
        sec_filling_db.save_local( faiss_db_path + "sec_filling_db")
        research_db.save_local( faiss_db_path + "research_report_db" )
        news_db.save_local(faiss_db_path + "news_db")

    else:
        sec_filling_db = FAISS_manager(embedding=embeddings)
        research_db = FAISS_manager(embedding=embeddings)
        news_db = FAISS_manager(embedding=embeddings)

        sec_filling_db.load_local(faiss_db_path + "sec_filling_db", embeddings=embeddings)
        research_db.load_local(faiss_db_path + "research_report_db", embeddings=embeddings)
        news_db.load_local(faiss_db_path + "news_db", embeddings=embeddings)


# TODO: add the fuctionality of adding or deleting files from db
# thinking about add some process of selecting data files, summary then rag?

# a lazy implementation to accommodate langchain use
class FAISS_manager:
    def __init__(self, embedding):
        # initial index from the embedding
        index = faiss.IndexFlatL2(len(embedding.embed_query("hello world")))
        self.vector_store = FAISS(
            embedding_function=embedding,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

    def add_documents(self, documents: [Document]):
        self.vector_store.add_documents(documents=documents)


    def search(self, query, top_k):
        retriever = self.vector_store.as_retriever()
        result = retriever.get_relevant_documents(query)
        return result[:top_k]


    def save_local(self, dir):
        self.vector_store.save_local(dir)


    def load_local(self, dir, embeddings):
        self.vector_store = FAISS.load_local(dir, embeddings=embeddings, allow_dangerous_deserialization=True)

