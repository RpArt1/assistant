import unittest
import openai
from app.services.ai_service import categorise_user_query
from app.utils.env_settings import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


# !!! EACH QUERY COSTS !!!

BASELINE_RESPONSES = {
    "What is meta model in AI?": {'type': 'query', 'tags': ['ai']},
    "What is the bes song in the world ?" : {'type': 'query', 'tags': []},
    "please store me this attachment" : {'type': 'action', 'tools': ['memory'], 'content': 'store attachment'}
}


def assert_query_response(actual, expected):
    assert actual == expected, f"Expected {expected}, but got {actual}"

def assert_action_response(actual, expected):
    assert actual['type'] == expected['type'], f"Expected type {expected['type']}, but got {actual['type']}"
    assert actual['tools'] == expected['tools'], f"Expected tools {expected['tools']}, but got {actual['tools']}"
    assert any(content in actual['content'] for content in expected['content']), \
        f"Expected content to contain one of {expected['content']}, but got {actual['content']}"



class TestRegression(unittest.TestCase):
    def test_regression_cases(self):
        for query, expected_response in BASELINE_RESPONSES.items():
            actual_response = categorise_user_query(query, False)
            if expected_response['type'] == 'query':
                assert_query_response(actual_response, expected_response)
            elif expected_response['type'] == 'action':
                assert_action_response(actual_response, expected_response)
            else:
                self.fail(f"Unexpected type: {expected_response['type']}")



if __name__ == '__main__':
    unittest.main()