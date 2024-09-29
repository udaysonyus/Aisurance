
# MediFriend - Streamlit Application

## Overview

**MediFriend** is a healthcare-oriented web application built using **Streamlit**, designed to interact with a SQLite database containing information about doctors. The app allows users to ask questions in natural language, which are then converted into SQL queries to retrieve relevant data. It leverages Google's Gemini model for AI-based SQL generation.

## Key Features

- **Natural Language to SQL**: Users can input questions in plain English, and the app will convert these into SQL queries to fetch data from the database.
- **Doctor Database**: The app accesses a database with information about doctors, such as names, specializations, locations, insurance providers, and insurance ratings.
- **Real-time Data Display**: Query results are displayed in real-time using a pandas DataFrame.
- **Error Handling**: If the query cannot be executed, a user-friendly message is shown.

## Prerequisites

- Python 3.7+
- Streamlit
- SQLite
- Google Generative AI API (Gemini)
- A SQLite database named `healthcare.db` with a `doctors` table.

## Project Structure

```
MediFriend/
│
├── .env                   # Environment variables (API keys)
├── healthcare.db           # SQLite database
├── logo-transparent-png.png # Logo for the app
├── app.py                 # Main Streamlit app
└── README.md              # Project documentation (this file)
```

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/MediFriend.git
   cd MediFriend
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Setup environment variables**:
   Create a `.env` file in the project root directory with your Google Generative AI API key:
   ```
   API_KEY=your_google_api_key
   ```

4. **Run the application**:
   ```
   streamlit run app.py
   ```

## Detailed Breakdown

### 1. Load Environment Variables
```python
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key="YOUR_API_KEY")
```
- Uses `python-dotenv` to load environment variables from `.env` file.
- Configures Google Generative AI API using `genai.configure()`.

### 2. SQL Query Generator Function

```python
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text
```
- Sends the user’s question along with a pre-defined prompt to the **Gemini model**.
- Returns the SQL query as the response.

### 3. Execute SQL Queries

```python
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
```
- Connects to the SQLite database, executes the generated SQL query, and returns the results.

### 4. Streamlit UI Components

- **Logo Display**: 
   Embeds a logo into the UI using base64 encoding for images.

- **User Input**:
   Accepts a question from the user via `st.text_input()`.

- **Submit Button**:
   Executes the logic to convert the question into SQL and displays results in a pandas DataFrame.

```python
question = st.text_input("", key="")
submit = st.button("Submit")

if submit:
    response = get_gemini_response(question, prompt)
    try:
        response = response.lower()
        if response.split()[0].lower() == 'select':
            resp = read_sql_query(response, "healthcare.db")
            st.dataframe(pd.DataFrame(resp))
    except:
        st.write("Cannot query this from database, kindly rephrase the statement.")
```

### 5. Error Handling
- If the response is not a valid SQL query or if an error occurs during execution, a custom error message is displayed.

```python
except:
    st.write("Cannot query this from database, kindly rephrase the statement.")
```

## Database Schema

The application interacts with a single table in the SQLite database:

### `doctors` Table

| Column               | Type    | Description                                  |
|----------------------|---------|----------------------------------------------|
| `id`                 | INTEGER | Primary Key, Autoincrement                   |
| `insurance_provider` | TEXT    | Name of the insurance provider               |
| `doctor_name`        | TEXT    | Name of the doctor                           |
| `doctor_specialization` | TEXT  | Specialization of the doctor                 |
| `location`           | TEXT    | Location of the doctor                       |
| `ins_rating`         | INTEGER | Insurance rating associated with the doctor  |

## Usage Examples

### Query: "How many doctors are there?"
Generated SQL: `SELECT COUNT(*) FROM doctors;`

### Query: "List all doctors in New York."
Generated SQL: `SELECT * FROM doctors WHERE location = 'New York';`

### Query: "Find doctors with an insurance rating greater than 4."
Generated SQL: `SELECT doctor_name, doctor_specialization FROM doctors WHERE ins_rating > 4;`

## Future Enhancements

- **Improved Query Handling**: Enhance the natural language processing to cover more complex SQL queries.
- **Additional Tables**: Extend the database with more tables, such as `patients`, `appointments`, etc.
- **Data Visualization**: Incorporate visual charts for better data insights.
- **User Authentication**: Add user authentication and role-based access control.

## Conclusion

MediFriend aims to simplify querying healthcare databases by using natural language inputs, thus enabling users to retrieve data easily. With further enhancements, this tool can become more robust and user-friendly for healthcare professionals and analysts.

## License

This project is licensed under the MIT License.


## Analysis and Future Expansion

### 1. Natural Language Processing (NLP)
   - The NLP capabilities of the Google Gemini model provide an important backbone for converting natural language queries into SQL commands. However, some key areas for improvement include:
     - **Handling Ambiguity**: Improving the model's ability to handle vague or ambiguous queries by prompting users for clarifications.
     - **Query Expansion**: Supporting more complex SQL queries that include JOIN operations, nested queries, and aggregate functions with multiple conditions.
     - **Synonym Handling**: Ensuring the model recognizes synonyms (e.g., “physician” instead of “doctor”) or even different phrasings of similar questions.

### 2. SQL Query Execution and Database Efficiency
   - The project currently handles basic SQL queries, but as the dataset scales, **performance optimization** will become essential. Considerations could include:
     - **Indexing**: Adding appropriate indexing on commonly queried fields like `doctor_specialization` and `location` to speed up searches.
     - **Query Optimization**: Analyzing query execution plans for more complex queries to ensure the database is performing efficiently.
     - **Database Schema Evolution**: With future expansion into other healthcare entities like patients or appointments, the schema will need normalization and proper foreign key constraints for better data integrity.

### 3. Scalability and Extensibility
   - Currently, the app is limited to a local SQLite database. As the application scales, migrating to more robust databases (like **PostgreSQL** or **MySQL**) for multi-user support will be necessary. This would involve:
     - **Connection Pooling**: Managing database connections more efficiently, especially under high traffic.
     - **Horizontal Scaling**: With more users querying simultaneously, employing load balancing and replicating the database across servers may be necessary.

### 4. User Interface (UI) and User Experience (UX)
   - The UI currently offers a clean interface, but some features could be improved:
     - **Autocomplete for Query Input**: Offering suggestions as users type in their queries would guide users and reduce errors.
     - **Search History**: Allowing users to see past queries and their results could improve usability.
     - **Custom Filters**: Incorporating drop-down menus or multi-select filters for location, specialization, or insurance provider could enhance the user experience for non-technical users.

### 5. Data Visualization
   - The app could further improve by integrating data visualization tools, such as bar charts or pie charts, especially for aggregate queries (e.g., showing average ratings or number of doctors by specialization). Libraries like **Plotly** or **Matplotlib** could be used in conjunction with Streamlit to display this data more effectively.

