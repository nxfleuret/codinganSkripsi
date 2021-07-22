import matplotlib.pyplot as plt
import numpy as np
  
# x axis values
x = np.linspace(1, 10, 10)
# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# corresponding y axis values for 50% Summary
precision = [0.571, 0.597, 0.598, 0.454, 0.714, 0.808, 0.598, 0.844, 0.565, 0.841]
recall = [0.441, 0.563, 0.742, 0.613, 0.706, 0.695, 0.712, 0.767, 0.683, 0.849]
fmeasure = [0.442, 0.563, 0.739, 0.609, 0.706, 0.696, 0.709, 0.768, 0.681, 0.849]
  
# # corresponding y axis values for 25% Summary
# precision = [0.708, 0.653, 0.660, 0.677, 0.733, 0.768, 0.549, 0.697, 0.639, 0.971]
# recall = [0.579, 0.551, 0.865, 0.577, 0.687, 0.747, 0.494, 0.426, 0.673, 0.447]
# fmeasure = [0.581, 0.552, 0.861, 0.578, 0.687, 0.748, 0.495, 0.428, 0.672, 0.450]

# # corresponding y axis values for 10% Summary
# precision = [0.521, 0.992, 0.997, 0.992, 0.992, 0.819, 0.641, 0.801, 0.994, 0.994]
# recall = [0.351, 1.0, 1.0, 1.0, 1.0, 0.296, 0.652, 0.379, 1.0, 1.0]
# fmeasure = [0.352, 0.998, 0.999, 0.999, 0.999, 0.299, 0.652, 0.382, 0.999, 0.999]

# plotting the points 
# plt.plot(x, precision, label="Precision", color='#f54748', marker='o', linewidth=3)
# plt.plot(x, recall, label="Recall", color='#1eae98', marker='s', linewidth=3)
# plt.plot(x, fmeasure, label="F-Measure", color='#ffc947', marker='d', linewidth=3)
plt.grid(axis = 'y')

plt.bar(x - 0.2, precision, 0.2, label="Precision", color='#3CAEA3')
plt.bar(x, recall, 0.2, label="Recall", color='#F6D55C')
plt.bar(x + 0.2, fmeasure, 0.2, label="F-Measure", color='#ED553B')
plt.xticks(x)


# plt.set_xlabel('x-axis', fontsize=10)
# plt.set_ylabel('y-axis', fontsize=10)

legend = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)
legend.get_frame().set_alpha(None)
legend.get_frame().set_facecolor((0, 0, 0, 0))
  
# naming the x axis
plt.xlabel('Teks Berita')
# naming the y axis
# plt.ylabel('Nilai Precision, Recall, F-Measure')
  
# giving a title to my graph
# plt.title('Hasil Uji Ringkasan Persentase 25%')
  
# function to show the plot
plt.show()