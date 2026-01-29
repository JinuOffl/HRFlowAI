# backend/models/db.py
from sqlalchemy import create_engine, text
import pandas as pd

# Use SQLite for MVP
DATABASE_URL = "sqlite:///./hrms_mvp.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    with engine.connect() as conn:
        # 1. Create Tables (Condensed for brevity - add all your CREATE TABLE statements here)
        # We will add the critical ones for the demo
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                uuid char(36) PRIMARY KEY,
                first_name varchar(255),
                last_name varchar(255),
                official_email varchar(255),
                job_role varchar(255)
            );
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS attendance_records (
                uuid char(36) PRIMARY KEY,
                employee_id char(36),
                date date,
                check_in_time datetime,
                check_out_time datetime,
                status varchar(50)
            );
        """))

        # 2. Insert Sample Data (Idempotent check)
        check = conn.execute(text("SELECT count(*) FROM employees")).scalar()
        if check == 0:
            print("Seeding data...")
            conn.execute(text("""
                INSERT INTO employees (uuid, first_name, last_name, official_email, job_role) VALUES 
                ('emp001', 'Rahul', 'Sharma', 'rahul@company.com', 'Developer'),
                ('emp002', 'Priya', 'Verma', 'priya@company.com', 'HR'),
                ('emp003', 'Amit', 'Singh', 'amit@company.com', 'Manager');
            """))
            
            conn.execute(text("""
                INSERT INTO attendance_records (uuid, employee_id, date, check_in_time, check_out_time, status) VALUES 
                ('att1', 'emp001', '2023-10-01', '2023-10-01 09:00:00', '2023-10-01 18:00:00', 'present'),
                ('att2', 'emp001', '2023-10-02', '2023-10-02 09:15:00', '2023-10-02 18:15:00', 'present'),
                ('att3', 'emp001', '2023-10-03', '2023-10-03 10:00:00', '2023-10-03 16:00:00', 'half-day'),
                ('att4', 'emp002', '2023-10-01', '2023-10-01 09:00:00', '2023-10-01 17:00:00', 'present');
            """))
            conn.commit()
            print("Data seeded.")

def get_engine():
    return engine