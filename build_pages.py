#!/usr/bin/env python3
"""Generate Soul Fuel Juice static pages from a shared template."""
import os

ROOT = os.path.expanduser("~/soul-fuel-juice")

MARK = '''<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><path d="M50 89 C29 73 8 58 8 37 C8 24.5 17.5 15 30 15 C38.8 15 46 20 50 27.5 C54 20 61.2 15 70 15 C82.5 15 92 24.5 92 37 C92 58 71 73 50 89 Z" fill="currentColor"/><path d="M50 74 C37 64 24 55 24 41.5 C24 33.5 30 27.5 37.5 27.5 C43 27.5 47.5 30.7 50 35.4 C52.5 30.7 57 27.5 62.5 27.5 C70 27.5 76 33.5 76 41.5 C76 55 63 64 50 74 Z" fill="none" stroke="var(--mark-bg,#FAF6ED)" stroke-width="4"/><path d="M50 74 C50 58 54 40 68 30" fill="none" stroke="var(--mark-bg,#FAF6ED)" stroke-width="4" stroke-linecap="round"/></svg>'''

NAV_ITEMS = [
    ("index.html", "Home"), ("shop.html", "Shop"), ("cleanse.html", "Cleanse &amp; Detox"),
    ("wellness-shots.html", "Wellness Shots"), ("benefits.html", "Benefits"),
    ("about.html", "About"), ("blog.html", "Blog"), ("contact.html", "Contact"),
]

ICONS = {
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18h-5"/><path d="M14 8h5l3 5v4a1 1 0 0 1-1 1h-1"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
    "tt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"/></svg>',
}

STAR5 = ('<div class="stars" aria-label="5 out of 5 stars">' + ICONS["star"] * 5 + "</div>")


