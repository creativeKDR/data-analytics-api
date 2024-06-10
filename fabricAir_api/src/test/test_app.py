import os

import pytest
from fastapi.testclient import TestClient
from main import app
from src.test import test_config

client = TestClient(app)


def test_get_summary():
    response = client.get(f"fabricAir/api/summary/{test_config.fileId}")
    assert response.status_code == 200
    summary = response.json()
    assert "summary" in summary


def test_histogram_valid_columns():
    response = client.get(
        f"fabricAir/api/visualize/{test_config.fileId}?chart_type=Histogram&columns={test_config.columns[0]}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_histogram_invalid_column():
    response = client.get(
        f"fabricAir/api/visualize/{test_config.fileId}?chart_type=Histogram&columns={test_config.invalid_column[0]}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Column 'invalid_column' not found"}


def test_scatter_valid_columns():
    response = client.get(
        f"fabricAir/api/visualize/{test_config.fileId}?chart_type=Scatter&columns={test_config.columns[0]}&columns={test_config.columns[1]}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_scatter_missing_column():
    response = client.get(
        f"fabricAir/api/visualize/{test_config.fileId}?chart_type=Scatter&columns={test_config.columns[0]}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Scatter plot requires exactly 2 columns"}


def test_upload_file():
    sample_file_path = os.path.join(os.path.dirname(__file__), "sample_csv/ecommerce.csv")
    # Open the file in binary mode
    with open(sample_file_path, "rb") as file:
        response = client.post("fabricAir/api/upload/", files={"fileData": ("ecommerce.csv", file, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"filename": "test.csv", "columns": test_config.columns}


if __name__ == "__main__":
    pytest.main()
