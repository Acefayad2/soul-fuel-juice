/* Soul Fuel Juice — product catalog
   Juice sizes/prices from the official price list:
   8oz $9 · 12oz $12 · 16oz $15 · 20oz $18
   NOTE: wellness shot price set to $5 — CONFIRM with owner before launch. */

const JUICE_SIZES = [
  { label: "8 oz", price: 9 },
  { label: "12 oz", price: 12 },
  { label: "16 oz", price: 15 },
  { label: "20 oz", price: 18 },
];

const PRODUCTS = [
  /* ---- Cold-pressed juices ---- */
  {
    id: "healing-greens", type: "juice", name: "Healing Greens",
    img: "/assets/img/healing-greens.jpg",
    ingredients: "Kale, Apple, Cucumber, Spinach, Lemon, Celery, Ginger",
    benefits: ["Detox", "Gut Health", "Immunity", "Hydration", "Skin & Eye Health"],
    sizes: JUICE_SIZES,
  },
  {
    id: "golden-glow", type: "juice", name: "Golden Glow",
    img: "/assets/img/golden-glow.jpg",
    ingredients: "Mango, Pineapple, Carrot, Lemon, Ginger",
    benefits: ["Vitamins A & C", "Energy", "Skin & Eye Health", "Digestive Health"],
    sizes: JUICE_SIZES,
  },
  {
    id: "carrot-glow", type: "juice", name: "Carrot Glow",
    img: "/assets/img/carrot-glow.jpg",
    ingredients: "Pineapple, Orange, Carrot, Turmeric, Ginger",
    benefits: ["Brain & Eye Health", "Immunity", "Circulation", "Glow"],
    sizes: JUICE_SIZES,
  },
  {
    id: "queens-power", type: "juice", name: "Queen's Power",
    img: "/assets/img/queens-power.jpg",
    ingredients: "Beetroot, Watermelon, Ginger, Pineapple, Lemon, Maca Root Powder",
    benefits: ["Hormonal Balance", "Stamina", "Iron & Blood Health", "Skin Glow"],
    sizes: JUICE_SIZES,
  },
  {
    id: "beet-bless", type: "juice", name: "Beet & Bless",
    img: "/assets/img/beet-bless.jpg",
    ingredients: "Beets, Apple, Ginger, Carrot, Hint of Lemon",
    benefits: ["Circulation", "Digestion", "Liver Health", "Endurance"],
    sizes: JUICE_SIZES,
  },
  {
    id: "island-glow", type: "juice", name: "Island Glow",
    img: "/assets/img/island-glow.jpg",
    ingredients: "Watermelon, Cucumber, Pineapple, Lime, Ginger",
    benefits: ["Hydration", "Collagen Boost", "Digestion Aid", "Refreshing Energy"],
    sizes: JUICE_SIZES,
  },

  /* ---- Wellness shots (2 oz) ---- */
  {
    id: "citrus-defense", type: "shot", name: "Citrus Defense",
    img: "/assets/img/shot-citrus-defense.jpg",
    ingredients: "Immune & digestion support with Vitamin C",
    benefits: ["Immunity", "Vitamin C", "Digestion"],
    sizes: [{ label: "2 oz", price: 5 }],
  },
  {
    id: "fiery-ginger", type: "shot", name: "Fiery Ginger",
    img: "/assets/img/shot-fiery-ginger.jpg",
    ingredients: "Ginger, Lemon, Cayenne, Honey, Coconut Water",
    benefits: ["Metabolism", "Circulation", "Anti-Inflammatory"],
    sizes: [{ label: "2 oz", price: 5 }],
  },
  {
    id: "immune-shield", type: "shot", name: "Immune Shield",
    img: "/assets/img/shot-immune-shield.jpg",
    ingredients: "Anti-inflammatory blend with a Vitamin C boost",
    benefits: ["Immunity", "Anti-Inflammatory", "Vitamin C"],
    sizes: [{ label: "2 oz", price: 5 }],
  },
  {
    id: "golden-root-tonic", type: "shot", name: "Golden Root Tonic",
    img: "/assets/img/shot-golden-root.jpg",
    ingredients: "Turmeric-forward golden root blend",
    benefits: ["Immune Support", "Anti-Inflammatory", "Joint Health"],
    sizes: [{ label: "2 oz", price: 5 }],
  },
  {
    id: "pineapple-mint-soother", type: "shot", name: "Pineapple Mint Soother",
    img: "/assets/img/shot-pineapple-mint.jpg",
    ingredients: "Pineapple, Mint, Lime, Honey, Ginger",
    benefits: ["Liver Support", "Digestion", "Reduces Bloating"],
    sizes: [{ label: "2 oz", price: 5 }],
  },
  {
    id: "spiced-beet-elixir", type: "shot", name: "Spiced Beet Elixir",
    img: "/assets/img/shot-spiced-beet.jpg",
    ingredients: "Spiced beet blend for daily vitality",
    benefits: ["Stamina", "Endurance", "Detox", "Circulation"],
    sizes: [{ label: "2 oz", price: 5 }],
  },

  /* ---- Bundles & cleanse packs ---- */
  {
    id: "sampler-3", type: "bundle", name: "3-Pack Sampler",
    img: "/assets/img/juice-trio.jpg",
    ingredients: "Mix & match any three juices — tell us your flavors at checkout",
    benefits: ["Mix & Match", "Best For First-Timers"],
    sizes: [
      { label: "3 × 8 oz", price: 27 },
      { label: "3 × 12 oz", price: 34 },
    ],
  },
  {
    id: "detox-3day", type: "bundle", name: "3-Day Detox Challenge",
    img: "/assets/img/lineup.jpg",
    ingredients: "9 fresh juices + downloadable devotional PDF",
    benefits: ["9 Juices", "Devotional PDF", "Reset & Refresh"],
    sizes: [
      { label: "9 × 8 oz", price: 81 },
      { label: "9 × 12 oz", price: 99 },
    ],
  },
  {
    id: "detox-7day", type: "bundle", name: "7-Day Detox + Devotional",
    img: "/assets/img/styled-greens-moss.jpg",
    ingredients: "21 juices + wellness shots + 7-Day Faith & Fit Devotional",
    benefits: ["21 Juices", "Wellness Shots", "7-Day Devotional"],
    sizes: [
      { label: "21 × 8 oz", price: 205 },
      { label: "21 × 12 oz", price: 245 },
    ],
  },
  {
    id: "soul-slim-3", type: "bundle", name: "3-Day Soul Slim Reset",
    img: "/assets/img/ph-soul-slim.svg",
    ingredients: "6 detox juices + Soul Slim Reset Guide + Discipline Tracker",
    benefits: ["Most Popular", "Reduce Bloating", "Boost Metabolism"],
    sizes: [{ label: "3-Day Reset", price: 49 }],
  },
  {
    id: "soul-slim-7", type: "bundle", name: "7-Day Soul Slim Transformation",
    img: "/assets/img/ph-soul-slim-7.svg",
    ingredients: "14 juices + Reset Guide + Discipline Tracker",
    benefits: ["Premium Reset", "14 Juices", "Full Transformation"],
    sizes: [{ label: "7-Day Reset", price: 99 }],
  },
];
