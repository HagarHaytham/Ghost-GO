from __future__ import print_function
from __future__ import absolute_import
import os
import random
from dataset.download_dataset import KGSIndex
from six.moves import range


class Splitter:
    def __init__(self, data_dir, num_test_games=100, cap_year=2015, seed=1337):
        self.data_dir = data_dir
        self.num_test_games = num_test_games
        self.test_games = []
        self.train_games = []
        self.test_folder = 'test_samples.py'
        self.cap_year = cap_year

        random.seed(seed)
        self.compute_test_samples()

    def draw_data(self, data_type, num_samples):
        if data_type == 'test':
            return self.test_games
        elif data_type == 'train' and num_samples is not None:
            return self.draw_training_samples(num_samples)
        else:
            raise ValueError(data_type + " is not a valid data type, choose from 'train' or 'test'")

    def draw_samples(self, num_sample_games):
        """Draw num_sample_games many training games from index."""
        available_games = []
        index = KGSIndex(data_directory=self.data_dir)

        for fileinfo in index.file_info:
            filename = fileinfo['filename']
            year = int(filename.split('-')[1].split('_')[0])
            if year > self.cap_year: # training set is the set of year > 2015 and test set before that
                continue
            num_games = fileinfo['num_games']
            for i in range(num_games):
                available_games.append((filename, i))
        # print('Total number of games used: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                sample_set.add(sample)
        # print('Drawn ' + str(num_sample_games) + ' samples:')
        return list(sample_set)


    def compute_test_samples(self):
        #If not already existing, create local file to store fixed set of test samples"""
        # if not os.path.isfile(self.test_folder):
        #     test_games = self.draw_samples(self.num_test_games)
        #     test_sample_file = open(self.test_folder, 'w')
        #     for sample in test_games:
        #         test_sample_file.write(str(sample) + "\n")
        #     test_sample_file.close()

        test_sample_file = open(self.test_folder, 'r')
        sample_contents = test_sample_file.read()
        test_sample_file.close()
        for line in sample_contents.split('\n'):
            if line != "":
                (filename, index) = eval(line)
                self.test_games.append((filename, index))

    def draw_training_samples(self, num_sample_games):
        """Draw training games, not overlapping with any of the test games."""
        available_games = []
        index = KGSIndex(data_directory=self.data_dir)
        for fileinfo in index.file_info:
            filename = fileinfo['filename']
            year = int(filename.split('-')[1].split('_')[0])
            if year > self.cap_year:
                continue
            num_games = fileinfo['num_games']
            for i in range(num_games):
                available_games.append((filename, i))
        # print('total num games: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in self.test_games:
                sample_set.add(sample)
        # print('Drawn ' + str(num_sample_games) + ' samples:')
        return list(sample_set)

