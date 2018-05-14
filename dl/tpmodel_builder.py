import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Dropout, Flatten
from keras.utils.np_utils import to_categorical

batch_size = 16

image_data_generator = ImageDataGenerator(rescale=1./255)

train_generator = image_data_generator.flow_from_directory(
    'data/train',
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False)

validation_generator = image_data_generator.flow_from_directory(
    'data/validation',
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)

train = np.load('train_100.npy')
validation = np.load('validation_100.npy')

model = Sequential()
model.add(Flatten(input_shape=train.shape[1:]))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_generator.class_indices), activation='sigmoid'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_labels = to_categorical(train_generator.classes, num_classes=len(train_generator.class_indices))
validation_labels = to_categorical(validation_generator.classes, num_classes=len(train_generator.class_indices))

result = model.fit(train, train_labels,
                    epochs=50,
                    batch_size=batch_size,
                    validation_data=(validation, validation_labels))

np.save('classes_100.npy', train_generator.class_indices)
model.save('./model_100.h5')

(eval_loss, eval_accuracy) = model.evaluate(
    validation, validation_labels, batch_size=batch_size, verbose=1)


plt.plot(result.history['acc'])
plt.plot(result.history['val_acc'])
plt.title('Accuracy over epochs')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

plt.plot(result.history['loss'])
plt.plot(result.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
