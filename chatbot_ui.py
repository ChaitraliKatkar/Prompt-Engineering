import streamlit as st
from rag_response import generate_response  # Import the function from the previous script

st.title("💰 Personal Finance Chatbot")
st.write("Ask me anything about your expenses and income!")

user_query = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_query:
        response = generate_response(user_query)
        st.write("**Bot Response:**")
        st.write(response)
    else:
        st.warning("Please enter a query.")
