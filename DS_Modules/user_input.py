
import streamlit as st
from htmlTemplates import bot_template, user_template
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
import os
from sentence_transformers import SentenceTransformer, util
import os
import json
import torch
def handle_userinput(user_question):
    try:
        if st.session_state.chat_history is None:
            st.session_state.chat_history = []

        # Define the instruction to prepend to each user question
        instruction = (
            "You are an assistant that formats the context retrieved from the documents. "
            "You should only format the provided information properly and ensure no extra information is added. "
            "If the query is related to images, provide the relevant images."
        )

        # Combine the instruction with the user question
        combined_question = f"{instruction}\n\n{user_question}"

        response = st.session_state.conversation({'question': combined_question})
        response['chat_history'][len(response['chat_history'])-2].content = user_question
        
        # response = st.session_state.conversation({'question': combined_question})
        
        st.session_state.chat_history = response['chat_history']
        
        # Display user question without the instruction
        # st.session_state.chat_history.append(HumanMessage(user_question))

        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                display_relevant_images(user_question)
                # Check if the response includes an indication of images
                # if "image" in message.content.lower():
                #     display_relevant_images(user_question)

    except Exception as e:
        print(f"An error occurred while handling user input: {e}")

def load_image_contexts(file="image_contexts.json"):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:  # Ensure proper encoding
            return json.load(f)
    return []

def embed_texts(texts, model):
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

def display_relevant_images(user_question):
    try:
        image_contexts = load_image_contexts()
        
        if not image_contexts:
            st.write("No image contexts available.")
            return
        
        model = SentenceTransformer('all-MiniLM-L6-v2')

        user_query_embedding = embed_texts([user_question], model)
        context_texts = [img_ctx["context"] for img_ctx in image_contexts]
        context_embeddings = embed_texts(context_texts, model)

        similarities = util.pytorch_cos_sim(user_query_embedding, context_embeddings).squeeze()

        relevant_images = []
        for i, score in enumerate(similarities):
            if score >= 0.1:  # You can adjust the threshold value
                relevant_images.append(image_contexts[i])

        if relevant_images:
            for img_ctx in relevant_images:
                print(img_ctx, img_ctx["filename"])
                st.image(os.path.join("extracted_images", img_ctx["filename"]))
        else:
            st.write("No relevant images found.")
    except Exception as e:
        print(f"An error occurred while displaying images: {e}")