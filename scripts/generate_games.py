import os
import requests
from bs4 import BeautifulSoup

# Constants
api_url = "https://api.github.com/repos/touchmetender/GameFiles/contents/games"
output_file = "generated/games.html"
search_url = "https://duckduckgo.com/html/"

# Make sure output folder exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Get folder list from GitHub API
res = requests.get(api_url)
items = res.json()

# Filter only directories (games)
game_dirs = [item['name'] for item in items if item['type'] == 'dir']

def search_duckduckgo_image(query):
    """Search DuckDuckGo and return first image URL."""
    try:
        params = {"q": f"{query} game logo"}
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.post(search_url, data=params, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        img = soup.find("img", class_="tile--img__img")
        return img["src"] if img else "https://via.placeholder.com/150"
    except:
        return "https://via.placeholder.com/150"

# Generate HTML with thumbnails
with open(output_file, "w", encoding="utf-8") as f:
    for game in sorted(game_dirs):
        name = game.replace("-", " ").title()
        game_url = f"https://touchmetender.github.io/GameFiles/games/{game}/index.html"
        thumb_url = search_duckduckgo_image(name)

        f.write(f"""
<div class="grid-item generated-game" onclick="openGame('{game_url}')">
  <img src="{thumb_url}" alt="{name}" />
  <div class="name">{name}</div>
</div>
""")

print("✅ Game blocks saved to", output_file)
