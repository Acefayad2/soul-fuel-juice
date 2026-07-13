# Soul Fuel Juice — Product Image Generation Brief

Goal: generate a **consistent, professional set of product photos** for every drink,
matching the look of the **real bottles** (clear bottle, matte black cap, white kraft
label) photographed on a bright white marble counter.

Use these as visual references (already shot in the target style):
`IMG_6752.PNG` (Queen's Power) and `IMG_6753.PNG` (orange bottle). If your image tool
supports a reference/style image, attach one of these — it's the biggest consistency win.

---

## Style spec (applies to every image)

- Clear rectangular **plastic cold-pressed juice bottle** with a **matte black screw cap**
- **White kraft-paper label** with softly notched corners
- Label contains: olive-green **heart-and-leaf logo** at top, "SOUL FUEL JUICE",
  the line *"3 John 1:2 — …Be in health, even as your soul prospers,"* a **bold flavor
  name**, "COLD-PRESSED", and a short ingredients list
- Setting: **white marble / quartz countertop**, subtle light tile backsplash, soft
  natural daylight, gentle reflection and shadow
- Photorealistic, crisp focus, clean minimal e-commerce look
- **One bottle centered per image**, plenty of clean space around it
- Aspect ratio 3:2 or 4:5 (portrait-ish is fine); high resolution

Note: perfect label text is NOT required — at product-card size it reads as a real
branded bottle. If exact labels are wanted, generate **plain unlabeled colored bottles**
and the real label can be composited on afterward.

---

## Master prompt (swap in one flavor per generation)

> Professional e-commerce product photograph of a single **cold-pressed juice bottle**
> centered on a **white marble countertop** with a subtle light tile backsplash, bright
> soft natural daylight, gentle reflections and shadows. Clear rectangular plastic bottle
> with a **matte black screw cap** and a **white kraft-paper label with notched corners**;
> the label shows an olive-green heart-and-leaf logo, "SOUL FUEL JUICE", the scripture
> "3 John 1:2 — …Be in health, even as your soul prospers", a bold flavor name
> "**{NAME}**", "COLD-PRESSED", and ingredients "{INGREDIENTS}". The juice is **{COLOR}**.
> Photorealistic, crisp focus, clean minimal look, high resolution.

---

## Juices — fill-ins + output filename

| Flavor | Color | Ingredients | Save as |
|---|---|---|---|
| Healing Greens | vivid green | Kale, Apple, Cucumber, Spinach, Lemon, Celery, Ginger | `healing-greens.jpg` |
| Golden Glow | golden yellow | Mango, Pineapple, Carrot, Lemon, Ginger | `golden-glow.jpg` |
| Carrot Glow | bright orange | Pineapple, Orange, Carrot, Turmeric, Ginger | `carrot-glow.jpg` |
| Queen's Power | deep magenta-red | Beetroot, Watermelon, Ginger, Pineapple, Lemon, Maca | `queens-power.jpg` |
| Beet & Bless | dark burgundy | Beets, Apple, Ginger, Carrot, Lemon | `beet-bless.jpg` |
| Island Glow | pale green | Watermelon, Cucumber, Pineapple, Lime, Ginger | `island-glow.jpg` |

## Wellness shots (small 2 oz bottle, same style, small white label)

| Flavor | Color | Save as |
|---|---|---|
| Citrus Defense | bright yellow | `shot-citrus-defense.jpg` |
| Fiery Ginger | golden | `shot-fiery-ginger.jpg` |
| Immune Shield | orange-yellow | `shot-immune-shield.jpg` |
| Golden Root Tonic | deep turmeric gold | `shot-golden-root.jpg` |
| Pineapple Mint Soother | pale yellow-green | `shot-pineapple-mint.jpg` |
| Spiced Beet Elixir | deep red | `shot-spiced-beet.jpg` |

---

## Delivery

Save the finished images into the `Soul Fuel Content` folder (Desktop) using the exact
filenames above. Claude will then crop each to the site's 800×680 card size, swap them
into the drink cards in `js/products.js`, verify in the browser, and deploy to Netlify.
No code changes are needed if the filenames match — they overwrite the existing images.
