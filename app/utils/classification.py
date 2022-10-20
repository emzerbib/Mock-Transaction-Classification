import pickle
import numpy as np
from ..mock_transactions import TransactionInput

classifier_path = "utils/transformers/classifier.sav"
vectorizer_path = "utils/transformers/word_vectorizer.sav"

loaded_model = pickle.load(open(classifier_path, 'rb'))
loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))

N_FEATURES = 13

def process_tag(tag: str):
    vector = loaded_vectorizer.transform([tag])
    return vector.toarray()

def convert_input_to_array(input_transaction: TransactionInput):
    input_array = np.zeros(N_FEATURES)

    input_array[0] = input_transaction.amount
    input_array[1] = input_transaction.hour
    input_array[2:] = process_tag(input_transaction.tag)

    return input_array.reshape(1,-1)

def make_prediction(input_transaction: TransactionInput):
    input_array = convert_input_to_array(input_transaction)
    prediction = loaded_model.predict(input_array)
    return prediction
