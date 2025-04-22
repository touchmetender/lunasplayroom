import os
import requests
from bs4 import BeautifulSoup

base_url = "https://github.com/touchmetender/GameFiles/tree/master/games"
raw_base_url = "https://touchmetender.github.io/GameFiles/games"

output_file = "generated/games.html"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Get list of games from GitHub HTML
res = requests.get(base_url)
soup = BeautifulSoup(res.text, "html.parser")
game_dirs = [a.text.strip() for a in soup.select('a.js-navigation-open') if a['href'].startswith('/touchmetender/GameFiles/tree/master/games/')]

# Generate HTML
with open(output_file, "w", encoding="utf-8") as f:
    for game in sorted(game_dirs):
        game_url = f"{raw_base_url}/{game}/index.html"
        thumb_url = f"{raw_base_url}/{game}/thumbnail.jpg"
        name = game.replace('-', ' ').title()

        f.write(f"""
<div class="grid-item" onclick="openGame('{game_url}')">
  <img src="{thumb_url}" alt="{name}" />
  <div class="name">{name}</div>
</div>
""")
print("✅ Game blocks saved.")
