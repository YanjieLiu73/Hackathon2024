import streamlit as st
import time
from streamlit_free_text_select import st_free_text_select
from page_modules.profiler import show_profiler
from page_modules.chat_bot import show_chat_bot
from page_modules.valuation import show_valuation, show_valuation_empty
from page_modules.Introduction import show_overview  # Import the Overview function
from page_modules.call_backend import get_financial_report
from page_modules.utilities import save_content_to_ppt, save_content_to_pdf
from page_modules.about import show_about
from page_modules.help import show_help

import pandas as pd

def add_styling():
    st.html("""
        <style>
            /* convert radio to list of buttons */
            div[role="radiogroup"] {
                flex-direction:column;
            }
            input[type="radio"] + div {
                background: #003366 !important;
                color: white;
                font-size: 18px !important;
                border-radius: 10px !important;
                padding: 10px 20px !important;
                width: 160px !important;
                display: flex;
                justify-content: center; 
                align-items: center;
                box-sizing: border-box;
            }
            input[type="radio"] + div p {
                font-size: 18px !important;
            }
            input[type="radio"][tabindex="0"] + div {
                background: #00bfff !important;
                color: white !important;
            }
            input[type="radio"][tabindex="0"] + div p {
                color: white !important;
                font-size: 18px !important;
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
    
### Output
def output(page, company_ticker):
    st.sidebar.markdown("### Output")
    possible_slides = ["Overview", "Financials", "Geographic Mix", "Management",
                       "Recent News", "M&A Profile", "Miscellanea", "Discounted Cash Flow Analysis", "Leveraged Buyout Analysis"]
    for title in possible_slides:
        if st.session_state.get(title, False):
            st.sidebar.markdown(title)
    # Download presentation

    if st.sidebar.button("Download Slides", key=page+"_ppt"):
        save_content_to_ppt(company_ticker)
        st.sidebar.info("The slides have been downloaded successfully.")
    if st.sidebar.button("Download Report", key=page+"_pdf"):
        save_content_to_pdf(company_ticker)
        st.sidebar.info("The report has been downloaded successfully.")

### Upload
def upload():
    for _ in range(10):  # Adjust the number as needed to create more space
        st.sidebar.write("")
    st.sidebar.markdown("## Upload a File")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"], key="file_uploader")
    if uploaded_file is not None:
        st.sidebar.write(f"Uploaded file: {uploaded_file.name}")
    return uploaded_file
    
st.set_page_config(
    page_title="Pitcher",
    layout="wide",
    initial_sidebar_state="expanded"
    )

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("pitcher.PNG", use_column_width=True)

st.markdown(
    """
    <style>
    img{
    width: 70% !important;
    padding-top:15px;
    gap:0.5rem;
    }
    </style> 
""", 
unsafe_allow_html=True
 )


### Sidebar
for _ in range(2):  # Adjust the number as needed to create more space
    st.sidebar.write("#### ")
    
### Navigation using st.radio for persistent state
add_styling()
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["Profiler", "Chat Bot", "Valuation", "About", "Help"],index=None, label_visibility="collapsed")
company_ticker = None

    
if "page" not in st.session_state:
    st.session_state["page"] = "Intro"
else:
    st.session_state["page"] = page # Set the selected page in session state for tracking

ticker_options = [ "AAL", "AAPL", "AMZN", "GOOGL", "JBLU", "LUV", "META", "NVDA", "SAVE", "UAL"]

if st.session_state["page"] == "Profiler":    
    # layout for "Company/ Ticker" input and Start button
    st.markdown("##### Company Ticker")
    company_ticker = st_free_text_select(
        label=None,
        options=ticker_options,
        index=None,
        format_func=lambda x: x.upper(),
        placeholder="Hello! Please select or enter a company ticker🤓",
        disabled=False,
        delay=300,
        label_visibility="visible",
    )

    if company_ticker:
        result = get_financial_report(ticker = company_ticker, test = True)
        with st.spinner("PITCHER Running..."):
            time.sleep(5)
            show_profiler(result)
        output(page, company_ticker)
        upload() #decoration
    else:
        st.info("Please select or enter a company ticker")
        
elif st.session_state["page"] == "Chat Bot":
    st.markdown("##### Company Ticker")
    company_ticker = st_free_text_select(
        label=None,
        options=ticker_options,
        index=None,
        format_func=lambda x: x.upper(),
        placeholder="Hello! Please select or enter a company ticker🤓",
        disabled=False,
        delay=300,
        label_visibility="visible",
    )

    if company_ticker:
        upload() #decoration
        show_chat_bot(company_ticker)
elif st.session_state["page"] == "Valuation":
    uploaded_file = upload()
    if uploaded_file is not None:  
        show_valuation(uploaded_file)
    else:
        show_valuation_empty()
elif st.session_state["page"] == "About":
    show_about()
elif st.session_state["page"] == "Help":
    show_help()
else:
    show_overview()

        
css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:18px;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color:transparent;
    }
    .stTabs [data-baseweb="tab-border"] { 
            background-color: transparent;
        }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

st.markdown(
    """
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #00bfff;  padding: 2px; text-align: right;'>
        <p style='color: white; height: 20px font-size: 10px;'>&copy; 2024 Hackathon Team QuantifAI</p>
    </div>
    """,
    unsafe_allow_html=True
)