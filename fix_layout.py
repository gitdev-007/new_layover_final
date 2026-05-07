import re
import codecs

def fix_layout(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the main container
    html = html.replace(
        'max-w-7xl mx-auto flex flex-col lg:flex-row gap-6 relative',
        'max-w-4xl mx-auto flex flex-col gap-6 relative'
    )

    # 2. Update level2 container width
    html = html.replace(
        'w-full lg:w-[45%] flex-shrink-0',
        'w-full flex-shrink-0'
    )

    # 3. Remove "Theme: Blue/Purple" and "Theme: Orange" labels
    html = re.sub(r'<span class="text-meta-label text-(primary|secondary) uppercase">Theme:.*?</span>', '', html, flags=re.DOTALL)

    # 4. Remove max-h and sticky from level2 inner container so it expands down naturally
    html = html.replace('h-full max-h-[85vh] sticky top-28 overflow-hidden ', '')

    # 5. Fix Javascript: remove the width toggles
    html = re.sub(r"l1\.classList\.remove\('max-w-4xl', 'mx-auto'\);\s*l1\.classList\.add\('lg:w-\[55%\]'\);", '', html)
    html = re.sub(r"l1\.classList\.remove\('lg:w-\[55%\]'\);\s*l1\.classList\.add\('max-w-4xl', 'mx-auto'\);", '', html)

    # 6. Add scrollIntoView in openLevel2
    scroll_code = """    requestAnimationFrame(() => { 
        l2.classList.remove('opacity-0'); 
        setTimeout(() => {
            l2.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    });"""
    
    html = re.sub(
        r"requestAnimationFrame\(\(\) => \{ l2\.classList\.remove\('opacity-0'\); \}\);",
        scroll_code,
        html
    )
    
    html = re.sub(
        r"requestAnimationFrame\(\(\) => \{\s*l2\.classList\.remove\('opacity-0'\);\s*\}\);",
        scroll_code,
        html,
        flags=re.DOTALL
    )

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

for page in ['hotel.html', 'restaurants.html', 'spas.html', 'entertainment.html']:
    try:
        fix_layout(page)
        print(f"Fixed {page}")
    except Exception as e:
        print(f"Failed to fix {page}: {e}")
