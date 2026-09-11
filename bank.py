import random, time, json, sys, qrcode, csv
from datetime import datetime
from reportlab.pdfgen import canvas

accounts = {}
owner_account = {"account_number": "11111", "name": "Owner", "password": "34"}
admin_accounts = {}


def create_account():
    name = input("Enter your full name ")
    password = input("Set a password: ")
    account_number = str(random.randint(100000, 999999))
    while account_number in accounts:
        account_number = str(random.randint(100000, 999999))

    accounts[account_number] = {
        "name": name,
        "password": password,
        "balance": 0.0,
        "transactions": [],
        "locked": False,
        "savings_balance": 0,
        "last_interest_date": datetime.now().strftime("%Y-%m-%d")
    }
    print(f"Account created! Your account number is {account_number}")
    save_accounts()

def access_account():
    account_number = input("Enter account number: ")
    if account_number not in accounts:
        print("Account not found.")
        return
    elif accounts[account_number].get("locked"):
        print("This account is locked. Contact an admin.")
        return
    password = input("Enter password: ")
    if accounts[account_number]["password"] != password:
        print("Incorrect password.")
        return
    
    print(f"Welcome, {accounts[account_number]['name']}!")
    while True:
        print("\n1. Check Balance\n2. Deposit\n3. Withdrawal\n4. Transactions\n5. Transfer\n6. Change Password\n7. Generate account QR code\n8. Export Statement (PDF / CSV)\n9. Savings Menu\n10. Lottery\n11. Logout")
        choice = input("Choose: ")
    
        if choice == "1":
            print(f"Balance: £{accounts[account_number]['balance']:.2f}")
        elif choice == "2":
            amount = float(input("Amount to deposit: £"))
            accounts[account_number]["balance"] += amount
            accounts[account_number]["transactions"].append(f"Deposited £{amount:.2f}")
            save_accounts()
            print(f"Deposited £{amount:.2f}")
        elif choice == "3":
            amount = float(input("Amount to withdraw: £"))
            if amount <= accounts[account_number]["balance"]:
                accounts[account_number]["balance"] -= amount
                accounts[account_number]["transactions"].append(f"Withdrew £{amount:.2f}")
                save_accounts()
                print(f"Withdrew £{amount:.2f}")
            else:
                print("Insufficient funds")
        elif choice == "4":
                    history = accounts[account_number]["transactions"]
                    if not history:
                        print("No transactions yet.")
                    else:
                        print("\n--- Transaction History ---")
                        for entry in history:
                            print(entry)
        elif choice == "5":
            target = input("Enter the recipient's account number: ")
            if target not in accounts:
                print("Target account not found.")
            elif accounts[target].get("locked"):
                print("Recipient account is locked.")
            else:
                try:
                    amount = float(input("Enter amount to transfer: £"))
                    if amount <= 0:
                        print("Invalid amount")
                    elif amount > accounts[account_number]["balance"]:
                        print("Insufficient funds.")
                    else:
                        accounts[account_number]["balance"] -= amount
                        accounts[target]["balance"] += amount
                        accounts[account_number]["transactions"].append(f"Transferred £{amount:.2f} to {target}")
                        accounts[target]["transactions"].append(f"Received £{amount:.2f} from {account_number}")
                        save_accounts()
                        print(f"Transferred £{amount:.2f} to {accounts[target]['name']}")
                except ValueError:
                    print("Invalid amount.")
        elif choice == "6":
            verify = input("Enter current password to proceed: ")
            if verify != accounts[account_number]['password']:
                print("Password incorrect.")
            else:
                new_password = input("Enter new password: ")
                accounts[account_number]['password'] = new_password
                save_accounts()
                print("Password updated successfully")
        elif choice == "7":
            generate_qr(account_number)
        elif choice == "8":
            print("Export in PDF or CSV?")
            which = input().strip().lower()
            if which == "pdf":
                export_account_statement_pdf(account_number)
            elif which == "csv":
                export_account_statement_csv(account_number)
            else:
                print("Invalid option")

        elif choice == "9":
            print("\n--- Savings Menu ---\n1. Create Savings Account\n2. Deposit to Savings\n3. View Savings")
            sub = input("Choose an option: ")

            if sub == "1":
                create_savings_account(account_number)
            elif sub == "2":
                deposit_to_savings(account_number)
            elif sub == "3":
                view_savings(account_number)
            else:
                print("Invalid option.")        
        elif choice == "10":
            lottery(account_number)
        elif choice == "11":
            print("Logging out...")
            break
        
        else:
            print("Invalid option")

def save_accounts():
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_accounts():
    global accounts
    try:
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
    except FileNotFoundError:
        accounts = {}

load_accounts()

