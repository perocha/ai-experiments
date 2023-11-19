from config.notebook_config import *

print("Testing notebook_config.py...")
filename = "settings.json"

try:
    config = notebook_config(filename)
    config.load_config_from_file()

    # Print the config object with all its attributes, in a nice json format
    print(json.dumps(config.__dict__, indent=4, sort_keys=True))

except FileNotFoundError:
    config = notebook_config()
    config.ask_api_type()
    config.ask_endpoint()
    config.ask_model()
    config.ask_model_version()
    config.ask_api_key()
    config.save_config_to_file()
