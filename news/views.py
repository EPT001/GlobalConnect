from django.shortcuts import render
import requests

def news(request):
    print("News view called")  # Log that the view is called
    url = "https://newsapi.org/v2/everything?q=international%20students%20UK&apiKey=459dfcff88a741bcaa24a187e5751b49"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch news: {response.status_code}")
        print(response.text)  # Print the error message from the API
        return render(request, 'news.html', {'mylist': []})

    news_data = response.json()
    print(news_data)  # Log the response JSON

    articles = news_data.get('articles', [])
    
    # Limit to top 10 articles
    top_articles = articles[:10]
    
    # Prepare data for rendering
    mylist = [(article['title'], article['description'], article['urlToImage'], article['url']) for article in top_articles]

    context = {'mylist': mylist}
    
    return render(request, 'news.html', context)



