
import asyncio
import streamlit as st
from AI import generate_agent_response
from pathlib import Path

st.set_page_config(page_title="Study Notes & Quiz Generator", layout="wide")
st.title("📚 Study Notes Summarizer & Quiz Generator")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = ""

def run_agent(prompt: str, session_key: str):
    """Run agent and save result to session state"""
    try:
        response = asyncio.run(generate_agent_response(prompt))
    except RuntimeError:
        # Streamlit rerun workaround
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(generate_agent_response(prompt))
    st.session_state[session_key] = response.final_output

if uploaded_file:
    # Save uploaded PDF locally
    temp_file = Path("uploaded.pdf")
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("PDF uploaded successfully!")

    # Summarize Button
    if st.button("Generate Summary"):
        with st.spinner("Summarizing PDF..."):
            run_agent("Summarize the uploaded PDF into study notes.", "summary")

    if st.session_state.summary:
        st.markdown("### 📝 Study Notes Summary")
        st.markdown(st.session_state.summary)

    # Quiz Generator Button
    if st.button("Create Quiz"):
        with st.spinner("Generating Quiz..."):
            run_agent("Generate MCQs and mixed-style quiz from the PDF.", "quiz")

    if st.session_state.quiz:
        st.markdown("### ❓ Generated Quiz")
        st.markdown(st.session_state.quiz)