def head(title, desc, path, extra=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://soulfueljuice.com/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://soulfueljuice.com/assets/img/juice-trio.jpg">
<link rel="icon" type="image/svg+xml" href="assets/img/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Raleway:wght@300;400;500;600;700&family=Great+Vibes&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<style>.visually-hidden{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}</style>
{extra}
</head>
<body>'''


def header(active):
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{current if href == active else ""}>{label}</a>'
        for href, label in NAV_ITEMS
    )
    return f'''
<a class="visually-hidden" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Soul Fuel Juice home">
      {MARK}
      <span class="brand-name">SOUL FUEL<small>J U I C E</small></span>
    </a>
    <nav class="main-nav" aria-label="Main navigation">{links}</nav>
    <div class="header-actions">
      <button type="button" class="cart-btn" aria-label="Open cart">{ICONS["cart"]}<span class="cart-count" style="display:none">0</span></button>
      <button type="button" class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">{ICONS["menu"]}</button>
    </div>
  </div>
</header>
<main id="main">'''


CART_AND_CHECKOUT = f'''
<div class="cart-overlay"></div>
<aside class="cart-drawer" aria-label="Shopping cart">
  <div class="cart-head"><h3>Your Cart</h3><button type="button" class="cart-close" aria-label="Close cart">{ICONS["x"]}</button></div>
  <div class="cart-items"></div>
  <div class="cart-foot">
    <div class="cart-total-row"><span>Subtotal</span><span class="cart-total">$0</span></div>
    <p class="cart-note">Local delivery in Hagerstown, MD &amp; surrounding areas ($10, free on orders $50+), pickup, or $18 flat-rate shipping nationwide (added when we confirm your order). Please order 24&ndash;48 hours ahead.</p>
    <button type="button" class="btn btn--gold checkout-btn">Place Order</button>
  </div>
</aside>
<div class="modal-overlay checkout-modal" role="dialog" aria-modal="true" aria-label="Checkout">
  <div class="modal">
    <button type="button" class="modal-close" aria-label="Close checkout">{ICONS["x"]}</button>
    <h2>Complete Your Order</h2>
    <p class="muted" style="font-size:.92rem">Send us your order &mdash; we&rsquo;ll confirm your total (plus delivery or shipping) by text or email, then you pay securely by Cash App or Zelle.</p>
    <ul class="order-summary-view" style="padding-left:20px;font-size:.92rem"></ul>
    <form name="order" method="POST" action="/?order=received" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="order">
      <p class="visually-hidden"><label>Don&rsquo;t fill this out: <input name="bot-field"></label></p>
      <input type="hidden" name="order-summary">
      <input type="hidden" name="order-total">
      <div class="form-grid">
        <div class="field"><label for="o-name">Name <span class="req">*</span></label><input id="o-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="o-phone">Phone <span class="req">*</span></label><input id="o-phone" name="phone" type="tel" required autocomplete="tel"></div>
        <div class="field field--full"><label for="o-email">Email</label><input id="o-email" name="email" type="email" autocomplete="email"></div>
        <div class="field"><label for="o-fulfill">Delivery, Pickup or Shipping <span class="req">*</span></label>
          <select id="o-fulfill" name="fulfillment" required>
            <option>Local delivery — $10 (free over $50)</option>
            <option>Pickup</option>
            <option>Ship to me ($18 flat rate)</option>
          </select></div>
        <div class="field"><label for="o-date">Preferred date <span class="req">*</span></label><input id="o-date" name="preferred-date" type="date" required><span class="hint">Please allow 24&ndash;48 hours</span></div>
        <div class="field field--full"><label for="o-address">Shipping address (if shipping)</label><input id="o-address" name="address" autocomplete="street-address"></div>
        <div class="field field--full"><label for="o-notes">Notes (flavor choices, allergies, etc.)</label><textarea id="o-notes" name="notes" rows="3"></textarea></div>
      </div>
      <div class="pay-info" style="margin:18px 0">
        <strong>How payment works:</strong> after you place your order we&rsquo;ll confirm availability and total, then you can pay via
        <strong>Cash App ($Josiejo87)</strong> or <strong>Zelle (301-892-6707)</strong>. Thank you for supporting a small business! &#10084;
      </div>
      <button type="submit" class="btn btn--forest" style="width:100%">Send Order</button>
    </form>
  </div>
</div>'''


def footer():
    year = 2026
    return f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand" style="--mark-bg:#14271C">
        {MARK}
        <p class="scripture">&ldquo;&hellip;Be in health, even as your soul prospers.&rdquo; &mdash; 3 John 1:2</p>
        <p>Fresh, cold-pressed juice handcrafted in Hagerstown, Maryland. Fuel your body. Feed your soul.</p>
        <div class="social-links">
          <a href="https://instagram.com/soulfueljuice_" aria-label="Instagram" rel="noopener" target="_blank">{ICONS["ig"]}</a>
          <a href="https://www.facebook.com/SoulFuelJuice" aria-label="Facebook" rel="noopener" target="_blank">{ICONS["fb"]}</a>
          <a href="https://www.tiktok.com/@soulfueljuice" aria-label="TikTok" rel="noopener" target="_blank">{ICONS["tt"]}</a>
        </div>
      </div>
      <div>
        <h4>Shop</h4>
        <ul>
          <li><a href="shop.html">All Products</a></li>
          <li><a href="cleanse.html">Juice Cleanse &amp; Detox</a></li>
          <li><a href="wellness-shots.html">Wellness Shots</a></li>
          <li><a href="benefits.html">Health Benefits</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="testimonials.html">Testimonials</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="shipping.html">Shipping &amp; Delivery</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in Touch</h4>
        <ul>
          <li><a href="tel:+13018926707">301-892-6707</a></li>
          <li><a href="mailto:soulfueljuice@gmail.com">soulfueljuice@gmail.com</a></li>
          <li>Hagerstown, Maryland</li>
          <li><a href="contact.html">Contact Form</a></li>
        </ul>
        <p style="margin-top:14px;font-size:.82rem">Proudly serving Hagerstown, Frederick, Gaithersburg, Baltimore, Washington DC &amp; shipping nationwide.</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {year} Soul Fuel Juice LLC. All rights reserved.</span>
      <span><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms &amp; Conditions</a></span>
    </div>
    <p class="disclaimer">*These statements have not been evaluated by the Food and Drug Administration. Our products are not intended to diagnose, treat, cure, or prevent any disease. Please consult your physician before beginning any cleanse or detox program, especially if you are pregnant, nursing, or have a medical condition.</p>
  </div>
</footer>
{CART_AND_CHECKOUT}
<script src="js/products.js"></script>
<script src="js/main.js"></script>
</body>
</html>'''


def page(filename, title, desc, body, extra_head=""):
    html = head(title, desc, filename, extra_head) + header(filename) + body + footer()
    with open(os.path.join(ROOT, filename), "w") as f:
        f.write(html)
    print("wrote", filename)


NEWSLETTER = '''
<section class="section section--tight">
  <div class="container">
    <div class="newsletter reveal">
      <div>
        <span class="eyebrow">Join the community</span>
        <h2>Wellness for Body &amp; Soul, In Your Inbox</h2>
        <p>Fresh drops, cleanse tips, seasonal flavors, and a little encouragement. No spam &mdash; just goodness.</p>
      </div>
      <form name="newsletter" method="POST" action="/?sent=1" data-netlify="true">
        <input type="hidden" name="form-name" value="newsletter">
        <label class="visually-hidden" for="nl-email">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="Your email address" required autocomplete="email">
        <button type="submit" class="btn btn--gold">Subscribe</button>
      </form>
    </div>
  </div>
</section>'''

# ============================== INDEX ==============================
index_body = f'''
<section class="hero">
  <video autoplay muted loop playsinline webkit-playsinline preload="auto" disablepictureinpicture controlslist="nodownload nofullscreen noplaybackrate" disableremoteplayback aria-hidden="true" tabindex="-1">
    <source src="assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="container">
    <div class="hero-content">
      <p class="scripture">&ldquo;&hellip;Be in health, even as your soul prospers.&rdquo; &mdash; 3 John 1:2</p>
      <h1>Fuel Your Body.<br><em>Feed Your Soul.</em></h1>
      <p class="lead">Fresh, cold-pressed juices and wellness shots handcrafted in small batches in Hagerstown, Maryland &mdash; real fruits and vegetables, no added sugar, no preservatives. Ever.</p>
      <div class="hero-ctas">
        <a class="btn btn--gold" href="shop.html">Shop Juices</a>
        <a class="btn btn--outline-light" href="cleanse.html">Start a Cleanse</a>
      </div>
    </div>
  </div>
</section>

<section class="trust-strip" aria-label="Why Soul Fuel Juice">
  <div class="container trust-grid">
    <div class="trust-item">{ICONS["drop"]}<span>100% Cold-Pressed, Never Heated</span></div>
    <div class="trust-item">{ICONS["leaf"]}<span>No Added Sugar or Preservatives</span></div>
    <div class="trust-item">{ICONS["heart"]}<span>Handcrafted in Small Batches</span></div>
    <div class="trust-item">{ICONS["sun"]}<span>Faith-Centered Wellness</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Flavors</span>
      <h2>Signature Cold-Pressed Juices</h2>
      <p>Every bottle is pressed fresh with real produce and a purpose &mdash; nourishment for the body, strength for the soul.</p>
    </div>
    <div class="grid grid--3" data-product-grid="juice" data-products="healing-greens,carrot-glow,beet-bless"></div>
    <p class="text-center mt-lg reveal"><a class="btn btn--outline" href="shop.html">View All Juices &amp; Shots</a></p>
  </div>
</section>

<section class="section section--forest">
  <div class="container split">
    <div class="split-media reveal"><img src="assets/img/styled-greens-moss.jpg?v=2" alt="Healing Greens cold-pressed juice bottle in a natural setting" loading="lazy" width="1400" height="1244"></div>
    <div class="reveal">
      <span class="eyebrow">Made with purpose</span>
      <h2>More Than Juice &mdash; It&rsquo;s a Ministry of Wellness</h2>
      <p class="muted">Soul Fuel Juice is a faith-inspired wellness brand dedicated to nourishing the body while encouraging the soul. Every bottle is made with love, prayer, and premium ingredients.</p>
      <div class="pillars">
        <div class="pillar">{ICONS["drop"]}<div><h3>100% Cold-Pressed Juice</h3><p>Never heated. Never pasteurized. All natural, no additives.</p></div></div>
        <div class="pillar">{ICONS["leaf"]}<div><h3>Fresh, Pure, Handcrafted</h3><p>Made in small batches for maximum freshness and nutrition.</p></div></div>
        <div class="pillar">{ICONS["heart"]}<div><h3>Nourishment for the Body, Strength for the Soul</h3><p>Every bottle is made with love and purpose &mdash; and a verse to carry with you.</p></div></div>
      </div>
      <a class="btn btn--gold" style="margin-top:28px" href="about.html">Our Story</a>
    </div>
  </div>
</section>

<section class="section section--cream2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Feel lighter. Feel renewed.</span>
      <h2>The Soul Slim Reset</h2>
      <p>A simple, faith-centered detox to reduce bloating, boost energy, and rebuild discipline &mdash; in just 3 or 7 days.</p>
    </div>
    <div class="price-cards">
      <div class="price-card featured reveal">
        <span class="badge">Most Popular</span>
        <h3>3-Day Soul Slim Line Reset</h3>
        <div class="amount">$49</div>
        <ul class="check-list">
          <li>6 fresh Soul Slim Line juices (2 per day)</li>
          <li>Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice</li>
          <li>Soul Slim Reset Guide &amp; simple meal guide</li>
          <li>Soul Slim Discipline Tracker</li>
        </ul>
        <a class="btn btn--forest" href="cleanse.html">Start Your Reset</a>
      </div>
      <div class="price-card reveal">
        <h3>7-Day Soul Slim Line Transformation</h3>
        <div class="amount">$99</div>
        <ul class="check-list">
          <li>4 fresh Soul Slim Line juices</li>
          <li>Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice</li>
          <li>The 7-Day Faith &amp; Fit Reset eBook</li>
          <li>Printable Discipline Tracker</li>
          <li>Daily faith-centered encouragement</li>
          <li>The full-body reset experience</li>
        </ul>
        <a class="btn btn--outline" href="cleanse.html">Go Premium</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Small but mighty</span>
      <h2>Wellness Shots</h2>
      <p>Two ounces of concentrated goodness &mdash; immunity, digestion, energy, and glow.</p>
    </div>
    <div class="grid grid--3" data-product-grid="shot" data-products="citrus-defense,fiery-ginger,golden-root-tonic"></div>
    <p class="text-center mt-lg reveal"><a class="btn btn--outline" href="wellness-shots.html">Explore All Shots</a></p>
  </div>
</section>

<section class="section section--cream2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Loved by our community</span>
      <h2>What Customers Are Saying</h2>
    </div>
    <div class="grid grid--3">
      <div class="testimonial reveal">{STAR5}<blockquote>&ldquo;The Healing Greens juice has become part of my morning routine. I feel more energized and the scripture on every bottle blesses me every time.&rdquo;</blockquote><cite>Danielle M. <small>Hagerstown, MD</small></cite></div>
      <div class="testimonial reveal">{STAR5}<blockquote>&ldquo;I did the 3-Day Soul Slim Reset and felt lighter, clearer, and more disciplined. The devotional made it so much more than a detox.&rdquo;</blockquote><cite>Marcus T. <small>Frederick, MD</small></cite></div>
      <div class="testimonial reveal">{STAR5}<blockquote>&ldquo;Fresh, delicious, and made with so much love. The Fiery Ginger shot is my go-to before every workout.&rdquo;</blockquote><cite>Alicia R. <small>Baltimore, MD</small></cite></div>
    </div>
    <p class="text-center mt-lg reveal"><a class="btn btn--outline" href="testimonials.html">Read More Reviews</a></p>
  </div>
</section>
''' + NEWSLETTER

index_jsonld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Soul Fuel Juice LLC",
  "slogan": "Fuel Your Body. Feed Your Soul.",
  "description": "Faith-inspired wellness brand offering fresh cold-pressed juices, wellness shots, and detox programs with no added sugar or preservatives.",
  "telephone": "+1-301-892-6707",
  "email": "soulfueljuice@gmail.com",
  "url": "https://soulfueljuice.com",
  "address": {"@type": "PostalAddress", "addressLocality": "Hagerstown", "addressRegion": "MD", "addressCountry": "US"},
  "areaServed": ["Hagerstown MD", "Frederick MD", "Gaithersburg MD", "Baltimore MD", "Washington DC", "United States"],
  "sameAs": ["https://instagram.com/soulfueljuice_", "https://www.tiktok.com/@soulfueljuice"]
}
</script>
<script>
// Keep the hero video looping continuously with no play button.
document.addEventListener("DOMContentLoaded", function () {
  var v = document.querySelector(".hero video");
  if (!v) return;
  v.muted = true; v.defaultMuted = true; v.loop = true; v.autoplay = true;
  v.controls = false; v.disablePictureInPicture = true;
  v.setAttribute("autoplay", "");
  v.setAttribute("muted", "");
  v.setAttribute("loop", "");
  v.setAttribute("playsinline", "");
  v.setAttribute("webkit-playsinline", "");
  v.setAttribute("preload", "auto");
  v.setAttribute("disablepictureinpicture", "");
  v.setAttribute("controlslist", "nodownload nofullscreen noplaybackrate");
  v.setAttribute("disableremoteplayback", "");
  v.removeAttribute("controls");
  var keepPlaying = function () {
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
  };
  keepPlaying();
  v.addEventListener("pause", keepPlaying);
  v.addEventListener("ended", keepPlaying);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) keepPlaying();
  });
  var kick = function () {
    keepPlaying();
    ["pointerdown", "keydown", "scroll", "touchstart", "mousemove"].forEach(function (ev) {
      window.removeEventListener(ev, kick);
    });
  };
  ["pointerdown", "keydown", "scroll", "touchstart", "mousemove"].forEach(function (ev) {
    window.addEventListener(ev, kick, { passive: true });
  });
});
</script>'''

page("index.html",
     "Soul Fuel Juice | Cold-Pressed Juice & Wellness — Hagerstown, MD",
     "Fresh cold-pressed juices, wellness shots, and faith-centered detox programs made in Hagerstown, Maryland. No added sugar, no preservatives. Local pickup & nationwide shipping.",
     index_body, index_jsonld)

# ============================== SHOP ==============================
shop_body = '''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Pure. Fresh. Purposeful.</span>
    <h1>Shop Soul Fuel Juice</h1>
    <p>Cold-pressed juices, wellness shots, and cleanse bundles &mdash; made fresh in small batches. Order 24&ndash;48 hours ahead for pickup or shipping.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="filter-tabs" role="tablist" aria-label="Filter products">
      <button type="button" class="active" data-filter="all">All Products</button>
      <button type="button" data-filter="juice">Juices</button>
      <button type="button" data-filter="shot">Wellness Shots</button>
      <button type="button" data-filter="bundle">Bundles &amp; Cleanses</button>
    </div>
    <div class="grid grid--3" data-product-grid="all"></div>
    <div class="notice-band mt-lg">
      <strong>Sizes &amp; pricing:</strong> single bottles &mdash; 8&nbsp;oz $9 · 12&nbsp;oz $12 · 16&nbsp;oz $15 · 20&nbsp;oz $18.
      $18 flat-rate shipping nationwide, packed with care and shipped fresh. Pickup available in Hagerstown, MD.
    </div>
  </div>
