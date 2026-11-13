## 4. Create the mock menu

Paste the entire block at the shell prompt. It writes the file in your current directory. If you prefer the editor, open `cloudshell edit menu.json`, paste only the JSON between the two delimiter lines, save, and run the validation separately.

```bash
cat > menu.json <<'JSON'
[
  {
    "name": "Espresso Solo",
    "description": "A single shot of rich, bold espresso.",
    "price": 2.50,
    "tags": ["strong", "hot", "dairy-free", "sugar-free"],
    "allergens": []
  },
  {
    "name": "Oat Milk Honey Latte",
    "description": "Creamy steamed oat milk with espresso and a touch of honey.",
    "price": 5.00,
    "tags": ["sweet", "hot", "dairy-free"],
    "allergens": []
  },
  {
    "name": "Cold Brew Coffee",
    "description": "Smooth, slow-steeped cold brew served over ice.",
    "price": 4.00,
    "tags": ["strong", "cold", "dairy-free", "sugar-free"],
    "allergens": []
  },
  {
    "name": "Seasonal Pumpkin Latte",
    "description": "Spiced pumpkin sauce, espresso, and steamed milk, topped with whipped cream.",
    "price": 5.50,
    "tags": ["sweet", "hot", "seasonal"],
    "allergens": ["dairy"]
  },
  {
    "name": "Classic Croissant",
    "description": "Flaky, buttery traditional French pastry.",
    "price": 3.50,
    "tags": ["bakery", "savory"],
    "allergens": ["wheat", "dairy"]
  },
  {
    "name": "Vegan Blueberry Muffin",
    "description": "Soft, sweet muffin packed with real blueberries, entirely plant-based.",
    "price": 3.75,
    "tags": ["bakery", "sweet", "dairy-free", "vegan"],
    "allergens": ["wheat"]
  },
  {
    "name": "Nitro Cold Brew",
    "description": "Cold brew infused with nitrogen for a super smooth, creamy head.",
    "price": 4.50,
    "tags": ["strong", "cold", "dairy-free", "sugar-free"],
    "allergens": []
  },
  {
    "name": "Iced Caramel Macchiato",
    "description": "Chilled milk and vanilla syrup marked with espresso and caramel drizzle.",
    "price": 5.25,
    "tags": ["sweet", "cold"],
    "allergens": ["dairy"]
  }
]
JSON

python3 -m json.tool menu.json >/dev/null && echo "Valid JSON"
```

If Bash shows a continuation prompt, enter the closing delimiter `JSON` on a line by itself or press Ctrl+C and retry the entire block. With `nano menu.json`, save using Ctrl+O, Enter, then exit with Ctrl+X.

---

[Lab overview](README.md) · [Previous](03_choose_track.md) · [Next](05_build_agent_and_ui.md)
