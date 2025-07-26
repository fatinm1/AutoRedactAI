from setuptools import setup, find_packages

setup(
    name="autoredact-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "structlog",
    ],
) 