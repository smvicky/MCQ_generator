import os
import json
import pandas as pd
import traceback
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.utils import get_table_data, read_file
import streamlit as st
from src.mcqgenerator.mcq_generator import generate_review_chain
from src.mcqgenerator.logger import logging 
from dotenv import load_dotenv

# with open('response.json', 'r') as file:
    # RESPONSE_JSON = json.load(file)

RESPONSE_JSON={
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        "correct": "correct answer"
    }
}

print(RESPONSE_JSON)
# RESPONSE_JSON.replace("'",'"')
st.title("MCQ Generator using langchin and opneai api")

with st.form('user_inputs'):
    #upload file 
    uploaded_file = st.file_uploader('Please upload your file')

    #input filed
    mcq_count = st.number_input('Please enter mcq count', min_value=3,max_value=20)

    #subject
    subject = st.text_input('Please enter subject', max_chars=20)

    #quiz tone
    tone = st.text_input('Please enter quize tone', max_chars= 20)

    #add button for submitting
    button = st.form_submit_button('Create Quiz')
    # if button:
    #     print(mcq_count)
    #     print(subject)
    #     print(tone)

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading"):
            try:
                text = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response = generate_review_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json" : json.dumps(RESPONSE_JSON)
                        }
                    )
                
            except Exception as e:
                traceback.print_exc(type(e),e,e.__traceback__)
                st.error("Error generating review chain")
            
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response, dict):
                    #extact quiz from response
                    quiz = response.get('quiz', None)
                    quiz.replace("'", '"')
                    print('type_quiz ',type(quiz))
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if(table_data is not None):
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label="review",value=response.get('review'))
                        else:
                            st.error('Could not find')

                else:
                    st.write(response)

