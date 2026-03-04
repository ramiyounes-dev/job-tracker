# jobAppTrackerApi
Job Application Tracker API

It is a RESTful API that allows users to track their job applications. Users can create, read, update, and delete job application records, making it easier to manage their job search process.
## Features
- Create, read, update, and delete job application records
- User authentication and authorization
- Filter and search job applications
- Pagination for job application records
- Error handling and validation
## Tech Stack
- Python 3.12+: programming language for building the API
- FastAPI: web framework for building the API
- PostgreSQL: database for storing job application data
- SQLAlchemy: ORM for database interactions
- Pydantic: data validation and serialization
- JWT: JSON Web Tokens for user authentication and authorization
- Docker + Docker Compose: Containerization for easy deployment
- Railway: Cloud platform for hosting the API
## Getting Started
### Prerequisites
- Docker installed (handles everything, no need for other installations)
### Installation
using docker-compose

1. Clone the repository:
```bash
    git clone https://github.com/ramiyounes-dev/job-tracker.git
```
2. Navigate to the project directory:
```bash
    cd job-tracker
```
3. Set up environment variables (see .env.example for reference):
```bash
    cp .env.example .env
```
4. Running with Docker:
```bash
    docker-compose up
``` 
5. The API will be available at `http://localhost:8000`
6. You can access the API documentation at `http://localhost:8000/docs`
## Environment Variables
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for JWT access tokens in minutes
- `DATABASE_URL`: Connection string for the PostgreSQL database (e.g., `postgres://user:password@localhost:5432/jobapptracker`)
- `SECRET_KEY`: Secret key for signing JWT tokens
## API Documentation
coming soon
## Deployment           
Coming soon