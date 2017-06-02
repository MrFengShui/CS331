import math

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

if __name__ == '__main__':
	train_set = func_load_file('trainingSet.txt')
	word_list, label_list = func_filter_line(train_set)
	feature_list = func_create_feature(train_set, word_list)
	# func_write_file('preprocessed_train.txt', word_list, label_list, feature_list)
	# print func_calc_feature_prob(word_list, label_list, feature_list)
