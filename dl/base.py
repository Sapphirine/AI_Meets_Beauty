from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend

batch_size = 8

if backend.image_data_format() == 'channels_first':
    input_shape = (3, 224, 224)
else:
    input_shape = (224, 224, 3)

model = Sequential()
model.add(Conv2D(128, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(96, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(30))
model.add(Activation('sigmoid'))

print(model.summary())

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

train_image_generator = ImageDataGenerator(
                                   rescale=1./255,
                                   zoom_range=0.3,
                                   shear_range=0.3,
                                   horizontal_flip=True)

train = train_image_generator.flow_from_directory(
                                    'data/train',
                                    target_size=(224, 224),
                                    batch_size=batch_size,
                                    class_mode='categorical')

validation_image_generator = ImageDataGenerator(rescale=1./255)

validation = validation_image_generator.flow_from_directory(
                                                        'data/validation',
                                                        target_size=(224, 224),
                                                        batch_size=batch_size,
                                                        class_mode='categorical')
model.fit_generator(
                    train,
                    steps_per_epoch=2000//batch_size,
                    epochs=30,
                    validation_data=validation,
                    validation_steps=800//batch_size)

model.save('test_model.h5')
