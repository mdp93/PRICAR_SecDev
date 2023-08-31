import json

import matplotlib
from matplotlib import pyplot
from matplotlib.pyplot import plot

matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams['savefig.dpi'] = 200

# driver_scores_none
# driver_scores_pure

cover = "best_cover_uni_full.json"
f1 = "best_f1_uni_full.json"

every_names = {
    "driver_scores_every2": {
        "name": "Every Other",
        "window": 1
    },
    "driver_scores_every4": {
        "name": "Every 2",
        "window": 2
    },
    "driver_scores_every8": {
        "name": "Every 4",
        "window": 4
    },
    "driver_scores_every16": {
        "name": "Every 8",
        "window": 8
    },
    "driver_scores_every20": {
        "name": "Every 10",
        "window": 10
    },
    "driver_scores_every40": {
        "name": "Every 20",
        "window": 20
    },
    "driver_scores_every80": {
        "name": "Every 40",
        "window": 40
    },
    "driver_scores_every50": {
        "name": "Every 25",
        "window": 25
    },
    "driver_scores_every100": {
        "name": "Every 50",
        "window": 50
    },
    "driver_scores_every150": {
        "name": "Every 75",
        "window": 75
    },
    "driver_scores_every200": {
        "name": "Every 100",
        "window": 100
    },
    "driver_scores_every250": {
        "name": "Every 125",
        "window": 125
    },
    "driver_scores_every300": {
        "name": "Every 150",
        "window": 150
    },
    "driver_scores_every350": {
        "name": "Every 175",
        "window": 175
    },
    "driver_scores_every400": {
        "name": "Every 200",
        "window": 200
    },
    "driver_scores_every450": {
        "name": "Every 225",
        "window": 225
    },
    "driver_scores_every500": {
        "name": "Every 250",
        "window": 250
    },
    "driver_scores_every550": {
        "name": "Every 275",
        "window": 275
    },
    "driver_scores_every600": {
        "name": "Every 300",
        "window": 300
    },
    "driver_scores_every650": {
        "name": "Every 325",
        "window": 325
    },
    "driver_scores_every700": {
        "name": "Every 350",
        "window": 350
    },
    "driver_scores_every750": {
        "name": "Every 375",
        "window": 375
    },
    "driver_scores_every800": {
        "name": "Every 400",
        "window": 400
    },
    "driver_scores_every850": {
        "name": "Every 425",
        "window": 425
    },
    "driver_scores_every900": {
        "name": "Every 450",
        "window": 450
    },
    "driver_scores_every950": {
        "name": "Every 475",
        "window": 475
    },
    "driver_scores_every1000": {
        "name": "Every 500",
        "window": 500
    },
    "driver_scores_every1050": {
        "name": "Every 525",
        "window": 525
    },
    "driver_scores_every1100": {
        "name": "Every 550",
        "window": 550
    },
    "driver_scores_every1150": {
        "name": "Every 575",
        "window": 575
    },
    "driver_scores_every1200": {
        "name": "Every 600",
        "window": 600
    },
    "driver_scores_every1250": {
        "name": "Every 625",
        "window": 625
    },
    "driver_scores_every1300": {
        "name": "Every 650",
        "window": 650
    },
    "driver_scores_every1350": {
        "name": "Every 675",
        "window": 675
    },
    "driver_scores_every1400": {
        "name": "Every 700",
        "window": 700
    },
    "driver_scores_every1450": {
        "name": "Every 725",
        "window": 725
    },
    "driver_scores_every1500": {
        "name": "Every 750",
        "window": 750
    },
    "driver_scores_every1550": {
        "name": "Every 775",
        "window": 775
    },
    "driver_scores_every1600": {
        "name": "Every 800",
        "window": 800
    },
    "driver_scores_every1650": {
        "name": "Every 825",
        "window": 825
    },
    "driver_scores_every1700": {
        "name": "Every 850",
        "window": 850
    },
    "driver_scores_every1750": {
        "name": "Every 875",
        "window": 875
    },
    "driver_scores_every1800": {
        "name": "Every 900",
        "window": 900
    },
    "driver_scores_every1850": {
        "name": "Every 925",
        "window": 925
    },
    "driver_scores_every1900": {
        "name": "Every 950",
        "window": 950
    },
    "driver_scores_every1950": {
        "name": "Every 975",
        "window": 975
    },
    "driver_scores_half": {
        "name": "Every 1000",
        "window": 1000
    }
}
random_names = {
    "driver_scores_random1": {
        "name": "1 Random",
        "window": 2000 / (1 + 1)
    },
    "driver_scores_random2": {
        "name": "2 Random",
        "window": 2000 / (1 + 2)
    },
    "driver_scores_random4": {
        "name": "4 Random",
        "window": 2000 / (1 + 4)
    },
    "driver_scores_random5": {
        "name": "5 Random",
        "window": 333.3333333333333
    },
    "driver_scores_random10": {
        "name": "10 Random",
        "window": 181.8181818181818
    },
    "driver_scores_random15": {
        "name": "15 Random",
        "window": 125.0
    },
    "driver_scores_random20": {
        "name": "20 Random",
        "window": 95.23809523809524
    },
    "driver_scores_random25": {
        "name": "25 Random",
        "window": 76.92307692307692
    },
    "driver_scores_random30": {
        "name": "30 Random",
        "window": 64.51612903225806
    },
    "driver_scores_random35": {
        "name": "35 Random",
        "window": 55.55555555555556
    },
    "driver_scores_random40": {
        "name": "40 Random",
        "window": 48.78048780487805
    },
    "driver_scores_random45": {
        "name": "45 Random",
        "window": 43.47826086956522
    },
    "driver_scores_random50": {
        "name": "50 Random",
        "window": 39.21568627450981
    },
    "driver_scores_random55": {
        "name": "55 Random",
        "window": 35.714285714285715
    },
    "driver_scores_random60": {
        "name": "60 Random",
        "window": 32.78688524590164
    },
    "driver_scores_random65": {
        "name": "65 Random",
        "window": 30.303030303030305
    },
    "driver_scores_random70": {
        "name": "70 Random",
        "window": 28.169014084507044
    },
    "driver_scores_random75": {
        "name": "75 Random",
        "window": 26.31578947368421
    },
    "driver_scores_random80": {
        "name": "80 Random",
        "window": 24.691358024691358
    },
    "driver_scores_random85": {
        "name": "85 Random",
        "window": 23.25581395348837
    },
    "driver_scores_random90": {
        "name": "90 Random",
        "window": 21.978021978021978
    },
    "driver_scores_random95": {
        "name": "95 Random",
        "window": 20.833333333333332
    },

    "driver_scores_random200": {
        "name": "200 Random",
        "window": 2000 / (1 + 200)
    },
    "driver_scores_random400": {
        "name": "400 Random",
        "window": 2000 / (1 + 400)
    },
    "driver_scores_random1000": {
        "name": "1000 Random",
        "window": 2000 / (1 + 1000)
    },
}
length_names = {
    "driver_scores_every50_100": {
        "name": "Every 25, 100",
        "window": 25,
        "length": 100
    },
    "driver_scores_every50_200": {
        "name": "Every 25, 200",
        "window": 25,
        "length": 200
    },
    "driver_scores_every50": {
        "name": "Every 25, 2000",
        "window": 25,
        "length": 2000
    },
}

