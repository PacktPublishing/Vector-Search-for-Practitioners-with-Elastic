import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
k = 5
threshold = 2

# Sigmoid Function
def soc_function(R, C, T, A, k, wR=1, wC=1, wT=1, wA=1, threshold=0):
    return 1 / (1 + np.exp(-k * (wR*R + wC*C + wT*T + wA*A - threshold)))

# 1. Sigmoid function curve
x = np.linspace(-10, 10, 400)
y = 1 / (1 + np.exp(-x))

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title("Figure 1: Sigmoid Function Curve")
plt.xlabel("x")
plt.ylabel("Sigmoid(x)")
plt.grid(True)
plt.show()

# 2. 3D Plot for interaction
from mpl_toolkits.mplot3d import Axes3D

# Generating random data for the example (you might want to use real data)
R_vals = np.linspace(0, 1, 10)
C_vals = np.linspace(0, 1, 10)
T_vals = np.linspace(0, 1, 10)

R, C, T = np.meshgrid(R_vals, C_vals, T_vals)
A_val = 0.5  # fixed for simplicity in this example
SoC = soc_function(R, C, T, A_val, k)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(R, C, T, c=SoC.ravel(), cmap='viridis')
ax.set_xlabel('Relevance (R)')
ax.set_ylabel('Continuity (C)')
ax.set_zlabel('Timeliness (T)')
ax.set_title("Figure 2: Interaction of R, C, and T")
fig.colorbar(scatter, ax=ax, label='SoC Value')  # This adds the colorbar
plt.show()

# 3. Effect of varying k
ks = [1, 5, 10]
R_val, C_val, T_val, A_val = 0.5, 0.6, 0.7, 0.8

plt.figure(figsize=(8, 6))


plt.title("Figure 3: Effect of Varying k on SoC")
plt.xlabel("Combined Factors")
plt.ylabel("SoC Value")
plt.legend()
plt.grid(True)
plt.show()

# 4. Heatmap of weights
# For simplicity, we'll consider the interaction between two weights, say wR and wC.

weights = np.linspace(0, 2, 50)
wR, wC = np.meshgrid(weights, weights)
SoC_heatmap = soc_function(R_val, C_val, T_val, A_val, k, wR, wC)

plt.figure(figsize=(8, 6))
sns.heatmap(SoC_heatmap, cmap='viridis', cbar_kws={'label': 'SoC Value'})
plt.title("Figure 4: Heatmap of Varying wR and wC")
plt.xlabel("Weight of Relevance (wR)")
plt.ylabel("Weight of Continuity (wC)")
plt.xticks(ticks=np.linspace(0, len(weights)-1, 5), labels=np.linspace(0, 2, 5))
plt.yticks(ticks=np.linspace(0, len(weights)-1, 5), labels=np.linspace(0, 2, 5))
plt.show()

# Note: For the remaining figures and tables, we would need more specific scenarios or datasets to plot them effectively.
