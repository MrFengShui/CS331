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
		if label_list[i] == 1:
			pos_cnt += 1
			pos_feature_list.append(feature_list[i])
		if label_list[i] == 0:
			neg_cnt += 1
			neg_feature_list.append(feature_list[i])
	return pos_cnt, neg_cnt, pos_feature_list, neg_feature_list

def func_calc_prob(word_list, feature_list, idx, feature_cnt):
	features, count = [item[idx] for item in feature_list], 0
	for feature in features:
		if feature == 1: count += 1
	return float(count + 1) / (feature_cnt + len(word_list))

def func_calc_label_prob(label_list):
	pos_prob = float(sum(label_list) + 1) / (len(label_list) + 2)
	neg_prob = float(len(label_list) - sum(label_list) + 1) / (len(label_list) + 2)
	return pos_prob, neg_prob

def func_calc_feature_prob(word_list, label_list, feature_list):
	pos_prob, neg_prob = {}, {}
	pos_cnt, neg_cnt, pos_feature_list, neg_feature_list = func_feature_classify(label_list, feature_list)
	for i in range(len(word_list)):
		pos_prob[word_list[i]] = func_calc_prob(word_list, pos_feature_list, i, pos_cnt)
		neg_prob[word_list[i]] = func_calc_prob(word_list, neg_feature_list, i, neg_cnt)
	return pos_prob, neg_prob

def func_fetch_prob(word_list, label_list, feature_list, label, idx = None):
	if idx == None:
		prob = func_calc_label_prob(label_list)
		return prob[label]
	else:
		word = word_list[idx]
		pos_prob, neg_prob = func_calc_feature_prob(word_list, label_list, feature_list)
		return pos_prob[word] if label else neg_prob[word]

def func_sum_prob(word_list, label_list, feature_list, feature, label):
	result = math.log(func_fetch_prob(word_list, label_list, feature_list, label))
	tick = time.time()
	for i in range(len(feature)):
		if feature[i] == 1: result += math.log(func_fetch_prob(word_list, label_list, feature_list, label, i))
	print '--- %.3f(s)' % (time.time() - tick)
	return result

def func_test_data(word_list, label_list, feature_list, pred_list = []):
	for feature in feature_list:
		sum_prob = []
		sum_prob.append(func_sum_prob(word_list, label_list, feature_list, feature, 1))
		sum_prob.append(func_sum_prob(word_list, label_list, feature_list, feature, 0))
		print '+++', sum_prob
		idx = sum_prob.index(sum_prob[0] if sum_prob[0] > sum_prob[1] else sum_prob[1])
		pred_list.append(idx)
	print pred_list
	pred_len, pred_sum = len(pred_list), [abs(pred_list[i] - label_list[i]) for i in range(len(pred_list))]
	accuracy = float(pred_len - sum(abs(pred_list - pred_sum))) / pred_len
	return str(accuracy * 100) + '%'

if __name__ == '__main__':
	train_set, test_set = func_load_file('trainingSet.txt'), func_load_file('testSet.txt')
	word_list, label_list = func_filter_line(train_set)
	feature_list = func_create_feature(train_set, word_list)
	# func_write_file('preprocessed_train.txt', word_list, label_list, feature_list)
	# for feature in feature_list: print func_sum_prob(feature, 1)
	print func_test_data(word_list, label_list, feature_list)
