
# ALX Backend Python - User Data Streaming

## Project Overview

This project demonstrates how to:

- Set up a MySQL database named `ALX_prodev`.
- Create a `user_data` table with the following fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populate the table with sample user data from a CSV file.
- Implement a Python generator that streams rows from the SQL database one by one, efficiently handling data retrieval.

---

## Files

- `seed.py`:  
  Connects to MySQL, creates the database and table if they don't exist, and inserts sample data from `data.csv`.

- `user_data.csv`:  
  Sample CSV data used to populate the `user_data` table.

- `1-database_generator.py`:  
  Contains the `stream_users()` generator function that yields user rows from the database one at a time.

- `1-main.py`:  
  Test script that imports and uses the generator to print user data row-by-row.

---

## Setup Instructions

1. **Install MySQL server** and ensure it is running.

2. **Install Python dependencies**:

   ```bash
   pip install mysql-connector-python
Prepare your CSV data (user_data.csv), ensure it has these columns:

pgsql
Copy
Edit
name,email,age
Run seed.py to set up the database and populate it:

bash
Copy
Edit
python seed.py
Run 1-main.py to test the generator that streams rows:

bash
Copy
Edit
python 1-main.py
How It Works
seed.py sets up the database and loads user data.

1-database_generator.py defines stream_users(), a generator function that:

Connects to the MySQL database.

Executes a SELECT * FROM user_data query.

Yields one row at a time as a dictionary.

1-main.py consumes this generator and prints each user row.

Example Output
python
Copy
Edit
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
Notes
The generator approach is memory-efficient for large datasets.

Make sure your MySQL user credentials in the scripts match your local setup.

user_id is stored as a UUID string.