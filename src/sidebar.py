# session.py
import os
import streamlit as st


def create_sidebar():
    """Create sidebar for API configuration with environment variable defaults."""
    with st.sidebar:
        st.header("Configuration Settings")

        # Create expander for API settings
        with st.expander("API Configuration", expanded=False):
            # Embedding type selector
            st.session_state.embedding_type = st.radio(
                "Embedding Type",
                options=["openai", "azure"],  # 'fastembed' not totally enabled yet
                index=0 if st.session_state.embedding_type == "openai" else 1,
                help="Select embedding provider",
            )

            # Toggle for using environment variables
            st.session_state.using_env_vars = st.checkbox(
                "Use Environment Variables",
                value=st.session_state.using_env_vars,
                help="Toggle between environment variables and custom settings",
            )

            if st.session_state.using_env_vars:
                # Display current environment variable values
                st.info("Using environment variables")
                st.write("Environment Variables Status:")
                if st.session_state.embedding_type == "openai":
                    st.write(
                        "- OpenAI API Key:",
                        "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Not Set",
                    )
                if st.session_state.embedding_type == "azure":
                    st.write(
                        "- Azure API Key:",
                        "✅ Set" if os.getenv("AZURE_API_KEY") else "❌ Not Set",
                    )
                st.write(
                    "- Qdrant URL:",
                    "✅ Set" if os.getenv("QDRANT_URL") else "❌ Not Set",
                )
                st.write(
                    "- Qdrant API Key:",
                    "✅ Set" if os.getenv("QDRANT_KEY") else "❌ Not Set",
                )

                # Reset to environment variables
                st.session_state.qdrant_url = os.getenv("QDRANT_URL", "")
                st.session_state.qdrant_api_key = os.getenv("QDRANT_KEY", "")
                if st.session_state.embedding_type == "openai":
                    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
            else:
                # Custom configuration inputs
                if st.session_state.embedding_type == "openai":
                    openai_key = st.text_input(
                        "OpenAI API Key",
                        value=st.session_state.openai_api_key,
                        type="password",
                        help="Enter your OpenAI API key",
                    )
                    if openai_key:
                        st.session_state.openai_api_key = openai_key
                elif st.session_state.embedding_type == "azure":
                    azure_key = st.text_input(
                        "Azure API Key",
                        value=st.session_state.azure_api_key,
                        type="password",
                        help="Enter your Azure API key",
                    )
                    if azure_key:
                        st.session_state.azure_api_key = azure_key

                    azure_endpoint = st.text_input(
                        "Azure Endpoint",
                        value=st.session_state.azure_endpoint,
                        help="Enter your Azure API endpoint",
                    )
                    if azure_endpoint:
                        st.session_state.azure_endpoint = azure_endpoint

                    azure_api_version = st.text_input(
                        "Azure API Version",
                        value=st.session_state.azure_api_version,
                        help="Enter your Azure API version",
                    )
                    if azure_api_version:
                        st.session_state.azure_api_version = azure_api_version

                qdrant_url = st.text_input(
                    "Qdrant URL",
                    value=st.session_state.qdrant_url,
                    help="Enter your Qdrant server URL",
                )
                if qdrant_url:
                    st.session_state.qdrant_url = qdrant_url

                qdrant_key = st.text_input(
                    "Qdrant API Key",
                    value=st.session_state.qdrant_api_key,
                    type="password",
                    help="Enter your Qdrant API key",
                )
                if qdrant_key:
                    st.session_state.qdrant_api_key = qdrant_key

                # Save button (only shown when using custom settings)
                if st.button("Save Configuration"):
                    st.success("Custom configuration saved successfully!")

        # Show current active configuration
        st.write("Active Configuration:")
        st.write(
            "Using:",
            (
                "Environment Variables"
                if st.session_state.using_env_vars
                else "Custom Settings"
            ),
        )
        st.write("Embedding Provider:", st.session_state.embedding_type.upper())
        if st.session_state.embedding_type == "openai":
            st.write(
                "- OpenAI API Key:",
                "✅ Set" if st.session_state.openai_api_key else "❌ Not Set",
            )
        st.write(
            "- Qdrant URL:", "✅ Set" if st.session_state.qdrant_url else "❌ Not Set"
        )
        st.write(
            "- Qdrant API Key:",
            "✅ Set" if st.session_state.qdrant_api_key else "❌ Not Set",
        )
