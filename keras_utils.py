import tensorflow as tf
from file_operations import File, Directory
from app.configuration import Configuration
import os
from sklearn.model_selection import train_test_split
import csv
import numpy


def create_model():

    Sequential = tf.keras.models.Sequential
    Dense = tf.keras.layers.Dense
    

    yolo_labels = File.read_labels(Configuration.get_selected_game())
    allowed_keys = File.read_keys(Configuration.get_selected_game())

    model = Sequential()
    model.add(Dense(10, activation=tf.nn.relu, input_shape=(len(yolo_labels) * 4,)))
    model.add(Dense(10))
    model.add(Dense(len(allowed_keys), activation='sigmoid'))
    optimizer = tf.train.AdamOptimizer()
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

def numpy_training_test_data(x_list, y_list):
    x_train, x_test, y_train, y_test = train_test_split(x_list, y_list, test_size=0.2)
    return (numpy.array(x_train), numpy.array(y_train), numpy.array(x_test), numpy.array(y_test))

def train(dataset, labels):
    x_train, y_train, x_test, y_test = numpy_training_test_data(dataset, labels)
    checkpoint_file = File.get_checkpoint_file(Configuration.get_selected_game())
    model = create_model()


    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_file,
                                                 save_weights_only=True,
                                                 verbose=1)   

    model.fit(x_train, y_train,  epochs = 10,
          validation_data = (x_test,y_test),
          callbacks = [cp_callback]) 

def predict(dataset):
    return

if __name__ == "__main__":
    Configuration.set_selected_game('pong')
    checkpoint_file = File.get_checkpoint_file(Configuration.get_selected_game())
  

    dataset_file = File.get_training_dataset_fullpath(Configuration.get_selected_game())
    training_labels_file = File.get_training_labels_fullpath(Configuration.get_selected_game())
    dataset_list = []
    labels_list = []

    with open(dataset_file, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        dataset_list = list(reader)

    with open(training_labels_file, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        labels_list = list(reader)

    #print(dataset_list)
    #print(labels_list)

    #print((str(len(dataset_list)) + ' ' + str(len(labels_list))))

    #x_train, x_test, y_train, y_test = train_test_split(dataset_list, labels_list, test_size=0.2)    

    #print(x_train)
    #print(y_train)
    #print(x_test)
    #print(y_test)

    #print(str(len(x_train)))
    #print(str(len(y_train)))
    #print(str(len(x_test)))
    #print(str(len(y_test)))
    #X = numpy.array(dataset_list)
    #Y = numpy.array(labels_list)
    #train(dataset_list, labels_list)
    x_train, y_train, x_test, y_test = numpy_training_test_data(dataset_list, labels_list)
    latest = tf.train.latest_checkpoint(checkpoint_file)
    #print(latest)
    model = create_model()
    model.load_weights(latest)
    #loss, acc = model.evaluate(x_train, y_train)

    #asdf = tuple(map(tuple, x_train[0]))
    #print('now: ' + str(asdf))
    #shaped_data = K.shape(x_train[0])
    #print(shaped_data)

    single_row = numpy.expand_dims(x_train[0], axis=0)
    
    retval = model.predict(single_row)[0]
    for label in retval:
        print(label)

    #print("Restored model, accuracy: {:5.2f}%".format(100*acc))
