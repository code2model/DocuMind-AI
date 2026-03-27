<div align="center">
  <h1> DocuMind AI</h1>
  <p><b>Intelligent Document Explorer</b> powered by Retrieval-Augmented Generation.</p>
  <p><i>Developed and Maintained by <b>code2model</b></i></p>

  <!-- Badges -->
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://www.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/></a>
  <a href="https://openai.com/"><img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/></a>
</div>

<br/>

##  Overview

This modern Streamlit application implements a seamless, highly-responsive RAG (Retrieval-Augmented Generation) flow for "chatting" with your PDF documents. The application has been meticulously upgraded for maximum performance, aesthetic appeal, and developer experience by **code2model**.

### ✨ Key Upgrades & Features

-  **Modern UI / UX:** Beautiful glassmorphism sidebar, gradient typography, and customized interactive buttons.
-  **Model Upgrade:** Upgraded default chat completions to use OpenAI's latest architecture, robustly falling back to `gpt-4o-mini` for fast and cost-effective generations.
-  **Efficient PDF Extraction:** Native processing directly from binary streams using PyMuPDF (`fitz`).
-  **Memory Vector Storage:** High-speed, dependency-light embedding storage using LangChain `InMemoryVectorStore`.
-  **Session Chat History:** Context-aware conversations leveraging `st.chat_message` and `st.chat_input`.

## 📂 Project Structure

- `documind_app.py` - Main Streamlit UI, aesthetic configurations, and chat flow.
- `rag_engine.py` - Core RAG Neural Pipeline (PDF extraction, chunking, embeddings, and QA generation).
- `requirements.txt` - Required Python dependencies mapped to stable versions.

## 🛠️ Quick Start

### 1. Environment Setup

It's recommended to create an isolated Python virtual environment.

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Secrets

Create a `.env` file in the project directory root:

```env
OPENAI_API_KEY=your_openai_key_here
# Optional: Override the default gpt-4o-mini model
# OPENAI_MODEL=gpt-4o-mini
```

### 4. Lift Off 

```bash
streamlit run documind_app.py
```

## Architecture Flow

1. **Extraction:** PDF parsed by user upload via `read_pdf_fitz()`.
2. **Chunking & Storage:** Text split into chunks, converted locally using OpenAI Embeddings, and deposited into LangChain's `InMemoryVectorStore`.
3. **Retrieval:** K-th nearest neighbor similarity search returns highest relevance document parts.
4. **Augmentation & Generation:** LLM formulates context-aware answers incorporating chat history state. If insufficient context arises, it elegantly defaults to "I dont know", protecting against hallucinations.

<br/>
<p align="center">Made with ❤️ by <b>code2model</b></p>
