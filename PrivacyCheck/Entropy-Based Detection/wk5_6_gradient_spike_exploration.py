# -*- coding: utf-8 -*-
"""Wk5-6: Gradient Spike Exploration

Automatically generated by Colaboratory.

# Helper Functions
"""

import json
import os
import random

import tabulate
import numpy as np
import scipy.stats as stats
import scipy.signal as signal
import matplotlib.pyplot as plt

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

def get_sliding_window_entropies(data, window_size):
  window = SlidingWindow(window_size)
  for i in range(window_size):
    window.push(np.nan)
  entropies = []
  for datum in data:
    window.push(datum)
    entropy = calculate_shannon_entropy(window.data)
    entropies.append(entropy)
  return entropies

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
  plt.xlabel("Timestep")
  plt.ylabel("Shannon Entropy (bits)")
  plt.title(filename.split("/")[-1])

def plot_colored_gradient(filename, window_size=100):
  data = get_data(filename)
  calculate_shannon_entropy(data)
  entropies = get_sliding_window_entropies(data, window_size)
  gradients = np.gradient(entropies)
  changepoints = get_correct_changepoints(filename)
  labeled_data = get_data_labels(changepoints, len(data))

  #partition data into anomaly and valid
  valid, anomaly = partition_array(gradients, labeled_data)
  
  plt.figure(figsize=(19.2,4.8)) 
  plt.plot(valid, color="b")
  plt.plot(anomaly, color="r")
  plt.xlabel("Timestep")
  plt.ylabel("Shannon Entropy (bits)")
  plt.title(filename.split("/")[-1])

def analyze_predictions(predicted_anomalies, real_anomalies):
  correct_anomalies = 0
  correct_normal = 0
  normal_classified_as_anomaly = 0
  anomaly_classified_as_normal = 0
  n = len(predicted_anomalies)

  for i in range(n):
    if real_anomalies[i] and predicted_anomalies[i]:
      correct_anomalies += 1
    elif real_anomalies[i] and not predicted_anomalies[i]:
      anomaly_classified_as_normal += 1
    elif not real_anomalies[i] and not predicted_anomalies[i]:
      correct_normal += 1
    elif not real_anomalies[i] and predicted_anomalies[i]:
      normal_classified_as_anomaly += 1

  return correct_anomalies, correct_normal, normal_classified_as_anomaly, anomaly_classified_as_normal

def calculate_f1_of_predictions(predicted_anomalies, real_anomalies):
  correct_anomalies, correct_normal, normal_classified_as_anomaly, anomaly_classified_as_normal = analyze_predictions(predicted_anomalies, real_anomalies)
  precision = correct_anomalies / (correct_anomalies + normal_classified_as_anomaly)
  recall = correct_anomalies / (correct_anomalies + anomaly_classified_as_normal)

  return stats.hmean([precision, recall])

def plot_incorrect_predictions(entropy_data, predicted_anomalies, real_anomalies):
  assert len(predicted_anomalies) == len(real_anomalies)
  correct_predictions = []
  for i in range(len(predicted_anomalies)):
    correct_predictions.append(predicted_anomalies[i] == real_anomalies[i])

  #partition array based on correctness
  incorrect, correct = partition_array(entropy_data, correct_predictions)

  plt.plot(incorrect, color="r")
  plt.plot(correct, color="k")
  plt.xlabel("Timestep")
  plt.ylabel("Shannon Entropy (bits)")
  plt.title(filename.split("/")[-1])

def gradient_anomaly_detection(data, window_size):
  e = get_sliding_window_entropies(data, window_size)
  der = np.gradient(e)
  return calculate_f1_of_predictions([g < 0.0099 for g in der], labeled_data)

#order of input: [True Positive    True Negative    False Positive    False Negative]
def print_results(data):
  headers = ["Method", "Sensitivity", "Specificity"]
  processed_data = []
  for row in data:
    sensitivity = row[1] / (row[1] + row[4])
    specificity = row[2] / (row[2] + row[3])
    processed_data.append([row[0], sensitivity, specificity])
  print(tabulate.tabulate(processed_data, headers=headers))

"""# Gradient Spike Detection"""

filename = "/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random200.json"
window_size = 100
plot_colored_gradient(filename, window_size)

data = get_data(filename)
entropies = get_sliding_window_entropies(data, window_size)
gradients = np.gradient(entropies)
changepoints = get_correct_changepoints(filename)
labeled_data = get_data_labels(changepoints, len(data))

# smooth gradients
# for i in range(1, len(gradients) -1):
#   gradients[i] = (0.1 * gradients[i-1] + 0.8 * gradients[i] + 0.1*gradients[i+1])/3

