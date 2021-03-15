# autorack-back

[![badge-ci]][badge-ci-link]
[![badge-cq-badge]][badge-cq-link]
[![badge-coverage-badge]][badge-coverage-link]

Backend of AutoRack.

## Environment Variables

### `FLASK_APP`

Required if starting the app via Flask CLI. Optional otherwise.

Indicate the location of the flask app.

### `FLASK_ENV`

Required if starting the app via Flask CLI. Optional otherwise.

Indicate if the current environment is either in `development` or `production`.

This changes how Flask behaves.

### `FIREBASE_ACCOUNT_KEY`

Required.

Content of the credential file `serviceAccountKey.json` obtained from Firebase.

- This can be obtained from `Firebase Project Settings > Service Accounts > Generate Private Key`.

### `CI`

Optional.

Indicate if the app is running in CI. Set this to `1` to indicate that the app is running in CI.

CI-specific behavior will **not** be enabled if this is not set to `1`.

## Prerequisites

- Install Python **3.9**.

  - It is recommended to use the installer provided by Python.
    
  - [Click to navigate to the Python download page](https://www.python.org/downloads/)

- Install PostgreSQL **v13**.

  - It is recommended to use the installer provided by PostgreSQL.
    
  - Check the [PostgreSQL installation guide](#postgresql-installation-guide) for the complete steps.
    
  - [Click to navigate to the download page](https://www.postgresql.org/download/)

## Getting Started

### Start the app via Flask CLI

1. Run `pip -r requirements.txt` for installing all required dependencies.

    - If the app is cloned for development, run `pip -r requirements-dev.txt` instead.

    - `requirements-dev.txt` contains additional dependencies for development only.

2. Set the environment variables for `FLASK_APP` to `run.py`; `FLASK_ENV` to the intended value.

    - For `FLASK_ENV`, set it to `development` if the code is cloned for development. Doing so will enable Flask debug
      mode, which will hot-reload the code.

3. `flask db upgrade` & `flask db migrate` to update the database.

4. `flask run` to start the app.

### Start the app via Python

Simply run `run.py`:

```bash
py run.py
```

To configure the environment, set the argument `debug` when starting the app.

For debug environment:
```python
from app import create_app

create_app().run(debug=True)
```

For production environment:
```python
from app import create_app

create_app().run(debug=False)
```

Note that if either `.env` or `.flaskenv` is present, variables in these files will be loaded.

- Values in `.flaskenv` overrides the values in `.env`.

- `debug` in the function call `run()` above overrides the value in both files.

## Development Notes

- **Create tests before actually implementing a feature.**
  
  Code quality check will fail if the coverage is not > 80%.
  
- **Type hint all things that can be type-hinted.**
  
  IDE will find some data type mismatch if any, to prevent some weird bugs during development.
  
- **Make sure the commit message is concise.**
  
  A good practice is to make sure it does not go over 50 characters.
  
- **Make sure the commit message starts with a verb.**
  
  This helps the commit message to be more readable.
  
- **Don't change a lot in a single commit.**
  
  This helps narrow down the problem if needed. This also helps the code reviewer to review the code.
  
    - An exception is when a new interface or architecture is introduced. However, this rarely happens.

- **Run `precommit.sh` before committing the code.**
  
  Doing so ensure the code for every code can run without any bugs.
  
### New Implementations

- Whenever a new file is created, have a module level field `__all__` stating what is exported from the file.

- Whenever a new data model is created, 
  run `flask db migrate` and `flask db upgrade` before running the app.

- To obey the case convention of TypeScript, **arguments for web requests should be named in camelCase**.

### Import 

If import from the parent of the current directory, import it from `app`.

For example, importing response class from routes:
```python
from app.response import ResponseBase
```

- **DO NOT** import like this: `from ..response import ResponseBase`

If import from the same directory, import it relatively.

For example, importing the response base class to the main response class file (`app/response/main.py`):
```python
from .base import ResponseBase
```

If import a type simply for type-hinting and such import causes circular import, add a wrapping if statement:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.response import ResponseBase
```

> This means that `ResponseBase` is only imported for type checking purposes.
> `ResponseBase` is used only when performing type checking, not when the application is running.
  
### Adding an endpoint

This is only a rough guide of how to add an endpoint.

1. Add tests in `tests`.

    - Adding one or two tests for success behavior suffice.
      More tests are expected to be added after the development, 
      if the endpoint development is urgent.

2. Add a view function in the corresponding file in `app/routes`.

3. Create a Response class that inherits from `app.response.base.ResponseBase` and do any necessary modifications.

4. In the view function created in step 2, return the response class created in step 3.

[badge-ci]: https://github.com/CS506-Oversight/autorack-back/workflows/CI/badge.svg

[badge-ci-link]: https://github.com/CS506-Oversight/autorack-back/actions?query=CI

[badge-coverage-badge]: https://app.codacy.com/project/badge/Coverage/b413dc35cd3341bd9e69d20af72fcd0e

[badge-coverage-link]: https://www.codacy.com/gh/CS506-Oversight/autorack-back/dashboard

[badge-cq-badge]: https://app.codacy.com/project/badge/Grade/b413dc35cd3341bd9e69d20af72fcd0e

[badge-cq-link]: https://www.codacy.com/gh/CS506-Oversight/autorack-back/dashboard

## PostgreSQL Installation Guide 

[Click to navigate to the download page](https://www.postgresql.org/download/)

Note that we are using **v13**.

1. Download and execute the installer for PostgreSQL.

    - Uncheck `Stack Builder` for the installation components because we are unlikely to use it.
    
    - Remember your password created during installation.

2. Add the absolute path of the `bin` directory of your installation into the `PATH` environment variables.

3. Type `psql --version` to verify that step 1 and step 2 has done correctly.

    - The expected output will be something like `psql (PostgreSQL) 13.2`.

4. Type `psql -U postgres` in the terminal. Use the password created in step 1 to login.

    - You should see something like `postgres=#`. Seeing this means that you've logged in.

5. Type `create database mydb;` to create a database.

    - `mydb` can be substituted to any name you want.
    
    - Note the colon `;` at the end. Don't forget that.

6. Type `\c mydb` to connect to the database.

7. Type `\d` to view available tables (relations).

8. Type `table <TABLE_NAME>;` to view the content of the table.
    
    - Note the colon `;` at the end. Don't forget that.
    
9. Type `\q` to exit.
