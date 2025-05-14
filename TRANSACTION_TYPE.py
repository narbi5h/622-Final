#import the necessary libraries
import json
from typing import List, Dict, Any
import pandas as pd

#TRANSACTION_TYPE CLASS

class TRANSACTION_TYPE:
    def __init__(self):
        # Example dataset
        self.data = [
            {'type_id': 1, 'category_name': 'Income'},
            {'type_id': 2, 'category_name': 'Expense'},
            {'type_id': 3, 'category_name': 'Asset'},
        ]

    def LIST_ALL(self):
        """List all transaction types."""
        return self.data

    def UPDATE_NAME(self, type_id, new_name):
        """Update the category_name of a given type_id."""
        for item in self.data:
            if item['type_id'] == type_id:
                item['category_name'] = new_name
                return f"Updated type_id {type_id} to new name '{new_name}'"
        return "Type ID not found"

    def DELETE_TYPE(self, type_id):
        """Delete a transaction type by type_id."""
        for i, item in enumerate(self.data):
            if item['type_id'] == type_id:
                del self.data[i]
                return f"Deleted type_id {type_id}"
        return "Type ID not found"

    def SEARCH(self, keyword):
        """Search for transaction types containing the keyword in category_name."""
        return [item for item in self.data if keyword.lower() in item['category_name'].lower()]

    def ADD(self, type_id, category_name):
        """Add a new transaction type."""
        for item in self.data:
            if item['type_id'] == type_id:
                return f"Type ID {type_id} already exists"
        self.data.append({'type_id': type_id, 'category_name': category_name})
        return f"Added new transaction type with type_id {type_id} and category_name '{category_name}'"

    def GROUP(self):
        """Group transaction types by the first letter of their category_name."""
        grouped = {}
        for item in self.data:
            key = item['category_name'][0].upper()
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        return grouped
