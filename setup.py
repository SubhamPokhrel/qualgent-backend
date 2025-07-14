from setuptools import setup, find_packages

setup(
    name="qgjob",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["cli.qgjob"],
    entry_points={
        "console_scripts": [
            "qgjob=cli.qgjob:main",
        ],
    },
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "pydantic",
    ],
)
