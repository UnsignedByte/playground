import json

import requests

import os
import queue
import time
import random

data = {
  "elements": [
    {"text": "Water", "emoji": "💧", "discovered": False},
    {"text": "Fire", "emoji": "🔥", "discovered": False},
    {"text": "Wind", "emoji": "🌬️", "discovered": False},
    {"text": "Earth", "emoji": "🌍", "discovered": False},
  ],
  "pinned": [],
  "recipes": {

  }
}

if os.path.exists("data.json"):
  with open("data.json", "r") as f:
    data = json.load(f)

emojis = {}

tried_recipes = set()

for recipes in data["recipes"].values():
  for recipe in recipes:
   tried_recipes.add(tuple(sorted(r["text"] for r in recipe)))

to_try = queue.SimpleQueue()

for element in data["elements"]:
  emojis[element["text"]] = element["emoji"]
  element = element["text"]
  for element2 in data["elements"]:
    element2 = element2["text"]
    if element <= element2 and (element, element2) not in tried_recipes:
      to_try.put((element, element2))

del tried_recipes

def combine(a, b):
  s = requests.Session()
  s.headers.update({'referer': "https://neal.fun/infinite-craft/"})
  r = s.get(
      f"https://neal.fun/api/infinite-craft/pair?first={a}&second={b}"
  )
  if r.status_code != 200:
    raise TimeoutError("Rate Limited...")
  j = json.loads(r.content)
  return (j["result"], j["isNew"], j["emoji"])

# print(emojis)

try:
  while not to_try.empty():
    time.sleep(random.uniform(0, 0.5))
    try:
      a, b = to_try.get()
      text, isnew, emoji = combine(a, b)

      if text == "Nothing":
        continue

      if isnew:
        print(f"FIRST Discovered: {a} + {b} = {text}")

      if text not in emojis:
        print(f"{a} + {b} = {text}")
        emojis[text] = emoji
        data["elements"].append({
          "text": text,
          "emoji": emoji,
          "discovered": isnew
        })
        for element in emojis.keys():
          to_try.put((element, text))

      if text not in data["recipes"]:
        data["recipes"][text] = []

      data["recipes"][text].append(
        [
          {"text": a, "emoji": emojis[a]},
          {"text": b, "emoji": emojis[b]},
        ]
      )
    except TimeoutError:
      print("Rate limited, trying again...")
      time.sleep(60)
except KeyboardInterrupt as e:
  print(e)
  print("Stopping...")
finally:
  with open("data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)