import os
import requests
from bs4 import BeautifulSoup
import time

# Constants
api_url = "https://api.github.com/repos/touchmetender/GameFiles/contents/games"
output_file = "generated/games.html"
search_url = "https://duckduckgo.com/html/"
fallback_image = "https://via.placeholder.com/150"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Get list of game directories from GitHub
res = requests.get(api_url)
items = res.json()
game_dirs = [item['name'] for item in items if item['type'] == 'dir']

def get_duckduckgo_image_url(query):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": f"{query} game logo"}
        response = requests.post(search_url, data=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img = soup.find('img')
        if img and img.get("src"):
            return img["src"]
        else:
            return fallback_image
    except Exception as e:
        print(f"❌ Error fetching logo for {query}: {e}")
        return fallback_image

# Write HTML blocks
with open(output_file, "w", encoding="utf-8") as f:
    for game in sorted(game_dirs):
        name = game.replace("-", " ").title()
        game_url = f"https://touchmetender.github.io/GameFiles/games/{game}/index.html"
        logo_url = get_duckduckgo_image_url(name)
        print(f"🖼️  {name} → {logo_url}")

        f.write(f"""
<div class="grid-item generated-game" onclick="openGame('{game_url}')">
  <img src="{logo_url}" alt="{name}" />
  <div class="name">{name}</div>
</div>
""")
        time.sleep(1)  # Delay to avoid rate limiting

print("✅ Finished generating game blocks.")
