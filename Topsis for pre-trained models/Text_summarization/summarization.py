import sys
import pandas as pd
import numpy as np

def topsis(data, weights, impacts):
    # Convert weights and impacts to the correct formats
    weights = np.array([float(i) for i in weights.split(',')])
    impacts = np.array([1 if i == '+' else -1 for i in impacts.split(',')])

    # Step 1: Normalize the decision matrix
    normalized_data = data / np.sqrt((data**2).sum(axis=0))

    # Step 2: Apply weights to the normalized matrix
    weighted_normalized_data = normalized_data * weights

    # Step 3: Calculate the ideal best and ideal worst
    ideal_best = np.max(weighted_normalized_data * impacts, axis=0)
    ideal_worst = np.min(weighted_normalized_data * impacts, axis=0)

    # Step 4: Calculate the distances from the ideal best and worst
    distance_best = np.sqrt(((weighted_normalized_data - ideal_best)**2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_normalized_data - ideal_worst)**2).sum(axis=1))

    # Step 5: Calculate the TOPSIS score
    scores = distance_worst / (distance_best + distance_worst)

    return scores

if __name__ == "__main__":
    # Command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit()

    # Read command-line arguments
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    # Load the dataset
    df = pd.read_csv(input_file)

    # Separate the model names and the data
    model_names = df.iloc[:, 0]
    data = df.iloc[:, 1:].values

    # Apply TOPSIS
    scores = topsis(data, weights, impacts)

    # Create a result dataframe
    result_df = pd.DataFrame({
        'Model': model_names,
        'TOPSIS Score': scores
    })

    # Sort the result by TOPSIS score
    result_df = result_df.sort_values(by='TOPSIS Score', ascending=False)

    # Save the result to a CSV file
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
