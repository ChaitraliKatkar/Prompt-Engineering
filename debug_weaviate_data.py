
import requests

# Configuration
WEAVIATE_URL = "http://localhost:9090"
COLLECTION_NAME = "FinanceQA"
QUERY_ENDPOINT = f"{WEAVIATE_URL}/v1/graphql"

def debug_weaviate_data(query="income"):
    """
    Query Weaviate to fetch records using semantic search with nearText.
    Args:
        query (str): The user's input question or keyword.
    """
    graphql_query = {{
        "query": f"""
        {{
          Get {{
            {COLLECTION_NAME} (
              nearText: {{
                concepts: ["{{query}}"]
              }}
              limit: 5
            ) {{
              question
              answer
            }}
          }}
        }}
        """
    }}

    headers = {{"Content-Type": "application/json"}}

    try:
        response = requests.post(QUERY_ENDPOINT, json=graphql_query, headers=headers)
        response.raise_for_status()

        results = response.json().get("data", {}).get("Get", {}).get(COLLECTION_NAME, [])
        if results:
            print(f"\n--- Results for query '{{query}}' ---")
            for idx, item in enumerate(results, start=1):
                print(f"\nRecord {{idx}}:")
                print(f"Question: {{item.get('question', 'N/A')}}")
                print(f"Answer: {{item.get('answer', 'N/A')}}")
        else:
            print("No relevant records found for your query.")
    except Exception as e:
        print(f"Error: {{e}}")
