"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program reads transaction records from
transactions.txt and returns the transaction lines to the main
Streamlit application.

Reflection: I learned how a separate module can safely read a text
file and return its contents without displaying them directly.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""


def view_history():
    try:
        with open("transactions.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        return lines

    except FileNotFoundError:
        return []