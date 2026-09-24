# Python MySQL Development with `uv` and `python-decouple`

This document details the step-by-step process of setting up a modern, ultra-fast Python development environment using **`uv`**, managing secrets securely using **`python-decouple`**, and executing parameterized MySQL queries via **`mysql-connector-python`**.

---

## 1. Project Initialization & Virtual Environment Setup (`uv`)

**`uv`** is an extremely fast Python package and project manager written in Rust.

### Step 1.1: Initialize Project Directory
Navigate to your working directory and initialize a new Python project:

```bash
uv init 
```

### Step 1.2: Create and Activate Virtual Environment
Create a virtual environment using `uv`:

```bash
uv venv
```

Activate the environment based on your operating system:

* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

---

## 2. Dependency Management

Add the required packages to your environment:

```bash
uv add mysql-connector-python python-decouple
```

* **`mysql-connector-python`**: Official Oracle MySQL driver for executing queries from Python.
* **`python-decouple`**: Library used to separate configuration settings/credentials from source code using a `.env` file.

---

## 3. Environment Configuration (`.env`)

To prevent hardcoding sensitive credentials inside Python source code, create a `.env` file in the project root directory:

### `.env` File
```ini
host=localhost
database=wtm_backend_dev
port=3306
user=birhane001
password=password001
```

> **Security Note:** Add `.env` to your `.gitignore` file to ensure database passwords are never committed to version control.

---

## 4. Source Code & Logic Walkthrough

Below is your script attempting to read configuration variables, list databases, switch context, perform a parameterized `INSERT`, commit the transaction, and attempt to fetch rows.

### `main.py`
```python
from decouple import config
from mysql import connector

# 1. Establish database connection using decoupled parameters
connection = connector.connect(
    host=config("host"),
    database=config("database"),
    port=config("port", cast=int),
    user=config("user"),
    password=config("password"),
)

if connection.is_connected():
    print(
        "Congratulations! You have successfully connected to MySQL server, wtm_backend_dev database"
    )

    cursor = connection.cursor()

    # 2. Inspect available databases
    cursor.execute("SHOW DATABASES;")
    print("==== AVAILABLE DATABASES ====")
    for db in cursor.fetchall():
        print(f"- {db[0]}")

    # 3. Switch database context
    cursor.execute("USE wtm_backend_dev;")

    # 4. Prepared Parameterized Insert Query
    query = """
        INSERT INTO franco(username, password, city) VALUES (%s, %s, %s);
    """
    data = ("franco001", "idnotknow01", "Kampala")

    cursor.execute(query, data)

    # 5. Commit transaction to write changes to disk
    connection.commit()

    # NOTE: The loop below will trigger an InterfaceError!
    # for table in cursor.fetchall():
    #     print(f"{table}")

else:
    print("You did a wrong configuration, try again")
```

---

## 5. Script Analysis & Bug Analysis

### What Works Well:
1. **Security via `python-decouple`:** The `config()` functions pull database credentials cleanly without hardcoding.
2. **SQL Injection Prevention:** Using `%s` placeholders with `cursor.execute(query, data)` passes query string and parameter tuples separately to MySQL for proper sanitization.
3. **Transaction Persistence:** `connection.commit()` ensures the inserted data is permanently saved to the database.

### Critical Runtime Bug: `InterfaceError: No result set to fetch from`
In your loop:
```python
for table in cursor.fetchall():
    print(f"{table}")
```
Calling `cursor.fetchall()` directly after an `INSERT` command triggers a runtime exception because `INSERT` operations modify database state rather than returning a result set table.

### Recommended Correction
To retrieve and display updated data after an insertion, issue a `SELECT` query prior to calling `cursor.fetchall()`:

```python
# Insert record
cursor.execute(query, data)
connection.commit()
print(f"Inserted row. Affected rows: {cursor.rowcount}")

# Query updated table contents
cursor.execute("SELECT * FROM franco;")
for row in cursor.fetchall():
    print(row)
```