/* Soul Fuel Juice — Square Web Payments card checkout (frontend)
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

  // Swap the Cash App/Zelle note + "Send Order" button for a card form + Pay button.
  var payInfo = form.querySelector(".pay-info");
  var submitBtn = form.querySelector("button[type='submit']");
  var ui = document.createElement("div");
  ui.innerHTML =
    '<div class="field field--full">' +
    '<label for="sfj-card-container">Pay securely by card <span class="req">*</span></label>' +
    '<div id="sfj-card-container" style="padding:6px 0"></div></div>' +
    '<p id="sfj-pay-status" role="status" aria-live="polite" style="min-height:1.2em;font-size:.9rem;margin:4px 0 10px"></p>' +
    '<button type="button" id="sfj-pay-btn" class="btn btn--forest" style="width:100%">Pay</button>';
  if (payInfo) payInfo.style.display = "none";
  if (submitBtn) submitBtn.style.display = "none";
  form.appendChild(ui);

  var statusEl = ui.querySelector("#sfj-pay-status");
  var payBtn = ui.querySelector("#sfj-pay-btn");

  function setStatus(msg, isError) {
    statusEl.textContent = msg || "";
    statusEl.style.color = isError ? "#B3261E" : "var(--forest-3)";
  }

  function orderTotal() {
    var cart = getCart();
    var total = cart.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var fulfill = form.querySelector("[name='fulfillment']");
    if (fulfill && /ship/i.test(fulfill.value)) total += 18;
    return total;
  }

  function refreshAmount() {
    var t = orderTotal();
    payBtn.textContent = "Pay " + money(t);
    payBtn.disabled = t <= 0;
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
    }).then(function () { mounted = true; }).catch(function (err) {
      setStatus(err.message || "Payment form failed to load.", true);
      throw err;
    });
    return initPromise;
  }

  // Mount the card + refresh the amount whenever the checkout modal opens.
  var observer = new MutationObserver(function () {
    if (modal.classList.contains("open")) {
      if (!mounted) initCard().catch(function () {});
      refreshAmount();
    }
  });
  observer.observe(modal, { attributes: true, attributeFilter: ["class"] });
  form.addEventListener("change", function (e) {
    if (e.target && e.target.name === "fulfillment") refreshAmount();
  });

  payBtn.addEventListener("click", async function () {
    var name = (form.querySelector("[name='name']") || {}).value;
    var phone = (form.querySelector("[name='phone']") || {}).value;
    if (!name || !phone) { setStatus("Please add your name and phone first.", true); return; }
    var cart = getCart();
    if (!cart.length) { setStatus("Your cart is empty.", true); return; }
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
      var customer = {
        name: name,
        phone: phone,
        email: (form.querySelector("[name='email']") || {}).value || "",
        fulfillment: (form.querySelector("[name='fulfillment']") || {}).value || "",
        address: (form.querySelector("[name='address']") || {}).value || "",
        notes: (form.querySelector("[name='notes']") || {}).value || "",
      };
      var items = cart.map(function (i) { return { id: i.id, size: i.size, qty: i.qty }; });

      var resp = await fetch("/.netlify/functions/square-payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: result.token, items: items, customer: customer }),
      });
      var data = await resp.json();
      if (!resp.ok || !data.ok) {
        setStatus(data.error || "Payment could not be completed.", true);
        payBtn.disabled = false;
        return;
      }

      // Success — clear cart and show confirmation.
      localStorage.removeItem(CART_KEY);
      document.querySelectorAll(".cart-count").forEach(function (el) { el.textContent = "0"; el.style.display = "none"; });
      var modalInner = modal.querySelector(".modal");
      if (modalInner) {
        modalInner.innerHTML =
          '<button type="button" class="modal-close" aria-label="Close">&times;</button>' +
          '<h2>Thank you &amp; God bless! &#10084;</h2>' +
          '<p>Your payment of <strong>' + money(Number(data.amount)) + '</strong> went through. ' +
          "We&rsquo;ll confirm your delivery or shipping details by text or email shortly.</p>" +
          '<p class="muted" style="font-size:.9rem">Questions? Call or text 301-892-6707.</p>';
      }
    } catch (err) {
      setStatus("Something went wrong processing your card. Please try again.", true);
      payBtn.disabled = false;
    }
  });
})();
