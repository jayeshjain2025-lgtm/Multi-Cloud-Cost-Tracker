import random

def get_aws_cost():
    # List of AWS services to generate mock cost data for
    services = ["Amazon EC2", "Amazon S3", "AWS Lambda", "CloudWatch"]
    
    # Sample date range for mock data (4 consecutive days)
    dates = ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04"]
    
    # Initialize empty list to store daily cost data
    mock_data = []
    
    # Track total cost across all services and dates
    Total = 0
    
    # Generate cost data for each day (excluding the last date which is used as end boundary)
    for i in range(len(dates)-1):
        # Create daily cost structure with time period
        day_data = {
        'Timeperiod' : {'Start': dates[i], 'End' : dates[i+1]},
        'Groups' : [],
        'Estimated' : False,
        }
        
        # Generate random cost for each service on this day
        for service in services:
            # Generate random cost amount between $0.50 and $5.00
            amount = round(random.uniform(0.5, 5.0), 2)
            
            # Add service cost data in AWS Cost Explorer format
            day_data['Groups'].append({
                "Keys": [service],
                "Metrics": {
                    "UnblendedCost": {
                        "Amount": str(amount),  # AWS returns string amounts
                        "Unit": "USD"
                    }
                }
            })
        
        # Calculate total cost by summing all service costs for this day
        for i in range(len(day_data['Groups'])):
            Total += float(day_data['Groups'][i]['Metrics']['UnblendedCost']['Amount'])
        
        # Add daily data to results
        mock_data.append(day_data)
    
    # Return data in AWS Cost Explorer response format with total bill
    return ({'ResultsByTime' : mock_data}, f'Total Bill: ${Total:.2f}')

# Test the function by generating and printing mock AWS cost data
data = get_aws_cost()
print(data)
