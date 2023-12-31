# -*- coding: utf-8 -*-
"""Plotting Turing Benchmark.ipynb

Automatically generated by Colaboratory.

"""

import matplotlib.pyplot as plt

"""# Data

"""

best_cover_fixed_entropies = {	
  2000/1000: {
		"bocpd": 0.8263194253638343,
		"cpnp": 0.3228737769080235,
		"pelt": 0.8225816407692527
	},
	2000/16: {
		"bocpd": 0.5600251186564441,
		"cpnp": 0.8100579237755695,
		"pelt": 0.5254590145273399
	},
	2000/20: {
		"bocpd": 0.5401739233723855,
		"cpnp": 0.47026814185718113,
		"pelt": 0.5400325802445031
	},
	2000/40: {
		"bocpd": 0.38193560991800457,
		"cpnp": 0.430670001507484,
		"pelt": 0.42952599837975386
	},
	2000/400: {
		"bocpd": 0.6010449966546499,
		"cpnp": 0.43586257277493434,
		"pelt": 0.6015331047514806
	},
	2000/8: {
		"bocpd": 0.49270390131956493,
		"cpnp": 0.5992718614718623,
		"pelt": 0.569454144868533
	},
	2000/80: {
		"bocpd": 0.6146813708204669,
		"cpnp": 0.6318553787849248,
		"pelt": 0.6390634171323122
  }
}

best_cover_fixed_regular = {
  2000/1000: {
		"bocpd": 0.9231916996047431,
		"cpnp": 0.979190178953564,
		"pelt": 0.7679845965859737
	},
	2000/16: {
		"bocpd": 0.3680373737373737,
		"cpnp": 0.5174775050096102,
		"pelt": 0.4520269345658601
	},
	2000/20: {
		"bocpd": 0.3148235930735931,
		"cpnp": 0.49632045415268083,
		"pelt": 0.43075694570658646
	},
	2000/40: {
		"bocpd": 0.19304761904761902,
		"cpnp": 0.44146890859323007,
		"pelt": 0.504732446104049
	},
	2000/400: {
		"bocpd": 0.6564536214146558,
		"cpnp": 0.9013197893042034,
		"pelt": 0.6614708319082613
	},
	2000/8: {
		"bocpd": 0.5597904761904763,
		"cpnp": 0.4772343467935582,
		"pelt": 0.552
	},
	2000/80: {
		"bocpd": 0.14982349165596912,
		"cpnp": 0.6151555262898495,
		"pelt": 0.5313660020830182
	}
}

best_cover_random_entropies = {
  10: {
		"bocpd": 0.6135565487900205,
		"cpnp": 0.38066544090665283,
		"pelt": 0.6247758319270312
	},
	20: {
		"bocpd": 0.5449414313109922,
		"cpnp": 0.45665947865698564,
		"pelt": 0.555911061227262
	},
	200: {
		"bocpd": 0.43691595946483697,
		"cpnp": 0.438932212379101,
		"pelt": 0.4467541722447793
	},
	4: {
		"bocpd": 0.8403688990948293,
		"cpnp": 0.34598275862068967,
		"pelt": 0.831613751760784
	},
	40: {
		"bocpd": 0.4795267799837001,
		"cpnp": 0.45620458605657477,
		"pelt": 0.4444364235221182
	},
	400: {
		"bocpd": 0.4001905942629895,
		"cpnp": 0.4346284303333768,
		"pelt": 0.43958870509896847
	},
	80: {
		"bocpd": 0.4676521091280272,
		"cpnp": 0.4638802318966244,
		"pelt": 0.4393280536181682
	}
}

best_cover_random_regular = {	
  10: {
		"bocpd": 0.6848926453375368,
		"cpnp": 0.634689583357468,
		"pelt": 0.658445581634372
	},
	20: {
		"bocpd": 0.5530165133908032,
		"cpnp": 0.6784324750504381,
		"pelt": 0.5685748797613867
	},
	200: {
		"bocpd": 0.26825883256528416,
		"cpnp": 0.44403597410811263,
		"pelt": 0.4322072033617756
	},
	4: {
		"bocpd": 0.9081060892250998,
		"cpnp": 0.9647327139614142,
		"pelt": 0.8866452082415649
	},
	40: {
		"bocpd": 0.37592736939926946,
		"cpnp": 0.5564403703778559,
		"pelt": 0.5159472940569291
	},
	400: {
		"bocpd": 0.39477619047619056,
		"cpnp": 0.4529618415790436,
		"pelt": 0.39052792830823096
	},
	80: {
		"bocpd": 0.17965481458565608,
		"cpnp": 0.4875416299915025,
		"pelt": 0.5122815630189078
	}
}

best_f1_fixed_entropies = {
  2000/1000: {
		"bocpd": 0.4,
		"cpnp": 0.19354838709677416,
		"pelt": 0.2
	},
	2000/16: {
		"bocpd": 0.652232746955345,
		"cpnp": 0.9377593360995852,
		"pelt": 0.836036036036036
	},
	2000/20: {
		"bocpd": 0.7592592592592593,
		"cpnp": 0.7478260869565218,
		"pelt": 0.6440677966101694
	},
	2000/40: {
		"bocpd": 0.2765273311897106,
		"cpnp": 0.5325443786982249,
		"pelt": 0.4193548387096775
	},
	2000/400: {
		"bocpd": 0.18181818181818182,
		"cpnp": 0.23076923076923073,
		"pelt": 0.0909090909090909
	},
	2000/8: {
		"bocpd": 0.8060453400503779,
		"cpnp": 0.8756998880179171,
		"pelt": 0.8621399176954733
	},
	2000/80: {
		"bocpd": 0.6578947368421052,
		"cpnp": 0.6187050359712231,
		"pelt": 0.3576158940397351
	}
}

