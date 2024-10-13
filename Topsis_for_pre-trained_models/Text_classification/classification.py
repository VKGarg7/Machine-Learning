import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# TOPSIS Implementation
def topsis(data, weights, impacts):
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

# Visualization of Results and Saving Graph
def visualize_results(results_df, graph_file):
    # Set the aesthetics for the plot
    sns.set(style="whitegrid")

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='TOPSIS Score', y='Model', data=results_df, hue='Model', palette='viridis', legend=False)
    plt.title('TOPSIS Scores of Text Classification Models')
    plt.xlabel('TOPSIS Score')
    plt.ylabel('Model')
    plt.xlim(0, 1)  # Assuming scores are normalized between 0 and 1
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(graph_file)
    print(f"Graph saved as {graph_file}")

# Main script execution
if __name__ == "__main__":
    # Command-line arguments
    if len(sys.argv) != 6:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName> <GraphFileName>")
        sys.exit()

    # Read command-line arguments
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]
    graph_file = sys.argv[5]

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

    # Visualize the results and save the graph
    visualize_results(result_df, graph_file)
