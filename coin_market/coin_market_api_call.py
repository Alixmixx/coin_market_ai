import requests

def make_api_call(endpoint, api_key):
    """ Make an API call to the CoinMarketCap API.
    
    Args:
        endpoint (str): The API endpoint generated by the LLM.
        api_key (str): Your CoinMarketCap API key.

    Returns:
        dict: The JSON response from the API call.
    """
    base_url = "https://sandbox-api.coinmarketcap.com"
    
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accept': 'application/json',  # Corrected header key
        'X-CMC_PRO_API_KEY': api_key
    }
    try:
        # if "?" in endpoint:
        #     endpoint = endpoint.split("?")[0]
        # if " " in endpoint:
        #     endpoint = endpoint.split(" ")[1]
        print(f"Making API call to {base_url + endpoint}")
        url = base_url + endpoint
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
