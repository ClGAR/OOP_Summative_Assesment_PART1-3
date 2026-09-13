"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program reads ATM transaction records from
transactions.txt and analyzes deposits and withdrawals. It calculates
transaction counts, totals, averages, the latest transaction, and the
largest transaction.

Reflection: I learned how loops, lists, dictionaries, file processing,
and calculations can work together to analyze multiple transaction
records stored in a text file.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""


def analyze_transactions():

    # TODO 1 and TODO 2
    try:
        with open("transactions.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

    except FileNotFoundError:
        return {
            "total_transactions": 0,
            "deposits": 0,
            "withdrawals": 0,
            "total_deposited": 0.0,
            "total_withdrawn": 0.0,
            "average_transaction": 0.0,
            "latest_transaction": "None",
            "latest_timestamp": "None",
            "largest_transaction": 0.0
        }

    # TODO 3
    transactions = []

    # TODO 4
    current = {}

    # TODO 5
    for line in lines:

        # TODO 6
        line = line.strip()

        # TODO 7
        if not line:
            continue

        # TODO 8
        if line.startswith("Timestamp:"):
            current["timestamp"] = line.split(":", 1)[1].strip()

        # TODO 9
        elif line.startswith("Account:"):
            current["account"] = line.split(":", 1)[1].strip()

        # TODO 10
        elif line.startswith("Transaction:"):
            current["type"] = line.split(":", 1)[1].strip()

        # TODO 11
        elif line.startswith("Amount:"):
            amount_text = line.split(":", 1)[1].strip()

            amount_text = amount_text.replace("₱", "")
            amount_text = amount_text.replace(",", "")

            try:
                current["amount"] = float(amount_text)
            except ValueError:
                current["amount"] = 0.0

            # TODO 12
            if (
                "timestamp" in current
                and "account" in current
                and "type" in current
                and "amount" in current
            ):
                transactions.append(current)
                current = {}

    # TODO 13
    total_transactions = len(transactions)

    # TODO 14
    deposits = 0

    # TODO 15
    withdrawals = 0

    # TODO 16
    total_deposited = 0.0

    # TODO 17
    total_withdrawn = 0.0

    total_amount = 0.0

    # TODO 18
    largest_transaction = 0.0

    for transaction in transactions:
        amount = transaction["amount"]
        transaction_type = transaction["type"]

        total_amount += amount

        if amount > largest_transaction:
            largest_transaction = amount

        if transaction_type == "Deposit":
            deposits += 1
            total_deposited += amount

        elif transaction_type == "Withdraw":
            withdrawals += 1
            total_withdrawn += amount

    # TODO 19 and TODO 20
    if total_transactions > 0:
        latest_transaction = transactions[-1]["type"]
        latest_timestamp = transactions[-1]["timestamp"]
    else:
        latest_transaction = "None"
        latest_timestamp = "None"

    # TODO 21
    if total_transactions > 0:
        average_transaction = total_amount / total_transactions
    else:
        average_transaction = 0.0

    # TODO 22
    return {
        "total_transactions": total_transactions,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "total_deposited": total_deposited,
        "total_withdrawn": total_withdrawn,
        "average_transaction": average_transaction,
        "latest_transaction": latest_transaction,
        "latest_timestamp": latest_timestamp,
        "largest_transaction": largest_transaction
    }