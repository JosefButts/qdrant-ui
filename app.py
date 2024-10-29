import os
from typing import Any, Dict, List

import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient


def initialize_session_state():
    """Initialize session state variables for API keys and URLs with environment defaults."""
    # Get environment variables
    env_openai_key = os.getenv("OPENAI_API_KEY", "")
    env_qdrant_url = os.getenv("QDRANT_URL", "")
    env_qdrant_key = os.getenv("QDRANT_KEY", "")
    
    # Initialize session state with environment variables
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = env_openai_key
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

def create_sidebar():
    """Create sidebar for API configuration with environment variable defaults."""
    with st.sidebar:
        st.header("Configuration Settings")
        
        # Create expander for API settings
        with st.expander("API Configuration", expanded=False):
            # Embedding type selector
            st.session_state.embedding_type = st.radio(
                "Embedding Type",
                options=['openai', 'fastembed'],
                index=0 if st.session_state.embedding_type == 'openai' else 1,
                help="Select embedding provider"
            )
            
            # Toggle for using environment variables
            st.session_state.using_env_vars = st.checkbox(
                "Use Environment Variables",
                value=st.session_state.using_env_vars,
                help="Toggle between environment variables and custom settings"
            )
            
            if st.session_state.using_env_vars:
                # Display current environment variable values
                st.info("Using environment variables")
                st.write("Environment Variables Status:")
                if st.session_state.embedding_type == 'openai':
                    st.write("- OpenAI API Key:", "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Not Set")
                st.write("- Qdrant URL:", "✅ Set" if os.getenv("QDRANT_URL") else "❌ Not Set")
                st.write("- Qdrant API Key:", "✅ Set" if os.getenv("QDRANT_KEY") else "❌ Not Set")
                
                # Reset to environment variables
                st.session_state.qdrant_url = os.getenv("QDRANT_URL", "")
                st.session_state.qdrant_api_key = os.getenv("QDRANT_KEY", "")
                if st.session_state.embedding_type == 'openai':
                    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
            else:
                # Custom configuration inputs
                if st.session_state.embedding_type == 'openai':
                    openai_key = st.text_input(
                        "OpenAI API Key",
                        value=st.session_state.openai_api_key,
                        type="password",
                        help="Enter your OpenAI API key"
                    )
                    if openai_key:
                        st.session_state.openai_api_key = openai_key
                
                qdrant_url = st.text_input(
                    "Qdrant URL",
                    value=st.session_state.qdrant_url,
                    help="Enter your Qdrant server URL"
                )
                if qdrant_url:
                    st.session_state.qdrant_url = qdrant_url
                
                qdrant_key = st.text_input(
                    "Qdrant API Key",
                    value=st.session_state.qdrant_api_key,
                    type="password",
                    help="Enter your Qdrant API key"
                )
                if qdrant_key:
                    st.session_state.qdrant_api_key = qdrant_key
                
                # Save button (only shown when using custom settings)
                if st.button("Save Configuration"):
                    st.success("Custom configuration saved successfully!")
        
        # Show current active configuration
        st.write("Active Configuration:")
        st.write("Using:", "Environment Variables" if st.session_state.using_env_vars else "Custom Settings")
        st.write("Embedding Provider:", st.session_state.embedding_type.upper())
        if st.session_state.embedding_type == 'openai':
            st.write("- OpenAI API Key:", "✅ Set" if st.session_state.openai_api_key else "❌ Not Set")
        st.write("- Qdrant URL:", "✅ Set" if st.session_state.qdrant_url else "❌ Not Set")
        st.write("- Qdrant API Key:", "✅ Set" if st.session_state.qdrant_api_key else "❌ Not Set")

def get_embeddings(query: str):
    """Get embeddings based on selected provider."""
    if st.session_state.embedding_type == 'openai':
        embedding = OpenAIEmbeddings(api_key=st.session_state.openai_api_key)
        return embedding.embed_query(query)
    else:
        # Use Qdrant's built-in FastEmbed
        return {
            "name": "fastembed",
            "query": query
        }
    
def create_filter_condition(
    filter_type: str, key: str, operator: str, value: Any
) -> Dict:
    """Create a filter condition based on the operator type."""
    if operator == "match":
        return {"key": key, "match": {"value": value}}
    elif operator == "range":
        return {"key": key, "range": value}
    elif operator == "geo_radius":
        return {"key": key, "geo_radius": value}
    elif operator == "values_count":
        return {"key": key, "values_count": value}
    return None


