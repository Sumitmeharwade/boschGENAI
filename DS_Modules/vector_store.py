import os
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from DS_Modules.text_splitter import get_text_chunks
from DS_Modules.pdf_reader import get_pdf_text

def get_vectorstore(text_chunks):
    try:
        embeddings = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    
    except Exception as e:
        print(f"An error occurred while handling vectorstore: {e}")
        return None 

def retrieve_or_embed(pdf):
    pdf_name = pdf.name.split('.')[0]
    index_store = f"faiss_indexes/{pdf_name}.faiss"
    
    if os.path.exists(index_store):
        embeddings = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.load_local(index_store, embeddings=embeddings)
    else:
        raw_text = get_pdf_text(pdf)
        if raw_text is not None:
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            if vectorstore is not None:
                vectorstore.save_local(folder_path=index_store)
            return vectorstore
        else:
            return None
