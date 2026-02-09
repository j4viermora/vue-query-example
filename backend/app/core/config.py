"""
Configuración de la aplicación FastAPI
"""

from pydantic import BaseModel


class Settings(BaseModel):
    """Configuración de la aplicación"""

    app_name: str = "API de Reservas"
    app_version: str = "1.0.0"
    app_description: str = "API REST para gestión de reservas siguiendo JSON:API v1.1"

    # JSON:API
    jsonapi_version: str = "1.1"
    jsonapi_media_type: str = "application/vnd.api+json"

    class Config:
        case_sensitive = True


settings = Settings()
