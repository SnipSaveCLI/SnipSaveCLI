"""

Code to use the SnipSave cli

"""
import requests
import sys
import json
import os
from getpass import getpass
import configparser

URL = "http://snipsavedev.com"

HELP_STRING = "For more help, please visit\nour documentation at:\nhttps://github.com/SnipSaveCLI/SnipSaveCLI/blob/main/README.md"

def error_response(resp):
    print()
    print("ERROR: {}".format(resp["message"]))
    print()

def help_():
    print()
    print("    Welcome to the SnipSave CLI!")
    print("------------------------------------")
    print()
    print("Available Commands:")
    print("`ssv configure`                         - Add your Username and Password to the SnipSave CLI")
    print("`ssv pull <snippet_title>`              - Clone a snippet from your repository")
    print("`ssv push <local_file> <snippet_title>` - Push a snippet to your repository")
    print()
    print(HELP_STRING)
    print()
    print("------------------------------------")


def login():
    config = configparser.ConfigParser()
    filepath = os.path.expanduser("~/.snipsave/credentials")
    config.read(filepath)
    email = config.get('CREDENTIALS', 'EMAIL') 
    password = config.get('CREDENTIALS', 'PASSWORD')
    return { "email" : email, "password" : password }



def push(f, snippet_name=None):
    myobj = login()

    try:
        snippet = open(f, "r")
    except FileNotFoundError:
        print("File not found in local")
        print()
        sys.exit(1)

    # Get File Contents    
    snippet = snippet.read()

    # Put contents into object
    myobj["contents"] = snippet 
    myobj["filename"] = f
    myobj["snippet_name"] = snippet_name

    # Send to SS
    resp = requests.post("{}/cli/push".format(URL), json = myobj)
    
    resp_json = json.loads(resp.content)
    
    if not resp_json["success"]:
        error_response(resp_json)    
        sys.exit(1)
    if snippet_name == None:
        snippet_name = f
    
    print("------------------------------")
    print()
    print("Successful Upload to SnipSave:")
    print("+ {}".format(snippet_name))
    print()
    print("------------------------------")
  
    return resp
    
def pull(title):
    payload = login()
 
    payload["title"] = title

    resp = requests.post("{}/cli/pull".format(URL), json = payload)

    resp_json = json.loads(resp.content)
    if not resp_json["success"]:
        error_response(resp_json)    
        sys.exit(1)


    # Needs to check for file and prompt to overwrite, or look for -force flag
    with open(resp_json['new_title'], 'w') as _file:
        _file.write(resp_json['contents'])
        
    print("------------------------------")
    print()
    print("Successful Pull from SnipSave:")
    print("- {} --> {}".format(title, resp_json['new_title']))
    print()
    print("------------------------------")
    
    return resp


def configure():
    email = input("Enter Email: ")
    password = getpass("Enter Password: ")

    filepath = os.path.expanduser("~/.snipsave/credentials")
    config = open(filepath, "w")
    config.write("[CREDENTIALS]\n")
    config.write("EMAIL={}\n".format(email))
    config.write("PASSWORD={}".format(password))
    config.close()
   
    payload = login()
    print(payload)
    resp = requests.post("{}/cli/configure".format(URL), json = payload)
    resp_json = json.loads(resp.content)
    print()
    if resp_json['success']:
        print("-----------------------------------------")
        print()
        print("Successful Configuration of SnipSave CLI")
        print()
        print("-----------------------------------------")
    else:
        print("--------------------------------------------------")
        print()
        print("ERROR: Unsuccessful Configuration of SnipSave CLI")
        print()
        print("--------------------------------------------------")
        


if len(sys.argv) < 2:
    help_()
    sys.exit(1)

if (sys.argv[1] == "push"):
    # Check for no argv 2 || 3
    # Can have no arg3, but needs to match a snippet name
    if (len(sys.argv) != 4 and len(sys.argv) != 3):
        print("Incorrect Usage of `ssv push`")
        print()
        print("Correct usage is:")
        print("ssv push <local_filename> <snippet_name> or")
        print("ssv push <local_filename>.extension")
        print()
        print(HELP_STRING)
        print()
        print("Or use the command:\n`ssv help`")
        print()
    else:
        if (len(sys.argv) == 4):
            push(sys.argv[2], sys.argv[3])
        else:
            push(sys.argv[2])
elif (sys.argv[1] == "pull"):
    # Check for no/incorrect argv 2
    if (len(sys.argv) != 3):
        print("Incorrect Usage of `ssv pull`")
        print()
        print("Correct usage is:")
        print("ssv pull <snippet_name>")
        print()
        print(HELP_STRING)
        print()
        print("Or use the command:\n`ssv help`")
        print()
    else:
        pull(sys.argv[2])
elif (sys.argv[1] == "configure"):
    if (len(sys.argv) != 2):
        print("Incorrect Usage of `ssv configure`")
        print()
        print("Correct usage is:")
        print("ssv configure")
        print()
        print(HELP_STRING)
        print()
        print("Or use the command:\n`ssv help`")
        print()
    else:
        configure()
elif (sys.argv[1] == "help"):
    help_()
