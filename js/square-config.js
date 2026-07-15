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
  APP_ID: "sq0idp--mDOxRLwAWdcUXqTOayj5Q",
  LOCATION_ID: "L41T8XMRT0Q31",
  ENVIRONMENT: "production", // "sandbox" or "production"
};

/* Google Sheet order-tracking webhook (Google Apps Script Web App /exec URL).
 * Paste the deployed web-app URL here to log every order to the
 * "Soul Fuel Juice — Orders" sheet. Leave blank to disable logging. */
window.SHEETS_WEBHOOK = "https://script.google.com/macros/s/AKfycbyTr-duDH27gRDLMZaDZN0zBok33EPPYZ5wqQrrhSmfsG645Wo02abyOmbMCC4uU_lx/exec";
