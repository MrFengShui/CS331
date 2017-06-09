#Sentiment Analysis
#Songjian Luan: luans
#Raja Petroff: petroffr

import math, time

def func_load_file(name, dataset = []):
	with open(name, 'r') as file:
		for item in file:
			line = item.split('\t')
			dataset.append([line[0], int(line[1])])
		file.close()
	return dataset

def func_write_file(name, word_list, label_list, feature_list):
    with open(name, 'w+') as file:
        file.write(' '.join(word_list) + ' - label\n')
        for i in range(len(feature_list)):
            file.write(' '.join([str(item) for item in feature_list[i]]) + ' - ' + str(label_list[i]) + '\n')
        file.close()

def func_filter_line(dataset):
    word_list, label_list = [], []
    for data in dataset:
        words = data[0].translate(None, '?/-+*!&.:[]()",').lower().split()
        for word in words:
            if word not in word_list: word_list.append(word)
        label_list.append(data[1])
    return sorted(word_list), label_list

def func_create_feature(dataset, word_list, feature_list = []):
    for data in dataset:
        words = data[0].translate(None, '?/-+*!&.:[]()",').lower().split()
        feature = [0] * len(word_list)
        for word in words: feature[word_list.index(word)] = 1
        feature_list.append(feature)
    return feature_list

def func_feature_classify(label_list, feature_list):
	pos_cnt, neg_cnt = 0, 0
	pos_feature_list, neg_feature_list = [], []
	for i in range(len(label_list)):
		tmp_list = feature_list[i]
		if label_list[i] == 1:
			pos_cnt += 1
			pos_feature_list.append(tmp_list)
		if label_list[i] == 0:
			neg_cnt += 1
			neg_feature_list.append(tmp_list)
	return pos_cnt, neg_cnt, pos_feature_list, neg_feature_list

def func_calc_prob(word_list, feature_list, idx, feature_cnt):
	features, count = [item[idx] for item in feature_list], 0
	for feature in features:
		if feature == 1: count += 1
	return float(count + 1) / (feature_cnt + len(word_list))

def func_calc_label_prob(label_list):
	label_sum, label_size = sum(label_list), len(label_list)
	pos_prob = float(label_sum + 1) / (label_size + 2)
	neg_prob = float(label_size - label_sum + 1) / (label_size + 2)
	return pos_prob, neg_prob

def func_calc_feature_prob(word_list, label_list, feature_list):
    pos_prob, neg_prob = {}, {}
    pos_cnt, neg_cnt, pos_feature_list, neg_feature_list = func_feature_classify(label_list, feature_list)
    for i in range(len(word_list)):
	    pos_prob[word_list[i]] = func_calc_prob(word_list, pos_feature_list, i, pos_cnt)
	    neg_prob[word_list[i]] = func_calc_prob(word_list, neg_feature_list, i, neg_cnt)
    return pos_prob, neg_prob

def func_fetch_prob(word_list, label_list, label, idx = None, pos_prob = None, neg_prob = None):
	if idx == None:
		prob = func_calc_label_prob(label_list)
		return prob[label]
	else:
		word = word_list[idx]
		return pos_prob[word] if label else neg_prob[word]

def func_sum_prob(word_list, label_list, feature_list, feature, label, pos_prob, neg_prob):
	prob_sum = math.log(func_fetch_prob(word_list, label_list, label))
	for idx in range(len(feature)):
		if feature[idx]:
			prob = func_fetch_prob(word_list, label_list, label, idx, pos_prob, neg_prob)
			prob_sum += math.log(prob)
	return prob_sum

def func_train_test(word_list, label_list, feature_list):
	pos_prob, neg_prob = func_calc_feature_prob(word_list, label_list, feature_list)
	pred_list, count = [], 1
	for feature in feature_list:
		probs = func_sum_prob(word_list, label_list, feature_list, feature, 1, pos_prob, neg_prob), func_sum_prob(word_list, label_list, feature_list, feature, 0, pos_prob, neg_prob)
		idx = probs.index(probs[0] if probs[0] > probs[1] else probs[1])
		pred_list.append(idx)
	diff_list = [pred_list[i] - label_list[i] for i in range(len(label_list))]
	accuracy = float(len(pred_list) - sum(diff_list)) / len(pred_list)
	return str(accuracy * 100) + '%'

def func_run_data(src, dest, title):
	train_set = func_load_file(src)
	word_list, label_list = func_filter_line(train_set)
	feature_list = func_create_feature(train_set, word_list, [])
	print '===== Writing Results to', title, 'File ====='
	func_write_file(dest, word_list, label_list, feature_list)
	print '=====', title, 'on Traning Set Result ====='
	print 'Accuracy:', func_train_test(word_list, label_list, feature_list)
	with open('results.txt', 'a+') as file:
		file.write('=====' + title + ' on Traning Set Result =====')
		file.write('\n')
		file.write('Accuracy: ' + str(func_train_test(word_list, label_list, feature_list)))
		file.write('\n')
		file.close()

if __name__ == '__main__':
	func_run_data('trainingSet.txt', 'preprocessed_train.txt', 'Training')
	func_run_data('testSet.txt', 'preprocessed_test.txt', 'Test')
