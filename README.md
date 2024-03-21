# Example LangChain Chains

This project demonstrates how to use LangChain to create and manage language model chains using LangChain's Expression Language (LCEL).

## Prerequisites

Before you start, ensure you have Python 3.9 or higher installed on your system. You will also need `pip` for installing the dependencies.

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the following packages:

- dotenv
- langchain
- langchain_openai
- langchain_core

## Configuration

To configure the project, you need to set up your environment variables:

1. Copy the `example.env` file to a new file named `.env`.
2. Replace `YOUR_OPENAI_API_KEY` and `YOUR_SERP_API_KEY` with your actual API keys.

```bash
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
SERP_API_KEY=YOUR_SERP_API_KEY
```

Ensure that the `.env` file is listed in your `.gitignore` to keep your API keys secure.

## Running the Project

To run the project, execute the following command in your terminal:

```bash
python3 app.py
```

This script will start the application using the configuration specified in your `.env` file. Look at the `example.env` file for the expected variables.
