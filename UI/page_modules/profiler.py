import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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
    fig_path = os.path.join(os.path.dirname(__file__),'..', 'result', 'bar_chart.png')
    plt.savefig(fig_path)  # Save the chart as an image file
    plt.close(fig)
    return fig_path

def show_profiler(result):
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Profiler sub-tabs
    profiler_tabs = st.tabs(["Overview", "Financials", "Geographic Mix", "Management", "Recent News"])

    # Collect content for each tab
    with profiler_tabs[0]:
        # overview_str = "This is the company overview with a sample paragraph.\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent nec nisl vel mauris blandit interdum."
        overview_str = result['overview']
        st.write("### Overview")
        st.write(overview_str)
        agree = st.checkbox("Add Overview to presentation",
                            value = st.session_state.get('Overview', False))

        st.session_state['Overview'] = overview_str if agree else False

    with profiler_tabs[1]:
        financials_str = "Financial Table:\n" + df.to_string()
        st.write("### Financial Table")
        st.dataframe(df)
        st.write("### Financial Bar Chart")
        chart_path = create_bar_chart()
        st.image(chart_path)
        agree = st.checkbox("Add Financials to presentation",
                            value = st.session_state.get("Financials", False))

        st.session_state["Financials"] = financials_str if agree else False
        st.session_state["chart_path"] = chart_path

    with profiler_tabs[2]:
        geographic_mix_str = "Geographic Distribution Table:\n" + df[["Region", "Revenue"]].to_string()
        st.write("### Geographic Distribution Table")
        st.dataframe(df[["Region", "Revenue"]])
        agree = st.checkbox("Add Geographic Mix to presentation",
                            value = st.session_state.get("Geographic Mix"))

        st.session_state["Geographic Mix"] = geographic_mix_str if agree else False

    with profiler_tabs[3]:
        management_str = "This section could include profiles or key information about the management team."
        st.write("### Management Information")
        st.write(management_str)
        agree = st.checkbox("Add Managment Information to presentation",
                            value=st.session_state.get("Management Information", False))

        st.session_state["Management Information"] = management_str if agree else False

    with profiler_tabs[4]:
        # news_str = "1. Company launches new product.\n2. Q3 earnings report shows positive growth.\n3. Expansion into new markets."
        news_str = result['news']
        st.write("### Recent News")
        st.write(news_str)
        agree = st.checkbox("Add Recent News to presentation",
                            value=st.session_state.get('Recent News', False))

        st.session_state["Recent News"] = news_str if agree else False
