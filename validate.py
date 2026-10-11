from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

root=Path(__file__).parent/'dist'
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.links=[];self.ids=set();self.h1=0;self.images=[];self.title=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.images.append(a)
        if tag=='link' and a.get('rel') in ['stylesheet','icon']:self.links.append(a.get('href',''))
        if tag=='script' and 'src' in a:self.links.append(a['src'])
pages={}
errors=[]
for file in root.glob('*.html'):
    p=Page();p.feed(file.read_text(encoding='utf-8'));pages[file.name]=p
    if p.h1!=1:errors.append(f'{file.name}: expected one h1')
    for im in p.images:
        if not (root/im['src']).exists():errors.append(f'{file.name}: missing image {im["src"]}')
        if 'alt' not in im:errors.append(f'{file.name}: missing alt')
for name,p in pages.items():
    for href in p.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        dest=u.path or name
        if not (root/dest).exists():errors.append(f'{name}: missing {dest}')
        if u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:errors.append(f'{name}: missing anchor {href}')
css=(root/'assets/style.css').read_text(encoding='utf-8')
for asset in re.findall(r'url\([\"\']?([^\)\"\']+)',css):
    if asset.startswith('data:'):continue
    if not (root/'assets'/asset).exists():errors.append(f'CSS missing {asset}')
if errors:raise SystemExit('\n'.join(errors))
print(f'OK: {len(pages)} pages, all local links, anchors, images and fonts exist; one h1 per page.')
