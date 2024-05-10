import json
import os

# Directory containing the extracted API docs
api_docs_dir = '/home/amuller/Documents/mirinae/lookup/coin_market/api_docs'
training_data_path = '/home/amuller/Documents/mirinae/lookup/coin_market/api_training_data.txt'

def prepare_training_data(api_docs_dir):
    training_data = []
    for json_file in os.listdir(api_docs_dir):
        if json_file.endswith('.json'):
            with open(os.path.join(api_docs_dir, json_file), 'r', encoding='utf-8') as f:
                api_info = json.load(f)
                for endpoint in api_info['endpoints']:
                    training_data.append({
                        'title': endpoint['title'],
                        'description': endpoint['description'],
                        'params': endpoint['params'],
                    })

    training_data_texts = []
    for item in training_data:
        title = item['title']
        description = item['description']
        params = ', '.join(item['params'])
        training_data_texts.append(f"Endpoint: {title}\nDescription: {description}\nParameters: {params}\n")

    with open(training_data_path, 'w', encoding='utf-8') as f:
        for text in training_data_texts:
            f.write(text + '\n')

    print(f"Training data saved to {training_data_path}")

class APIExplorer:
    def __init__(self, api_docs_path):
        self.api_docs = self.load_api_docs(api_docs_path)

    def load_api_docs(self, api_docs_path):
        api_docs = {}
        for json_file in os.listdir(api_docs_path):
            if json_file.endswith('.json'):
                with open(os.path.join(api_docs_path, json_file), 'r', encoding='utf-8') as f:
                    api_info = json.load(f)
                    api_docs[api_info['title']] = api_info
        return api_docs

    def get_endpoint_info(self, endpoint_name):
        for api_name, api_info in self.api_docs.items():
            for endpoint in api_info['endpoints']:
                if endpoint_name.lower() in endpoint['title'].lower():
                    return endpoint
        return None

    def list_all_endpoints(self):
        endpoints = []
        for api_name, api_info in self.api_docs.items():
            for endpoint in api_info['endpoints']:
                endpoints.append(endpoint['title'])
        return endpoints

    def find_endpoint_by_param(self, param):
        matching_endpoints = []
        for api_name, api_info in self.api_docs.items():
            for endpoint in api_info['endpoints']:
                if param in endpoint['params']:
                    matching_endpoints.append(endpoint['title'])
        return matching_endpoints

if __name__ == '__main__':
    # Prepare training data
    prepare_training_data(api_docs_dir)

    # Example Usage
    api_explorer = APIExplorer(api_docs_dir)

    all_endpoints = api_explorer.list_all_endpoints()
    print("All Endpoints:", all_endpoints)

    endpoint_info = api_explorer.get_endpoint_info('get-latest-price')
    print("Specific Endpoint Info:", endpoint_info)

    matching_endpoints = api_explorer.find_endpoint_by_param('symbol')
    print("Endpoints containing 'symbol':", matching_endpoints)
