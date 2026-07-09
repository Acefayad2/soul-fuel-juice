/* Soul Fuel Juice — site behavior: nav, product grids, cart, checkout, forms */

(function () {
  "use strict";

  /* ---------- Mobile nav ---------- */
  const navToggle = document.querySelector(".nav-toggle");
  const mainNav = document.querySelector(".main-nav");
  if (navToggle && mainNav) {
    navToggle.addEventListener("click", () => {
      const open = mainNav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
      }),
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("visible"));
  }

  /* ---------- Toast ---------- */
  let toastTimer;
  function toast(msg) {
    let el = document.querySelector(".toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "toast";
      el.setAttribute("role", "status");
      el.setAttribute("aria-live", "polite");
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("show"), 3200);
  }

  /* ---------- Cart state ---------- */
  const CART_KEY = "sfj-cart";
  const money = (n) => "$" + (Number.isInteger(n) ? n : n.toFixed(2));
  const getCart = () => { try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch { return []; } };
  const saveCart = (c) => { localStorage.setItem(CART_KEY, JSON.stringify(c)); renderCartCount(); renderCartDrawer(); };
  const findProduct = (id) => (typeof PRODUCTS !== "undefined" ? PRODUCTS.find((p) => p.id === id) : null);

  function addToCart(id, sizeLabel) {
    const product = findProduct(id);
    if (!product) return;
    const size = product.sizes.find((s) => s.label === sizeLabel) || product.sizes[0];
    const cart = getCart();
    const existing = cart.find((i) => i.id === id && i.size === size.label);
    if (existing) existing.qty += 1;
    else cart.push({ id, name: product.name, size: size.label, price: size.price, img: product.img, qty: 1 });
    saveCart(cart);
    toast(product.name + " (" + size.label + ") added to cart");
  }

  function renderCartCount() {
    const count = getCart().reduce((s, i) => s + i.qty, 0);
    document.querySelectorAll(".cart-count").forEach((el) => {
      el.textContent = count;
      el.style.display = count ? "flex" : "none";
    });
  }

  /* ---------- Cart drawer ---------- */
  const overlay = document.querySelector(".cart-overlay");
  const drawer = document.querySelector(".cart-drawer");

  function openCart() {
    if (!drawer) return;
    renderCartDrawer();
    drawer.classList.add("open");
    overlay && overlay.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeCart() {
    if (!drawer) return;
    drawer.classList.remove("open");
    overlay && overlay.classList.remove("open");
    document.body.style.overflow = "";
  }

  function renderCartDrawer() {
    const itemsEl = document.querySelector(".cart-items");
    const totalEl = document.querySelector(".cart-total");
    if (!itemsEl) return;
    const cart = getCart();
    if (!cart.length) {
      itemsEl.innerHTML = '<p class="cart-empty">Your cart is empty.<br>Fill it with something fresh &amp; purposeful.</p>';
    } else {
      itemsEl.innerHTML = cart.map((i, idx) => `
        <div class="cart-item">
          <img src="${i.img}" alt="" width="62" height="62">
          <div>
            <h4>${i.name}</h4>
            <div class="meta">${i.size} · ${money(i.price)} each</div>
            <div class="qty-controls">
              <button type="button" data-qty="-1" data-idx="${idx}" aria-label="Decrease quantity">−</button>
              <span aria-live="polite">${i.qty}</span>
              <button type="button" data-qty="1" data-idx="${idx}" aria-label="Increase quantity">+</button>
            </div>
          </div>
          <div style="text-align:right">
            <div class="line-price">${money(i.price * i.qty)}</div>
            <button type="button" class="remove" data-remove="${idx}">Remove</button>
          </div>
        </div>`).join("");
    }
    const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
    if (totalEl) totalEl.textContent = money(total);
    const checkoutBtn = document.querySelector(".checkout-btn");
    if (checkoutBtn) checkoutBtn.disabled = !cart.length;
  }

  document.addEventListener("click", (e) => {
    const t = e.target;
    if (t.closest(".cart-btn")) { openCart(); return; }
    if (t.closest(".cart-close") || t === overlay) { closeCart(); return; }
    const qtyBtn = t.closest("[data-qty]");
    if (qtyBtn) {
      const cart = getCart();
      const item = cart[Number(qtyBtn.dataset.idx)];
      if (item) {
        item.qty += Number(qtyBtn.dataset.qty);
        if (item.qty <= 0) cart.splice(Number(qtyBtn.dataset.idx), 1);
        saveCart(cart);
      }
      return;
    }
    const removeBtn = t.closest("[data-remove]");
    if (removeBtn) {
      const cart = getCart();
      cart.splice(Number(removeBtn.dataset.remove), 1);
      saveCart(cart);
      return;
    }
    const addBtn = t.closest("[data-add]");
    if (addBtn) {
      const card = addBtn.closest("[data-product]");
      const select = card ? card.querySelector(".size-select") : null;
      addToCart(addBtn.dataset.add, select ? select.value : undefined);
      return;
    }
    if (t.closest(".checkout-btn")) { openCheckout(); return; }
    if (t.closest(".modal-close")) { closeCheckout(); return; }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeCart(); closeCheckout(); }
  });

  /* ---------- Product size select → price update ---------- */
  document.addEventListener("change", (e) => {
    const select = e.target.closest(".size-select");
    if (!select) return;
    const card = select.closest("[data-product]");
    const priceEl = card && card.querySelector(".price");
    const product = findProduct(card && card.dataset.product);
    if (product && priceEl) {
      const size = product.sizes.find((s) => s.label === select.value);
      if (size) priceEl.textContent = money(size.price);
    }
  });

  /* ---------- Product grid rendering ---------- */
  function productCard(p) {
    const sizeOptions = p.sizes.map((s) => `<option value="${s.label}">${s.label}</option>`).join("");
    const typeLabel = p.type === "juice" ? "Cold-Pressed Juice" : p.type === "shot" ? "Wellness Shot" : "Bundle & Cleanse";
    const isSvg = p.img.endsWith(".svg");
    return `
      <article class="card reveal" data-product="${p.id}" data-type="${p.type}">
        <div class="card-media"><img src="${p.img}" alt="${p.name} — ${typeLabel}" loading="lazy" ${isSvg ? "" : 'width="800" height="680"'}></div>
        <div class="card-body">
          <span class="card-tag">${typeLabel}</span>
          <h3>${p.name}</h3>
          <p class="ingredients">${p.ingredients}</p>
          <div class="benefit-chips">${p.benefits.map((b) => `<span>${b}</span>`).join("")}</div>
          <div class="card-buy">
            ${p.sizes.length > 1 ? `<label class="visually-hidden" for="size-${p.id}">Size</label><select class="size-select" id="size-${p.id}" aria-label="Choose size">${sizeOptions}</select>` : `<span class="ingredients">${p.sizes[0].label}</span>`}
            <span class="price">${money(p.sizes[0].price)}</span>
            <button type="button" class="btn btn--forest btn--sm" data-add="${p.id}">Add to Cart</button>
          </div>
        </div>
      </article>`;
  }

  document.querySelectorAll("[data-product-grid]").forEach((grid) => {
    const types = grid.dataset.productGrid.split(",");
    const ids = grid.dataset.products ? grid.dataset.products.split(",") : null;
    let items = PRODUCTS.filter((p) => types.includes("all") || types.includes(p.type));
    if (ids) items = ids.map((id) => findProduct(id)).filter(Boolean);
    grid.innerHTML = items.map(productCard).join("");
    grid.querySelectorAll(".reveal").forEach((el) => el.classList.add("visible"));
  });

  /* ---------- Shop filter tabs ---------- */
  const tabs = document.querySelectorAll(".filter-tabs button");
  tabs.forEach((tab) => tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    const type = tab.dataset.filter;
    document.querySelectorAll("[data-product-grid] [data-type]").forEach((card) => {
      card.style.display = type === "all" || card.dataset.type === type ? "" : "none";
    });
  }));

  /* ---------- Checkout modal ---------- */
  const checkoutModal = document.querySelector(".checkout-modal");

  function openCheckout() {
    if (!checkoutModal) { window.location.href = "shop.html"; return; }
    const cart = getCart();
    if (!cart.length) return;
    const summary = cart.map((i) => `${i.qty} × ${i.name} (${i.size}) — ${money(i.price * i.qty)}`).join("\n");
    const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const summaryField = checkoutModal.querySelector("[name='order-summary']");
    const totalField = checkoutModal.querySelector("[name='order-total']");
    const summaryView = checkoutModal.querySelector(".order-summary-view");
    if (summaryField) summaryField.value = summary + "\nTotal: " + money(total);
    if (totalField) totalField.value = money(total);
    if (summaryView) summaryView.innerHTML = cart.map((i) => `<li>${i.qty} × ${i.name} (${i.size}) — <strong>${money(i.price * i.qty)}</strong></li>`).join("") + `<li style="margin-top:8px"><strong>Total: ${money(total)}</strong></li>`;
    closeCart();
    checkoutModal.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeCheckout() {
    if (!checkoutModal) return;
    checkoutModal.classList.remove("open");
    document.body.style.overflow = "";
  }

  /* Clear cart after successful order submit (Netlify redirects back with ?order=received) */
  if (new URLSearchParams(window.location.search).get("order") === "received") {
    localStorage.removeItem(CART_KEY);
    toast("Order received! We'll confirm by text or email shortly. God bless!");
  }
  if (new URLSearchParams(window.location.search).get("sent") === "1") {
    toast("Message sent! We'll get back to you soon.");
  }

  renderCartCount();
  renderCartDrawer();
})();
