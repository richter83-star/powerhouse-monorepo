"""
Application settings and configuration.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Powerhouse Multi-Agent Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Security
    secret_key: str = Field(
        ...,
        description="Secret key for JWT encoding",
        env="SECRET_KEY"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Keys (for enterprise clients)
    api_keys: list[str] = Field(
        ...,
        description="Valid API keys for authentication",
        env="API_KEYS"
    )
    
    # Database
    database_url: str = Field(
        ...,
        description="Database connection URL",
        env="DATABASE_URL"
    )
    
    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Agent Configuration
    max_agents_per_workflow: int = 19
    agent_timeout_seconds: int = 300
    
    # Workflow Configuration
    max_retry_attempts: int = 3
    workflow_timeout_seconds: int = 600
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    log_format: str = Field(
        default="text",
        description="Log format (text or json)"
    )
    
    # LLM Configuration
    abacusai_api_key: str = Field(
        default="",
        description="Abacus.AI API key for RouteLLM"
    )
    environment: str = Field(
        default="production",
        description="Environment (development, staging, production)"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        """Ensure a secure secret key is provided via environment variables."""
        if not value or value == "your-secret-key-change-in-production":
            raise ValueError("SECRET_KEY environment variable must be set to a secure value")
        return value

    @field_validator("api_keys")
    @classmethod
    def validate_api_keys(cls, value: list[str]) -> list[str]:
        """Ensure API keys are supplied and demo defaults are not used."""
        if isinstance(value, str):
            value = [key.strip() for key in value.split(",") if key.strip()]

        if not value:
            raise ValueError("API_KEYS environment variable must include at least one key")

        if any(key == "demo-api-key-12345" for key in value):
            raise ValueError("Demo API keys are not allowed; configure production API keys via API_KEYS")

        return value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        """Ensure a database URL is provided and not a local demo default."""
        if not value:
            raise ValueError("DATABASE_URL environment variable must be set")

        if value == "sqlite:///./powerhouse.db":
            raise ValueError(
                "Local SQLite demo database is not allowed; configure a production database via DATABASE_URL"
            )

        return value


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: Application settings
    """
    return settings
