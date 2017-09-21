import gensim
from nltk.tokenize import word_tokenize
from nlp import QA_DATASET_CSV, SIM_WORKDIR, TFIDF_PICKLE, \
    DICTIONARY_PICKLE, SIMS_PICKLE
from nlp.model.q import q_to_line, csv_to_qs
from os.path import exists

THRESHOLD = 0.5


class TfidfSimilarity(object):

    sims = None
    tf_idf = None
    dictionary = None
    qs = None
    questions_to_add = []

    def __init__(self, try_pickle=True):
        if try_pickle:
            self._initialiase_from_pickle()
        else:
            self._generate_similarity_index()

    def add_question(self, q):
        self.questions_to_add.append(q)
        self.questions_to_add = list(set(self.questions_to_add))

    def _write_question(self, q):
        with open(QA_DATASET_CSV, 'a', encoding='utf-8') as f:
            f.write(q_to_line(q))

    def query(self, q):
        query_doc = [w.lower() for w in word_tokenize(q.question)]
        query_doc_bow = self.dictionary.doc2bow(query_doc)
        query_doc_tf_idf = self.tf_idf[query_doc_bow]

        self.sims.num_best = 5
        results = self.sims[query_doc_tf_idf]

        if len(results) == 0 or results[0][1] < THRESHOLD:
            return []
        else:
            return [{"score": r[1], "question": self.qs[r[0]].question}
                    for r in results]

    def _initialiase_from_pickle(self):
        if exists(TFIDF_PICKLE) and exists(DICTIONARY_PICKLE) \
                and exists(SIMS_PICKLE) and exists(QA_DATASET_CSV):
            self.sims = gensim.similarities.Similarity.load(SIMS_PICKLE)
            self.tf_idf = gensim.models.TfidfModel.load(TFIDF_PICKLE)
            self.dictionary = gensim.corpora.Dictionary.load(DICTIONARY_PICKLE)
            self.qs = csv_to_qs(QA_DATASET_CSV)
        else:
            self._generate_similarity_index()

    def update_model(self):
        if len(self.questions_to_add) != 0:
            self._generate_similarity_index()
        else:
            print("Update not required")

    def _generate_similarity_index(self):
        if len(self.questions_to_add) != 0:
            for q_to_add in self.questions_to_add:
                self._write_question(q_to_add)
            self.questions_to_add = []

        qs = csv_to_qs(QA_DATASET_CSV)
        gen_docs = [[w.lower() for w in word_tokenize(q.question)] for q in qs]

        dictionary = gensim.corpora.Dictionary(gen_docs)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

        tf_idf = gensim.models.TfidfModel(corpus)

        sims = gensim.similarities.Similarity(SIM_WORKDIR, tf_idf[corpus],
                                              num_features=len(dictionary))

        # pickle data
        tf_idf.save(TFIDF_PICKLE)
        dictionary.save(DICTIONARY_PICKLE)
        sims.save(SIMS_PICKLE)

        self.sims = sims
        self.tf_idf = tf_idf
        self.dictionary = dictionary
        self.qs = qs
