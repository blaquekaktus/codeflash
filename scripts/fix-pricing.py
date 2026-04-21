import glob

files = glob.glob("bundles/*.html")
files.append("index.html")

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix individual pack price in bundles
    content = content.replace(
        '<div class="price-option"><div class="po-label">Individual Pack</div><div class="po-price">€24</div>',
        '<div class="price-option"><div class="po-label">Individual Pack</div><div class="po-price">€9</div>'
    )
    
    # Fix individual pack price in index
    content = content.replace(
        '<div class="bundle-name">Individual Pack · License</div><div class="bundle-price">€24</div>',
        '<div class="bundle-name">Individual Pack · License</div><div class="bundle-price">€9</div>'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Fixed Individual Pack pricing.")
