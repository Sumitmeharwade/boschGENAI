import streamlit as st
import os
from htmlTemplates import css, bot_template, user_template
from dotenv import load_dotenv
from DS_Modules.vector_store import retrieve_or_embed
from DS_Modules.chatbot_model import get_conversation_chain
from DS_Modules.user_input import handle_userinput
from DS_Modules.pdf_reader import extract_images_from_pdf

def main():
    load_dotenv()
    
    st.set_page_config(page_title="Chatbot for PDFs", page_icon=":🤖")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDF Files :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'")
        button = st.button("Process")
        if button:
            with st.spinner("Processing... Please Wait..."):
                if pdf_docs:
                    vectorstore = retrieve_or_embed(pdf_docs)
                    image_count = extract_images_from_pdf(pdf_docs)
                    
                    st.success("Processing Done. Please ask a question now.")
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    
                    st.sidebar.subheader("Extracted Images")
                    if image_count:
                        st.sidebar.write(f"Extracted {image_count} images from the PDF.")
                        for img_file in os.listdir("extracted_images"):
                            st.sidebar.image(os.path.join("extracted_images", img_file))
                    else:
                        st.sidebar.write("No images found in the PDF.")

if __name__ == '__main__':
    main()
