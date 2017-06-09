#Sentiment Analysis
#Songjian Luan: luans
#Raja Petroff: petroffr

import math

class DataSet:

	def __init__(self, fst_file, snd_file):
		self.fst_file = fst_file
		self.snd_file = snd_file
		self.fst_set = []
		self.snd_set = []

	def func_load_file(self):
		with open(self.fst_file, 'r') as file:
			for item in file:
				line = item.split('\t')
				self.fst_set.append([line[0], int(line[1])])
			file.close()
		with open(self.snd_file, 'r') as file:
			for item in file:
				line = item.split('\t')
				self.snd_set.append([line[0], int(line[1])])
			file.close()

	def func_filter_line(self, data_src, word_list = []):
	    for data in data_src:
	        words = data[0].translate(None, '?/-+*!&.:[]()",').lower().split()
	        for word in words:
	            if word not in word_list: word_list.append(word)
	    return sorted(word_list)

	def func_build_set(self):
		self.func_load_file()
		word_list = self.func_filter_line(self.fst_set, [])
		word_list = self.func_filter_line(self.snd_set, word_list)
		return word_list

class DataRaw:

	def __init__(self, word_list, name):
		self.word_list = word_list
		self.name = name

	def func_feature_label(self, feature_list = [], label_list = []):
		with open(self.name, 'r') as file:
			for item in file:
				data = item.split('\t')
				words = data[0].translate(None, '?/-+*!&.:[]()",').lower().split()
				feature = [0] * len(word_list)
				for word in words: feature[word_list.index(word)] = 1
				feature_list.append(feature)
				label_list.append(int(data[1]))
			file.close()
		return feature_list, label_list

	def func_write_file(self, target):
		feature_list, label_list = self.func_feature_label([], [])
		with open(target, 'w+') as file:
			file.write(' '.join(self.word_list) + ' - classlabel\n')
			for i in range(len(feature_list)):
				file.write(' '.join([str(item) for item in feature_list[i]]) + ' - ' + str(label_list[i]) + '\n')
			file.close()

class DataEval:

	def __init__(self, word_list, feature_list, label_list):
		self.word_list = word_list
		self.feature_list = feature_list
		self.label_list = label_list

	def func_feature_classify(self):
		pos_cnt, neg_cnt = 0, 0
		pos_feature_list, neg_feature_list = [], []
		for i in range(len(self.label_list)):
			tmp_list = self.feature_list[i]
			if self.label_list[i] == 1:
				pos_cnt += 1
				pos_feature_list.append(tmp_list)
			if self.label_list[i] == 0:
				neg_cnt += 1
				neg_feature_list.append(tmp_list)
		return pos_cnt, neg_cnt, pos_feature_list, neg_feature_list

	def func_calc_prob(self, feature_list, idx, feature_cnt):
		features = [item[idx] for item in feature_list if item[idx] == 1]
		return float(len(features) + 1) / (feature_cnt + len(self.word_list))

	def func_calc_feature_prob(self, pos_prob = {}, neg_prob = {}):
		pos_cnt, neg_cnt, pos_feature_list, neg_feature_list = self.func_feature_classify()
		for i in range(len(word_list)):
			word = self.word_list[i]
			pos_prob[word] = self.func_calc_prob(pos_feature_list, i, pos_cnt)
			neg_prob[word] = self.func_calc_prob(neg_feature_list, i, neg_cnt)
		return pos_prob, neg_prob

	def func_calc_label_prob(self):
		label_sum, label_size = sum(self.label_list), len(self.label_list)
		pos_prob = float(label_sum + 1) / (label_size + 2)
		neg_prob = float(label_size - label_sum + 1) / (label_size + 2)
		return pos_prob, neg_prob

	def func_fetch_label_prob(self, label):
		pos_prob, neg_prob = self.func_calc_label_prob()
		return pos_prob if label == 0 else neg_prob

	def func_fetch_feature_prob(self, label, idx, pos_prob, neg_prob):
		word = self.word_list[idx]
		return pos_prob[word] if label == 0 else neg_prob[word]

	def func_sum_prob(self, feature, label, pos_prob, neg_prob):
		prob_sum = math.log(self.func_fetch_label_prob(label))
		for idx in range(len(feature)):
			if feature[idx]:
				prob = self.func_fetch_feature_prob(label, idx, pos_prob, neg_prob)
				prob_sum += math.log(prob)
		return prob_sum

def func_train_test(dataeval, pred_list = []):
	pos_prob, neg_prob = dataeval.func_calc_feature_prob({}, {})
	for feature in feature_list:
		pos_sum = dataeval.func_sum_prob(feature, 1, pos_prob, neg_prob)
		neg_sum = dataeval.func_sum_prob(feature, 0, pos_prob, neg_prob)
		pred_list.append(1 if pos_sum > neg_sum else 0)
	diff_list = [pred_list[i] - dataeval.label_list[i] for i in range(len(dataeval.label_list))]
	accuracy = float(len(pred_list) - sum(diff_list)) / len(pred_list)
	return str(accuracy * 100) + '%'

if __name__ == '__main__':
	dataset = DataSet('trainingSet.txt', 'testSet.txt')
	word_list = dataset.func_build_set()
	print '=====', 'Training on Training Accuracy Result', '====='
	dataraw = DataRaw(word_list, 'trainingSet.txt')
	dataraw.func_write_file('preprocessed_test.txt')
	feature_list, label_list = dataraw.func_feature_label([], [])
	dataeval = DataEval(word_list, feature_list, label_list)
	training_accuracy = func_train_test(dataeval, [])
	print 'Accuracy:', training_accuracy
	print '=====', 'Test on Training Accuracy Result', '====='
	dataraw = DataRaw(word_list, 'testSet.txt')
	dataraw.func_write_file('preprocessed_test.txt')
	feature_list, label_list = dataraw.func_feature_label([], [])
	dataeval = DataEval(word_list, feature_list, label_list)
	test_accuracy = func_train_test(dataeval, [])
	print 'Accuracy:', test_accuracy
	with open('results.txt', 'w+') as file:
		file.write('===== Training on Training Accuracy Result =====')
		file.write('\n')
		file.write('Accuracy: ' + training_accuracy + '\n')
		file.write('===== Test on Training Accuracy Result =====')
		file.write('\n')
		file.write('Accuracy: ' + test_accuracy + '\n')
		file.close()
