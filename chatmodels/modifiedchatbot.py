from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MyChat AI",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0f1117;
    color: white;
}

/* Hide Streamlit elements */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Main container */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 2rem;
    font-size: 1rem;
}

/* Card */
.custom-card {
    background-color: #161b22;
    border: 1px solid #2d333b;
    padding: 1.2rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
}

/* Role text */
.role-text {
    color: #60a5fa;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.8rem;
    margin-top: 2rem;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background-color: #6366f1;
    color: white;
    font-weight: 600;
    padding: 0.55rem;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #4f46e5;
}

/* Chat input */
.stChatInputContainer {
    border-radius: 15px;
}

/* Input box */
.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">🤖 MyChat AI</div>

<div class="sub-title">
Professional AI Assistant powered by Groq
</div>
""", unsafe_allow_html=True)

# ---------------- INFO CARD ----------------
st.markdown("""
<div class="custom-card">

### 📌 Instructions

• Enter an AI role below and click <b>Apply Role</b><br>
• Start chatting with your AI assistant<br>
• Type <b>0</b> to exit the chatbot<br>
• Use <b>Clear Chat</b> to reset conversation<br>
• Maximum limit: <b>6 messages</b>

</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "current_role" not in st.session_state:
    st.session_state.current_role = "a helpful AI assistant"

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=f"You are {st.session_state.current_role}"
        )
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_active" not in st.session_state:
    st.session_state.chat_active = True

# ---------------- MODEL ----------------
@st.cache_resource
def get_model():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
         max_tokens=150
    )

model = get_model()

# ---------------- ROLE SECTION ----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)

st.subheader("🎭 AI Role")

role_input = st.text_input(
    "Enter AI Role",
    placeholder="Example: Teacher, Motivational Coach, Python Expert..."
)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(
        f"""
        Current Role:
        <span class="role-text">
        {st.session_state.current_role}
        </span>
        """,
        unsafe_allow_html=True
    )

with col2:
    apply_role = st.button("Apply Role")

if apply_role:

    if role_input.strip():

        st.session_state.current_role = role_input.strip()

        st.session_state.messages = [
            SystemMessage(
                content=f"You are {st.session_state.current_role}"
            )
        ]

        st.session_state.chat_history = []

        st.success(
            f"AI role changed to {st.session_state.current_role}"
        )

        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CLEAR CHAT ----------------
col1, col2 = st.columns([5,1])

with col2:
    clear = st.button("🗑 Clear")

if clear:

    st.session_state.messages = [
        SystemMessage(
            content=f"You are {st.session_state.current_role}"
        )
    ]

    st.session_state.chat_history = []

    st.session_state.chat_active = True

    st.rerun()

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.chat_history:

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
if st.session_state.chat_active:

    user_input = st.chat_input("Type your message...")

    if user_input:

        # Exit chatbot
        if user_input.strip() == "0":

            st.session_state.chat_active = False

            st.warning(
                "Chatbot exited. Click Clear to restart."
            )

            st.stop()

        # Message limit
        if len(st.session_state.chat_history) >= 6:

            st.error(
                "Message limit reached (6 messages)."
            )

            st.stop()

        # Store user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.messages.append(
            HumanMessage(content=user_input)
        )

        # AI response
        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

        ai_response = response.content

        # Store AI response
        st.session_state.messages.append(
            AIMessage(content=ai_response)
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        st.rerun()

else:
    st.error("Chatbot is currently closed.")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">

MyChat AI • Powered by Groq • Built with Streamlit

</div>
""", unsafe_allow_html=True)