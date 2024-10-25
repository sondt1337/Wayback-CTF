
# CTF Scoreboard System

This project is a Flask-based microservices application designed to display CTF (Capture the Flag) scoreboards. It uses Docker and Kubernetes for deployment, ensuring scalability, ease of management, and portability.

## Table of Contents

- [CTF Scoreboard System](#ctf-scoreboard-system)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Setup and Installation](#setup-and-installation)
  - [Running the Application](#running-the-application)
    - [1. Run Flask Application Locally (Without Docker)](#1-run-flask-application-locally-without-docker)
    - [2. Build and Run with Docker Compose](#2-build-and-run-with-docker-compose)
    - [Dockerfile Breakdown](#dockerfile-breakdown)
  - [Kubernetes Deployment](#kubernetes-deployment)
    - [1. Apply Kubernetes Configurations](#1-apply-kubernetes-configurations)
    - [Kubernetes Files Overview](#kubernetes-files-overview)
  - [Accessing the Application](#accessing-the-application)
  - [Monitoring and Scaling](#monitoring-and-scaling)
    - [View Logs](#view-logs)
    - [Scaling with Horizontal Pod Autoscaler](#scaling-with-horizontal-pod-autoscaler)
    - [Manually Scaling Pods](#manually-scaling-pods)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

---

## Project Structure

```
F:\WAYBACK-CTFD
│   docker-compose.yml        # Docker Compose file to orchestrate multiple containers (Flask app and database) for local development
│   echo.txt                  # Example text file (purpose may vary)
│   README.md                 # Project documentation with setup, usage, and deployment instructions
│
├───app                       # Main application folder containing Flask code and configuration
│   │   app.py                # Main Flask application file with route definitions and logic
│   │   Dockerfile            # Dockerfile to build the Flask application container image
│   │   requirements.txt      # List of Python dependencies required for the Flask app
│   │
│   ├───instance              # Flask instance folder to store runtime files and database (if SQLite is used)
│   │       database.db       # SQLite database file (if using SQLite for development)
│   │
│   ├───static                # Folder for static assets (CSS, JavaScript, images, etc.)
│   │
│   └───templates             # HTML templates for rendering pages in Flask
│           all_scoreboards.html  # Template to display all available scoreboards
│           base.html             # Base template for consistent layout and styling across pages
│           index.html            # Homepage template for the CTF Scoreboard System
│           scoreboard.html       # Template to display individual scoreboard details
│
└───k8s                        # Kubernetes configuration folder for deploying microservices
        db-deployment.yaml       # Deployment configuration for the database service
        db-service.yaml          # Service configuration for database (ClusterIP or internal access only)
        flask_app-deployment.yaml # Deployment configuration for the Flask application
        flask_app-hpa.yaml        # Horizontal Pod Autoscaler to auto-scale Flask pods based on CPU usage
        flask_app-service.yaml    # LoadBalancer service to expose Flask app externally
```

---

## Requirements

- **Python 3.9+**: To run the application locally without Docker.
- **Docker**: To containerize the application.
- **Docker Compose**: For local multi-container setup.
- **Kubernetes**: For orchestrating and deploying microservices.
- **kubectl**: CLI tool to manage Kubernetes clusters.

---

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sondt1337/wayback-ctf.git
   cd wayback-ctf
   ```

2. **Install Python dependencies**:
   If you are running locally without Docker, install the dependencies manually:
   ```bash
   pip install -r app/requirements.txt
   ```

---

## Running the Application

### 1. Run Flask Application Locally (Without Docker)

To run the application without Docker, follow these steps:

1. **Navigate to the `app` directory**:
   ```bash
   cd app
   ```

2. **Set environment variables for Flask**:
   - **On Linux/macOS**:
     ```bash
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```

   - **On Windows (Command Prompt)**:
     ```cmd
     set FLASK_APP=app.py
     set FLASK_ENV=development
     ```

   - **On Windows (PowerShell)**:
     ```powershell
     $env:FLASK_APP = "app.py"
     $env:FLASK_ENV = "development"
     ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

### 2. Build and Run with Docker Compose

To run the application locally with Docker Compose:

```bash
docker-compose up --build
```

This will start both the Flask app and the SQLite database in Docker containers, exposing the Flask app on port `5000`.

### Dockerfile Breakdown

The `Dockerfile` in `app/` sets up the Flask environment:

```Dockerfile
# Use Python 3.9
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y     build-essential     && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy application files into the container
COPY . /app

# Install required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Run Flask startup command
CMD ["python", "app.py"]
```

---

## Kubernetes Deployment

This project includes Kubernetes configurations to deploy the application with microservices architecture. Each component (Flask app and database) is deployed as a separate service.

### 1. Apply Kubernetes Configurations

To deploy the services to a Kubernetes cluster, run the following:

```bash
kubectl apply -f k8s/
```

This command will deploy:
- `flask-app`: The Flask application with a LoadBalancer service for external access.
- `sqlite-db`: SQLite database as a ClusterIP service, accessible only within the cluster.
- `flask-app-hpa`: A Horizontal Pod Autoscaler to scale the Flask application based on CPU utilization.

### Kubernetes Files Overview

- **flask_app-deployment.yaml**: Defines the Flask app deployment with replicas.
- **flask_app-service.yaml**: Exposes the Flask app with a LoadBalancer.
- **db-deployment.yaml**: Defines the SQLite database deployment.
- **db-service.yaml**: Exposes the database as an internal ClusterIP service.
- **flask_app-hpa.yaml**: Configures auto-scaling for the Flask app.

---

## Accessing the Application

1. **Check Service Status**:
   ```bash
   kubectl get services
   ```

   Note the external IP of the `flask-app-service` LoadBalancer.

2. **Open the Application**:
   Visit the external IP in your browser:
   ```
   http://<EXTERNAL-IP>:80
   ```

---

## Monitoring and Scaling

### View Logs

To view logs of the Flask application, use:
```bash
kubectl logs -f <flask-app-pod-name>
```

### Scaling with Horizontal Pod Autoscaler

The Horizontal Pod Autoscaler (HPA) automatically scales the Flask application based on CPU utilization. You can check the HPA status with:
```bash
kubectl get hpa
```

### Manually Scaling Pods

You can manually scale the number of replicas with:
```bash
kubectl scale deployment flask-app --replicas=5
```

---

## Troubleshooting

1. **Database Connection Issues**:
   Ensure the database service (`sqlite-db`) is running correctly and accessible by checking the pod and service status.

2. **Application Access**:
   If the LoadBalancer IP is not accessible, confirm that your Kubernetes cluster supports LoadBalancer services, or use `kubectl port-forward` to access the service locally.

---

## License

This project is licensed under the MIT License.

---

This `README.md` should give clear instructions for setting up, running, and scaling the application using Docker and Kubernetes.
