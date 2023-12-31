import os
import sys
import requests
from dotenv import load_dotenv
import finnhub
from babel.numbers import format_currency
from flask import Flask, jsonify, render_template

# Store share and average cost data
file_path = "portfolio_data.txt"

# Hosts Flask app
app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    value = portfolio_value(file_path)
    return render_template('index.html', portfolio_value=value)

# Route for thesis page
@app.route('/thesis')
def thesis():
    return render_template('thesis.html')

# Route for videos page
@app.route('/videos')
def videos():
    return render_template('videos.html')

# Route for portfolio updates every 2 seconds
@app.route('/get_portfolio_value')
def get_portfolio_value():
    updated_portfolio_value = portfolio_value(file_path)
    return jsonify({'portfolio_value': updated_portfolio_value})

# Format portfolio value
def format_dollar(value):
    return format_currency(value, 'USD', locale='en_US')

# Reads data from data file
def read_data(file_path):
    # If file does not exist
    if not os.path.exists(file_path):
        return 0, 0  
    # Else if the file exists
    with open(file_path, "r") as file:
        lines = file.readlines()
        shares = int(lines[0].strip())
        average_cost = float(lines[1].strip())
    return shares, average_cost

# Update stored share count and average cost
def write_data(file_path, shares, average_cost):
    with open(file_path, "w") as file:
        file.write(f"{shares}\n{average_cost}\n")

# Resets data file to 0 shares and 0 average cost
def reset(file_path):
    with open(file_path, "w") as file:
        file.write("0\n0\n")

# User inputs: shares bought and at what average cost
def inputs():
    print("Shares Bought: ")
    shares_inputted = int(input())
    
    print("Average Cost: ")
    average_cost_inputted = float(input())

    return shares_inputted, average_cost_inputted

# Calculates average cost using the formula
def calculate_average_cost(total_shares, total_value, new_shares, new_cost):
    updated_shares = total_shares + new_shares
    updated_value = total_value + (new_shares * new_cost)
    if updated_shares == 0:
        return 0
    return updated_value / updated_shares

# Calculates the portfolio value
def portfolio_value(file_path):
    load_dotenv()
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    stock_quote = int(finnhub_client.quote('TSLA')["c"])
    shares, average_cost = read_data(file_path)
    return format_dollar(shares * stock_quote)

if __name__ == "__main__":
    # Runs the CLI code, else it will just run the Flask app
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        while True:
            stdin = input('''
Add Shares: a
View Portfolio Value: v
Reset Portfolio: r
Quit: q
Enter your choice: ''')

            if stdin.lower() == "a": 
                shares, average_cost = read_data(file_path)
                new_shares, new_cost = inputs()
                new_average_cost = calculate_average_cost(shares, shares * average_cost, new_shares, new_cost)
                write_data(file_path, shares + new_shares, new_average_cost)
                print(f"Updated Average Cost: {new_average_cost}")
                break
            elif stdin.lower() == "v":
                print("Portfolio Value: ", portfolio_value(file_path))
                break
            elif stdin.lower() == "r":
                reset(file_path)
                print("Portfolio has been reset.")
                break
            elif stdin.lower() == "q":
                print("Exiting program.")
                break
            else:
                print("Invalid input. Please try again.")
    else:
        app.run(debug=True)
