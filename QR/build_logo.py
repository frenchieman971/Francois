from collections import deque

from PIL import Image

SRC = "/private/tmp/claude-501/-Users-frenchie-Library-Mobile-Documents-com-apple-CloudDocs-CLAUDE-SAVE-CLAUDE/0a7ccc57-ecd0-46a9-96ea-067fdd8f9ae8/images/1.png"
OUT = "/Users/frenchie/Library/Mobile Documents/com~apple~CloudDocs/Francois DJ/logo-dj.png"

img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()


def is_white(x, y, t):
    r, g, b = px[x, y]
    return min(r, g, b) > t


# 1) efface le numéro de téléphone : petites zones blanches fermées dans le bandeau noir
white = [[is_white(x, y, 90) for x in range(W)] for y in range(H)]
seen = [[False] * W for _ in range(H)]
removed = 0
boxes = []
for sy in range(0, 140):
    for sx in range(W):
        if not white[sy][sx] or seen[sy][sx]:
            continue
        comp, q, touches = [], deque([(sx, sy)]), False
        seen[sy][sx] = True
        while q:
            x, y = q.popleft()
            comp.append((x, y))
            if x in (0, W - 1) or y in (0, H - 1):
                touches = True
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H and white[ny][nx] and not seen[ny][nx]:
                    seen[ny][nx] = True
                    q.append((nx, ny))
        ys = [y for _, y in comp]
        if not touches and len(comp) < 1500 and max(ys) < 140:
            for x, y in comp:
                px[x, y] = (0, 0, 0)
            xs = [x for x, _ in comp]
            boxes.append((min(xs), min(ys), max(xs), max(ys)))
            removed += 1

# 1b) liseré gris autour des chiffres : pixels gris (pas orangés) dans la zone effacée
for x0, y0, x1, y1 in boxes:
    for y in range(max(0, y0 - 3), min(H, y1 + 4)):
        for x in range(max(0, x0 - 3), min(W, x1 + 4)):
            r, g, b = px[x, y]
            if min(r, g, b) > 12 and max(r, g, b) - min(r, g, b) < 60:
                px[x, y] = (0, 0, 0)

# 2) fond blanc extérieur -> transparent (uniquement ce qui touche le bord)
out = img.convert("RGBA")
opx = out.load()
vis = [[False] * W for _ in range(H)]
q = deque()
for x in range(W):
    for y in (0, H - 1):
        q.append((x, y))
for y in range(H):
    for x in (0, W - 1):
        q.append((x, y))
while q:
    x, y = q.popleft()
    if vis[y][x]:
        continue
    vis[y][x] = True
    if min(px[x, y]) <= 200:
        continue
    opx[x, y] = (255, 255, 255, 0)
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < W and 0 <= ny < H and not vis[ny][nx]:
            q.append((nx, ny))

out.save(OUT)
print("zones effacées :", removed)
print("ok", OUT)
