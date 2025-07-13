




from pathlib import Path
import json
import random
import string
import streamlit as st  #yaha se humne streamlit ko bulaya

class Bank:
    __database = "data.json"
    data = []

    try:
        if Path(__database).exists():
            with open(__database) as fs:
                data = json.loads(fs.read())
    except Exception as err:
        print(f"An error occured as {err}")
    
    @classmethod
    def Update_data(cls):
        with open(cls.__database,'w') as fs:
            fs.write(json.dumps(cls.data))
    
    @classmethod
    def Generate_Account(cls):
        alpha = random.choices(string.ascii_letters,k = 4)
        numbers = random.choices(string.digits,k = 8)
        id = alpha + numbers
        random.shuffle(id)
        return "".join(id)
        
    def createuser(self,name,email,age,phonenumber,pin):
        
        info = {
            "name":name,
            "email":email,
            "age":age,
            "phonenumber":phonenumber,
            "pin":pin,
            "AccountNo.":Bank.Generate_Account(),
            "balance":0
        }
        
        if info["age"] < 18:
            print("sorry you can't create an account at this age 💀")
        
        elif (not len(str(info["phonenumber"])) == 10) or (not len(str(info["pin"])) == 4):
            print("invalid input please try again")
        
        else:
            print(f"\n\n\nplease keep your account number safe\n   your account number is:{info['AccountNo.']}")
            Bank.data.append(info)
            Bank.Update_data()
    
    def Deposit_money(self,accountno,pin,amount):
        # for i in Bank.data:
        #     if i["AccountNo."] == AC and i['pin'] == pin:
        #         userdata = i
        #         break
        # else:
        #     print("sorry no data found please recheck your A.C number and pin")
        
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            amount = amount
            if amount <= 0:
                print("your deposit money should not be less than 0")
            elif amount > 10000:
                print("sorry you cannot deposit more that 10000")
            else:
                user_data[0]["balance"] += amount
                Bank.Update_data()
                return f"Done"

    def Withdraw_money(self,accountno,pin,amount):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))
        
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            amount = amount
            if amount <= 0:
                print("your withdrawal money should not be less than 0")
            elif amount > 10000:
                print("sorry you cannot withdraw more that 10000")
            else:
                if user_data[0]["balance"] < amount:
                    print("sorry insufficient balance.")
                else:
                    user_data[0]["balance"] -= amount
                    Bank.Update_data()
                    print("withdrawl successfull.")

    def details(self,accountno,pin):
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]

        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            print("your details are : ")
            for i in user_data[0]:
                st.write(f"{i} --> {user_data[0][i]} ")
    
    def update_details(self):
        AC = input("please tell your account number")
        pin = int(input("please tell your pin"))

        user_data = [i for i in Bank.data if i["AccountNo."] == AC and i["pin"] == pin]

        if user_data == False:
                print("sorry no data found please check your credentials.")
        
        else:
            print("you cannot change the Account No.")
            print("now update your details or skip it by just pressing enter")

            newdata = {
                "name":input("Update your name or press enter to skip"),
                "age":input("update your age or press enter to skip"),
                "email":input("update your email or press enter to skip"),
                "phonenumber":input("update your phonenumber or press enter to skip"),
                "pin":input("update your pin or press enter to skip")
            }
        
            if newdata["name"] == "":
                newdata["name"] = user_data[0]["name"]
            if newdata["age"] == "":
                newdata["age"] = user_data[0]["age"]
            if newdata["email"] == "":
                newdata["email"] = user_data[0]["email"]
            if newdata["phonenumber"] == "":
                newdata["phonenumber"] = user_data[0]["phonenumber"]
            if newdata["pin"] == "":
                newdata["pin"] = user_data[0]["pin"]
            
            newdata["AccountNo."] = user_data[0]["AccountNo."]
            newdata["balance"] = user_data[0]["balance"]

            
            for i in user_data[0]:
                if user_data[0][i] == newdata[i]:
                    continue
                else:
                    if newdata[i].isnumeric():
                        user_data[0][i] = int(newdata[i])
                    else:
                        user_data[0][i] = newdata[i]


            Bank.Update_data()
            print("details updated successfully")

    def delete_user(self,accountno,pin):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if not user_data:
            return "Account not found or invalid credentials"
        else:
            Bank.data.remove(user_data[0])
            Bank.Update_data()
            return "Account Deleted Successfully"


            





st.title("Vijay Malya Bank")#Title Assign aapke website pe
bank = Bank()
menu = ["Create Account","Deposite Money","Withdraw Money","View Details","Delete User"]#List form deni hai
choices = st.sidebar.selectbox("Selcect here",menu)

if choices == "Create Account":
    st.subheader("Create Account")
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email id")
    age = st.number_input("Apna number batao ",min_value=0, step=1)
    phonenumber = st.text_input("Apna phone number batao ")
    pin = st.text_input("Apna pin batao",type="password")
    
    if st.button("Create Account"):
        if name and email and phonenumber and pin:
            response = bank.createuser(name,email,age,int(phonenumber),int(pin))
            st.success("Mubarak Ho aapka account create ho gaya hai")
        else:
            st.error("Hey mahan aatma aapne kuch galat likha hai yaa phir aapne kuch block miss kr diye hai😊")
 

if choices == "Deposite Money":
    st.subheader("Deposite Money")
    accountno = st.text_input("Apna account number bataiye")
    pin = st.text_input("Apna pin batao",type="password")
    amount = st.number_input("Kitna paisa hai batao",min_value=0 , step = 1)

    if st.button("Deposite"):
        result = bank.Deposit_money(accountno,int(pin),int(amount))
        st.success("Mubarak Ho aapka account create ho gaya hai")
    else:
        st.error("Wrong Input")


if choices == "Withdraw Money":
    st.subheader("Withdraw Money")
    accountno = st.text_input("Apna account number bataiye")
    pin = st.text_input("Apna pin batao",type="password")
    amount = st.number_input("Enter home much ammount you want to take",min_value=0,step=1)
    if st.button("Withdraw"):
        response = bank.Withdraw_money(accountno,int(pin),amount)
        st.success("Paisa Khaate se nikal chuka hai")
    else:
        st.error("Paisa nahi nikla bhai aapka")


if choices =="View Details":
    st.subheader("View Details")
    accountno = st.text_input("Apna account number bataiye")
    pin = st.text_input("Apna pin batao",type="password")

    if st.button("View Details"):
        response = bank.details(accountno,int(pin))

if choices == "Delete User":
    st.subheader("Delete user")
    accountno = st.text_input("Apna account number bataiye")
    pin = st.text_input("Apna pin batao",type="password")
    if st.button("Delete user"):
        response = bank.delete_user(accountno,int(pin))
        if "successfullly" in response:
            st.success(response)
        else:
            st.error(response)