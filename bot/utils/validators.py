from datetime import datetime
from typing import Optional

import cv2
import pyzbar.pyzbar as pyzbar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.users import User


async def valid_phone_number(phone_number: str) -> bool:
    return len(phone_number) == 10 and phone_number.isdigit()


async def find_user_by_phone(phone_number: str, session: AsyncSession) -> Optional[User]:
    return await session.scalars(select(User).where(User.phone_number == phone_number))


def decode_qr_code(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data
    return None


async def valid_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        decoded_data = decode_qr_code(frame)
        if decoded_data:
            return decoded_data
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None


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
