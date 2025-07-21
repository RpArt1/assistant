import pytest
import requests_mock
from app.services.ai_service import categorise_user_query, function_list
import openai
import logging
from unittest.mock import patch, ANY


@pytest.fixture
def user_message():
    return "What is artificial intelligence?"

@patch('app.services.ai_service.call_ai')
# @pytest.mark.skip(reason="Temporarily disabled")
def test_classify_query_with_response(mock_call_ai, user_message):
    excepted_value = {'type': 'query', 'tags': ['ai']}

   # Set the return value of the mocked call_ai function to simulate a real API response
    mock_call_ai.return_value = excepted_value

    logging.debug("Mock OpenAI API setup complete")

    # Call the categorise_user_query function with the user message
    response = categorise_user_query(user_message, False)

    mock_call_ai.assert_called_once_with(user_message, ANY, function_list)
    logging.info(f"response for test call for user query categorisation is {response}")

    assert response == excepted_value


@patch('app.services.ai_service.call_ai')
# @pytest.mark.skip(reason="Temporarily disabled")
def test_categorise_user_query_with_no_response(mock_call,user_message):
    mock_call.return_value = None
    response = categorise_user_query(user_message)
    mock_call.assert_return_value = None 
    assert response == None

@patch('app.services.ai_service.call_ai')
@patch('app.services.ai_service.logging')
def test_categorise_user_query_with_exception(mock_logging,mock_ai_call,user_message):
    mock_ai_call.side_effect = Exception("Test exception")
    response = categorise_user_query(user_message, False)
    mock_ai_call.assert_called_once_with(user_message, ANY, function_list)
    assert response is None
    mock_logging.error.assert_called_once_with("Query cannot be categorised")