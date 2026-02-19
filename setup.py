"""Setup configuration for Roll Cake Recipes package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="roll-cake-recipes",
    version="1.0.0",
    author="Roll Cake Recipes Team",
    author_email="contact@example.com",
    description="Vietnamese Roll Cake Recipes Database with API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhungKhacVu/roll-cake-recipes",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.109.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "uvicorn[standard]>=0.27.0",
        "python-multipart>=0.0.6",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "python-dotenv>=1.0.0",
        "slowapi>=0.1.9",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.23.0",
            "hypothesis>=6.98.0",
            "httpx>=0.26.0",
            "black>=24.1.0",
            "ruff>=0.2.0",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
            "bandit>=1.7.5",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "roll-cake-api=src.api.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.md"],
    },
    zip_safe=False,
)