#partition data into anomaly and valid
valid, anomaly = partition_array(gradients, labeled_data)

predictions = []
saturating_predictions = []
threshold = 0.0099
saturating_counter = 0
saturation_level = 2
spike_threshold = 0.02
ct = 0
current_spike = None
for gradient in gradients:
  # update spike if needed
  if abs(gradient) > spike_threshold:
    #increasing gradient implies valid data
    current_spike = gradient < threshold

    saturating_counter -= 2 * int(gradient < threshold) - 1
    saturating_counter = min(saturation_level, max(-1*saturation_level, saturating_counter))
    
    ct += 1
 
  if current_spike is None:
    prediction = gradient < threshold
    predictions.append(prediction)
  else:
    predictions.append(current_spike)

    if saturating_counter == 0:
      saturating_predictions.append(gradient < threshold)
    else:
      saturating_predictions.append(saturating_counter < 0)
  
#calculate f1 of new predictions
print(f"Gradient Prediction: {calculate_f1_of_predictions([gradient < 0.0099 for gradient in gradients], labeled_data)}")
print(f"Gradient Spike Prediction (threshold {spike_threshold}): {calculate_f1_of_predictions(predictions, labeled_data)}")
print(f"Gradient Spike Saturating Prediction (saturating to {saturation_level}): {calculate_f1_of_predictions(saturating_predictions, labeled_data)}")

def saturating_gradient_detection(data, saturation_level, threshold, spike_threshold):
  predictions = []
  saturating_predictions = []
  saturating_counter = 0
  current_spike = None
  for gradient in gradients:
    # update spike if needed
    if abs(gradient) > spike_threshold:
      #increasing gradient implies valid data
      current_spike = gradient < threshold

      saturating_counter -= 2 * int(gradient < threshold) - 1
      saturating_counter = min(saturation_level, max(-1*saturation_level, saturating_counter))
      
    if saturating_counter == 0:
      saturating_predictions.append(gradient < threshold)
    else:
      saturating_predictions.append(saturating_counter < 0)

  return saturating_predictions



"""# TP/FP Evaluation

"""

filename = "/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random400.json"
window_size = 100

data = get_data(filename)
entropies = get_sliding_window_entropies(data, window_size)
gradients = np.gradient(entropies)
changepoints = get_correct_changepoints(filename)
labeled_data = get_data_labels(changepoints, len(data))
predictions = [g < 0.0099 for g in gradients]

results = []

gradient_results = analyze_predictions(predictions, labeled_data)
results.append(["Gradient", *gradient_results])
print("Gradient F1:", calculate_f1_of_predictions(predictions, labeled_data))


saturating_predictions = saturating_gradient_detection(data, 1, 0.0099, 0.0)
saturating_results = analyze_predictions(saturating_predictions, labeled_data)
results.append(["Saturating", *saturating_results])
print("Saturating F1:", calculate_f1_of_predictions(saturating_predictions, labeled_data))
print_results(results)

"""#Window size's affect on performance (on same data for consistency)"""

filename = "/content/drive/MyDrive/School Work/Junior Year/Research/Input files/driver_scores_random2.json"

data = get_data(filename)
f1s = [gradient_anomaly_detection(data, w) for w in range(10,200)]

# f1test = []
# for w in range(10,30):
#   f1test.append(gradient_anomaly_detection(data, w))

print(f1s)
gradient_anomaly_detection(data, 10)

