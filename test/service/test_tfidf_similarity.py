import unittest
from unittest.mock import patch
from nlp.model.q import q
from nlp.service.tfidf_similarity import TfidfSimilarity


class TfIdfSimilarityTestCase(unittest.TestCase):

    @patch.object(TfidfSimilarity, '_initialiase_from_pickle')
    def test_ShouldAddQuestionOnce_WhenSameQuestionAddedAgain(self, pickle_spy):

        q1 = q(question="question1")
        q2 = q(question="question2")

        x = TfidfSimilarity()
        x.add_question(q1)
        self.assertEqual(1, len(x.questions_to_add))
        x.add_question(q1)
        self.assertEqual(1, len(x.questions_to_add))
        x.add_question(q2)
        self.assertEqual(2, len(x.questions_to_add))

        print(x.questions_to_add)

    @patch.object(TfidfSimilarity, '_initialiase_from_pickle')
    @patch.object(TfidfSimilarity, '_generate_similarity_index')
    def test_ShouldUpdateTheModel_WhenNewQuestionsAreAvailable(self,
                                                              generate_spy,
                                                              pickle_spy):
        x = TfidfSimilarity()
        q1 = q(question="question1")
        x.add_question(q1)
        x.update_model()

        x._generate_similarity_index.assert_called_once()

    @patch.object(TfidfSimilarity, '_initialiase_from_pickle')
    @patch.object(TfidfSimilarity, '_generate_similarity_index')
    def test_ShouldNotUpdateTheModel_WhenNoNewQuestionsAreAvailable(self,
                                                              generate_spy,
                                                              pickle_spy):
        x = TfidfSimilarity()
        x.questions_to_add = []
        x.update_model()

        x._generate_similarity_index.assert_not_called()
