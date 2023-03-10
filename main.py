
from model import Model

def main():
   model = Model()

   model.load_dataset('COMBINEDFINAL.csv')
   model.prep_dataset()
   model.neural_network()

   # Can use my_model with the predict function
   my_model = model.get_model()



if __name__ == '__main__':
    main()