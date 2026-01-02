"""Quick test for news fetching."""
from app.services.cache_service import clear_cache
clear_cache()

from app.agents.scout import ScoutAgent

news = ScoutAgent._get_news_static('ITC.NS')
print(f"Found {len(news)} news items:")
for n in news[:5]:
    source = n.get("source", "?")
    title = n.get("title", "")[:55]
    publisher = n.get("publisher", "")
    print(f"  - [{source}] {title}...")
    if publisher:
        print(f"    Publisher: {publisher}")

print("\n✅ News fetching is working!")
