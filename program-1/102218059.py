# import pandas as pd
# import numpy as np
# import sys

# def download_and_convert_excel_to_csv(excel_url, roll_number):
#     df = pd.read_excel(excel_url)
#     csv_filename = f"{roll_number}-data.csv"
#     df.to_csv(csv_filename, index=False)
#     print(f"Converted and saved as {csv_filename}")
#     return csv_filename

# def topsis(matrix, weights, impacts):
#     norm = matrix / np.sqrt((matrix**2).sum(axis=0))
    
#     weight = norm * weights

#     solution = np.max(weight, axis=0) * (impacts == '+') + np.min(weight, axis=0) * (impacts == '-')
#     negative_solution = np.min(weight, axis=0) * (impacts == '+') + np.max(weight, axis=0) * (impacts == '-')

#     positive_distance = np.sqrt(((weight - solution) ** 2).sum(axis=1))
#     negative_distance = np.sqrt(((weight - negative_solution) ** 2).sum(axis=1))
    
#     scores = negative_distance / (positive_distance + negative_distance)
     
#     ranking = scores.argsort()[::-1] + 1
    
#     return scores, ranking

# def main():
#     if len(sys.argv) != 5:
#         print("Usage: python <Rollnumber>.py <excel_url> <weights> <impacts> <roll_number>")
#         sys.exit(1)
    
#     excel_url = sys.argv[1]
#     weights = [float(x) for x in sys.argv[2].split(",")]
#     impacts = sys.argv[3].split(",")
#     roll_number = sys.argv[4]

#     csv_filename = download_and_convert_excel_to_csv(excel_url, roll_number)

#     data = pd.read_csv(csv_filename)
#     fund_names = data.iloc[:, 0]
#     matrix = data.iloc[:, 1:].values
    
#     if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
#         print("Error: Weights and impacts length must match the number of columns in the decision matrix")
#         sys.exit(1)

#     scores, ranking = topsis(matrix, np.array(weights), np.array(impacts))
    
#     results = pd.DataFrame({
#         "Fund Name": fund_names,
#         **{f"P{i+1}": data.iloc[:, i+1] for i in range(matrix.shape[1])},
#         "Topsis Score": scores,
#         "Rank": ranking
#     })
    
#     result_filename = f"{roll_number}-result.csv"
#     results.to_csv(result_filename, index=False)
#     print(f"Results saved to {result_filename}")

# if __name__ == "__main__":
#     main()


import pandas as pd
import numpy as np
import sys

def topsis( weights, impacts, matrix):
    norm = matrix / np.sqrt((matrix**2).sum(axis=0))
    
    weight = norm * weights

    sol = np.max(weight, axis=0) * (impacts == '+') + np.min(weight, axis=0) * (impacts == '-')
    neg_sol = np.min(weight, axis=0) * (impacts == '+') + np.max(weight, axis=0) * (impacts == '-')

    pos_dis = np.sqrt(((weight - sol) ** 2).sum(axis=1))
    neg_dis = np.sqrt(((weight - neg_sol) ** 2).sum(axis=1))
    
    scores = neg_dis / (pos_dis + neg_dis)
     
    ranking = scores.argsort()[::-1] + 1
    
    return scores, ranking

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py>  <Weights> <Impacts> <InputDataFile> <ResultFileName>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = [float(x) for x in sys.argv[2].split(",")]
    impacts = sys.argv[3].split(",")
    result_file = sys.argv[4]

    # Read the input CSV file
    data = pd.read_csv(input_file)
    fund_names = data.iloc[:, 0]
    matrix = data.iloc[:, 1:].values
    
    if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
        print("Error: Weights and impacts length must match the number of columns in the decision matrix")
        sys.exit(1)

    # Perform TOPSIS analysis
    scores, ranking = topsis(matrix, np.array(weights), np.array(impacts))
    
    results = pd.DataFrame({
        "Fund Name": fund_names,
        **{f"P{i+1}": data.iloc[:, i+1] for i in range(matrix.shape[1])},
        "Topsis Score": scores,
        "Rank": ranking
    })
    
    results.to_csv(result_file, index=False)
    print(f"Results saved to {result_file}")

if __name__ == "__main__":
    main()
