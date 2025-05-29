from duckduckgo_search import DDGS

def search_youtube_link(query):
    with DDGS() as ddgs:
        results = ddgs.text(f"{query} site:youtube.com", max_results=1)
        for r in results:
            return r["href"]
    return "No result found."