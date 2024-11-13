from vector_store import initialize_vector_store
from backend import team, dialog_print

import os
import pathlib
import time
import asyncio

global sec_filling_db
global research_db
global news_db

import glob
import pickle


### initializing the data store

# pre-defined
cwd = pathlib.Path.cwd()
data_folder = f"{cwd}/../../Data"
#
file_mapping = {
    'sec_filling': f"{data_folder}/10k_mini/",
    'research_report': f'{data_folder}/research_reports_mini/',
    'news': f'{data_folder}/news_mini/',
}

if len(glob.glob(f"{cwd}/../../faiss-db/*/*.faiss")) == 0:
    initialize_vector_store(file_mapping)
else:
    initialize_vector_store(None)

print('done with vector store init\n')


# The part which needs to be called at front end
async def frontend_run():
    basic_info_team = team(['news_analysis_agent', 'report_agent'])
    result =await basic_info_team.run("What's trump victory mean for google")
    dialog_print(result)


def save_results(filename : str, result):
    dir = os.path.join(os.path.dirname(__file__), 'output')
    with open(os.path.join(dir, filename + '_diaglog.pkl'), 'wb') as f:
        pickle.dump(result, f)
    with open(os.path.join(dir, filename + ".md"), 'w') as f:
        f.write(result.messages[-1].content)

# question 1, 2,3, 4, 5, 6
async def overview(company):
    overview_info_team = team(['sec_filling_report_analysis_agent', 'report_agent'])
    questions = [
        "When was the company founded?",
        "What does the company do and what are their key products?",
        "What is the company's monetization model?",
        "Who is the company's target customer?",
        "Who owns the company?",
        "Any marquee customer logos?"
    ]

    result = await overview_info_team.run(
        f"Elaborate each question, and give me as more information as possible for {company}?\n" + "\n".join(questions))

    save_results('overview', result)
    # overview_info_team.dialog_print(result)
    return result

# question 8, 9, 10, 11
async def recent_news_trends(company):
    news_trend_team = team(['sec_filling_report_analysis_agent', 'news_analysis_agent', 'stock_price_analysis_agent', 'report_agent'])

    questions = [
        "Recent news?",
        "What has the company's stock price growth been like?",
        "What is the company's profitability been like?",
        "Has the company indicated any materials change to its business operations?",
    ]

    result = await news_trend_team.run(
        f"Elaborate each question, and give me as more information as possible for {company}?\n" + "\n".join(questions))

    save_results('recent_news_trends', result)
    return result


# question  13, 14, 15, 16, 17
async def financial_info(company):
    financial_info_team = team(['sec_filling_report_analysis_agent', 'news_analysis_agent', 'research_report_analysis_agent', 'stock_price_analysis_agent', 'report_agent'])

    questions = [
        "If the company is public, how is its share price look like?",
        "If the company is public, how have its valuation multiples performed?",
        "What is the company's overall financial profile?",
        "If the company is public, what is the current consensus equity research views on its projections and business performances? What are the target prices and ratings? ",
        "If the company if private, are there any indications to its value? (e.g. procedent capital raises, parent valuation marks, prior transactions)"
    ]

    result = await financial_info_team.run(
        f"Elaborate each question, and give me as more information as possible for {company}?\n" + "\n".join(questions))

    save_results('financial_info', result)
    return result

# question 18, 19
async def oppotunities_competition_info(company):
    oppo_compet_team = team(['news_analysis_agent', 'research_report_analysis_agent', 'report_agent'])

    questions = [
        "Who are company's competitors?",
        "How big is the company's addressable market?",
    ]

    result = await oppo_compet_team.run(
        f"Elaborate each question, and give me as more information as possible for {company}?\n" + "\n".join(questions))

    save_results('oppotunities_competition_info', result)
    return result

# question 20, 21
async def geographic(company):
    geographic_team = team(['sec_filling_report_analysis_agent', 'report_agent'])

    questions = [
        "Where is company based?",
        "What geographies does the company operate in/has offices in?",
    ]

    result = await geographic_team.run(
        f"Elaborate each question, and give me as more information as possible for {company}?\n" + "\n".join(questions))

    save_results('geographic', result)
    return result

# question 22, 23
async def M_n_A_profile(company):
    M_n_A_profile_team = team(['news_analysis_agent', 'research_report_analysis_agent', 'report_agent'])

    questions = [
        "Has the company engaged in any mergers and acquisitions activity?(completed, announced or terminated)",
        "Has the company indicated that it is looking to sell itself or any of its divisions or to buy something?",
    ]

    result = await M_n_A_profile_team.run(
        f"Elaborate each question, and give me as more information as possible for {company} in 2023?\n" + "\n".join(questions))

    save_results('M_n_A_profile', result)
    return result


# main()


# result = asyncio.run(overview("GOOGLE"))
# result = asyncio.run(recent_news_trends("GOOGLE"))
# result = asyncio.run(financial_info("GOOGLE"))
# result = asyncio.run(oppotunities_competition_info("GOOGLE"))
# result = asyncio.run(geographic("GOOGLE"))
# result = asyncio.run(M_n_A_profile("GOOGLE"))


# dialog_print(result)
