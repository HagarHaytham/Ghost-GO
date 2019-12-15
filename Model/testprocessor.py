from dataprocessor import DataProcessor
# pass the encoder
# processor = DataProcessor()
# features, labels = processor.load_go_data('train', 100)

from encoder.oneplane import OnePlaneEncoder
encoder = OnePlaneEncoder((19, 19))

processor = DataProcessor(encoder)
generator = processor.load_go_data('train', 100, use_generator=True)
print(generator.get_num_samples())
generator = generator.generate(batch_size=10)
# X, y = generator.next() # implement next ??