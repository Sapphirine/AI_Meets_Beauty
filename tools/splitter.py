import os
import shutil
import numpy as np


original = './original_part6'
train_path = './splitted_part6/train/'
test_path = './splitted_part6/validation/'

if test_path.count('/') > 1:
    shutil.rmtree(test_path, ignore_errors=False)
    os.makedirs(test_path)

if train_path.count('/') > 1:
    shutil.rmtree(train_path, ignore_errors=False)
    os.makedirs(train_path)

for folder, pl, files in os.walk(original):
    class_name = os.path.basename(folder)

    if class_name == os.path.basename(original):
        continue

    train_directory = train_path + '/' + class_name
    test_directory = test_path + '/' + class_name

    if not os.path.exists(train_directory):
        os.mkdir(train_directory)

    if not os.path.exists(test_directory):
        os.mkdir(test_directory)

    for file in files:
        current = os.path.join(folder, file)
        if np.random.rand(1) < 0.2:
            shutil.copy(current, test_path + '/'+class_name+'/'+file)
        else:
            shutil.copy(current, train_path+'/'+class_name+'/'+file)
