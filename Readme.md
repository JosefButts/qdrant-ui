# Advanced Qdrant Query Interface with Streamlit

This Streamlit application provides an advanced interface for querying a [Qdrant](https://qdrant.tech/) vector database. It allows users to perform semantic searches with optional filters using either OpenAI embeddings with future plans to incorporate Qdrant's built-in FastEmbed model.

## Features

- **Embedding Options**: Choose between OpenAI embeddings for query vectorization.  Qdrant's FastEmbed will be implemented in the near future
- **Environment Variable Support**: Utilize environment variables for API keys and URLs.
- **Dynamic Filter Interface**: Create complex filters (`must`, `must_not`, `should`) based on metadata fields.
- **Collection Management**: Select from available collections in your Qdrant database.
- **Result Exploration**: View and expand search results with payload details.

## Demo

![Demo Screenshot](screenshot.png)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/JosefButts/qdrant-ui.git
   cd qdrant-ui
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Set the following environment variables if you prefer to use them:

- `OPENAI_API_KEY`: Your OpenAI API key (required if using OpenAI embeddings).
- `QDRANT_URL`: The URL of your Qdrant server.
- `QDRANT_KEY`: Your Qdrant API key (if required).

You can set them in your terminal:

```bash
export OPENAI_API_KEY='your-openai-api-key'
export QDRANT_URL='your-qdrant-url'
export QDRANT_KEY='your-qdrant-api-key'
```

### Streamlit Sidebar Configuration

Alternatively, you can enter your API keys and URLs directly in the Streamlit app via the sidebar configuration.

## Usage

1. **Run the Application**

   ```bash
   streamlit run src/app.py
   ```

2. **Configure API Settings**

   - Use the sidebar to select the embedding provider (`OpenAI` or `FastEmbed`).
   - Choose whether to use environment variables or custom settings.
   - Enter your API keys and URLs if not using environment variables.

3. **Query Qdrant**

   - Enter your query text.
   - Select the collection you want to search.
   - Set the result limit.
   - Create filters using the dynamic filter interface:
     - **Must Filters**: Conditions that **must** be met.
     - **Must Not Filters**: Conditions that **must not** be met.
     - **Should Filters**: Conditions that **should** be met (optional).
   - Click on **"Query Qdrant"** to execute the search.

4. **View Results**

   - Expand each result to view the payload and other details.
   - If no results are found, adjust your query or filters.

## Requirements

- Python 3.7 or higher
- Streamlit
- LangChain Community Embeddings
- Qdrant Client
- OpenAI API key (if using OpenAI embeddings)
- Access to a Qdrant server with your data indexed

## Dependencies

All required Python packages are listed in `requirements.txt`.

## Notes


- **Metadata Keys**: The filter interface dynamically loads metadata keys from your selected collection.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the interactive web interface.
- [Qdrant](https://qdrant.tech/) for the vector database and search capabilities.
- [OpenAI](https://openai.com/) for their powerful embedding models.
- [LangChain](https://langchain.com/) for community embeddings support.

## Contact

For any questions or suggestions, please contact [buttsjosef@gmail.com](mailto:buttsjosef@gmail.com).