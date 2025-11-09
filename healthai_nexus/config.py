"""Configuration file for organized file structure"""
import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# Subdirectories
REPORTS_DIR = os.path.join(OUTPUTS_DIR, "reports")
PRESCRIPTIONS_DIR = os.path.join(OUTPUTS_DIR, "prescriptions")
PDFS_DIR = os.path.join(OUTPUTS_DIR, "pdfs")

# Database paths
USERS_DB = os.path.join(BASE_DIR, "users.db")
HEALTH_DB = os.path.join(BASE_DIR, "healthai.db")

# Create directories if they don't exist
for directory in [OUTPUTS_DIR, REPORTS_DIR, PRESCRIPTIONS_DIR, PDFS_DIR]:
    os.makedirs(directory, exist_ok=True)
