#!/usr/bin/env python2

from math import log
import numpy as np
import string

class Vocabulary:
    def __init__(self):
        self.vocabulary = set([])
        self.training_data = open('trainingSet.txt', 'r')
        self.testing_data = open('testSet.txt', 'r')

    def build(self):
        self._build_vocabulary(self.training_data)
        self._build_vocabulary(self.testing_data)
        self.training_data.close()
        self.testing_data.close()
        return sorted(self.vocabulary)

    def _build_vocabulary(self, file):
        for line in file:
            for word in line.translate(None, string.punctuation).lower().split()[:-1]:
                if word not in self.vocabulary:
                    self.vocabulary.add(word)

class Data:
    def __init__(self, vocabulary, filename):
        file = open(filename, 'r')
        self.vocabulary = vocabulary
        (self.features, self.classlabels) = self._build_data_arrays(file)

    def __getitem__(self, i):
        return (self.features[i], self.classlabels[i])

    def write_file(self, filename):
        file = open(filename, 'w+')
        file.write(','.join(self.vocabulary) + ',classlabel\n')
        for i, entry in enumerate(self.features):
            entry_list = entry.tolist()
            entry_list.append(self.classlabels[i])
            file.write(','.join(map(str, entry_list)))
            file.write('\n')
        file.close()

    def _build_data_arrays(self, file):
        (features, classlabels) = self._build_data_lists(file)
        return (np.array(features, dtype=int), np.array(classlabels,
            dtype=int))

    def _build_data_lists(self, file):
        (features, classlabels) = ([], [])
        for line in file:
            feature_list = [0] * len(self.vocabulary)
            split_line = line.translate(None, string.punctuation).lower().split()
            for word in split_line[:-1]:
                feature_list[self.vocabulary.index(word)] = 1
            features.append(feature_list)
            classlabels.append(split_line[-1])
        return (features, classlabels)

class ConditionalProbabilityTable:
    def __init__(self, training_data):
        self.training = training_data
        self.vocabulary = training_data.vocabulary
        self.classlabel_probabilities = {}
        self.params_given_cl = {}
        self.params_given_not_cl = {}

    def get_probability(self, classlabel, index=None):
        if index is None:
            return self.classlabel_probabilities[classlabel]
        else:
            word = self.vocabulary[index]
            if classlabel:
                return self.params_given_cl[word]
            else:
                return self.params_given_not_cl[word]

    def train(self):
        self._calculate_classlabel_probabilities()
        self._calculate_conditional_feature_probabilites()

    def _calculate_classlabel_probabilities(self):
        probability = (np.sum(self.training.classlabels) + 1) / float(
                (len(self.training.classlabels) + 2))
        self.classlabel_probabilities[1] = probability

        probability = (len(self.training.classlabels) -
                np.sum(self.training.classlabels) + 1) / float(
                        (len(self.training.classlabels) + 2))
        self.classlabel_probabilities[0] = probability

    def _calculate_conditional_feature_probabilites(self):
		true_count = len(self.training.classlabels[self.training.classlabels == 1])
		false_count = len(self.training.classlabels[self.training.classlabels == 0])
		features_given_cl = self.training.features[self.training.classlabels == 1]
		features_given_not_cl = self.training.features[self.training.classlabels == 0]
		n_j = len(self.vocabulary)
		
		for i, word in enumerate(self.vocabulary):
			prob_true_given_cl = (len(features_given_cl[features_given_cl[:,i] == 1]) + 1) / float((true_count + n_j))
			prob_true_given_not_cl = (len(features_given_not_cl[features_given_not_cl[:,i] == 1]) + 1) / float(false_count + n_j)
			self.params_given_cl[word] = prob_true_given_cl
			self.params_given_not_cl[word] = prob_true_given_not_cl

class NaiveBayes:
    def __init__(self, training_data):
        self.parameters = ConditionalProbabilityTable(training_data)

    def train(self):
        self.parameters.train()

    def test(self, testing_data):
        predictions = []
        for feature_vec in testing_data.features:
            predictions.append(self._make_prediction(feature_vec))

        accuracy = (len(predictions) - sum(abs(predictions -
            testing_data.classlabels))) / float(len(predictions))

        return ''.join([str(round(accuracy, 4) * 100), '%'])

    def _make_prediction(self, feature_vec):
        probabilities = []
        probabilities.append(self._calculate_probability(feature_vec, 0))
        probabilities.append(self._calculate_probability(feature_vec, 1))
        return probabilities.index(max(probabilities))

    def _calculate_probability(self, feature_vec, classlabel):
        sum = log(self.parameters.get_probability(classlabel))
        for index, value in enumerate(feature_vec):
            if value:
                sum += log(self.parameters.get_probability(classlabel, index))
        return sum

def main():
    v = Vocabulary()
    vocabulary = v.build()

    training_data = Data(vocabulary, 'trainingSet.txt')
    testing_data = Data(vocabulary, 'testSet.txt')
    # training_data.write_file('preprocessed_train.txt')
    # testing_data.write_file('preprocessed_test.txt')

    naive_bayes = NaiveBayes(training_data)
    naive_bayes.train()
    training_accuracy = naive_bayes.test(training_data)
    testing_accuracy = naive_bayes.test(testing_data)

    print ' '.join(['Training Accuracy:', training_accuracy])
    print ' '.join(['Testing Accuracy:', testing_accuracy])

    # write_results(training_accuracy, testing_accuracy)

def write_results(training_accuracy, testing_accuracy):
    results = open('results/results.txt', 'w')
    results.write('RESULTS\n')
    results.write('-----------------------------------------\n\n')
    results.write('Trained on: data/trainingSet.txt\n')
    results.write('Tested on: data/trainingSet.txt\n')
    results.write(''.join(['Accuracy: ', training_accuracy, '\n']))
    results.write('\n-----------------------------------------\n\n')
    results.write('Trained on: data/trainingSet.txt\n')
    results.write('Tested on: data/testSet.txt\n')
    results.write(''.join(['Accuracy: ', testing_accuracy, '\n']))
    results.write('\n-----------------------------------------')
    results.close()

if __name__ == '__main__':main()