best_f1_fixed_regular = {
  2000/1000: {
		"bocpd": 0.4,
		"cpnp": 0.5,
		"pelt": 0.4
	},
	2000/16: {
		"bocpd": 0.4686035613870665,
		"cpnp": 0.6045340050377833,
		"pelt": 0.65625
	},
	2000/20: {
		"bocpd": 0.39215686274509803,
		"cpnp": 0.5739130434782609,
		"pelt": 0.5994962216624684
	},
	2000/40: {
		"bocpd": 0.21810250817884402,
		"cpnp": 0.41632653061224484,
		"pelt": 0.3888888888888889
	},
	2000/400: {
		"bocpd": 0.5714285714285715,
		"cpnp": 0.608695652173913,
		"pelt": 0.3636363636363636
	},
	2000/8: {
		"bocpd": 0.7575757575757575,
		"cpnp": 0.8414055080721747,
		"pelt": 0.8186753528773072
	},
	2000/80: {
		"bocpd": 0.13870967741935486,
		"cpnp": 0.38647342995169087,
		"pelt": 0.38016528925619836
	}
}

best_f1_random_entropies = {
  10: {
		"bocpd": 0.2162162162162162,
		"cpnp": 0.21052631578947367,
		"pelt": 0.09999999999999999
	},
	20: {
		"bocpd": 0.24657534246575344,
		"cpnp": 0.1971830985915493,
		"pelt": 0.21276595744680848
	},
	200: {
		"bocpd": 0.5689655172413793,
		"cpnp": 0.5524861878453039,
		"pelt": 0.5831960461285008
	},
	4: {
		"bocpd": 0.3636363636363636,
		"cpnp": 0.17647058823529413,
		"pelt": 0.26666666666666666
	},
	40: {
		"bocpd": 0.3220338983050847,
		"cpnp": 0.2809917355371901,
		"pelt": 0.21587301587301588
	},
	400: {
		"bocpd": 0.6973684210526315,
		"cpnp": 0.7268571428571429,
		"pelt": 0.7512899896800825
	},
	80: {
		"bocpd": 0.4732142857142857,
		"cpnp": 0.46153846153846156,
		"pelt": 0.36065573770491804
	}
}

best_f1_random_regular = {	
  10: {
		"bocpd": 0.25000000000000006,
		"cpnp": 0.25000000000000006,
		"pelt": 0.28571428571428575
	},
	20: {
		"bocpd": 0.3846153846153846,
		"cpnp": 0.3870967741935483,
		"pelt": 0.36363636363636365
	},
	200: {
		"bocpd": 0.398019801980198,
		"cpnp": 0.5049645390070922,
		"pelt": 0.5339805825242717
	},
	4: {
		"bocpd": 0.6666666666666665,
		"cpnp": 0.6,
		"pelt": 0.6
	},
	40: {
		"bocpd": 0.12,
		"cpnp": 0.3163841807909604,
		"pelt": 0.32727272727272727
	},
	400: {
		"bocpd": 0.6578730420445177,
		"cpnp": 0.7173447537473234,
		"pelt": 0.6900726392251816
	},
	80: {
		"bocpd": 0.23193916349809887,
		"cpnp": 0.3933054393305439,
		"pelt": 0.35294117647058826
	}
}

methods = ["bocpd", "cpnp", "pelt"]



"""# Plotting"""

def plot2(dict1, dict2, method):

  # plt.title("Random  Window Anomaly Detection Accuracy")
  plt.xlabel("Number of Anomalies")
  plt.ylabel("F1 Score")

  #plot dict1
  random_windowsizes = []
  random_values = []
  for key in sorted(dict1):
    random_windowsizes.append(key)
    random_values.append(dict1[key][method])
  plt.plot(random_windowsizes, random_values, 'b', label="Before Entropy Calculation")

  #plot dict2
  random_windowsizes = []
  random_values = []
  for key in sorted(dict2):
    random_windowsizes.append(key)
    random_values.append(dict2[key][method])
  plt.plot(random_windowsizes, random_values, 'r', label="After Entropy Calculation")

  plt.legend(loc="lower right")

plot2(best_f1_fixed_regular, best_f1_fixed_entropies, "pelt")

# plt.title("Random  Window Anomaly Detection Accuracy")
plt.xlabel("Number of Anomalies")
plt.ylabel("F1 Score")

#plot best_f1_fixed_regular
random_windowsizes = []
random_values = []
for key in sorted(best_f1_fixed_regular):
  random_windowsizes.append(key)
  random_values.append(best_f1_fixed_regular[key]["pelt"])
plt.plot(random_windowsizes, random_values, 'b', label="PELT")

#plot best_f1_fixed_entropies
random_windowsizes = []
random_values = []
for key in sorted(best_f1_fixed_entropies):
  random_windowsizes.append(key)
  random_values.append(best_f1_fixed_entropies[key]["pelt"])
plt.plot(random_windowsizes, random_values, 'r', label="PELT on Entropy")

plt.legend(loc="lower right")

#plot best_f1_fixed_regular
random_windowsizes = []
random_values = []
for key in sorted(best_f1_fixed_regular):
  random_windowsizes.append(key)
  random_values.append(best_f1_fixed_regular[key]["cpnp"])
plt.plot(random_windowsizes, random_values, 'b--', label="CPNP")

#plot best_f1_fixed_entropies
random_windowsizes = []
random_values = []
for key in sorted(best_f1_fixed_entropies):
  random_windowsizes.append(key)
  random_values.append(best_f1_fixed_entropies[key]["cpnp"])
plt.plot(random_windowsizes, random_values, 'r--', label="CPNP on Entropy")

plt.legend(loc="lower right")
# plt.savefig("Best F1 Comparison.pdf", dpi="500")