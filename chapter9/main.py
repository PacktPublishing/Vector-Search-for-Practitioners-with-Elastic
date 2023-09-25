import streamlit as st
import requests
import json
from recipe_generator import RecipeGenerator
from config import OPENAI_API_KEY, ES_ENDPOINT, ES_USERNAME, ES_PASSWORD

# Initialize the RecipeGenerator
generator = RecipeGenerator(OPENAI_API_KEY)

# Elasticsearch query
def elasticsearch_query(query):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(ES_ENDPOINT, headers=headers, data=json.dumps(query), auth=(ES_USERNAME, ES_PASSWORD))

    result = {
        "name": response.json()["hits"]["hits"][0]["_source"]["name"],
        "group": response.json()["hits"]["hits"][0]["_source"]["group"],
        "ingredient": response.json()["hits"]["hits"][0]["_source"]["ingredient"],
    }
    return result

# Rest of your Streamlit code
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(
    """
        <style>
    @font-face {
        font-family: 'Inconsolata';
        src: url(https://fonts.googleapis.com/css?family=Inconsolata);
    }

    html, body, [class*="css"]  {
    font-family: 'Incosolata', monospace !important;
    color: #fff;

    }
    </style>

    """,
    unsafe_allow_html=True,
)


st.title('CookBot')
st.caption('Your Personal Cooking Assistant')
col1, col2 = st.columns([1,6])
with col1:
    st.image("https://i.ibb.co/bWDhmTg/Screenshot-2023-07-28-at-11-06-56-PM.png")
with col2:
    input_text = st.text_input(" ", placeholder="Ask me anything about cooking")

    if input_text:
        query = {
            "sub_searches": [
                {
                    "query": {
                        "bool": {
                            "must_not": [
                                {
                                    "match": {
                                        "ingredient": "onion"
                                    }
                                }
                            ]
                        }
                    }
                },
                {
                    "query": {
                        "text_expansion": {
                            "ml.tokens": {
                                "model_id": ".elser_model_1",
                                "model_text": input_text
                            }
                        }
                    }
                }
            ],
            "rank": {
                "rrf": {
                    "window_size": 50,
                    "rank_constant": 20
                }
            }
        }

        recipe = elasticsearch_query(query)
        st.write(recipe)
        st.write(generator.generate(recipe))
