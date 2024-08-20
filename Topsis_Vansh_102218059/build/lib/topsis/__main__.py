# topsis_firstname_rollnumber/topsis.py
import pandas as pd
import numpy as np
import sys

def topsis( weights, impacts,matrix):
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

    data = pd.read_csv(input_file)
    fund_names = data.iloc[:, 0]
    matrix = data.iloc[:, 1:].values
    
    if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
        print("Error: Weights and impacts length must match the number of columns in the decision matrix")
        sys.exit(1)

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