def create_filter_interface(metadata_keys: List[str]) -> Dict[str, List[Dict]]:
    """Create a comprehensive filter interface for Qdrant queries."""

    # Initialize session state for different filter types
    if "must_filters" not in st.session_state:
        st.session_state.must_filters = []
    if "must_not_filters" not in st.session_state:
        st.session_state.must_not_filters = []
    if "should_filters" not in st.session_state:
        st.session_state.should_filters = []

    # Create columns for filter type buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Must Filter"):
            st.session_state.must_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )
    with col2:
        if st.button("Add Must Not Filter"):
            st.session_state.must_not_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )
    with col3:
        if st.button("Add Should Filter"):
            st.session_state.should_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )

    filter_clause = {"must": [], "must_not": [], "should": []}

    # Create UI for Must filters
    if st.session_state.must_filters:
        st.subheader("Must Filters")
        for i, filter_item in enumerate(st.session_state.must_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"must_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"must_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"must_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"must_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"must_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"must_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"must_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_must_{i}"):
                        st.session_state.must_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition("must", key, operator, value)
                if filter_condition:
                    filter_clause["must"].append(filter_condition)

    # Create UI for Must Not filters
    if st.session_state.must_not_filters:
        st.subheader("Must Not Filters")
        for i, filter_item in enumerate(st.session_state.must_not_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"must_not_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"must_not_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"must_not_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"must_not_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"must_not_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"must_not_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"must_not_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_must_not_{i}"):
                        st.session_state.must_not_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition(
                    "must_not", key, operator, value
                )
                if filter_condition:
                    filter_clause["must_not"].append(filter_condition)

    # Create UI for Should filters
    if st.session_state.should_filters:
        st.subheader("Should Filters")
        for i, filter_item in enumerate(st.session_state.should_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"should_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"should_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"should_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"should_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"should_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"should_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"should_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_should_{i}"):
                        st.session_state.should_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition(
                    "should", key, operator, value
                )
                if filter_condition:
                    filter_clause["should"].append(filter_condition)

    # Display current filter structure
    if any([filter_clause["must"], filter_clause["must_not"], filter_clause["should"]]):
        st.subheader("Current Filter Structure")
        st.json(filter_clause)

    return filter_clause

def main():
    initialize_session_state()
    create_sidebar()
    st.title("Advanced Qdrant Query with Filters")

    client = QdrantClient(url=st.session_state.qdrant_url, api_key=st.session_state.qdrant_api_key)
    
    query = st.text_input("Enter your query:")
    limit = st.number_input("Limit", min_value=1, max_value=20, value=5)

    # Get collections
    collections = client.get_collections()
    collection_names = [collection.name for collection in collections.collections]
    collection_name = st.selectbox("Select Collection", collection_names)

    # Get metadata keys from collection
    record, pointId = client.scroll(collection_name=collection_name, limit=1)
    metadata_keys = list(record[0].payload.keys())

    # Create filter interface
    filter_clause = create_filter_interface(metadata_keys)

    # Query button and results
    if st.button("Query Qdrant"):
        try:
            if st.session_state.embedding_type == 'openai':
                # OpenAI embedding
                query_embedding = get_embeddings(query)
                results = client.search(
                    collection_name=collection_name,
                    query_vector=query_embedding,
                    limit=limit,
                    query_filter=filter_clause,
                )
            else:
                # FastEmbed
                results = client.search(
                    collection_name=collection_name,
                    query_text=query,  # Send raw text for server-side embedding
                    limit=limit,
                    query_filter=filter_clause,
                    append_payload=True,  # Make sure we get payloads back
                )

            if not results:
                st.write("No results found")

            for i, hit in enumerate(results):
                with st.expander(f"Result {i+1}", expanded=True):
                    # extract keys from hit.payload
                    keys = list(hit.payload.keys())
                    payload_dict = {key: hit.payload.get(key, "N/A") for key in keys}
                    
                    st.json(payload_dict)
                    
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
            if st.session_state.embedding_type == 'fastembed':
                st.info("Note: Make sure FastEmbed is properly configured on your Qdrant server")

if __name__ == "__main__":
    main()