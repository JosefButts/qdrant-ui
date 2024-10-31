# session.py

import os
import streamlit as st

def initialize_session_state():
    """Initialize session state variables for API keys and URLs with environment defaults."""
    # Get environment variables
    env_openai_key = os.getenv("OPENAI_API_KEY", "")
    env_qdrant_url = os.getenv("QDRANT_URL", "")
    env_qdrant_key = os.getenv("QDRANT_KEY", "")
 
    env_azure_key = os.getenv("AZURE_API_KEY", "")
    env_azure_endpoint = os.getenv("AZURE_ENDPOINT", "")
    env_azure_api_version = os.getenv("AZURE_API_VERSION", "")

    # Initialize session state with environment variables
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = env_openai_key
    if 'azure_api_key' not in st.session_state:
        st.session_state.azure_api_key = env_azure_key
    if 'azure_endpoint' not in st.session_state:
        st.session_state.azure_endpoint = env_azure_endpoint
    if 'azure_api_version' not in st.session_state:
        st.session_state.azure_api_version = env_azure_api_version
    if 'qdrant_url' not in st.session_state:
        st.session_state.qdrant_url = env_qdrant_url
    if 'qdrant_api_key' not in st.session_state:
        st.session_state.qdrant_api_key = env_qdrant_key
    if 'using_env_vars' not in st.session_state:
        st.session_state.using_env_vars = True
    if 'must_filters' not in st.session_state:
        st.session_state.must_filters = []
    if 'must_not_filters' not in st.session_state:
        st.session_state.must_not_filters = []
    if 'should_filters' not in st.session_state:
        st.session_state.should_filters = []
    if 'embedding_type' not in st.session_state:
        st.session_state.embedding_type = 'openai'
