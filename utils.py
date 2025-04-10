from .database import db
from .models import Expense, Budget, User
from sqlalchemy.sql import func
from .mailer import send_alert

def calculate_monthly_expense(user_id, month):
    expenses = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label("total_spent")
    ).filter(
        Expense.user_id == user_id,
        func.date_format(Expense.date, "%Y-%m") == month
    ).group_by(Expense.category).all()

    return {category: float(total) for category, total in expenses}

def evaluate_budget_alerts(user_id, month):
    try:
        user = User.query.get(user_id)
        category_expenses = calculate_monthly_expense(user_id, month)
        user_budgets = Budget.query.filter_by(user_id=user_id, month=month).all()

        alert_messages = []

        for budget in user_budgets:
            spent = category_expenses.get(budget.category, 0)
            if spent >= budget.limit:
                message = f"❌ Limit exceeded in {budget.category}: Spent {spent}, Limit {budget.limit}"
            elif spent >= 0.9 * budget.limit:
                message = f"⚠️ 90% of budget used in {budget.category}: Spent {spent}, Limit {budget.limit}"
            else:
                continue

            alert_messages.append(message)
            try:
                send_alert(user.email, "Budget Notification", message)
            except Exception as email_error:
                print(f"[Email Sending Failed] {email_error}")

        return alert_messages

    except Exception as error:
        print(f"[Alert Evaluation Error] {error}")
        return [f"Internal error: {str(error)}"]
