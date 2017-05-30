import string

class Sentence:

    def __init__(self, sentence, classify):
        self.sentence = sentence
        self.classify = classify

    def split_to_words(self):
        self.sentence = self.sentence.translate(None, string.punctuation)
        return self.sentence.split()

    def format_line(self):
        return self.split_to_words(), self.classify

def func_load_file(name):
    dataset = []
    with open(name, 'r') as file:
        for item in file:
            line = item.split('\t')
            dataset.append(Sentence(line[0], int(line[1][:-1])))
    return dataset

def func_cnt_word(dataset, cnt_set = {}):
    for data in dataset:
        for word in data.split_to_words():
            if word in cnt_set: cnt_set[word] += 1
            else: cnt_set[word] = 1
    return cnt_set

def func_fetch_cnt(cnt_set, word):
    return cnt_set[word] if word in cnt_set else 0

def func_build_feature(cnt_set, line, feature):
    for word in cnt_set:
        if word in line.split_to_words(): feature.append(1)
        else: feature.append(0)
    feature.append(int(line.classify))
    return feature

dataset = func_load_file('trainingSet.txt')
cnt_set = func_cnt_word(dataset)
features = [func_build_feature(cnt_set, data, []) for data in dataset]
print features
# for data in dataset:
#     print '+++', data.sentence, data.classify
#     print '---', data.split_to_words(), data.classify
