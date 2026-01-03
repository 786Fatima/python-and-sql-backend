from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.transaction import Transaction

def transfer_money(
    db: Session,
    sender_account_id: int,
    receiver_account_id: int,
    amount: float
):
    sender = db.query(Account).filter(Account.id == sender_account_id).first()
    receiver = db.query(Account).filter(Account.id == receiver_account_id).first()

    if sender.balance < amount:
        raise Exception("Insufficient balance")

    sender.balance -= amount
    receiver.balance += amount

    transaction = Transaction(
        sender_account_id=sender_account_id,
        receiver_account_id=receiver_account_id,
        amount=amount
    )

    db.add(transaction)
    db.commit()
