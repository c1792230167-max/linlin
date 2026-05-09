import os
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DATA_DIR = "data"
PERSIST_DIR = "./chroma_db"


def load_documents():
    docs = []

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                loader = TextLoader(path, encoding="utf-8")
                loaded_docs = loader.load()

                for d in loaded_docs:
                    d.metadata["source"] = path

                docs.extend(loaded_docs)

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def main():
    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )

    vectorstore.persist()

    print("Vector DB created successfully")


if __name__ == "__main__":
    main()
