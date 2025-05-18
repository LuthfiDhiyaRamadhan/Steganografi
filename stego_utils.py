from PIL import Image

def hide_message_in_image(image, message):
    img = image.convert("RGB")
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '00000000'  # Null terminator
    pixels = list(img.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Pesan terlalu panjang untuk disisipkan ke dalam gambar ini.")

    new_pixels = []
    idx = 0
    for pixel in pixels:
        r, g, b = pixel
        new_pixel = []
        for channel in (r, g, b):
            if idx < len(binary_message):
                bit = int(binary_message[idx])
                new_channel = (channel & ~1) | bit
                idx += 1
            else:
                new_channel = channel
            new_pixel.append(new_channel)
        new_pixels.append(tuple(new_pixel))

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(new_pixels)
    return encoded_img

def extract_message_from_image(image):
    binary_data = ""
    img = image.convert("RGB")
    pixels = list(img.getdata())

    for pixel in pixels:
        for channel in pixel:
            binary_data += bin(channel)[-1]

    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for char in chars:
        if char == "00000000":  # Null terminator
            break
        message += chr(int(char, 2))

    if message:
        return message
    else:
        return "Tidak ada pesan tersembunyi terdeteksi."
