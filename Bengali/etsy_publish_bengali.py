"""
Etsy v3 API – Publish Bengali cookbook listings to DhanioDigital shop.
Triggered by GitHub Actions workflow; run after exchanging OAuth auth code for tokens.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# ── config ──────────────────────────────────────────────────────────────────
API_KEY      = os.environ["ETSY_API_KEY"]        # keystring (not secret)
ACCESS_TOKEN = os.environ["ETSY_ACCESS_TOKEN"]   # Bearer token

REPO_RAW = "https://raw.githubusercontent.com/dhaniocreators/dhanio-cookbooks/main/Bengali"
BASE     = "https://api.etsy.com/v3/application"

HEADERS = {
    "x-api-key": API_KEY,
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

TAGS = [
    "indian recipe book", "bengali cookbook", "digital cookbook",
    "vegetarian recipes", "pdf recipe book", "authentic recipes",
    "regional cuisine", "indian cooking pdf", "bengali food",
    "instant download", "indian vegetarian", "recipe ebook pdf",
    "traditional recipe",
]

PRICE_INR     = 419.00
BUNDLE_PRICE  = 1259.00
QUANTITY      = 999
TAXONOMY_ID   = 2078   # Books, Movies & Music > Books > Cookbooks, Food & Wine

# ── listings ─────────────────────────────────────────────────────────────────
# slug: (title, description, cover_jpg, preview_jpgs, pdf_file)
BOOKS = {
    "Mochar_Ghonto_FINAL": (
        "Mochar Ghonto - Authentic Bengali Banana Flower Curry | Vegetarian Indian Recipe Book PDF",
        """Discover the authentic Bengali recipe for Mochar Ghonto — a classic, slow-cooked dry curry made with tender banana flowers (mocha), potatoes, and aromatic spices.

This digital cookbook PDF brings you:
✅ Step-by-step, beginner-friendly instructions
✅ Traditional Bengali spice blend guide
✅ Prep tips for cleaning and cooking banana flower
✅ Authentic home-style flavour with no shortcuts
✅ Printable, downloadable format — read anywhere

WHAT'S INSIDE
• Ingredient list with exact measurements
• Detailed method with timing
• Tips for getting the texture just right
• Serving suggestions

