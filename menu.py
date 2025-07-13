from pathlib import Path
import json
import random
import string
import streamlit as st

class Bank:
    __database = "data.json"
    data = []

    # Initialize data from JSON file
    try:
        if Path(__database).exists():
            with open(__database) as fs:
                data = json.load(fs)
    except Exception as err:
        print(f"An error occurred: {err}")

    @classmethod
    def Update_data(cls):
        with open(cls.__database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def Generate_Account(cls):
        alpha = random.choices(string.ascii_uppercase, k=4)
        numbers = random.choices(string.digits, k=8)
        account_no = alpha + numbers
        random.shuffle(account_no)
        return "".join(account_no)

    def create_user(self, name, email, age, phone_number, pin):
        if age < 18:
            return "You must be at least 18 years old to create an account."
        if len(str(phone_number)) != 10 or len(str(pin)) != 4:
            return "Invalid phone number or PIN. Please try again."

        account_no = Bank.Generate_Account()
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "phone_number": phone_number,
            "pin": pin,
            "AccountNo": account_no,
            "balance": 0
        }
        Bank.data.append(user_info)
        Bank.Update_data()
        return f"Account created successfully! Your account number is: {account_no}"

    def deposit_money(self, account_no, pin, amount):
        user_data = [i for i in Bank.data if i.get("AccountNo") == account_no and i.get("pin") == pin]
        if not user_data:
            return "Account not found or invalid credentials."
        if amount <= 0:
            return "Deposit amount must be greater than 0."
        if amount > 10000:
            return "You cannot deposit more than 10,000 at once."

        user_data[0]["balance"] += amount
        Bank.Update_data()
        return f"Deposit successful! Your new balance is: {user_data[0]['balance']}"

    def withdraw_money(self, account_no, pin, amount):
        user_data = [i for i in Bank.data if i.get("AccountNo") == account_no and i.get("pin") == pin]
        if not user_data:
            return "Account not found or invalid credentials."
        if amount <= 0:
            return "Withdrawal amount must be greater than 0."
        if user_data[0]["balance"] < amount:
            return "Insufficient balance."

        user_data[0]["balance"] -= amount
        Bank.Update_data()
        return f"Withdrawal successful! Your new balance is: {user_data[0]['balance']}"

    def view_details(self, account_no, pin):
        user_data = [i for i in Bank.data if i.get("AccountNo") == account_no and i.get("pin") == pin]
        if not user_data:
            return "Account not found or invalid credentials."
        return user_data[0]

    def delete_user(self, account_no, pin):
        user_data = [i for i in Bank.data if i.get("AccountNo") == account_no and i.get("pin") == pin]
        if not user_data:
            return "Account not found or invalid credentials."
        
        Bank.data.remove(user_data[0])
        Bank.Update_data()
        return "Account deleted successfully."


# Streamlit App
st.title("Bank Management System")
bank = Bank()

menu = ["Create Account", "Deposit Money", "Withdraw Money", "View Details", "Delete User"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")
    age = st.number_input("Enter Your Age", min_value=0, step=1)
    phone_number = st.text_input("Enter Your Phone Number")
    pin = st.text_input("Set Your PIN", type="password")

    if st.button("Create Account"):
        if name and email and phone_number and pin:
            response = bank.create_user(name, email, age, int(phone_number), int(pin))
            st.success(response)
        else:
            st.error("All fields are required!")

elif choice == "Deposit Money":
    st.subheader("Deposit Money")
    account_no = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your PIN", type="password")
    amount = st.number_input("Enter Amount to Deposit", min_value=0, step=1)

    if st.button("Deposit"):
        response = bank.deposit_money(account_no, int(pin), int(amount))
        if "successful" in response:
            st.success(response)
        else:
            st.error(response)

elif choice == "Withdraw Money":
    st.subheader("Withdraw Money")
    account_no = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your PIN", type="password")
    amount = st.number_input("Enter Amount to Withdraw", min_value=0, step=1)

    if st.button("Withdraw"):
        response = bank.withdraw_money(account_no, int(pin), int(amount))
        if "successful" in response:
            st.success(response)
        else:
            st.error(response)

elif choice == "View Details":
    st.subheader("View Account Details")
    account_no = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your PIN", type="password")

    if st.button("View"):
        response = bank.view_details(account_no, int(pin))
        if isinstance(response, dict):
            st.json(response)
        else:
            st.error(response)

elif choice == "Delete User":
    st.subheader("Delete Your Account")
    account_no = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your PIN", type="password")

    if st.button("Delete"):
        response = bank.delete_user(account_no, int(pin))
        if "successfully" in response:
            st.success(response)
        else:
            st.error(response)