</section>
''' + NEWSLETTER

page("shop.html",
     "Shop Cold-Pressed Juice, Wellness Shots & Cleanses | Soul Fuel Juice",
     "Shop fresh cold-pressed juice online: Healing Greens, Carrot Glow, Beet & Bless, wellness shots, and juice cleanse bundles. Maryland pickup & nationwide shipping.",
     shop_body)

# ============================== CLEANSE ==============================
cleanse_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Reset your body in 3 days</span>
    <h1>Juice Cleanse &amp; Detox</h1>
    <p>Simple, faith-centered detox programs to reduce bloating, boost energy, and rebuild discipline. Feel lighter. Feel refreshed. Feel renewed.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">The Soul Slim line</span>
      <h2>Choose Your Reset</h2>
    </div>
    <div class="price-cards">
      <div class="price-card featured reveal" data-product="soul-slim-3">
        <span class="badge">Most Popular</span>
        <h3>3-Day Soul Slim Line Reset</h3>
        <div class="amount">$49</div>
        <ul class="check-list">
          <li>6 fresh Soul Slim Line juices (2 juices per day)</li>
          <li>Includes Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice</li>
          <li>Soul Slim Discipline Tracker</li>
          <li>Simple Meal Guide</li>
        </ul>
        <button type="button" class="btn btn--forest" data-add="soul-slim-3">Add to Cart &mdash; $49</button>
      </div>
      <div class="price-card reveal" data-product="soul-slim-7">
        <h3>7-Day Soul Slim Line Transformation</h3>
        <div class="amount">$99</div>
        <ul class="check-list">
          <li>4 fresh Soul Slim Line juices</li>
          <li>Includes Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice</li>
          <li>The 7-Day Faith &amp; Fit Reset eBook</li>
          <li>Printable Discipline Tracker</li>
          <li>Daily scripture &amp; encouragement</li>
          <li>The complete transformation experience</li>
        </ul>
        <button type="button" class="btn btn--outline" data-add="soul-slim-7">Add to Cart &mdash; $99</button>
      </div>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Your daily reset flow</span>
      <h2>How the Reset Works</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Morning</h3><p>Apple Cider Glow Drink &mdash; boost metabolism and support digestion to start your day strong.</p></div>
      <div class="step reveal"><h3>Afternoon</h3><p>Holy Hydration Detox &mdash; reduce bloating and flush toxins while you stay energized.</p></div>
      <div class="step reveal"><h3>Evening</h3><p>A light, healthy meal &mdash; salad, grilled protein, and vegetables. Simple, satisfying, and clean.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Soul Slim flavors</span>
      <h2>What&rsquo;s in the Bottles</h2>
      <ul class="check-list">
        <li><strong>Holy Hydration Detox</strong> &mdash; Cucumber, Lemon, Ginger, Mint</li>
        <li><strong>Belly Burner Pineapple Cleanse</strong> &mdash; Pineapple, Cucumber, Ginger, Lime</li>
        <li><strong>Apple Cider Glow Drink</strong> &mdash; Raw Honey, Lemon, Cinnamon, Warm Water</li>
        <li><strong>Green Fat Flush Juice</strong> &mdash; Spinach, Green Apple, Cucumber, Ginger</li>
      </ul>
      <h3 style="margin-top:26px">Benefits you can feel</h3>
      <div class="benefit-chips">
        <span>Reduce bloating</span><span>Support healthy weight loss</span><span>Boost metabolism</span><span>Improve digestion</span><span>Increase natural energy</span>
      </div>
    </div>
    <div class="split-media reveal"><img src="assets/img/soul-slim-line.jpg?v=3" alt="Soul Slim Line bottles: Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice" loading="lazy" width="800" height="680"></div>
  </div>
</section>

<section class="section section--cream2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Go deeper</span>
      <h2>Detox Challenge Packages</h2>
      <p>The 3-Day Detox Challenge includes 9 regular juices from Healing Greens, Carrot Glow, Beet &amp; Bless, Golden Glow, King&rsquo;s/Queen&rsquo;s Power, and Island Glow. The 7-Day option adds the devotional reset experience.</p>
    </div>
    <div class="grid grid--2" data-product-grid="bundle" data-products="detox-3day,detox-7day"></div>
  </div>
</section>

<section class="section" id="devotional">
  <div class="container">
    <div class="split">
      <a class="split-media reveal" href="devotional.html" aria-label="Learn about The 7-Day Faith &amp; Fit Reset">
        <img src="assets/img/faith-fit-reset.jpg?v=2" alt="The 7-Day Faith &amp; Fit Reset devotional by Josephine Sanso" loading="lazy" width="800" height="680">
      </a>
      <div class="reveal">
        <span class="eyebrow">Included with the 7-day transformation</span>
        <h2>The 7-Day Faith &amp; Fit Reset</h2>
        <p class="muted">The full eBook and printable Discipline Tracker are included with the 7-Day Soul Slim Line Transformation, giving you juice, structure, scripture, and accountability in one complete reset.</p>
        <a class="btn btn--gold" href="devotional.html">
          See What&rsquo;s Included
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </a>
        <p class="muted" style="font-size:.85rem;margin-top:14px">No need to buy this separately &mdash; it comes bundled with the 7-day Soul Slim Line plan.</p>
      </div>
    </div>
  </div>
</section>
''' + NEWSLETTER

