import requests
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import re  # Importing regular expressions to extract the amount

# ----------------------------
# CONFIGURATION
# ----------------------------
WEAVIATE_URL = "http://localhost:9090"
COLLECTION_NAME = "FinanceQA"
QUERY_ENDPOINT = f"{WEAVIATE_URL}/v1/graphql"

# Initialize embedding model and language model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = pipeline("text-generation", model="gpt2")  # Replaced with GPT-2 (valid model)

def retrieve_from_weaviate(query, k=3):
    vector = embed_model.encode(query).tolist()
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
    headers = {"Content-Type": "application/json"}
    response = requests.post(QUERY_ENDPOINT, json=graphql_query, headers=headers)

    results = response.json().get("data", {}).get("Get", {}).get(COLLECTION_NAME, [])
    return results

def generate_response(user_query):
    # Retrieve relevant data from Weaviate
    retrieved_data = retrieve_from_weaviate(user_query)
    
    # Filter for Food (Snacks) related entries
    snacks_data = [item for item in retrieved_data if "Food (Snacks)" in item.get("question", "")]

    # If there are relevant snack entries, calculate total spending
    if snacks_data:
        total_spending = 0
        for item in snacks_data:
            # Use regular expression to find the dollar amount in the answer
            match = re.search(r"\$([\d\.]+)", item.get("answer", ""))
            if match:
                total_spending += float(match.group(1))  # Add the extracted amount to total
        response_text = f"The total amount spent on Food (Snacks) is ${total_spending:.2f}."
    else:
        response_text = "I couldn't find any records for spending on Food (Snacks)."

    return response_text

# Example Interaction
if __name__ == "__main__":
    user_input = input("Enter your question: ")
    response = generate_response(user_input)
    print("\nBot Response:")
    print(response)
