"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - Model

File contains the code to build the neural network
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np
from keras.layers import Dense, Dropout
from keras import models

class Model:
   """
   Initializer
   """
   def __init__(self):
      self.model = None
      self.df = None
      self.x_train = None
      self.x_test = None
      self.y_train = None
      self.y_train = None
      self.UNIT = 5
      self.EPOCHS = 200
      self.BATCH_SIZE = 100

   """
   Pass in a file name to load in the dataset to be used to train the model
   """
   def load_dataset(self, file_name):
      self.df = pd.read_csv(file_name)

   """
   Custom encoding function to encode whether we have spam or ham in the dataset
   """
   def custom_encode(self, val):
      if val == 'spam':
         return 1
      else:
         return 0

   """
   Function prepares the data to be used by the neural network
   """
   def prep_dataset(self):

      # Only using relevent columns with features we want
      self.df = self.df[['non_standard_html_tag_count', 'spam_keywords', 'total_links', 'total_keywords_in_subject', 'total_keywords_in_body', 'classification']]

      # Scale numerical columns (normalize) so model can understand them more easily
      scaler = MinMaxScaler()
      self.df[['non_standard_html_tag_count', 'spam_keywords', 'total_links', 'total_keywords_in_subject', 'total_keywords_in_body']] = \
         scaler.fit_transform(self.df[['non_standard_html_tag_count', 'spam_keywords', 'total_links', 'total_keywords_in_subject', 'total_keywords_in_body']])

      self.df['classification'] = self.df['classification'].apply(self.custom_encode)

      # Seperate into features (X) and lable (y)
      X = self.df.loc[:, self.df.columns != 'classification']
      y = self.df['classification']

      # Do a 75% (data) to 25% (test data) split
      self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y, random_state=104, test_size=0.25, shuffle=True)


   """
   Function build the neural network and uses early stopping to ensure we prevent
   overfitting
   """
   def neural_network(self):

      # Build neural network
      self.model = models.Sequential()
      self.model.add(Dense(self.UNIT, activation='relu'))
      self.model.add(Dropout(0.15))
      self.model.add(Dense(self.UNIT, activation='relu'))
      self.model.add(Dropout(0.05))
      self.model.add(Dense(1, activation='sigmoid'))

      # Compile model
      self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

      # Train model + use early stopping
      self.model.fit(self.x_train, self.y_train, batch_size=self.BATCH_SIZE, epochs=self.EPOCHS, validation_data=(self.x_test, self.y_test))

      # Evaluate model
      score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
      print('Test loss:', score[0])
      print('Test accuracy:', score[1])

      # Summary of neural network
      self.model.summary()

   """
   Return the neural network model for later use.
   """
   def get_model(self):
      return self.model