import numpy as np
import math
from keras import applications
from keras.preprocessing.image import ImageDataGenerator

batch_size = 16

model = applications.VGG16(weights='imagenet', include_top=False)

image_data_generator = ImageDataGenerator(rescale=1./255)

train_generator = image_data_generator.flow_from_directory(
    'data/train',
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)

train = model.predict_generator(
    train_generator, int(math.ceil(len(train_generator.filenames)/batch_size)))

np.save('train_100.npy', train)

validation_generator = image_data_generator.flow_from_directory(
    'data/validation',
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)

validation = model.predict_generator(
    validation_generator, int(math.ceil(len(validation_generator.filenames)/batch_size)))

np.save('validation_100.npy', validation)
