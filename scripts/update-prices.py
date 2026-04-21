import glob
import re

files = glob.glob("bundles/*.html")
files.append("index.html")

pricing_map = {
    "Front End Engineer": {"old_price": "€49", "new_price": "€89", "packs": 23},
    "Security Engineer": {"old_price": "€39", "new_price": "€69", "packs": 15},
    "Back End Engineer": {"old_price": "€39", "new_price": "€59", "packs": 12},
    "DevOps Engineer": {"old_price": "€39", "new_price": "€59", "packs": 12},
    "Cloud / AWS Architect": {"old_price": "€29", "new_price": "€49", "packs": 8},
    "Interview Prep": {"old_price": "€29", "new_price": "€39", "packs": 6},
    "Mobile Developer": {"old_price": "€29", "new_price": "€39", "packs": 6},
    "Data Engineer": {"old_price": "€24", "new_price": "€39", "packs": 6},
    "Game Developer": {"old_price": "€29", "new_price": "€39", "packs": 5},
}

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Update Global Prices in index.html and bundle shared blocks
    content = content.replace(">€9 <", ">€24 <") # Monthly
    content = content.replace(">€99 <", ">€149 <") # Annual
    content = content.replace(">€7<", ">€9<") # Individual pack price
    content = content.replace(">€9<", ">€24<") # Ensure Monthly is 24 in index
    content = content.replace(">€24<", ">€24<") # idempotency
    
    # Update the old dollar versions just in case
    content = content.replace(">$7<", ">€9<")
    content = content.replace(">$49<", ">€89<")
    content = content.replace(">$39<", ">€39<") # will be handled below
    content = content.replace(">$29<", ">€39<")
    content = content.replace(">$24<", ">€39<")

    # In bundles, the individual pack price might be inside a po-price div
    content = re.sub(r'<div class="po-price">€?\$?7</div>', '<div class="po-price">€9</div>', content)
    
    # In index, "Individual Pack · License"
    content = content.replace('<div class="bundle-price">€7</div>', '<div class="bundle-price">€9</div>')

    # 2. Update specific bundles
    for bundle_name, data in pricing_map.items():
        old_p = data["old_price"]
        new_p = data["new_price"]
        packs = data["packs"]
        saving = (packs * 9) - int(new_p.replace('€', ''))
        
        # In index.html
        # We need to target the block for that specific bundle
        # e.g., <div class="bundle-name">Front End Engineer</div><div class="bundle-price">€49</div>
        pattern_index = f'(<div class="bundle-name">{re.escape(bundle_name)}</div>\\s*<div class="bundle-price">){re.escape(old_p)}(</div>)'
        content = re.sub(pattern_index, f'\\g<1>{new_p}\\g<2>', content)
        
        # Also handle edge cases where old_price might still have $
        pattern_index_usd = f'(<div class="bundle-name">{re.escape(bundle_name)}</div>\\s*<div class="bundle-price">)\\${old_p[1:]}(</div>)'
        content = re.sub(pattern_index_usd, f'\\g<1>{new_p}\\g<2>', content)

        # In bundles/*.html
        if bundle_name in content:
            # Update the main highlighted price
            pattern_bundle = f'(<div class="po-label">{re.escape(bundle_name)}</div>\\s*<div class="po-price">)[€$]{old_p[1:]}(</div>)'
            content = re.sub(pattern_bundle, f'\\g<1>{new_p}\\g<2>', content)
            
            # Update savings
            content = re.sub(r'Save [€$]\d+ vs individual', f'Save €{saving} vs individual', content)

    # Some manual cleanup for the All-Access text
    content = re.sub(r'<div class="bundle-price">€9 <small>', '<div class="bundle-price">€24 <small>', content)
    content = re.sub(r'<div class="bundle-price">€99 <small>', '<div class="bundle-price">€149 <small>', content)
    content = re.sub(r'<div class="po-price">€9</div>', '<div class="po-price">€24</div>', content)
    content = re.sub(r'<div class="po-price">€99</div>', '<div class="po-price">€149</div>', content)

    # Fix equivalent text for Annual (149 / 12 = 12.41)
    content = content.replace("€8.25 / month equivalent", "€12.41 / month equivalent")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Successfully applied new pricing strategy to all files.")
