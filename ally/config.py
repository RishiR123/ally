import os
import yaml

def get_config_path():
    return os.path.expanduser("~/.ally/config.yaml")

class Config:
    """Configuration settings for Ally."""
    _config_data = {}

    @classmethod
    def load(cls):
        path = get_config_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                cls._config_data = yaml.safe_load(f) or {}

    @classmethod
    def get_base_url(cls):
        url = cls._config_data.get('llm', {}).get('base_url', "https://api.openai.com/v1")
        if url and not url.endswith("/v1") and "api.openai.com" not in url:
            if url.endswith("/"):
                url += "v1"
            else:
                url += "/v1"
        return url

    @classmethod
    def get_api_key(cls):
        return cls._config_data.get('llm', {}).get('api_key', "not-needed-for-local")

    @classmethod
    def get_model(cls):
        return cls._config_data.get('llm', {}).get('model', "gpt-3.5-turbo")

    @classmethod
    def get_mcp_servers(cls):
        return cls._config_data.get('mcp_servers', {})

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
