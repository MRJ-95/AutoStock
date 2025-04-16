from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini', encoding='utf-8')

# Print sections to verify if config.ini is being loaded correctly
print("Config Sections:", config.sections())

# Print the API key value
try:
    print("Alpha Vantage API Key:", config.get('alpha_vantage', 'api_key'))
except Exception as e:
    print("Error accessing alpha_vantage section:", str(e))



import os

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')
print("Checking path:", config_path)
print("File Exists:", os.path.exists(config_path))
