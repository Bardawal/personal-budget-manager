from flask import Blueprint, request, jsonify
from .database import db
from .models import User, Budget, Expense, Group, GroupMember, SharedExpense
from .utils import get_monthly_spending, check_alerts
from datetime import datetime

# Define blueprint for routing
api = Blueprint('api', __name__)

@api.route("/")
def index():
    return "Expense Tracker API is active!"

# User registration endpoint
@api.route('/user', methods=['POST'])
def register_user():
    info = request.get_json()
    new_user = User(name=info['name'], email=info['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({ "id": new_user.id, "name": new_user.name })

# Set monthly budget for a category
@api.route('/budget', methods=['POST'])
def assign_budget():
    data = request.get_json()
    new_budget = Budget(
        user_id=data['user_id'],
        category=data['category'],
        month=data['month'],
        limit=data['limit']
    )
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({ "status": "Budget recorded successfully." })

# Add a personal expense
@api.route('/expense', methods=['POST'])
def log_expense():
    entry = request.get_json()
    expense = Expense(
        user_id=entry['user_id'],
        category=entry['category'],
        amount=entry['amount']
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({ "status": "Expense logged." })

# Generate a monthly spending report
@api.route('/report/<int:user_id>/<month>')
def monthly_report(user_id, month):
    summary = get_monthly_spending(user_id, month)
    return jsonify(summary)

# Check for spending alerts
@api.route('/alerts/<int:user_id>/<month>')
def spending_alerts(user_id, month):
    alerts = check_alerts(user_id, month)
    return jsonify(alerts)

# Group management: create group
@api.route('/group', methods=['POST'])
def new_group():
    data = request.get_json()
    group = Group(name=data['name'])
    db.session.add(group)
    db.session.commit()
    return jsonify({ "group_id": group.id })

# Add user to a group
@api.route('/group/member', methods=['POST'])
def include_member():
    member = GroupMember(**request.get_json())
    db.session.add(member)
    db.session.commit()
    return jsonify({ "status": "Member added to group." })

# Add a shared group expense
@api.route('/group/expense', methods=['POST'])
def record_shared_expense():
    info = request.get_json()
    shared = SharedExpense(
        group_id=info['group_id'],
        paid_by=info['paid_by'],
        amount=info['amount'],
        description=info['description']
    )
    db.session.add(shared)
    db.session.commit()
    return jsonify({ "status": "Group expense recorded." })

# Calculate settlements for group members
@api.route('/group/settle/<int:group_id>')
def calculate_settlement(group_id):
    members = GroupMember.query.filter_by(group_id=group_id).all()
    expenses = SharedExpense.query.filter_by(group_id=group_id).all()

    balance_sheet = {m.user_id: 0 for m in members}

    for exp in expenses:
        per_person = exp.amount / len(members)
        for member in members:
            if member.user_id == exp.paid_by:
                balance_sheet[member.user_id] += exp.amount - per_person
            else:
                balance_sheet[member.user_id] -= per_person

    result = { str(uid): round(amount, 2) for uid, amount in balance_sheet.items() }
    return jsonify(result)
