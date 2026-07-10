const crypto = require("crypto");

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const SHEET_NAME = "Contact Submissions";

function redirect(location, statusCode = 303) {
  return {
    statusCode,
    headers: { Location: location },
    body: "",
  };
}

function parseBody(event) {
  const contentType = event.headers["content-type"] || event.headers["Content-Type"] || "";

  if (contentType.includes("application/json")) {
    return JSON.parse(event.body || "{}");
  }

  const params = new URLSearchParams(event.body || "");
  return Object.fromEntries(params.entries());
}

function base64Url(input) {
  return Buffer.from(input)
    .toString("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

async function getAccessToken() {
  const clientEmail = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKey = (process.env.GOOGLE_PRIVATE_KEY || "").replace(/\\n/g, "\n");

  if (!clientEmail || !privateKey) {
    throw new Error("Missing Google service account environment variables.");
  }

  const now = Math.floor(Date.now() / 1000);
  const header = base64Url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const claim = base64Url(
    JSON.stringify({
      iss: clientEmail,
      scope: "https://www.googleapis.com/auth/spreadsheets",
      aud: TOKEN_URL,
      exp: now + 3600,
      iat: now,
    })
  );

  const unsignedToken = `${header}.${claim}`;
  const signer = crypto.createSign("RSA-SHA256");
  signer.update(unsignedToken);
  signer.end();
  const signature = signer
    .sign(privateKey, "base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");

  const response = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
      assertion: `${unsignedToken}.${signature}`,
    }),
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error_description || payload.error || "Google token request failed.");
  }

  return payload.access_token;
}

async function appendToSheet(values) {
  const sheetId = process.env.GOOGLE_SHEET_ID;
  if (!sheetId) {
    throw new Error("Missing GOOGLE_SHEET_ID environment variable.");
  }

  const accessToken = await getAccessToken();
  const range = encodeURIComponent(`${SHEET_NAME}!A:J`);
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${range}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ values: [values] }),
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`Google Sheets append failed: ${message}`);
  }
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  try {
    const data = parseBody(event);
    if (data["bot-field"]) {
      return redirect("/contact.html?sent=1");
    }

    const headers = event.headers || {};
    const submittedAt = new Date().toISOString();
    const row = [
      submittedAt,
      event.headers["x-nf-request-id"] || "",
      data.name || "",
      data.phone || "",
      data.email || "",
      data.subject || "",
      data.message || "",
      headers.referer || headers.referrer || "",
      headers["user-agent"] || "",
      headers["x-nf-client-connection-ip"] || headers["client-ip"] || "",
    ];

    await appendToSheet(row);
    return redirect("/contact.html?sent=1");
  } catch (error) {
    console.error("Contact form sync failed:", error);
    return {
      statusCode: 500,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
      body: "Sorry, your message could not be saved. Please call or text 301-892-6707.",
    };
  }
};
