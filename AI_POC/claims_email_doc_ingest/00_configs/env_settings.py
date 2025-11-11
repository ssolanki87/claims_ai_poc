import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Environment settings management"""
    
    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_ACCOUNT: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")
    AZURE_STORAGE_KEY: str = os.getenv("AZURE_STORAGE_KEY", "")
    
    # Database
    DB_SERVER: str = os.getenv("DB_SERVER", "")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    
    # AI API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Notifications
    TEAMS_WEBHOOK_URL: str = os.getenv("TEAMS_WEBHOOK_URL", "")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def db_connection_string(self) -> str:
        """Get database connection string"""
        return (
            f"Driver={self.DB_DRIVER};"
            f"Server={self.DB_SERVER};"
            f"Database={self.DB_DATABASE};"
            f"UID={self.DB_USERNAME};"
            f"PWD={self.DB_PASSWORD};"
        )
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        required = [
            "AZURE_STORAGE_CONNECTION_STRING",
            "DB_SERVER",
            "DB_DATABASE",
            "ANTHROPIC_API_KEY"
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        return True

settings = Settings()
