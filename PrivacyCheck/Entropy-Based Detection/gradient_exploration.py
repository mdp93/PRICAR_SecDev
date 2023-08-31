# -*- coding: utf-8 -*-
"""Gradient Exploration

Automatically generated by Colaboratory.

# Helper Functions
"""

import json
import os
import random
  
import numpy as np
import scipy.stats as stats
import scipy.signal as signal
import matplotlib.pyplot as plt
import math

# Sliding window class to handle data being passed in one value at a time 
# This is based on number of data points, not time
class SlidingWindow:
  def __init__(self, size):
    assert size > 0
    self.size = size
    self.data = np.array([])
  def push(self, val):
    if len(self.data) < self.size:
      self.data = np.append(self.data, [val])
    else:
      self.data = np.append(self.data[1:], [val])

def calculate_shannon_entropy(data, precision=2):
  #sort continuous data into discrete buckets so entropy doesn't grow unbounded
  truncated_data = (data.round(decimals=precision) * (10 ** precision)).astype(int)
  value,counts = np.unique(truncated_data, return_counts=True)
  return stats.entropy(counts, base=2)

def get_data(filename):
  with open(filename) as data_file:
    data = np.array(json.load(data_file)['series'][0]['raw'])
    return data

def get_sliding_window_entropies(data, window_size):
  window = SlidingWindow(window_size)
  entropies = []
  for datum in data:
    window.push(datum)
    entropy = calculate_shannon_entropy(window.data)
    entropies.append(entropy)
  return entropies

def get_correct_changepoints(filepath):
  with open("/content/drive/MyDrive/School Work/Junior Year/Research/Input files/correct_changepoints.json") as file:
    correct_changepoints = json.load(file)
    filename = os.path.basename(filepath)
    assert filename in correct_changepoints
    return correct_changepoints[filename]

#REQUIRES: data starts off as normal, first changepoint marks anomalous
def get_data_labels(changepoints, length):
  is_anomaly = False
  tagged_data = np.zeros(length, dtype=bool)
  for i in range(length):
    if i in changepoints:
      is_anomaly = not is_anomaly
    tagged_data[i] = is_anomaly
  return tagged_data

def partition_array(values, partitions):
  #assumes values and partitions have same length
  assert(len(partitions) == len(values))

  p1 = np.array([])
  p2 = np.array([])

  for i in range(len(values)):
    if partitions[i]:
      p1 = np.append(p1, np.nan)
      p2 = np.append(p2, values[i])
    else:
      p1 = np.append(p1, values[i])
      p2 = np.append(p2, np.nan)
  
  return p1, p2

def plot_colored_entropy(filename, window_size=100):
  data = get_data(filename)
  calculate_shannon_entropy(data)
  entropies = get_sliding_window_entropies(data, window_size)
  changepoints = get_correct_changepoints(filename)
  labeled_data = get_data_labels(changepoints, len(data))

  #partition data into anomaly and valid
  valid, anomaly = partition_array(entropies, labeled_data)

  plt.plot(valid, color="b")
  plt.plot(anomaly, color="r")
  plt.xlabel("Data Sample")
  plt.ylabel("Shannon Entropy (bits)")
  # plt.title(filename.split("/")[-1])
  # plt.savefig("test.pdf", dpi=500)
  # plt.show()

def calculate_f1_of_predictions(predicted_anomalies, real_anomalies):
  correct_anomalies = 0
  correct_normal = 0
  normal_classified_as_anomaly = 0
  anomaly_classified_as_normal = 0

  for i in range(len(predicted_anomalies)):
    if real_anomalies[i] and predicted_anomalies[i]:
      correct_anomalies += 1
    elif real_anomalies[i] and not predicted_anomalies[i]:
      anomaly_classified_as_normal += 1
    elif not real_anomalies[i] and not predicted_anomalies[i]:
      correct_normal += 1
    elif not real_anomalies[i] and predicted_anomalies[i]:
      normal_classified_as_anomaly += 1

  precision = correct_anomalies / (correct_anomalies + normal_classified_as_anomaly)
  recall = correct_anomalies / (correct_anomalies + anomaly_classified_as_normal)

  # print(f"Precision: {precision}")
  # print(f"Recall: {recall}")

  # return stats.hmean([precision, recall])
  return (2 * precision * recall)/ (precision + recall)

"""# Exploration"""

