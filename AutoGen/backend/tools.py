import pandas as pd
from langchain_community.vectorstores import FAISS

import vector_store
##################################################
# yahoo finance

def stock_prices(ticker: str) -> pd.DataFrame:
    """
    Get the historical prices and volume for a ticker for the last month.

    Args:
    ticker (str): the stock ticker to be given to yfinance

    """
    # Construct the relative path to the target data folder
    import os
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, '..', "..", 'Data', 'stock_price')

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




# news retrieve
def news_retrieve(query: str) -> list:
    return db_retrieve(vector_store.news_db, query)

def research_retrieve(query: str) -> list:
    return db_retrieve(vector_store.research_db, query)

def sec_filling_retrieve(query: str) -> list:
    return db_retrieve(vector_store.sec_filling_db, query)