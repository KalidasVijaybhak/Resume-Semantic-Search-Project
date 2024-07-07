
import requests
import json
def send_query(query_text):
    url = "http://localhost:8000/retrieve"
    payload = {"text": query_text}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            print("Retrieved sources:")
            for item in data['metadata']:
                source = item.get('source', 'No source available')
                print(f"- {source}")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError:
        print("Failed to decode the response as JSON")
    except KeyError:
        print("The response doesn't contain the expected 'metadata' key")

if __name__ == "__main__":
    while True:
        query = input("\nEnter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        send_query(query)