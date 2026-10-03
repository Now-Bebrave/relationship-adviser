import base64, pathlib, re

p = pathlib.Path(r'D:\WorkFiles\adviser\关系观察手册.html')
html = p.read_text(encoding='utf-8')

base = pathlib.Path(r'D:\WorkFiles\adviser')
pattern = re.compile(r'src="(assets/relationship-handbook-illustrations/[^"]+\.png)"')

def repl(m):
    rel = m.group(1)
    img = base / rel
    if not img.exists():
        print('missing:', rel)
        return m.group(0)
    b64 = base64.b64encode(img.read_bytes()).decode()
    print('inlined:', rel)
    return f'src="data:image/png;base64,{b64}"'

html = pattern.sub(repl, html)
p.write_text(html, encoding='utf-8')
print('done, size =', p.stat().st_size)
