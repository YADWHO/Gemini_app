
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from streamlit_option_menu  import option_menu
from PIL import Image

st.set_page_config(
    page_title='Bot',
    layout='centered'  
    )


load_dotenv()

working_directory=os.path.dirname(os.path.abspath(__file__))

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
gen_ai.configure(api_key=GOOGLE_API_KEY)
 

def load_gemini_model():
    model=gen_ai.GenerativeModel('gemini-pro') 
    return model

def load_gemini_image(prompt,image):
    model=gen_ai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([prompt,image])
    result=response.text
    return result
    
def embed_model(input_text):
    e_model='models/text-embedding-004'
    embedding=gen_ai.embed_content(model=e_model, content=input_text,task_type='retrieval_document')
    e_l=embedding['embedding']
    return e_l  

def load_ask(user_prompt):
    model=gen_ai.GenerativeModel('gemini-pro')
    response=model.generate_content(user_prompt)
    return response.text
    

with st.sidebar:
    selected=option_menu('Gemini AI',
                                   ['Chatbot',
                                    'Image Captioning',
                                    'Text Embedding',
                                    'Ask me anything'],
                                   default_index=0)
def translate_role(user_role):
    if(user_role=='model'):
        return 'assistant'
    else:
        return user_role

if(selected=='Chatbot'):
    model=load_gemini_model()
    
    if('chat_session' not in st.session_state):
        st.session_state.chat_session=model.start_chat(history=[])
    st.title('Chatbot')
    
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role(message.role)):
            st.markdown(message.parts[0].text)
            
    user_prompt=st.chat_input('Type the query')
    if(user_prompt):
        st.chat_message('user').markdown(user_prompt)
        gemini_response=st.session_state.chat_session.send_message(user_prompt)
        
        with st.chat_message('assistant'):
            st.markdown(gemini_response.text)
            
if(selected=='Image Captioning'):
    st.title('Image Captioning')
    uploaded_image=st.file_uploader('upload the image',type=['jpg','jpeg','png'])
    if(st.button('generate')):
        image=Image.open(uploaded_image)
        
        col1,col2=st.columns(2)
        
        with col1:
            r_img=image.resize((150,150))
            st.image(r_img)
            
            
        
        with col2:
            prompt='write a short caption for this image'
            caption=load_gemini_image(prompt,image)
            st.info(caption)
            
if(selected=='Text Embedding'):
    st.title('Text Embedding')
    input_text=st.text_area(label='',placeholder='enter the text')
    if(st.button('get embedding')):
        response=embed_model(input_text)
        st.markdown(response)
        
if(selected=='Ask me anything'):
    st.title('Ask me anything')
    user_prompt=st.text_area(label='',placeholder='ask the question')
    
    if(st.button('get answer')):
        response=load_ask(user_prompt)
        st.markdown(response)
    
        
    
        
    
            
    
    
    
    
    
    
    
    
    
    