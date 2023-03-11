from model import Model
import numpy as np

def main():
    model = Model()

    model.load_dataset('COMBINEDFINAL.csv')
    model.prep_dataset()
    model.neural_network()

    # Can use my_model with the predict function
    my_model = model.get_model()

    x = np.array([[0.0, 0.44, 0.001, 0.8, 0.75]])
    result = my_model.predict(x)
    print(result)

if __name__ == '__main__':
    main()
