from setuptools import setup, find_packages

setup(
    name="agentsculptor",
    version="0.1.2",
    author="Perpetue237",
    author_email="youremail@example.com",
    description="agentsculptor: Shape your AI agents into powerful coding assistants — powered by GPT-OSS and vLLM.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Perpetue237/agentsculptor",
    project_urls={
        "Bug Tracker": "https://github.com/Perpetue237/agentsculptor/issues",
        "Source": "https://github.com/Perpetue237/agentsculptor",
    },
    packages=find_packages(exclude=["tests*", "test_project*", ".devcontainer*"]),
    python_requires=">=3.10",
    install_requires=[
        "black",
        "pytest",
        "colorlog",
        # add more runtime dependencies here
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
    license="Apache-2.0",   # <-- SPDX identifier
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        "console_scripts": [
            'agentsculptor-cli = agentsculptor.main:main',  # if your main.py has a main() function
        ],
    },
)