def reset_bank():
    text = "Are you sure you want to reset the bank data? This will delete all accounts. (yes/no): "
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    confirm = input()
    if confirm.lower() == "yes":
        accounts.clear()
        with open("accounts.json", "w") as f:
            f.write("{}")
    else:
        print("Reset cancelled.")

def owner_area():
    password = input("Enter owner access code: ")
    if password != owner_account["password"]:
        print("Incorrect access code.")
        return

    print(f"Welcome, {owner_account['name']}!")
    while True:
        print("\n--- Owner Menu ---")
        print("1. View All Accounts")
        print("2. Edit account balance")
        print("3. Delete admin account")
        print("4. Lock an account")
        print("5. Unlock an account")
        print("6. Export Accounts Data")
        print("7. Reset Bank")
        print("8. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\n--- All Accounts ---")
            count = 0
            for acc_num, details in accounts.items():
                locked_status = "Yes" if details.get("locked") else "No"
                print(f"Account: {acc_num} | Name: {details['name']} | Balance: £{details['balance']:.2f} | Password: {details['password']} | Locked: {locked_status}")
                count += 1
            print("--------------------")
            print(f"Total accounts: {count}")
        elif choice == "2":
            edit_account_balance()
        elif choice == "3":
            target = input("Enter the admin account number to delete: ")
            if target in admin_accounts:
                del admin_accounts[target]
                print(f"Admin accounts {target} deleted")
            else:
                print("Admin account not found.")
        elif choice == "4":
            lock_account()
        elif choice == "5":
            unlock_account()
        elif choice == "6":
            export_accounts_report()
        elif choice == "7":
            reset_bank()
        elif choice == "8":
            print("Logging out..")
            break
        else:
            print("Invalid choice.")
    

def create_admin_account():
    name = input("Enter admin name: ")
    password = input("Set admin password: ")
    account_number = str(random.randint(100000, 999999))
    while account_number in admin_accounts:
        account_number = str(random.randint(100000, 999999))

    admin_accounts[account_number] = {
        "name": name,
        "password": password
    }
    print(f"Admin account created! Admin number: {account_number}")

def access_admin_account():
    account_number = input("Enter account number: ")
    if account_number not in admin_accounts:
        print("Admin account not found.")
        return
    password = input("Enter admin password: ")
    if admin_accounts[account_number]["password"] != password:
        print("Incorrect password.")
        return

    print(f"Welcome, {admin_accounts[account_number]['name']}!")
    while True:
        print("\n1. View accounts\n2. Delete an account\n3. Lock an account\n4. Unlock an account\n5. Logout")
        choice = input("Choose: ")

        if choice == "1":
            print("\n--- All Accounts ---")
            count = 0
            for acc_num, details in accounts.items():
                locked_status = "Yes" if details.get("locked") else "No"
                print(f"Account: {acc_num} | Name: {details['name']} | Balance: £{details['balance']:.2f} | Locked: {locked_status}")
                count += 1
            print("--------------------")
            print(f"Total accounts: {count}")
        elif choice == "2":
            target = input("Enter the account number to delete: ")
            if target in accounts:
                del accounts[target]
                print(f"Account {target} deleted")
                save_accounts()
            else:
                print("Account not found.")
        elif choice == "3":
            lock_account()
        elif choice == "4":
            unlock_account()
        elif choice == "5":
            break

def lock_account():
    target = input("Enter the account number to lock: ")
    if target in accounts:
        accounts[target]["locked"] = True
        print(f"Account {target} has been locked.")
        save_accounts()
    else:
        print("Account not found.")

def unlock_account():
    target = input("Enter the account number to unlock: ")
    if target in accounts:
        accounts[target]["locked"] = False
        print(f"Account {target} has been unlocked.")
        save_accounts()
    else:
        print("Account not found.")

def edit_account_balance():
    target = input("Enter the account number to edit: ")
    if target in accounts:
        try:
            new_balance = float(input("Enter the new balance: "))
            accounts[target]["balance"] = new_balance
            print(f"Balance for account {target} updated to £{new_balance}.")
        except ValueError:
            print("Invalid amount.")
    else:
        print("Account not found.")

def lottery(account_number):
    fee = 5
    play = input("Lottery prize = £5000.\nFee = £5. Play? (yes/no)")
    if play.lower() == "yes":
        if account_number not in accounts:
            print("Account not found.")
            return
        if accounts[account_number]["balance"] >= fee:
            accounts[account_number]["balance"] -= fee
            accounts[account_number]["transactions"].append(f"Played lottery fee £{fee:.2f}")
            if random.randint(1, 50) == 1:
                prize = 5000
                accounts[account_number]["balance"] += prize
                accounts[account_number]["transactions"].append(f"Won lottery £{prize:.2f}")
                print(f"You won £{prize}")
            else:
                print("No luck this time..")
            save_accounts()
        else:
            print("Not enough funds.")
    else:
        return

