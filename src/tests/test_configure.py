import json
import os
import pytest
from unittest.mock import Mock, patch
import main as snipsave
import sys
from io import StringIO

def test_configure_valid_email_password(mocker):
    email = "valid@email.com"
    password = "valid_password"

    # Capture the stdout output
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Mock input and getpass.getpass to avoid user interaction
    mocker.patch('builtins.input', return_value=email)
    mocker.patch('main.getpass', return_value=password)
    
    # Mock open to avoid writing to an actual file
    mock_file = mocker.mock_open()
    mocker.patch('builtins.open', mock_file)
    
    # Mock login to return the credentials without reading the actual file
    mocker.patch('main.login', return_value={"email": email, "password": password})
    
    # Prepare a mock response from the server indicating the configuration was successful
    mock_response = Mock()
    mock_response.content = json.dumps({"success": True}).encode('utf-8')
    mocker.patch('main.requests.post', return_value=mock_response)
    
    snipsave.configure()
    
    filepath = os.path.expanduser("~/.snipsave/credentials")
    
    # Assert the open was called with the expected arguments
    mock_file.assert_called_once_with(filepath, 'w')
    
    # Assert write calls on the mock file object
    mock_file().write.assert_any_call("[CREDENTIALS]\n")
    mock_file().write.assert_any_call(f"EMAIL={email}\n")
    mock_file().write.assert_any_call(f"PASSWORD={password}")
    
    # Assert the close was called on the mock file object
    mock_file().close.assert_called_once()
    
    # Assert post request with expected payload
    snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/configure", json={"email": email, "password": password})

    output = sys.stdout.getvalue()
    sys.stdout = original_stdout  # Reset the standard output to its original state
    
    assert "Successful Configuration of SnipSave CLI" in output


#TODO code doesnt currently handle invalid email so this test will have to be modified to actually catch the returned error but should be a strong starting point
# def test_configure_invalid_email(mocker):
#     invalid_email = "invalidemail.com"  # without '@'
#     password = "valid_password"

#     Capture the stdout output
#     original_stdout = sys.stdout
#     sys.stdout = StringIO()
    
#     # Mock input and getpass.getpass to avoid user interaction
#     mocker.patch('builtins.input', return_value=invalid_email)
#     mocker.patch('main.getpass', return_value=password)
    
#     # Mock open to avoid writing to an actual file
#     mock_file = mocker.mock_open()
#     mocker.patch('builtins.open', mock_file)
    
#     # Mock login to return the credentials without reading the actual file
#     mocker.patch('main.login', return_value={"email": invalid_email, "password": password})
    
#     # Prepare a mock response from the server indicating the invalid email error
#     mock_response = Mock()
#     mock_response.content = json.dumps({"success": False, "message": "Invalid email"}).encode('utf-8')
#     mocker.patch('main.requests.post', return_value=mock_response)
    
#     snipsave.configure()
    
#     # Assert the open was not called as the configuration is unsuccessful
#     mock_file.assert_not_called()
    
#     # Assert post request with expected payload
#     snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/configure", json={"email": invalid_email, "password": password})

#     output = sys.stdout.getvalue()
#     sys.stdout = original_stdout  # Reset the standard output to its original state
    
#     assert "ERROR: Unsuccessful Configuration of SnipSave CLI" in output


def test_configure_server_error(mocker):
    email = "valid@email.com"
    password = "valid_password"

    # Capture the stdout output
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Mock input and getpass.getpass to avoid user interaction
    mocker.patch('builtins.input', return_value=email)
    mocker.patch('main.getpass', return_value=password)
    
    # Mock open to avoid writing to an actual file
    mock_file = mocker.mock_open()
    mocker.patch('builtins.open', mock_file)
    
    # Mock login to return the credentials without reading the actual file
    mocker.patch('main.login', return_value={"email": email, "password": password})
    
    # Prepare a mock response from the server indicating a server error
    mock_response = Mock()
    mock_response.content = json.dumps({"success": False, "message": "Server Error"}).encode('utf-8')
    mocker.patch('main.requests.post', return_value=mock_response)
    
    snipsave.configure()
    
    # Assert post request with expected payload
    snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/configure", json={"email": email, "password": password})

    output = sys.stdout.getvalue()
    sys.stdout = original_stdout  # Reset the standard output to its original state
    
    assert "ERROR: Unsuccessful Configuration of SnipSave CLI" in output