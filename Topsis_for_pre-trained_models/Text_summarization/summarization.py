import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def topsis(data, weights, impacts):
    norm_data = data / np.sqrt((data**2).sum(axis=0))
    
    weighted_data = norm_data * weights
    
    ideal_best = np.max(weighted_data * impacts, axis=0)
    ideal_worst = np.min(weighted_data * impacts, axis=0)
    
    distance_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    
    topsis_score = distance_worst / (distance_best + distance_worst)
    
    return topsis_score

df = pd.read_csv('models_data.csv')

weights = np.array([0.5, 0.3, 0.2]) 
impacts = np.array([1, -1, -1]) 

scores = topsis(df.iloc[:, 1:].values, weights, impacts)

df['TOPSIS Score'] = scores
df['Rank'] = df['TOPSIS Score'].rank(ascending=False)

df = df.sort_values(by='TOPSIS Score', ascending=False)

df.to_csv('result.csv', index=False)
print(f"TOPSIS results saved to 'result.csv'.")

plt.figure(figsize=(10, 6))
plt.barh(df['Model'], df['TOPSIS Score'], color='skyblue')
plt.xlabel('TOPSIS Score')
plt.ylabel('Model')
plt.title('TOPSIS Scores of Text Summarization Models')
plt.gca().invert_yaxis()  
plt.savefig('result.png') 
print(f"Bar plot saved as 'result.png'.")
