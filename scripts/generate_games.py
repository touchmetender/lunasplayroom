import os
import requests

# Constants
api_url = "https://api.github.com/repos/touchmetender/GameFiles/contents/games"
raw_base_url = "https://touchmetender.github.io/GameFiles/games"
output_file = "generated/games.html"

# Make sure output folder exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Get folder list from GitHub API
res = requests.get(api_url)
items = res.json()

# Filter only directories
game_dirs = [item['name'] for item in items if item['type'] == 'dir']

# Write HTML blocks
with open(output_file, "w", encoding="utf-8") as f:
    for game in sorted(game_dirs):
        game_url = f"{raw_base_url}/{game}/index.html"
        thumb_url = f"{raw_base_url}/{game}/thumbnail.jpg"
        name = game.replace("-", " ").title()

        f.write(f"""
<div class="grid-item" onclick="openGame('{game_url}')">
  <img src="{thumb_url}" alt="{name}" />
  <div class="name">{name}</div>
</div>
""")

print("✅ Game blocks saved to", output_file)
