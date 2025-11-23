import streamlit as st
import pandas as pd
import sqlite3
import ollama

# -------------------------
# Helper: Run SQL on DataFrame
# -------------------------
def run_sql_on_dataframe(df, query):
    conn = sqlite3.connect(":memory:")
    df.to_sql("table_1", conn, index=False, if_exists="replace")
    try:
        results = pd.read_sql_query(query, conn)
    except Exception as e:
        results = str(e)
    conn.close()
    return results

# -------------------------
# Helper: Generate SQL from prompt
# -------------------------
def generate_sql(prompt, model_name, schema):
    system_prompt = f"""
    You are an AI that converts natural language into SQL queries.
    The database schema is: {schema}.
    Generate only the SQL query without explanations.
    """
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Prompt2SQL", layout="wide")
st.title("🧑‍💻 Prompt2SQL — Query Excel/CSV with Natural Language")

uploaded_files = st.file_uploader(
    "📂 Upload one or more Excel/CSV files",
    type=["xlsx", "xls", "csv"],
    accept_multiple_files=True
)

# Sidebar: Model choice
model_name = st.sidebar.selectbox(
    "Choose Ollama model",
    ["llama3.1:8b", "qwen2.5:7b", "mistral:7b", "phi3:3.8b", "gemma2:9b"],
    index=0
)

# Sidebar: Visualization choice
chart_choice = st.sidebar.radio(
    "📊 Visualization Type",
    ["Auto", "Bar", "Line", "Scatter", "Area"]
)

# Sidebar: Prompting guide
st.sidebar.markdown("### 📝 Prompting Guide")
st.sidebar.info(
    """
**Ask a Question** → Use short, precise queries  
- Example: *What is the average salary?*  
- Example: *List top 5 products by sales.*  

**Free-form Prompt** → Use detailed, conversational prompts  
- Example: *Summarize sales performance by region over the last year.*  
- Example: *Explain which department has the highest employee turnover.*  

**Summarize Data** → Automatically generates a plain-English overview of the dataset.  
    """
)

# Mode selector
mode = st.radio("Choose action:", ["Ask a Question", "Free-form Prompt", "Summarize Data"])

# Text box for prompt/query
user_input = st.text_area("💬 Enter your prompt or question here:")

if uploaded_files:
    for file in uploaded_files:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader(f"📄 {file.name}")
        st.dataframe(df.head())

        schema = str(df.dtypes.to_dict())

        if st.button(f"Run on {file.name}"):
            if mode == "Summarize Data":
                # Direct summarization
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Summarize this dataset in plain English."},
                        {"role": "user", "content": df.head(20).to_csv()}
                    ]
                )
                st.subheader("📑 Summary")
                st.write(response["message"]["content"])

            else:
                if not user_input.strip():
                    st.warning("⚠️ Please enter a prompt or question.")
                else:
                    # Generate SQL
                    sql_query = generate_sql(user_input, model_name, schema)
                    st.subheader("📝 Generated SQL")
                    st.code(sql_query, language="sql")

                    results = run_sql_on_dataframe(df, sql_query)

                    if isinstance(results, str):
                        st.error(f"SQL Error: {results}")
                    else:
                        st.subheader("📋 Query Results")
                        st.dataframe(results)

                        # Add visualization
                        if not results.empty:
                            st.subheader("📊 Visualization")
                            try:
                                if chart_choice == "Auto":
                                    if results.shape[1] == 2:
                                        col1, col2 = results.columns
                                        if pd.api.types.is_numeric_dtype(results[col2]) and not pd.api.types.is_numeric_dtype(results[col1]):
                                            st.bar_chart(results.set_index(col1)[col2])
                                        elif pd.api.types.is_numeric_dtype(results[col1]) and pd.api.types.is_numeric_dtype(results[col2]):
                                            st.line_chart(results)
                                        else:
                                            st.area_chart(results)
                                    elif results.shape[1] > 2:
                                        st.line_chart(results)
                                    else:
                                        st.info("Not enough data to generate a chart.")
                                else:
                                    if chart_choice == "Bar":
                                        st.bar_chart(results.set_index(results.columns[0]))
                                    elif chart_choice == "Line":
                                        st.line_chart(results.set_index(results.columns[0]))
                                    elif chart_choice == "Scatter":
                                        st.scatter_chart(results)
                                    elif chart_choice == "Area":
                                        st.area_chart(results)
                            except Exception as e:
                                st.warning(f"Could not generate chart: {e}")
