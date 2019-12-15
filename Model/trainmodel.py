from dataprocessor import DataProcessor
from datagenerator import DataGenerator
from encoder.oneplane import OnePlaneEncoder
from encoder.sevenplanes import SevenPlaneEncoder
from encoder.elevenplanes import ElevenPlaneEncoder

import arch
# import smallarch as arch
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical

go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 16000
num_games_test = 4000
# encoder = OnePlaneEncoder((go_board_rows, go_board_cols))
# encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
encoder = ElevenPlaneEncoder((go_board_rows, go_board_cols))

processor = DataProcessor(encoder)

generator = processor.load_go_data('train', num_games,use_generator=True)
test_generator =processor.load_go_data('test', num_games_test,use_generator=True)

# from split import Splitter
# dir = 'dataset/data'
# splitter = Splitter(data_dir=dir)
# data = splitter.draw_data('train', num_games) 
# data_test = splitter.draw_data('test', num_games) 

# generator = DataGenerator(dir, data)
# test_generator = DataGenerator(dir,data_test)


input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
network_layers = arch.layers(input_shape)
model = Sequential()
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='sgd',metrics=['accuracy'])


# X, y = processor.load_go_data(num_samples=1000)
# X = X.astype('float32')
# Y = to_categorical(y, num_classes)

# network_layers = arch.layers(input_shape)
# model = Sequential()
# for layer in network_layers:
#     model.add(layer)
# model.add(Dense(num_classes, activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

# model.fit(X, Y, batch_size=128, epochs=100, verbose=1)

# weight_file = 'weights.hd5'
# model.save_weights(weight_file, overwrite=True)

# res =model.predict(X,batch_size=128)
# print(res)
epochs = 60
batch_size = 128
model.fit_generator(
generator=generator.generate(batch_size, num_classes), 
epochs=epochs,
steps_per_epoch=generator.get_num_samples() / batch_size, 
validation_data=test_generator.generate(
batch_size, num_classes), 
validation_steps=test_generator.get_num_samples() / batch_size) 

# model.save('my_model.h5')
# model.evaluate_generator(
# generator=test_generator.generate(batch_size, num_classes),
# steps=test_generator.get_num_samples() / batch_size)