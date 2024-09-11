# bnb
[![codecov](https://codecov.io/gh/amakarudze/bnb/graph/badge.svg?token=u2ZBx7VojS)](https://codecov.io/gh/amakarudze/bnb)

Bed and Breakfast (BnB) Reservation System

This app is developed as a fulfillment to Blekinge Institute of Technology PA2550 Seminar Series in Software
Engineering course project for Group 1.

## Group members
Anna Makarudze
Payel
Jammitri
Meenakshi
Sanjeeb

## Installation and Set Up
To set up this project in your local environment do the following steps (this guideline assumes you have Git and Python
already installed and set up on your computer):

1. Fork this repository to your own account.

2. Copy the link to the repository and type in your shell/command line:

```git clone git@github.com:your_repository/bnb.git```

3. Navigate into bnb by typing the following command:

```cd bnb```

4. Run the following command to create a virtual environment. The Python version used to create this project is Python
3.12

```python3 -m venv venv```

5. Activate the virtual environment by running the following command on Mac OSX and Linux

```source venv/bin/activate```

or on Windows

```venv\Scripts\activate```

6. Install the required packages by running the following command:

```pip install -r requirements.txt```

7. Run migrations to create a local copy of the database:

```python manage.py migrate```

*Note:*- This project uses SQLite database so there is no need to install any database software or plugins.

## Configuring your local environment
For security reasons, some important and secret configuration values have been removed from the project `settings.py`
file. For your project to work properly, create an empty file in the root of your project called `.env`. Copy the
contents of `sample_env_file` into your `.env` file and write some values for everything that has a `blank` or `""` value.

### Setting up pre-commit
The project uses `ruff` as a `linter` and `format`. It also uses `pre-commit` to ensure that code is linted and
formatted properly before being committed. Both ruff and `pre-commit` are already in the `requirements.txt` file.
However, you will need to run the following command to ensure that all files are properly linted and formatted before
being pushed to GitHub:

```pre-commit install```

## Testing your setup
With your virtual environment activated, run the following commands:

To run tests:

```pytest``` or ```coverage run pytest```

To see if your development server is set up correctly:

```python manage.py runserver```

and open this URL in the browser to see the homepage ```http://127.0.0.1:8000```.

## Contributing to this project
To contribute to this project, create a branch in your local development environment. After you are finished with your
changes, push the changes to your fork and make a pull request to the main repo
`git@github.com:amakarudze/bnb.git` where you forked this project.
