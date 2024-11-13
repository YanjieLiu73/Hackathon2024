import streamlit as st
from page_modules.profiler import show_profiler
from page_modules.chat_bot import show_chat_bot
from page_modules.valuation import show_valuation
from page_modules.Introduction import show_overview  # Import the Overview function
from page_modules.call_backend import get_financial_report
from page_modules.utilities import save_content_to_ppt, save_content_to_pdf

import pandas as pd

def add_styling():
    st.html("""
        <style>
            /* convert radio to list of buttons */
            div[role="radiogroup"] {
                flex-direction:column;
            }
            input[type="radio"] + div {
                background: #63ADD2 !important;
                color: #FFF;
                border-radius: 8px !important;
                padding: 8px 18px !important;
            }
            input[type="radio"][tabindex="0"] + div {
                background: #E6FF4D !important;
                color: #17455C !important;
            }
            input[type="radio"][tabindex="0"] + div p {
                color: #17455C !important;
            }
            div[role="radiogroup"] label > div:first-child {
                display: none !important;
            }
            div[role="radiogroup"] label {
                margin-right: 0px !important;
            }
            div[role="radiogroup"] {
                gap: 12px;
            }
        </style>
    """)

# Sidebar layout for "Company/ Ticker" input and Start button
st.sidebar.markdown("### Company/ Ticker")
company_ticker = st.sidebar.text_input("Enter Company/Ticker", key="company_ticker")

# Start button below the company ticker input
if st.sidebar.button("Start"):
    st.session_state["started"] = True

# Initialize session state for "started" if not already set
if "started" not in st.session_state:
    st.session_state["started"] = False
    
# Navigation using st.radio for persistent state
add_styling()
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["Profiler", "Chat Bot", "Valuation"], label_visibility="collapsed")

# Only display the content if "Start" button has been clicked
if st.session_state["started"]:

    result = get_financial_report(test = True, ticker = company_ticker)
    
    # Set the selected page in session state for tracking
    st.session_state["page"] = page

    #st.markdown('<div class="main-content">', unsafe_allow_html=True)
    # Display the selected page content
    if st.session_state["page"] == "Profiler":
        show_profiler(result)
    elif st.session_state["page"] == "Chat Bot":
        show_chat_bot()
    elif st.session_state["page"] == "Valuation":
        show_valuation()
    #st.markdown('</div>', unsafe_allow_html=True)
else:
    # Display a message prompting the user to click the Start button
    st.write("Please enter a Company/Ticker and click the Start button to begin.")
    show_overview()
    
# File uploader in the sidebar
st.sidebar.markdown("### Upload a File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"], key="file_uploader")

# Display uploaded file info (for demonstration)
if uploaded_file is not None:
    st.sidebar.write(f"Uploaded file: {uploaded_file.name}")
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        st.write("### Uploaded Excel File Content")
        st.dataframe(df)
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded CSV File Content")
        st.dataframe(df)
    elif uploaded_file.type == "application/pdf":
        st.write("PDF files cannot be displayed directly here, but they are uploaded successfully.")

# Display slides which will be included in presentation
if st.session_state["started"]:
    st.sidebar.markdown("### Output")
    possible_slides = ["Overview", "Financials", "Geographic Mix", "Management Information",
                       "Recent News", "Discounted Cash Flow Analysis", "Leveraged Buyout Analysis"]
    for title in possible_slides:
        if st.session_state.get(title, False):
            st.sidebar.markdown(title)
    # Download presentation
    if st.sidebar.button("Download Slides", key=page+"_ppt"):
        save_content_to_ppt()
    if st.sidebar.button("Download Report", key=page+"_pdf"):
        save_content_to_pdf()