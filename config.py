"""This module defines and extracts environment variables
for use in other parts of the application.
"""

import os
from pydantic_settings import BaseSettings


# Define environment variables directly in the file
os.environ["ALPHA_API_KEY"] = "2019c19ecd71029ffd831e6e7a19a782aa15bbf53f92852b6d7570ac579cf20ec42df48349653230d938827cbcabc0ba12a6fb313d58840132a3a117bf4484325d4d87253f370c3c263a2be5c4d4fd3baedd9625289a9655d0f6480e73c633ec6593e423233db134ac3a2d26b3af3512e56ff4f2dabd692350349fd0ad392005"
os.environ["DB_NAME"] = "stocks.sqlite"
os.environ["MODEL_DIRECTORY"] = "models"


class Settings(BaseSettings):
    """Uses pydantic to define settings for the project."""

    alpha_api_key: str
    db_name: str
    model_directory: str

    class Config:
        # Resolve the protected namespace warning by updating this setting
        protected_namespaces = ("settings_",)


# Create an instance of the `Settings` class to access environment variables
settings = Settings(
    alpha_api_key=os.getenv("ALPHA_API_KEY"),
    db_name=os.getenv("DB_NAME"),
    model_directory=os.getenv("MODEL_DIRECTORY"),
)

# Example of accessing the settings
if __name__ == "__main__":
    print(f"Alpha API Key: {settings.alpha_api_key}")
    print(f"Database Name: {settings.db_name}")
    print(f"Model Directory: {settings.model_directory}")
