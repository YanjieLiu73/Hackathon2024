##### import the backend function
import os
import sys
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'AutoGen', 'backend')
sys.path.append(backend_path)

import asyncio
# from main import overview, recent_news_trends, financial_info, oppotunities_competition_info, geographic, M_n_A_profile


def get_financial_report(test=False, ticker=None):

    """
    get the financial report calling backend function
        test_mode with input test=True, input sample result

    return:
        result = Dict[function_name(str), response(str)]
    """
    
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
        result = {}

        # TODO: ticker - company_name map
        # res = asyncio.run(financial_info("GOOGLE"))
        
        # TODO: function_name - function map
        # result['financial_info'] = res.messages[-1].content

        # TODO: other keys - default ''
        
        return result

if __name__ == '__main__':
    print(get_financial_report(False, 'GOOGL'))