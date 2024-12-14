
import requests
from sentence_transformers import SentenceTransformer

# ----------------------------
# CONFIGURATION
# ----------------------------
WEAVIATE_URL = "http://localhost:9090"
COLLECTION_NAME = "FinanceQA"
QUERY_ENDPOINT = f"{WEAVIATE_URL}/v1/graphql"

# Initialize SentenceTransformer model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def query_weaviate(user_query, k=3):
    # Generate embedding for the user query
    vector = embed_model.encode(user_query).tolist()

    # Define GraphQL query
    graphql_query = {
        "query": f"""
        {{
          Get {{
            {COLLECTION_NAME} (
              nearVector: {{ vector: {vector} }}
              limit: {k}
            ) {{
              question
              answer
            }}
          }}
        }}
        """
    }

    # Send request to Weaviate
    headers = {"Content-Type": "application/json"}
    response = requests.post(QUERY_ENDPOINT, json=graphql_query, headers=headers)

    # Process response
    if response.status_code == 200:
        results = response.json().get("data", {}).get("Get", {}).get(COLLECTION_NAME, [])
        if results:
            print("\nRetrieved Results:")
            for idx, item in enumerate(results):
                print(f"\nResult {idx + 1}:")
                print(f"Question: {item['question']}")
                print(f"Answer: {item['answer']}")
        else:
            print("No relevant results found.")
    else:
        print(f"Error: {response.text}")

# Example Query
if __name__ == "__main__":
    user_input = input("Enter your question: ")
    query_weaviate(user_input)
