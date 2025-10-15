from flask import jsonify
import boto3
from datetime import datetime, timedelta

def get_aws_costs():
    """
    Fetch AWS cost data from Cost Explorer API
    """
    try:
        client = boto3.client('ce', region_name='us-east-1')
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        
        costs = []
        for result in response['ResultsByTime']:
            costs.append({
                'date': result['TimePeriod']['Start'],
                'cost': float(result['Total']['UnblendedCost']['Amount'])
            })
        
        return jsonify({'provider': 'AWS', 'costs': costs})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
