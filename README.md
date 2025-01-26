# LuigiETL

# Data Pipeline with Luigi

This project is a data pipeline built using **Luigi** to extract, transform, and load (ETL) data into a PostgreSQL database. It demonstrates how to automate data workflows and handle dependencies between tasks.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)


## About
The project consists of the following tasks:
1. **Extract**: Fetch data from a database and a JSON file.
2. **Transform**: Clean, join, and transform the data.
3. **Load**: Load the transformed data into a PostgreSQL database.

The pipeline is orchestrated using **Luigi**, a Python library for building complex data workflows.

## Features
- **Extract**: Fetch data from multiple sources (database and JSON).
- **Transform**: Perform data cleaning, joining, and column transformations.
- **Load**: Load the transformed data into a PostgreSQL database.
- **Automation**: Use Luigi to manage task dependencies and execution.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/alwanrahmanas/LuigiETL.git
   cd repo-name

2. pip install -r requirements.txt

3. Set up Env

- DB_USER_Neon=your_db_user
- DB_PASSWORD_Neon=your_db_password
- DB_HOST_Neon=your_db_host
- DB_NAME_Neon=your_db_name
- DB_SSLMODE_Neon=require

4. Run The Pipeline

```
python -m luigi --module main LoadData --local-scheduler
```

## Usage

1. Extract
- The ExtractFromDB task fetches data from a PostgreSQL database.

- The ExtractFromJson task fetches data from a JSON file.

2. Transform
- The TransformTask performs the following transformations:

- Joins customer and reservation data.

- Adds new columns (full_name, currency, email_domain).

- Handles missing values in the payment_date column.

3. Load
- The LoadData task loads the transformed data into a PostgreSQL database.

## Project Structure
```
project/
├── data/
├── docker/
│   ├── dokcer-compose.yml       # yml extension
│   ├── init.sql        # one of data source
├── module/
│   ├── __init__.py       # Empty file to make `module` a package
│   ├── Extract.py        # Contains ExtractFromJson and ExtractFromDB
│   ├── Transform.py      # Contains TransformTask
│   ├── Load.py           # Contains LoadData
├── main.py               # Main script to run the pipeline
├── requirements.txt      # List of dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation

```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Commit your changes (git commit -m "Add new feature").

4. Push to the branch (git push origin feature-branch).

5. Open a pull request.