def generate_qr(account_number):
    acc = accounts[account_number]
    data = f"Account: {account_number}\nName: {acc['name']}\nBalance: £{acc['balance']}"
    img = qrcode.make(data)
    filename = f"account_{account_number}_qr.png"
    img.save(filename)
    print(f"QR code saved as {filename}")

def export_accounts_report():
    with open("accounts_report.txt", "w") as f:
        f.write("--- All Accounts ---\n")
        for acc_num, acc_data in accounts.items():
            locked_status = "Yes" if acc_data.get("locked") else "No"
            name = acc_data.get("name", "")
            balance = acc_data.get("balance", 0.0)
            savings = acc_data.get("savings_balance", 0.0)
            password = acc_data.get("password", "")
            f.write(f"Account: {acc_num} | Name: {name} | Balance: {balance:.2f} | Savings Balance: {savings:.2f} | Password: {password} | Locked: {locked_status}\n")
        f.write(f"Total Accounts: {len(accounts)}\n")
    print("Accounts report exported to accounts_report.txt")

def export_account_statement_csv(account_number):
    acc = accounts[account_number]
    filename = f"statement_{account_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(["Account Number", "Name", "Balance", "Timestamp", "Transaction"])
        for t in acc.get("transactions", []):
            writer.writerow([account_number, acc["name"], f"£{acc['balance']:.2f}", datetime.now().isoformat(), t])
    print(f"CSV statement saved as {filename}")

def export_account_statement_pdf(account_number):
    acc = accounts[account_number]
    filename = f"statement_{account_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename)
    y = 800
    c.drawString(50, y, f"Account Statement = {account_number}    Generated: {datetime.now().isoformat()}")
    y -= 30
    c.drawString(50, y, f"Name: {acc['name']}    Balance: £{acc['balance']:.2f}")
    y -= 30
    c.drawString(50, y, "Recent transactions:")
    y -= 20
    for t in acc.get("transactions", [])[-50:]:
        if y < 50:
            c.showPage()
            y = 800
        c.drawString(60, y, f"- {t}")
        y -= 18
    c.save()
    print(f"PDF statement saved as {filename}")

def apply_interest(account_number):
    if account_number not in accounts:
        return
    if "savings_balance" not in accounts[account_number] or "last_interest_date" not in accounts[account_number]:
        return

    daily_rate = 0.02 / 365
    today = datetime.now()
    try:
        last = datetime.strptime(accounts[account_number]["last_interest_date"], "%Y-%m-%d")
    except Exception:
        accounts[account_number]["last_interest_date"] = today.strftime("%Y-%m-%d")
        save_accounts()
        return

    days = (today - last).days

    if days > 0:
        savings_balance = accounts[account_number].get("savings_balance", 0.0)
        interest = savings_balance * daily_rate * days
        accounts[account_number]["savings_balance"] = savings_balance + interest
        accounts[account_number]["last_interest_date"] = today.strftime("%Y-%m-%d")
        save_accounts()
        print(f"Interest added for {days} days: £{interest:.2f}")

def create_savings_account(account_number):
    if "savings_balance" not in accounts[account_number]:
        accounts[account_number]["savings_balance"] = 0.0
        accounts[account_number]["last_interest_date"] = datetime.now().strftime("%Y-%m-%d")
        save_accounts()
        print("Savings account created successfully!")
    else:
        print("Savings account already exists.")

def deposit_to_savings(account_number):
    if account_number not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter amount to transfer from main balance to savings: £"))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0 or amount > accounts[account_number].get("balance", 0):
        print("Invalid amount.")
        return

    if "savings_balance" not in accounts[account_number]:
        accounts[account_number]["savings_balance"] = 0.0
        accounts[account_number]["last_interest_date"] = datetime.now().strftime("%Y-%m-%d")

    accounts[account_number]["balance"] -= amount
    accounts[account_number]["savings_balance"] += amount
    accounts[account_number].setdefault("transactions", []).append(f"Moved £{amount:.2f} to savings")
    save_accounts()
    print(f"£{amount:.2f} moved to savings account.")

def view_savings(account_number):
    apply_interest(account_number)
    savings_balance = accounts[account_number]["savings_balance"]
    print(f"Current Savings Balance: £{savings_balance:.2f}")


while True:
    print("\n--- Welcome to UK Bank ---")
    print("1. Create account\n2. Access account\n3. Exit")
    action = input("Choose: ")

    if action == "1":
        create_account()
    elif action == "2":
        access_account()
    elif action == "3":
        print("Goodbye!")
        break
    elif action == "admin":
        code = input()
        if code == "owner":
            owner_area()
        elif code == "admincreate":
            create_admin_account()
        elif code == "admin":
            access_admin_account()
        else:
            print("Invalid admin code")
    else:
        print("Invalid choice")
