import json

import matplotlib
from matplotlib import pyplot
from matplotlib.pyplot import plot
import bisect

matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams['savefig.dpi'] = 200

# driver_scores_none
# driver_scores_pure

cover = "best_cover_uni_full.json"
f1 = "best_f1_uni_full.json"

names20 = {
    "driver_scores_every20_10": {
        "name": "Every 10, 10",
        "window": 10
    },
    "driver_scores_every20_20": {
        "name": "Every 10, 20",
        "window": 10
    },
    "driver_scores_every20_30": {
        "name": "Every 10, 30",
        "window": 10
    },
    "driver_scores_every20_40": {
        "name": "Every 10, 40",
        "window": 10
    },
    "driver_scores_every20_50": {
        "name": "Every 10, 50",
        "window": 10
    },
    "driver_scores_every20_100": {
        "name": "Every 10, 100",
        "window": 10
    },
    "driver_scores_every20_150": {
        "name": "Every 10, 150",
        "window": 10
    },
    "driver_scores_every20_200": {
        "name": "Every 10, 200",
        "window": 10
    },
    "driver_scores_every20_250": {
        "name": "Every 10, 250",
        "window": 10
    },
    "driver_scores_every20_300": {
        "name": "Every 10, 300",
        "window": 10
    },
    "driver_scores_every20_350": {
        "name": "Every 10, 350",
        "window": 10
    },
    "driver_scores_every20_400": {
        "name": "Every 10, 400",
        "window": 10
    },
    "driver_scores_every20_450": {
        "name": "Every 10, 450",
        "window": 10
    },
    "driver_scores_every20_500": {
        "name": "Every 10, 500",
        "window": 10
    },
    "driver_scores_every20_550": {
        "name": "Every 10, 550",
        "window": 10
    },
    "driver_scores_every20_600": {
        "name": "Every 10, 600",
        "window": 10
    },
    "driver_scores_every20_650": {
        "name": "Every 10, 650",
        "window": 10
    },
    "driver_scores_every20_700": {
        "name": "Every 10, 700",
        "window": 10
    },
    "driver_scores_every20_750": {
        "name": "Every 10, 750",
        "window": 10
    },
    "driver_scores_every20_800": {
        "name": "Every 10, 800",
        "window": 10
    },
    "driver_scores_every20_850": {
        "name": "Every 10, 850",
        "window": 10
    },
    "driver_scores_every20_900": {
        "name": "Every 10, 900",
        "window": 10
    },
    "driver_scores_every20_950": {
        "name": "Every 10, 950",
        "window": 10
    },
    "driver_scores_every20_1000": {
        "name": "Every 10, 1000",
        "window": 10
    },
    "driver_scores_every20_1050": {
        "name": "Every 10, 1050",
        "window": 10
    },
    "driver_scores_every20_1100": {
        "name": "Every 10, 1100",
        "window": 10
    },
    "driver_scores_every20_1150": {
        "name": "Every 10, 1150",
        "window": 10
    },
    "driver_scores_every20_1200": {
        "name": "Every 10, 1200",
        "window": 10
    },
    "driver_scores_every20_1250": {
        "name": "Every 10, 1250",
        "window": 10
    },
    "driver_scores_every20_1300": {
        "name": "Every 10, 1300",
        "window": 10
    },
    "driver_scores_every20_1350": {
        "name": "Every 10, 1350",
        "window": 10
    },
    "driver_scores_every20_1400": {
        "name": "Every 10, 1400",
        "window": 10
    },
    "driver_scores_every20_1450": {
        "name": "Every 10, 1450",
        "window": 10
    },
    "driver_scores_every20_1500": {
        "name": "Every 10, 1500",
        "window": 10
    },
    "driver_scores_every20_1550": {
        "name": "Every 10, 1550",
        "window": 10
    },
    "driver_scores_every20_1600": {
        "name": "Every 10, 1600",
        "window": 10
    },
    "driver_scores_every20_1650": {
        "name": "Every 10, 1650",
        "window": 10
    },
    "driver_scores_every20_1700": {
        "name": "Every 10, 1700",
        "window": 10
    },
    "driver_scores_every20_1750": {
        "name": "Every 10, 1750",
        "window": 10
    },
    "driver_scores_every20_1800": {
        "name": "Every 10, 1800",
        "window": 10
    },
    "driver_scores_every20_1850": {
        "name": "Every 10, 1850",
        "window": 10
    },
    "driver_scores_every20_1900": {
        "name": "Every 10, 1900",
        "window": 10
    },
    "driver_scores_every20_1950": {
        "name": "Every 10, 1950",
        "window": 10
    },

}
names50 = {
    "driver_scores_every50_25": {
        "name": "Every 25, 25",
        "window": 25
    },
    "driver_scores_every50_50": {
        "name": "Every 25, 50",
        "window": 25
    },
    "driver_scores_every50_75": {
        "name": "Every 25, 75",
        "window": 25
    },
    "driver_scores_every50_100": {
        "name": "Every 25, 100",
        "window": 25
    },
    "driver_scores_every50_150": {
        "name": "Every 25, 150",
        "window": 25
    },
    "driver_scores_every50_250": {
        "name": "Every 25, 250",
        "window": 25
    },
    "driver_scores_every50_300": {
        "name": "Every 25, 300",
        "window": 25
    },
    "driver_scores_every50_350": {
        "name": "Every 25, 350",
        "window": 25
    },
    "driver_scores_every50_400": {
        "name": "Every 25, 400",
        "window": 25
    },
    "driver_scores_every50_450": {
        "name": "Every 25, 450",
        "window": 25
    },
    "driver_scores_every50_500": {
        "name": "Every 25, 500",
        "window": 25
    },
    "driver_scores_every50_550": {
        "name": "Every 25, 550",
        "window": 25
    },
    "driver_scores_every50_600": {
        "name": "Every 25, 600",
        "window": 25
    },
    "driver_scores_every50_650": {
        "name": "Every 25, 650",
        "window": 25
    },
    "driver_scores_every50_700": {
        "name": "Every 25, 700",
        "window": 25
    },
    "driver_scores_every50_750": {
        "name": "Every 25, 750",
        "window": 25
    },
    "driver_scores_every50_800": {
        "name": "Every 25, 800",
        "window": 25
    },
    "driver_scores_every50_850": {
        "name": "Every 25, 850",
        "window": 25
    },
    "driver_scores_every50_900": {
        "name": "Every 25, 900",
        "window": 25
    },
    "driver_scores_every50_950": {
        "name": "Every 25, 950",
        "window": 25
    },
    "driver_scores_every50_1000": {
        "name": "Every 25, 1000",
        "window": 25
    },
    "driver_scores_every50_1050": {
        "name": "Every 25, 1050",
        "window": 25
    },
    "driver_scores_every50_1100": {
        "name": "Every 25, 1100",
        "window": 25
    },
    "driver_scores_every50_1150": {
        "name": "Every 25, 1150",
        "window": 25
    },
    "driver_scores_every50_1200": {
        "name": "Every 25, 1200",
        "window": 25
    },
    "driver_scores_every50_1250": {
        "name": "Every 25, 1250",
        "window": 25
    },
    "driver_scores_every50_1300": {
        "name": "Every 25, 1300",
        "window": 25
    },
    "driver_scores_every50_1350": {
        "name": "Every 25, 1350",
        "window": 25
    },
    "driver_scores_every50_1400": {
        "name": "Every 25, 1400",
        "window": 25
    },
    "driver_scores_every50_1450": {
        "name": "Every 25, 1450",
        "window": 25
    },
    "driver_scores_every50_1500": {
        "name": "Every 25, 1500",
        "window": 25
    },
    "driver_scores_every50_1550": {
        "name": "Every 25, 1550",
        "window": 25
    },
    "driver_scores_every50_1600": {
        "name": "Every 25, 1600",
        "window": 25
    },
    "driver_scores_every50_1650": {
        "name": "Every 25, 1650",
        "window": 25
    },
    "driver_scores_every50_1700": {
        "name": "Every 25, 1700",
        "window": 25
    },
    "driver_scores_every50_1750": {
        "name": "Every 25, 1750",
        "window": 25
    },
    "driver_scores_every50_1800": {
        "name": "Every 25, 1800",
        "window": 25
    },
    "driver_scores_every50_1850": {
        "name": "Every 25, 1850",
        "window": 25
    },
    "driver_scores_every50_1900": {
        "name": "Every 25, 1900",
        "window": 25
    },
    "driver_scores_every50_1950": {
        "name": "Every 25, 1950",
        "window": 25
    },
    "driver_scores_every50_200": {
        "name": "Every 25, 200",
        "window": 25
    },

}
names100 = {
    "driver_scores_every100_50": {
        "name": "Every 50, 50",
        "window": 50
    },
    "driver_scores_every100_100": {
        "name": "Every 50, 100",
        "window": 50
    },
    "driver_scores_every100_150": {
        "name": "Every 50, 150",
        "window": 50
    },
    "driver_scores_every100_200": {
        "name": "Every 50, 200",
        "window": 50
    },
    "driver_scores_every100_250": {
        "name": "Every 50, 250",
        "window": 50
    },
    "driver_scores_every100_300": {
        "name": "Every 50, 300",
        "window": 50
    },
    "driver_scores_every100_350": {
        "name": "Every 50, 350",
        "window": 50
    },
    "driver_scores_every100_400": {
        "name": "Every 50, 400",
        "window": 50
    },
    "driver_scores_every100_450": {
        "name": "Every 50, 450",
        "window": 50
    },
    "driver_scores_every100_500": {
        "name": "Every 50, 500",
        "window": 50
    },
    "driver_scores_every100_550": {
        "name": "Every 50, 550",
        "window": 50
    },
    "driver_scores_every100_600": {
        "name": "Every 50, 600",
        "window": 50
    },
    "driver_scores_every100_650": {
        "name": "Every 50, 650",
        "window": 50
    },
    "driver_scores_every100_700": {
        "name": "Every 50, 700",
        "window": 50
    },
    "driver_scores_every100_750": {
        "name": "Every 50, 750",
        "window": 50
    },
    "driver_scores_every100_800": {
        "name": "Every 50, 800",
        "window": 50
    },
    "driver_scores_every100_850": {
        "name": "Every 50, 850",
        "window": 50
    },
    "driver_scores_every100_900": {
        "name": "Every 50, 900",
        "window": 50
    },
    "driver_scores_every100_950": {
        "name": "Every 50, 950",
        "window": 50
    },
    "driver_scores_every100_1000": {
        "name": "Every 50, 1000",
        "window": 50
    },
    "driver_scores_every100_1050": {
        "name": "Every 50, 1050",
        "window": 50
    },
    "driver_scores_every100_1100": {
        "name": "Every 50, 1100",
        "window": 50
    },
    "driver_scores_every100_1150": {
        "name": "Every 50, 1150",
        "window": 50
    },
    "driver_scores_every100_1200": {
        "name": "Every 50, 1200",
        "window": 50
    },
    "driver_scores_every100_1250": {
        "name": "Every 50, 1250",
        "window": 50
    },
    "driver_scores_every100_1300": {
        "name": "Every 50, 1300",
        "window": 50
    },
    "driver_scores_every100_1350": {
        "name": "Every 50, 1350",
        "window": 50
    },
    "driver_scores_every100_1400": {
        "name": "Every 50, 1400",
        "window": 50
    },
    "driver_scores_every100_1450": {
        "name": "Every 50, 1450",
        "window": 50
    },
    "driver_scores_every100_1500": {
        "name": "Every 50, 1500",
        "window": 50
    },
    "driver_scores_every100_1550": {
        "name": "Every 50, 1550",
        "window": 50
    },
    "driver_scores_every100_1600": {
        "name": "Every 50, 1600",
        "window": 50
    },
    "driver_scores_every100_1650": {
        "name": "Every 50, 1650",
        "window": 50
    },
    "driver_scores_every100_1700": {
        "name": "Every 50, 1700",
        "window": 50
    },
    "driver_scores_every100_1750": {
        "name": "Every 50, 1750",
        "window": 50
    },
    "driver_scores_every100_1800": {
        "name": "Every 50, 1800",
        "window": 50
    },
    "driver_scores_every100_1850": {
        "name": "Every 50, 1850",
        "window": 50
    },
    "driver_scores_every100_1900": {
        "name": "Every 50, 1900",
        "window": 50
    },
    "driver_scores_every100_1950": {
        "name": "Every 50, 1950",
        "window": 50
    },

}
names200 = {
    "driver_scores_every200_100": {
        "name": "Every 100, 100",
        "window": 100
    },
    "driver_scores_every200_150": {
        "name": "Every 100, 150",
        "window": 100
    },
    "driver_scores_every200_200": {
        "name": "Every 100, 200",
        "window": 100
    },
    "driver_scores_every200_250": {
        "name": "Every 100, 250",
        "window": 100
    },
    "driver_scores_every200_300": {
        "name": "Every 100, 300",
        "window": 100
    },
    "driver_scores_every200_350": {
        "name": "Every 100, 350",
        "window": 100
    },
    "driver_scores_every200_400": {
        "name": "Every 100, 400",
        "window": 100
    },
    "driver_scores_every200_450": {
        "name": "Every 100, 450",
        "window": 100
    },
    "driver_scores_every200_500": {
        "name": "Every 100, 500",
        "window": 100
    },
    "driver_scores_every200_550": {
        "name": "Every 100, 550",
        "window": 100
    },
    "driver_scores_every200_600": {
        "name": "Every 100, 600",
        "window": 100
    },
    "driver_scores_every200_650": {
        "name": "Every 100, 650",
        "window": 100
    },
    "driver_scores_every200_700": {
        "name": "Every 100, 700",
        "window": 100
    },
    "driver_scores_every200_750": {
        "name": "Every 100, 750",
        "window": 100
    },
    "driver_scores_every200_800": {
        "name": "Every 100, 800",
        "window": 100
    },
    "driver_scores_every200_850": {
        "name": "Every 100, 850",
        "window": 100
    },
    "driver_scores_every200_900": {
        "name": "Every 100, 900",
        "window": 100
    },
    "driver_scores_every200_950": {
        "name": "Every 100, 950",
        "window": 100
    },
    "driver_scores_every200_1000": {
        "name": "Every 100, 1000",
        "window": 100
    },
    "driver_scores_every200_1050": {
        "name": "Every 100, 1050",
        "window": 100
    },
    "driver_scores_every200_1100": {
        "name": "Every 100, 1100",
        "window": 100
    },
    "driver_scores_every200_1150": {
        "name": "Every 100, 1150",
        "window": 100
    },
    "driver_scores_every200_1200": {
        "name": "Every 100, 1200",
        "window": 100
    },
    "driver_scores_every200_1250": {
        "name": "Every 100, 1250",
        "window": 100
    },
    "driver_scores_every200_1300": {
        "name": "Every 100, 1300",
        "window": 100
    },
    "driver_scores_every200_1350": {
        "name": "Every 100, 1350",
        "window": 100
    },
    "driver_scores_every200_1400": {
        "name": "Every 100, 1400",
        "window": 100
    },
    "driver_scores_every200_1450": {
        "name": "Every 100, 1450",
        "window": 100
    },
    "driver_scores_every200_1500": {
        "name": "Every 100, 1500",
        "window": 100
    },
    "driver_scores_every200_1550": {
        "name": "Every 100, 1550",
        "window": 100
    },
    "driver_scores_every200_1600": {
        "name": "Every 100, 1600",
        "window": 100
    },
    "driver_scores_every200_1650": {
        "name": "Every 100, 1650",
        "window": 100
    },
    "driver_scores_every200_1700": {
        "name": "Every 100, 1700",
        "window": 100
    },
    "driver_scores_every200_1750": {
        "name": "Every 100, 1750",
        "window": 100
    },
    "driver_scores_every200_1800": {
        "name": "Every 100, 1800",
        "window": 100
    },
    "driver_scores_every200_1850": {
        "name": "Every 100, 1850",
        "window": 100
    },
    "driver_scores_every200_1900": {
        "name": "Every 100, 1900",
        "window": 100
    },
    "driver_scores_every200_1950": {
        "name": "Every 100, 1950",
        "window": 100
    },

}

