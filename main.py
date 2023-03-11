from model import Model
import numpy as np


def main():
    model = Model('COMBINEDFINAL.csv')

    # Can use my_model with the predict function
    my_model = model.get_model()

    x = np.array([[0.0, 0.44, 0.001, 0.8, 0.75]])  # Test Value to test prediction
    result = my_model.predict(x)
    print(result)  # test prediction

    result2 = model.model.predict(x)
    print(result2)


if __name__ == '__main__':
    main()
