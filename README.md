# CS130
CS130 open source project

## Luanching the server (Local)

1. Download the source code to your desired path

2. Luanching the virtualenv in the repository. 
    * Change your path to venv
    ```
    cd your_path/CS130/webserver/venv
    ```
    * Luaching the virtualenv by typing the command
    ``` shell
    $ source bin/activate
    ``` 
    * You should see **(venv)** before your command prompt
    * If you want to leave venv, type "deactivate"

3. Launching the server
    * Go the website directory
    ```
    cd your_path/CS130/webserver/website
    ```
    * Before running the server, the database should be setup by running the command
    ```
    $ python manage.py migrate
    ```
    &nbsp; &nbsp; &nbsp; &nbsp;If the previous command doesn't work, run the following instead:
    ```
    $ python manage.py syncdb 
    ```
    * Running the server 
    ```
    $ python manage.py runserver
    ```
   * You should see the information like this
   ```
   Performing system checks...

    System check identified no issues (0 silenced).
    February 03, 2018 - 22:00:15
    Django version 2.0.2, using settings 'website.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
   ``` 
   * Check the server by going to http://127.0.0.1:8000/alphacode in your browser 

## Running test cases for web server 
    your_path/CS130/webserver/website$ python manage.py test
