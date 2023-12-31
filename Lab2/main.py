# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pv9nEmb_dkx3cu5Qe6zqyfjyF3KsOfdl
"""

import numpy as np
from sklearn.datasets import load_iris

#Loading Data--------------------------------------------------------------------------------->
iris = load_iris()
X = iris.data
y = iris.target

# Shuffling----------------------------------------------------------------------------------->
data = np.column_stack((X, y))
np.random.shuffle(data)

# Splitting it--------------------------------------------------------------------------------->
split_ratio = 0.2
split_index = int(len(data) * (1 - split_ratio))

X_train = data[:split_index, :-1]
y_train = data[:split_index, -1].astype(int)
X_test = data[split_index:, :-1]
y_test = data[split_index:, -1].astype(int)

# K-Fold------------------------------------------------------------------------------------------>
num_folds = 5
fold_size = len(X_train) // num_folds

# Storing results--------------------------------------------------------------------------------->
validation_results = []

# Check for all K values -------------------------------------------------------------------------->
for k in range(1, 16):
    validation_accuracies = []

    for i in range(num_folds):
        val_start = i * fold_size
        val_end = val_start + fold_size

        X_val_fold = X_train[val_start:val_end]
        y_val_fold = y_train[val_start:val_end]

        X_train_fold = np.concatenate((X_train[:val_start], X_train[val_end:]), axis=0)
        y_train_fold = np.concatenate((y_train[:val_start], y_train[val_end:]), axis=0)

        correct_predictions = 0

        for j, test_point in enumerate(X_val_fold):
            distances = []

            for train_point, train_label in zip(X_train_fold, y_train_fold):
                distance = np.sqrt(np.sum((test_point - train_point) ** 2))
                distances.append((distance, train_label))

            distances.sort()
            neighbors = [label for (_, label) in distances[:k]]
            predicted_label = max(set(neighbors), key=neighbors.count)

            if predicted_label == y_val_fold[j]:
                correct_predictions += 1

        accuracy = correct_predictions / len(X_val_fold)
        validation_accuracies.append(accuracy)

    mean_accuracy = np.mean(validation_accuracies)
    std_deviation = np.std(validation_accuracies)
    validation_results.append((k, mean_accuracy, std_deviation))

    print(f"K = {k}, Mean Validation Accuracy = {mean_accuracy:.4f}, Std Deviation = {std_deviation:.4f}")

# Findind best K value----------------------------------------------------------------------------->
best_k, best_mean_accuracy, best_std_deviation = max(validation_results, key=lambda x: x[1])

print(f"Best K value is : {best_k}")
print(f"Validation Accuracy for Best K value is ---------------> {best_mean_accuracy:.4f}")
print(f"Standard Deviation for Best K value is ----------------> {best_std_deviation:.4f}")

best_knn_predictions = []

for test_point in X_test:
    distances = []

    for train_point, train_label in zip(X_train, y_train):
        distance = np.sqrt(np.sum((test_point - train_point) ** 2))
        distances.append((distance, train_label))

    distances.sort()
    neighbors = [label for (_, label) in distances[:best_k]]
    predicted_label = max(set(neighbors), key=neighbors.count)
    best_knn_predictions.append(predicted_label)

# Calculating accuracy for best k----------------------------------------------------------------------->
test_correct_predictions = np.sum(best_knn_predictions == y_test)
test_accuracy = test_correct_predictions / len(y_test)

print(f"Test Accuracy for Best K value is -----------> ({best_k}): {test_accuracy:.4f}")