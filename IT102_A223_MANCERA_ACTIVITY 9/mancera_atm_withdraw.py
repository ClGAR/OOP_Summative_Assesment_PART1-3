"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program handles ATM withdrawals by validating
the amount, asking the Account object to process the withdrawal, creating
a timestamp, and saving successful transactions in transactions.txt.

Reflection: I learned that withdrawals need more validation than deposits
because the Account object must also check whether enough balance is available.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

from datetime import datetime


def withdraw_money(account, amount):
    if amount <= 0:
        return False

    result = account.withdraw(amount)

    if result:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open("transactions.txt", "a", encoding="utf-8") as file:
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Account: {account.account_name}\n")
            file.write("Transaction: Withdraw\n")
            file.write(f"Amount: ₱{amount:.2f}\n")
            file.write("\n")

        return True

    return False