windows = {
    10: names20,
    25: names50,
    50: names100,
    100: names200
}

with open(f1) as f1_file:
    f1_data = json.load(f1_file)

with open(cover) as cover_file:
    cover_data = json.load(cover_file)

window_scores = {
    10: {
        "cpnp_f": [],
        "pelt_f": [],
        "cpnp_c": [],
        "pelt_c": [],
        "lengths": []
    },
    25: {
        "cpnp_f": [],
        "pelt_f": [],
        "cpnp_c": [],
        "pelt_c": [],
        "lengths": []
    },
    50: {
        "cpnp_f": [],
        "pelt_f": [],
        "cpnp_c": [],
        "pelt_c": [],
        "lengths": []
    },
    100: {
        "cpnp_f": [],
        "pelt_f": [],
        "cpnp_c": [],
        "pelt_c": [],
        "lengths": []
    }
}

f1_scores_fixed = {}
cover_scores_fixed = {}
for w, names in windows.items():
    for k, v in names.items():
        length = int(k.split('_')[-1])
        i = bisect.bisect_left(window_scores[w]['lengths'], length)
        window_scores[w]['lengths'].insert(i, length)
        window_scores[w]['cpnp_f'].insert(i, f1_data[k]['cpnp'])
        window_scores[w]['pelt_f'].insert(i, f1_data[k]['pelt'])
        window_scores[w]['cpnp_c'].insert(i, cover_data[k]['cpnp'])
        window_scores[w]['pelt_c'].insert(i, cover_data[k]['pelt'])

for w, scores in window_scores.items():
    plot(scores['lengths'], scores['cpnp_f'], label="cpnp")
    plot(scores['lengths'], scores['pelt_f'], label="pelt")
    pyplot.legend(bbox_to_anchor=(1, 1))
    pyplot.xlabel("Batch Length")
    pyplot.ylabel("F1 Score")
    pyplot.title("F1 Score vs Batch Length, Window Size " + str(w))
    pyplot.grid()
    pyplot.savefig('graphs/window_' + str(w) + '_vs_length_f1.png', bbox_inches='tight')
    pyplot.close()
    plot(scores['lengths'], scores['cpnp_c'], label="cpnp")
    plot(scores['lengths'], scores['pelt_c'], label="pelt")
    pyplot.legend(bbox_to_anchor=(1, 1))
    pyplot.xlabel("Batch Length")
    pyplot.ylabel("Coverage Score")
    pyplot.title("Coverage Score vs Batch Length, Window Size " + str(w))
    pyplot.grid()
    pyplot.savefig('graphs/window_' + str(w) + '_vs_length_coverage.png', bbox_inches='tight')
    pyplot.close()
    # pyplot.show()

print('done')
