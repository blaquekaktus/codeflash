import glob

files = glob.glob("bundles/*.html")

old_text = '''<div class="price-option"><div class="po-label">All-Access (1 Year)</div><div class="po-price">$99</div><div class="po-detail">All 80+ packs. 12 months of updates.</div></div>
<div class="price-option"><div class="po-label">All-Access (Lifetime)</div><div class="po-price">$129</div><div class="po-detail">Every pack forever. One payment.</div></div>'''

new_text = '''<div class="price-option"><div class="po-label">All-Access (Monthly)</div><div class="po-price">€9</div><div class="po-detail">Stream via web app. Non-downloadable.</div></div>
<div class="price-option"><div class="po-label">All-Access (Annual)</div><div class="po-price">€99</div><div class="po-detail">Stream via web app. Non-downloadable.</div></div>'''

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace the all access pass text
    content = content.replace(old_text, new_text)
    
    # Replace $ with €
    content = content.replace('>$', '>€')
    
    # Also update '80+ packs' to '82 packs' everywhere
    content = content.replace('80+ packs', '82 packs')
    content = content.replace('80 packs', '82 packs')
    content = content.replace('1,600 cards', '1,640 cards')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Bundle pricing updated.")
