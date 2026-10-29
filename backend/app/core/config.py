from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url:str
    anthropic_api_key:str
    claude_model:str="claude-sonnet-4-6"
    openai_api_key:str
    embedding_model:str="text-embedding-3-small"
    embedding_dim: int =1536
    environment:str ="development"
    cors_origins:str =""
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

    @property
    def cors_origin_list(self)->list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

settings=Settings()
