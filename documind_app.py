import streamlit as st

from rag_engine import build_retriever_from_pdf, generate_answer

st.set_page_config(page_title="DocuMind AI | code2model", page_icon="✨", layout="wide")

# Custom CSS for a modern, fancy look
CUSTOM_CSS = """
<style>
/* Main background and font styling */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Glassmorphism sidebar */
[data-testid="stSidebar"] {
    background: rgba(30, 34, 45, 0.6);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Gradient Title */
h1 {
    background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    margin-bottom: -15px;
}

/* Improved Toggle */
.stToggle label {
    font-weight: 600;
}

/* Formatted chat input */
[data-testid="stChatInput"] {
    border: 1px solid #4facfe;
    border-radius: 12px;
}

/* Primary Button Styling */
.stButton button {
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 242, 254, 0.4);
}

/* Divider styling */
hr {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
"""

HEADER_HTML = """
<div style='display: flex; align-items: center; margin-bottom: 5px; margin-top: -15px;'>
    <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 15px; filter: drop-shadow(0px 0px 8px rgba(0, 242, 254, 0.6));">
        <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="url(#gradient)"/>
        <path d="M12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18C15.31 18 18 15.31 18 12C18 8.69 15.31 6 12 6ZM12 16C9.79 16 8 14.21 8 12C8 9.79 9.79 8 12 8C14.21 8 16 9.79 16 12C16 14.21 14.21 16 12 16Z" fill="url(#gradient)"/>
        <defs>
            <linearGradient id="gradient" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
                <stop stop-color="#00f2fe"/>
                <stop offset="1" stop-color="#4facfe"/>
            </linearGradient>
        </defs>
    </svg>
    <h1 style='margin: 0; background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>DocuMind AI</h1>
</div>
"""

# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 **Welcome!** I'm your advanced AI assistant, crafted by **code2model**. Upload a PDF in the sidebar, build the retriever, and let's uncover some insights!",
            }
        ]
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "indexed_pdf_name" not in st.session_state:
        st.session_state.indexed_pdf_name = None


def clear_chat() -> None:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "✨ Chat cleared. Ready for a new topic!",
        }
    ]


def clear_retriever() -> None:
    st.session_state.retriever = None
    st.session_state.indexed_pdf_name = None
    st.toast("🗑️ Retriever cleared successfully.", icon="✅")


def render_chat_history() -> None:
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


def main() -> None:
    initialize_state()

    st.markdown(HEADER_HTML, unsafe_allow_html=True)
    st.caption("Intelligent Document Explorer • Developed by **code2model**")

    with st.sidebar:
        st.markdown(HEADER_HTML.replace('width="45"', 'width="35"').replace('height="45"', 'height="35"'), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 👨‍💻 About")
        st.info("This application is proudly developed and maintained by **code2model**. It features cutting-edge Retrieval-Augmented Generation for reading and chatting with PDFs.", icon="💡")
        st.divider()
        
        st.subheader("⚙️ Settings")
        use_rag = st.toggle("Enable RAG Intelligence", value=False)
        uploaded_pdf = st.file_uploader("📄 Upload PDF Document", type=["pdf"])

        if uploaded_pdf is not None:
            if st.button("🚀 Build Retriever", use_container_width=True):
                with st.spinner("Processing PDF and generating embeddings..."):
                    st.session_state.retriever = build_retriever_from_pdf(uploaded_pdf.getvalue(), k=3)
                    st.session_state.indexed_pdf_name = uploaded_pdf.name
                st.toast(f"Retriever built for: {uploaded_pdf.name}", icon="🚀")

        if st.session_state.indexed_pdf_name:
            st.success(f"**📚 Indexed:** {st.session_state.indexed_pdf_name}")

        st.divider()
        st.button("🧹 Clear Retriever", on_click=clear_retriever, use_container_width=True)
        st.button("💬 Clear Chat", on_click=clear_chat, use_container_width=True)
        
        st.markdown("<br><p style='text-align: center; color: #888;'>© code2model</p>", unsafe_allow_html=True)

    render_chat_history()

    user_prompt = st.chat_input("Ask me anything about your document...")
    if not user_prompt:
        return

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("🧠 Analyzing..."):
            assistant_reply_generator, sources = generate_answer(
                user_prompt,
                st.session_state.messages,
                use_rag=use_rag,
                retriever=st.session_state.retriever,
            )
            
            if hasattr(assistant_reply_generator, '__iter__') and not isinstance(assistant_reply_generator, str):
                assistant_reply = st.write_stream(assistant_reply_generator)
            else:
                st.markdown(assistant_reply_generator)
                assistant_reply = assistant_reply_generator
            
            if sources:
                with st.expander("📚 View Source References"):
                    for i, doc in enumerate(sources):
                        st.markdown(f"**Source {i+1}**:\n\n{doc.page_content}\n")

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()
