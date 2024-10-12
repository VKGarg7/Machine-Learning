import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def topsis(data, weights, impacts):
    weights = np.array([float(i) for i in weights.split(',')])
    impacts = np.array([1 if i == '+' else -1 for i in impacts.split(',')])

    normalized_data = data / np.sqrt((data**2).sum(axis=0))

    weighted_normalized_data = normalized_data * weights

    ideal_best = np.max(weighted_normalized_data * impacts, axis=0)
    ideal_worst = np.min(weighted_normalized_data * impacts, axis=0)

    distance_best = np.sqrt(((weighted_normalized_data - ideal_best)**2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_normalized_data - ideal_worst)**2).sum(axis=1))

    scores = distance_worst / (distance_best + distance_worst)

    return scores

def plot_results(df, result_file):
    plt.figure(figsize=(10, 6))
    plt.barh(df['Model'], df['TOPSIS Score'], color='skyblue')
    plt.xlabel('TOPSIS Score')
    plt.ylabel('Models')
    plt.title('TOPSIS Score for Sentence Similarity Models')
    plt.savefig(result_file.replace(".csv", ".png"))
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit()

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    df = pd.read_csv(input_file)

    model_names = df.iloc[:, 0]
    data = df.iloc[:, 1:].values

    scores = topsis(data, weights, impacts)

    result_df = pd.DataFrame({
        'Model': model_names,
        'TOPSIS Score': scores
    })

    result_df = result_df.sort_values(by='TOPSIS Score', ascending=False)

    result_df.to_csv(output_file, index=False)
    
    plot_results(result_df, output_file)

    print(f"Results saved to {output_file}")
