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

def func_calc_label_prob(label_list):
	pos_prob = float(sum(label_list) + 1) / (len(label_list) + 2)
	neg_prob = float(len(label_list) - sum(label_list) + 1) / (len(label_list) + 2)
	return pos_prob, neg_prob

def func_calc_feature_prob(dataset, label_list, feature_list):
	print None

if __name__ == '__main__':
    # train_set = func_load_file('trainingSet.txt')
    # word_list, label_list = func_filter_line(train_set)
    # feature_list = func_create_feature(train_set, word_list)
    # func_write_file('preprocessed_train.txt', word_list, label_list, feature_list)
	data, ones = [0, 0, 0, 0, 0], [0, 0, 0]
	print data[data == 1]
