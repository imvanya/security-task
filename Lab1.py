import numpy as np

img = np.zeros((4, 6, 3), dtype=np.uint8)
img[0:2, 0:3] = (255, 0, 0)       
img[0:2, 3:6] = (0, 255, 0)        
img[2:4, 0:3] = (0, 0, 255)        
img[2:4, 3:6] = (255, 255, 255)    

with open("test.ppm", "wb") as f:
    f.write(b"P6\n6 4\n255\n")
    f.write(img.tobytes())

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

ppm_img = read_ppm("test.ppm")
print("Завдання 1 - Перевірка:")
print("Розмір масиву:", ppm_img.shape) 
print("Піксель [0, 0]:", ppm_img[0, 0]) 
print("Піксель [3, 5]:", ppm_img[3, 5])


import struct #Завдання 2

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

write_bmp24("test.bmp", ppm_img)
import os
print("\nЗавдання 2 - Перевірка:")
print("Розмір файлу test.bmp на диску:", os.path.getsize("test.bmp"), "байт")



def read_bmp24(path): #Завдання 3
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

a = read_ppm("test.ppm")
write_bmp24("test.bmp", a)
b = read_bmp24("test.bmp")

print("\nЗавдання 3 - Перевірка:")
print("Масиви збігаються:", np.array_equal(a, b))



def write_bmp8(path, img): #Завдання 4
    height, width, _ = img.shape

    palette = bytearray()
    for i in range(256):
        if i < 216:
            r = (i // 36) * 51
            g = ((i // 6) % 6) * 51
            b = (i % 6) * 51
        else:
            r = g = b = 0
        palette += bytes((b, g, r, 0))  

    def color_index(r, g, b):
        return 36 * (int(r) // 51) + 6 * (int(g) // 51) + (int(b) // 51)

    bits = 8
    stride = ((width * bits + 31) // 32) * 4
    padding = stride - width
    offbits = 54 + 256 * 4  
    filesize = offbits + stride * height

    out = bytearray()
    out += struct.pack("<2sIHHI", b"BM", filesize, 0, 0, offbits)
    out += struct.pack("<IiiHHIIiiII", 40, width, height, 1, 8,
                       0, stride * height, 2835, 2835, 256, 0)
    out += palette

    for y in range(height - 1, -1, -1):
        for x in range(width):
            r, g, b = img[y, x]
            idx = color_index(r, g, b)
            out.append(idx)
        out += b"\x00" * padding

    with open(path, "wb") as f:
        f.write(out)

write_bmp8("test_8bit.bmp", ppm_img)

print("\nЗавдання 4 - Порівняння розмірів тестового файлу:")
print("PPM 24-bit:   ", os.path.getsize("test.ppm"), "байт")
print("BMP 24-bit:   ", os.path.getsize("test.bmp"), "байт")
print("BMP 8-bit:    ", os.path.getsize("test_8bit.bmp"), "байт")




import sys #Завдання 5
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