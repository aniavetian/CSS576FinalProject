"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - main

File contains the code for the main driver
"""
from model import Model
from backup_model import BackupModel
from plugin import run_filter


def main():
    """
    main driver to create models and run filter plugin code
    """
    my_model = Model('dataset.csv').get_model()  # generate and build the main model
    my_backup = BackupModel('spambase.data.csv').get_model()  # generate and build the backup model

    run_filter(my_model, my_backup)  # run the plugin


if __name__ == '__main__':
    main()
