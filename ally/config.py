import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for Ally."""
    
    # Provider settings (Defaults to OpenAI if not set, but can be LM Studio e.g. http://localhost:1234/v1)
    BASE_URL = os.getenv("ALLY_API_BASE_URL", "https://api.openai.com/v1")
    API_KEY = os.getenv("ALLY_API_KEY", "not-needed-for-local")
    MODEL = os.getenv("ALLY_MODEL", "gpt-3.5-turbo") # Default model name, override in .env for local

    @classmethod
    def get_openai_client_kwargs(cls):
        """Returns kwargs suitable for initializing the OpenAI client."""
        kwargs = {
            "api_key": cls.API_KEY,
        }
        if cls.BASE_URL and cls.BASE_URL != "https://api.openai.com/v1":
            kwargs["base_url"] = cls.BASE_URL
        return kwargs
