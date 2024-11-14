# pages/chat_bot.py
import streamlit as st
import os

# Create an agent that can access and use a large language model (LLM).
def create_agent():
    # init AzureChatOpenAI
    from langchain.chat_models import AzureChatOpenAI
    os.environ['AZURE_OPENAI_API_KEY'] = "1b31fc4eb58c4879960c46f697d72af6"
    os.environ['AZURE_OPENAI_ENDPOINT'] = "https://genai-openai-quantifai.openai.azure.com/"
    os.environ['OPENAI_API_VERSION'] = '2024-02-01'
    llm = AzureChatOpenAI(model_name='gpt-4o')
    
    return llm

# Query an agent and return the response as a string.
def query_agent(agent, company_ticker, query):
    if company_ticker:
        prompt = ("Please answer the queries as a professional financial analyst. Please answer the queries based on the given company, the company ticker is " + company_ticker + ". Below is the query. Query: "
            + query
        )
    else:
        prompt = ("Please answer the queries as a professional financial analyst. Below is the query. Query: "
            + query)

    # Run the prompt through the agent.
    response = agent.invoke(prompt)

    # Convert the response to a string.
    return response.content



def show_chat_bot(company_ticker):
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    st.write("##### Chat Bot Section")
    query = st.text_area("Insert your query")
    # st.text_input("Enter your question or prompt here:")
    # st.write(response)

    if st.button("Submit Query", type="primary"):
        # Create an agent from the CSV file.
        llm = create_agent()
        
        with st.spinner("Generating response..."):
            # Query the agent.
            response = query_agent(agent=llm, company_ticker=company_ticker, query=query)

        # Add user query and model response to chat history
        st.session_state.chat_history.append({"sender": "User", "message": query})
        st.session_state.chat_history.append({"sender": "AI", "message": response})
        
        # Clear the input box after submission
        st.session_state.user_query = ""
    
    # Display the chat history
    for entry in st.session_state.chat_history:
        align = "left" if entry["sender"] == "AI" else "right"
        
        st.markdown(
            f"<div style='text-align: {align};'>"
            f"<div style=' display: inline-block; max-width: 70%; padding: 10px; border-radius: 10px;"
            f"margin: 5px; background-color: {'#E8F5E9' if align == 'left' else '#f0f0f0'};'>"
            f"<strong>{entry['sender']}:</strong> {entry['message']}</div>",
            unsafe_allow_html=True,
        )
        