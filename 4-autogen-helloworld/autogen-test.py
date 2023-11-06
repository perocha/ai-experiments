# Import the autogen module
from autogen import AssistantAgent, UserProxyAgent, get_config_list

# Instatiate the config class
import sys
sys.path.append("../config")
from notebook_config import notebook_config
config = notebook_config()
# Load config from file
config.load_config_from_file()

# Get the config
api_type = config.get_api_type()
endpoint = config.get_endpoint()
model = "gpt-35-turbo" # It's hardcoded in autogen to gpt4
model_version = config.get_model_version()
azure_api_key = config.get_api_key()
config_list = get_config_list(
    api_keys=[azure_api_key],
    api_bases=[endpoint],
    api_type=api_type,
    api_version=model_version
)
print(config_list)

assistant = AssistantAgent(name="Assistant", llm_config=config_list)

input_str = input("How can I help you? ")
user_proxy = UserProxyAgent(name="user_proxy", code_execution_config={"work_dir": "coding"}, llm_config=config_list)
user_proxy.initiate_chat(assistant, message=input_str)