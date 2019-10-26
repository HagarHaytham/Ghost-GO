import os.path
import tarfile
import gzip
import glob
import shutil
import numpy as np
from keras.utils import to_categorical
from encoder.sgf.sgf import Sgf_game
from encoder.gostuff.goboard_fast import Board, GameState, Move
from encoder.gostuff.gotypes import Player, Point
from split import Splitter
from datagenerator import DataGenerator



class DataProcessor:
    def __init__(self, encoder,data_directory='dataset/data'):
        self.encoder = encoder
        self.data_dir = data_directory

    def load_go_data(self, data_type='train', num_samples=1000,use_generator=False):
        
        splitter = Splitter(data_dir=self.data_dir)
        data = splitter.draw_data(data_type, num_samples)
        # self.map_to_workers(data_type, data) 
        zip_names = set()
        indices_by_zip_name = {}
        
        for filename, index in data:
            zip_names.add(filename) #collect all zip file names contained in the data in a list
            if filename not in indices_by_zip_name:
                indices_by_zip_name[filename] = []
            indices_by_zip_name[filename].append(index) #group all sgf file indices by zip file name
        
        for zip_name in zip_names:
            base_name = zip_name.replace('.tar.gz', '')
            data_file_name = base_name + data_type  # train or test
            if not os.path.isfile(self.data_dir + '/' + data_file_name): 
                # extracrt the sgf files and encode them to numpy arrays (features and labels) and save them as chunks on disk
                self.process_zip(zip_name, data_file_name, indices_by_zip_name[zip_name])  
    
        if use_generator:
            generator = DataGenerator(self.data_dir, data)
            return generator 
        else:
            features_and_labels = self.group_games(data_type, data)
            return features_and_labels

    # def map_to_workers(self, data_type, samples):
    #     zip_names = set()
    #     indices_by_zip_name = {}
    #     for filename, index in samples:
    #         zip_names.add(filename)
    #         if filename not in indices_by_zip_name:
    #             indices_by_zip_name[filename] = []
    #         indices_by_zip_name[filename].append(index)

    #     zips_to_process = []
    #     for zip_name in zip_names:
    #         base_name = zip_name.replace('.tar.gz', '')
    #         data_file_name = base_name + data_type
    #         if not os.path.isfile(self.data_dir + '/' + data_file_name):
    #             zips_to_process.append((self.__class__, zip_name,
    #                                     data_file_name, indices_by_zip_name[zip_name]))

    #     cores = multiprocessing.cpu_count()  # Determine number of CPU cores and split work load among them
    #     pool = multiprocessing.Pool(processes=cores)
    #     p = pool.map_async(worker, zips_to_process)
    #     try:
    #         _ = p.get()
    #     except KeyboardInterrupt:  # Caught keyboard interrupt, terminating workers
    #         pool.terminate()
    #         pool.join()
    #         sys.exit(-1)

    
            
    # def load_go_data(self, data_type='train',num_samples=1000):  
        
    #     splitter = Splitter(data_dir=self.data_dir)
    #     data = splitter.draw_data(data_type, num_samples)  

    #     zip_names = set()
    #     indices_by_zip_name = {}
        
    #     for filename, index in data:
    #         zip_names.add(filename) #collect all zip file names contained in the data in a list
    #         if filename not in indices_by_zip_name:
    #             indices_by_zip_name[filename] = []
    #         indices_by_zip_name[filename].append(index) #group all sgf file indices by zip file name
        
    #     for zip_name in zip_names:
    #         base_name = zip_name.replace('.tar.gz', '')
    #         data_file_name = base_name + data_type  # train or test
    #         if not os.path.isfile(self.data_dir + '/' + data_file_name): 
    #             # extracrt the sgf files and encode them to numpy arrays (features and labels) and save them as chunks on disk
    #             self.process_zip(zip_name, data_file_name, indices_by_zip_name[zip_name])  

    #     features_and_labels = self.group_games(data_type, data)  
    #     return features_and_labels



    
    def unzip_data(self, zip_file_name):
        #Unpack the `gz` file into a `tar` file.
        this_gz = gzip.open(self.data_dir + '/' + zip_file_name)  

        # Remove ".gz" at the end to get the name of the tar file.
        tar_file = zip_file_name[0:-3]  
        this_tar = open(self.data_dir + '/' + tar_file, 'wb')

        #  Copy the contents of the unpacked file into the `tar` file.
        shutil.copyfileobj(this_gz, this_tar)  # <3>
        this_tar.close()
        return tar_file


    # zip file name (.tar.gz)
    #data file name (name of zip + train or test)
    # game list (indices of sgf files in this zip)
    def process_zip(self, zip_file_name, data_file_name, game_list):
        tar_file = self.unzip_data(zip_file_name)  # convert .tar.gz tojust .tar
        zip_file = tarfile.open(self.data_dir + '/' + tar_file)
        name_list = zip_file.getnames() # get names of the sgf files in this zip folder
        total_examples = self.num_total_examples(zip_file, game_list, name_list)  # get no of moves in the files in this zip 

        shape = self.encoder.shape() 
        feature_shape = np.insert(shape, 0, np.asarray([total_examples]))
        features = np.zeros(feature_shape)
        labels = np.zeros((total_examples,))

        counter = 0
        for index in game_list:
            name = name_list[index + 1]
            if not name.endswith('.sgf'):
                raise ValueError(name + ' is not a valid sgf')
            # read every sgf and convert it to string then convert it to game state
            sgf_content = zip_file.extractfile(name).read()
            sgf = Sgf_game.from_string(sgf_content)  # <3>

            game_state, first_move_done = self.get_handicap(sgf)  # <4>

            # for each move int the sgf file
            for item in sgf.main_sequence_iter(): 
                color, move_tuple = item.get_move()
                point = None
                if color is not None:
                    if move_tuple is not None:  
                        row, col = move_tuple # get the place where the stone is played
                        point = Point(row + 1, col + 1)
                        move = Move.play(point)
                    else:
                        move = Move.pass_turn()  # if the player passed his turn
                    if first_move_done and point is not None:
                        features[counter] = self.encoder.encode(game_state)  # encode game state to plane(s) to be fed to the cnn
                        labels[counter] = self.encoder.encode_point(point)  # encode move
                        counter += 1
                    game_state = game_state.apply_move(move)  
                    first_move_done = True
        self.store_features_and_labels(data_file_name,features,labels)
        
    def store_features_and_labels(self,data_file_name,features,labels):
        feature_file_base = self.data_dir + '/' + data_file_name + '_features_%d'
        label_file_base = self.data_dir + '/' + data_file_name + '_labels_%d'

        # store every chunk in a seperate file 
        chunk = 0  # Due to files with large content, split up after chunksize
        chunksize = 1024
        while features.shape[0] >= chunksize:  
            feature_file = feature_file_base % chunk # add chunk number to the name
            label_file = label_file_base % chunk
            chunk += 1
            current_features, features = features[:chunksize], features[chunksize:] # remove the current features from the whole features
            current_labels, labels = labels[:chunksize], labels[chunksize:]  
            np.save(feature_file, current_features)
            np.save(label_file, current_labels)  

    #group the results from each zip into one set of features and labels
    def group_games(self, data_type, samples):
        files_needed = set(file_name for file_name, index in samples)
        file_names = []
        for zip_file_name in files_needed:
            file_name = zip_file_name.replace('.tar.gz', '') + data_type
            file_names.append(file_name)

        feature_list = []
        label_list = []
        for file_name in file_names:
            file_prefix = file_name.replace('.tar.gz', '')
            base = self.data_dir + '/' + file_prefix + '_features_*.npy'
            for feature_file in glob.glob(base):
                label_file = feature_file.replace('features', 'labels')
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype('float32')
                y = to_categorical(y.astype(int), 19 * 19)
                feature_list.append(x)
                label_list.append(y)
        features = np.concatenate(feature_list, axis=0)
        labels = np.concatenate(label_list, axis=0)
        np.save('{}/features_{}.npy'.format(self.data_dir, data_type), features)
        np.save('{}/labels_{}.npy'.format(self.data_dir, data_type), labels)

        return features, labels

    @staticmethod
    def get_handicap(sgf):
        go_board = Board(19, 19)
        first_move_done = False
        move = None
        game_state = GameState.new_game(19)
        if sgf.get_handicap() is not None and sgf.get_handicap() != 0:
            for setup in sgf.get_root().get_setup_stones():
                for move in setup:
                    row, col = move
                    go_board.place_stone(Player.black, Point(row + 1, col + 1))
            first_move_done = True
            game_state = GameState(go_board, Player.white, None, move)
        return game_state, first_move_done

    # this function gets the no of moves in all the files in the zip
    def num_total_examples(self, zip_file, game_list, name_list): # examples (trainable examples)
        total_examples = 0
        for index in game_list:
            name = name_list[index + 1]
            if name.endswith('.sgf'):
                sgf_content = zip_file.extractfile(name).read()
                sgf = Sgf_game.from_string(sgf_content)
                game_state, first_move_done = self.get_handicap(sgf)

                num_moves = 0
                for item in sgf.main_sequence_iter():
                    color, move = item.get_move()
                    if color is not None:
                        if first_move_done:
                            num_moves += 1
                        first_move_done = True
                total_examples = total_examples + num_moves
            else:
                raise ValueError(name + ' is not a valid sgf')
        return total_examples