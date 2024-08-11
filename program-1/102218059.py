import pandas as pd
import numpy as np
import sys

def download_and_convert_excel_to_csv(excel_url, roll_number):
    df = pd.read_excel(excel_url)
    csv_filename = f"{roll_number}-data.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Converted and saved as {csv_filename}")
    return csv_filename

def topsis(decision_matrix, weights, impacts):
    # Step 1: 
    norm_matrix = decision_matrix / np.sqrt((decision_matrix**2).sum(axis=0))
    
    # Step 2:
    weighted_matrix = norm_matrix * weights
    
    # Step 3: 
    ideal_solution = np.max(weighted_matrix, axis=0) * (impacts == '+') + np.min(weighted_matrix, axis=0) * (impacts == '-')
    negative_ideal_solution = np.min(weighted_matrix, axis=0) * (impacts == '+') + np.max(weighted_matrix, axis=0) * (impacts == '-')
    
    # Step 4:
    positive_distance = np.sqrt(((weighted_matrix - ideal_solution) ** 2).sum(axis=1))
    negative_distance = np.sqrt(((weighted_matrix - negative_ideal_solution) ** 2).sum(axis=1))
    
    # Step 5:
    scores = negative_distance / (positive_distance + negative_distance)
    
    # Step 6: 
    ranking = scores.argsort()[::-1] + 1
    
    return scores, ranking

def main():
    if len(sys.argv) != 5:
        print("Usage: python <Rollnumber>.py <excel_url> <weights> <impacts> <roll_number>")
        sys.exit(1)
    
    excel_url = sys.argv[1]
    weights = [float(x) for x in sys.argv[2].split(",")]
    impacts = sys.argv[3].split(",")
    roll_number = sys.argv[4]

    csv_filename = download_and_convert_excel_to_csv(excel_url, roll_number)

    data = pd.read_csv(csv_filename)
    fund_names = data.iloc[:, 0]
    decision_matrix = data.iloc[:, 1:].values
    
    if len(weights) != decision_matrix.shape[1] or len(impacts) != decision_matrix.shape[1]:
        print("Error: Weights and impacts length must match the number of columns in the decision matrix")
        sys.exit(1)

    scores, ranking = topsis(decision_matrix, np.array(weights), np.array(impacts))
    
    results = pd.DataFrame({
        "Fund Name": fund_names,
        **{f"P{i+1}": data.iloc[:, i+1] for i in range(decision_matrix.shape[1])},
        "Topsis Score": scores,
        "Rank": ranking
    })
    
    result_filename = f"{roll_number}-result.csv"
    results.to_csv(result_filename, index=False)
    print(f"Results saved to {result_filename}")

if __name__ == "__main__":
    main()