page("cleanse.html",
     "Juice Cleanse & Detox Programs | Soul Fuel Juice — Maryland",
     "Faith-centered juice cleanse and detox programs: the 3-Day Soul Slim Reset ($49) and 7-Day Soul Slim Transformation ($99). Reduce bloating, boost energy, rebuild discipline.",
     cleanse_body)

# ============================== WELLNESS SHOTS ==============================
shots_body = '''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Small but mighty</span>
    <h1>Wellness Shots</h1>
    <p>Concentrated 2 oz shots of cold-pressed goodness &mdash; built for immunity, digestion, energy, and recovery.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3" data-product-grid="shot"></div>
    <div class="notice-band mt-lg">
      <strong>Pro tip:</strong> add a shot (or three) to any juice order &mdash; they&rsquo;re the perfect daily ritual. Take first thing in the morning or before a workout.
    </div>
  </div>
</section>
''' + NEWSLETTER

page("wellness-shots.html",
     "Wellness Shots — Ginger, Turmeric & Immunity | Soul Fuel Juice",
     "Cold-pressed 2 oz wellness shots: Fiery Ginger, Citrus Defense, Immune Shield, Golden Root Tonic, Pineapple Mint Soother, and Spiced Beet Elixir.",
     shots_body)

# ============================== BENEFITS ==============================
benefits_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Nourish your body</span>
    <h1>The Benefits of Cold-Pressed Juice</h1>
    <p>Why cold-pressed, why fresh, and what every ingredient does for you.</p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split-media reveal"><img src="assets/img/juice-trio.png?v=2" alt="Carrot Glow, Beet & Bless, and Healing Greens cold-pressed juices" loading="lazy" width="1254" height="1254"></div>
    <div class="reveal">
      <span class="eyebrow">Never heated, never rushed</span>
      <h2>Why Cold-Pressed Matters</h2>
      <p>Traditional juicing methods generate heat that destroys delicate vitamins, minerals, and enzymes. Cold-pressing slowly extracts juice with thousands of pounds of pressure &mdash; <strong>no heat, no oxidation, no compromise</strong> &mdash; so more of the good stuff makes it into your bottle.</p>
      <div class="pillars">
        <div class="pillar">{ICONS["drop"]}<div><h3>More Nutrients Per Sip</h3><p>Up to 3&ndash;5x more vitamins and enzymes retained versus heat-processed juice.</p></div></div>
        <div class="pillar">{ICONS["leaf"]}<div><h3>Nothing Artificial</h3><p>No added sugar, no preservatives, no concentrates &mdash; just pressed produce.</p></div></div>
        <div class="pillar">{ICONS["sun"]}<div><h3>Made Fresh Daily</h3><p>Small batches, consumed within 3&ndash;5 days for peak potency.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Juice by juice</span>
      <h2>What Each Flavor Does For You</h2>
    </div>
    <div class="grid grid--2">
      <div class="card reveal"><div class="card-body"><span class="card-tag">Healing Greens</span><h3>The Daily Detoxifier</h3><p class="ingredients">Kale, Apple, Cucumber, Spinach, Lemon, Celery, Ginger</p><p class="muted">Detoxifies the body, supports digestion and gut health, boosts immunity, supports hydration and skin &amp; eye health. Ginger soothes the digestive system and reduces inflammation.</p></div></div>
      <div class="card reveal"><div class="card-body"><span class="card-tag">Golden Glow</span><h3>The Sunshine Bottle</h3><p class="ingredients">Mango, Pineapple, Carrot, Lemon, Ginger</p><p class="muted">Rich in Vitamins A &amp; C, boosts immunity and energy, supports skin &amp; eye health, anti-inflammatory properties, and digestive health.</p></div></div>
      <div class="card reveal"><div class="card-body"><span class="card-tag">Carrot Glow</span><h3>The Brain &amp; Beauty Blend</h3><p class="ingredients">Pineapple, Orange, Carrot, Turmeric, Ginger</p><p class="muted">Supports brain and eye health, boosts immunity and energy, anti-inflammatory properties, improves circulation, and promotes glowing skin.</p></div></div>
      <div class="card reveal"><div class="card-body"><span class="card-tag">King&rsquo;s/Queen&rsquo;s Power</span><h3>The Empowerment Elixir</h3><p class="ingredients">Beetroot, Watermelon, Ginger, Pineapple, Lemon, Maca Root Powder</p><p class="muted">Supports hormonal balance, boosts stamina and endurance, improves fertility &amp; reproductive health, enhances skin health and glow, promotes iron &amp; blood health, reduces inflammation and stress.</p></div></div>
      <div class="card reveal"><div class="card-body"><span class="card-tag">Beet &amp; Bless</span><h3>The Circulation Champion</h3><p class="ingredients">Beets, Apple, Ginger, Carrot, Hint of Lemon</p><p class="muted">Great for blood circulation, digestion support, liver health, and endurance.</p></div></div>
      <div class="card reveal"><div class="card-body"><span class="card-tag">Island Glow</span><h3>The Hydration Hero</h3><p class="ingredients">Watermelon, Cucumber, Pineapple, Lime, Ginger</p><p class="muted">Hydration support, skin glow &amp; collagen boost, digestion aid, anti-inflammatory properties, immunity boost, and refreshing energy.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="notice-band reveal">
      *These statements have not been evaluated by the Food and Drug Administration. Our products are not intended to diagnose, treat, cure, or prevent any disease. Always consult your healthcare provider before starting any new wellness program.
    </div>
    <p class="text-center mt-lg reveal"><a class="btn btn--forest" href="shop.html">Shop the Flavors</a></p>
  </div>
