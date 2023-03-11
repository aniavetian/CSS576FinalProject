import numpy as np
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
        self.__train_model()
        self.model.summary()

    def __build_model(self):
        # Build neural network
        model = models.Sequential()
        model.add(Dense(self.UNIT * 2, activation='relu'))
        model.add(Dense(self.UNIT * 4, activation='relu'))
        model.add(Dense(self.UNIT, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        return model

    def __load_data(self, file):
        data = pd.read_csv(file)
        x = data.loc[:, data.columns != 'label']  # all the feature vectors
        y = data['label']   # labels, 0 as benign, 1 as malicious

        # Load data
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

        # Reshape data
        self.X_train = np.asarray(x_train.astype('float32'))
        self.X_test = np.asarray(x_test.astype('float32'))
        self.y_train = np.asarray(y_train.astype('float32'))
        self.y_test = np.asarray(y_test.astype('float32'))

    def __train_model(self):
        # Train model
        self.model.fit(self.X_train, self.y_train,
                       batch_size=self.BATCH_SIZE,
                       epochs=self.EPOCHS,
                       callbacks=[self.early_stopping],
                       verbose=1,
                       validation_data=(self.X_test, self.y_test)
                       )

        score = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def get_model(self):
        return self.model
