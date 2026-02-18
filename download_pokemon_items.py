import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://pokemondb.net"
URL = BASE + "/item/all"
SKIP_ICON = "https://img.pokemondb.net/s.png"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# fetch page
resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# output folder
os.makedirs("item_icons", exist_ok=True)

rows = soup.select("table.data-table tbody tr")
print("Rows found:", len(rows))

for row in rows:
    cols = row.find_all("td")
    if len(cols) != 3:
        continue

    img_tag = cols[0].find("img")
    name_tag = cols[0].find("a", class_="ent-name")

    if not img_tag or not name_tag:
        continue

    icon_url = img_tag.get("src")

    # 🔴 skip placeholder image ONLY
    if icon_url == SKIP_ICON:
        continue

    filename = os.path.join(
        "img/pokemon/items",
        icon_url.split("/")[-1]
    )

    try:
        img = requests.get(icon_url, headers=HEADERS)
        img.raise_for_status()

        with open(filename, "wb") as f:
            f.write(img.content)

        print("Downloaded:", filename)
    except:
        print("Failed to download:", icon_url)
