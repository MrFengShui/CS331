import string

class DataRow:

	def __init__(self, row):
		self.row = row

	def word_list(self):
		words = self.row[0].translate(None, string.punctuation)
		return words.split()

	def row_feature(self):
		return int(self.row[1][:-1])
		
	def build_common_words(self, dataset):
		count, common = func_count_word(dataset), []
		for key, value in count.items():
			if value >= 5: common.append(key)
		return sorted(common)

class BayesData:

	def __init__(self, word, idx, features):
		self.word = word
		self.idx = idx
		self.features = features
		
class Feature:

	def __init__(self, feature, label):
		self.feature = feature
		self.label = label
		
def func_load_file(name):
	dataset = []
	with open(name, 'r') as file:
		for item in file:
			line = item.split('\t')
			dataset.append(DataRow(line))
		file.close()
	return dataset

def func_store_file(name, words, features):
	with open(name, 'w') as file:
		for feature in features:
			file.write(feature)
		file.close()
	
def func_count_word(dataset):
	count = {}
	for datarow in dataset:
		for word in datarow.word_list():
			if word in count: count[word] += 1
			else: count[word] = 1
	return count

def func_build_feature(dataset):
	features = []
	for datarow in dataset:
		tmp_list = []
		for word in datarow.build_common_words(dataset):
			tmp_list.append(1 if word in datarow.word_list() else 0)
		features.append(Feature(tmp_list, datarow.row_feature()))
	return features

if __name__ == '__main__':
	dataset = func_load_file('trainingSet.txt')
	datarow = dataset[1]
	print datarow.word_list()
	print datarow.row_feature()
	print datarow.build_common_words(dataset)
	print func_build_feature(dataset)