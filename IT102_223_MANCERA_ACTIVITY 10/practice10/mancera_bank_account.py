"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 14, 2026

Program Description: This program defines an abstract BankAccount class
and specialized SavingsAccount and StudentAccount classes. It supports
secure PIN verification, balance checking, deposits, and withdrawals.

Reflection: I learned how the four OOP pillars can work together in one
banking application. Encapsulation protects internal account data,
abstraction defines required behavior, inheritance allows specialized
account classes, and polymorphism allows each account type to provide
its own implementation.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(
        self,
        account_number,
        name,
        pin,
        starting_balance
    ):
        self.account_number = account_number
        self.account_name = name

        # Encapsulation
        self._pin = pin
        self._balance = float(starting_balance)

    # Encapsulation
    def check_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            return False

        self._balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0:
            return False

        if amount > self._balance:
            return False

        self._balance -= amount
        return True

    def verify_pin(self, pin):
        return self._pin == pin

    def get_pin(self):
        return self._pin

    # Controlled method used when restoring saved data.
    # This is better than changing _balance directly
    # from another module.
    def restore_balance(self, balance):
        if balance >= 0:
            self._balance = float(balance)
            return True

        return False

    # Abstraction
    @abstractmethod
    def get_account_type(self):
        pass


# Inheritance
class SavingsAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):
        return "Savings Account"


# Inheritance
class StudentAccount(BankAccount):

    # Polymorphism
    def get_account_type(self):
        return "Student Account"