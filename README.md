# Bank Account Management System

A command-line banking simulation built in Python during Year 11

## Features

- **Account management** — create accounts, secure login, change password
- **Core banking** — deposit, withdraw, view balance, transaction history
- **Transfers** — send money between accounts with balance validation
- **Savings accounts** — separate savings balance with automatic daily interest calculation
- **Statement export** — generate account statements as PDF or CSV
- **QR codes** — generate a QR code containing account details
- **Admin & owner roles** — separate privilege levels for account management, locking/unlocking accounts, and viewing all account data
- **Data persistence** — account data is saved to and loaded from a JSON file between sessions

## How it works

The program runs in a loop, offering a main menu to create a new account or log into an existing one. Once logged in, users can access a full menu of banking actions. A separate `admin` command unlocks admin and owner menus with elevated permissions (viewing all accounts, locking/unlocking, editing balances).

## Requirements

```
pip install qrcode reportlab
```

## Running it

```
python bank.py
```

## What I'd do differently now

This was one of my first larger Python projects, written before I'd learned proper object-oriented programming. Looking back, I'd restructure it using classes (an `Account` class, a `Bank` class) instead of one large dictionary and a long list of functions — and I'd use proper password hashing instead of storing passwords in plain text. Revisiting this project has been a useful way to see how much my understanding of code structure has developed since.

## Tech used

Python — `random`, `json`, `csv`, `datetime`, `qrcode`, `reportlab`
