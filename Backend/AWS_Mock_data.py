import random

def get_aws_cost():

    services = ["Amazon EC2", "Amazon S3", "AWS Lambda", "CloudWatch"]
    dates = ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04"]
    mock_data = []
    total = 0
    # Defining the dates form the first of the current month to today
    
    for i in range(len(dates)-1):
        day_data = {
        'TimePeriod' : {'Start': dates[i], 'End' : dates[i+1]},
        'Groups' : [],
        'Estimated' : False,
        }


        for service in services:
            ammount = round(random.uniform(0.5, 5.0),2)
            day_data['Groups'].append({
                "Keys": [service],
                "Metrics": {
                    "UnblendedCost": {
                        "Amount": str(ammount),  # AWS returns string amounts
                        "Unit": "USD"
                    }
                }
            })
            mock_data.append(day_data)
        #This is not given by AWS 
        for j in range(len(day_data['Groups'])):
            total += float(day_data['Groups'][j]['Metrics']['UnblendedCost']['Amount'])
 
    return {
    'ResultsByTime': mock_data,
    'Total': round(total, 2)
}
    # print()

data = get_aws_cost()
print(data)
