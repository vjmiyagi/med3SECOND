import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import spacy

# Set up DataFrame
df = pd.read_csv('csv/med.csv')


nlp = spacy.load("en_core_web_sm")


# Load pickled model
model = "model.pkl"
with open(model, 'rb') as file:
   nn = pickle.load(file)


# Define function to recommend strains
# input is a string consisting of species, effect and flavor
# returned is 3 recommended strains
def recommend(input):
   vect = nlp(input).vector
   result = nn.kneighbors(vect.reshape(1,-1))
   strains = [df['strain'].iloc[x] for x in result[1][0]]
  
   return strains