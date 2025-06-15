import streamlit as st
from backend.code_to_pseudo import convert_code_to_pseudo
from backend.pseudo_to_code import convert_pseudo_to_code
from backend.generate_pseudo import generate_pseudocode
from backend.existing_creations import list_creations

openai_key = st.secrets["api_keys"]["openai_key"]
email = st.secrets["general"]["email"]

st.set_page_config(page_title="Code2Pseudo AI", layout="centered")
st.title("🧠 Code2Pseudo AI – Convert Code and Pseudocode Easily")

menu = st.sidebar.selectbox("Choose an action", [
    "Convert Code ➡️ Pseudocode",
    "Convert Pseudocode ➡️ Code",
    "Generate Pseudocode from Prompt",
    "View Existing Creations"
])

if menu == "Convert Code ➡️ Pseudocode":
    st.subheader("🔁 Code to Pseudocode")
    user_code = st.text_area("Paste your code below")
    if st.button("Convert"):
        if user_code.strip():
            result = convert_code_to_pseudo(user_code)
            st.code(result, language='text')
        else:
            st.warning("Please paste some code.")

elif menu == "Convert Pseudocode ➡️ Code":
    st.subheader("🔁 Pseudocode to Code")
    pseudo_input = st.text_area("Paste your pseudocode below")
    if st.button("Convert"):
        if pseudo_input.strip():
            result = convert_pseudo_to_code(pseudo_input)
            st.code(result, language='python')
        else:
            st.warning("Please paste some pseudocode.")

elif menu == "Generate Pseudocode from Prompt":
    st.subheader("✨ Generate Pseudocode from a Prompt")
    prompt = st.text_input("Enter a description (e.g., sort a list)")
    if st.button("Generate"):
        if prompt.strip():
            pseudo = generate_pseudocode(prompt)
            st.code(pseudo, language='text')
        else:
            st.warning("Please enter a prompt.")

elif menu == "View Existing Creations":
    st.subheader("📁 Existing Pseudocode Creations")
    data = list_creations()
    if not data:
        st.info("No creations found.")
    else:
        for item in data:
            st.markdown(f"### {item['title']}")
            st.code(item['content'], language='text')