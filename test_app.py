import unittest
import json
from app import app,db
from models import Expense

class ExpenseTrackerTestCases(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] =True
        # Use in-memory SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # Start the application context
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # Pop the context
        self.app_context.pop()
    

    def testAddExpense(self):
        response = self.app.post('/add',json={
            "description" : "Test Expense",
            "amount" : 500,
            "category" : "Test"
        })
        self.assertEqual(response.status_code,200)
        data = json.loads(response.data)
        self.assertIn('expenses',data)
        self.assertEqual(data['expenses'][0]['description'],"Test Expense")

    def test_get_total_expense(self):
    # Add an expense first
        self.app.post('/add', json={
            "description": "Test Expense",
            "amount": 500,
            "category": "Test"
        })
        response = self.app.get('/total')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['Total Expenses'], 500)

    def test_get_all_expenses(self):
        # Add a couple of expenses first
        self.app.post('/add', json={"description": "Exp1", "amount": 100, "category": "Food"})
        self.app.post('/add', json={"description": "Exp2", "amount": 200, "category": "Bills"})
    
        response = self.app.get('/expenses')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
    
        # Check if we got 2 expenses
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['description'], "Exp1")
        self.assertEqual(data[1]['description'], "Exp2")

    def test_get_expense_by_id(self):
        # Add an expense
        post_resp = self.app.post('/add', json={"description": "Exp1", "amount": 100, "category": "Food"})
        exp_id = json.loads(post_resp.data)['expenses'][0]['id']
    
        # Get by ID
        response = self.app.get(f'/expense/{exp_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['expense']['description'], "Exp1")
        self.assertEqual(data['expense']['amount'], 100)

    def test_get_expenses_by_category(self):
        # Add expenses
        self.app.post('/add', json={"description": "Food1", "amount": 50, "category": "Food"})
        self.app.post('/add', json={"description": "Bill1", "amount": 100, "category": "Bills"})
    
        # Filter by category
        response = self.app.get('/expense/category/Food')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['category'], "Food")

    def test_update_expense(self):
        # Add expense
        post_resp = self.app.post('/add', json={"description": "OldDesc", "amount": 100, "category": "Food"})
        exp_id = json.loads(post_resp.data)['expenses'][0]['id']
    
        # Update it
        response = self.app.put(f'/update/{exp_id}', json={"description": "NewDesc", "amount": 150, "category": "Food"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['expense']['description'], "NewDesc")
        self.assertEqual(data['expense']['amount'], 150)

    def test_delete_expense(self):
        # Add expense
        post_resp = self.app.post('/add', json={"description": "ToDelete", "amount": 100, "category": "Food"})
        exp_id = json.loads(post_resp.data)['expenses'][0]['id']
    
        # Delete it
        response = self.app.delete(f'/delete/{exp_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Expense Deleted!', data['message'])
    
        # Confirm it's really deleted
        get_resp = self.app.get(f'/expenses/{exp_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_report_summary(self):
        # Add multiple expenses in different categories
        self.app.post('/add', json={
            "description": "Electricity Bill",
            "amount": 1000,
            "category": "Bills"
        })
        self.app.post('/add', json={
            "description": "Water Bill",
            "amount": 500,
            "category": "Bills"
        })
        self.app.post('/add', json={
            "description": "Dress",
            "amount": 1500,
            "category": "Clothes"
        })

        # Call the report endpoint
        response = self.app.get('/report')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        # Check that categories exist
        self.assertIn("Bills", data)
        self.assertIn("Clothes", data)

        # Check that amounts are summed correctly
        self.assertEqual(data["Bills"], 1500)     # 1000 + 500
        self.assertEqual(data["Clothes"], 1500)


if __name__ == "__main__":
    unittest.main()