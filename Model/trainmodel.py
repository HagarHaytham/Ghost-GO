from dataprocessor import DataProcessor
from datagenerator import DataGenerator
from encoder.oneplane import OnePlaneEncoder
import arch
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import ModelCheckpoint

go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 100
encoder = OnePlaneEncoder((go_board_rows, go_board_cols))
processor = DataProcessor(encoder)
# print(processor.load_go_data('train', num_games))
# generator = DataGenerator('dataset/data', processor.load_go_data('train', num_games))
# test_generator = DataGenerator('dataset/data',processor.load_go_data('test', num_games))

from split import Splitter
dir = 'dataset/data'
splitter = Splitter(data_dir=dir)
data = splitter.draw_data('train', num_games) 
data_test = splitter.draw_data('test', num_games) 

generator = DataGenerator(dir, data)
test_generator = DataGenerator(dir,data_test)


input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
network_layers = arch.layers(input_shape)
model = Sequential()
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='sgd',metrics=['accuracy'])

epochs = 5
batch_size = 128
model.fit_generator(
generator=generator.generate(batch_size, num_classes), 
epochs=epochs,
steps_per_epoch=generator.get_num_samples() / batch_size, 
validation_data=test_generator.generate(
batch_size, num_classes), 
validation_steps=test_generator.get_num_samples() / batch_size, 
callbacks=[
ModelCheckpoint('checkpoints/FirtsLarge_model_epoch_{epoch}.h5')
]) 

model.evaluate_generator(
generator=test_generator.generate(batch_size, num_classes),
steps=test_generator.get_num_samples() / batch_size)