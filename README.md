# Poc Prefect

- Docs: https://docs.prefect.io

## Requirements

- Python 3.6.x
- Docker

## Local Setup

**Project dependencies**

```bash
pipenv install
```

**Prefect viz module**

- [Tool - installing-optional-dependencies](shttps://docs.prefect.io/core/getting_started/install.html#installing-optional-dependencies)

Tools for visualizing Prefect flows.

```bash
pipenv run pip install 'prefect[viz]'
```

### Localhost development

**Init prefect local backend server**

```bash
pipenv run prefect backend server
```

**Prefect UI init**

```bash
pipenv run prefect server start
```

**Create a project**

```bash
pipenv run prefect create project "Tests"
```

**Registering a task**

```bash
pipenv run prefect register -p ./etl/funcional_flow.py --project "Tests"
```

## Setup Universal deployment

- [Docs - universal-deploy](https://cloud.prefect.io/tutorial/Universal-Deploy#universal-deploy)

**Init prefect universal backend cloud**

```bash
pipenv run prefect backend cloud
```

**Autenticate**

```bash
pipenv run prefect auth login --key <key>
```

**Create a project**

```bash
pipenv run prefect create project <projct-name>
```

**Register the flow**

As an example, using the flow `funcional_flow.py` to create in https://cloud.prefect.io/

```bash
pipenv run prefect register -p ./etl/funcional_flow.py --project <project-name>
```

**Start the agent**

```bash
pipenv run prefect agent <agent-name> start
```