</section>
''' + NEWSLETTER

page("benefits.html",
     "Health Benefits of Cold-Pressed Juice | Soul Fuel Juice",
     "Learn why cold-pressed juice retains more nutrients, and what every Soul Fuel Juice flavor does for your body — from Healing Greens to King's/Queen's Power.",
     benefits_body)

# ============================== ABOUT ==============================
about_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Our story</span>
    <h1>Nourishing the Body, Encouraging the Soul</h1>
    <p>&ldquo;&hellip;Be in health, even as your soul prospers.&rdquo; &mdash; 3 John 1:2</p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split-media reveal"><img src="assets/img/styled-beet-bike.jpg?v=2" alt="Beet & Bless juice on a vintage bicycle with flowers" loading="lazy" width="1400" height="1253"></div>
    <div class="reveal">
      <span class="eyebrow">Faith-inspired wellness</span>
      <h2>Why We Press</h2>
      <p>Soul Fuel Juice is a faith-inspired wellness brand born in Hagerstown, Maryland, and dedicated to one simple mission: <strong>helping people embrace healthier lifestyles through nutrition, encouragement, and faith.</strong></p>
      <p>We handcraft fresh, cold-pressed juices, wellness shots, and detox programs using real fruits and vegetables &mdash; never with added sugar or preservatives. Every bottle carries a scripture, because we believe true wellness feeds the body <em>and</em> the soul.</p>
      <p>When you order from us, you&rsquo;re not just buying juice. You&rsquo;re supporting a small business, joining a wellness community, and taking a step toward the abundant health God desires for you.</p>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">What we stand for</span>
      <h2>Our Values</h2>
    </div>
    <div class="grid grid--3">
      <div class="step reveal"><h3>Faith First</h3><p>Every batch is made with love, prayer, and purpose. Scripture is on every label because encouragement belongs in every bottle.</p></div>
      <div class="step reveal"><h3>Real Ingredients</h3><p>Premium fruits and vegetables, cold-pressed in small batches. No added sugar. No preservatives. No shortcuts.</p></div>
      <div class="step reveal"><h3>Community Wellness</h3><p>From Hagerstown to the whole DMV and beyond &mdash; we exist to help our neighbors live healthier, more hopeful lives.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Who we serve</span>
      <h2>Made For Real Life</h2>
      <p>Health-conscious individuals, busy professionals, families, fitness enthusiasts &mdash; anyone seeking natural wellness and a healthier way to drink.</p>
    </div>
    <p class="text-center reveal"><a class="btn btn--forest" href="shop.html">Shop Our Juices</a>&nbsp;&nbsp;<a class="btn btn--outline" href="contact.html">Say Hello</a></p>
  </div>
</section>
''' + NEWSLETTER

page("about.html",
     "About Soul Fuel Juice | Faith-Inspired Cold-Pressed Juice — Hagerstown, MD",
     "Soul Fuel Juice is a faith-inspired wellness brand in Hagerstown, Maryland, handcrafting cold-pressed juices with real ingredients, scripture on every bottle, and a mission to nourish body and soul.",
     about_body)

# ============================== FAQ ==============================
faqs = [
    ("How fresh is the juice, and how long does it last?",
     "Every juice is cold-pressed in small batches and made fresh daily. Because we use zero preservatives, we recommend keeping your juice refrigerated and enjoying it within 3–5 days."),
    ("How far in advance do I need to order?",
     "Please place orders 24–48 hours before your pickup or shipping date so we can press your juice fresh."),
    ("Where can I get my juice?",
     "Pickup is available in Hagerstown, MD. We also ship nationwide for a $18 flat rate, packed with care and shipped fresh."),
    ("How do I pay?",
     "After you place your order, we confirm your total and you pay via Cash App ($Josiejo87) or Zelle (301-892-6707). Simple and secure."),
    ("Is there really no added sugar?",
     "Correct — nothing but real fruits and vegetables. Any sweetness comes straight from the produce itself. No added sugar, no preservatives, no concentrates."),
    ("What is the Soul Slim Reset?",
     "Our signature faith-centered detox: 2 detox juices per day plus a light, healthy evening meal, guided by the Reset Guide and Discipline Tracker. Choose 3 days ($49) or 7 days ($99)."),
    ("Will I be hungry during a cleanse?",
     "The Soul Slim plans include a light evening meal, so most people feel satisfied while still getting the reset benefits. Hydrate well and listen to your body."),
    ("Can I do a cleanse if I'm pregnant or have a health condition?",
     "Please consult your physician before beginning any cleanse or detox program, especially if you are pregnant, nursing, taking medication, or managing a medical condition."),
    ("Can I mix and match flavors?",
     "Absolutely! The 3-Pack Sampler is fully mix-and-match, and you can leave flavor requests in the order notes on any bundle."),
    ("Do you offer subscriptions or gift cards?",
     "Both are coming soon! Join the newsletter or follow @soulfueljuice_ on Instagram to be the first to know."),
]
faq_items = "\n".join(
    f'<details class="reveal"><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in faqs
)
faq_jsonld_items = ",".join(
    '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q.replace('"', "'"), a.replace('"', "'"))
    for q, a in faqs
)
faq_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Good questions</span>
    <h1>Frequently Asked Questions</h1>
    <p>Everything you need to know about ordering, freshness, shipping, and cleansing.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="accordion">{faq_items}</div>
    <p class="text-center mt-lg reveal">Still have a question? <a href="contact.html">Reach out</a> &mdash; we&rsquo;d love to help.</p>
  </div>
