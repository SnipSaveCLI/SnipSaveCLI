# [SnipSave](https://snipsave.com/) Command Line Interface (CLI) BETA VERSION #
This is the Official Repository for the SnipSave Command Line Interface (CLI)

NOTE: The SnipSave CLI is currently in Beta Mode


## Intro ##
In order to interact with your SnipSave repository from the command line, you can use the SnipeSave command line interface (CLI) to do so. It is very simple to use compared to other common version control systems, while maintaining the main features.

## Dependencies: ##
The SnipSave CLI is written in python, therefore python 3.6 or greater is recommended on your machine.


## Steps to Get Started ##
1. Clone the repository
2. Run the installer script, for your respective operating system Ex: if on Mac OS: run `sh MAC_INSTALLER.sh`
  - The general Steps the installer script follows are:
    - Checking if Python 3 is installed
    - Creating a credentials file on your machine in the location ~/.snipsave/credentials
    - Copy the main Python file to ~/.snipsave
    - Sets the following [alias](https://linuxize.com/post/how-to-create-bash-aliases/)
      - alias ssv='python3 ~/.snipsave/snipsave_cli.py' 
3. Run `ssv configure` and enter your email and password when prompted

## Running with Docker ##
Docker provides an isolated environment to run the SnipSave CLI without the need to install its dependencies directly on your machine.
1. Clone the repository
2. docker build -t snipsave-cli .
3. docker run -it snipsave-cli

## Running unittests
1. follow steps to build docker image
2. docker run -it snipsave-cli pytest /opt/tests

tests can be run outside of docker with
pytest ./src/tests

## Commands ##
All commands are preceded by `ssv`

### ssv pull <snippet name> ###
This command is used to pull a snippet from the user’s account. It will overwrite any file with the same name as the snippet.

Ex:
$ ssv pull login

If the snippet is more than one word, simply add quotations. 

Ex:
$ ssv pull “login snippet”

This will pull in the snippet into your local environment.

If your Snippet is in one of the following languages, it will automatically append the file extension: Python, Javascript, Text, C#, CSS, Groovy, HTML, Java, JSON, MySQL, PHP, R, Shell, Ruby, Rust, Swift, Typescript, YAML

### ssv push <local_file> <snippet_title> ###
This command pushes the local code snippet to SnipSave. Before pushing to your repository, the snippet has to be created in the browser. This is to ensure that the command knows what Snippet is being referenced when pushing to your Snippet Repository.

Ex:
$ ssv push login.py login

This will push your snippet to your repository

### ssv configure ###
This command is used to configure the user’s email and password in order to authenticate users from the command line. It will prompt you for your email and password, which will add your credentials to a file located at ~/.snipsave/credentials

## Throttling ##
The SnipSave CLI allows for 5 requests every 30 seconds under the free tier. Upgrading to SnipSave Pro allows for a much greater 100 requests per 30 seconds. It is recommended to upgrade to SnipSave pro if your applications will be utilizing the CLI, so they are not stopped by the request limit.

You can contact SnipSave Support at support@snipsave.com for details on our unlimited request plan for the CLI.
