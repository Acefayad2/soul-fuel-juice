/**
 * Soul Fuel Juice — Square card payment processor
 *
 * Receives a card token (nonce) from the Square Web Payments SDK plus the
 * cart contents, recomputes the amount SERVER-SIDE from an authoritative price
 * map (so the client can't tamper with prices), and creates the payment via the
 * Square Payments API.
 *
 * Required Netlify environment variables:
 *   SQUARE_ACCESS_TOKEN   — secret access token from the Square Developer app
 *   SQUARE_LOCATION_ID    — the Square location id to attribute the sale to
 *   SQUARE_ENVIRONMENT    — "sandbox" (default) or "production"
 */

const crypto = require("crypto");

// Authoritative prices (must match js/products.js). Amount is charged from HERE,
// never from values sent by the browser.
const PRICES = {
  "healing-greens": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "golden-glow": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "carrot-glow": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "queens-power": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "beet-bless": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "island-glow": { "8 oz": 9, "12 oz": 12, "16 oz": 15, "20 oz": 18 },
  "citrus-defense": { "2 oz": 5 },
  "fiery-ginger": { "2 oz": 5 },
  "immune-shield": { "2 oz": 5 },
  "golden-root-tonic": { "2 oz": 5 },
  "pineapple-mint-soother": { "2 oz": 5 },
  "spiced-beet-elixir": { "2 oz": 5 },
  "sampler-3": { "3 × 8 oz": 27, "3 × 12 oz": 34 },
  "detox-3day": { "9 × 8 oz": 81, "9 × 12 oz": 99 },
  "detox-7day": { "21 × 8 oz": 205, "21 × 12 oz": 245 },
  "soul-slim-3": { "3-Day Reset": 49 },
  "soul-slim-7": { "7-Day Reset": 99 },
};

const SHIPPING_FLAT = 18; // $18 flat-rate shipping when the order is shipped

function json(statusCode, obj) {
  return {
    statusCode,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(obj),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return json(405, { error: "Method not allowed" });
  }

  const accessToken = process.env.SQUARE_ACCESS_TOKEN;
  const locationId = process.env.SQUARE_LOCATION_ID;
  const environment = (process.env.SQUARE_ENVIRONMENT || "sandbox").toLowerCase();

  if (!accessToken || !locationId) {
    return json(500, {
      error: "Payments are not configured yet. Please contact us to complete your order.",
    });
  }

  let data;
  try {
    data = JSON.parse(event.body || "{}");
  } catch {
    return json(400, { error: "Invalid request." });
  }

  const { token, items, customer } = data;
  if (!token) return json(400, { error: "Missing card token." });
  if (!Array.isArray(items) || items.length === 0) {
    return json(400, { error: "Your cart is empty." });
  }

  // Recompute the total from the server-side price map.
  let total = 0;
  const lineSummary = [];
  for (const item of items) {
    const priced = PRICES[item.id] && PRICES[item.id][item.size];
    const qty = Math.max(1, parseInt(item.qty, 10) || 0);
    if (priced == null) {
      return json(400, { error: `Unknown item in cart: ${item.id} (${item.size}).` });
    }
    total += priced * qty;
    lineSummary.push(`${qty}x ${item.id} (${item.size})`);
  }

  const ships = customer && /ship/i.test(customer.fulfillment || "");
  if (ships) total += SHIPPING_FLAT;

  const amountCents = Math.round(total * 100);
  if (amountCents <= 0) return json(400, { error: "Invalid order total." });

  const note =
    `Soul Fuel Juice order — ${lineSummary.join(", ")}` +
    (ships ? " + $18 shipping" : "") +
    (customer && customer.name ? ` | ${customer.name}` : "") +
    (customer && customer.phone ? ` ${customer.phone}` : "") +
    (customer && customer.fulfillment ? ` | ${customer.fulfillment}` : "");

  const host =
    environment === "production"
      ? "https://connect.squareup.com"
      : "https://connect.squareupsandbox.com";

  try {
    const resp = await fetch(`${host}/v2/payments`, {
      method: "POST",
      headers: {
        "Square-Version": "2024-08-21",
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source_id: token,
        idempotency_key: crypto.randomUUID(),
        amount_money: { amount: amountCents, currency: "USD" },
        location_id: locationId,
        note: note.slice(0, 500),
        buyer_email_address: customer && customer.email ? customer.email : undefined,
      }),
    });

    const payload = await resp.json();
    if (!resp.ok) {
      const detail =
        (payload.errors && payload.errors[0] && payload.errors[0].detail) ||
        "Payment could not be processed.";
      return json(402, { error: detail });
    }

    return json(200, {
      ok: true,
      amount: (amountCents / 100).toFixed(2),
      paymentId: payload.payment && payload.payment.id,
    });
  } catch (err) {
    console.error("Square payment failed:", err);
    return json(500, { error: "Payment service error. Please try again or contact us." });
  }
};
