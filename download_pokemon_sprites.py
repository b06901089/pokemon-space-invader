# Usage: python3 download_pokemon_sprites.py
# Run one or two more times if requests time out, as the server may be slow.
# Image source: https://pokemondb.net/sprites

import os
import requests
from bs4 import BeautifulSoup

SPRITES_PAGE = "https://pokemondb.net/sprites"

def get_pokemon_names():
    r = requests.get(SPRITES_PAGE, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    names = set()
    for a in soup.select('a.infocard[href^="/sprites/"]'):
        names.add(a["href"].split("/")[-1].lower())

    return sorted(names)


def main(names, sprite_base_url, output_dir):

    downloaded = 0
    skipped_existing = 0
    failed = 0

    print(f"Found {len(names)} Pokémon\n")

    for name in names:
        url = f"{sprite_base_url}/{name}.png"
        path = os.path.join(output_dir, f"{name}.png")

        if os.path.exists(path):
            skipped_existing += 1
            continue

        r = requests.get(url, timeout=10)

        if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image"):
            with open(path, "wb") as f:
                f.write(r.content)
            downloaded += 1
            print(f"✔ {name}")
        else:
            failed += 1
            print(f"✘ No sprite: {name}")

    print("\n=== Download Summary ===")
    print(f"Generation          : {output_dir.split('/')[-1]}")
    print(f"Total Pokémon found : {len(names)}")
    print(f"Downloaded          : {downloaded}")
    print(f"Already existed     : {skipped_existing}")
    print(f"Failed / missing    : {failed}")


if __name__ == "__main__":
    names = get_pokemon_names()

    Gen2URL = {
        "./img/pokemon/gen5": "https://img.pokemondb.net/sprites/black-white/normal",
        "./img/pokemon/gen4": "https://img.pokemondb.net/sprites/diamond-pearl/normal",
        "./img/pokemon/gen3": "https://img.pokemondb.net/sprites/ruby-sapphire/normal",
        "./img/pokemon/gen2": "https://img.pokemondb.net/sprites/silver/normal",
    }

    for output_dir, sprite_base_url in Gen2URL.items():
        os.makedirs(output_dir, exist_ok=True)
        main(names, sprite_base_url, output_dir)