"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - Model

File contains the code to build the neural network
"""

import keras.backend as K
import pandas as pd
from keras import models
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class Model:
    """
    Initializer
    """

    def __init__(self, file_name):
        self.model = None
        self.df = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.UNIT = 5
        self.EPOCHS = 200
        self.BATCH_SIZE = 100
        self.early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=5,
        )

        self.__load_dataset(file_name)
        self.__prep_dataset()
        self.__neural_network()

    def __load_dataset(self, file_name):
        """
        Pass in a file name to load in the dataset to be used to train the model
        :param file_name:
        """
        self.df = pd.read_csv(file_name)

    def __prep_dataset(self):
        """
        Function prepares the data to be used by the neural network
        """
        # Separate into features (X) and label (y)
        X = self.df.loc[:, self.df.columns != 'classification']
        y = self.df['classification']

        # Scale numerical columns (normalize) so model can understand them more easily
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)

        # Do a 75% (data) to 25% (test data) split
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y, random_state=104, test_size=0.25,
                                                                                shuffle=True)

    def __neural_network(self):
        """
        Function build the neural network and uses early stopping to ensure we prevent overfitting
        """
        # Build neural network
        self.model = models.Sequential()
        self.model.add(Dense(self.UNIT, activation='relu'))
        self.model.add(Dropout(0.15))
        self.model.add(Dense(self.UNIT, activation='relu'))
        self.model.add(Dropout(0.05))
        self.model.add(Dense(1, activation='sigmoid'))

        # Compile model
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', my_f1_score])

        # Train model + use early stopping
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.BATCH_SIZE,
                       epochs=self.EPOCHS,
                       callbacks=[self.early_stopping],
                       validation_data=(self.x_test, self.y_test))

        # Evaluate model
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        print('F1 score:', score[2])

        # Summary of neural network
        self.model.summary()

    def get_model(self):
        """
        Return the neural network model for later use.
        """
        return self.model


def my_f1_score(y_true, y_pred):  # taken from old keras source code
    """
    custom f1 score function
    :param y_true:
    :param y_pred:
    :return: calculated f1 value
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2 * ((precision * recall) / (precision + recall + K.epsilon()))
    return f1_val