# cached f1 scores for random input files
f400 = [0.6550040683482506, 0.6402966625463535, 0.649671052631579, 0.6498135101533361, 0.654103852596315, 0.6458157227387996, 0.6371379897785349, 0.6517241379310345, 0.6620570440795159, 0.6658031088082902, 0.6666666666666666, 0.6704446381865737, 0.6651943462897526, 0.6687306501547988, 0.6702033598585323, 0.6901718818862936, 0.7049469964664311, 0.7018165706690297, 0.6894107221976075, 0.6878868258178603, 0.6870838881491346, 0.6997782705099779, 0.6991581745680107, 0.7008849557522123, 0.7028697571743929, 0.6829702089817696, 0.689376961004034, 0.6957303370786516, 0.696276357110812, 0.7060915962650067, 0.702775290957923, 0.710431654676259, 0.7061462539255271, 0.7086330935251799, 0.7144766146993319, 0.7104907699234578, 0.7164179104477612, 0.7269422989550204, 0.7301587301587301, 0.7195287720888083, 0.7146108329540283, 0.7072835547411819, 0.7305605786618444, 0.7324698526127735, 0.7218453188602442, 0.7097637093178779, 0.7102552619794, 0.7193533902110463, 0.7266996848266547, 0.7312894499549143, 0.732824427480916, 0.7342342342342342, 0.7350813743218807, 0.7273542600896861, 0.7330357142857143, 0.7302867383512545, 0.7371225577264654, 0.7421944692239073, 0.7421944692239073, 0.7346938775510203, 0.7399821905609973, 0.7474295932051855, 0.7456724367509987, 0.7406417112299465, 0.7470956210902591, 0.7451858486341245, 0.7526881720430108, 0.7543780871127077, 0.7553956834532375, 0.7433707865168538, 0.7548532731376976, 0.7658426966292136, 0.758896797153025, 0.7555555555555554, 0.7462019660411082, 0.7476635514018692, 0.7484554280670785, 0.744661921708185, 0.7438533750558785, 0.743831314490803, 0.743578188373141, 0.7477638640429338, 0.7522281639928698, 0.7492287351256058, 0.7524575513851653, 0.7533392698130008, 0.7534675615212528, 0.7492204899777284, 0.7576974564926372, 0.758744394618834, 0.7585899152164212, 0.7616511318242344, 0.7376623376623376, 0.7403218790778598, 0.7419354838709676, 0.7398091934084996, 0.7376623376623376, 0.7352051835853132, 0.7386215864759429, 0.7327070879590094, 0.7363013698630138, 0.7459086993970715, 0.7509677419354838, 0.7427078798432738, 0.7428821725799387, 0.7413945278022948, 0.7513089005235603, 0.7525098210388477, 0.7473958333333333, 0.7492473118279569, 0.7462039045553146, 0.7397141619748809, 0.7493517718236818, 0.7499999999999999, 0.7483645878761448, 0.7444492816717458, 0.7483645878761448, 0.7508710801393728, 0.7447735191637631, 0.7491289198606271, 0.7453362255965293, 0.7546678245766392, 0.7471958584987058, 0.7465277777777778, 0.7484769364664926, 0.7528187337380746, 0.7514002585092633, 0.7518279569892473, 0.7496757457846953, 0.7491349480968857, 0.7505385609651013, 0.7505422993492408, 0.751185855972402, 0.7491349480968857, 0.74814491488433, 0.7448275862068966, 0.7478336221837089, 0.755058114507103, 0.7540983606557377, 0.7562879444926279, 0.7423917702528933, 0.7488192357234864, 0.7525862068965516, 0.7564543889845095, 0.7412467976088812, 0.7449462365591397, 0.7514099783080261, 0.7594606350587212, 0.7541412380122058, 0.7542262678803642, 0.7524583155194527, 0.7470187393526406, 0.7457044673539518, 0.7506448839208941, 0.7529007305543618, 0.7435677530017153, 0.7550407550407552, 0.7517064846416381, 0.7526881720430106, 0.7510803802938634, 0.7477282561661618, 0.7499999999999999, 0.7532133676092545, 0.7507481829841813, 0.7481953290870488, 0.7441663131098855, 0.7467921300256629, 0.7458351131994874, 0.7427350427350428, 0.7523727351164797, 0.7506471095772217, 0.7549611734253666, 0.7607573149741824, 0.7427350427350428, 0.7466780968709815, 0.7520482966796032, 0.7478411053540588, 0.7543934847835404, 0.7555746140651801, 0.7540425531914893, 0.7509611277231952, 0.7564766839378237, 0.7582653499355948, 0.7502138579982892, 0.7563386334336055, 0.7498931167165456, 0.7508561643835616, 0.7404255319148936, 0.7407407407407407, 0.7395744680851064]
f200 = [0.622564935064935, 0.6326530612244897, 0.631578947368421, 0.6464478604071457, 0.6494156928213689, 0.6506935687263555, 0.6531474440219688, 0.6587737843551797, 0.6549807610089783, 0.6525862068965518, 0.6531492666091459, 0.6320836965998256, 0.6407682234831952, 0.651528384279476, 0.6657940663176265, 0.6759703445268207, 0.670464504820333, 0.6672558550596553, 0.6802120141342756, 0.6841870824053452, 0.694755714926042, 0.7086684539767649, 0.7163912460920053, 0.7136445242369839, 0.719642857142857, 0.7208888888888889, 0.7180400890868596, 0.7278368794326241, 0.724122612172368, 0.726063829787234, 0.7230837394771821, 0.7180400890868596, 0.7187222715173026, 0.710832587287377, 0.7190710138454667, 0.7153742716270731, 0.717720391807658, 0.7161921708185053, 0.7192118226600985, 0.7167420814479637, 0.7189896256202074, 0.7313769751693002, 0.7302304563940352, 0.7421555252387448, 0.7476297968397291, 0.7417158420335905, 0.7423340961098398, 0.7476125511596181, 0.7542908762420957, 0.7566832804712279, 0.7523852794184462, 0.7488667271078876, 0.7468239564428313, 0.7449025826914364, 0.742183960126869, 0.7446712018140589, 0.7488667271078876, 0.7460389316432775, 0.7412777526053466, 0.7394653375623018, 0.7403365165984539, 0.7423620611035112, 0.7459016393442623, 0.7446322521699406, 0.7472627737226276, 0.753543667123914, 0.752411575562701, 0.758557736193519, 0.7550274223034734, 0.7563636363636363, 0.758337140246688, 0.7683823529411765, 0.7719780219780219, 0.766697163769442, 0.7650022904260192, 0.7645709040844424, 0.7673992673992674, 0.7730560578661845, 0.7731397459165154, 0.7721691678035472, 0.7672727272727272, 0.7637687756030952, 0.7673357664233577, 0.777979981801638, 0.784510250569476, 0.7714025500910745, 0.7756030951297224, 0.7772685609532539, 0.7862385321100916, 0.7830446672743847, 0.779385171790235, 0.7768220914440923, 0.7541998231653404, 0.7506607929515419, 0.7617801047120419, 0.7574430823117337, 0.7570867858700391, 0.7572052401746724, 0.7674113009198424, 0.765938864628821, 0.7653461036134088, 0.761239633347883, 0.7545375972342264, 0.7501078981441519, 0.7579672695951766, 0.7591240875912408, 0.7588865096359743, 0.7598290598290598, 0.7552688172043012, 0.7506448839208941, 0.756287944492628, 0.753686036426713, 0.7487001733102253, 0.7456747404844292, 0.7513906718014549, 0.7537473233404711, 0.758443779392903, 0.7558785805899958, 0.7533020877716232, 0.7544910179640718, 0.7529007305543618, 0.7545064377682403, 0.7581755593803786, 0.7559395248380129, 0.7575496117342536, 0.753686036426713, 0.7564991334488735, 0.7564766839378239, 0.7553053269813772, 0.754240974336668, 0.7558239861949957, 0.7561080154307759, 0.7595370767252465, 0.7582653499355946, 0.7593628928110202, 0.7639484978540773, 0.7667097887020267, 0.7650367806144526, 0.762734000870701, 0.768361581920904, 0.7673611111111109, 0.7694974003466204, 0.7685627442466347, 0.7640156453715777, 0.7655502392344496, 0.7681660899653979, 0.7655172413793103, 0.7640449438202247, 0.7635105923043666, 0.7690311418685121, 0.764093668690373, 0.767170626349892, 0.7692307692307692, 0.7636676711149375, 0.7656116338751069, 0.7669819432502148, 0.7666523420713365, 0.7603092783505154, 0.7592988456605386, 0.7605995717344753, 0.7563386334336054, 0.7595698924731182, 0.7604301075268817, 0.7634177758694718, 0.7660491167600172, 0.7688984881209503, 0.7681660899653979, 0.7662671232876712, 0.7694944301628106, 0.76592082616179, 0.7664516129032258, 0.7685025817555938, 0.7703639514731369, 0.7708964919878736, 0.773747841105354, 0.7744165946413137, 0.7746660922016372, 0.7746113989637305, 0.7754749568221071, 0.775616083009079, 0.7748058671268334, 0.7669819432502148, 0.7657192075796726, 0.7622317596566524, 0.7580025608194622, 0.7599486521181, 0.7614561027837259, 0.7637457044673539, 0.7640256959314775, 0.7635425623387789]
f40 = [0.5565015479876161, 0.5501567398119123, 0.5570416994492525, 0.5647709320695102, 0.5694996028594123, 0.5662650602409639, 0.569814366424536, 0.5711960943856794, 0.5797219950940311, 0.5928338762214984, 0.5935589074602527, 0.6018706791378609, 0.6040049039640377, 0.6009892827699918, 0.6070103092783505, 0.6270841805612037, 0.624235006119951, 0.6320523303352413, 0.6335250616269514, 0.6385245901639345, 0.6403292181069958, 0.6444169756901524, 0.6430948419301166, 0.6471816283924844, 0.6694045174537987, 0.6647350993377484, 0.6641635377555277, 0.6680619506069485, 0.6733333333333333, 0.6747188671386922, 0.6835548172757475, 0.6913169921063564, 0.6957605985037406, 0.6909242994562944, 0.6966666666666667, 0.6945256999582115, 0.7022518765638032, 0.7018867924528301, 0.7090301003344482, 0.7185031185031184, 0.7197001249479383, 0.7281029472810294, 0.7321131447587356, 0.7318900915903414, 0.7333887043189369, 0.7308333333333333, 0.7335553705245629, 0.7365792759051186, 0.7466996699669968, 0.7492723492723492, 0.7521793275217933, 0.743237619642114, 0.7482254697286014, 0.749579831932773, 0.7542904981163667, 0.7617074181516783, 0.7600831600831601, 0.760914760914761, 0.7593360995850623, 0.7734989648033127, 0.7734439834024897, 0.7741666666666667, 0.7812630698452531, 0.7823899371069184, 0.7788057190916736, 0.7808564231738034, 0.7870913663034367, 0.7896060352053645, 0.7847571189279733, 0.7896277708071936, 0.7931751976695798, 0.7923269391159299, 0.790113112693758, 0.7961246840775063, 0.7932631578947367, 0.7875473285654186, 0.7971440571188575, 0.8040370058873002, 0.8013553578991953, 0.8011769651113912, 0.8010096760622634, 0.8094634558512884, 0.808421052631579, 0.8134171907756813, 0.8157124947764313, 0.8143812709030099, 0.8158995815899581, 0.8142557651991614, 0.8197820620284995, 0.8200589970501475, 0.8256107834877844, 0.8266331658291457, 0.8048484848484848, 0.8022690437601295, 0.8024340770791075, 0.8022644561261625, 0.801779935275081, 0.7969193352249695, 0.7985407377381434, 0.8021001615508886, 0.8049859268194611, 0.8097913322632424, 0.8028962188254225, 0.8025682182985554, 0.7998398718975179, 0.8, 0.8078306032760687, 0.8068772491003599, 0.801924619085806, 0.8022462896109105, 0.8035284683239776, 0.8027265437048918, 0.8022462896109105, 0.8051323175621492, 0.8056112224448899, 0.801762114537445, 0.7998398718975179, 0.8006443817962141, 0.8043478260869564, 0.8080321285140561, 0.8083067092651758, 0.8099239695878351, 0.8068772491003599, 0.8022417934347477, 0.8065678814577493, 0.8064, 0.8088353413654618, 0.8107242897158865, 0.8142799839550741, 0.8138319260152794, 0.8085782366957902, 0.8082572449384676, 0.8107893692978977, 0.8122270742358078, 0.8113282808137215, 0.8097521982414069, 0.8111776447105788, 0.8151696606786428, 0.8180007964954201, 0.8173497811380821, 0.8151999999999999, 0.8137765318382059, 0.815021973631642, 0.8178202068416864, 0.8230616302186878, 0.82104424073336, 0.8203902827558742, 0.8196328810853951, 0.8222133439872154, 0.8218849840255591, 0.8197767145135565, 0.8209014758675709, 0.8251192368839426, 0.8266241530490236, 0.8264858396489828, 0.8232, 0.8222133439872154, 0.827037773359841, 0.8268467037331215, 0.8247914183551848, 0.8238568588469185, 0.8263806118394914, 0.8283552369573874, 0.8267090620031795, 0.8263806118394914, 0.8287644020659515, 0.8301587301587302, 0.8263283108643934, 0.827037773359841, 0.8293650793650793, 0.8303535955502582, 0.8282184137106418, 0.8298126743722598, 0.8288216560509554, 0.8289578361177407, 0.8267090620031795, 0.8261904761904763, 0.8246031746031746, 0.8259141494435612, 0.8253968253968254, 0.8287644020659515, 0.8304140127388535, 0.8294234592445328, 0.8298126743722598, 0.8334667734187349, 0.8360590347028322, 0.8347964884277733, 0.8327345309381238, 0.8344689378757515, 0.8337330135891288]
f20 = [0.5225578658297372, 0.5121465551573078, 0.5152487961476725, 0.5201288244766505, 0.5260185558693021, 0.5285772192946899, 0.5301302931596091, 0.5314285714285715, 0.5342072920934043, 0.5516115871073032, 0.5589555283557731, 0.5582345729464651, 0.5629872794419368, 0.569427276473012, 0.5760065735414954, 0.5841868086849652, 0.5864350703060379, 0.6105176663927692, 0.6086956521739131, 0.6142975893599335, 0.6228690228690229, 0.6174496644295302, 0.6302170283806344, 0.635600335852225, 0.6372053872053871, 0.6391925988225399, 0.6388537715971344, 0.6387124099957645, 0.6431904963937207, 0.654867256637168, 0.6624579124579124, 0.6675084175084175, 0.6776649746192893, 0.6869970351545954, 0.6867061812023709, 0.6912951167728237, 0.6959488272921108, 0.7037351443123939, 0.7093220338983052, 0.7154953429297206, 0.709153122326775, 0.7151979565772668, 0.720375106564365, 0.7155727155727156, 0.7213951509995746, 0.7262664963814389, 0.7340471092077088, 0.7384091875797534, 0.7394815129621759, 0.7395029991431019, 0.745617785378367, 0.7504273504273505, 0.7612958226768969, 0.7537473233404711, 0.7633390705679862, 0.7722007722007722, 0.7625215889464595, 0.7606614447345518, 0.7663632423060253, 0.7656452309020285, 0.7637314734088928, 0.7721132897603485, 0.7748058671268334, 0.7810344827586208, 0.7759372275501307, 0.7820791648542845, 0.7797927461139896, 0.7818574514038876, 0.7820791648542845, 0.7850064627315814, 0.7893607893607893, 0.7951910691283811, 0.7944732297063903, 0.7909995672868889, 0.8015497201894103, 0.8095644748078565, 0.8102564102564103, 0.8145610278372591, 0.8175182481751826, 0.8142052836725856, 0.8090277777777777, 0.8173987941429802, 0.8152645273200348, 0.8178664353859497, 0.8212728857890148, 0.8258792878853669, 0.8253142609449502, 0.82271348071088, 0.8156521739130433, 0.8271068635968724, 0.8316659417137886, 0.8302214502822405, 0.8075156576200417, 0.8077084206116464, 0.8087615838247684, 0.8048883270122207, 0.8087248322147651, 0.8095838587641866, 0.8137295939723734, 0.8169250104733976, 0.819206680584551, 0.8198236035279295, 0.8193684210526315, 0.8153134202776608, 0.809945217024863, 0.8096651123357355, 0.8111533586818758, 0.8140025305778152, 0.8143157894736841, 0.8162574089754445, 0.8171041490262488, 0.8168776371308017, 0.8186046511627907, 0.8174133558748944, 0.8181049069373943, 0.8227311280746394, 0.8189109328830729, 0.8212927756653993, 0.8261238337574214, 0.8223823654090716, 0.8239763613338962, 0.8238276299112801, 0.8281117696867062, 0.8260685569191705, 0.8250741211351122, 0.8293918918918919, 0.8333333333333334, 0.8343868520859673, 0.8351555929352397, 0.8343868520859673, 0.8305509181969951, 0.8282490597576264, 0.8295122967903293, 0.8313758389261744, 0.8348623853211009, 0.8341666666666666, 0.8363939899833055, 0.8350083752093802, 0.8363939899833055, 0.8366834170854272, 0.8352842809364548, 0.8320133388912047, 0.8327075511055485, 0.8352842809364548, 0.8351464435146443, 0.8370339338081273, 0.834242551405791, 0.8364093959731543, 0.8377358490566038, 0.8357082984073764, 0.8383032339353212, 0.8393083087304934, 0.8428150021070376, 0.8427249789739277, 0.8425925925925926, 0.8431208053691275, 0.839630562552477, 0.8421498095641134, 0.8462837837837837, 0.8505067567567569, 0.8502741459299874, 0.8460565162378744, 0.848842105263158, 0.8468317247167436, 0.8489692890197729, 0.850632911392405, 0.8500211237853823, 0.8494077834179358, 0.8496399830580263, 0.8532769556025369, 0.8564167725540025, 0.8588486140724946, 0.8536064874093043, 0.8532654792196778, 0.8543524416135883, 0.8504672897196263, 0.8504870817450233, 0.8527659574468085, 0.8566552901023892, 0.854086435601198, 0.8591065292096219, 0.8591065292096219, 0.8584946236559139, 0.8599827139152982, 0.8626943005181348, 0.8610871440897325, 0.8640483383685801, 0.8615916955017301, 0.8628472222222222, 0.8659704090513489]
f4 = [0.6722997795738428, 0.6703662597114318, 0.6671608598962195, 0.6651685393258426, 0.6639035418236624, 0.6619243728940472, 0.661138333961553, 0.6562974203338392, 0.6542976145399471, 0.6581132075471697, 0.6633776091081595, 0.6636398032538781, 0.6656626506024096, 0.6648996592199924, 0.6557126480703095, 0.662636947487722, 0.6583616459041147, 0.6578449905482042, 0.6613333333333333, 0.6567732115677322, 0.6603343465045592, 0.6565579984836998, 0.6469472885855139, 0.6518234165067177, 0.6552511415525114, 0.6549752192146397, 0.648565965583174, 0.6477794793261867, 0.6443418013856812, 0.6445899114362726, 0.6459054209919262, 0.6454823889739663, 0.6408585665005749, 0.636083269082498, 0.6360123647604328, 0.6362582141476614, 0.6362229102167183, 0.6402178140801246, 0.6349082389691526, 0.633216647218981, 0.6434378629500581, 0.64765625, 0.6367538041357783, 0.6271585557299842, 0.6313309776207303, 0.6440545808966862, 0.6339181286549708, 0.6283704572098476, 0.6263736263736264, 0.628099173553719, 0.624163715072806, 0.6249014972419228, 0.6275430359937402, 0.6296875000000001, 0.6326129666011787, 0.6291338582677165, 0.6194411648957103, 0.6222922410397794, 0.6238170347003155, 0.6285488958990536, 0.6218885815883051, 0.625147812376823, 0.6194620253164557, 0.6181818181818182, 0.6240126382306477, 0.6191802626343017, 0.6227687425624752, 0.6248025276461295, 0.6270313119302418, 0.6282101935993678, 0.6227687425624752, 0.6182539682539683, 0.6158730158730159, 0.6081081081081081, 0.6124553748512495, 0.6181242580134547, 0.6076555023923444, 0.6073131955484897, 0.6082104424073336, 0.6086261980830671, 0.6023999999999999, 0.6021591363454618, 0.5984757320497393, 0.6014376996805112, 0.6044835868694957, 0.5882825040128411, 0.588235294117647, 0.6015218261914297, 0.6094249201277955, 0.6062300319488817, 0.6074429771908764, 0.605475040257649, 0.6502609992542878, 0.6505576208178439, 0.6535608308605341, 0.6525139664804469, 0.650187265917603, 0.6502242152466368, 0.6529543754674645, 0.651355421686747, 0.6465712132629993, 0.6426696662917134, 0.6436090225563911, 0.6444111027756939, 0.6433933933933934, 0.6393380970289583, 0.6463963963963963, 0.6471251409244646, 0.641381900112655, 0.6420218785364014, 0.6453313253012047, 0.6422087745839637, 0.6418816388467375, 0.6413662239089185, 0.6446719757299961, 0.6469248291571754, 0.6468344774980932, 0.6430745814307458, 0.6440548780487805, 0.647887323943662, 0.6497153700189754, 0.6514806378132119, 0.6502463054187191, 0.6488753335874952, 0.6459770114942529, 0.6460244648318043, 0.6524390243902439, 0.6511094108645754, 0.6487935656836462, 0.646541841803592, 0.655392709507704, 0.6576475009394965, 0.6594066841907623, 0.6588855421686748, 0.6540927951716333, 0.6516007532956686, 0.6546003016591252, 0.6535403256342295, 0.6508966043494849, 0.6539634146341463, 0.6545178435839029, 0.6540068363083935, 0.6573161485974223, 0.6570561456752656, 0.6600985221674877, 0.6570670708601742, 0.6501145912910619, 0.6536697247706421, 0.6559386973180077, 0.6577540106951871, 0.6597780329123613, 0.6577129700690714, 0.6567049808429118, 0.656441717791411, 0.660557464681176, 0.6618431073876619, 0.6661596958174906, 0.6633549866259075, 0.6587240584166025, 0.6538461538461539, 0.6559015763168012, 0.6571867794004612, 0.6576819407008085, 0.6599922988063149, 0.6623026569118212, 0.6638494045332308, 0.6628219915417147, 0.6633243347473969, 0.6640926640926641, 0.6589237320944638, 0.6586687306501549, 0.6612403100775194, 0.658385093167702, 0.663312693498452, 0.6633048875096975, 0.6630434782608696, 0.6609575710393149, 0.6604434072345391, 0.6614967041488948, 0.6612403100775194, 0.6653741760372237, 0.6695145631067961, 0.6640625, 0.6611829220524872, 0.6637897214593959, 0.6650961915979584, 0.6721247563352827, 0.671606864274571, 0.6674491392801252, 0.6637897214593959]
f2 = [0.4080625257095845, 0.3961794019933555, 0.3901420217209691, 0.38895859473023836, 0.3873949579831933, 0.392586352148273, 0.4005037783375315, 0.3998320033599328, 0.3878942881500426, 0.4015345268542199, 0.41376380628717074, 0.40721649484536077, 0.4135564135564135, 0.4150943396226415, 0.4165232358003442, 0.4229607250755287, 0.43122035360068994, 0.4392964392964393, 0.4256055363321799, 0.44587077449721857, 0.44939965694682676, 0.46094750320102434, 0.45653104925053534, 0.45454545454545453, 0.4697357203751066, 0.4728051391862956, 0.46531667384747954, 0.45865970409051343, 0.470894874022589, 0.4823123382226057, 0.48837209302325585, 0.4870242214532872, 0.49525452976704054, 0.4909404659188956, 0.49784668389319553, 0.5060449050086356, 0.5034662045060659, 0.5032708242477104, 0.5150065245759026, 0.5227568270481145, 0.5272255834053587, 0.53126347563605, 0.5333333333333333, 0.5378296584522265, 0.536332179930796, 0.5426356589147288, 0.5379310344827586, 0.5385609651012495, 0.5544041450777203, 0.5528031290743155, 0.5530434782608695, 0.5591677503250976, 0.5700773860705073, 0.5741216795201372, 0.5716753022452504, 0.5831533477321814, 0.5816282107096212, 0.5710514738231411, 0.5787384208204676, 0.5803336259877085, 0.5801928133216477, 0.5834061135371179, 0.5796847635726795, 0.588389349628983, 0.5956140350877193, 0.6025472112428634, 0.5973568281938325, 0.6062472503299605, 0.6001757469244289, 0.6020942408376964, 0.6068601583113457, 0.6105263157894737, 0.6056644880174292, 0.6112320417936439, 0.6180707114797032, 0.6147110332749562, 0.6132282084975909, 0.6287713161346742, 0.6252189141856392, 0.6206593406593406, 0.6283694211224038, 0.6368467670504872, 0.6269982238010657, 0.627589246364037, 0.6351172047766475, 0.6420404573438875, 0.6425738210665491, 0.6392294220665499, 0.6385595081247254, 0.6477024070021882, 0.6470846120122753, 0.6439024390243904, 0.5924726831242412, 0.5987878787878788, 0.6004842615012107, 0.6001622060016221, 0.6033292732440114, 0.6009732360097323, 0.599104599104599, 0.6068237205523965, 0.6077079107505071, 0.6084848484848484, 0.6078829744006502, 0.613506916192026, 0.6125611745513867, 0.6123778501628665, 0.6088726088726089, 0.6084115965700286, 0.6180187525479005, 0.6214781543487138, 0.6167689161554192, 0.6175869120654397, 0.6204918032786886, 0.6237704918032786, 0.6221311475409835, 0.6225872689938399, 0.6278210915059499, 0.631231973629996, 0.6332236842105263, 0.6293706293706294, 0.6275320380322447, 0.6292783505154639, 0.6297662976629766, 0.6270627062706271, 0.6284765462847656, 0.6282157676348549, 0.6317539484621778, 0.6356846473029046, 0.6363260239966901, 0.6395348837209301, 0.6308943089430894, 0.6291041751114714, 0.6279447603574331, 0.6284086284086284, 0.6316646316646317, 0.6310640032613127, 0.6356209150326797, 0.6329634196465269, 0.6351684470008216, 0.6330463304633047, 0.6321792260692465, 0.6323529411764707, 0.6377049180327868, 0.6414473684210527, 0.6395396629675297, 0.6398687448728466, 0.641215106732348, 0.6428571428571428, 0.6449752883031301, 0.6454545454545455, 0.6474226804123712, 0.6496079240610813, 0.6468401486988847, 0.645134575569358, 0.6415094339622642, 0.643527970600245, 0.6434426229508198, 0.6441237113402062, 0.6443618339529121, 0.6473749483257545, 0.6512013256006628, 0.6512205213074059, 0.6538942107455227, 0.654151022110972, 0.6555878687162443, 0.6539260490236809, 0.6564059900166389, 0.6567040265670404, 0.6564315352697097, 0.6561330561330562, 0.6578073089700996, 0.6597337770382695, 0.6608333333333333, 0.6591478696741855, 0.655819774718398, 0.6572261557684298, 0.6597077244258872, 0.6597077244258872, 0.6588726513569937, 0.6597164303586323, 0.6624895572263994, 0.663316582914573, 0.6661059714045416, 0.6655476290390264, 0.6669470142977292, 0.6672261854804868, 0.6647132691502722, 0.6652702136573105, 0.6663862010938157, 0.6663854913538592]

window_sizes = range(10,200)
plt.plot(window_sizes, f2, label="2")
plt.plot(window_sizes, f4, label="4")
plt.plot(window_sizes, f20, label="20")
plt.plot(window_sizes, f40, label="40")
plt.plot(window_sizes, f200, label="200")
plt.plot(window_sizes, f400, label="400")
plt.xlabel("Window Size")
plt.ylabel("F1 Score")
plt.legend(loc="upper left")

"""# Next Steps:

* Start writing findings
* See if I can tune saturating detection parameters to improve performance across the board
* Run benchmark code from repo on a couple approaches (saturating spike, regular gradient)

* True pos rate and false pos rate
* 4/20 availability 2:30-4

"""