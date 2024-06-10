# Data Analytics API

## Description
This project is a FastAPI application that provides endpoints for uploading CSV files, generating summary statistics, transforming data, and creating visualizations.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Uploading a File](#uploading-a-file)
  - [Getting Summary Statistics](#getting-summary-statistics)
  - [Transforming Data](#transforming-data)
  - [Visualizing Data](#visualizing-data)
- [Endpoints](#endpoints)
- [Tests](#tests)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/creativeKDR/data-analytics-api.git
    cd data-analytics-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. And to run the project use following command or directly run `main.py`
    ```bash
    uvicorn fabricAir_api.main:app --reload
    ```

## Usage

You can also refer API documents by hitting this endpoint `/redoc`

Example:
```bash
curl -X POST "http://127.0.0.1:8000/redoc

```

### Uploading a File
To upload a file, send a POST request to `fabricAir/api/upload/` with a CSV file.

Example:
```bash
curl -X POST "http://127.0.0.1:8000/fabricAir/api/upload/" -F "fileData=@sample.csv"

```
### Get Summary of File
To upload a file, send a POST request to `fabricAir/api/summary/<fileId>` with a CSV file.

Example:
```bash
curl -X GET "http://127.0.0.1:8000/fabricAir/api/summary/<fileId>" 
```

### Transform a File
To upload a file, send a POST request to `fabricAir/api/transform/<fileId>` with a CSV file.

Example:
```bash
curl -X POST "http://127.0.0.1:8000/fabricAir/api/transform/<fileId>/" -Q "transformationPayload"
```

### Visualize a File
To upload a file, send a POST request to `fabricAir/api/visualize/<fileId>` with a CSV file.

Example:
```bash
curl -X GET "http://127.0.0.1:8000/fabricAir/api/visualize/<fileId>/" -Q "chart_type=Histogram&Columns=Quantity"
```

## Endpoints

- POST /fabricAir/api/upload/ : Upload a CSV file.
- GET /fabricAir/api/summary/<file_id> : Get summary statistics of the uploaded CSV.
- POST /fabricAir/api/transform/<file_id> : Transform data (e.g., normalize specified columns).
- GET /fabricAir/api/visualize/<file_id> : Generate a histogram or scatter plot for specified columns.


## Tests

To run the tests, use `pytest`:

Example:
```bash
pytest test_main.py
```

## Thanks