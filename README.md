# FastAPI CRUD App with MySQL
Fast API Python CRUD

# 1. Clone the Repository
git clone https://github.com/jpshaw111/pythonfastapicrud.git
cd pythonfastapicrud
# 2. Create and Activate Virtual Environment
python -m venv env
env\Scripts\activate

# 3. Set Up MySQL Database

CREATE DATABASE fastapi_db;

USE fastapi_db;

CREATE TABLE items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  description TEXT
);

# 4. Update Database Connection
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/fastapi_db"

If you're using a password for MySQL, replace @ with :your_password@

# 5. Run the App
uvicorn main:app --reload



