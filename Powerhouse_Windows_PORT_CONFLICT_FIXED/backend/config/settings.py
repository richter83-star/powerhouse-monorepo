"""
Application settings and configuration.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


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
        default="your-secret-key-change-in-production",
        description="Secret key for JWT encoding"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Keys (for enterprise clients)
    api_keys: list[str] = Field(
        default_factory=lambda: ["demo-api-key-12345"],
        description="Valid API keys for authentication"
    )
    
    # Database
    database_url: str = Field(
        default="sqlite:///./powerhouse.db",
        description="Database connection URL"
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


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: Application settings
    """
    return settings