</section>
''' + NEWSLETTER

page("faq.html",
     "FAQ | Soul Fuel Juice — Ordering, Freshness, Shipping & Cleanses",
     "Answers to common questions about Soul Fuel Juice: how fresh our cold-pressed juice is, pickup & shipping, payment, and how the Soul Slim Reset cleanse works.",
     faq_body,
     f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_jsonld_items}]}}</script>')

# ============================== TESTIMONIALS ==============================
testimonials = [
    ("Danielle M.", "Hagerstown, MD", "The Healing Greens juice has become part of my morning routine. I feel more energized and the scripture on every bottle blesses me every time."),
    ("Marcus T.", "Frederick, MD", "I did the 3-Day Soul Slim Reset and felt lighter, clearer, and more disciplined. The devotional made it so much more than a detox."),
    ("Alicia R.", "Baltimore, MD", "Fresh, delicious, and made with so much love. The Fiery Ginger shot is my go-to before every workout."),
    ("Tanya W.", "Gaithersburg, MD", "King's/Queen's Power is everything. You can taste how fresh it is, and I love supporting a faith-led small business."),
    ("James K.", "Washington, DC", "Ordered the 7-Day Detox package for my wife and me. Great communication, fresh juice, and we both felt amazing by day four."),
    ("Renee P.", "Hagerstown, MD", "Beet & Bless got me through marathon training. The name says it all — I truly feel blessed and fueled."),
]
t_cards = "\n".join(
    f'<div class="testimonial reveal">{STAR5}<blockquote>&ldquo;{quote}&rdquo;</blockquote><cite>{name} <small>{loc}</small></cite></div>'
    for name, loc, quote in testimonials
)
testimonials_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Loved by our community</span>
    <h1>Testimonials</h1>
    <p>Real people, real results &mdash; nourished bodies and encouraged souls.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">{t_cards}</div>
  </div>
</section>
<section class="section section--cream2">
  <div class="container" style="max-width:720px">
    <div class="section-head reveal">
      <span class="eyebrow">Share the love</span>
      <h2>Leave a Review</h2>
      <p>Tried our juice? We&rsquo;d be honored to hear how it blessed you.</p>
    </div>
    <div class="form-card reveal">
      <form name="review" method="POST" action="/testimonials.html?sent=1" data-netlify="true">
        <input type="hidden" name="form-name" value="review">
        <div class="form-grid">
          <div class="field"><label for="r-name">Name <span class="req">*</span></label><input id="r-name" name="name" required></div>
          <div class="field"><label for="r-city">City / State</label><input id="r-city" name="city"></div>
          <div class="field field--full"><label for="r-product">What did you try?</label><input id="r-product" name="product" placeholder="e.g. Healing Greens, 3-Day Reset"></div>
          <div class="field field--full"><label for="r-review">Your review <span class="req">*</span></label><textarea id="r-review" name="review" rows="4" required></textarea></div>
        </div>
        <button type="submit" class="btn btn--forest" style="margin-top:18px">Submit Review</button>
      </form>
    </div>
  </div>
</section>
''' + NEWSLETTER

page("testimonials.html",
     "Customer Testimonials & Reviews | Soul Fuel Juice",
     "See what customers across Maryland and DC say about Soul Fuel Juice cold-pressed juices, wellness shots, and the Soul Slim Reset cleanse.",
     testimonials_body)

# ============================== BLOG ==============================
posts = [
    {
        "file": "blog/why-cold-pressed.html",
        "title": "Why Cold-Pressed? 5 Reasons Your Body Will Thank You",
        "desc": "What makes cold-pressed juice different from store-bought juice — and why it matters for nutrition, energy, and gut health.",
        "date": "July 2026", "tag": "Nutrition",
        "img": "../assets/img/juice-trio.jpg",
        "alt": "Three Soul Fuel Juice cold-pressed juices",
        "body": '''
<p>Walk down any grocery aisle and you&rsquo;ll see shelves of &ldquo;juice&rdquo; that spent months in a warehouse. Most of it was heat-pasteurized, reconstituted from concentrate, and sweetened along the way. Cold-pressed juice is a different food entirely. Here&rsquo;s why.</p>
<h2>1. Heat destroys nutrients &mdash; pressure doesn&rsquo;t</h2>
<p>Conventional juicing and pasteurization expose juice to heat, which degrades vitamin C, B vitamins, and living enzymes. A cold press extracts juice slowly using thousands of pounds of pressure and no heat, so far more of those nutrients survive the trip from produce to bottle.</p>
<h2>2. Nothing added means nothing hidden</h2>
<p>Our label is the whole story: fruits, vegetables, roots. No added sugar, no preservatives, no &ldquo;natural flavors.&rdquo; When juice is made fresh and enjoyed within 3&ndash;5 days, it doesn&rsquo;t need anything else.</p>
<h2>3. Your gut gets a head start</h2>
<p>Juicing removes insoluble fiber, which means the vitamins and minerals are absorbed quickly and gently &mdash; a welcome reset when your digestion feels sluggish. Blends with ginger, like our Healing Greens, add an extra layer of digestive comfort.</p>
<h2>4. Real energy, not a sugar spike</h2>
<p>Because cold-pressed blends balance vegetables with fruit, you get steady, natural energy instead of the crash that follows sweetened drinks. Try swapping your afternoon soda for a Carrot Glow for one week &mdash; you&rsquo;ll feel the difference.</p>
<h2>5. It&rsquo;s stewardship, not a trend</h2>
<blockquote>&ldquo;Do you not know that your bodies are temples of the Holy Spirit?&rdquo; &mdash; 1 Corinthians 6:19</blockquote>
<p>We believe caring for your body is an act of faith. Choosing real, nutrient-dense food is one of the simplest daily ways to honor the life you&rsquo;ve been given.</p>
<p><a href="../shop.html">Shop our cold-pressed juices &rarr;</a></p>''',
    },
    {
        "file": "blog/prepare-juice-cleanse.html",
        "title": "How to Prepare for Your First Juice Cleanse (Body & Soul)",
        "desc": "A practical, grace-filled guide to getting ready for a 3-day juice cleanse — what to eat before, what to expect, and how to finish strong.",
        "date": "July 2026", "tag": "Cleanse",
        "img": "../assets/img/soul-slim-line.jpg?v=3",
        "alt": "Soul Slim Line bottles: Holy Hydration Detox, Belly Burner Pineapple Cleanse, Apple Cider Glow Drink, and Green Fat Flush Juice",
        "body": '''
<p>A cleanse works best when you ease into it. If you&rsquo;ve booked a 3-Day Soul Slim Reset (or you&rsquo;re thinking about it), here&rsquo;s how to set yourself up for success &mdash; physically and spiritually.</p>
<h2>Three days before: lighten the load</h2>
<p>Start scaling back caffeine, alcohol, fried food, and refined sugar. Add an extra glass of water to each day. This softens the transition so day one of your cleanse feels refreshing instead of jarring.</p>
<h2>The day before: eat clean and simple</h2>
<p>Think salads, grilled protein, fruit, and plenty of water &mdash; basically the same light evening meal you&rsquo;ll enjoy during the reset. Set your juices in the fridge in daily order so the plan runs itself.</p>
<h2>During the cleanse: follow the flow</h2>
<p>Morning: Apple Cider Glow Drink to wake up your metabolism. Afternoon: Holy Hydration Detox to flush and refresh. Evening: a light, healthy meal. Use the Discipline Tracker to check off each day &mdash; small wins build momentum.</p>
<h2>Expect a dip &mdash; and a breakthrough</h2>
<p>Day two can bring a headache or low energy as your body adjusts. That&rsquo;s normal. Rest, hydrate, and lean on the devotional. Most people wake up on day three feeling lighter, clearer, and genuinely renewed.</p>
<blockquote>&ldquo;Faith without works is dead.&rdquo; &mdash; James 2:17. Discipline is a spiritual practice &mdash; your body is simply where it shows up first.</blockquote>
<h2>After: re-enter gently</h2>
<p>Break your cleanse with fruit or a smoothie, then add solid meals back over a day or two. Many customers keep one juice a day as a habit &mdash; the reset is the start, not the finish line.</p>
<p><a href="../cleanse.html">Start your Soul Slim Reset &rarr;</a></p>''',
    },
    {
        "file": "blog/faith-and-wellness.html",
        "title": "Faith & Wellness: What 3 John 1:2 Teaches Us About Health",
        "desc": "Why Soul Fuel Juice puts scripture on every bottle — and how faith and physical wellness strengthen each other.",
        "date": "June 2026", "tag": "Faith",
        "img": "../assets/img/styled-greens-moss.jpg",
        "alt": "Healing Greens juice in a peaceful natural setting",
        "body": '''
<blockquote>&ldquo;Beloved, I pray that you may prosper in all things and be in health, just as your soul prospers.&rdquo; &mdash; 3 John 1:2</blockquote>
<p>This single verse is printed on every bottle we press. It&rsquo;s more than a tagline &mdash; it&rsquo;s the reason Soul Fuel Juice exists.</p>
<h2>Health is part of the blessing</h2>
<p>John&rsquo;s prayer links physical health with a prospering soul. Scripture doesn&rsquo;t treat the body as an afterthought; it calls it a temple. Caring for it &mdash; with real food, movement, and rest &mdash; is a form of worship and stewardship.</p>
<h2>Discipline is discipleship</h2>
<p>Nobody drifts into health, just like nobody drifts into spiritual maturity. Both take small, repeated choices: the morning prayer, the daily walk, the vegetables you actually eat. That&rsquo;s why our cleanses come with a devotional and a discipline tracker &mdash; the habits reinforce each other.</p>
<h2>Encouragement is nutrition too</h2>
<p>We&rsquo;ve watched customers start with a juice and end up with a renewed routine &mdash; not because juice is magic, but because one act of self-care gives you hope for the next one. Encouragement compounds. That&rsquo;s the &ldquo;soul&rdquo; half of Soul Fuel.</p>
<h2>Start where you are</h2>
<p>You don&rsquo;t need a perfect diet or a perfect prayer life to begin. Swap one drink a day for something that nourishes you. Read one verse with it. Small and faithful beats big and burned-out &mdash; every time.</p>
<p><a href="../about.html">Read our story &rarr;</a></p>''',
    },
]

