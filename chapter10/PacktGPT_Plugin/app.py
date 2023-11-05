import json
import requests
import urllib.parse

import quart
import quart_cors
from quart import request

import os
import openai
from elasticsearch import Elasticsearch

from embedchain import App
from embedchain import CustomApp
from embedchain.config import CustomAppConfig, ElasticsearchDBConfig
from embedchain.models import Providers, EmbeddingFunctions, VectorDatabases

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")

openai.api_key = os.environ['openai_api']
os.environ["OPENAI_API_KEY"] = openai.api_key

model = "gpt-3.5-turbo-0301"

# Connect to Elastic Cloud cluster
def es_connect(cid, user, passwd):
  es = Elasticsearch(cloud_id=cid, http_auth=(user, passwd))
  return es

# Search ElasticSearch index and return body and URL of the result
def ESSearch(query_text):

  print(query_text)

  cloud_url = os.environ['cloud_url']
  cid = os.environ['cloud_id']
  cp = os.environ['cloud_pass']
  cu = os.environ['cloud_user']
  es = es_connect(cid, cu, cp)

  # Elasticsearch query (BM25)
  query = {
    "bool": {
      "filter": [
        {
          "prefix": {
            "url": "https://www.elastic.co/guide"
          }
        }
        
        ], 
        "must": [{
          "match": {
            "title": {
              "query": query_text,
              "boost": 1
            }
          }
        }]
    }
  }

  fields = ["title", "body_content", "url"]
  index = 'search-elastic-doc'
  resp = es.search(index=index,
                   query=query,
                   fields=fields,
                   size=10,
                   source=False)

  body = resp['hits']['hits'][0]['fields']['body_content'][0]
  url = resp['hits']['hits'][0]['fields']['url'][0]

  # es_config = ElasticsearchDBConfig(
  #   es_url=cloud_url,
  #   basic_auth=(cu, cp)
  # )
  # config = CustomAppConfig(
  #   embedding_fn=EmbeddingFunctions.OPENAI,
  #   provider=Providers.OPENAI,
  #   db_type=VectorDatabases.ELASTICSEARCH,
  #   es_config=es_config,
  # )

  # es_app = CustomApp(config)

  print(len(resp['hits']['hits']))


  elastic_bot = App()


   # Assuming 'resp' is the response object you've mentioned
  for hit in resp['hits']['hits']:
    for url in hit['fields']['url']:
        print(url)
        #es_app.add(url)
        elastic_bot.add(url)

  #print(es_app.query("Give me the latest documentation on " + query_text))

  return elastic_bot.query("What can you tell me about " + query_text)



def truncate_text(text, max_tokens):
  tokens = text.split()
  if len(tokens) <= max_tokens:
    return text

  return ' '.join(tokens[:max_tokens])


# Generate a response from ChatGPT based on the given prompt
def chat_gpt(prompt,
             model="gpt-3.5-turbo",
             max_tokens=1024,
             max_context_tokens=4000,
             safety_margin=5):
  # Truncate the prompt content to fit within the model's context length
  truncated_prompt = truncate_text(
    prompt, max_context_tokens - max_tokens - safety_margin)

  response = openai.ChatCompletion.create(model=model,
                                          messages=[{
                                            "role":
                                            "system",
                                            "content":
                                            "You are a helpful assistant."
                                          }, {
                                            "role": "user",
                                            "content": truncated_prompt
                                          }])

  return response["choices"][0]["message"]["content"]


@app.get("/search")
async def search():
  query = request.args.get("query")
  url = ESSearch(query)
  return quart.Response(url)


@app.get("/logo.png")
async def plugin_logo():
  filename = 'logo.png'
  return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
  host = request.headers['Host']
  with open("./.well-known/ai-plugin.json") as f:
    text = f.read()
    text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
    return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
  host = request.headers['Host']
  with open("openapi.yaml") as f:
    text = f.read()
    text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
    return quart.Response(text, mimetype="text/yaml")


def main():
  port = int(os.environ.get("PORT", 5001))
  app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
  main()