PERFECT FOR
Home cooks who want to explore regional Bengali vegetarian cooking beyond the usual dishes.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
    "Labra_FINAL": (
        "Labra - Bengali Mixed Vegetable Curry Recipe | Authentic Regional Vegetarian Cookbook PDF",
        """Labra is a beloved Bengali mixed-vegetable dish cooked with panch phoron (five-spice blend) and served as prasad during festivals and religious occasions.

This digital cookbook PDF brings you:
✅ Traditional recipe with 7+ seasonal vegetables
✅ How to use panch phoron perfectly
✅ Festival-style cooking method
✅ No onion, no garlic — pure sattvic preparation
✅ Printable, downloadable PDF format

WHAT'S INSIDE
• Full ingredient list with quantities
• Step-by-step cooking method
• Seasonal vegetable substitution guide
• Tips for the authentic dry-stir-fry finish

PERFECT FOR
Anyone who loves no-onion-no-garlic Bengali cooking, or wants to explore prasad-style recipes.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
    "Begun_Basanti_FINAL": (
        "Begun Basanti - Bengali Mustard Brinjal Curry | Vegetarian Indian Recipe Ebook PDF",
        """Begun Basanti is a classic Bengali recipe where tender brinjal (eggplant) is cooked in a golden mustard-and-turmeric gravy — simple, pungent, and utterly satisfying.

This digital cookbook PDF brings you:
✅ Traditional mustard paste technique (no shortcuts)
✅ How to pick and prep the right brinjal
✅ Authentic Bengali kitchen method
✅ Rich golden colour without artificial colouring
✅ Instant PDF download — read on any device

WHAT'S INSIDE
• Ingredient list with exact quantities
• Full step-by-step method
• Tips for a smooth, non-bitter mustard paste
• Serving ideas with rice

PERFECT FOR
Mustard-gravy lovers, Bengali food enthusiasts, and anyone looking for a quick yet deeply flavourful vegetarian recipe.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Works on phone, tablet, computer, or print it at home.""",
    ),
    "Cholar_Dal_FINAL": (
        "Cholar Dal - Bengali Chana Dal with Coconut | Traditional Festive Recipe Ebook PDF",
        """Cholar Dal is THE Bengali festive dal — Bengal gram (chana dal) cooked with coconut pieces, raisins, ghee, and warm spices. Rich, slightly sweet, deeply comforting.

This digital cookbook PDF brings you:
✅ Authentic festive-style Cholar Dal recipe
✅ Right coconut-to-dal ratio for the classic texture
✅ Ghee tempering technique (chaunk) explained
✅ Perfect for Durga Puja, Bengali New Year, or any special occasion
✅ Instant PDF download — no waiting

WHAT'S INSIDE
• Full ingredient list with exact measurements
• Step-by-step method from soaking to serving
• Tips for a golden, non-mushy dal
• Serving suggestions (pairs beautifully with luchi or rice)

PERFECT FOR
Anyone who has tasted Cholar Dal at a Bengali feast and wanted to recreate it at home.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
    "Dhokar_Dalna_FINAL": (
        "Dhokar Dalna - Bengali Lentil Cake Curry | Authentic Niramish Recipe Ebook PDF",
        """Dhokar Dalna is a show-stopping Bengali niramish (no onion-garlic) recipe — fried lentil cakes (dhokar) simmered in a fragrant potato-based gravy. A festive favourite.

This digital cookbook PDF brings you:
✅ How to make perfectly firm, golden dhokar (lentil cakes)
✅ Authentic niramish gravy without onion or garlic
✅ Spice ratios for the classic Bengali flavour
✅ Troubleshooting tips — cakes that hold shape, not crumble
✅ Instant download, printable PDF

WHAT'S INSIDE
• Ingredient list for both dhokar and gravy
• Step-by-step method with timings
• Frying guide for golden, non-oily cakes
• Serving suggestions

PERFECT FOR
Bengali cooking enthusiasts and anyone who loves vegetarian dishes with real complexity and depth.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Works on phone, tablet, computer, or print it at home.""",
    ),
    "Kumro_Chhokka_FINAL": (
        "Kumro Chhokka - Bengali Spiced Pumpkin Recipe | Easy Vegetarian Indian Cookbook PDF",
        """Kumro Chhokka is a quick, dry-spiced Bengali pumpkin recipe made with mustard seeds, dried red chilli, and a touch of sugar — the perfect simple side dish.

This digital cookbook PDF brings you:
✅ Fast, fuss-free Bengali pumpkin preparation
✅ Panch phoron (five-spice) tempering method
✅ The sweet-spicy-smoky balance that makes this dish special
✅ Tips for choosing the right pumpkin (kumro)
✅ Instant PDF — no waiting, download immediately

WHAT'S INSIDE
• Ingredient list with exact quantities
• Step-by-step method
• Tips for the right dry texture (not mushy)
• Serving ideas — great with dal and rice

PERFECT FOR
Beginners to Bengali cooking, or anyone who wants a quick weeknight vegetable dish with real flavour.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
    "Aloo_Posto__FINAL": (
        "Aloo Posto - Bengali Potato in Poppy Seed Paste | Classic Niramish Recipe Ebook PDF",
        """Aloo Posto is perhaps the most iconic Bengali vegetarian recipe — potatoes cooked in a smooth, earthy poppy seed (posto) paste. Simple, addictive, irreplaceable.

This digital cookbook PDF brings you:
✅ The correct water-soaked posto paste method
✅ Authentic dry-style preparation (not gravy)
✅ Tips to avoid bitterness in the poppy seed paste
✅ No onion, no garlic — true niramish style
✅ Instant PDF download — start cooking today

WHAT'S INSIDE
• Ingredient list with exact quantities
• Full step-by-step method
• Grinding/blending tips for smooth posto paste
• Serving suggestions (best with steamed rice)

PERFECT FOR
Everyone — from Bengali homesick cooks to curious food lovers discovering posto for the first time.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Works on phone, tablet, computer, or print it at home.""",
    ),
    "Niramish_Shorshe_Potol_FINAL": (
        "Niramish Shorshe Potol - Bengali Mustard Pointed Gourd | Vegetarian Recipe Ebook PDF",
        """Niramish Shorshe Potol is a traditional Bengali vegetarian recipe — pointed gourd (potol/parwal) cooked in a sharp, fragrant mustard gravy without onion or garlic.

This digital cookbook PDF brings you:
✅ How to make a perfect, smooth shorshe (mustard) paste
✅ Authentic niramish method — no onion, no garlic
✅ Tips to remove bitterness from potol
✅ Golden, pungent gravy with perfect coating
✅ Instant PDF — download immediately after purchase

WHAT'S INSIDE
• Full ingredient list with quantities
• Step-by-step cooking method
• Mustard paste technique with grinding tips
• Serving suggestions

PERFECT FOR
Mustard-gravy lovers, Bengali cuisine enthusiasts, and anyone looking to cook authentic regional vegetarian food.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
    "Shukto_FINAL": (
        "Shukto - Bengali Bitter Mixed Vegetable Starter | Traditional Niramish Recipe Ebook PDF",
        """Shukto is the quintessential Bengali opening course — a bittersweet, complex mixed-vegetable dish cooked with milk, mustard, and panch phoron. No onion, no garlic.

This digital cookbook PDF brings you:
✅ Classic 7-vegetable Shukto recipe with bitter gourd
✅ The milk-and-mustard technique that defines this dish
✅ How to balance bitter, sweet, and spicy flavours
✅ Authentic niramish (no onion-garlic) preparation
✅ Instant PDF — download and start cooking

WHAT'S INSIDE
• Full ingredient list including all 7 vegetables
• Step-by-step method with timings
• Tips for a creamy, not watery, sauce
• Serving suggestions (always first course with rice)

PERFECT FOR
Adventurous cooks, Bengali food lovers, and anyone curious about the layered flavours of regional Indian cuisine.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Works on phone, tablet, computer, or print it at home.""",
    ),
    "Basanti_Pulao__FINAL": (
        "Basanti Pulao - Bengali Saffron Turmeric Rice | Traditional Festive Recipe Ebook PDF",
        """Basanti Pulao is Bengali festive rice at its finest — golden with turmeric and saffron, dotted with cashews, raisins, and whole spices. Served at every special occasion.

This digital cookbook PDF brings you:
✅ Authentic golden Basanti Pulao recipe
✅ Perfect rice-to-water ratio for fluffy, separate grains
✅ Ghee-tempering with whole spices technique
✅ How to get the golden colour right (turmeric + saffron balance)
✅ Instant PDF — download immediately

WHAT'S INSIDE
• Full ingredient list with exact quantities
• Step-by-step cooking method
• Tips for non-sticky festive rice
• Serving suggestions (pairs perfectly with Cholar Dal or Kosha Mangsho)

PERFECT FOR
Festive cooking, Bengali cuisine lovers, or anyone who wants a show-stopping rice dish for special occasions.

INSTANT DOWNLOAD
Your PDF is delivered immediately after purchase. No physical item is shipped.

📌 Compatible with all devices — phone, tablet, computer, or print it out.""",
    ),
}

BUNDLE = {
    "title": "Bengali Vegetarian Cookbook Bundle - All 10 Classic Recipes | Complete PDF Collection",
    "description": """Get all 10 authentic Bengali vegetarian recipe PDFs in one complete collection — a full repertoire of classic niramish and festive cooking from Bengal.

📚 WHAT'S INCLUDED (10 PDF Cookbooks):
1. Mochar Ghonto – Banana Flower Curry
2. Labra – Mixed Vegetable Festival Dish
3. Begun Basanti – Mustard Brinjal Curry
4. Cholar Dal – Festive Bengal Gram Dal
5. Dhokar Dalna – Lentil Cake Curry
6. Kumro Chhokka – Spiced Pumpkin
7. Aloo Posto – Potato in Poppy Seed Paste
8. Niramish Shorshe Potol – Mustard Pointed Gourd
9. Shukto – Bengali Bitter Starter
10. Basanti Pulao – Festive Saffron Rice

✅ All recipes are authentic, traditional, and niramish (no onion-garlic for most)
✅ Step-by-step instructions for home cooks
✅ Instant download — all 10 PDFs delivered immediately
✅ Printable format — works on all devices

PERFECT FOR
Bengali cooking enthusiasts, food lovers exploring regional Indian cuisine, or as a gift for someone who loves authentic vegetarian cooking.

INSTANT DOWNLOAD — 10 PDFs delivered immediately after purchase. No physical items shipped.""",
}

# ── helpers ───────────────────────────────────────────────────────────────────

def get_shop_id():
    r = requests.get(f"{BASE}/shops", headers=HEADERS, params={"shop_name": "DhanioDigital"})
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        # Try via user endpoint
        r2 = requests.get(f"{BASE}/users/me/shops", headers=HEADERS)
        r2.raise_for_status()
        results = r2.json().get("results", [])
    if not results:
        raise ValueError("Could not find DhanioDigital shop. Check ETSY_ACCESS_TOKEN.")
    shop = results[0]
    print(f"  Shop: {shop['shop_name']} (id={shop['shop_id']})")
    return shop["shop_id"]


def create_listing(shop_id, title, description, price, is_bundle=False):
    payload = {
        "quantity": QUANTITY,
        "title": title,
        "description": description,
        "price": price,
        "who_made": "i_did",
        "when_made": "made_to_order",
        "taxonomy_id": TAXONOMY_ID,
        "type": "download",
        "is_digital": True,
        "should_auto_renew": True,
        "tags": TAGS,
    }
    r = requests.post(f"{BASE}/shops/{shop_id}/listings", headers=HEADERS, json=payload)
    if not r.ok:
        print(f"  ERROR creating listing: {r.status_code} {r.text}")
        r.raise_for_status()
    listing_id = r.json()["listing_id"]
    print(f"  Created listing {listing_id}")
    return listing_id


def upload_image(listing_id, image_path_or_url, rank):
    """Upload an image file (local path) to a listing."""
    with open(image_path_or_url, "rb") as f:
        files = {"image": (Path(image_path_or_url).name, f, "image/jpeg")}
        data = {"rank": rank, "overwrite": "true"}
        r = requests.post(
            f"{BASE}/listings/{listing_id}/images",
            headers={k: v for k, v in HEADERS.items() if k != "Content-Type"},
            files=files,
            data=data,
        )
    if not r.ok:
        print(f"  ERROR uploading image rank {rank}: {r.status_code} {r.text}")
        r.raise_for_status()
    print(f"  Uploaded image rank {rank}: {Path(image_path_or_url).name}")
    time.sleep(0.5)


def upload_digital_file(shop_id, listing_id, file_path, display_name):
    """Upload a digital file (PDF) to a listing."""
    with open(file_path, "rb") as f:
        files = {"file": (display_name, f, "application/pdf")}
        data = {"name": display_name}
        r = requests.post(
            f"{BASE}/shops/{shop_id}/listings/{listing_id}/files",
            headers={k: v for k, v in HEADERS.items() if k != "Content-Type"},
            files=files,
            data=data,
        )
    if not r.ok:
        print(f"  ERROR uploading file '{display_name}': {r.status_code} {r.text}")
        r.raise_for_status()
    print(f"  Uploaded digital file: {display_name}")
    time.sleep(0.5)


def publish_listing(shop_id, listing_id):
    r = requests.patch(
        f"{BASE}/shops/{shop_id}/listings/{listing_id}",
        headers=HEADERS,
        json={"state": "active"},
    )
    if not r.ok:
        print(f"  ERROR publishing: {r.status_code} {r.text}")
        r.raise_for_status()
    print(f"  Published listing {listing_id} ✓")


def process_book(shop_id, slug, title, description):
    print(f"\n{'='*60}")
    print(f"BOOK: {slug}")
    print(f"{'='*60}")

    base_dir = Path(__file__).parent
    cover_path   = base_dir / "covers"   / f"{slug}.jpg"
    p2_path      = base_dir / "previews" / f"{slug}_p2.jpg"
    p3_path      = base_dir / "previews" / f"{slug}_p3.jpg"
    p4_path      = base_dir / "previews" / f"{slug}_p4.jpg"
    pdf_path     = base_dir / f"{slug}.pdf"
    download_pdf = base_dir / "How_to_Download.pdf"

    for p in [cover_path, p2_path, p3_path, p4_path, pdf_path, download_pdf]:
        if not p.exists():
            print(f"  MISSING: {p}")
            sys.exit(1)

    listing_id = create_listing(shop_id, title, description, PRICE_INR)

    # Images: rank 1=cover, 2-4=preview pages
    upload_image(listing_id, str(cover_path), rank=1)
    upload_image(listing_id, str(p2_path),    rank=2)
    upload_image(listing_id, str(p3_path),    rank=3)
    upload_image(listing_id, str(p4_path),    rank=4)

    # Digital files
    display_name = slug.replace("_FINAL", "").replace("__", " ").replace("_", " ") + ".pdf"
    upload_digital_file(shop_id, listing_id, str(pdf_path), display_name)
    upload_digital_file(shop_id, listing_id, str(download_pdf), "How_to_Download.pdf")

    publish_listing(shop_id, listing_id)
    return listing_id


def process_bundle(shop_id, book_slugs):
    print(f"\n{'='*60}")
    print("BUNDLE: Bengali Cookbook Collection")
    print(f"{'='*60}")

    base_dir = Path(__file__).parent
    # Use Cholar Dal cover as bundle hero (book 4 — already published; use Mochar Ghonto instead)
    # Covers for bundle: use first 4 books' covers as 4 images
    cover_slugs = ["Mochar_Ghonto_FINAL", "Labra_FINAL", "Begun_Basanti_FINAL", "Cholar_Dal_FINAL"]
    cover_paths = [base_dir / "covers" / f"{s}.jpg" for s in cover_slugs]
    for p in cover_paths:
        if not p.exists():
            print(f"  MISSING: {p}")
            sys.exit(1)

    listing_id = create_listing(shop_id, BUNDLE["title"], BUNDLE["description"], BUNDLE_PRICE, is_bundle=True)

    for rank, cp in enumerate(cover_paths, start=1):
        upload_image(listing_id, str(cp), rank=rank)

    # Upload all 10 PDFs + How_to_Download
    for slug in book_slugs:
        pdf_path = base_dir / f"{slug}.pdf"
        display_name = slug.replace("_FINAL", "").replace("__", " ").replace("_", " ") + ".pdf"
        upload_digital_file(shop_id, listing_id, str(pdf_path), display_name)

    upload_digital_file(shop_id, listing_id, str(base_dir / "How_to_Download.pdf"), "How_to_Download.pdf")

    publish_listing(shop_id, listing_id)
    return listing_id


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    # Which books to publish: pass slugs as CLI args, or publish all
    if len(sys.argv) > 1:
        slugs_to_publish = sys.argv[1:]
    else:
        slugs_to_publish = list(BOOKS.keys())

    publish_bundle = "--bundle" in slugs_to_publish
    if publish_bundle:
        slugs_to_publish = [s for s in slugs_to_publish if s != "--bundle"]
    if not slugs_to_publish and not publish_bundle:
        slugs_to_publish = list(BOOKS.keys())
        publish_bundle = True

    print("Fetching shop ID…")
    shop_id = get_shop_id()

    published = []
    for slug in slugs_to_publish:
        if slug not in BOOKS:
            print(f"Unknown slug: {slug}. Valid slugs: {list(BOOKS.keys())}")
            sys.exit(1)
        title, description = BOOKS[slug]
        lid = process_book(shop_id, slug, title, description)
        published.append((slug, lid))

    if publish_bundle:
        lid = process_bundle(shop_id, list(BOOKS.keys()))
        published.append(("BUNDLE", lid))

    print(f"\n{'='*60}")
    print("ALL DONE")
    for slug, lid in published:
        print(f"  {slug}: listing {lid}")


if __name__ == "__main__":
    main()
