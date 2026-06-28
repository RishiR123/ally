import os
from dotenv import load_dotenv

def get_config_path():
    return os.path.expanduser("~/.ally/.env")

# Load environment variables from global .env file
load_dotenv(get_config_path())

class Config:
    """Configuration settings for Ally."""
    
    @classmethod
    def get_base_url(cls):
        return os.getenv("ALLY_API_BASE_URL", "https://api.openai.com/v1")

    @classmethod
    def get_api_key(cls):
        return os.getenv("ALLY_API_KEY", "not-needed-for-local")

    @classmethod
    def get_model(cls):
        return os.getenv("ALLY_MODEL", "gpt-3.5-turbo")

    @classmethod
    def get_openai_client_kwargs(cls):
        """Returns kwargs suitable for initializing the OpenAI client."""
        base_url = cls.get_base_url()
        api_key = cls.get_api_key()
        
        kwargs = {
            "api_key": api_key,
        }
        if base_url and base_url != "https://api.openai.com/v1":
            kwargs["base_url"] = base_url
        return kwargs
