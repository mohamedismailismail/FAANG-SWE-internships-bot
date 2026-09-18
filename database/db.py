import sqlite3    # database to keep the sent jobs to prevent it from being sent again.
import os    # make the code speak with the Operating system.

# Define database file path inside the project root.
DB_NAME = "jobs.db"
# Making accessing the jobs.db file from the main folder easy and prevent FileNotFoundError.
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_NAME)

def get_connection():    # Establishes and returns a connection to the SQLite database.
    return sqlite3.connect(DB_PATH)

def init_db():    # Initializes the database schema if it doesn't exist and when exist the function will be skipped.
    with get_connection() as conn:    # using Context Manager helps preventing Resource Leaks.
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def is_job_seen(job_id: str) -> bool:    # Checks if a job has already been tracked and alerted.
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
        return cursor.fetchone() is not None

def save_job(job_id: str, company: str, title: str, link: str) -> bool:
    """
    Saves a new job to the database.
    Returns True if inserted, False if it already exists.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # SQL query
            cursor.execute("""
                INSERT INTO jobs (job_id, company, title, link)
                VALUES (?, ?, ?, ?)
            """, (job_id, company, title, link))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # Prevent insertion if job_id already exists (Constraint violation)
        return False

if __name__ == "__main__":
    # Test database operations
    init_db()
    test_id = "meta-swe-intern-2026-001"
    
    print(f">> Initial Seen Check: {is_job_seen(test_id)}")  # Should be False
    saved = save_job(test_id, "Meta", "SWE Intern", "https://metacareers.com")
    print(f">> Saved Successfully: {saved}")                 # Should be True
    print(f">> Second Seen Check: {is_job_seen(test_id)}")   # Should be True
    saved_again = save_job(test_id, "Meta", "SWE Intern", "https://metacareers.com")
    print(f">> Duplicate Prevented: {not saved_again}")     # Should be True