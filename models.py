from .database import db
from datetime import datetime

# User table to store account information
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email_address = db.Column(db.String(100))

# Personal expense tracking
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    category = db.Column(db.String(50))
    cost = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Budget limits by category and month
class SpendingLimit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)
    category = db.Column(db.String(50))
    period = db.Column(db.String(7))  # Format: YYYY-MM
    max_amount = db.Column(db.Float)

# Groups for shared expenses
class ExpenseGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))

# Members participating in groups
class GroupParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_ref = db.Column(db.Integer)
    account_ref = db.Column(db.Integer)

# Shared payments within a group
class GroupTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_ref = db.Column(db.Integer)
    payer_id = db.Column(db.Integer)
    total_amount = db.Column(db.Float)
    note = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
