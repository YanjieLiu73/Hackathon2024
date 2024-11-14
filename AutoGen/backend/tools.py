import pandas as pd
from langchain_community.vectorstores import FAISS
import os

import vector_store
import matplotlib.pyplot as plt
##################################################
# yahoo finance
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, '..', "..", 'Data')
df_financial = pd.read_csv(data_path + "/financials_SP500_hack/" + "financials.csv")
df_statements = pd.read_csv(data_path + "/financial_statement_hack/" + "Financial Statements.csv")


def stock_prices(ticker: str) -> pd.DataFrame:
    """
    Get the historical prices and volume for a ticker for the last month.

    Args:
    ticker (str): the stock ticker to be given to yfinance

    """
    # Construct the relative path to the target data folder
    import os
    filepath = os.path.join(data_path, 'stock_price')

    # get the historical data (max 10yr)
    df = pd.read_csv(os.path.join(filepath, f'{ticker}.csv'), index_col=0)
    df.index = df.index.astype('datetime64[ns, America/New_York]')

    return df.loc['2014-01-01':]


# def stock_news(ticker: str) -> list:
#     """
#     Get the most recent news of a stock or an instrument from Yahoo Finance
#
#     Args:
#     ticker (str): the stock ticker to be given to yfinance
#     """
#
#     return []
# get the information


# get the information
def sector_top_caps(ticker: str, save_dir=None, df_financials=df_financial, top_k=10):
    sector = df_financials[df_financials['Symbol'] == ticker]['Sector'].item()
    df_sector = df_financials[df_financials['Sector'] == sector]

    df_sorted = df_sector.sort_values(by=['Market Cap'], ascending=False).iloc[:top_k]

    plt.figure(figsize=(10, 8))
    plt.pie(df_sorted['Market Cap'], labels=df_sorted['Symbol'], autopct='%1.1f%%', startangle=140)

    if not save_dir == None:
        plt.savefig(save_dir)

    plt.title(f"{sector} sector top {top_k} market cap companies relative ratios")
    plt.show()

    return df_sorted[['Symbol', 'Name', 'Market Cap', 'Price/Earnings', 'Earnings/Share', 'Price/Sales']]


def ts_bar_charts(ticker: str, col: str, save_dir=None, df_financial_statements=df_statements):
    df_company = df_financial_statements[df_financial_statements['Company '] == ticker]

    plt.bar(df_company['Year'], df_company[col])

    if not save_dir == None:
        plt.savefig(save_dir)
    plt.xlabel('Year')
    plt.ylabel(col)
    plt.show()

    return df_company

def db_retrieve(db: vector_store.FAISS_manager, query: str, top_k: int = 2) -> list:
    """
    Retrieve the relevant information and print out
    """
    resources = db.search(query, top_k=top_k)

    result = []
    for resource in resources:
        metadata = resource.metadata
        content = resource.page_content

        result.append({
            'metadata': metadata,
            'content': content
        })
        # text = f"From document {metadata['source']} page {metadata['page']}, we have following information. \n {content} \n"
        # text_result = text_result + text

    return result


def get_stock_overview(ticker: str) -> pd.DataFrame:
    df_stock_overview = df_financial[df_financial['Symbol'] == ticker]

    # plotting relevant information


    return df_stock_overview


# news retrieve
def news_retrieve(query: str) -> list:
    return db_retrieve(vector_store.news_db, query)

def research_retrieve(query: str) -> list:
    return db_retrieve(vector_store.research_db, query)

def sec_filling_retrieve(query: str) -> list:
    return db_retrieve(vector_store.sec_filling_db, query)