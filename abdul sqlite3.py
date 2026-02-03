import sqlite3

# =========================
# CONNECT TO DATABASE
# =========================
database = sqlite3.connect("biomed_friend.db")
database.execute("PRAGMA foreign_keys = ON;")
cursor = database.cursor()
print("Connected to the friend's database successfully\n")

# =========================
# CREATE TABLES
# =========================

# Patients Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS PatientInfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER CHECK(age BETWEEN 18 AND 90),
    gender TEXT CHECK(gender IN ('Male','Female','Other')),
    enrollment TEXT NOT NULL
);
""")
print("PatientInfo table created")

# Visits Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS PatientVisits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    visit_date TEXT NOT NULL,
    sys_bp INTEGER,
    dia_bp INTEGER,
    glucose REAL,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES PatientInfo(id) ON DELETE CASCADE
);
""")
print("PatientVisits table created")

# Samples Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS PatientSamples (
    sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    collect_date TEXT NOT NULL,
    type TEXT CHECK(type IN ('Blood','Serum','Plasma','Urine')),
    location TEXT,
    FOREIGN KEY (patient_id) REFERENCES PatientInfo(id) ON DELETE CASCADE
);
""")
print("PatientSamples table created\n")

# =========================
# INSERT DATA
# =========================

# Patients
patient_list = [
    ("Paiman", 22, "Female", "2025-01-10"),
    ("Abdul Rehman", 24, "Male", "2025-02-15"),
    ("Ammar", 23, "Male", "2025-03-01")
]

for p in patient_list:
    cursor.execute("""
    INSERT INTO PatientInfo (name, age, gender, enrollment)
    VALUES (?, ?, ?, ?);
    """, p)
print("Patients added successfully\n")

# Visits
visit_records = [
    (1, "2025-01-20", 150, 95, 7.2, "High BP noted"),
    (1, "2025-02-20", 140, 90, 6.8, "BP improved"),
    (2, "2025-02-25", 120, 80, 5.5, "Routine check"),
    (3, "2025-03-10", 160, 100, 8.1, "Diabetes risk")
]

for v in visit_records:
    cursor.execute("""
    INSERT INTO PatientVisits
    (patient_id, visit_date, sys_bp, dia_bp, glucose, notes)
    VALUES (?, ?, ?, ?, ?, ?);
    """, v)
print("Visits added successfully\n")

# Samples
sample_data = [
    (1, "2025-01-20", "Blood", "Freezer A1"),
    (1, "2025-02-20", "Serum", "Freezer A2"),
    (2, "2025-02-25", "Urine", "Shelf B1"),
    (3, "2025-03-10", "Plasma", "Freezer C1"),
    (3, "2025-03-15", "Blood", "Freezer C2")
]

for s in sample_data:
    cursor.execute("""
    INSERT INTO PatientSamples
    (patient_id, collect_date, type, location)
    VALUES (?, ?, ?, ?);
    """, s)
print("Samples added successfully\n")

# =========================
# READ QUERIES
# =========================

# Simple SELECT
print("=== List of Patients ===")
cursor.execute("SELECT name, age, enrollment FROM PatientInfo")
for row in cursor.fetchall():
    print(f"Name: {row[0]}, Age: {row[1]}, Enrollment: {row[2]}")

# JOIN Query
print("\n=== Visits for Paiman ===")
cursor.execute("""
SELECT PatientInfo.name, PatientVisits.visit_date, PatientVisits.sys_bp, PatientVisits.dia_bp
FROM PatientInfo
JOIN PatientVisits
ON PatientInfo.id = PatientVisits.patient_id
WHERE PatientInfo.name='Paiman';
""")
for row in cursor.fetchall():
    print(f"Name: {row[0]}, Visit: {row[1]}, Systolic: {row[2]}, Diastolic: {row[3]}")

# Conditional SELECT
print("\n=== Patients with Systolic BP > 140 ===")
cursor.execute("""
SELECT DISTINCT PatientInfo.name, PatientVisits.sys_bp
FROM PatientInfo
JOIN PatientVisits
ON PatientInfo.id = PatientVisits.patient_id
WHERE PatientVisits.sys_bp > 140;
""")
for row in cursor.fetchall():
    print(f"Name: {row[0]}, Systolic BP: {row[1]}")

# =========================
# UPDATE & DELETE
# =========================

# Update sample location
cursor.execute("""
UPDATE PatientSamples
SET location='Freezer Z1'
WHERE sample_id=1;
""")
print("\nSample location updated")

# Delete a patient (cascade)
cursor.execute("""
DELETE FROM PatientInfo
WHERE id=2;
""")
print("Patient Abdul Rehman deleted with related visits and samples\n")

# =========================
# FINAL SAVE AND CLOSE
# =========================
database.commit()
database.close()
print("All operations completed successfully!")
