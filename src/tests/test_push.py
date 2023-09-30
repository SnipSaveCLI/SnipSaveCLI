from unittest.mock import Mock
import main as snipsave
from io import StringIO
import sys
import pytest

def test_push_file_exists(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="file_content"), create=True)
    mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
    mock_response = Mock()
    mock_response.content = b'{"success": true}'
    mocker.patch('main.requests.post', return_value=mock_response)
    
    response = snipsave.push("test_file", "test_snippet")
    
    snipsave.requests.post.assert_called_once_with(
        "https://snipsave.com/cli/push",
        json={
            "email": "test",
            "password": "test",
            "contents": "file_content",
            "filename": "test_file",
            "snippet_name": "test_snippet"
        }
    )
    
    assert response == mock_response


def test_push_file_not_exists(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError())
    mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
    # Capture the stdout output
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Assert the program exits with status code 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        snipsave.push("test_file", "test_snippet")
    
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    output = sys.stdout.getvalue()
    sys.stdout = original_stdout  # Reset the standard output to its original state
    
    assert "File not found in local" in output


def test_push_snipsave_error(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="file_content"), create=True)
    mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
    mock_response = Mock()
    mock_response.content = b'{"success": false, "message": "some error"}'
    mocker.patch('main.requests.post', return_value=mock_response)
    mocker.patch('main.error_response')

    # Assert the program exits with status code 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        snipsave.push("test_file", "test_snippet")
    
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    
    snipsave.error_response.assert_called_once_with({"success": False, "message": "some error"})
