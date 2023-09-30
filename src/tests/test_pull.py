from unittest.mock import Mock
import main as snipsave  # Replace with your actual module name
import json
import pytest

def test_pull_file_not_exist_locally(mocker):
    mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
    mock_response = Mock()
    mock_response_content = {"success": True, "new_title": "test_snippet", "contents": "print('Hello, World!')"}
    mock_response.content = json.dumps(mock_response_content).encode('utf-8')
    mocker.patch('main.requests.post', return_value=mock_response)
    
    mock_open = mocker.patch('builtins.open', mocker.mock_open(), create=True)
    
    title = "test_snippet"
    response = snipsave.pull(title)
    
    snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/pull", json={"email": "test", "password": "test", "title": "test_snippet"})
    
    # Asserting that the file is attempted to be created with correct name and content is written to it.
    mock_open.assert_called_once_with(mock_response_content['new_title'], 'w')
    file_handle = mock_open()
    file_handle.write.assert_called_once_with(mock_response_content['contents'])
    
    assert response == mock_response

# TODO this test should be uncommented when the code to check if the file exists locally is implemented
# def test_pull_file_exist_locally_ask_overwrite(mocker):
#     mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
#     mock_response = Mock()
#     mock_response_content = {"success": True, "new_title": "test_snippet", "contents": "print('Hello, World!')"}
#     mock_response.content = json.dumps(mock_response_content).encode('utf-8')
#     mocker.patch('main.requests.post', return_value=mock_response)
    
#     # Mocking built-in open function globally.
#     mocker.patch('builtins.open', mocker.mock_open(read_data='Existing Content'), create=True)
    
#     # Mocking os.path.exists to return True, indicating that the file exists locally.
#     mocker.patch('os.path.exists', return_value=True)
    
#     # Mocking built-in input function to return 'y', simulating user agreeing to overwrite the file.
#     mock_input = mocker.patch('builtins.input', return_value='y')
    
#     title = "test_snippet"
#     response = snipsave.pull(title)
    
#     snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/pull", json={"email": "test", "password": "test", "title": "test_snippet"})
    
#     # Asserting that the user was asked to overwrite.
#     mock_input.assert_called_once_with("File exists locally. Do you want to overwrite? (y/n): ") # TODO: replace this message with the actual message when implemented.
    
#     # Asserting that the file is attempted to be created with correct name and new content is written to it.
#     snipsave.open.assert_called_once_with(mock_response_content['new_title'], 'w')
#     file_handle = snipsave.open()
#     file_handle.write.assert_called_once_with(mock_response_content['contents'])
    
#     assert response == mock_response

# TODO this test should be uncommented when the force flag is implemented, this test assumes a parameter called force is passed to the pull function
# def test_pull_file_exists_locally_with_force_flag(mocker):
#     # Mock the login to return some credentials
#     mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
#     # Prepare a mock response from the server
#     mock_response = Mock()
#     mock_response_content = {"success": True, "new_title": "test_snippet", "contents": "print('Hello, World!')"}
#     mock_response.content = json.dumps(mock_response_content).encode('utf-8')
#     mocker.patch('main.requests.post', return_value=mock_response)
    
#     # Mock the existence of the file
#     mocker.patch('os.path.exists', return_value=True)
    
#     # Mock the built-in open function
#     mocker.patch('builtins.open', mocker.mock_open(), create=True)
    
#     # Mock the input function. This should not be called due to the force flag
#     mock_input = mocker.patch('builtins.input', side_effect=Exception("input should not be called with force flag"))

#     # Call the pull function with force flag set to True
#     title = "test_snippet"
#     response = snipsave.pull(title, force=True)
    
#     # Assert post request with expected payload
#     snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/pull", json={"email": "test", "password": "test", "title": "test_snippet"})
    
#     # Assert that the input function was not called
#     mock_input.assert_not_called()
    
#     # Assert the file was opened in write mode and content was written to it
#     snipsave.open.assert_called_once_with(mock_response_content['new_title'], 'w')
#     file_handle = snipsave.open()
#     file_handle.write.assert_called_once_with(mock_response_content['contents'])
    
#     assert response == mock_response


# TODO currently the code only checks for any error with the call to snipsave, but does not check for specific errors. This test should be copied and modified to check for other errors such as a 500 error
def test_pull_file_not_exists_in_snipsave(mocker):
    # Mock the login to return some credentials
    mocker.patch('main.login', return_value={"email": "test", "password": "test"})
    
    # Prepare a mock response from the server indicating the file does not exist
    mock_response = Mock()
    mock_response.content = json.dumps({"success": False, "message": "File not found"}).encode('utf-8')
    mocker.patch('main.requests.post', return_value=mock_response)
    
    # Mock the error_response to avoid printing to the console and to assert it was called
    mock_error_response = mocker.patch('main.error_response')
    
    # Assert the program exits with status code 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        snipsave.pull("nonexistent_file")
    
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    
    # Assert post request with expected payload
    snipsave.requests.post.assert_called_once_with("https://snipsave.com/cli/pull", json={"email": "test", "password": "test", "title": "nonexistent_file"})
    
    # Assert error_response was called with the correct argument
    mock_error_response.assert_called_once_with(json.loads(mock_response.content))