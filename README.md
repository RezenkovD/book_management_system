# Book Management System

This is a FastAPI application with Alembic for database migrations.

## Setup and Run the Application

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RezenkovD/book_management_system.git
   cd book_management_system
   ```

2. Create a virtual environment and activate it:

   ```bash
   sudo apt-get install -y python3.11-venv
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   ```env
   export PYTHONPATH=$PWD/app
   export APP_HOST=127.0.0.1
   export APP_PORT=8000
   export SQLALCHEMY_DATABASE_URI="sqlite:///./books.db"
   ```

### Database Migrations

1. Initialize Alembic (only if not already done):

   ```bash
   alembic init alembic
   ```

2. Edit `alembic.ini` to configure your database connection string.

3. Generate a new migration script:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. Apply the migrations:

   ```bash
   alembic upgrade head
   ```

### Running the Application

To run the application, use the following command:

```bash
uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload
