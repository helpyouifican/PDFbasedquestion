from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate
)
from langchain.chains import LLMChain
import streamlit as st
import tempfile
import os

#제목
st.title("PDF파일로 문제 만들기")
st.write("------")

#파일업로드
uploaded_file = st.file_uploader("PDF 파일을 올려주세요",type=['pdf'])
st.write("------")

#PDF저장함수
def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name,uploaded_file.name)
    with open(temp_filepath,"wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages


#업로드 되면 동작하는 코드
if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)  
    
    #gpt 로드
    gpt = ChatOpenAI(
        model_name="gpt-3.5-turbo-1106",
        temperature=0,
        model_kwargs={"frequency_penalty": 1.0}
    )

    # 프롬프트 엔지니어링 템플릿 n지선다
    Multiple_Choice_template = """
    You are a {subject} teacher. You are teaching a class of students. You are teaching them about the importance of basic.
    Make Test {Question_num} Questions for the following text Answer the Questions and write Commentary

    ---
    Question Info
    Types: {Answer_num}-choice (sentence or short words options)
    Language: {language}
    
    if Answer_num == 4:
    
    1. 
    2.
    3.
    4.
    
    Answer the Questions and write Commentary
    Correct Answer: 
    Commentary:
    ---
    TEXT:
    {text}
    """
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(Multiple_Choice_template)
    ])

    chatchain = LLMChain(llm=gpt,prompt=prompt,verbose=True)
    test=chatchain.run(subject="Korean", Question_num="3", Answer_num="4",language='Korean',text=pages)
    st.write(test)
    # 테스트결과 pdf파일 크기에 비해 문제수나 선택지가 너무 많으면 오작동함
    # pdf파일이 너무크면 토큰 수 부족

