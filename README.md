#  GraphServe

A backend service built with **FastAPI** and **Neo4j** graph database for modeling and managing relationships between entities in the eCar system.

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** – Modern, high-performance web framework for building APIs with Python.
- **Neo4j** – Native graph database for modeling highly connected data.
- **Docker** – Containerized development environment (Neo4j runs in Docker).
- **Neomodel** - OGM (Object Graph Mapper) for the Neo4j graph database.
- **Angular** - JavaScript framework for making intuitive mangement frontend app.

## 🚀 Running the Application
First, clone the repository to your local machine:
`git clone <repository-url>`
### 1. Backend (FastAPI,Neo4j,Docker)
1.  Navigate to the root directory of the cloned repository where the `docker-compose.yaml` file is located.
2.  Run the following command in your terminal:
    `docker-compose up --build`
### 2. Frontend (Angular)
1. Navigate to the frontend application's folder:
   `cd path/to/frontend-app`
2. Install the necessary dependencies:
   `npm install`
3. Start the development server:
   `ng serve`