methods = [
    "amoc",
    "binseg",
    "bocpd",
    "cpnp",
    "pelt",
    "rfpop",
    "segneigh",
    "wbs",
    "zero",
]

with open(f1) as f1_file:
    f1_data = json.load(f1_file)

with open(cover) as cover_file:
    cover_data = json.load(cover_file)

method_scores = {}

for m in methods:
    f1_scores_fixed = {}
    cover_scores_fixed = {}
    for k, v in every_names.items():
        f1_scores_fixed[v['window']] = {
            'score': f1_data[k][m],
            'name': v['name']
        }
        cover_scores_fixed[v['window']] = {
            'score': cover_data[k][m],
            'name': v['name']
        }
    f1_scores_random = {}
    cover_scores_random = {}
    for k, v in random_names.items():
        f1_scores_random[v['window']] = {
            'score': f1_data[k][m],
            'name': v['name']
        }
        cover_scores_random[v['window']] = {
            'score': cover_data[k][m],
            'name': v['name']
        }
    f1_scores_fixed = sorted(f1_scores_fixed.items(), key=lambda s: s[0])
    cover_scores_fixed = sorted(cover_scores_fixed.items(), key=lambda s: s[0])
    f1_scores_random = sorted(f1_scores_random.items(), key=lambda s: s[0])
    cover_scores_random = sorted(cover_scores_random.items(), key=lambda s: s[0])

    fixed_windows = []
    f1_scores_fixed_y = []
    cover_scores_fixed_y = []
    for i in range(len(f1_scores_fixed)):
        fixed_windows.append(f1_scores_fixed[i][0])
        f1_scores_fixed_y.append(f1_scores_fixed[i][1]['score'])
        cover_scores_fixed_y.append(cover_scores_fixed[i][1]['score'])

    random_windows = []
    f1_scores_random_y = []
    cover_scores_random_y = []
    for i in range(len(f1_scores_random)):
        random_windows.append(f1_scores_random[i][0])
        f1_scores_random_y.append(f1_scores_random[i][1]['score'])
        cover_scores_random_y.append(cover_scores_random[i][1]['score'])

    method_scores[m] = {}
    method_scores[m]['Fixed'] = {}
    method_scores[m]['Fixed']['x'] = fixed_windows
    method_scores[m]['Fixed']['F1'] = f1_scores_fixed_y
    method_scores[m]['Fixed']['Coverage'] = cover_scores_fixed_y
    method_scores[m]['Random'] = {}
    method_scores[m]['Random']['x'] = random_windows
    method_scores[m]['Random']['F1'] = f1_scores_random_y
    method_scores[m]['Random']['Coverage'] = cover_scores_random_y

