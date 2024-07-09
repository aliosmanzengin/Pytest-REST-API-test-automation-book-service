# Pytest-REST-API-test-automation-book-service



## Setup Instructions

### Prerequisites

- Python 3.8
- Docker (for running the API) 

### Setup Virtual Environment

1. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:

    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

### Install Dependencies

1. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Running Tests

1. Ensure your API is running in Docker.

2. Run the tests:

    ```sh
    pytest --alluredir=allure-results
    ```

### Generating Allure Report

1. Generate and view the Allure report:

    ```sh
    allure serve reports
    ```
