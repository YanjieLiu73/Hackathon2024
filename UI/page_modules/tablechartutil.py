import os
import sys
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'AutoGen', 'backend')
sys.path.append(backend_path)

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from tools import stock_prices, sector_top_caps

tablechart = os.path.join(os.path.dirname(__file__), 'tablechart')


def gen_stock_cumret_plot(ticker):
    """generate cumulative stock return price

    Args:
        ticker (_type_): _description_
    """

    def calc_ret(df, ticker):
        df[ticker] = df.pct_change()['Close']
        return df[[ticker]]

    cumlist = []
    for tick in [ticker, 'SPX']:
        df = stock_prices(tick)
        df = df.loc['2019-01-01':]
        ret = calc_ret(df, tick)
        cumret = (1+ret).cumprod()-1
        cumlist.append(cumret)
    res = pd.concat(cumlist, axis = 1).dropna()
    
    fig, ax = plt.subplots(1,1, figsize = (16, 6))
    res.plot(ax = ax, color = ['tab:orange', 'tab:blue'])
    ax.set_title(f'cumulative stock return of {ticker} vs S&P', fontsize = 16)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
    ax.set_ylabel('cumulative return')
    ax.set_xlabel('time')
    plt.savefig(os.path.join(tablechart, f'{ticker}_cumret.png'))
    

def gen_competitors_table(ticker):
    """generate the competitors table

    Args:
        ticker (_type_): _description_
    """
    df = sector_top_caps(ticker)
    def highlight_ticker(s):
        return ['color: blue; font-weight: bold' if s['Symbol'] == ticker else '' for _ in s]
    styled_df = df.style.apply(highlight_ticker, axis=1).format({'Market Cap': '{:.2e}'}, precision=2)
    return styled_df


def gen_pie_chart(ticker, top_k=10):
    """generate stock section Market Cap pie chart from financials.csv

    Args:
        ticker (_type_): _description_
    """
    
    import numpy as np
    from matplotlib import cm
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'financials_SP500_hack','financials.csv')
    df_financials = pd.read_csv(filepath)
    
    sector = df_financials[df_financials['Symbol'] == ticker]['Sector'].item()
    df_sector = df_financials[df_financials['Sector'] == sector]
    df_sorted = df_sector.sort_values(by=['Market Cap'], ascending=False).iloc[:top_k]
    colors = cm.Blues(np.linspace(0.3, 0.7, len(df_sorted)))
    
    fig, ax = plt.subplots(1,1,figsize=(10, 8))
    ax.pie(df_sorted['Market Cap'], labels=df_sorted['Symbol'], autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title(f'Market Cap of Competitors')
    plt.savefig(os.path.join(tablechart, f'{ticker}_pie.png'))
    

def plot_rev_ebit(ticker):
    """generate Revenue EBITDA plot

    Args:
        ticker (_type_): _description_
    """
    filename = f'{ticker}_finsnap.png'
    if ticker == 'GOOGL':
        ticker = 'GOOG'
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'financial_statement_hack','Financial Statements.csv')
    fin_stmt_df = pd.read_csv(filepath)
    cols = ['Revenue','EBITDA']
    df = fin_stmt_df.loc[fin_stmt_df["Company "]==ticker,cols+["Debt/Equity Ratio","Year"]].set_index("Year").sort_index()
    df[cols].plot(kind='bar', figsize = (15,10), color=[ 'deepskyblue', 'navy'])

    plt.title(f"Financial Snapshot")
    plt.ylabel("$ USD")
    
    plt.savefig(os.path.join(tablechart, filename))
    

def generate_financial_tab(ticker):
    """call above functions for profiler - financials tables and charts

    Args:
        ticker (_type_): _description_
    """
    gen_stock_cumret_plot(ticker)
    styled_df = gen_competitors_table(ticker)
    gen_pie_chart(ticker)
    plot_rev_ebit(ticker)
    return styled_df
    
if __name__ == '__main__':
    # gen_stock_cumret_plot('AAPL')
    
    # styled_df = gen_competitors_table('GOOGL')
    # styled_df.to_excel(os.path.join(tablechart, 'sample.xlsx'))
    
    # gen_pie_chart('AAPL')
    
    # plot_rev_ebit('AAPL')
    
    generate_financial_tab('GOOGL')