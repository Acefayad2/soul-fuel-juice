/* Soul Fuel Juice — Square Web Payments checkout (card + Apple Pay + Google Pay)
 * Activates only when js/square-config.js has APP_ID + LOCATION_ID filled in.
 * Until then, the existing "Send Order / pay by Cash App or Zelle" flow stays. */
(function () {
  "use strict";
  var cfg = window.SQUARE_CONFIG || {};
  if (!cfg.APP_ID || !cfg.LOCATION_ID) return; // not configured -> keep fallback

  var modal = document.querySelector(".checkout-modal");
  if (!modal) return;
  var form = modal.querySelector("form[name='order']");
  if (!form) return;

  var CART_KEY = "sfj-cart";
  var money = function (n) { return "$" + (Number.isInteger(n) ? n : n.toFixed(2)); };
  var getCart = function () { try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch (e) { return []; } };

  var sdkUrl = cfg.ENVIRONMENT === "production"
    ? "https://web.squarecdn.com/v1/square.js"
    : "https://sandbox.web.squarecdn.com/v1/square.js";

  var card = null, payments = null, mounted = false, initPromise = null;
  var applePay = null, googlePay = null;

  // Apple Pay button styling.
  var apStyle = document.createElement("style");
  apStyle.textContent =
    ".apple-pay-button{display:block;width:100%;height:48px;-webkit-appearance:-apple-pay-button;appearance:-apple-pay-button;-apple-pay-button-type:plain;-apple-pay-button-style:black;border-radius:999px;cursor:pointer}";
  document.head.appendChild(apStyle);

  // Swap the Cash App/Zelle note + "Send Order" button for the payment UI.
  var payInfo = form.querySelector(".pay-info");
  var submitBtn = form.querySelector("button[type='submit']");
  var ui = document.createElement("div");
  ui.innerHTML =
    '<div id="sfj-wallets" style="display:none;margin:0 0 12px">' +
      '<div id="sfj-applepay" style="display:none;margin-bottom:8px"></div>' +
      '<div id="sfj-gpay" style="display:none;margin-bottom:8px"></div>' +
      '<div id="sfj-wallet-or" style="display:none;text-align:center;color:var(--ink-soft);font-size:.82rem;margin:4px 0 2px">— or pay by card —</div>' +
    '</div>' +
    '<div class="field field--full">' +
      '<label for="sfj-card-container">Pay securely by card <span class="req">*</span></label>' +
      '<div id="sfj-card-container" style="padding:6px 0"></div></div>' +
    '<p id="sfj-fee-note" style="font-size:.82rem;color:var(--ink-soft);margin:2px 0 6px"></p>' +
    '<p id="sfj-pay-status" role="status" aria-live="polite" style="min-height:1.2em;font-size:.9rem;margin:4px 0 10px"></p>' +
    '<button type="button" id="sfj-pay-btn" class="btn btn--forest" style="width:100%">Pay</button>';
  if (payInfo) payInfo.style.display = "none";
  if (submitBtn) submitBtn.style.display = "none";
  form.appendChild(ui);

  var intro = modal.querySelector(".modal > p.muted");
  if (intro) {
    intro.innerHTML =
      "Pay securely below — card, Apple Pay, or Google Pay. Your order is confirmed " +
      "instantly and we’ll reach out about delivery, pickup, or shipping. Payments are handled by " +
      "Square — we never see or store your card.";
  }

  var statusEl = ui.querySelector("#sfj-pay-status");
  var payBtn = ui.querySelector("#sfj-pay-btn");
  var walletWrap = ui.querySelector("#sfj-wallets");

  function setStatus(msg, isError) {
    statusEl.textContent = msg || "";
    statusEl.style.color = isError ? "#B3261E" : "var(--forest-3)";
  }

  var fellBack = false;
  function revealFallback() {
    if (fellBack) return;
    fellBack = true;
    ui.style.display = "none";
    if (payInfo) payInfo.style.display = "";
    if (submitBtn) submitBtn.style.display = "";
    if (intro) {
      intro.innerHTML =
        "Send us your order below and we’ll confirm your total, then you pay by " +
        "Cash App or Zelle. (Card payment is being set up.)";
    }
  }

  function subtotalAndFulfillment() {
    var cart = getCart();
    var subtotal = cart.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var f = form.querySelector("[name='fulfillment']");
    return { subtotal: subtotal, v: f ? f.value : "" };
  }

  function orderTotal() {
    var x = subtotalAndFulfillment();
    if (/ship/i.test(x.v)) return x.subtotal + 18;
    if (/deliver/i.test(x.v) && x.subtotal < 50) return x.subtotal + 10;
    return x.subtotal;
  }

  function feeNote() {
    var x = subtotalAndFulfillment();
    if (/ship/i.test(x.v)) return "Includes $18 flat-rate shipping.";
    if (/deliver/i.test(x.v)) return x.subtotal >= 50 ? "Free local delivery (order $50+)." : "Includes a $10 local delivery fee.";
    return "";
  }

  function refreshAmount() {
    var t = orderTotal();
    payBtn.textContent = "Pay " + money(t);
    payBtn.disabled = t <= 0;
    var note = document.getElementById("sfj-fee-note");
    if (note) note.textContent = feeNote();
  }

  function loadSdk() {
    return new Promise(function (resolve, reject) {
      if (window.Square) return resolve();
      var s = document.createElement("script");
      s.src = sdkUrl;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("Could not load the Square payment library.")); };
      document.head.appendChild(s);
    });
  }

  function initCard() {
    if (initPromise) return initPromise;
    initPromise = loadSdk().then(function () {
      payments = window.Square.payments(cfg.APP_ID, cfg.LOCATION_ID);
      return payments.card();
    }).then(function (c) {
      card = c;
      return card.attach("#sfj-card-container");
    }).then(function () { mounted = true; buildWallets(); }).catch(function (err) {
      setStatus(err.message || "Payment form failed to load.", true);
      throw err;
    });
    return initPromise;
  }

  // Build Apple Pay / Google Pay buttons for the current total. Safe to call repeatedly;
  // each button only appears if the device/browser supports it (and, for Apple Pay, the
  // domain is registered in Square). Failures hide the wallet quietly — card still works.
  var buildingWallets = false;
  async function buildWallets() {
    if (!payments || buildingWallets) return;
    buildingWallets = true;
    try {
      try { if (applePay && applePay.destroy) await applePay.destroy(); } catch (e) {}
      try { if (googlePay && googlePay.destroy) await googlePay.destroy(); } catch (e) {}
      applePay = null; googlePay = null;
      var apEl = document.getElementById("sfj-applepay");
      var gpEl = document.getElementById("sfj-gpay");
      apEl.innerHTML = ""; apEl.style.display = "none";
      gpEl.innerHTML = ""; gpEl.style.display = "none";

      var total = orderTotal();
      if (total <= 0) { walletWrap.style.display = "none"; return; }

      var req = payments.paymentRequest({
        countryCode: "US",
        currencyCode: "USD",
        total: { amount: total.toFixed(2), label: "Soul Fuel Juice" },
      });

      var anyShown = false;
      try {
        applePay = await payments.applePay(req);
        apEl.innerHTML = '<button type="button" class="apple-pay-button" aria-label="Pay with Apple Pay"></button>';
        apEl.style.display = "block";
        apEl.querySelector("button").addEventListener("click", function () { walletPay(applePay); });
        anyShown = true;
      } catch (e) { /* Apple Pay unavailable on this device/domain */ }

      try {
        googlePay = await payments.googlePay(req);
        gpEl.style.display = "block";
        await googlePay.attach("#sfj-gpay", { buttonColor: "black", buttonType: "long", buttonSizeMode: "fill" });
        gpEl.addEventListener("click", function () { walletPay(googlePay); });
        anyShown = true;
      } catch (e) { gpEl.style.display = "none"; /* Google Pay unavailable */ }

      document.getElementById("sfj-wallet-or").style.display = anyShown ? "block" : "none";
      walletWrap.style.display = anyShown ? "block" : "none";
    } catch (e) {
      walletWrap.style.display = "none";
    } finally {
      buildingWallets = false;
    }
  }

  // Shared: send a payment token + order to the serverless function.
  async function submitPayment(token) {
    var cart = getCart();
    if (!cart.length) { setStatus("Your cart is empty.", true); return false; }
    var customer = {
      name: (form.querySelector("[name='name']") || {}).value || "",
      phone: (form.querySelector("[name='phone']") || {}).value || "",
      email: (form.querySelector("[name='email']") || {}).value || "",
      fulfillment: (form.querySelector("[name='fulfillment']") || {}).value || "",
      address: (form.querySelector("[name='address']") || {}).value || "",
      notes: (form.querySelector("[name='notes']") || {}).value || "",
    };
    var items = cart.map(function (i) { return { id: i.id, size: i.size, qty: i.qty }; });

    var resp = await fetch("/.netlify/functions/square-payment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: token, items: items, customer: customer }),
    });
    var data = await resp.json();
    if (!resp.ok || !data.ok) {
      var msg = data.error || "Payment could not be completed.";
      if (resp.status >= 500 || /not been enabled|not configured|service error/i.test(msg)) {
        revealFallback();
      } else {
        setStatus(msg, true);
      }
      return false;
    }

    if (window.sfjLogOrder) {
      window.sfjLogOrder({
        order: data.paymentId || "",
        name: customer.name, phone: customer.phone, email: customer.email,
        fulfillment: customer.fulfillment, address: customer.address,
        items: cart.map(function (i) { return i.qty + "x " + i.name + " (" + i.size + ")"; }).join(", "),
        total: "$" + data.amount,
        payment: "Card / Apple Pay / Google Pay",
        notes: customer.notes,
      });
    }

    localStorage.removeItem(CART_KEY);
    document.querySelectorAll(".cart-count").forEach(function (el) { el.textContent = "0"; el.style.display = "none"; });
    var modalInner = modal.querySelector(".modal");
    if (modalInner) {
      modalInner.innerHTML =
        '<button type="button" class="modal-close" aria-label="Close">&times;</button>' +
        '<h2>Thank you &amp; God bless! &#10084;</h2>' +
        '<p>Your payment of <strong>' + money(Number(data.amount)) + '</strong> went through. ' +
        "We&rsquo;ll confirm your delivery, pickup, or shipping details by text or email shortly.</p>" +
        '<p class="muted" style="font-size:.9rem">Questions? Call or text 301-892-6707.</p>';
    }
    return true;
  }

  function requireContact() {
    var name = (form.querySelector("[name='name']") || {}).value;
    var phone = (form.querySelector("[name='phone']") || {}).value;
    if (!name || !phone) { setStatus("Please add your name and phone first.", true); return false; }
    return true;
  }

  // Apple Pay / Google Pay button handler.
  async function walletPay(wallet) {
    if (!wallet || !requireContact()) return;
    if (!getCart().length) { setStatus("Your cart is empty.", true); return; }
    setStatus("Processing…");
    try {
      var result = await wallet.tokenize();
      if (result.status !== "OK") { setStatus("Payment was canceled.", true); return; }
      await submitPayment(result.token);
    } catch (e) {
      setStatus("Wallet payment couldn’t be completed — please try a card.", true);
    }
  }

  // Card "Pay" button handler.
  payBtn.addEventListener("click", async function () {
    if (!requireContact()) return;
    if (!getCart().length) { setStatus("Your cart is empty.", true); return; }
    if (!card) { setStatus("Payment form is still loading — one moment.", true); return; }
    payBtn.disabled = true;
    setStatus("Processing…");
    try {
      var result = await card.tokenize();
      if (result.status !== "OK") {
        setStatus("Please check your card details and try again.", true);
        payBtn.disabled = false;
        return;
      }
      var ok = await submitPayment(result.token);
      if (!ok) payBtn.disabled = false;
    } catch (err) {
      setStatus("Something went wrong processing your card. Please try again.", true);
      payBtn.disabled = false;
    }
  });

  // Mount + refresh whenever the checkout modal opens; rebuild wallets on amount change.
  var observer = new MutationObserver(function () {
    if (modal.classList.contains("open")) {
      if (!mounted) initCard().catch(function () {});
      else buildWallets();
      refreshAmount();
    }
  });
  observer.observe(modal, { attributes: true, attributeFilter: ["class"] });
  form.addEventListener("change", function (e) {
    if (e.target && e.target.name === "fulfillment") { refreshAmount(); buildWallets(); }
  });
})();
