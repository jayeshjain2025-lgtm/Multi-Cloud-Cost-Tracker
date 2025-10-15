# AWS Cost Tracking Module
# This module retrieves and calculates AWS costs using the Cost Explorer API

import boto3, datetime

class AWS_Cost:
    """Class to fetch and calculate AWS costs for the current month"""
    
    def __init__(self):
        """Initialize the class and fetch AWS cost data"""
        self.data = self.get_aws_cost()
    
    def get_aws_cost(self):
        """Retrieve daily AWS costs from the Cost Explorer API
        
        Returns:
            list: Daily cost data grouped by service, or None if error occurs
        """
        try:
            # Initialize AWS Cost Explorer client in us-east-1 region
            client = boto3.client('ce', region_name = 'us-east-1')
            
            # Define the date range from the first day of the current month to today
            end = datetime.datetime.today() 
            start = end.replace(day=1)
            
            # Fetch cost and usage data from AWS Cost Explorer
            response = client.get_cost_and_usage(
                TimePeriod = {'Start': str(start.date()), 'End' : str(end.date())},
                Granularity='DAILY',  # Get daily cost breakdown
                Metrics = ['UnblendedCost'],  # Use unblended cost metric
                GroupBy = [{'Type' : 'DIMENSION', 'Key' : 'SERVICE'}]  # Group costs by AWS service
            )
            
            return (response['ResultsByTime'])
        
        except Exception as e:
            print(f"Error fetching AWS cost data: {e}")
            return None
    
    def total(self):
        """Calculate the total AWS cost for the current month
        
        Returns:
            str: Formatted total bill amount or error message
        """
        if self.data is None:
            return "Error: Failed to fetch AWS cost data"
        
        try:
            cost = 0
            # Iterate through each day's cost data
            for day_cost in self.data:
                # Sum up costs across all service groups for each day
                for group in day_cost['Groups']:
                    cost += float(group['Metrics']['UnblendedCost']['Amount'])
            
            return (f'Total Bill: ${cost:.2f}')
        
        except Exception as e:
            return f'Error calculating total cost: {e}'
    
# Sample usage: Create an instance and display cost data
a = AWS_Cost()
print(a.data, a.total())
