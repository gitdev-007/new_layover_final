import codecs
import glob

for fpath in glob.glob('hotel*.html'):
    with codecs.open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace("\\'Hotel\\'", "'Hotel'")
    with codecs.open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
