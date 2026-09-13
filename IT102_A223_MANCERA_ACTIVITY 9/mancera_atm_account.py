"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program creates an Account object that can
check its balance, accept valid deposits, and perform withdrawals only
when the amount is valid and the account has enough balance.

Reflection: I learned how encapsulation allows the Account class to
control changes to its internal balance and prevent invalid withdrawals.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""


class Account:
    def __init__(self, name, starting_balance):
        self.account_name = name
        self._balance = starting_balance

    def check_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        else:
            return False


# TEST PROGRAM
account = Account("Roger Mancera", 10000)

print("Account Name:", account.account_name)
print(f"Starting Balance: P{account.check_balance():.2f}")

withdraw_amount = 2000

if account.withdraw(withdraw_amount):
    print(f"Withdrawal: P{withdraw_amount:.2f}")
    print(f"New Balance: P{account.check_balance():.2f}")
else:
    print("Withdrawal failed.")


# Test insufficient balance
withdraw_amount = 15000

if account.withdraw(withdraw_amount):
    print(f"Withdrawal: P{withdraw_amount:.2f}")
else:
    print(
        f"Withdrawal of P{withdraw_amount:.2f} failed."
    )
    print("Reason: Insufficient balance.")
    print(
        f"Current Balance: P{account.check_balance():.2f}"
    )