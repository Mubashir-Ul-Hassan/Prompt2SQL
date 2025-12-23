import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

# Configuration
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found. Add it as a secret in Hugging Face Spaces settings.")
    st.stop()

genai.configure(api_key=api_key)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "file_info" not in st.session_state:
    st.session_state.file_info = {}

def get_data_summary(df):
    """Generate comprehensive data summary"""
    summary = []
    summary.append(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
    summary.append(f"Column Names: {', '.join(df.columns.tolist())}\n")
    summary.append(f"\nColumn Data Types:\n{df.dtypes.to_string()}\n")
    summary.append(f"\nBasic Statistics:\n{df.describe().to_string()}\n")
    summary.append(f"\nMissing Values:\n{df.isnull().sum().to_string()}\n")
    summary.append(f"\nFirst 5 Rows:\n{df.head().to_string()}\n")
    return "\n".join(summary)

def build_analysis_context(user_query):
    """Build context for Gemini including data summary"""
    if st.session_state.df is None:
        return "No data loaded. Please upload a CSV or Excel file first."
    
    data_context = f"""You are a data analyst AI assistant. Analyze the following dataset and answer user questions.

{get_data_summary(st.session_state.df)}

User Question: {user_query}

Provide detailed, accurate analysis based on the data above. Include specific numbers and insights."""
    
    return data_context

# Streamlit UI
st.title("📊 Data Analyst Agent")
st.caption("Upload CSV/Excel files and ask questions about your data")

# Sidebar for file upload and data info
with st.sidebar:
    st.header("📁 Upload Data")
    uploaded_file = st.file_uploader("Choose CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file:
        try:
            # Load file
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            
            st.session_state.file_info = {
                "filename": uploaded_file.name,
                "rows": st.session_state.df.shape[0],
                "columns": st.session_state.df.shape[1]
            }
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.metric("Rows", st.session_state.df.shape[0])
            st.metric("Columns", st.session_state.df.shape[1])
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    if st.button("Clear Data & Chat"):
        st.session_state.messages = []
        st.session_state.df = None
        st.session_state.file_info = {}
        st.rerun()

# Main area - Data preview and chat
if st.session_state.df is not None:
    # Data preview tabs
    tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "📊 Statistics", "💬 Chat"])
    
    with tab1:
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head(100), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Column Names:**")
            st.write(st.session_state.df.columns.tolist())
        with col2:
            st.write("**Data Types:**")
            st.write(st.session_state.df.dtypes)
    
    with tab2:
        st.subheader("Statistical Summary")
        st.dataframe(st.session_state.df.describe(), use_container_width=True)
        
        st.subheader("Missing Values")
        missing = st.session_state.df.isnull().sum()
        if missing.sum() > 0:
            st.dataframe(missing[missing > 0], use_container_width=True)
        else:
            st.success("No missing values found!")
    
    with tab3:
        st.subheader("Ask Questions About Your Data")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your data... (e.g., 'What are the main trends?', 'Summarize the data')"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    context = build_analysis_context(prompt)
                    
                    with st.spinner("Analyzing data..."):
                        response = model.generate_content(context)
                    
                    assistant_response = response.text
                    message_placeholder.markdown(assistant_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

else:
    # No data loaded
    st.info("👈 Please upload a CSV or Excel file from the sidebar to begin analysis")
    
    st.markdown("""
    ### What you can do:
    - 📤 Upload CSV or Excel files
    - 📊 View data previews and statistics
    - 💬 Ask questions about your data using AI
    - 🔍 Get insights, trends, and summaries
    
    ### Example questions:
    - "What are the main patterns in this dataset?"
    - "Which columns have the most missing values?"
    - "Summarize the key statistics"
    - "What insights can you find?"
    """)
