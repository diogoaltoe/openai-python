# OpenAI Python

OpenAI GPT integration project using Python.


## Features

This project provide the below features:
- `OpenAI Chat`
  - "Given a list of messages comprising a conversation, the model will return a response."


## Installation

Download the project using the below GIT command:
```
$ git clone https://github.com/diogoaltoe/openai-python.git
```

### Activate the virtual environment (venv)

Using the Terminal, execute the command below.

On Windows:
```
.venv\Scripts\activate
```

On Unix or MacOS:
```
source .venv/bin/activate
```

### Install project dependencies

Use pip to install the project dependencies listed in the `requirements.txt` file:
```
pip install -r requirements.txt
```

### Publish static assets

To publish the static assets, execute the command below:
```
python manage.py collectstatic 
```


## Usage

Run the project using the command below:
```
python manage.py runserver
```

Then access the application, clicking in the link: http://127.0.0.1:8000/


## Libraries

- [Django](https://www.djangoproject.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [OpenAI Python API library](https://pypi.org/project/openai/)

For more all the libraries, check `requirements.txt` file.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
