"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program handles ATM deposits by validating
the amount, updating the Account object, creating a timestamp, and
saving the transaction in transactions.txt.

Reflection: I learned how a separate deposit module can work with an
Account object, record transaction details, and return a result to the
main program.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

from datetime import datetime


def deposit_money(account, amount):
    if amount <= 0:
        return False

    result = account.deposit(amount)

    if result:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open("transactions.txt", "a", encoding="utf-8") as file:
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Account: {account.account_name}\n")
            file.write("Transaction: Deposit\n")
            file.write(f"Amount: ₱{amount:.2f}\n")
            file.write("\n")

        return True

    return False