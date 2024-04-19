import io

import qrcode


def generate_qrcode(data):
    try:
        img_byte_arr = io.BytesIO()
        img = qrcode.make(data)
        img.save(img_byte_arr, 'PNG')
        return img_byte_arr.getvalue()
    except Exception as error:
        return