# Blog post pages (paths are nested → adjust asset/link prefixes)
for p in posts:
    body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{p["tag"]}</span>
    <h1 style="font-size:clamp(1.9rem,4vw,2.8rem)">{p["title"]}</h1>
    <p>{p["date"]} · Soul Fuel Juice</p>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <img src="{p["img"]}" alt="{p["alt"]}" loading="lazy">
    {p["body"]}
  </div>
</section>'''
    html = head(p["title"] + " | Soul Fuel Juice Blog", p["desc"], p["file"]) + header("blog.html") + body + footer()
    # fix relative paths for nested blog pages
    html = (html
            .replace('href="css/style.css"', 'href="../css/style.css"')
            .replace('href="assets/img/logo.svg"', 'href="../assets/img/logo.svg"')
            .replace('src="js/', 'src="../js/'))
    # nav/footer links
    for href, _ in NAV_ITEMS:
        html = html.replace(f'href="{href}"', f'href="../{href}"')
    for extra in ["testimonials.html", "faq.html", "shipping.html", "privacy.html", "terms.html", "wellness-shots.html", "cleanse.html", "benefits.html", "shop.html"]:
        html = html.replace(f'href="{extra}"', f'href="../{extra}"')
    html = html.replace('href="../../', 'href="../')  # guard double-ups
    with open(os.path.join(ROOT, p["file"]), "w") as f:
        f.write(html)
    print("wrote", p["file"])

post_cards = "\n".join(f'''
<article class="card reveal">
  <a href="{p["file"]}" aria-label="Read: {p["title"]}"><div class="card-media"><img src="{p["img"].replace("../", "")}" alt="{p["alt"]}" loading="lazy"></div></a>
  <div class="card-body">
    <span class="post-meta">{p["tag"]} · {p["date"]}</span>
    <h3><a href="{p["file"]}">{p["title"]}</a></h3>
    <p class="muted" style="font-size:.93rem">{p["desc"]}</p>
    <a href="{p["file"]}" style="font-weight:700;font-size:.9rem">Read Article &rarr;</a>
  </div>
</article>''' for p in posts)

blog_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">The Soul Fuel journal</span>
    <h1>Wellness, Faith &amp; Fresh Juice</h1>
    <p>Practical nutrition tips, cleanse guidance, and encouragement for the journey.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">{post_cards}</div>
  </div>
</section>
''' + NEWSLETTER

page("blog.html",
     "Blog — Wellness, Faith & Cold-Pressed Juice | Soul Fuel Juice",
     "The Soul Fuel Juice journal: cold-pressed nutrition explained, juice cleanse preparation guides, and faith-centered wellness encouragement.",
     blog_body)

# ============================== CONTACT ==============================
contact_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">We&rsquo;d love to hear from you</span>
    <h1>Contact Us</h1>
    <p>Questions, custom orders, events, or prayer requests &mdash; reach out anytime.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="split" style="align-items:start">
      <div class="form-card reveal">
        <h2 style="font-size:1.5rem">Send a Message</h2>
        <form name="contact" method="POST" action="/.netlify/functions/contact-to-sheets" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="contact">
          <p class="visually-hidden"><label>Don&rsquo;t fill this out: <input name="bot-field"></label></p>
          <div class="form-grid">
            <div class="field"><label for="c-name">Name <span class="req">*</span></label><input id="c-name" name="name" required autocomplete="name"></div>
            <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field field--full"><label for="c-email">Email <span class="req">*</span></label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
            <div class="field field--full"><label for="c-subject">Subject</label>
              <select id="c-subject" name="subject">
                <option>General question</option>
                <option>Place / modify an order</option>
                <option>Juice cleanse guidance</option>
                <option>Wholesale or event inquiry</option>
                <option>Something else</option>
              </select></div>
            <div class="field field--full"><label for="c-message">Message <span class="req">*</span></label><textarea id="c-message" name="message" rows="5" required></textarea></div>
          </div>
          <button type="submit" class="btn btn--forest" style="margin-top:18px;width:100%">Send Message</button>
        </form>
      </div>
      <div class="reveal">
        <div class="contact-info">
          <div class="contact-line">{ICONS["phone"]}<div><h3 style="font-size:1.05rem;margin-bottom:2px">Call or Text</h3><p style="margin:0"><a href="tel:+13018926707">301-892-6707</a></p></div></div>
          <div class="contact-line">{ICONS["mail"]}<div><h3 style="font-size:1.05rem;margin-bottom:2px">Email</h3><p style="margin:0"><a href="mailto:soulfueljuice@gmail.com">soulfueljuice@gmail.com</a></p></div></div>
          <div class="contact-line">{ICONS["pin"]}<div><h3 style="font-size:1.05rem;margin-bottom:2px">Based In</h3><p style="margin:0">Hagerstown, Maryland<br><span class="muted" style="font-size:.88rem">Pickup in Hagerstown, MD &amp; nationwide shipping</span></p></div></div>
          <div class="contact-line">{ICONS["heart"]}<div><h3 style="font-size:1.05rem;margin-bottom:2px">Follow Along</h3><p style="margin:0"><a href="https://instagram.com/soulfueljuice_" rel="noopener" target="_blank">Instagram</a> · <a href="https://www.tiktok.com/@soulfueljuice" rel="noopener" target="_blank">TikTok</a> · Facebook: Soul Fuel Juice</p></div></div>
        </div>
        <div class="map-embed mt-lg">
          <iframe title="Map of Hagerstown, Maryland" src="https://maps.google.com/maps?q=Hagerstown%2C+MD&amp;z=11&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
