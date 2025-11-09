import sqlite3
import json
from datetime import datetime

class Database:
    """Simple SQLite database for storing reports"""
    
    def __init__(self, db_path="healthai.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symptoms TEXT,
                risk_score REAL,
                synthesis TEXT,
                evidence TEXT,
                specialist_reports TEXT,
                report_json TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_report(self, report_data):
        """Save a report to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reports (timestamp, symptoms, risk_score, synthesis, evidence, specialist_reports, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            report_data.get('symptoms', ''),
            report_data.get('risk_score', 0.0),
            report_data.get('synthesis', ''),
            report_data.get('evidence', ''),
            json.dumps(report_data.get('specialist_reports', {})),
            json.dumps(report_data)
        ))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    def get_report(self, report_id):
        """Retrieve a report by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'timestamp': row[1],
                'symptoms': row[2],
                'risk_score': row[3],
                'synthesis': row[4],
                'evidence': row[5],
                'specialist_reports': json.loads(row[6]),
                'report_json': json.loads(row[7])
            }
        return None
    
    def get_all_reports(self, limit=10):
        """Get recent reports"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, symptoms, risk_score FROM reports ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [{'id': r[0], 'timestamp': r[1], 'symptoms': r[2], 'risk_score': r[3]} for r in rows]
