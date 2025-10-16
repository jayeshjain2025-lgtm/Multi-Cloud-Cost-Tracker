# AWS Cost Tracking Module
# This module retrieves and calculates AWS costs using the Cost Explorer API

import boto3, datetime
class AWS_Cost:
    def __init__(self):
        self.response = self.get_aws_cost()

    def get_aws_cost(self):
        try:
            client = boto3.client('ce', region_name = 'us-east-1')

            # Defining the dates form the first of the current month to today
            
            end = datetime.datetime.today() 
            start = end.replace(day=1)

            response = client.get_cost_and_usage(
                TimePeriod = {'Start': str(start.date()), 'End' : str(end.date())},
                Granularity='DAILY',
                Metrics = ['UnblendedCost'],
                GroupBy = [{'Type' : 'DIMENSION', 'Key' : 'SERVICE'}]
            )
            return (response['ResultsByTime'])
        
        except Exception as e:
            print(f"Error fetching AWS cost data: {e}")
            return None


    def total(self):

        if self.response is None:
            return "Error: Failed to fetch AWS cost data"

        try:
            cost = 0
            for day_cost in self.response:
                for group in day_cost['Groups']:
                    cost += float(group['Metrics']['UnblendedCost']['Amount'])
            return (f'Total Bill: ${cost:.2f}')
        except Exception as e:
            return f'Error calculating total cost: {e}'    


#Sample Run
a = AWS_Cost()
print(a.response, a.total())
