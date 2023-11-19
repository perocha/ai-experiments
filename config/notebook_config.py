#
# Config class to store all the configuration variables
# Requests the user for the following information:
#   - Azure or OpenAI
#   - Azure Endpoint
#   - Azure Model
#   - Azure API Key
#
# This class will be used in Visual Studio Code, requesting input from the user from a Jupyter Notebook.
#
import json
import os

# Define default values
DEFAULT_API_TYPE = "azure"
DEFAULT_MODEL = "gpt-35-turbo"
DEFAULT_MODEL_VERSION = "2023-05-15"

class notebook_config:
    def __init__(self, config_file: str = '../config/settings.json'):
        self.config_file = config_file
        self.api_type = DEFAULT_API_TYPE
        self.endpoint = ""
        self.model = DEFAULT_MODEL
        self.model_version = DEFAULT_MODEL_VERSION
        self.azure_api_key = ""

    def ask_api_type(self):
        api_type = input("Which API would you like to use? (Azure or OpenAI): ").lower()
        if api_type == "azure":
            self.api_type = "azure"
        elif api_type == "openai":
            self.api_type = "openai"
        else:
            raise ValueError(f"Invalid API type {api_type}. Please enter either Azure or OpenAI.")

        self.save_config_to_file()

    def ask_endpoint(self):
        if self.api_type == "azure":
            endpoint = input("Please enter your endpoint: ")
            if endpoint == "":
                raise ValueError("Endpoint cannot be empty.")
            self.endpoint = endpoint
            self.save_config_to_file()

    def ask_model(self):
        if self.api_type == "azure":
            model = input(f"Please enter your model (press ENTER for {DEFAULT_MODEL}): ")
            if model == "":
                model = DEFAULT_MODEL
            self.model = model
            self.save_config_to_file()

    def ask_api_key(self):
        azure_api_key = input("Please enter your API key: ")
        if azure_api_key == "":
            raise ValueError("API key cannot be empty.")
        self.azure_api_key = azure_api_key
        self.save_config_to_file()

    def ask_model_version(self):
        if self.api_type == "azure":
            model_version = input(f"Please enter your model version (press ENTER for {DEFAULT_MODEL_VERSION}): ")
            if model_version == "":
                model_version = DEFAULT_MODEL_VERSION
            self.model_version = model_version
            self.save_config_to_file()

    def save_config_to_file(self):
        with open(self.config_file, "w") as f:
            json.dump(self.__dict__, f)

    def load_config_from_file(self):
        try:
            with open(self.config_file, "r") as f:
                self.__dict__ = json.load(f)
                # Load config to environment variables
                self.load_config_to_env()
        except FileNotFoundError:
            # Raise error if file not found
            raise FileNotFoundError(f"File {self.config_file} not found.")

    def load_config_to_env(self):
        if self.api_type == "azure":
            os.environ["OPENAI_API_TYPE"] = self.api_type
            os.environ["AZURE_OPENAI_KEY"] = self.azure_api_key
            os.environ["AZURE_OPENAI_ENDPOINT"] = self.endpoint
            os.environ["AZURE_OPENAI_API_BASE"] = self.endpoint
            os.environ["AZURE_OPENAI_MODEL"] = self.model
            os.environ["AZURE_OPENAI_MODEL_VERSION"] = self.model_version
        elif self.api_type == "openai":
            os.environ["OPENAI_API_TYPE"] = self.api_type
            os.environ["OPENAI_KEY"] = self.azure_api_key

    def get_config(self) -> dict:
        return self.__dict__

    def get_api_type(self) -> str:
        return self.api_type

    def get_endpoint(self) -> str:
        return self.endpoint

    def get_model(self) -> str:
        return self.model

    def get_model_version(self) -> str:
        return self.model_version
    
    def get_api_key(self) -> str:
        return self.azure_api_key
