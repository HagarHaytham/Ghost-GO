from dataprocessor import DataProcessor
from datagenerator import DataGenerator
from encoder.oneplane import OnePlaneEncoder
from encoder.sevenplanes import SevenPlaneEncoder
from encoder.elevenplanes import ElevenPlaneEncoder

# import arch
import smallarch as arch
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical
from keras.models import load_model
model = load_model('/content/checkpoints/ElevenPlanes_smallarch_model_epoch_48.h5')

go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 10000
encoder = ElevenPlaneEncoder((go_board_rows, go_board_cols))

processor = DataProcessor(encoder)
test_generator =processor.load_go_data('test', num_games,use_generator=True)

epochs = 100
batch_size = 128

model.evaluate_generator(
generator=test_generator.generate(batch_size, num_classes),
steps=test_generator.get_num_samples() / batch_size)
