# 3rd party services connectors
Connect and operate 3rd party services from your application.

## Project configuration
```bash
./setup_project.sh
```
Will configure project for local run and development.

## Run project
```bash
./run_server.sh
```

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