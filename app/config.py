from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ERP AI Assistant"
    app_env: str = "dev"
    debug: bool = True
    secret_key: str = "change_me"
    api_prefix: str = "/api/v1"
    access_token_expire_minutes: int = 480

    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "erp_ai"
    postgres_user: str = "erp_ai_user"
    postgres_password: str = "erp_ai_pass"

    llm_api_key: str = "your_key"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_chat_model: str = "gpt-4.1-mini"
    llm_embedding_model: str = "text-embedding-3-small"

    onec_base_url: str = "http://onec-server/ut/odata/standard.odata"
    onec_http_service_url: str = "http://onec-server/ut/hs/ai"
    onec_username: str = "svc_ai"
    onec_password: str = "secret"

    sync_sales_cron: str = "*/15 * * * *"
    sync_products_cron: str = "0 * * * *"
    sync_customers_cron: str = "15 * * * *"
    sync_balances_cron: str = "*/10 * * * *"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
