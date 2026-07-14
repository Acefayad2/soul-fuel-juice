/* Soul Fuel Juice — Square payment config (PUBLIC values, safe to commit)
 *
 * Fill these in from your Square Developer dashboard (developer.squareup.com):
 *   APP_ID      — "Application ID"  (sandbox starts with "sandbox-sq0idb-...",
 *                                    production starts with "sq0idp-...")
 *   LOCATION_ID — a location id from your account
 *   ENVIRONMENT — "sandbox" while testing, then "production" to take real cards
 *
 * The SECRET access token is NOT here — it goes in Netlify env var
 * SQUARE_ACCESS_TOKEN (plus SQUARE_LOCATION_ID and SQUARE_ENVIRONMENT).
 *
 * Payments stay OFF until APP_ID and LOCATION_ID below are filled in; until
 * then the site falls back to the existing "pay by Cash App / Zelle" flow.
 */
window.SQUARE_CONFIG = {
  APP_ID: "sandbox-sq0idb-8jgUgU113NkT8-oAgf2xiw",
  LOCATION_ID: "LSXKDVXX90XFW",
  ENVIRONMENT: "sandbox", // "sandbox" or "production"
};
