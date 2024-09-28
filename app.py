import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd

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
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("MEDI-FRIEND")

question=st.text_input("Input: ",key="input")

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
    