plot_colored_entropy("/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random20.json")

filename = "/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random20.json"
window_size = 100

data = get_data(filename)
calculate_shannon_entropy(data)
entropies = get_sliding_window_entropies(data, window_size)
gradient = np.gradient(entropies)
changepoints = get_correct_changepoints(filename)
labeled_data = get_data_labels(changepoints, len(data))

#partition data into anomaly and valid
valid, anomaly = partition_array(gradient, labeled_data)

switch_threshold = 0.00
sig_valid = [i if abs(i) >= switch_threshold else np.nan for i in valid]
sig_anomaly = [i if abs(i) >= switch_threshold else np.nan for i in anomaly]

plt.plot(sig_valid[100:], color="b")
plt.plot(sig_anomaly[100:], color="r")

plt.xlabel("Data Sample")
plt.ylabel("Derivative of Shannon Entropy (bits)")
print(filename.split("/")[-1])
print("\tMin: ", min(entropies[2 * window_size:]))
print("\tMax: ", max(entropies[window_size:]))

# plt.savefig("test.pdf", dpi=500)
# plt.show()

predicted_anomalies = [d < 0.0099 for d in gradient]

assert(len(predicted_anomalies) == len(labeled_data))

correct_anomalies = 0
correct_normal = 0
normal_classified_as_anomaly = 0
anomaly_classified_as_normal = 0
for i in range(len(predicted_anomalies)):
  if labeled_data[i] and predicted_anomalies[i]:
    correct_anomalies += 1
  elif labeled_data[i] and not predicted_anomalies[i]:
    anomaly_classified_as_normal += 1
  elif not labeled_data[i] and not predicted_anomalies[i]:
    correct_normal += 1
  elif not labeled_data[i] and predicted_anomalies[i]:
    normal_classified_as_anomaly += 1
print(correct_anomalies, correct_normal)

precision = correct_anomalies / (correct_anomalies + normal_classified_as_anomaly)
recall = correct_anomalies / (correct_anomalies + anomaly_classified_as_normal)

print(f"Precision: {precision}")
print(f"Recall: {recall}")

print(f"F1 Score: {stats.hmean([precision, recall])}")

def gradient_anomaly_detection(filename, window_size):
  e = get_sliding_window_entropies(get_data(filename), window_size)
  der = np.gradient(e)
  return calculate_f1_of_predictions([g < 0.0099 for g in der], get_data_labels(get_correct_changepoints(filename), len(e)))

gradient_results_random = {}

random_file_numbers = [1, 2, 4, 10, 20, 40, 80, 200, 400]
for num in random_file_numbers:
  filename = f"/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random{num}.json"
  gradient_results_random[num] = gradient_anomaly_detection(filename, 100)

gradient_results_fixed = {}
fixed_file_numbers = [4, 8, 16, 20, 40, 80, 400, 1000]
for num in fixed_file_numbers:
  filename = f"/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_every{num}.json"
  gradient_results_fixed[2000/num] = gradient_anomaly_detection(filename, 100)

random_anomaly_count = [k for k in sorted(gradient_results_random.keys())]
random_anomaly_f1 = [gradient_results_random[k] for k in sorted(gradient_results_random.keys())]
fixed_anomaly_count = [k for k in gradient_results_fixed.keys()]
fixed_anomaly_f1 = [gradient_results_fixed[k] for k in sorted(gradient_results_fixed.keys())]
plt.xlabel("Number of Anomalies")
plt.ylabel("F1 Score")
plt.plot(random_anomaly_count, random_anomaly_f1, "b", label="Random Anomalies")
plt.plot(fixed_anomaly_count, fixed_anomaly_f1, "m", label="Fixed Anomalies")
plt.legend(loc="upper right")

cutoffs = np.linspace(-0.02, 0.02, 801)
f1_scores = []
for cutoff in cutoffs:
  predicted = [d < cutoff for d in gradient]
  f1 = calculate_f1_of_predictions(predicted, labeled_data)
  f1_scores.append(f1)

best = f1_scores.index(max(f1_scores))
print(f"Best cutoff: {cutoffs[best]}")
print(f"Best f1 score: {f1_scores[best]}")

"""#Next Steps

* Try to optimize detection for when entropy derivative is close to 0 ("toggle on spike" approach)
* Optimize threshold parameter
* Investigate window size's effect on accuracy
"""

