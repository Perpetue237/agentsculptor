from setuptools import setup, find_packages

setup(
    name="codesculptor",
    version="0.1.0",
    author="Perpetue237",
    author_email="youremail@example.com",
    description="AI-powered Python project refactoring and testing agent using GPT-OSS and vLLM",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Perpetue237/codesculptor",
    packages=find_packages(exclude=["tests*", "test_project*", ".devcontainer*"]),
    python_requires=">=3.10",
    install_requires=[
        "black",
        "pytest",
        # add more runtime dependencies here
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            # any dev tools
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            'codesculptor-cli = codesculptor.main:main',  # if your main.py has a main() function
        ],
    },
)
