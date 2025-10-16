from flask import Flask, render_template, jsonify
USE_MOCK = True

app = Flask(__name__, template_folder='templates', static_folder='static')

if USE_MOCK:
    from Mock_data import get_aws_cost
else:
    from aws_cost import AWS_Cost

def normalize_data(results_by_time):
    """
    Convert AWS-like ResultsByTime -> flattened data for frontend charts.
    Returns dict with: services[], service_costs[], dates[], daily_totals[], total
    """
    # service_cost accumulation
    service_costs = {}
    dates = []
    daily_totals = []

    for day in results_by_time:
        # day["TimePeriod"]["Start"] is like '2025-10-01'
        start = day['TimePeriod']['Start']
        dates.append(start)

        day_total = 0.0
        for group in day.get('Groups', []):
            service = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            service_costs[service] = service_costs.get(service, 0.0) + amount
            day_total += amount

        daily_totals.append(round(day_total, 2))

    services = list(service_costs.keys())
    service_cost_values = [round(service_costs[s], 2) for s in services]
    total = round(sum(service_cost_values), 2)

    return {
        "services": services,
        "service_costs": service_cost_values,
        "dates": dates,
        "daily_totals": daily_totals,
        "total": total
    }
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aws')
def aws():
    return render_template('aws.html')

@app.route('/api_aws')
def api_aws():
    if USE_MOCK:
        full = get_aws_cost()
        results = full.get('ResultsByTime')
    else:
        aws = AWS_Cost()
        results = aws.get_aws_cost()
    
    normalized = normalize_data(results)
    return jsonify(normalized)

@app.route('/azure')
def azure():
    return render_template('azure.html')

@app.route('/api_azure')
def api_azure():
    pass

if __name__ == '__main__':
    app.run(debug=True)
