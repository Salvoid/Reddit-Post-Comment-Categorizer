# [Imports]========================================================================================================================================[Imports]
import numpy as np
import scipy.sparse
from sklearn.feature_extraction.text import CountVectorizer

import other_module as otherModule # Other needed functions


# [Declarations & Initializations]==========================================================================================[Declarations & Initializations]
input_dir = "d_raw"
output_dir = "d_input"

# [Functions]====================================================================================================
def preprocess_data():
    texts = list()
    with open(otherModule.define_relativepath(False,"\\{}\\texts.txt".format(input_dir)), encoding="utf8") as file:
        for line in file:
            texts.append(line.strip())

    vectorizer = CountVectorizer(min_df=1)
    bow_matrix = vectorizer.fit_transform(texts).toarray()

    idx = np.where(bow_matrix.sum(axis=-1) > 0)
    bow_matrix = bow_matrix[idx]

    vocab = vectorizer.get_feature_names()

    scipy.sparse.save_npz(otherModule.define_relativepath(True,"\\{}\\bow_matrix.npz".format(output_dir)), scipy.sparse.csr_matrix(bow_matrix))
    with open(otherModule.define_relativepath(True,"\\{}\\vocab.txt".format(output_dir)), 'w') as file:
        for line in vocab:
            file.write(line + '\n')

