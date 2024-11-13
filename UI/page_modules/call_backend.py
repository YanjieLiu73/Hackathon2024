##### import the backend function
import os
import sys
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'AutoGen', 'backend')
sys.path.append(backend_path)

import asyncio
import main

## map backend functions in main.py
agg_functions = ['overview', 'recent_news_trends', 'financial_info', \
                 'oppotunities_competition_info', 'geographic', 'M_n_A_profile']

async def run_all_backend_functions(agg_functions, module, company):
    """
    Run all functions concurrently and store their results in a dictionary
    """
    
    results = await asyncio.gather(*[getattr(module, func_name)(company) for func_name in agg_functions])
    return {func_name: result.messages[-1].content for func_name, result in zip(agg_functions, results)}


def get_financial_report(ticker, test=False):

    """
    get the financial report calling backend function
        test_mode with input test=True, input sample result

    return:
        result = Dict[function_name(str), response(str)]
    """

    ticker = ticker.upper()
    
    if test:
        #### import sample markdown files
        
        import os
        filepath = os.path.join(backend_path, 'ui_sample_output')
        files = [f for f in os.listdir(filepath) if '.md' in f]

        # read in sample output in markdown file
        result = {}
        for f in files:
            with open(os.path.join(filepath, f), 'r') as file:
                res = file.read()
            result[f.split('.')[0]] = res.replace('TERMINATE', '')        
        return result

    else:
        #### call backend agent

        # TODO: ticker - company mapping
        result = asyncio.run(run_all_backend_functions(agg_functions, main, ticker))

        # format
        result = {k:v.replace('TERMINATE', '') for k,v in result.items()}
        
        return result

if __name__ == '__main__':
    print(get_financial_report('AAPL'))