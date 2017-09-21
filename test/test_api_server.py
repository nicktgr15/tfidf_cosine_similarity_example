import unittest
from unittest.mock import Mock, call
import api_server
from nlp.model.q import q


class ApiServerTestCase(unittest.TestCase):

    def test_ShouldReturnTheNumberOfQuestions_WhenIndexIsRequested(self):
        mocked_tfidf_service = Mock()
        mocked_tfidf_service.qs = [
            "question 1",
            "question 2"
        ]
        api_server.s = mocked_tfidf_service

        request, response = api_server.app.test_client.get('/')
        self.assertEqual(2, response.json['number_of_questions'])
        self.assertTrue(response.status == 200)

    def test_ShouldReturn404AndAddQuestion_WhenSimilarQuestionCannotBeFound(self):
        mocked_tfidf_service = Mock()
        mocked_tfidf_service.query.return_value = []
        api_server.s = mocked_tfidf_service
        question = "notavailablequestion"


        request, response = api_server.app.test_client.get('/ask?q='+question)
        self.assertTrue(response.status == 404)
        self.assertEqual(mocked_tfidf_service.add_question.call_args_list[0],
                         call(q(question=question)))

    def test_ShouldReturn200_WhenSimilarQuestionIsFound(self):
        mocked_tfidf_service = Mock()
        mocked_tfidf_service.query.return_value = [{
            "score": 1.0,
            "question": "somequestion"
        }]
        api_server.s = mocked_tfidf_service
        request, response = api_server.app.test_client.get('/ask?q=somequestion')
        self.assertTrue(response.status == 200)