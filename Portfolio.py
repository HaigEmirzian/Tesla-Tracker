import os

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
    
    print("Average cost: ")
    average_cost_inputted = float(input())

    return shares_inputted, average_cost_inputted

# Calculates average cost using the formula
def calculate_average_cost(total_shares, total_value, new_shares, new_cost):
    updated_shares = total_shares + new_shares
    updated_value = total_value + (new_shares * new_cost)
    if updated_shares == 0:
        return 0
    return updated_value / updated_shares

if __name__ == "__main__":
    file_path = "portfolio_data.txt"
    shares, average_cost = read_data(file_path)

    new_shares, new_cost = inputs()
    new_average_cost = calculate_average_cost(shares, shares * average_cost, new_shares, new_cost)
    
    write_data(file_path, shares + new_shares, new_average_cost)
    print(f"Updated Average Cost: {new_average_cost}")
    # reset(file_path)
