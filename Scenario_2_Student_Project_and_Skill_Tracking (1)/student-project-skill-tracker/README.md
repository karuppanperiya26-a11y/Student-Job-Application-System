# Student Project and Skill Tracking System

Scenario 2 · Register numbers 2, 32, 62, 92 and L2.

Department staff record student skills, individual projects, milestones and marks through a Java menu. A Python standard-library adapter saves each action to SQLite. A separate Python analysis reads that same database and creates three charts.

## Run on Windows

1. Extract the entire ZIP. Open the student-project-skill-tracker folder in VS Code.
2. Open Terminal → New Terminal. Check that `java -version` reports JDK 17 or newer and `python --version` shows Python 3. If Windows uses the Python launcher, run `$env:TRACKER_PYTHON="py"` in PowerShell and use `py` for the Python commands below.
3. Run `java TrackerApp.java`. Enter **7** to view the sample data. Book Finder is complete, Rain Log has one of two milestones submitted, and Lab Slots has no milestones yet. Enter **0** to exit.
4. To refresh the charts after edits, run `python -m pip install -r analysis/requirements.txt` and then `python analysis/charts.py`. Open the PNG files in analysis/output.

## Database and evidence

The included data/tracker.db is ready to use. To recreate a separate practice database, open a new SQLite database in DB Browser for SQLite, execute sql/schema.sql followed by sql/sample_data.sql and save it. sql/reports.sql contains the five report queries. All names and records are synthetic.

The demo input and captured Java output in samples/ were run against a separate copy of the included database. To replay on Windows from an extracted practice copy, use `cmd /c "java TrackerApp.java < samples/input.txt"`. A replay changes that copy. Project ID 5 assumes a fresh seed.

## Submission

docs/ contains the SRS, use case, class, architecture and ER diagrams, relational model, normalization, four subject write-ups and acceptance results. Upload the extracted files and folders to your individual repository.
