
import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt

DATA_PATH = "./Feature Extracted/data.json"


def load_data(data_path):
    with open(data_path, "r") as fp:
        data = json.load(fp)

    X = list( map( lambda x: x[0], data["mfcc"]) ) 
 
    pad = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    maxLen = len(max(X, key=len))
    total = []

    for element in X:
        lst = [pad] * ( maxLen - len( element ))
        total.append(element + lst)

    # X = np.array(total, dtype=object)
    X = np.asarray(total).astype('float32')
    y = np.array(data["labels"])

    return X, y

def prepare_datasets(test_size, validation_size):
    X, y = load_data(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split( X_train, y_train, test_size=validation_size )

    return X_train, X_validation, X_test, y_train, y_validation, y_test



def build_model(input_shape):
    """Generates RNN-LSTM model
    :param input_shape (tuple): Shape of input set
    :return model: RNN-LSTM model
    """

    # build network topology
    model = keras.Sequential()

    # 2 LSTM layers
    model.add(keras.layers.LSTM(128, input_shape=input_shape, return_sequences=True))
    model.add(keras.layers.LSTM(128))

    # dense layer
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.3))

    # output layer
    model.add(keras.layers.Dense(8, activation='softmax'))

    return model



X_train, X_validation, X_test, y_train, y_validation, y_test = prepare_datasets(0.25, 0.2)
input_shape = (X_train.shape[1], X_train.shape[2]) # 130, 13

model = build_model(input_shape)

optimiser = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimiser, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()


 # train model
history = model.fit(X_train, y_train, validation_data=(X_validation, y_validation), batch_size=32, epochs=30)

# plot accuracy/error for training and validation
# plot_history(history)

# evaluate model on test set
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print('\nTest accuracy:', test_acc)

print(input_shape)