import codecs

def fix_filename(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace all incorrect capitalizations with the exact filename
    updated_html = html.replace('qr_upload_state.html', 'QR_Upload_State.html')

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_html)

for page in ['hotel.html', 'restaurants.html', 'spas.html', 'entertainment.html']:
    try:
        fix_filename(page)
        print(f"Fixed {page}")
    except Exception as e:
        print(f"Failed to fix {page}: {e}")
