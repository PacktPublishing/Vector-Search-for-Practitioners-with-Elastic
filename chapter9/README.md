# CookBot: Your Personal Cooking Assistant

CookBot is an interactive cooking assistant powered by OpenAI's GPT-4 model, Elasticsearch, and Streamlit. This application aims to provide an interactive cooking experience by answering user queries with relevant recipes and providing a step-by-step guide.

## Prerequisites

Before you begin, make sure your development environment meets the following requirements:

- Python 3.8 or later
- [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
- [Streamlit](https://docs.streamlit.io/library/get-started/installation)

You should also install the necessary Python libraries:

- `openai`
- `streamlit`
- `elasticsearch`
- `requests`

These can be installed via pip:

```bash
pip install openai streamlit elasticsearch requests`
```

## Getting Started

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/CookBot.git
cd CookBot
```

### Set up the Environment
Create a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

### Install the required dependencies:

```bash
pip install -r requirements.txt
```


### Set Environment Variables

Set your OpenAI API key as an environment variable. 

```bash
export OPENAI_API_KEY='your-api-key'
```

Replace `'your-api-key'` with your actual OpenAI API key.

### Run the Application

To start the Streamlit server:

```bash
streamlit run app.py
```


The Streamlit app will be served on `http://localhost:8501`. Open this URL in your web browser to interact with CookBot.

## Usage

Input your cooking related question into the input box, and CookBot will fetch a relevant recipe and generate a step-by-step guide based on the information.