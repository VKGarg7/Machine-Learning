import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from sklearn.datasets import load_iris
data = load_iris()
X = data.data
y = data.target

scaler = StandardScaler()
X = scaler.fit_transform(X)

samples = [train_test_split(X, y, test_size=0.3, random_state=i) for i in range(10)]

def run_svm(X_train, y_train, X_test, y_test):
    accuracies = []
    best_accuracy = 0
    best_params = {}
    
    kernels = ['rbf']
    epsilon = 0.001 
    for kernel in kernels:
        for C in np.linspace(0.1, 1, 10):
            svm = SVC(C=C, kernel=kernel)
            svm.fit(X_train, y_train)
            y_pred = svm.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(accuracy)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_params = {
                    'kernel': kernel,
                    'C': C,
                    'epsilon': epsilon
                }
    
    return best_accuracy, best_params, accuracies

results = []
best_sample_idx = -1
best_sample_accuracy = 0
best_sample_accuracies = []
best_sample_params = {}

for i, (X_train, X_test, y_train, y_test) in enumerate(samples):
    best_accuracy , best_params , accuracies = run_svm(X_train , y_train , X_test , y_test)
    results.append([f"S{i+1}", best_accuracy, best_params['kernel'], best_params['C'], best_params['epsilon']])
    
    if best_accuracy > best_sample_accuracy:
        best_sample_idx = i
        best_sample_accuracy = best_accuracy
        best_sample_accuracies = accuracies
        best_sample_params = best_params

results_df = pd.DataFrame(results, columns=["Sample" , "Best Accuracy" , "Kernel" , "C (nu)" , "Epsilon"])
results_df.to_csv("svm_optimization_results.csv", index=False)

plt.plot(best_sample_accuracies)
plt.title(f'Convergence for Best Sample (S{best_sample_idx+1})')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.savefig(f'convergence_plot_S{best_sample_idx+1}.png')

print(results_df)

print(f"\nBest sample is S{best_sample_idx+1} with accuracy {best_sample_accuracy}")
print(f"Best parameters: Kernel = {best_sample_params['kernel']}, C = {best_sample_params['C']}, Epsilon = {best_sample_params['epsilon']}")
