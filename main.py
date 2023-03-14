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
    model = Model('dataset.csv')
    backup = BackupModel('spambase.data.csv')

    # Can use my_model with the predict function
    my_model = model.get_model()
    my_backup = backup.get_model()

    x = [0.65] * 48  # Test Value to test prediction
    z = [0.65] * 54
    y = np.array([z])
    w = np.array([x])

    result = my_model.predict(w)
    print(result)  # test prediction

    result2 = model.model.predict(w)
    print(result2)

    result3 = backup.model.predict(y)
    print(result3)
    result4 = my_backup.predict(y)
    print(result4)


if __name__ == '__main__':
    main()
