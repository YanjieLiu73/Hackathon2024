
import streamlit as st
from page_modules.utilities import save_content_to_ppt
import pandas as pd
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

def query_agent(agent, query):

    prompt = (
        """
           Please answer the queries as a professional financial analyst.

            Below is the query.
            Query: 
            """
        + query
    )

    # Run the prompt through the agent.
    response = agent.invoke(prompt)

    # Convert the response to a string.
    return response.content

def show_valuation(uploaded_file):
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    valuation_tabs = st.tabs(["DCF", "LBO"])
    # Create an agent from the CSV file.
    llm = create_agent()
    with st.spinner("DCF Analysis Running..."):
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                excel_data = pd.ExcelFile(uploaded_file)
                df = excel_data.parse(excel_data.sheet_names[0])

            # Convert data to a plain text table for LLM interpretation
            data_text = df.to_string(index=False)

            # Construct queries for DCF and LBO
            dcf_query = (
                """
                Using the data provided below, calculate the present value per share of given Corp using a Discounted Cash Flow (DCF) analysis. 
                Please provide the final present value per share at the beginning, followed by detailed steps, calculations, assumptions, and any formulas used.
                Identify necessary details like cash flows, tax rate, and discount rate from the data as best as possible. 
                """
                +"Below is the data:\n"
                + f"Data:\n{data_text}"
            )

            lbo_query = (
                "Using the data provided below, perform a Leveraged Buyout (LBO) analysis for given Corp. "
                "Identify necessary details like cash flows, debt financing, and exit assumptions from the data as best as possible. "
                "Please provide the final projected return at the beginning, followed by detailed steps, calculations, "
                "assumptions, and any formulas used.\n\n"
                f"Data:\n{data_text}"
            )
            with valuation_tabs[0]:
                # Button actions for DCF and LBO
                if st.button("Calculate DCF Analysis"):
                    try:
                        # Generate DCF response
                        dcf_response = query_agent(agent=llm, query=dcf_query)
                        st.write("DCF Analysis Result:")
                        st.write(dcf_response)
                    except Exception as e:
                        st.error(f"Error with DCF calculation: {e}")
                agree = st.checkbox("Add DCF Analysis", 
                                    value = st.session_state.get("Discounted Cash Flow Analysis", False))

                st.session_state["Discounted Cash Flow Analysis"] = sample_dfc_str if agree else False

            with valuation_tabs[1]:
                if st.button("Calculate LBO Analysis"):
                    try:
                        # Generate LBO response
                        lbo_response = query_agent(agent=llm, query=lbo_query)
                        st.write("LBO Analysis Result:")
                        st.write(lbo_response)
                    except Exception as e:
                        st.error(f"Error with LBO calculation: {e}")
                agree = st.checkbox("Add LBO Analysis", 
                                    value = st.session_state.get("Leveraged Buyout Analysis", False))

                st.session_state["Leveraged Buyout Analysis"] = sample_lbo_str if agree else False


        else:
            st.info("Please upload a CSV or Excel file.")

def show_valuation_empty():
    valuation_tabs = st.tabs(["DCF", "LBO"])
    with valuation_tabs[0]:
        st.info("Please upload a CSV or Excel file.")
        agree = st.checkbox("Add DCF Analysis", 
                            value = st.session_state.get("Discounted Cash Flow Analysis", False))

        st.session_state["Discounted Cash Flow Analysis"] = sample_dfc_str if agree else False

    with valuation_tabs[1]:
        st.info("Please upload a CSV or Excel file.")
        agree = st.checkbox("Add LBO Analysis", 
                            value = st.session_state.get("Leveraged Buyout Analysis", False))

        st.session_state["Leveraged Buyout Analysis"] = sample_lbo_str if agree else False
