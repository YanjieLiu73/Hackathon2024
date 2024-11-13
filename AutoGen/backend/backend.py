# import os

# os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('Key_AzureOpenAI')
# os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('Endpoint_AzureOpenAI')

import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..' , '..', ".env")
load_dotenv(dotenv_path = env_path)
os.environ['AZURE_OPENAI_API_KEY'] = os.getenv('AZURE_OPENAI_API_KEY')
os.environ['AZURE_OPENAI_ENDPOINT'] = os.getenv('AZURE_OPENAI_ENDPOINT')

from autogen_agentchat.agents import CodingAssistantAgent, ToolUseAssistantAgent
from autogen_agentchat.task import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.components.tools import FunctionTool
from autogen_core.components.models import AzureOpenAIChatCompletionClient, UserMessage

import yaml

from tools import news_retrieve, sec_filling_retrieve, research_retrieve, stock_prices


llm_base = AzureOpenAIChatCompletionClient(
            model="gpt-4o",
            api_version="2024-02-01",
            model_capabilities={
                "vision":True,
                "function_calling":True,
                "json_output":True,
            }
        )

def agents(llm_base):
    ### tools registration
    stock_prices_tool = FunctionTool(stock_prices, description='Historical prices and volume for a ticker')
    sec_filling_retrieve_tool = FunctionTool(sec_filling_retrieve, description='Relevant 10k sec filling reports info for a question')
    report_retrieve_tool = FunctionTool(research_retrieve, description='Relevant research reports info for a question')
    news_retrieve_tool = FunctionTool(news_retrieve, description='Relevant recent news for a question')

    sec_filling_report_analysis_agent = ToolUseAssistantAgent(
        name='SEC_filling_report_analyst',
        model_client=llm_base,
        registered_tools=[sec_filling_retrieve_tool],
        description='uncover and review relevant information from 10k sec filling reports',
        system_message="You are a helpful assistant with stock pitch, use your tool to retrieve the most relevant information provided, indicate source of your findings"
    )

    research_report_analysis_agent = ToolUseAssistantAgent(
        name="research_report_analyst",
        model_client=llm_base,
        registered_tools=[report_retrieve_tool],
        description="uncover and review relevant information from research reports",
        system_message="You are a analyst, use your tools to find the most relevant information and present it in a clear and concise manner, indicate source of your findings",
    )

    news_analysis_agent = ToolUseAssistantAgent(
        name="news_analyst",
        model_client=llm_base,
        registered_tools=[news_retrieve_tool],
        description="uncover and review relevant information from research reports",
        system_message="You're a professional news analyst. Use the search tool provided and find the most relevant information and present it in a clear and concise manner, indicate source of your findings",
    )

    stock_price_analysis_agent = ToolUseAssistantAgent(
        name="stock_price_analyst",
        model_client=llm_base,
        registered_tools=[stock_prices_tool],
        description="Analyze the stock data, provide an overview.",
        system_message="You're a professional stock data analyst.",
    )

    report_agent = CodingAssistantAgent(
        name="Report_Agent",
        model_client=llm_base,
        description="Generate a report based on the search and reports analysis results in markdown format",
        system_message="You are a helpful assistant that can generate a comprehensive report on a given topic based on search and reports analysis results. When you done with generating the report, reply with TERMINATE.",
    )

    agents_mapping = {
        'sec_filling_report_analysis_agent': sec_filling_report_analysis_agent,
        'research_report_analysis_agent': research_report_analysis_agent,
        'news_analysis_agent': news_analysis_agent,
        'stock_price_analysis_agent': stock_price_analysis_agent,
        'report_agent': report_agent
    }

    return agents_mapping


class team:
    def __init__(self, particapants_list: list):
        self.llm_base = AzureOpenAIChatCompletionClient(
            model="gpt-4o",
            api_version="2024-02-01",
            model_capabilities={
                "vision":True,
                "function_calling":True,
                "json_output":True,
            }
        )

        agents_mapping = agents(self.llm_base)

        self.particapants = []
        for agents_name in particapants_list:
            self.particapants.append(agents_mapping[agents_name])


    async def run(self, query: str):
        termination = TextMentionTermination("TERMINATE")

        team = RoundRobinGroupChat(self.particapants,
                                   termination_condition=termination)

        result = await team.run(query)

        return result


def dialog_print(result):
    for message in result.messages:
        print(message.source + ":")
        print(message.content)
        print('________________________')