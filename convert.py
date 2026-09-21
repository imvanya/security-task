import sys
import struct
import numpy as np

def read_ppm(path):
    with open(path, "rb") as f:
        header = f.readline().decode('ascii').strip()
        if header != 'P6':
            raise ValueError("Підтримується лише формат P6")
        line = f.readline().decode('ascii')
        while line.startswith('#'):
            line = f.readline().decode('ascii')
        width, height = map(int, line.split())
        maxval = int(f.readline().decode('ascii').strip())
        data = f.read()
        return np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))

def write_ppm(path, img):
    height, width, _ = img.shape
    with open(path, "wb") as f:
        header = f"P6\n{width} {height}\n255\n".encode('ascii')
        f.write(header)
        f.write(img.tobytes())

def write_bmp24(path, img):
    height, width, _ = img.shape
    stride   = ((width * 24 + 31) // 32) * 4
    padding  = stride - width * 3
    offbits  = 54
    filesize = offbits + stride * height

    out = bytearray()
    out += struct.pack("<2sIHHI", b"BM", filesize, 0, 0, offbits)
    out += struct.pack("<IiiHHIIiiII", 40, width, height, 1, 24,
                       0, stride * height, 2835, 2835, 0, 0)

    for y in range(height - 1, -1, -1):
        for x in range(width):
            r, g, b = img[y, x]
            out += bytes((b, g, r))
        out += b"\x00" * padding

    with open(path, "wb") as f:
        f.write(out)

def read_bmp24(path):
    with open(path, "rb") as f:
        data = f.read()

    offbits = struct.unpack_from("<I", data, 10)[0]
    width   = struct.unpack_from("<i", data, 18)[0]
    height  = struct.unpack_from("<i", data, 22)[0]
    bits    = struct.unpack_from("<H", data, 28)[0]
    stride  = ((width * bits + 31) // 32) * 4

    img = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        start = offbits + y * stride
        for x in range(width):
            b = data[start + x * 3 + 0]
            g = data[start + x * 3 + 1]
            r = data[start + x * 3 + 2]
            img[height - 1 - y, x] = (r, g, b)
    return img

def main():
    if len(sys.argv) < 3:
        print("Використання: python convert.py <input> <output>")
        return

    src = sys.argv[1]
    dst = sys.argv[2]

    if src.endswith(".ppm") and dst.endswith(".bmp"):
        img = read_ppm(src)
        write_bmp24(dst, img)
        print(f"Успішно перетворено {src} -> {dst}")
    elif src.endswith(".bmp") and dst.endswith(".ppm"):
        img = read_bmp24(src)
        write_ppm(dst, img)
        print(f"Успішно перетворено {src} -> {dst}")
    else:
        print("Не знаю, як перетворити ці формати (підтримуються тільки .ppm <-> .bmp)")

if __name__ == "__main__":
    main()