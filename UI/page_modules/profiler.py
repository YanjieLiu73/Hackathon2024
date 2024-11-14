import os
import sys
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tablechartutil import generate_financial_tab

# Sample data for financials and geographic distribution
####
data = {
    "Region": ["North America", "Europe", "Asia"],
    "Revenue": [120000, 85000, 100000],
    "Profit": [20000, 15000, 18000]
}
df = pd.DataFrame(data)

def create_bar_chart():
    fig, ax = plt.subplots()
    ax.bar(df["Region"], df["Revenue"], color="skyblue")
    ax.set_title("Revenue by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Revenue ($)")
    fig_path = "result/bar_chart.png"
    plt.savefig(fig_path)  # Save the chart as an image file
    plt.close(fig)
    return fig_path

def show_profiler(result):
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
#     css = '''
#     <style>
#         .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
#         font-size:18px;
#         }
#         .stTabs [data-baseweb="tab-highlight"] {
#             background-color:transparent;
#         }
#         .stTabs [data-baseweb="tab-border"] { 
#                 background-color: transparent;
#             }
#     </style>
#     '''
#     st.markdown(css, unsafe_allow_html=True)

    # Profiler sub-tabs, map to result key
    tab_list = ["Overview", "Financials", "Geographic Mix", "Management", "Recent News", "M&A Profile", "Miscellaneous"]
    res_key = ["overview", "financial_info", "geographic", "management_info", "recent_news_trends", "M_n_A_profile", "oppotunities_competition_info"]
    tab_key_map = dict(zip(tab_list, res_key))
    profiler_tabs = st.tabs(tab_list)

    # Collect content for each tab
    with profiler_tabs[0]:

        # display 
        tab = "Overview"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False

    
    with profiler_tabs[1]:
        
        # display
        tab = "Financials"
        # res_str = result[tab_key_map[tab]]
        # st.write(res_str)
        
        ticker = result['ticker']
        tablechart = os.path.join(os.path.dirname(__file__), 'tablechart')
        styled_df = generate_financial_tab(ticker)
        
        
        st.subheader('Historical Stock Price Performance')
        st.image(os.path.join(tablechart, f'{ticker}_cumret.png'), width = 2000)
        
        st.subheader('Sector Comparison')
        col1, col2 = st.columns(2)
        with col1:
            st.table(styled_df)
        with col2:
            st.image(os.path.join(tablechart, f'{ticker}_pie.png'), width = 1000)
            
        st.subheader('Financial Snapshot')
        st.image(os.path.join(tablechart, f'{ticker}_finsnap.png'), width = 1200)
        
        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False

    
    with profiler_tabs[2]:
        
        # display 
        tab = "Geographic Mix"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False

    
    with profiler_tabs[3]:
        
        # display 
        tab = "Management"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False
        

    with profiler_tabs[4]:
        
        # display 
        tab = "Recent News"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False


    with profiler_tabs[5]:
        
        # display 
        tab = "M&A Profile"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False
        
    with profiler_tabs[6]:
        
        # display 
        tab = "Miscellaneous"
        res_str = result[tab_key_map[tab]]
        st.write(res_str)

        # download ppt
        agree = st.checkbox(f"Add {tab}",
                            value = st.session_state.get(tab, False))
        st.session_state[tab] = res_str if agree else False
