import time
import streamlit as st
import os
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv

# Load environment variables
# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
# groq_api_key = os.getenv("GROQ_API_KEY")
# os.environ["GOOGLE_API_KEY"] = google_api_key
# os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
# Access Streamlit Secrets directly
google_api_key = st.secrets["GOOGLE_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]
hf_token = st.secrets["HF_TOKEN"]

# Ensure they're available as environment variables if needed elsewhere in the app
os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["HF_TOKEN"] = hf_token

# Initialize LLM
llm_llama3 = ChatGroq(
    # model="llama3-8b-8192",
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=groq_api_key,
)

# Initialize embeddings
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.environ["HF_TOKEN"],
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)

# Load FAISS vector store
def load_vectordb():
    PATH = r"modules\faiss_index_\Smart Farming"
    persisted_vectorstore = FAISS.load_local(PATH, embeddings, allow_dangerous_deserialization=True)
    return persisted_vectorstore.as_retriever()

# Generate chatbot response with language-specific instructions
def generate_response(user_input, session_history, retriever, language="en"):
    relevant_docs = retriever.get_relevant_documents(user_input)
    retrieved_context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Determine the language instruction based on the UI language
    if language == "mr":
        language_instruction = "Note: Please answer in Marathi"
    else:
        language_instruction = "Note: Please answer in English."
    
    template = """
    Role: AI assistant for agriculture schemes. Answer only scheme-related queries.
    {language_instruction}
    Session History:
    {session_history}
    Context:
    {retrieved_context}
    User: {user_input}
    AI:"""
    
    prompt = PromptTemplate(
        input_variables=["session_history", "user_input", "retrieved_context", "language_instruction"],
        template=template
    )
    llm_chain = LLMChain(llm=llm_llama3, prompt=prompt)
    
    return llm_chain.run({
        "session_history": session_history, 
        "user_input": user_input, 
        "retrieved_context": retrieved_context,
        "language_instruction": language_instruction
    })

# Streamlit Chat UI with language parameter
def chatbot_ui(language="en"):
    st.markdown("""<style>
    .chat-container { max-width: 700px; margin: auto; }
    .user-message { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 20px; }
    .assistant-message { background-color: #E8E8E8; padding: 10px; border-radius: 10px; margin-bottom: 30px; }
    .chat-avatar { width: 40px; height: 40px; border-radius: 50%; }
    </style>""", unsafe_allow_html=True)

    if "session_history" not in st.session_state:
        st.session_state.session_history = []

    if "retriever" not in st.session_state:
        st.session_state.retriever = load_vectordb()
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.session_history:
        role, content = message.split(":", 1)
        if role.strip().lower() == "user":
            st.markdown(f'<div class="user-message">👤 {content.strip()}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">🤖 {content.strip()}</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("Type your message...", key="user_input", value="", on_change=lambda: st.session_state.update(send_message=True))
    
    if st.session_state.get("send_message", False) or st.button("Send"):
        if user_input:
            st.session_state.session_history.append(f"User: {user_input}")
            response = generate_response(
                user_input, 
                "\n".join(st.session_state.session_history), 
                st.session_state.retriever,
                language=language
            )
            st.session_state.session_history.append(f"AI: {response}")
            st.session_state["send_message"] = False
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main function
def main():
    st.title("🌱 Agriculture Schemes Chatbot")
    st.markdown("Effortlessly explore government schemes for farmers. Ask anything!")
    # Pass the UI language (e.g., "mr" for Marathi, "en" for English)
    chatbot_ui(language="en")

if __name__ == "__main__":
    main()
