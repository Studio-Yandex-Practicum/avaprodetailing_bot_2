from enum import Enum


class PaymentStateEnum(str, Enum):
    WAITING = "Ожидание"
    PAID = "Оплачено"
    NOT_PAID = "Не оплачено"
