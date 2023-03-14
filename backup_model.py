"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - backup model

File contains the code to build the backup validation model
"""

import keras.backend as K
import pandas as pd
import sklearn
from keras import models
from keras.callbacks import EarlyStopping
from keras.layers import Dense


class BackupModel:
    def __init__(self, file):
        self.y_test = None
        self.y_train = None
        self.X_test = None
        self.X_train = None
        self.early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=5,
        )
        self.__load_data(file)

        self.BATCH_SIZE = 5
        self.EPOCHS = 50
        self.UNIT = 50

        self.model = self.__build_model()
        self.model.summary()

    def __build_model(self):
        """
        build and compile the model
        :return: trained model
        """
        # Build neural network
        model = models.Sequential()
        model.add(Dense(self.UNIT * 2, activation='relu'))
        model.add(Dense(self.UNIT * 4, activation='relu'))
        model.add(Dense(self.UNIT, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', my_f1_score])
        # Train model
        model.fit(self.X_train, self.y_train,
                  batch_size=self.BATCH_SIZE,
                  epochs=self.EPOCHS,
                  callbacks=[self.early_stopping],
                  verbose=1,
                  validation_data=(self.X_test, self.y_test)
                  )

        score = model.evaluate(self.X_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        print('F1 score:', score[2])

        return model

    def __load_data(self, file):
        """
        load a csv file of data to train with
        :param file:
        """
        data = pd.read_csv(file)
        x = data.loc[:, data.columns != 'label']  # all the feature vectors
        y = data['label']  # labels, 0 as benign, 1 as malicious

        # Load data
        self.x_train, self.x_test, self.y_train, self.y_test = \
            sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    def get_model(self):
        """
        get the model
        :return: trained model
        """
        return self.model


def my_f1_score(y_true, y_pred):  # taken from old keras source code
    """
    custom f1 calculation
    :param y_true:
    :param y_pred:
    :return: custom f1 score
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2 * ((precision * recall) / (precision + recall + K.epsilon()))
    return f1_val
