# GPL Backend

This project is the backend for the GPL application

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Docker](#docker)
- [API Endpoints](#api-endpoints)

## Installation

To install the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GPL-Backend.git
    ```
2. Navigate to the project directory:
    ```bash
     cd GPL-Backend
        ```
    3. Install the dependencies using Poetry:
        ```bash
        poetry install
        ```

    ## Usage

    To start the server, run:
    ```bash
    poetry run uvicorn main:app --reload
    ```

    The server will start on `http://localhost:8000`.

    ## Docker

    To build and run the project using Docker, follow these steps:

    1. Build the Docker image:
        ```bash
        DOCKER_BUILDKIT=1 docker build -t gpl-backend .
        ```
    2. Run the Docker container:
        ```bash
        docker run -p 8000:8000 gpl-backend
        ```

    The server will start on `http://localhost:8000`.

    ## API Endpoints

    The API documentation is available at `http://localhost:8000/docs`. You can explore the available endpoints and test them directly from the interactive documentation interface.
    ```
3. Install the dependencies using Poetry:
    ```bash
    poetry install
    ```

## Usage

To start the server, run: