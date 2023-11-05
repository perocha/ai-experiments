from autogen import AssistantAgent, UserProxyAgent, get_config_list
import os


api_type = "azure"
endpoint = "https://perocha.openai.azure.com"
model = "gpt-35-turbo"
model_version = "2023-05-15"
azure_api_key = "f712a34b52a740d0a6f8fe36fc7ed198"

config_list = get_config_list(
    api_keys=[azure_api_key],
    api_bases=[endpoint],
    api_type=api_type,
    api_version=model_version
)

print(config_list)


assistant = AssistantAgent(name="Assistant", llm_config=config_list)

user_proxy = UserProxyAgent(name="user_proxy", code_execution_config={"work_dir": "coding"}, llm_config=config_list)
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")