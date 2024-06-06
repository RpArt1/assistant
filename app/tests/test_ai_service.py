import pytest
import requests_mock
from ..services.ai_service import categorise_user_query, function_list
import openai
import logging
from unittest.mock import patch, ANY

@patch('app.services.ai_service.call_ai')
def test_classify_query(mock_call_ai):
    user_message = "What is artificial intelligence?"
    excepted_value = {'type': 'query', 'tags': ['ai']}

   # Set the return value of the mocked call_ai function to simulate a real API response
    mock_call_ai.return_value = excepted_value

    logging.info("Mock OpenAI API setup complete")

    # Call the categorise_user_query function with the user message
    response = categorise_user_query(user_message)

    mock_call_ai.assert_called_once_with(user_message, ANY, function_list)
    logging.info(f"response for test call for user query categorisation is {response}")

    assert response == excepted_value
