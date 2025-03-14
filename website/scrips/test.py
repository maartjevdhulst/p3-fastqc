# Import libraries
import matplotlib.pyplot as plt
import numpy as np


# Creating dataset
np.random.seed(10)
data = np.random.normal(100, 20, 200)

fig = plt.figure(figsize =(10, 7))

# Creating plot
plt.boxplot(data)

# show plot
plt.show()

# file = '../../../fastqc_v0.12.1/FastQC/Configuration/limits.txt'
# with open(file) as f:
#     for line in f:
#         if line.startswith('kmer'):
#             print(line)