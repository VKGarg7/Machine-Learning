# 🎯 SVM Optimization Project

Optimize **Support Vector Machines (SVM)** for multi-class classification using a dataset from the UCI Machine Learning Repository. This project aims to discover the best hyperparameters across multiple samples, evaluate performance, and visualize results.

---

## ✨ Features

- **🔍 Multi-Sample Testing**: Conducts evaluation on 10 different dataset splits.
- **⚙️ Hyperparameter Tuning**: Fine-tunes `kernel`, `C (nu)`, and `epsilon` for optimal performance.
- **📈 Convergence Plot**: Visualizes accuracy progression for the best-performing sample.
- **📊 Results in CSV**: Saves accuracy and hyperparameters for each sample in an easily accessible format.

---

## 📂 Files Included

| File Name                         | Description                                       |
|-----------------------------------|---------------------------------------------------|
| `svm_optimization.py`             | Main script for SVM optimization.                 |
| `svm_optimization_results.csv`    | Contains accuracy and hyperparameters for each sample. |
| `convergence_plot_SX.png`         | Convergence graph for the sample with the highest accuracy. |

---

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/svm-optimization.git
cd svm-optimization
