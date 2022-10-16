import pickle
import numpy as np
import sys
#sys.path.append("rt-transaction-classifier/app/utils") 

classifier_path = "utils/transformers/classifier.sav"
vectorizer_path = "utils/transformers/word_vectorizer.sav"

loaded_model = pickle.load(open(classifier_path, 'rb'))
loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))

N_FEATURES = 13

def process_tag(tag: str):
    vector = loaded_vectorizer.transform([tag])
    return vector.toarray()

def convert_input_to_array(input_dict: dict):
    input_array = np.zeros(N_FEATURES)

    input_array[0] = input_dict['amount']
    input_array[1] = input_dict['hour']
    input_array[2:] = process_tag(input_dict['tag'])
    return input_array.reshape(1,-1)

def make_prediction(input_dict):
    input_array = convert_input_to_array(input_dict=input_dict)
    prediction = loaded_model.predict(input_array)
    return prediction
