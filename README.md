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
- [License](#license)

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
   git clone https://github.com/username/repo-name.git
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

## Project Structure
```
project/
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
