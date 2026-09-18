"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 14, 2026

Program Description: This module contains additional Mancera Bank
services including money transfer, bills payment, savings goals,
and the Smart Balance Guard.

Reflection: I learned how new banking services can work with an
existing Account object while keeping the program modular. I also
learned how OOP objects, files, validation, and account methods can
work together to create more advanced banking features.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

import json

import mancera_bank_storage
import mancera_bank_transactions


GOALS_FILE = "savings_goals.txt"
PREFERENCES_FILE = "bank_preferences.txt"


# ============================================================
# GENERAL FILE HELPERS
# ============================================================

def read_json_file(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        return default


def save_json_file(filename, data):
    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# SMART BALANCE GUARD
# ============================================================

def get_guard(account_number):
    preferences = read_json_file(
        PREFERENCES_FILE,
        {}
    )

    return preferences.get(
        account_number,
        {
            "enabled": False,
            "reserve": 0.0
        }
    )


def set_guard(account, reserve, enabled):
    if reserve < 0:
        return False, "Reserve amount cannot be negative."

    if reserve > account.check_balance():
        return (
            False,
            "Reserve cannot be greater than "
            "your current balance."
        )

    preferences = read_json_file(
        PREFERENCES_FILE,
        {}
    )

    preferences[
        account.account_number
    ] = {
        "enabled": enabled,
        "reserve": float(reserve)
    }

    save_json_file(
        PREFERENCES_FILE,
        preferences
    )

    return True, "Smart Balance Guard updated."


def check_guard(account, amount):
    guard = get_guard(
        account.account_number
    )

    if not guard["enabled"]:
        return True, ""

    remaining_balance = (
        account.check_balance()
        - amount
    )

    if remaining_balance < guard["reserve"]:

        return (
            False,
            "Smart Balance Guard blocked this transaction. "
            f"You protected "
            f"₱{guard['reserve']:,.2f} "
            "as your emergency reserve."
        )

    return True, ""


def get_safe_to_spend(account):
    guard = get_guard(
        account.account_number
    )

    if not guard["enabled"]:
        return account.check_balance()

    safe_amount = (
        account.check_balance()
        - guard["reserve"]
    )

    return max(
        safe_amount,
        0
    )


# ============================================================
# MONEY TRANSFER
# ============================================================

def transfer_money(
    sender,
    recipient_account_number,
    amount,
    pin
):

    recipient_account_number = (
        recipient_account_number.strip()
    )

    pin = pin.strip()

    if amount <= 0:

        return (
            False,
            "Transfer amount must be greater than zero."
        )

    if recipient_account_number == "":

        return (
            False,
            "Please enter the recipient account number."
        )

    if (
        recipient_account_number
        == sender.account_number
    ):

        return (
            False,
            "You cannot transfer money "
            "to your own account."
        )

    if not sender.verify_pin(pin):

        return (
            False,
            "Incorrect PIN."
        )

    recipient = (
        mancera_bank_storage
        .find_account(
            recipient_account_number
        )
    )

    if recipient is None:

        return (
            False,
            "Recipient account was not found."
        )

    if amount > sender.check_balance():

        return (
            False,
            "Insufficient balance."
        )

    allowed, message = check_guard(
        sender,
        amount
    )

    if not allowed:

        return False, message

    withdraw_success = sender.withdraw(
        amount
    )

    if not withdraw_success:

        return (
            False,
            "Transfer could not be completed."
        )

    deposit_success = recipient.deposit(
        amount
    )

    if not deposit_success:

        # Restore sender balance if something
        # unexpected happens.
        sender.deposit(amount)

        return (
            False,
            "Transfer could not be completed."
        )

    mancera_bank_storage.update_account(
        sender
    )

    mancera_bank_storage.update_account(
        recipient
    )

    mancera_bank_transactions.record_transaction(
        sender,
        "Transfer Out",
        amount
    )

    mancera_bank_transactions.record_transaction(
        recipient,
        "Transfer In",
        amount
    )

    return (
        True,
        f"Transfer successful to "
        f"{recipient.account_name}."
    )


# ============================================================
# BILLS PAYMENT
# ============================================================

def pay_bill(
    account,
    biller,
    reference_number,
    amount,
    pin
):

    reference_number = (
        reference_number.strip()
    )

    pin = pin.strip()

    if biller == "":

        return (
            False,
            "Please select a biller."
        )

    if reference_number == "":

        return (
            False,
            "Please enter a reference number."
        )

    if amount <= 0:

        return (
            False,
            "Payment amount must be greater than zero."
        )

    if not account.verify_pin(pin):

        return (
            False,
            "Incorrect PIN."
        )

    if amount > account.check_balance():

        return (
            False,
            "Insufficient balance."
        )

    allowed, message = check_guard(
        account,
        amount
    )

    if not allowed:

        return False, message

    success = account.withdraw(
        amount
    )

    if not success:

        return (
            False,
            "Bill payment could not be completed."
        )

    mancera_bank_storage.update_account(
        account
    )

    mancera_bank_transactions.record_transaction(
        account,
        f"Bill Payment - {biller}",
        amount
    )

    return (
        True,
        f"{biller} payment successful. "
        f"Reference: {reference_number}"
    )


# ============================================================
# SAVINGS GOAL OBJECT
# ============================================================

class SavingsGoal:

    def __init__(
        self,
        account_number,
        goal_name,
        target,
        saved=0
    ):

        self.account_number = (
            account_number
        )

        self.goal_name = (
            goal_name
        )

        self.target = float(
            target
        )

        self.saved = float(
            saved
        )


    def get_remaining(self):

        remaining = (
            self.target
            - self.saved
        )

        return max(
            remaining,
            0
        )


    def get_progress(self):

        if self.target <= 0:
            return 0

        percentage = (
            self.saved
            / self.target
        ) * 100

        return min(
            percentage,
            100
        )


    def is_complete(self):

        return (
            self.saved
            >= self.target
        )


    def add_savings(self, amount):

        if amount <= 0:
            return False

        if (
            self.saved + amount
            > self.target
        ):
            return False

        self.saved += amount

        return True


    def to_dict(self):

        return {
            "account_number":
                self.account_number,

            "goal_name":
                self.goal_name,

            "target":
                self.target,

            "saved":
                self.saved
        }


    @classmethod
    def from_dict(
        cls,
        data
    ):

        return cls(
            data[
                "account_number"
            ],
            data[
                "goal_name"
            ],
            data[
                "target"
            ],
            data.get(
                "saved",
                0
            )
        )


# ============================================================
# SAVINGS GOAL FILE FUNCTIONS
# ============================================================

def load_goals():

    return read_json_file(
        GOALS_FILE,
        {}
    )


def save_goals(goals):

    save_json_file(
        GOALS_FILE,
        goals
    )


def get_savings_goal(
    account_number
):

    goals = load_goals()

    goal_data = goals.get(
        account_number
    )

    if goal_data is None:

        return None

    return SavingsGoal.from_dict(
        goal_data
    )


def create_savings_goal(
    account,
    goal_name,
    target
):

    goal_name = (
        goal_name.strip()
    )

    if goal_name == "":

        return (
            False,
            "Please enter a goal name."
        )

    if target <= 0:

        return (
            False,
            "Target amount must be greater than zero."
        )

    goals = load_goals()

    existing = goals.get(
        account.account_number
    )

    if existing is not None:

        existing_goal = (
            SavingsGoal
            .from_dict(
                existing
            )
        )

        if not existing_goal.is_complete():

            return (
                False,
                "You already have an active savings goal."
            )

    goal = SavingsGoal(
        account.account_number,
        goal_name,
        target
    )

    goals[
        account.account_number
    ] = goal.to_dict()

    save_goals(
        goals
    )

    return (
        True,
        "Savings goal created successfully."
    )


def contribute_to_goal(
    account,
    amount,
    pin
):

    pin = pin.strip()

    if amount <= 0:

        return (
            False,
            "Contribution must be greater than zero."
        )

    if not account.verify_pin(pin):

        return (
            False,
            "Incorrect PIN."
        )

    goal = get_savings_goal(
        account.account_number
    )

    if goal is None:

        return (
            False,
            "You do not have an active savings goal."
        )

    if goal.is_complete():

        return (
            False,
            "Your savings goal is already complete."
        )

    if amount > goal.get_remaining():

        return (
            False,
            "Contribution exceeds the remaining goal amount."
        )

    if amount > account.check_balance():

        return (
            False,
            "Insufficient account balance."
        )

    allowed, message = check_guard(
        account,
        amount
    )

    if not allowed:

        return False, message

    success = account.withdraw(
        amount
    )

    if not success:

        return (
            False,
            "Contribution could not be completed."
        )

    goal.add_savings(
        amount
    )

    goals = load_goals()

    goals[
        account.account_number
    ] = goal.to_dict()

    save_goals(
        goals
    )

    mancera_bank_storage.update_account(
        account
    )

    mancera_bank_transactions.record_transaction(
        account,
        "Savings Goal Contribution",
        amount
    )

    return (
        True,
        "Savings contribution successful."
    )