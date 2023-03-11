"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - main

File contains the code for the main driver
"""
from model import Model
from backup_model import BackupModel
import numpy as np


def main():
    model = Model('COMBINEDFINAL.csv')
    backup = BackupModel('spambase.data.csv')

    # Can use my_model with the predict function
    my_model = model.get_model()
    my_backup = backup.get_model()

    x = np.array([[0.0, 0.44, 0.001, 0.8, 0.75]])  # Test Value to test prediction
    z = [0.65] * 54
    y = np.array([z])
    result = my_model.predict(x)
    print(result[0][0])  # test prediction

    result2 = model.model.predict(x)
    print(result2[0][0])

    result3 = backup.model.predict(y)
    print(result3[0][0])
    result4 = my_backup.predict(y)
    print(result4[0][0])


if __name__ == '__main__':
    main()
