import datetime
from typing import Optional


class Bonus:
    def __init__(
        self,
        user_id: int,
        amount: float = 100.0,  # Сумма бонуса (по умолчанию 100)
        created_at: Optional[datetime.datetime] = None,
        expires_at: Optional[datetime.datetime] = None,
        description: Optional[str] = None,
    ):
        self.user_id = user_id
        self.amount = amount
        self.created_at = created_at or datetime.datetime.now()
        self.expires_at = expires_at
        self.description = description

    def __str__(self):
        return f"Bonus(user_id={self.user_id}, amount={self.amount})"

    def is_expired(self) -> bool:
        # Проверка, истек ли срок действия бонуса
        if self.expires_at is None:
            return False
        return datetime.datetime.now() > self.expires_at
