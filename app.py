import os
import streamlit as st
from openai import OpenAI

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI DevOps Assistant",
    page_icon="🚀",
    layout="wide"
)

# ================= NVIDIA CLIENT =================
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

MODEL = "nvidia/nemotron-3-super-120b-a12b"

# ================= CUSTOM CSS =================
st.markdown("""
<style>

.stApp {
    background: #0f172a;
    color: white;
}

.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 900;
    color: #76b852;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

.stChatMessage {
    background: #1e293b;
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(
    "<h1 class='main-title'>🚀 AI DevOps Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Powered by NVIDIA Nemotron 120B</p>",
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
with st.sidebar:

    st.title("⚙️ Settings")

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.6,
        0.1
    )

    max_tokens = st.slider(
        "Max Tokens",
        256,
        4096,
        1024,
        256
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= SHOW OLD MESSAGES =================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT INPUT =================
prompt = st.chat_input(
    "Ask Terraform, Docker, CI/CD, Kubernetes..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        try:

            completion = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            for chunk in completion:

                if (
                    chunk.choices
                    and chunk.choices[0].delta.content
                ):

                    content = chunk.choices[0].delta.content

                    full_response += content

                    placeholder.markdown(
                        full_response + "▌"
                    )

            placeholder.markdown(full_response)

        except Exception as e:

            full_response = f"❌ Error: {str(e)}"

            placeholder.error(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

# ================= FOOTER =================
st.divider()

st.markdown("""
<div style='text-align:center;color:gray;padding:20px;'>

Built with ❤️ by Manikanta Sai

</div>
""", unsafe_allow_html=True)