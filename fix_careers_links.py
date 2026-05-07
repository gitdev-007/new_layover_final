import os
import glob
import re

def update_links():
    html_files = glob.glob('*.html')
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='utf-16') as f:
                    content = f.read()
            except Exception as e:
                print(f"Skipping {filepath} due to decoding error: {e}")
                continue
                
        original_content = content
        
        # Replace specific hrefs pointing to old career pages
        content = re.sub(r'href="careerhome\.html"', 'href="careershome.html"', content)
        content = re.sub(r'href="careers\.html"', 'href="careershome.html"', content)
        
        # Replace href="#" where the text is exactly "Careers"
        content = re.sub(r'href="#"([^>]*>Careers<)', r'href="careershome.html"\1', content, flags=re.IGNORECASE)
        
        # Replace window.location.href for careerhome
        content = re.sub(r'window\.location\.href\s*=\s*[\'"]careerhome\.html[\'"]', 'window.location.href="careershome.html"', content)
        content = re.sub(r'window\.location\.href\s*=\s*[\'"]careers\.html[\'"]', 'window.location.href="careershome.html"', content)
        
        if content != original_content:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated links in {filepath}")
            except Exception as e:
                print(f"Failed to write to {filepath}: {e}")

update_links()
