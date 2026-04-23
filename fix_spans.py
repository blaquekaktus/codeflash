import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def replace_spans(match):
    div_start = match.group(1)
    content = match.group(2)
    div_end = match.group(3)
    # Replace all spans in content with a tags
    new_content = re.sub(r'<span>([^<]+)</span>', r'<a href=\"https://flashcards-programming-app.vercel.app/packs\" style=\"color:inherit;text-decoration:none;display:block;cursor:pointer;padding:4px 0;\">\1</a>', content)
    return div_start + new_content + div_end

# Regex to match <div class="topic-packs"...>...</div>
html = re.sub(r'(<div class="topic-packs"[^>]*>)(.*?)(</div>)', replace_spans, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
