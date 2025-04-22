import os
import requests
from bs4 import BeautifulSoup
import time

# Constants
api_url = "https://api.github.com/repos/touchmetender/GameFiles/contents/games"
output_file = "generated/games.html"
fallback_image = "https://via.placeholder.com/150"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_bing_image_url(query):
    search_query = f"{query} game logo"
    url = f"https://www.bing.com/images/search?q={search_query.replace(' ', '+')}&form=HDRSC2"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find("img", {"class": "mimg"})
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
    except Exception as e:
        print(f"Error for {query}: {e}")
    return fallback_image

# Create output directory if needed
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Get game folders from GitHub
res = requests.get(api_url)
items = res.json()
game_dirs = [item['name'] for item in items if item['type'] == 'dir']

# Write HTML
with open(output_file, "w", encoding="utf-8") as f:
    for game in sorted(game_dirs):
        name = game.replace("-", " ").title()
        game_url = f"https://touchmetender.github.io/GameFiles/games/{game}/index.html"
        logo_url = get_bing_image_url(name)
        print(f"🔍 {name} → {logo_url}")
        
        f.write(f"""
<div class="grid-item generated-game" onclick="openLink('{game_url}')">
  <img src="{logo_url}" alt="{name}" />
  <div class="name">{name}</div>
</div>
""")
        time.sleep(1)

print("✅ Game blocks with logos generated to", output_file)
