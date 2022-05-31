import pytest
import json
from task_2.app import get_app


@pytest.fixture
def app():
    app = get_app()
    return app


def test_should_return_list_of_items(client, mocker):
    headers = {
        'Content-Type': 'application/json'
    }
    request_body = {
        "text": "ACUVUE 1-DAY MOIST TAGESLINSEN WEICH"
    }
    expected_value = "CONTACT LENSES"
    mocker.patch('task_2.app.MultiClassificator.predict', return_value=expected_value)
    response = client.post('/api/goods/classify', data=json.dumps(request_body), headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert response.json['class'] == expected_value
