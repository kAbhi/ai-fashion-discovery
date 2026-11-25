"""Final batch of sample products to exceed 100 catalogue items.

All data here is clearly identified as development/sample data.
"""

IMAGE_BASE = "https://placehold.co/400x400/e2e8f0/475569?text={}"


def _img(text: str) -> str:
    return IMAGE_BASE.format(text.replace(" ", "+"))


MORE_PRODUCTS = [
    {
        "name": "W for Women Organza Saree",
        "brand": "W for Women",
        "description": "Sheer organza saree with embroidered border for evening events.",
        "category": "ethnic_wear", "subcategory": "saree", "gender_audience": "women",
        "style_tags": ["organza", "sheer", "evening"],
        "occasion_tags": ["evening", "party", "reception"],
        "image_references": [_img("W Organza Saree")],
        "variants": [{"size": "Free", "colour": "Lavender"}, {"size": "Free", "colour": "Peach"}],
        "merchant_listings": [{"merchant": "Myntra", "current_price": 6499.0, "availability": "in_stock"}],
    },
    {
        "name": "FabIndia Ajrakh Saree",
        "brand": "FabIndia",
        "description": "Ajrakh block-print saree from Gujarat for cultural occasions.",
        "category": "ethnic_wear", "subcategory": "saree", "gender_audience": "women",
        "style_tags": ["block_print", "traditional", "gujarat"],
        "occasion_tags": ["cultural", "festive", "daytime"],
        "image_references": [_img("FabIndia Ajrakh Saree")],
        "variants": [{"size": "Free", "colour": "Indigo"}, {"size": "Free", "colour": "Red"}],
        "merchant_listings": [{"merchant": "FabIndia", "current_price": 4999.0, "availability": "in_stock"}],
    },
    {
        "name": "Ritu Kumar Gown",
        "brand": "Ritu Kumar",
        "description": "Designer gown for cocktail parties and formal evenings.",
        "category": "dresses", "subcategory": "gown", "gender_audience": "women",
        "style_tags": ["designer", "cocktail", "formal"],
        "occasion_tags": ["cocktail_party", "formal_evening", "gala"],
        "image_references": [_img("Ritu Kumar Gown")],
        "variants": [{"size": "M", "colour": "Navy"}, {"size": "L", "colour": "Navy"}],
        "merchant_listings": [{"merchant": "Myntra", "current_price": 15999.0, "availability": "in_stock"}],
    },
    {
        "name": "Zara India Pleated Skirt",
        "brand": "Zara",
        "description": "Pleated midi skirt for smart-casual styling.",
        "category": "trousers", "subcategory": "skirt", "gender_audience": "women",
        "style_tags": ["pleated", "midi", "smart_casual"],
        "occasion_tags": ["office", "casual", "date_night"],
        "image_references": [_img("Zara Pleated Skirt")],
        "variants": [{"size": "S", "colour": "Black"}, {"size": "M", "colour": "Black"}],
        "merchant_listings": [{"merchant": "Zara", "current_price": 2999.0, "availability": "in_stock"}],
    },
    {
        "name": "H&M India Hoodie",
        "brand": "H&M",
        "description": "Cotton hoodie for casual winter wear.",
        "category": "tops_shirts", "subcategory": "hoodie", "gender_audience": "unisex",
        "style_tags": ["hoodie", "casual", "winter"],
        "occasion_tags": ["casual", "winter", "everyday_wear"],
        "image_references": [_img("H&M Hoodie")],
        "variants": [{"size": "M", "colour": "Grey"}, {"size": "L", "colour": "Grey"}, {"size": "XL", "colour": "Grey"}],
        "merchant_listings": [{"merchant": "H&M", "current_price": 2499.0, "availability": "in_stock"}],
    },
    {
        "name": "Levi's Trucker Jacket",
        "brand": "Levi's",
        "description": "Denim trucker jacket for casual layering.",
        "category": "tops_shirts", "subcategory": "jacket", "gender_audience": "men",
        "style_tags": ["denim", "trucker", "casual"],
        "occasion_tags": ["casual", "weekend", "layering"],
        "image_references": [_img("Levi's Trucker Jacket")],
        "variants": [{"size": "M", "colour": "Blue"}, {"size": "L", "colour": "Blue"}],
        "merchant_listings": [{"merchant": "Levi's", "current_price": 5999.0, "availability": "in_stock"}],
    },
    {
        "name": "Raymond Suit Separates Trousers",
        "brand": "Raymond",
        "description": "Trousers sold separately for suit mix-and-match styling.",
        "category": "trousers", "subcategory": "suit_trousers", "gender_audience": "men",
        "style_tags": ["separates", "formal", "mix_match"],
        "occasion_tags": ["office", "formal", "business"],
        "image_references": [_img("Raymond Suit Trousers")],
        "variants": [{"size": "34", "colour": "Navy"}, {"size": "36", "colour": "Navy"}],
        "merchant_listings": [{"merchant": "Raymond", "current_price": 2299.0, "availability": "in_stock"}],
    },
    {
        "name": "Pantaloons Women's Leggings",
        "brand": "Pantaloons",
        "description": "Cotton-blend leggings for casual and athleisure wear.",
        "category": "trousers", "subcategory": "leggings", "gender_audience": "women",
        "style_tags": ["athleisure", "cotton_blend", "casual"],
        "occasion_tags": ["casual", "athleisure", "daily_wear"],
        "image_references": [_img("Pantaloons Leggings")],
        "variants": [{"size": "M", "colour": "Black"}, {"size": "L", "colour": "Black"}, {"size": "S", "colour": "Black"}],
        "merchant_listings": [{"merchant": "Pantaloons", "current_price": 799.0, "availability": "in_stock"}],
    },
    {
        "name": "Nike Slides",
        "brand": "Nike",
        "description": "Post-sport slides for gym and shower use.",
        "category": "casual_footwear", "subcategory": "slides", "gender_audience": "unisex",
        "style_tags": ["slides", "sport", "post_workout"],
        "occasion_tags": ["fitness", "gym", "casual"],
        "image_references": [_img("Nike Slides")],
        "variants": [{"size": "8", "colour": "Black"}, {"size": "9", "colour": "Black"}, {"size": "10", "colour": "Black"}],
        "merchant_listings": [{"merchant": "Nike", "current_price": 1999.0, "availability": "in_stock"}],
    },
    {
        "name": "Adidas Pool Slides",
        "brand": "Adidas",
        "description": "Poolside slides for summer and vacation.",
        "category": "casual_footwear", "subcategory": "slides", "gender_audience": "unisex",
        "style_tags": ["poolside", "summer", "vacation"],
        "occasion_tags": ["goa_vacation", "beach", "summer"],
        "image_references": [_img("Adidas Pool Slides")],
        "variants": [{"size": "7", "colour": "Blue"}, {"size": "8", "colour": "Blue"}, {"size": "9", "colour": "Blue"}],
        "merchant_listings": [{"merchant": "Adidas", "current_price": 2499.0, "availability": "in_stock"}],
    },
    {
        "name": "Puma Slides",
        "brand": "Puma",
        "description": "Branded slides for casual and gym wear.",
        "category": "casual_footwear", "subcategory": "slides", "gender_audience": "unisex",
        "style_tags": ["branded", "casual", "gym"],
        "occasion_tags": ["gym", "casual", "everyday_footwear"],
        "image_references": [_img("Puma Slides")],
        "variants": [{"size": "8", "colour": "Black"}, {"size": "9", "colour": "Black"}],
        "merchant_listings": [{"merchant": "Puma", "current_price": 1799.0, "availability": "in_stock"}],
    },
    {
        "name": "FabIndia Block-Print Scarf",
        "brand": "FabIndia",
        "description": "Block-print cotton scarf for styling.",
        "category": "accessories", "subcategory": "scarf", "gender_audience": "women",
        "style_tags": ["block_print", "cotton", "accessory"],
        "occasion_tags": ["casual", "festive", "everyday"],
        "image_references": [_img("FabIndia Block-Print Scarf")],
        "variants": [{"size": "Free", "colour": "Multi"}, {"size": "Free", "colour": "Blue"}],
        "merchant_listings": [{"merchant": "FabIndia", "current_price": 599.0, "availability": "in_stock"}],
    },
    {
        "name": "Tanishq Silver Bangle",
        "brand": "Tanishq",
        "description": "Sterling silver bangle for traditional and daily wear.",
        "category": "accessories", "subcategory": "jewellery", "gender_audience": "women",
        "style_tags": ["silver", "traditional", "bangle"],
        "occasion_tags": ["festive", "daily_wear", "traditional"],
        "image_references": [_img("Tanishq Bangle")],
        "variants": [{"size": "Free", "colour": "Silver"}],
        "merchant_listings": [{"merchant": "Tanishq", "current_price": 2800.0, "availability": "in_stock"}],
    },
    {
        "name": "Raymond Cufflinks",
        "brand": "Raymond",
        "description": "Silver cufflinks for formal shirts and suits.",
        "category": "accessories", "subcategory": "cufflinks", "gender_audience": "men",
        "style_tags": ["silver", "formal", "accessory"],
        "occasion_tags": ["formal", "wedding", "office"],
        "image_references": [_img("Raymond Cufflinks")],
        "variants": [{"size": "Free", "colour": "Silver"}],
        "merchant_listings": [{"merchant": "Raymond", "current_price": 1299.0, "availability": "in_stock"}],
    },
    {
        "name": "Manyavar Bandi Jacket",
        "brand": "Manyavar",
        "description": "Sleeveless bandi jacket for festive layering over kurtas.",
        "category": "indo_western", "subcategory": "bandi", "gender_audience": "men",
        "style_tags": ["sleeveless", "festive", "layering"],
        "occasion_tags": ["festive", "wedding_guest", "family_gathering"],
        "image_references": [_img("Manyavar Bandi")],
        "variants": [{"size": "40", "colour": "Black"}, {"size": "42", "colour": "Black"}],
        "merchant_listings": [{"merchant": "Manyavar", "current_price": 3999.0, "availability": "in_stock"}],
    },
    {
        "name": "Biba Sharara Pants",
        "brand": "Biba",
        "description": "Flared sharara pants for fusion styling.",
        "category": "trousers", "subcategory": "sharara_pants", "gender_audience": "women",
        "style_tags": ["flared", "fusion", "traditional"],
        "occasion_tags": ["festive", "casual", "party"],
        "image_references": [_img("Biba Sharara Pants")],
        "variants": [{"size": "M", "colour": "Peach"}, {"size": "L", "colour": "Peach"}],
        "merchant_listings": [{"merchant": "Myntra", "current_price": 1499.0, "availability": "in_stock"}],
    },
]

SAMPLE_DATA_NOTICE = """
================================================================================
SAMPLE DATA NOTICE (MORE)
================================================================================
All products in this file are DEVELOPMENT/SAMPLE data. See the notice in
sample_catalogue.py for details.
================================================================================
"""
