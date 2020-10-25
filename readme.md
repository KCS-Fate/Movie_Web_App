# Movie Web Application

## Description

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd Movie_Web_App
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Execution

**Running the application**

From the *COMPSCI-235* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The *COMPSCI-235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing may require that file *movie_web_app/Tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *movie_web_app/Tests/data* directory. This can be done in terminal by copying the address path of the directory and cd ^V in terminal to display the path


You can then run tests from within PyCharm using
````shell
$ python -m pytest
```` 


 
