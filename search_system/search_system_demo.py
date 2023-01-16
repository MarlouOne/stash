# from googlesearch import search
# query = "СВО"
# for i in search(query, tld="ru", num=10, stop=10, pause=2): print(i)

import requests

API_KEY = 'AIzaSyBtVaNmzMLk8DbjdNh0Mq_OqyNN5QvcnY0' # get the API KEY here: https://developers.google.com/custom-search/v1/overview
SEARCH_ENGINE_ID = "d75c9236c9f8e4053" # get your Search Engine ID on your CSE control panel
query = "python" # the search query you want
page = 1  # using the first page

# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
start = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
data = requests.get(url).json() # make the API request
search_items = data.get("items") # get the result items
for i, search_item in enumerate(search_items, start=1): # iterate over 10 results found
    try:
        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
    except KeyError:
        long_description = "N/A"
    title = search_item.get("title") # get the page title
    snippet = search_item.get("snippet") # page snippet
    html_snippet = search_item.get("htmlSnippet") # alternatively, you can get the HTML snippet (bolded keywords)
    link = search_item.get("link") # extract the page url
    # print the results
    print("="*10, f"Result #{i+start-1}", "="*10)
    print("Title:", title)
    print("Description:", snippet)
    print("Long description:", long_description)
    print("URL:", link, "\n")