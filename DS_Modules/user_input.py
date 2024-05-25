# import streamlit as st
# from htmlTemplates import bot_template, user_template
# from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

# def handle_userinput(user_question):
#     try:
#         if st.session_state.chat_history is None:
#             st.session_state.chat_history = []

#         # Define the instruction to prepend to each user question
#         instruction = (
#             "You are an assistant that formats the context retrieved from the documents. "
#             "You should only format the provided information properly and ensure no extra information is added. "
#             "Respond with the formatted context only."
#             "if the question is not clear, you can ask for clarification."
#             "if the context provided does not contain the answer, you can respond with 'I don't have enough information to answer the question'."
#             "The following it the question you need to answer:"
#         )

#         # Combine the instruction with the user question
#         combined_question = f"{instruction}\n\n{user_question}"
        
#         response = st.session_state.conversation({'question': combined_question})
#         response['chat_history'][len(response['chat_history'])-2].content = user_question
#         # print("history:")
#         # print(response['chat_history'])
#         # print("\n\n\nlength of history:")
#         # print(len(response['chat_history']))
#         # print("\n\n\n\nlast message in history:")
#         # print(response['chat_history'][len(response['chat_history'])-2])
#         st.session_state.chat_history=response['chat_history']
#         # st.session_state.chat_history = [HumanMessage(content=user_question), response['chat_history'][1]]
#         # print(response['chat_history'][0])
#         # print(type(response['chat_history'][0]))
#         for i, message in enumerate(st.session_state.chat_history):
#             if i % 2 == 0:
#                 st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
#             else:
#                 st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
#     except Exception as e:
#         print(f"An error occurred while handling user input: {e}")


import streamlit as st
from htmlTemplates import bot_template, user_template
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
import os

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
                
                # Check if the response includes an indication of images
                if "image" in message.content.lower():
                    display_relevant_images(user_question)

    except Exception as e:
        print(f"An error occurred while handling user input: {e}")

def display_relevant_images(user_question):
    try:
        image_dir = "extracted_images"
        if not os.path.exists(image_dir):
            st.write("No images have been extracted.")
            return
        
        # Display images relevant to the user question
        # This is a placeholder for actual logic to match images with the query
        for img_file in os.listdir(image_dir):
            if user_question.lower() in img_file.lower():
                st.image(os.path.join(image_dir, img_file))
    except Exception as e:
        print(f"An error occurred while displaying images: {e}")
