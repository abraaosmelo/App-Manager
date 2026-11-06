"""Generate assets/logo-*.png and assets/icon.ico (no dependencies). Usage: python tools/make_logo.py"""
import struct, zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
TOP, BOTTOM = (59, 130, 246), (30, 64, 175)          # background gradient
WHITE, ACCENT = (255, 255, 255), (52, 211, 153)       # blocks
TILES = [(0.22, 0.22, WHITE), (0.53, 0.22, WHITE), (0.22, 0.53, WHITE), (0.53, 0.53, ACCENT)]
TILE, TILE_R, BG_R, MARGIN = 0.25, 0.06, 0.22, 0.04


def inside(x, y, x0, y0, w, h, r):
    """Is the point inside a rounded rectangle?"""
    if not (x0 <= x <= x0 + w and y0 <= y <= y0 + h):
        return False
    cx = min(max(x, x0 + r), x0 + w - r)
    cy = min(max(y, y0 + r), y0 + h - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def render(size, ss=4):
    """List of RGBA rows (top to bottom) with antialiasing by supersampling."""
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r = g = b = a = 0.0
            for sy in range(ss):
                for sx in range(ss):
                    x, y = (px + (sx + .5) / ss) / size, (py + (sy + .5) / ss) / size
                    if not inside(x, y, MARGIN, MARGIN, 1 - 2 * MARGIN, 1 - 2 * MARGIN, BG_R):
                        continue
                    t = (y - MARGIN) / (1 - 2 * MARGIN)
                    col = tuple(TOP[i] + (BOTTOM[i] - TOP[i]) * t for i in range(3))
                    for tx, ty, tc in TILES:
                        if inside(x, y, tx, ty, TILE, TILE, TILE_R):
                            col = tc
                            break
                    r += col[0]; g += col[1]; b += col[2]; a += 1
            n = ss * ss
            if a:
                row += bytes((round(r / a), round(g / a), round(b / a), round(255 * a / n)))
            else:
                row += b"\0\0\0\0"
        rows.append(bytes(row))
    return rows


def png(rows, size):
    raw = b"".join(b"\0" + r for r in rows)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def dib(rows, size):
    """BMP (DIB) image for small icons: bottom-up BGRA + empty AND mask."""
    px = b""
    for r in reversed(rows):
        px += b"".join(bytes((r[i + 2], r[i + 1], r[i], r[i + 3])) for i in range(0, len(r), 4))
    mask = (b"\0" * (((size + 31) // 32) * 4)) * size
    return struct.pack("<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0, len(px) + len(mask), 0, 0, 0, 0) + px + mask


def main():
    OUT.mkdir(exist_ok=True)
    images = {}
    for s in (16, 24, 32, 48, 64, 128, 256):
        images[s] = render(s, 4 if s >= 128 else 6)
    for s in (64, 256):
        (OUT / f"logo-{s}.png").write_bytes(png(images[s], s))
    entries, blobs, offset = b"", b"", 6 + 16 * len(images)
    for s, rows in images.items():
        data = png(rows, s) if s >= 128 else dib(rows, s)
        entries += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(data), offset + len(blobs))
        blobs += data
    (OUT / "icon.ico").write_bytes(struct.pack("<HHH", 0, 1, len(images)) + entries + blobs)
    print("ok:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
