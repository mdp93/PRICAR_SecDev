import json
import copy

import matplotlib
import matplotlib.pyplot as plt
import ruptures as rpt
import numpy as np
from sklearn.neighbors import KernelDensity
import scipy.stats as stats
from sklearn import metrics
import random
import scipy.signal as signal

matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams['savefig.dpi'] = 200


def get_data():
    fingerprints = []
    with open('fingerprints.txt') as fingerprints_file:
        for line in fingerprints_file:
            if line:
                fingerprints.append(float(line))
    fingerprints = np.array(fingerprints)

    scores = []
    with open('scores.txt') as scores_file:
        for line in scores_file:
            if line:
                scores.append(float(line))
    scores = np.array(scores)

    # raw signals
    # fig, axs = plt.subplots(1, 2)
    # fig.suptitle('Signal histograms')
    # axs[0].set_ylabel('Count')
    # axs[0].hist(fingerprints)
    # axs[0].set_xlabel('Fingerprints')
    # axs[1].hist(scores)
    # axs[1].set_xlabel('Scores')
    # fig.align_labels()
    # plt.show()

    # adjust scores and fingerprints to be between 0 and 1
    scores = (scores + 1) / 2
    fingerprints = ((fingerprints - 1) / 10)
    # make fingerprints in the same range as the scores
    fingerprints = fingerprints * 0.018 + 0.003

    # make kde of scores - need more data
    scores_kde = stats.gaussian_kde(scores)

    return scores_kde, fingerprints


def graph_malicious(_malicious, image_location):
    _x = np.array(range(0, len(_malicious)))
    plt.plot(_x, _malicious)
    plt.title('Timeseries view of malicious signal')
    plt.ylabel('Signal value')
    plt.xlabel('Signal index')
    plt.savefig(image_location, bbox_inches='tight')
    plt.close()


def save_malicious(_malicious, series_name, series_location):
    # normalize data to mean zero, deviation one for use in TCPDBenchmark suite
    _malicious = (_malicious - _malicious.mean()) / _malicious.std()
    dataset = {'name': series_name, 'longname': 'Driver Scores', 'n_obs': len(_malicious), 'n_dim': 1}
    time = {'index': [i for i in range(0, len(_malicious))]}
    dataset['time'] = time
    series = [{
        'label': 'Score',
        'type': 'float',
        'raw': [float('%.10f' % x) for x in _malicious.tolist()]
    }]
    dataset['series'] = series
    with open(series_location, 'w') as outfile:
        json.dump(dataset, outfile, indent=4)


def save_series_name_to_batch(series_name, batch_file):
    with open(batch_file, 'a') as batch:
        print('"' + series_name + '",', file=batch)


