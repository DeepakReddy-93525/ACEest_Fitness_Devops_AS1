# ACEest Fitness & Gym - DevOps CI/CD Assignment

This project implements a robust CI/CD pipeline for the ACEest Fitness & Gym Flask web application, providing automated deployment workflows for code integrity, environmental consistency, and rapid delivery.

## Features

- **Flask Web Application**: Core fitness management app with program selection, client profiles, and workout/diet plans.
- **Unit Testing**: Comprehensive Pytest suite for validating application logic.
- **Containerization**: Dockerized application for consistent deployment.
- **CI/CD Pipeline**: GitHub Actions workflow for automated build, lint, test, and Docker image creation.
- **Jenkins Integration**: Configured for secondary build validation from GitHub.

## Local Setup and Execution

### Prerequisites
- Python 3.9+
- Docker (for containerization)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone <your-github-repo-url>
   cd aceest-fitness
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser to `http://localhost:5000`

## Running Tests Manually

Execute the test suite using pytest:
```bash
pytest
```

This will run all unit tests validating the Flask application's endpoints and logic.

## Docker Build and Run

Build the Docker image:
```bash
docker build -t aceest-app .
```

Run the container:
```bash
docker run -p 5000:5000 aceest-app
```

## GitHub Actions Workflow

The CI/CD pipeline is defined in `.github/workflows/main.yml` and triggers on every push or pull request to the main branch. It performs:

1. **Build & Lint**: Sets up Python, installs dependencies, and runs flake8 linting.
2. **Automated Testing**: Executes the Pytest suite inside the environment.
3. **Docker Image Assembly**: Builds the Docker container to ensure portability.

## Jenkins Integration

To set up Jenkins for the BUILD phase:

1. Install Jenkins and required plugins (Git, Pipeline).
2. Create a new Freestyle project.
3. Configure source code management to pull from your GitHub repository.
4. Add build steps:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 app.py &
   sleep 5
   curl http://localhost:5000 || exit 1
   ```
5. Set up webhook in GitHub to trigger Jenkins on push.
6. Configure SCM polling with schedule: `H/5 * * * *` (polls every 5 minutes)

The Jenkins BUILD serves as a secondary validation layer, ensuring the code compiles and integrates correctly in a controlled environment. The SCM polling provides an additional trigger mechanism beyond webhooks, checking for repository changes every 5 minutes.

## Project Structure

```
├── app.py                 # Main Flask application
├── test_app.py            # Unit tests
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── templates/             # HTML templates
│   ├── home.html
│   ├── client_form.html
│   ├── client.html
│   └── program.html
├── .github/workflows/     # GitHub Actions
│   └── main.yml
└── README.md              # This file
```
