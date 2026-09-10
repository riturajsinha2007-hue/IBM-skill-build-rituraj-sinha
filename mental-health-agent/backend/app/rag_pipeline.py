"""
RAG pipeline – document loading, chunking, embedding, and retrieval.

Trusted mental-health knowledge documents are stored under data/knowledge_base/.
At startup the pipeline indexes them into a Chroma vector store.
Agents call retrieve() to get relevant context before prompting Granite.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.config import get_settings

logger = logging.getLogger(__name__)
_settings = get_settings()

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "data" / "knowledge_base"
EMBED_MODEL = "all-MiniLM-L6-v2"


class RAGPipeline:
    """Manages the vector store and exposes a retrieve() method."""

    def __init__(self):
        self._embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        self._vectorstore: Chroma | None = None
        self._initialize()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _initialize(self):
        persist_dir = _settings.chroma_persist_dir

        # If already persisted, load directly
        if Path(persist_dir).exists() and any(Path(persist_dir).iterdir()):
            logger.info("Loading existing Chroma vector store from %s", persist_dir)
            self._vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self._embeddings,
            )
            return

        # Otherwise build from knowledge-base docs
        logger.info("Building vector store from knowledge base at %s", KNOWLEDGE_BASE_DIR)
        documents = self._load_documents()
        if not documents:
            logger.warning("No documents found in knowledge base – RAG disabled.")
            return

        chunks = self._split_documents(documents)
        self._vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self._embeddings,
            persist_directory=persist_dir,
        )
        self._vectorstore.persist()
        logger.info("Vector store built with %d chunks.", len(chunks))

    def _load_documents(self):
        if not KNOWLEDGE_BASE_DIR.exists():
            logger.warning("Knowledge base directory not found: %s", KNOWLEDGE_BASE_DIR)
            return []
        loader = DirectoryLoader(
            str(KNOWLEDGE_BASE_DIR),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        logger.info("Loaded %d raw documents.", len(docs))
        return docs

    @staticmethod
    def _split_documents(documents) -> List:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=80,
            separators=["\n\n", "\n", ".", " "],
        )
        return splitter.split_documents(documents)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, k: int = 4) -> str:
        """Return a formatted string of the top-k relevant chunks."""
        if self._vectorstore is None:
            return ""

        try:
            docs = self._vectorstore.similarity_search(query, k=k)
            if not docs:
                return ""
            context_parts = [
                f"[Source: {doc.metadata.get('source', 'knowledge base')}]\n{doc.page_content}"
                for doc in docs
            ]
            return "\n\n---\n\n".join(context_parts)
        except Exception as exc:
            logger.error("RAG retrieval error: %s", exc)
            return ""


# Singleton
_rag: RAGPipeline | None = None


def get_rag_pipeline() -> RAGPipeline:
    global _rag
    if _rag is None:
        _rag = RAGPipeline()
    return _rag
