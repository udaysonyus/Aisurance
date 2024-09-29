   
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import pandas as pd
import re
import base64
from io import BytesIO
import requests

load_dotenv()
# Get the API key from environment variables
# api_key = st.secrets["api"]
genai.configure(api_key="AIzaSyCJnEh5PFdu1ng3TNhiy7b_3XkBxzQ-h0w")

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows
prompt=[
    """
    You are an expert in converting English questions to SQL queries!
The SQL database contains the following tables and columns:

doctors: 
- id: INTEGER, PRIMARY KEY, AUTOINCREMENT
- insurance_provider: TEXT
- doctor_name: TEXT
- doctor_specialization: TEXT
- location: TEXT
- ins_rating: INTEGER

For example:

How many doctors are there?
The SQL command will be something like this: SELECT COUNT(*) FROM doctors;

List all doctors working in a specific location.
The SQL command will be something like this: SELECT * FROM doctors WHERE location = '[specific_location]';

Show the names and specializations of doctors who have an insurance rating greater than a certain value.
The SQL command will be something like this: SELECT doctor_name, doctor_specialization FROM doctors WHERE ins_rating > [specific_rating];

Count how many doctors are associated with a specific insurance provider.
The SQL command will be something like this: SELECT COUNT(*) FROM doctors WHERE insurance_provider = '[specific_insurance_provider]';

Get the average insurance rating of doctors in a particular specialization.
The SQL command will be something like this: SELECT AVG(ins_rating) FROM doctors WHERE doctor_specialization = '[specific_specialization]';

Find doctors with the highest insurance ratings.
The SQL command will be something like this: SELECT * FROM doctors WHERE ins_rating = (SELECT MAX(ins_rating) FROM doctors);

Find insurance provider with the highest insurance ratings.
The SQL command will be something like this: SELECT insurance_provider FROM doctors WHERE ins_rating = (SELECT MAX(ins_rating) FROM doctors);

Find all the doctors based on their specializations.
The SQL command will be something like this: SELECT doctor_name FROM doctors WHERE doctor_specialization = '[specific_specialization]' ;

Find all the doctors based on their specialization and the location.
The SQL command will be something like this: select * from doctors where doctor_specialization = '[specific_specialization]' and location = '[specific_location]';' ;

Also, ensure the SQL code does not include ``` in the beginning or end and the word SQL in the output.

    """
]
# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Streamlit app starts here
st.set_page_config(layout="centered")

# Load the logo image from a URL
logo_url = "logo-transparent-png.png"
logo = Image.open(logo_url)

# Convert image to base64 for embedding in HTML
logo_base64 = image_to_base64(logo)

# Set the title with logo on the left and tagline in smaller font
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="width: 100px; margin-right: 20px;margin-left: 140px;" alt="Logo">
        <div>
            <h1 style="margin: 0; display: inline;">MediFriend</h1>
            <h5 style="margin: 0; margin-left: 180px;">...a friend indeed</h5>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


question=st.text_input("", key="")

submit=st.button("Submit")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    
    try:
        response=response.lower()
        #st.write(response)
        if response.split()[0].lower()=='select':
            resp=read_sql_query(response,"healthcare.db")
            string_col=response.split(" ")
            end=string_col.index('from')
            columns = string_col[1:end]
            data=pd.DataFrame(resp)    
            st.dataframe(resp)
            
    except:
            st.write("Cannot query this from database, kindly Rephrase the statement.")
    