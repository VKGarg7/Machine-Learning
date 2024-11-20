# Import necessary libraries
import numpy as np
import time
import matplotlib.pyplot as plt
import concurrent.futures

# Constants (smaller sizes to make it suitable for Colab)
MATRIX_SIZE = 1000  # Reduced matrix size
NUM_MATRICES = 50   # Reduced number of matrices
NUM_THREADS_LIST = [1, 2, 3, 4, 5, 6, 7, 8]

# Generate a constant matrix and random matrices
constant_matrix = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
random_matrices = [np.random.rand(MATRIX_SIZE, MATRIX_SIZE) for _ in range(NUM_MATRICES)]

# Function to perform matrix multiplication
def multiply_matrices(matrix):
    return np.dot(matrix, constant_matrix)

# Measure time for each number of threads
execution_times = []
for num_threads in NUM_THREADS_LIST:
    start_time = time.time()
    
    # Parallel matrix multiplication
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(multiply_matrices, random_matrices))
    
    # Calculate time taken
    time_taken = time.time() - start_time
    execution_times.append(time_taken / 60)  # Convert to minutes for consistency

# Display the results in a table format
print("Threads\tTime Taken (min)")
for threads, time_taken in zip(NUM_THREADS_LIST, execution_times):
    print(f"{threads}\t{time_taken:.2f}")

# Plot Execution Time vs Number of Threads
plt.figure(figsize=(10, 5))
plt.plot(NUM_THREADS_LIST, execution_times, marker='o', linestyle='-')
plt.title("Execution Time (Reduced Matrix Size)")
plt.xlabel("Number of Threads")
plt.ylabel("Time Taken (min)")
plt.grid(True)
plt.show()

# Simulate CPU usage graph (Optional)
# Here we create a static representation of CPU usage for visualization.
# This is a placeholder to simulate CPU graphs as shown in the image.
fig, axes = plt.subplots(4, 1, figsize=(6, 8))
for i, ax in enumerate(axes):
    ax.plot([0, 1, 2, 3, 4, 5], [0, 100, 0, 100, 0, 100] if i < len(NUM_THREADS_LIST) else [0] * 6)
    ax.set_title(f"CPU {i}")
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 50, 100])
    ax.set_xticks([])
plt.tight_layout()
plt.show()