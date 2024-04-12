from aiogram.types import CallbackQuery, Message
from pyzbar.pyzbar import decode
import cv2
import qrcode
from datetime import datetime

from bot.db.models.users import User


def generate_qr_code(data):
    pass
    # data = "..."
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    # )
    # qr.add_data(data)
    # qr.make(fit=True)
    # img = qr.make_image(fill_color="black", back_color="white")
    # return img


def scan_qr_code(message: Message):
    pass
    # cap = cv2.VideoCapture(0)
    # captured = False

    # while not captured:
    #     ret, frame = cap.read()
    #     decoded_objects = decode(frame)

    #     for obj in decoded_objects:
    #         data = obj.data.decode('utf-8')
    #         message.answer(f"QR Code Data: {data}")
    #         captured = True

    #     cv2.imshow("QR Scanner", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()


def generate_payment_check(user: User, amount: int):
    check_content = f"""
    Название компании: Avaprodetailing
    Дата и время: {datetime.now()}
    Тип оплаты: Наличные
    Сумма оплаты: {amount}
    Клиент: {user.first_name} {user.last_name}
    """
    check_file_path = "check.txt"
    with open(check_file_path, "w") as check_file:
        check_file.write(check_content)
    return check_file_path
