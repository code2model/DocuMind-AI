import os
from typing import Dict, List, Optional

import fitz
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI


load_dotenv()

qna_system_message = (
    "You will be provided with a text, and your task is to answer the question based on "
    "the text alone. If you are unable to answer or doubtful, please say \"I dont know\""
)

qna_user_message_template = """
###Context
Here are some documents that are relevant to the question mentioned below.
{context}

###Question
{question}
"""


def read_pdf_fitz(file_path: Optional[str] = None, file_bytes: Optional[bytes] = None) -> str:
    if not file_path and not file_bytes:
        raise ValueError("Provide either file_path or file_bytes")

    if file_bytes:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    else:
        doc = fitz.open(file_path)

    text_parts: List[str] = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts)


def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    if not text.strip():
        return []

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start = max(0, end - overlap)

    return chunks


def build_retriever_from_pdf(file_bytes: bytes, k: int = 3):
    text = read_pdf_fitz(file_bytes=file_bytes)
    texts = _chunk_text(text)
    if not texts:
        raise ValueError("Could not extract readable text from the PDF")

    embeddings = OpenAIEmbeddings()
    vectorstore = InMemoryVectorStore.from_texts(texts=texts, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})


def _build_augmented_context(retrieved_documents: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in retrieved_documents if doc.page_content)


def generate_answer(
    query: str,
    chat_history: List[Dict[str, str]],
    use_rag: bool = False,
    retriever=None,
) -> str:
    if not use_rag:
        return (
            "RAG is currently OFF. You asked: "
            f"\n\n> {query}\n\n"
            "Turn on 'Use RAG pipeline' in the sidebar after you upload a PDF."
        )

    if retriever is None:
        return "Please upload a PDF and build the retriever first."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is missing. Add it to your .env file and restart the app."

    retrieved_documents = retriever.invoke(query)
    augmented_search_context = _build_augmented_context(retrieved_documents)
    if not augmented_search_context.strip():
        return "I dont know"

    history_lines = [
        f"{message.get('role', 'user')}: {message.get('content', '')}"
        for message in chat_history[-6:]
        if message.get("content")
    ]
    history_text = "\n".join(history_lines)
    question_with_history = query if not history_text else f"{query}\n\nConversation:\n{history_text}"

    prompt = [
        {"role": "system", "content": qna_system_message},
        {
            "role": "user",
            "content": qna_user_message_template.format(
                context=augmented_search_context,
                question=question_with_history,
            ),
        },
    ]

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=prompt,
        temperature=0,
    )
    prediction = response.choices[0].message.content
    return prediction.strip() if prediction else "I dont know"
