## About The Project

This is a simple FastAPI project template that provides a foundation for building RESTful APIs with integrated database migration(Alembic), testing(pytest), and code formatting(black & isort). It includes REST endpoints for managing two models: "user" and "item."


### Key Features
  - [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python.
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/): A database migration tool for managing changes to your database schema.
  - [pytest](https://docs.pytest.org/en/7.4.x/): A testing framework for writing and running unit tests.
  - [pre-commit](https://pre-commit.com/): A tool that helps you manage and maintain your code quality by running checks and formatting before committing your code.


## Project Structure

```
project/
│
├── app/
│ ├── init.py
│ ├── main.py # FastAPI application
| ├── pre_start.py
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py # User model definition
│ │ └── item.py # Item model definition
│ │
│ ├── db/
│ │ ├── init.py
| | ├── init_db.py # Tables creation using alembic.
│ │ ├── base.py # SQLAlchemy base model
│ │ └── session.py # Database session handling
│ │
│ ├── api/
│ ├── init.py
│ ├── user.py # User API endpoints
│ └── item.py # Item API endpoints
│ |
│ ├── crud/
│ │ ├── init.py
| | ├── item.py
| | ├── user.py
│ │ └── base.py
│ |
├── tests/
│ ├── init.py
│ ├── test_user.py # Unit tests for the User model and API
│ └── test_item.py # Unit tests for the Item model and API
│
├── .pre-commit-config.yaml # Pre-commit configuration file
├── .env.example # Environment variables template
└── README.md # Project documentation
```


### Installation
    
1.  #### Create a Virtual Environment:
    
    Change your working directory to the newly created project folder:
        
    ```
    cd <project_directory>
    ``` 
    
    Inside your project directory, you can use `pipenv` to set up a virtual environment and install the project dependencies. If you haven't already installed `pipenv`, you can do so with the following command:
        
    ```
    pip install pipenv
    ``` 
    After installing `pipenv`, create and activate a virtual environment:
	```
	pipenv install
	```
   
    Activate the enviroment:
	   ```
	pipenv shell 
	   ```
	   This will create a virtual environment and install all the project dependencies within it. You'll be working within this virtual environment for the rest of your project.
#### Setting up databases:

1.  Create a database of your choice, set username and password for postgres.
    
2.  Add your DB credentials in the environment file (`.env`):
    ```
    DATABASE_URL= "postgresql://postgres:postgres@localhost:5432/fastapi"
	TESTING=false
    ```
3.  Create another database for testing purposes.
4.  Modify SQLALCHEMY_TEST_DATABASE_URI in .env with the test database name. Other properties like username, password would be the same as step 2.
    	```
    	TEST_DATABASE_URL= postgresql://<USERNAME>:<PASSWORD>@<SERVER>:<PORT>/<TEST_DB_NAME> 
    	``` 


#### Starting the Server
`uvicorn app.main:app --port 8080 --reload` 

else you can use boot.sh file at root to run other environments.
#### Commiting your changes with Git Hooks

1. Once you are ready to commit your changes, install [pre-commit](https://pre-commit.com/) and run

	```
	pre-commit  install
	```

#### Testing

As we have already created a test database so we do not need to create the database again.

-   Run the following command to run all the test cases:
`python -m pytest` 

-   Run the following command to run test cases for one module i.e., 'items':
`pytest tests/api/api_v1/test_items.py` 

-   Run the following command to run a specific test case like 'create an item':
`pytest tests/api/api_v1/test_items.py::test_create_item` 

#### Applying Automigration using Alembic

To apply automigration using Alembic, follow these steps:

1.  Create a new migration script:
`alembic revision --autogenerate -m "Your migration message"` 


2.  Apply the migration to update the database schema:
`alembic upgrade head` 

You can repeat these steps whenever you make changes to your database models. Alembic will generate migration scripts automatically based on the changes in your SQLAlchemy models.

### Documentation

The API documentation can be accessed at http://localhost:8000/docs when the FastAPI application is running.

#### CircleCI Setup:
circleCi is already integrated with Docker Images 
1. `cimg/python:3.10.12`
2. `cimg/postgres:14.0`

Connect your Github or Bitbucket Repo with the circleCi and there you are !! 

