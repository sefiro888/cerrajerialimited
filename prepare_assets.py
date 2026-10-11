from pathlib import Path
from PIL import Image
import json
root=Path(__file__).parent
origin=Path(r'C:\Users\sefir\.codex\generated_images\01a12bf0-1859-79e3-beb9-da103f36fa05')
files={'hero':'exec-36b8f81f-97f4-4bb0-a1c4-9bf73616cfb2.png','keys':'exec-4cf57c27-dbb4-4024-9f49-924094cff769.png','mobile':'exec-98cdde25-bd70-4d1e-b367-867e2c53f0d5.png'}
for name,file in files.items():
    im=Image.open(origin/file)
    im.save(root/'dist'/'assets'/f'{name}.webp',quality=89,method=6)
    print(name,im.size)
css=root/'dist'/'assets'/'style.css'
css.write_text(css.read_text(encoding='utf-8').replace("barlow-condensed.woff2') format('woff2')","barlow-condensed.ttf') format('truetype')"),encoding='utf-8')
manifest=root/'.openai'/'hosting.json'
manifest.write_text(json.dumps({'project_id':'appgprj_6acbc2ea3e9881919d05290ec9817e67','static':{'directory':'dist'}},indent=2))
