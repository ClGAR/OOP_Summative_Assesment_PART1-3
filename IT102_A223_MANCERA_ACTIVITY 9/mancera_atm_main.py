"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 13, 2026

Program Description: This program is a web-based ATM application built
with Streamlit. It allows the user to check the account balance, deposit
money, withdraw money, view transaction history, and analyze transactions.

Reflection: I learned how an Account object and separate Python modules
can work together with Streamlit to create a modular web application.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

import streamlit as st

# TODO 1: Import Account class
from mancera_atm_account import Account

# TODO 2: Import balance module
from mancera_atm_balance import check_balance

# TODO 3: Import deposit module
from mancera_atm_deposit import deposit_money

# TODO 4: Import withdraw module
from mancera_atm_withdraw import withdraw_money

# TODO 5: Import history module
from mancera_atm_history import view_history

# TODO 6: Import analysis module
from mancera_atm_analysis import analyze_transactions


# TODO 8: Configure Streamlit page
st.set_page_config(
    page_title="Python ATM",
    page_icon="🏦",
    layout="wide"
)


# TODO 7: Create Account object
#
# Streamlit reruns the Python program whenever
# the user interacts with the page.
# session_state keeps the same Account object
# instead of resetting the balance to P10,000.
if "account" not in st.session_state:
    st.session_state.account = Account(
        "Juan Dela Cruz",
        10000
    )

account = st.session_state.account


# TODO 9: Main title
st.title("🏦 PYTHON ATM")


# TODO 10: Welcome message
st.write(
    f"Welcome, **{account.account_name}**!"
)


# TODO 11: Divider
st.divider()


# TODO 12: Sidebar title
st.sidebar.title("ATM MENU")


# TODO 13: Sidebar radio menu
menu = st.sidebar.radio(
    "Select an ATM operation:",
    [
        "Check Balance",
        "Deposit",
        "Withdraw",
        "View History",
        "Analyze Transactions"
    ]
)


# ==================================================
# CHECK BALANCE
# ==================================================

if menu == "Check Balance":

    st.header("💰 Check Balance")

    balance = check_balance(account)

    st.metric(
        label="Current Balance",
        value=f"₱{balance:,.2f}"
    )

    st.info(
        f"Account Name: {account.account_name}"
    )


# ==================================================
# DEPOSIT
# ==================================================

elif menu == "Deposit":

    st.header("➕ Deposit Money")

    amount = st.number_input(
        "Enter deposit amount:",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    if st.button("Deposit Money"):

        if amount <= 0:

            st.error(
                "Invalid deposit amount."
            )

        else:

            result = deposit_money(
                account,
                amount
            )

            if result:

                st.success(
                    "Deposit successful."
                )

                st.metric(
                    "New Balance",
                    f"₱{account.check_balance():,.2f}"
                )

            else:

                st.error(
                    "Deposit failed."
                )


# ==================================================
# WITHDRAW
# ==================================================

elif menu == "Withdraw":

    st.header("➖ Withdraw Money")

    st.metric(
        "Available Balance",
        f"₱{account.check_balance():,.2f}"
    )

    amount = st.number_input(
        "Enter withdrawal amount:",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    if st.button("Withdraw Money"):

        if amount <= 0:

            st.error(
                "Invalid withdrawal amount."
            )

        elif amount > account.check_balance():

            st.error(
                "Insufficient balance."
            )

        else:

            result = withdraw_money(
                account,
                amount
            )

            if result:

                st.success(
                    "Withdrawal successful."
                )

                st.metric(
                    "New Balance",
                    f"₱{account.check_balance():,.2f}"
                )

            else:

                st.error(
                    "Withdrawal failed."
                )


# ==================================================
# VIEW HISTORY
# ==================================================

elif menu == "View History":

    st.header("📜 Transaction History")

    history = view_history()

    if len(history) == 0:

        st.info(
            "No transaction history available."
        )

    else:

        clean_history = []

        for line in history:

            line = line.strip()

            if line:
                clean_history.append(line)

        st.dataframe(
            {
                "Transaction History": clean_history
            },
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# ANALYZE TRANSACTIONS
# ==================================================

elif menu == "Analyze Transactions":

    st.header("📊 Transaction Analysis")

    data = analyze_transactions()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Transactions",
            data["total_transactions"]
        )

        st.metric(
            "Deposits",
            data["deposits"]
        )

        st.metric(
            "Withdrawals",
            data["withdrawals"]
        )

    with col2:

        st.metric(
            "Total Deposited",
            f"₱{data['total_deposited']:,.2f}"
        )

        st.metric(
            "Total Withdrawn",
            f"₱{data['total_withdrawn']:,.2f}"
        )

        st.metric(
            "Average Transaction",
            f"₱{data['average_transaction']:,.2f}"
        )

    with col3:

        st.metric(
            "Largest Transaction",
            f"₱{data['largest_transaction']:,.2f}"
        )

        st.metric(
            "Latest Transaction",
            data["latest_transaction"]
        )

        st.metric(
            "Latest Activity",
            data["latest_timestamp"]
        )