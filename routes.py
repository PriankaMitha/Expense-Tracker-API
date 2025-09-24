from flask import Blueprint, request, jsonify
from models import db, Expense
from sqlalchemy import func

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.route("/add", methods=["POST"])
def add_expense():
    data = request.json
    added_expenses = []   # collect all inserted expenses

    if isinstance(data, list):  # multiple expenses
        for item in data:
            new_expense = Expense(
                description=item['description'],
                amount=float(item['amount']),
                category=item['category']
            )
            db.session.add(new_expense)
            added_expenses.append(new_expense)  # add to list
    else:                         # single expense
        new_expense = Expense(
            description=data['description'],
            amount=float(data['amount']),
            category=data['category']
        )
        db.session.add(new_expense)
        added_expenses.append(new_expense)

    db.session.commit()

    return jsonify({
        "message": "Expense(s) added!",
        "expenses": [exp.to_dict() for exp in added_expenses]
    })


@expenses_bp.route("/expenses",methods=["GET"])
def list_expenses():
    expenses =Expense.query.all()
    return jsonify([e.to_dict() for e in expenses])

@expenses_bp.route("/report", methods=["GET"])
def report():
    expenses = Expense.query.all()
    summary={}

    for e in expenses:
        summary[e.category] = summary.get(e.category,0)+e.amount
    return jsonify(summary)

@expenses_bp.route("/update/<int:id>",methods=["PUT"])
def update_expense(id):
    data = request.json
    expense = Expense.query.get_or_404(id)

    expense.description = data.get('description',expense.description)
    expense.amount = float(data.get('amount',expense.amount))
    expense.category = data.get('category',expense.category)
    
    db.session.commit()
    return jsonify({
        "message":"Expense updated !",
        "expense" : expense.to_dict()
    })

@expenses_bp.route("/delete/<int:id>",methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message":"Expense Deleted!"})

@expenses_bp.route("/total",methods=["GET"])
def get_total_expense():
    total = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    return jsonify({'Total Expenses':total})

@expenses_bp.route("/expense/<int:id>",methods=["GET"])
def get_expense_by_id(id):
    expense = Expense.query.get_or_404(id)
    return jsonify({
        "message":"Expense Found",
        "expense" : expense.to_dict()
    })

@expenses_bp.route("/expense/category/<string:category>", methods=["GET"])
def get_expense_by_category(category):
    expenses = Expense.query.filter(func.lower(Expense.category) == category.lower()).all()

    if not expenses :
        return jsonify({
        "message":f"No expenses found in the category '{category}'"
        }), 404

    return jsonify([e.to_dict() for e in expenses])
