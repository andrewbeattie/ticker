import json
import pytest
from unittest.mock import patch

from tickspot.net.service import Authorize
from tickspot.net.manual_settings import Constants

constants = Constants()

@pytest.mark.parametrize(
    "username, password, mock_response, expected_result",
    [
        ("user1", "pass1", {"api_token": "123", "subscription_id": "456"}, ("123", "456")),
        ("user2", "pass2", {"api_token": "789", "subscription_id": "101112"}, ("789", "101112")),
    ],
)


def test_authorize(username, password, mock_response, expected_result):

    mock_response_obj = type("MockResponse", (object,), {"text": json.dumps([mock_response])})
    with patch("requests.get", return_value=mock_response_obj) as mock_get:

        auth = Authorize(username, password)
        result = auth.authorize(username, password)

        assert result == expected_result

        mock_get.assert_called_with(
            constants.BASE_URL + "roles.json", headers={"User-agent": f"Ticker ({username})"}, auth=(username, password)
        )
