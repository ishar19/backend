from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(verbose=True)

class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env")
  
  DATABASE_URL: str
  OPENFOODFACTS_API_URL: str
  GEMINI_KEY: str

# global instance
settings = Settings()

