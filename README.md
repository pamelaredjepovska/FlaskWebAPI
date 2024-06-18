# FlaskWebAPI

## Description
FlaskWebAPI is a straightforward Flask-based API connected to a PostgreSQL database, designed to be easily containerized using Docker.

## Setup

### Environment Variables
To configure FlaskWebAPI, follow these steps:
1. Duplicate the `example.env` file as `.env`.
2. Populate the `.env` file with your specific environment variable values. Default values will be used if not provided.

All database configuration settings are managed within the `.env` file.

## Running the App Locally

You can run FlaskWebAPI in your local environment in two ways:

### 1. Using Docker Container

Running FlaskWebAPI in a Docker container is the recommended approach, aligning with production deployment standards:

#### Setup Steps:
1. Set `DB_HOST=docker-db` in the `.env` file.
2. Define `TEST_HOST=0.0.0.0` and choose `TEST_PORT` for the app's listening port.
3. Launch the Flask app in debug mode:
   - Execute `docker compose up`.
   - For rebuilding images and removing orphaned containers: `docker compose up --build --remove-orphans`.
   - Docker will build two images and start containers named `docker-db` (Postgres instance) and `docker-webapi` (the app) respectively.
   - Access the app at `localhost:TEST_PORT`.

#### Container Manipulation:
- The Postgres database initializes with default data (refer to the [sql](sql) folder).
- Persistent database data is stored in `postgres_data` (new data persists across app restarts).
- To reset the database, delete `postgres_data`: `sudo rm -rf postgres_data` and rerun `docker compose up --build`.
- Inspect the `docker-db` container: `docker exec -it docker-db psql -d mydatabase -U user`.

### 2. Running Directly in Local Environment

For local development outside Docker:

#### Steps:
1. Ensure Python 3.8+ is installed.
2. Create and activate a virtual environment.
3. Use the existing `.env` file with modified `DB_HOST` (`x.x.x.x` for remote database) and `TEST_HOST=localhost`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Start the app: `python3 run.py`.

## Swagger UI
Explore the API documentation via Swagger UI at `http://localhost:5000/swagger-ui`.

## Logging
Log files are located in `logs/flaskwebapi.log`.

## Error Handling
Custom error handling ensures consistent error responses.

## Contributing
Contributions such as issues or pull requests are welcome.
