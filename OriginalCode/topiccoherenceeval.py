# [Imports]====================================================================================================
from genericpath import exists
import os
import sys

import pandas as pd

from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

import matplotlib.pyplot as plt
import seaborn as sns


# [Declarations & Initializations]==========================================================================================[Declarations & Initializations]


# [Functions]====================================================================================================
# [Defines the relative path from the absolute path of local files.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def define_relativepath(in_toCreate, in_path_relative):
    if exists(in_path_relative) or in_toCreate:
        try:
            # path_base = sys._MEIPASS
            # path_base = getattr(sys, '_MEIPASS', os.getcwd())
            path_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        except Exception:
            path_base = os.path.abspath(".")
        
        return path_base + in_path_relative
    else:
        return None


# [Main]====================================================================================================
# [Main.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    data_csv = pd.read_csv(define_relativepath(False, '.\\tce\\data.csv'),usecols=["cleaned", "topic", "categorized comments count"])

    df_texts = data_csv["cleaned"].tolist()

    df_topics = data_csv["topic"].tolist()

    df_ccc = int(data_csv["categorized comments count"][0])

    texts = []
    topics = []
    x = 1
    while x < (df_ccc+1):
        texts.append(df_texts[x].split(' '))
        if (df_topics[x] not in topics):
            topics.append(df_topics[x])
        x = x + 1
    topics = [topics]

    # Creating a dictionary with the vocabulary
    word2id = Dictionary(texts)

    coherence_per_topic = []

    try:
        # Coherence model
        cm = CoherenceModel(topics=topics, 
            texts=texts, 
            # corpus=corpus, 
            # coherence='c_v', 
            coherence='c_npmi', 
            dictionary=word2id, 
            window_size=10
        )
        coherence_per_topic = coherence_per_topic + cm.get_coherence_per_topic()
        # coherence_per_topic = coherence_per_topic + cm.get_coherence()
    except ValueError:
        coherence_per_topic.append(0)

    # Visualize Results
    topics_str = ['\n '.join(t) for t in topics]

    data_topic_score = pd.DataFrame( data=zip(topics_str, coherence_per_topic), columns=['Topic', 'Coherence'] )
    data_topic_score = data_topic_score.set_index('Topic')

    fig, ax = plt.subplots( figsize=(2,6) )
    ax.set_title("Topics coherence\n $C_{npmi}$")
    sns.heatmap(data=data_topic_score, annot=True, square=True,
                cmap='Reds', fmt='.2f',
                linecolor='black', ax=ax )
    plt.yticks( rotation=0 )
    ax.set_xlabel('')
    ax.set_ylabel('')
    fig.show()
    plt.show(block=True)

