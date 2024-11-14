import streamlit as st
from streamlit_free_text_select import st_free_text_select
from page_modules.profiler import show_profiler
from page_modules.chat_bot import show_chat_bot
from page_modules.valuation import show_valuation
from page_modules.Introduction import show_overview  # Import the Overview function
from page_modules.call_backend import get_financial_report
from page_modules.utilities import save_content_to_ppt, save_content_to_pdf
from page_modules.about import show_about
from page_modules.help import show_help

import pandas as pd

st.set_page_config(
    page_title="Pitcher",
    layout="wide",
    initial_sidebar_state="expanded"
    )

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("barclays.PNG", use_container_width=True)

st.markdown(
    """
    <style>
    img{
    width: 30% !important;
    padding-top:15px;
    gap:0.5rem;
    }
    </style> 
""", 
unsafe_allow_html=True
 )

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

# layout for "Company/ Ticker" input and Start button
st.markdown("#### Company/ Ticker")
ticker_options = [ "AAL", "AAPL", "AMZN", "GOOGL", "JBLU", "LUV", "META", "NVDA", "SAVE", "UAL"]
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
    st.session_state["started"] = True
    result = get_financial_report(ticker = company_ticker, test = False)


# Initialize session state for "started" if not already set
if "started" not in st.session_state:
    st.session_state["started"] = False
    
# Adjust the number as needed to create more space
for _ in range(5):  
    st.sidebar.write("")
# Navigation using st.radio for persistent state
add_styling()
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["Profiler", "Chat Bot", "Valuation", "About", "Help"], label_visibility="collapsed")

# Only display the content if "Start" button has been clicked
if st.session_state["started"]:
    
    # Set the selected page in session state for tracking
    st.session_state["page"] = page

    if st.session_state["page"] == "Profiler":
        show_profiler(result)
    elif st.session_state["page"] == "Chat Bot":
        show_chat_bot()
    elif st.session_state["page"] == "Valuation":
        show_valuation()
    elif st.session_state["page"] == "About":
        show_about()
    elif st.session_state["page"] == "Help":
        show_help()

    st.sidebar.markdown("### Output")
    possible_slides = ["Overview", "Financials", "Geographic Mix", "Management",
                       "Recent News", "M&A Profile", "Miscellanea", "Discounted Cash Flow Analysis", "Leveraged Buyout Analysis"]
    for title in possible_slides:
        if st.session_state.get(title, False):
            st.sidebar.markdown(title)
    # Download presentation
    if st.sidebar.button("Download Slides", key=page+"_ppt"):
        save_content_to_ppt(company_ticker)
        st.write("The slides have been downloaded successfully.")
    if st.sidebar.button("Download Report", key=page+"_pdf"):
        save_content_to_pdf(company_ticker)
        st.write("The report has been downloaded successfully.")
else:
    show_overview()
    
# Display slides which will be included in presentation
if st.session_state.get("page", False) in ["Profiler", "Chat Bot", "Valuation", "About", "Help"]:
    # File uploader in the sidebar
    # Add some space at the top of the sidebar
    for _ in range(20):  # Adjust the number as needed to create more space
        st.sidebar.write("")

    st.sidebar.markdown("### Upload a File")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"], key="file_uploader")

    # Display uploaded file info (for demonstration)
    if uploaded_file is not None:
        st.sidebar.write(f"Uploaded file: {uploaded_file.name}")
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            st.write("### Uploaded Excel File Content")
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded CSV File Content")
        elif uploaded_file.type == "application/pdf":
            st.write("PDF files cannot be displayed directly here, but they are uploaded successfully.")

        
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