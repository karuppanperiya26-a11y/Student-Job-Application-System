"""SQLite persistence for the Java menu. Each menu action uses one transaction."""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "data" / "tracker.db"

def write(conn, action, args):
    if action == "student":
        conn.execute("INSERT INTO student VALUES(?,?,?) ON CONFLICT(reg) DO UPDATE SET name=excluded.name,department=excluded.department",args)
    elif action == "skill":
        conn.execute("INSERT INTO student_skill VALUES(?,?)",args)
    elif action == "project":
        reg,title,domain,description,*tech = args
        key = conn.execute("INSERT INTO project(reg,title,domain,description) VALUES(?,?,?,?)",(reg,title,domain,description)).lastrowid
        conn.executemany("INSERT INTO project_tech VALUES(?,?)",[(key,t) for t in tech])
        return f"Project saved with ID {key}"
    elif action == "milestone":
        conn.execute("INSERT INTO milestone(project_id,name,due) VALUES(?,?,?)",args)
    elif action == "submit":
        date,project,name = args
        if not conn.execute("UPDATE milestone SET submitted=? WHERE project_id=? AND name=? AND submitted IS NULL",(date,project,name)).rowcount:
            raise ValueError("Milestone is missing or already complete.")
    elif action == "mark":
        conn.execute("INSERT INTO evaluation VALUES(?,?,?) ON CONFLICT(project_id,component) DO UPDATE SET mark=excluded.mark",args)
    elif action == "reports":
        for title,sql in zip(("Project progress","Student skills","Milestone dates","Component marks","Technologies"),(ROOT/"sql/reports.sql").read_text().strip().rstrip(";").split(";")):
            cursor=conn.execute(sql)
            print(title)
            print(" | ".join(column[0] for column in cursor.description))
            for row in cursor:
                print(" | ".join("-" if v is None else str(v) for v in row))
        return
    else:
        raise ValueError("Unknown action.")
    return "Saved."

if __name__ == "__main__":
    try:
        with sqlite3.connect(DATABASE.as_uri()+"?mode=rw",uri=True) as conn:
            conn.execute("PRAGMA foreign_keys=ON")
            message=write(conn,sys.argv[1],sys.argv[2:])
        if message:
            print(message)
    except (sqlite3.Error,ValueError) as error:
        sys.exit(f"Rejected: {error}")
