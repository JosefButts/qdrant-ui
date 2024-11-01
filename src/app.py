# app.py

import streamlit as st
from qdrant_client import QdrantClient

from session import initialize_session_state
from sidebar import create_sidebar
from embeddings import get_embeddings
from filters import create_filter_interface
from display_results import display_results_table
import pandas as pd

def main():
    initialize_session_state()
    create_sidebar()
    st.title("Advanced Qdrant Query with Filters")

    client = QdrantClient(
        url=st.session_state.qdrant_url, api_key=st.session_state.qdrant_api_key
    )

    query = st.text_input("Enter your query:")
    limit = st.number_input("Limit", min_value=1, max_value=30, value=5)
    # make score threshold optional
    score_threshold = st.number_input("Score Threshold", min_value=0.0, max_value=1.0, value=0.0)

    # Get collections
    try:
        collections = client.get_collections()
    except Exception as e:
        st.error(f"Error getting collections: {str(e)}")
        return
    
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
            if st.session_state.embedding_type == "openai":
                # OpenAI embedding
                query_embedding = get_embeddings(query)
                results = client.search(
                    collection_name=collection_name,
                    query_vector=query_embedding,
                    limit=limit,
                    query_filter=filter_clause,
                    score_threshold=score_threshold,
                )
            else:
                # FastEmbed
                results = client.search(
                    collection_name=collection_name,
                    query_text=query,
                    limit=limit,
                    query_filter=filter_clause,
                    append_payload=True,
                )
              
            # if 'results' in locals() or 'results' in globals():
            #     display_results_table(results)
            # else:
            #     st.error("No results data found")
            
            if not results:
                st.write("No results found")
            formatted_results = []
            for i, hit in enumerate(results):
                with st.expander(f"Result {i+1}", expanded=True):
                    payload_dict = {
                        key: hit.payload.get(key, "N/A") for key in hit.payload.keys()
                    }
                    payload_dict["score"] = hit.score
                    formatted_results.append(payload_dict)
                    st.json(payload_dict)
                    
            with st.expander(f"Result {i+1}", expanded=True):

                df = pd.DataFrame(formatted_results)
                st.dataframe(df)
                
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
            if st.session_state.embedding_type == "fastembed":
                st.info(
                    "Note: Make sure FastEmbed is properly configured on your Qdrant server"
                )


if __name__ == "__main__":
    main()
