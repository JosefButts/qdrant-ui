# embeddings.py

import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings


def get_embeddings(query: str):
    """Get embeddings based on selected provider."""
    if st.session_state.embedding_type == "openai":
        embedding = OpenAIEmbeddings(api_key=st.session_state.openai_api_key)
        return embedding.embed_query(query)
    else:
        # Use Qdrant's built-in FastEmbed
        return {"name": "fastembed", "query": query}