for window_type in ['Fixed', 'Random']:
    for metric in ['F1', 'Coverage']:
        for m in methods:
            x = method_scores[m][window_type]['x']
            y = method_scores[m][window_type][metric]
            plot(x, y, label=m, )
        pyplot.legend(bbox_to_anchor=(1, 1))
        # pyplot.tight_layout()
        pyplot.xlabel(window_type + " Window Size")
        pyplot.ylabel(metric + " Score")
        pyplot.title(metric + " Score vs " + window_type + " Window Size")
        pyplot.grid()
        pyplot.savefig('graphs/' + window_type + '_window_' + metric + '.png', bbox_inches='tight')
        pyplot.close()
        # pyplot.show()

for window_type in ['Fixed', 'Random']:
    for m in methods:
        pyplot.ylim(0, 1.2)
        for metric in ['F1', 'Coverage']:
            x = method_scores[m][window_type]['x']
            y = method_scores[m][window_type][metric]
            plot(x, y, 'o', label=metric + ' score')
        pyplot.legend(bbox_to_anchor=(1, 1))
        # pyplot.tight_layout()
        pyplot.xlabel(window_type + " Window Size")
        pyplot.ylabel(" Score")
        pyplot.title(" Score vs " + window_type + " Window Size")
        pyplot.grid()
        pyplot.savefig('graphs/' + m + '_' + window_type + '.png', bbox_inches='tight')
        pyplot.close()

timing_length_x = [500, 1000, 2000]
timing_length_ys = {
    "amoc": [1.00, 1.01, 1.02],
    "binseg": [1.01, 1.01, 1.04],
    "bocpd": [1.14, 1.64, 2.93],
    "cpnp": [1.04, 1.06, 1.15],
    "pelt": [1.00, 1.01, 1.02],
    "rfpop": [0.81, 0.81, 0.84],
    "segneigh": [1.16, 1.53, 2.86],
    "wbs": [0.86, 0.89, 0.93],
    "zero": [0.20, 0.21, 0.20],
}
for method, y in timing_length_ys.items():
    plot(timing_length_x, y, label=method, )
pyplot.legend(bbox_to_anchor=(1, 1))
pyplot.xlabel("Data length")
pyplot.ylabel("Execution Time (s)")
pyplot.xlim(400, 2100)
pyplot.ylim(0, 3)
pyplot.title("Execution Time vs Data Length")
pyplot.grid()
pyplot.savefig('graphs/time_vs_length.png', bbox_inches='tight')
pyplot.close()

timing_window_x = [20, 200, 400]
timing_window_ys = {
    "amoc": [1.02, 1.02, 1.03],
    "binseg": [1.03, 1.04, 1.03],
    "bocpd": [2.93, 2.93, 2.92],
    "cpnp": [1.24, 1.15, 1.17],
    "pelt": [1.03, 1.02, 1.04],
    "rfpop": [0.84, 0.84, 0.84],
    "segneigh": [2.88, 2.86, 2.83],
    "wbs": [0.92, 0.93, 0.93],
    "zero": [0.20, 0.20, 0.20],
}
for method, y in timing_window_ys.items():
    plot(timing_window_x, y, label=method, )
pyplot.legend(bbox_to_anchor=(1, 1))
pyplot.xlabel("Window size")
pyplot.ylabel("Execution Time (s)")
pyplot.xlim(0, 420)
pyplot.ylim(0, 3)
pyplot.title("Execution Time vs Window Size")
pyplot.grid()
pyplot.savefig('graphs/time_vs_window.png', bbox_inches='tight')
pyplot.close()

length_scores = {}
for m in methods:
    scores_f1 = {}
    scores_cover = {}
    for k, v in length_names.items():
        scores_f1[v['length']] = f1_data[k][m]
        scores_cover[v['length']] = cover_data[k][m]
    length_scores[m] = {
        "f1": scores_f1,
        "cover": scores_cover
    }
print(json.dumps(length_scores, indent=4))

print('done')
