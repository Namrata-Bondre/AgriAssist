# =====================================================
# Database Connection
# Connects Python with SQL Server database.
# =====================================================

import pyodbc


# SQL Server details
SERVER = "LAPTOP-VDU388KU"
DATABASE = "MiniAgriAssistDB"


# Create database connection
connection = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)