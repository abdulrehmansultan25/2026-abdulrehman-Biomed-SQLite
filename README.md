Biomedical Research Database using SQLite and Python

This project creates a small relational database system for managing biomedical study data using Python and SQLite. The database stores information about enrolled patients, their clinical follow-up visits, and collected biological samples.

Three related tables are implemented: Patients, Clinical_Visits, and Samples. Each table uses a primary key for unique identification, and foreign keys are used to connect visits and samples to patients. Cascading delete is enabled to automatically remove associated records when a patient is deleted.

The Python script demonstrates core database operations including inserting records, retrieving data using SELECT and JOIN queries, updating sample storage locations, and deleting patient records.

How to execute:

1. Ensure Python is installed.
2. Keep main.py in a project folder.
3. Open a terminal inside that folder.
4. Run: python main.py

After execution, the database file is created and populated, query results are printed to the console, and update and delete operations are demonstrated.
