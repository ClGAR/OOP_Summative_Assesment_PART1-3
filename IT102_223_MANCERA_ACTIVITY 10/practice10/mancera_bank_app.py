"""
######### Learning Signature #########
Programmed by: Roger Mancera
Date Submitted: September 14, 2026

Program Description: This program is a professional-looking Streamlit
digital banking application. It allows users to register and log in,
check their account dashboard, deposit money, withdraw money, review
transaction history, and analyze account activity.

Reflection: I learned how to improve a Streamlit interface using a
consistent layout, colors, icons, navigation, dashboard cards, and
clearer information displays while preserving the application's
existing OOP and modular structure.

AI Usage
[ ] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[X] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""


import streamlit as st


import mancera_bank_auth
import mancera_bank_storage
import mancera_bank_transactions
import mancera_bank_analysis
import mancera_bank_utils
import mancera_bank_services


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mancera Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM UI STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main page container */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f2747;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white;
    }

    /* Header */
    .bank-header {
        background: linear-gradient(
            135deg,
            #0f2747,
            #194f8a
        );

        color: white;
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 24px;

        box-shadow:
            0px 8px 22px
            rgba(15, 39, 71, 0.15);
    }

    .bank-header h1 {
        color: white;
        margin: 0;
        font-size: 34px;
        font-weight: 700;
    }

    .bank-header p {
        margin-top: 7px;
        margin-bottom: 0;
        color: #dbeafe;
        font-size: 15px;
    }

    /* Cards */
    .bank-card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;

        box-shadow:
            0px 4px 14px
            rgba(0, 0, 0, 0.04);
    }

    /* Streamlit metrics */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 15px;

        box-shadow:
            0px 3px 12px
            rgba(0, 0, 0, 0.04);
    }

    /* Buttons */
    div.stButton > button {
        min-height: 45px;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Inputs */
    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #172033;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "account" not in st.session_state:
    st.session_state.account = None


# ============================================================
# MAIN BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="bank-header">
        <h1>🏦 MANCERA BANK</h1>
        <p>
            Secure • Simple • Smart Digital Banking
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN / REGISTRATION
# ============================================================

if not st.session_state.logged_in:

    st.write(
        "Access your account or create a new digital bank account."
    )

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader(
            "Welcome Back"
        )

        st.caption(
            "Enter your account information to continue."
        )

        account_number = st.text_input(
            "Account Number",
            placeholder="Enter account number",
            key="login_account"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            placeholder="Enter your 4-digit PIN",
            key="login_pin"
        )

        if st.button(
            "🔐 Login to Account",
            type="primary",
            use_container_width=True
        ):

            account, message = (
                mancera_bank_auth.login_account(
                    account_number,
                    pin
                )
            )

            if account is not None:

                st.session_state.logged_in = True
                st.session_state.account = account

                st.success(
                    message
                )

                st.rerun()

            else:

                st.error(
                    message
                )


    # ========================================================
    # REGISTRATION
    # ========================================================

    with register_tab:

        st.subheader(
            "Create Your Mancera Bank Account"
        )

        st.caption(
            "Complete the form below to register."
        )

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Full Name",
                placeholder="Juan Dela Cruz",
                key="register_name"
            )

            account_number = st.text_input(
                "Account Number",
                placeholder="Example: 100001",
                key="register_account"
            )

            account_type = st.selectbox(
                "Account Type",
                [
                    "Savings Account",
                    "Student Account"
                ]
            )


        with col2:

            pin = st.text_input(
                "Create 4-Digit PIN",
                type="password",
                placeholder="4 digits",
                key="register_pin"
            )

            confirm_pin = st.text_input(
                "Confirm PIN",
                type="password",
                placeholder="Repeat PIN",
                key="register_confirm_pin"
            )

            starting_balance = st.number_input(
                "Starting Balance",
                min_value=0.0,
                step=100.0,
                format="%.2f"
            )


        if st.button(
            "✨ Create Bank Account",
            type="primary",
            use_container_width=True
        ):

            account, message = (
                mancera_bank_auth.register_account(
                    name,
                    account_number,
                    pin,
                    confirm_pin,
                    account_type,
                    starting_balance
                )
            )

            if account is not None:

                st.success(
                    message
                )

                st.info(
                    "Your account has been created successfully. "
                    "Open the Login tab and sign in using your "
                    "account number and PIN."
                )

            else:

                st.error(
                    message
                )


# ============================================================
# LOGGED-IN BANKING APPLICATION
# ============================================================

else:

    account = st.session_state.account


    # ========================================================
    # SIDEBAR ACCOUNT INFORMATION
    # ========================================================

    st.sidebar.markdown(
        "## 🏦 MANCERA BANK"
    )

    st.sidebar.caption(
        "DIGITAL BANKING"
    )

    st.sidebar.divider()

    st.sidebar.markdown(
        f"### 👤 {account.account_name}"
    )

    st.sidebar.caption(
        account.get_account_type()
    )

    st.sidebar.write(
        f"💳 **Account:** "
        f"{account.account_number}"
    )

    st.sidebar.write(
        "💰 **Balance:** "
        + mancera_bank_utils.format_currency(
            account.check_balance()
        )
    )

    st.sidebar.divider()


    # ========================================================
    # NAVIGATION
    # ========================================================

    menu = st.sidebar.radio(
        "BANKING MENU",
        [
            "🏠 Dashboard",
            "➕ Deposit",
            "➖ Withdraw",
            "📜 Transaction History",
            "📊 Transaction Analysis"
        ]
    )


    st.sidebar.divider()


    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.account = None

        st.rerun()


    # ========================================================
    # DASHBOARD
    # ========================================================

    if menu == "🏠 Dashboard":

        st.header(
            f"Welcome back, {account.account_name} 👋"
        )

        st.caption(
            "Here is an overview of your bank account."
        )

        st.divider()


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "💰 Available Balance",
            mancera_bank_utils.format_currency(
                account.check_balance()
            )
        )


        col2.metric(
            "🏦 Account Type",
            account.get_account_type()
        )


        col3.metric(
            "💳 Account Number",
            account.account_number
        )


        st.divider()


        st.subheader(
            "Quick Banking"
        )

        left, right = st.columns(2)


        with left:

            st.info(
                "➕ **Deposit Money**\n\n"
                "Add funds securely to your account "
                "using the Deposit menu."
            )


        with right:

            st.info(
                "➖ **Withdraw Money**\n\n"
                "Withdraw money while maintaining "
                "a valid available balance."
            )


        st.subheader(
            "Account Security"
        )

        st.success(
            "🔒 Your account is protected using "
            "PIN verification and account authentication."
        )


    # ========================================================
    # DEPOSIT
    # ========================================================

    elif menu == "➕ Deposit":

        st.header(
            "➕ Deposit Money"
        )

        st.caption(
            "Add funds securely to your bank account."
        )


        col1, col2 = st.columns(
            [1, 2]
        )


        with col1:

            st.metric(
                "Current Balance",
                mancera_bank_utils.format_currency(
                    account.check_balance()
                )
            )


        with col2:

            st.info(
                "Enter the amount you want to deposit. "
                "Only positive amounts are accepted."
            )


        st.divider()


        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "💰 Confirm Deposit",
            type="primary",
            use_container_width=True
        ):

            if not mancera_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid deposit amount."
                )

            else:

                success = account.deposit(
                    amount
                )

                if success:

                    mancera_bank_storage.update_account(
                        account
                    )

                    mancera_bank_transactions.record_transaction(
                        account,
                        "Deposit",
                        amount
                    )

                    st.success(
                        "✅ Deposit successful."
                    )

                    st.metric(
                        "Updated Balance",
                        mancera_bank_utils.format_currency(
                            account.check_balance()
                        )
                    )

                else:

                    st.error(
                        "Deposit could not be completed."
                    )


    # ========================================================
    # WITHDRAW
    # ========================================================

    elif menu == "➖ Withdraw":

        st.header(
            "➖ Withdraw Money"
        )

        st.caption(
            "Withdraw funds from your available balance."
        )


        col1, col2 = st.columns(
            [1, 2]
        )


        with col1:

            st.metric(
                "Available Balance",
                mancera_bank_utils.format_currency(
                    account.check_balance()
                )
            )


        with col2:

            st.warning(
                "The withdrawal amount cannot exceed "
                "your current account balance."
            )


        st.divider()


        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "💵 Confirm Withdrawal",
            type="primary",
            use_container_width=True
        ):

            if not mancera_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid withdrawal amount."
                )


            elif amount > account.check_balance():

                st.error(
                    "Insufficient balance."
                )


            else:

                success = account.withdraw(
                    amount
                )

                if success:

                    mancera_bank_storage.update_account(
                        account
                    )

                    mancera_bank_transactions.record_transaction(
                        account,
                        "Withdraw",
                        amount
                    )

                    st.success(
                        "✅ Withdrawal successful."
                    )

                    st.metric(
                        "Updated Balance",
                        mancera_bank_utils.format_currency(
                            account.check_balance()
                        )
                    )

                else:

                    st.error(
                        "Withdrawal could not be completed."
                    )


    # ========================================================
    # TRANSACTION HISTORY
    # ========================================================

    elif menu == "📜 Transaction History":

        st.header(
            "📜 Transaction History"
        )

        st.caption(
            "Review the transactions recorded for your account."
        )


        transactions = (
            mancera_bank_transactions
            .get_transactions()
        )


        # Show only transactions belonging
        # to the currently logged-in account.

        transactions = [
            transaction
            for transaction in transactions
            if transaction.get(
                "account_number"
            ) == account.account_number
        ]


        if transactions:

            st.metric(
                "Recorded Transactions",
                len(transactions)
            )

            st.divider()


            display_data = []


            for transaction in transactions:

                display_data.append(
                    {

                        "Timestamp":
                            transaction.get(
                                "timestamp",
                                "N/A"
                            ),

                        "Transaction":
                            transaction.get(
                                "transaction",
                                "N/A"
                            ),

                        "Amount":
                            mancera_bank_utils
                            .format_currency(
                                transaction.get(
                                    "amount",
                                    0
                                )
                            ),

                        "Balance After":
                            mancera_bank_utils
                            .format_currency(
                                transaction.get(
                                    "balance_after",
                                    0
                                )
                            )
                    }
                )


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "📭 No transaction history available yet."
            )


    # ========================================================
    # TRANSACTION ANALYSIS
    # ========================================================

    elif menu == "📊 Transaction Analysis":

        st.header(
            "📊 Transaction Analysis"
        )

        st.caption(
            "Understand the activity and money flow "
            "inside your account."
        )


        result = (
            mancera_bank_analysis
            .analyze_transactions(
                account.account_number
            )
        )


        # ====================================================
        # TRANSACTION SUMMARY
        # ====================================================

        st.subheader(
            "📋 1. Transaction Summary"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Transactions",
            result[
                "total_transactions"
            ]
        )


        col2.metric(
            "Deposits",
            result[
                "deposits"
            ]
        )


        col3.metric(
            "Withdrawals",
            result[
                "withdrawals"
            ]
        )


        st.divider()


        # ====================================================
        # MONEY FLOW
        # ====================================================

        st.subheader(
            "💵 2. Money Flow Analysis"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Deposited",
            mancera_bank_utils
            .format_currency(
                result[
                    "total_deposited"
                ]
            )
        )


        col2.metric(
            "Total Withdrawn",
            mancera_bank_utils
            .format_currency(
                result[
                    "total_withdrawn"
                ]
            )
        )


        col3.metric(
            "Net Cash Flow",
            mancera_bank_utils
            .format_currency(
                result[
                    "net_cash_flow"
                ]
            )
        )


        st.divider()


        # ====================================================
        # ACCOUNT ACTIVITY
        # ====================================================

        st.subheader(
            "📈 3. Account Activity Analysis"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Largest Transaction",
            mancera_bank_utils
            .format_currency(
                result[
                    "largest_transaction"
                ]
            )
        )


        col2.metric(
            "Average Transaction",
            mancera_bank_utils
            .format_currency(
                result[
                    "average_transaction"
                ]
            )
        )


        col3.metric(
            "Latest Transaction",
            result[
                "latest_transaction"
            ]
        )


        st.info(
            "🕒 Latest Activity: "
            f"{result['latest_timestamp']}"
        )