def every_save_series_name_to_names(series_name, window_size, length, names_file):
    series = {
        "name": "Every " + str(window_size // 2) + ', ' + str(length),
        "window": window_size // 2
    }
    with open(names_file, 'a') as names:
        print('"' + series_name + '": ' + json.dumps(series, indent=4) + ',', file=names)


def random_save_series_name_to_names(series_name, length, num_cps, names_file):
    series = {
        "name": str(num_cps) + " Random",
        "window": length / (1 + num_cps)
    }
    with open(names_file, 'a') as names:
        print('"' + series_name + '": ' + json.dumps(series, indent=4) + ',', file=names)


def save_correct_changepoints(series_name, cps, cp_list):
    series_cps = {
        "6": cps
    }
    with open(cp_list, 'a') as names:
        print('"' + series_name + '": ' + json.dumps(series_cps, indent=4) + ',', file=names)


def generate_fixed_window_series(series_output_folder, window_size, length):
    _scores_kde, _fingerprints = get_data()
    batch_list = series_output_folder + '.txt'
    names_list = series_output_folder + '_names.txt'
    cp_list = series_output_folder + '_cps.txt'

    _malicious = []
    cp = 0
    correct_cps = []
    scores_chunk = _scores_kde.resample(length * 2)[0]
    scores_chunk = scores_chunk[(scores_chunk >= 0) & (scores_chunk <= 1)]

    for i in range(0, length - window_size, window_size):
        _malicious.append(scores_chunk[0:(window_size // 2)])
        correct_cps.append(cp + window_size // 2)
        cp += window_size // 2
        scores_chunk = scores_chunk[(window_size // 2):]
        fingerprints_choice = np.random.choice(len(_fingerprints), window_size // 2)
        fingerprints_chunk = _fingerprints[fingerprints_choice]
        _fingerprints = np.delete(_fingerprints, fingerprints_choice)
        _malicious.append(fingerprints_chunk)
        correct_cps.append(cp + window_size // 2)
        cp += window_size // 2
    remaining = length - cp
    if remaining > window_size // 2:
        _malicious.append(scores_chunk[0:(window_size // 2)])
        correct_cps.append(cp + window_size // 2)
        cp += window_size // 2
        remaining = length - cp
        fingerprints_choice = np.random.choice(len(_fingerprints), remaining)
        fingerprints_chunk = _fingerprints[fingerprints_choice]
        _malicious.append(fingerprints_chunk)
    else:
        _malicious.append(scores_chunk[0:remaining])

    _malicious = np.concatenate(_malicious)
    print(len(_malicious))
    print(len(_malicious) == length)
    series_name = 'driver_scores_every' + str(window_size) + '_' + str(length)
    graph_malicious(_malicious, series_output_folder + '/images/' + series_name + '.png')
    save_malicious(_malicious, series_name, series_output_folder + '/' + series_name + '.json')
    save_series_name_to_batch(series_name, series_output_folder + '/' + batch_list)
    every_save_series_name_to_names(series_name, window_size, length, series_output_folder + '/' + names_list)
    save_correct_changepoints(series_name, correct_cps, series_output_folder + '/' + cp_list)


def generate_random_window_series(series_output_folder, num_cps):
    _scores_kde, _fingerprints = get_data()
    batch_list = series_output_folder + '.txt'
    names_list = series_output_folder + '_names.txt'
    cp_list = series_output_folder + '_cps.txt'

    length = 2000
    _malicious = []
    scores_chunk = _scores_kde.resample(length * 2)[0]
    scores_chunk = scores_chunk[(scores_chunk >= 0) & (scores_chunk <= 1)]

    # generate random changepoints then sort
    random_chunks = random.sample([i for i in range(1, length)], num_cps)
    random_chunks.sort()
    correct_cps = copy.deepcopy(random_chunks)
    random_chunks.insert(0, 0)
    random_chunks.insert(len(random_chunks), length)

    for i in range(0, len(random_chunks) - 2, 2):
        scores_len = random_chunks[i + 1] - random_chunks[i]
        _malicious.append(scores_chunk[0:scores_len])
        scores_chunk = scores_chunk[scores_len:]
        fingerprint_len = random_chunks[i + 2] - random_chunks[i + 1]
        fingerprints_choice = np.random.choice(len(_fingerprints), fingerprint_len)
        fingerprints_added = _fingerprints[fingerprints_choice]
        _fingerprints = np.delete(_fingerprints, fingerprints_choice)
        _malicious.append(fingerprints_added)
    if len(random_chunks) % 2 == 0:
        scores_len = random_chunks[len(random_chunks) - 1] - random_chunks[len(random_chunks) - 2]
        _malicious.append(scores_chunk[0:scores_len])

    _malicious = np.concatenate(_malicious)
    print(len(_malicious))
    print(len(_malicious) == length)
    series_name = 'driver_scores_random' + str(num_cps)
    graph_malicious(_malicious, series_output_folder + '/images/' + series_name + '.png')
    save_malicious(_malicious, series_name, series_output_folder + '/' + series_name + '.json')
    save_series_name_to_batch(series_name, batch_list)
    random_save_series_name_to_names(series_name, length, num_cps, names_list)
    save_correct_changepoints(series_name, correct_cps, cp_list)


if __name__ == "__main__":
    # batch1 = [i for i in range(50, 2000, 50)]
    # for i in batch1:
    #     generate_fixed_window_series('batch1', 'series_images',
    #                                  'batch1/batch1.txt', 'batch1/names1.txt', 'batch1/change_points1.txt',
    #                                  i)

    # generate_fixed_window_series('batch5', 50, 25)
    # generate_fixed_window_series('batch5', 50, 50)
    # generate_fixed_window_series('batch5', 50, 75)
    # generate_fixed_window_series('batch5', 50, 100)
    # generate_fixed_window_series('batch5', 50, 150)
    # generate_fixed_window_series('batch5', 50, 200)
    # for length in range(250, 2000, 50):
    #     generate_fixed_window_series('batch5', 50, length)

    generate_fixed_window_series('batch6', 20, 10)
    generate_fixed_window_series('batch6', 20, 20)
    generate_fixed_window_series('batch6', 20, 30)
    generate_fixed_window_series('batch6', 20, 40)
    for length in range(50, 2000, 50):
        generate_fixed_window_series('batch6', 20, length)

    for length in range(50, 2000, 50):
        generate_fixed_window_series('batch7', 100, length)

    for length in range(100, 2000, 50):
        generate_fixed_window_series('batch8', 200, length)

    # batch2 = [i for i in range(5, 100, 5)]
    # for i in batch2:
    #     generate_random_window_series('batch2', 'series_images',
    #                                   'batch2/batch2.txt', 'batch2/names2.txt', 'batch2/change_points2.txt',
    #                                   i)

    # only driver scores:
    # scores_chunk = scores_kde.resample(4000)[0]
    # scores_chunk = scores_chunk[(scores_chunk >= 0) & (scores_chunk <= 1)]
    # malicious = scores_chunk[0:2000]

    # fig, axs = plt.subplots(1, 3)
    # fig.suptitle('Adjusted signal histograms')
    # axs[0].set_ylabel('Count')
    # axs[0].hist(fingerprints)
    # axs[0].set_xlabel('Fingerprints')
    # axs[1].hist(scores)
    # axs[1].set_xlabel('Scores')
    # axs[2].hist(malicious)
    # axs[2].set_xlabel('Malicious')
    # fig.align_labels()
    # plt.show()

    # fig, axs = plt.subplots(1, 2)
    # plt.title('Scores distribution')
    # plt.ylabel('Count')
    # plt.hist(scores, bins=15)
    # plt.xlabel('Scores')
    # plt.show()

    # plt.title('Resampled Scores distribution')
    # plt.ylabel('Count')
    # plt.hist(malicious, bins=20)
    # plt.xlabel('Scores')
    # plt.show()

    # sp = np.fft.fft(malicious)
    # freq = np.fft.fftfreq(malicious.shape[-1])
    #
    # magnitude = np.sqrt(sp.real * sp.real + sp.imag * sp.imag)
    #
    # plt.plot(freq, magnitude)
    # plt.show()
