import re
import codecs

def fix_html(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove html5-qrcode
    html = re.sub(r'\s*<script src="https://unpkg.com/html5-qrcode"></script>', '', html)
    
    # 2. Change the button
    # It might be PLAN LAYOVER or PLAN EXPERIENCE.
    # Find the button and replace onclick and text.
    html = re.sub(
        r'<button onclick="openVerificationModal\(\)".*?>\s*(PLAN LAYOVER|PLAN EXPERIENCE)\s*</button>',
        r'<button onclick="window.location.href=\'qr_upload_state.html\'" class="w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors">\n                            PLAN LAYOVER\n                        </button>',
        html,
        flags=re.DOTALL
    )

    # 3. Remove VERIFICATION MODAL and Scanner Modal HTML
    html = re.sub(
        r'<!-- VERIFICATION MODAL -->.*?<script>',
        '<script>',
        html,
        flags=re.DOTALL
    )

    # 4. Remove verification modal JS functions and QR functions
    # They usually start with function openVerificationModal() and go to the end of the script.
    html = re.sub(
        r'function openVerificationModal\(\).*?(document\.addEventListener\(\'DOMContentLoaded\')',
        r'\1',
        html,
        flags=re.DOTALL
    )
    
    # In some pages, the DOMContentLoaded logic contains generateUploadFields(). Let's remove that.
    html = re.sub(
        r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{.*?\}\);',
        'document.addEventListener(\'DOMContentLoaded\', renderHotels);',
        html,
        flags=re.DOTALL
    )

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

for page in ['hotel.html', 'restaurants.html', 'spas.html', 'entertainment.html']:
    try:
        fix_html(page)
        print(f"Fixed {page}")
    except Exception as e:
        print(f"Failed to fix {page}: {e}")
