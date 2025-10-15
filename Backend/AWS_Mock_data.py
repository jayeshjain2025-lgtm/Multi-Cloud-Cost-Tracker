from flask import jsonify
from datetime import datetime, timedelta
import random

def get_mock_aws_costs():
    """
    Generate mock AWS cost data for testing
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    costs = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate random cost between $50 and $500
        daily_cost = round(random.uniform(50, 500), 2)
        
        costs.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'cost': daily_cost,
            'provider': 'AWS'
        })
        
        current_date += timedelta(days=1)
    
    return jsonify({
        'provider': 'AWS',
        'costs': costs,
        'total': sum(item['cost'] for item in costs),
        'period': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
    })
