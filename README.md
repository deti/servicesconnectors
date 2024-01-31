# 3rd party services connectors
Connect and operate 3rd party services from your application.

## Project layout
```bash
├── src                     # sources
│   ├── alembic             # Database migrations
│   ├── connections         
│   │   ├── api             # API
│   │   │   └── ...         # API implemntation
│   │   ├── connectors      # Connetors
│   │   │   └── ...         # Connectors implementations
│   │   ├── models          # Database models for connections
│   │   ├── runner          # Connectors runner
│   │   └── storage         # Storage abstraction
│   ├── database            # Database confiugration
│   └── main                # Application entry point
├── tests                   # Automated tests
├── lint.sh                 # Lint project script
├── requirements*           # Requirements files for pip-tools
├── run_server.sh           # Run application script
├── setup_project.sh        # Project setup script
├── test.sh                 # Run tests script
├── test_api.http           # API test requests
└── update_dependencies.sh  # Update dependencies script


```

## Project configuration
```bash
./setup_project.sh
```
Will configure project for local run and development.

## Run project
```bash
./run_server.sh
```

## API documentation
API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
when applicaiton is running.

## Run tests
```bash
./test.sh
```

## Lint project
To keep project code style consistent, run:

```bash
./lint.sh
```

This will run [black](https://github.com/psf/black),
[mypy](https://github.com/python/mypy),
[isort](https://github.com/PyCQA/isort),
[flake8](https://github.com/PyCQA/flake8).
and [pylint](https://github.com/pylint-dev/pylint) on the project.

## Update dependencies
Dependencies are managed by [pip-tools](https://github.com/jazzband/pip-tools)
Edit `requirements.in`  and `requirements-dev.in` files and run:

```bash
./update_dependencies.sh
```

## Generate migration
Generate migration file with:
```bash
 python -m alembic revision --autogenerate -m "Migration message"
```

## Apply migrations
Applying migratins is part of `run_server.sh` script, but you can also run it manually:
```bash
 python -m alembic upgrade head
```