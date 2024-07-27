import requests

def read_google_key():
    """
    Reads the Google API key from a file called 'google.key'.
    Returns: a string which is either None (no key found) or with a key.
    Remember to put 'google.key' in your .gitignore file to avoid committing it.
    """
    google_api_key = None
    try:
        with open('google.key', 'r') as f:
            google_api_key = f.readline().strip()
    except:
        try:
            with open('../google.key') as f:
                google_api_key = f.readline().strip()
        except:
            raise IOError('google.key file not found')

    if not google_api_key:
        raise KeyError('Google key not found')

    return google_api_key

def run_query(search_terms):
    """
    Sends a query to Google Custom Search API and returns the results.
    """
    google_key = read_google_key()
    search_engine_id = 'YOUR_CUSTOM_SEARCH_ENGINE_ID'  # Replace with your Custom Search Engine ID (cx)
    search_url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': google_key,
        'cx': search_engine_id,
        'q': search_terms
    }

    # Issue the request to Google Custom Search API
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        # Parse the search results and build a list of dictionaries
        results = []
        for item in search_results.get('items', []):
            results.append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'summary': item.get('snippet', '')
            })
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching results from Google Custom Search API: {e}")
        return []

# Example usage:
if __name__ == "__main__":
    search_terms = "Python programming"  # Replace with your search query
    results = run_query(search_terms)
    for idx, result in enumerate(results, 1):
        print(f"Result {idx}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Summary: {result['summary']}")
        print()
