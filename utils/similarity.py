import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings


# Wrapper so LangChain accepts local embeddings
class LocalEmbedding(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()


def clean_text(text):
    return text.replace("\n", " ").replace("\t", " ")[:5000]


def chunk(text, size=1000):
    text = clean_text(text)
    return [text[i:i + size] for i in range(0, len(text), size)]


def build_vector_db(jd_text, resumes):
    embedding = LocalEmbedding()

    texts = []
    metadata = []

    # JD chunks
    for c in chunk(jd_text):
        texts.append(c)
        metadata.append({"source": "Job Description"})

    # Resume chunks
    for r in resumes:
        for c in chunk(r["text"]):
            texts.append(c)
            metadata.append({"source": r["filename"]})

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadata
    )

    return vectorstore


def similarity_score(vectorstore, resume_text):
    """We return fixed similarity because Gemini ranking will be used."""
    return 1.0
