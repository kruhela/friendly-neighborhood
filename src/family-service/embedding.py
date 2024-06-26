import numpy as np
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os


OPENAI_API_TYPE = "azure"
OPENAI_API_KEY = "INSERT_OPENAI_API_KEY"
OPENAI_API_BASE = "INSERT_OPENAI_API_BASE"
OPENAI_API_VERSION = "2023-05-15"
DEPLOYMENT_NAME = "text-embedding-ada-002"

os.environ["OPENAI_API_TYPE"] = OPENAI_API_TYPE
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)

AZURE_SEARCH_ENDPOINT = "INSERT_AZURE_SEARCH_ENDPOINT"
os.environ["AZURE_SEARCH_ENDPOINT"] = AZURE_SEARCH_ENDPOINT

AZURE_SEARCH_KEY = "INSERT_AZURE_SEARCH_KEY"
os.environ["AZURE_SEARCH_KEY"] = AZURE_SEARCH_KEY

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = "profile_data_new"
# index_name = "profile_dataset"

azure_search_client = SearchClient(search_endpoint, index_name, AzureKeyCredential(search_key))
azure_search_client_profile = SearchClient(search_endpoint, "profile_dataset", AzureKeyCredential(search_key))

def generate_embedding_and_metadata(text):
    embedding_data = openai_client.embeddings.create(input=[text], model="text-embedding-ada-002").data[0]
    embedding = embedding_data.embedding
    # print(embedding)
    # metadata = {'text': text}
    return embedding

def search_similar_text_old(query_text):
    query_embedding = openai_client.embeddings.create(input=[query_text], model="text-embedding-ada-002").data[0].embedding
    # print(query_text)
    # print(query_embedding)
    # similar_documents = azure_search_client.search(query_embedding)
    select = ["id", "Summary", "Diagnosis", "Email"]
    # Perform similarity search using the generated embedding
    # similar_documents = azure_search_client.search(search_text="", filter=f"search.ismatch('{query_embedding}', 'Embedding')", select=select)
    similar_documents = azure_search_client.search(search_text="", filter=f"search.ismatch('{query_text}', 'Summary')", select=select)
    
    # print(similar_documents)
    return similar_documents

def search_similar_text(query_text):
    query_embedding = openai_client.embeddings.create(input=[query_text], model="text-embedding-ada-002").data[0].embedding
    # print(query_text)
    # print(query_embedding)
    # similar_documents = azure_search_client.search(query_embedding)
    select = ["id", "Autism_Diagnosis_Summary", "Email"]
    # Perform similarity search using the generated embedding
    # similar_documents = azure_search_client.search(search_text="", filter=f"search.ismatch('{query_embedding}', 'Embedding')", select=select)
    similar_documents = azure_search_client_profile.search(search_text="", filter=f"search.ismatch('{query_text}', 'Autism_Diagnosis_Summary')", select=select)
    
    # print(similar_documents)
    return similar_documents