''' + NEWSLETTER

page("contact.html",
     "Contact Soul Fuel Juice | Hagerstown, MD Cold-Pressed Juice",
     "Contact Soul Fuel Juice in Hagerstown, Maryland: call or text 301-892-6707, email soulfueljuice@gmail.com, or send a message for orders, cleanses, and events.",
     contact_body)

# ============================== SHIPPING ==============================
shipping_body = f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Fresh to your door</span>
    <h1>Shipping &amp; Delivery</h1>
    <p>Packed with care, delivered fresh &mdash; locally and nationwide.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <div class="step reveal"><h3>Local Delivery &amp; Pickup</h3><p>Local delivery in Hagerstown, MD &amp; surrounding areas &mdash; $10 delivery fee, <strong>free on orders $50+</strong>. Or arrange a free pickup time when we confirm your order.</p></div>
      <div class="step reveal"><h3>Nationwide Shipping</h3><p>$18 flat-rate shipping on all orders. Every box is packed with care and shipped fresh with cold packaging. Shipping is not included in product prices.</p></div>
      <div class="step reveal"><h3>Order Timing</h3><p>Please order 24&ndash;48 hours before your preferred pickup or ship date. Everything is pressed fresh to order &mdash; no warehouse stock, ever.</p></div>
    </div>
    <div class="legal-wrap mt-lg">
      <h2>Keeping your juice fresh</h2>
      <p>Refrigerate your juice as soon as it arrives and enjoy within 3&ndash;5 days. Cold-pressed juice is a fresh product with no preservatives &mdash; a little shake before drinking is natural and normal.</p>
      <h2>Payment</h2>
      <p>Orders are confirmed by text or email, then paid via Cash App (<strong>$Josiejo87</strong>) or Zelle (<strong>301-892-6707</strong>). Your order is scheduled for pressing once payment is received.</p>
      <h2>Questions about your order?</h2>
      <p>Call or text <a href="tel:+13018926707">301-892-6707</a> or email <a href="mailto:soulfueljuice@gmail.com">soulfueljuice@gmail.com</a> and we&rsquo;ll make it right.</p>
    </div>
  </div>
</section>
''' + NEWSLETTER

page("shipping.html",
     "Shipping & Delivery | Soul Fuel Juice",
     "Soul Fuel Juice pickup & shipping details: local pickup in Hagerstown, MD, $18 flat-rate nationwide shipping, and 24–48 hour fresh-press order timing.",
     shipping_body)

# ============================== PRIVACY ==============================
privacy_body = '''
<section class="page-hero">
  <div class="container"><h1>Privacy Policy</h1><p>Last updated: July 2026</p></div>
</section>
<section class="section">
  <div class="container legal-wrap">
    <p>Soul Fuel Juice LLC (&ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) respects your privacy. This policy explains what information we collect through soulfueljuice.com and how we use it.</p>
    <h2>Information we collect</h2>
    <p>When you place an order, contact us, leave a review, or subscribe to our newsletter, we collect the information you provide: your name, phone number, email address, shipping address, and order details. We do not collect or store payment card information on this website &mdash; payments are completed through Cash App or Zelle.</p>
    <h2>How we use your information</h2>
    <p>We use your information to fulfill and deliver orders, respond to your messages, send the newsletter you subscribed to, and improve our products and website. We do not sell, rent, or trade your personal information to third parties.</p>
    <h2>Cookies &amp; local storage</h2>
    <p>This site uses your browser&rsquo;s local storage to remember the contents of your shopping cart. We may use basic analytics to understand site traffic; these tools do not identify you personally.</p>
    <h2>Email communications</h2>
    <p>You may unsubscribe from our newsletter at any time using the link in any email or by contacting us directly.</p>
    <h2>Data retention &amp; security</h2>
    <p>We retain order information only as long as needed for business and legal purposes and take reasonable measures to protect it.</p>
    <h2>Children&rsquo;s privacy</h2>
    <p>Our website is not directed to children under 13, and we do not knowingly collect their information.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:soulfueljuice@gmail.com">soulfueljuice@gmail.com</a> or call 301-892-6707.</p>
  </div>
</section>'''

page("privacy.html",
     "Privacy Policy | Soul Fuel Juice",
     "How Soul Fuel Juice LLC collects, uses, and protects your personal information.",
     privacy_body)

# ============================== TERMS ==============================
terms_body = '''
<section class="page-hero">
  <div class="container"><h1>Terms &amp; Conditions</h1><p>Last updated: July 2026</p></div>
</section>
<section class="section">
  <div class="container legal-wrap">
    <p>Welcome to Soul Fuel Juice. By using soulfueljuice.com and purchasing our products, you agree to the following terms.</p>
    <h2>Products &amp; freshness</h2>
    <p>All juices and wellness shots are made fresh in small batches with no preservatives. Products must be refrigerated upon receipt and consumed within 3&ndash;5 days. Natural separation and settling are normal.</p>
    <h2>Orders &amp; payment</h2>
    <p>Orders should be placed 24&ndash;48 hours before your preferred pickup or shipping date. Orders are confirmed by text or email and paid via Cash App or Zelle. An order is scheduled for production once payment is received. Prices are subject to change without notice.</p>
    <h2>Delivery &amp; shipping</h2>
    <p>Local pickup is available in Hagerstown, MD. Nationwide shipping is a flat $18 and is not included in product prices. We are not responsible for delays caused by carriers or for product quality issues resulting from packages left unrefrigerated after delivery.</p>
    <h2>Refunds</h2>
    <p>Because our products are perishable and made to order, all sales are final. If something is wrong with your order, contact us within 24 hours of receipt and we will make it right.</p>
    <h2>Health disclaimer</h2>
    <p>Our products and any wellness content on this site are not intended to diagnose, treat, cure, or prevent any disease, and are not a substitute for medical advice. These statements have not been evaluated by the Food and Drug Administration. Consult your physician before beginning any cleanse or detox program, especially if you are pregnant, nursing, taking medication, or have a medical condition.</p>
    <h2>Intellectual property</h2>
    <p>All content on this site &mdash; including the Soul Fuel Juice name, logo, photography, and text &mdash; is the property of Soul Fuel Juice LLC and may not be used without permission.</p>
    <h2>Contact</h2>
    <p>Questions about these terms? Email <a href="mailto:soulfueljuice@gmail.com">soulfueljuice@gmail.com</a>.</p>
  </div>
</section>'''

page("terms.html",
     "Terms & Conditions | Soul Fuel Juice",
     "Terms and conditions for ordering from Soul Fuel Juice LLC: freshness, payment, shipping, refunds, and health disclaimer.",
     terms_body)

print("\nAll pages generated.")
