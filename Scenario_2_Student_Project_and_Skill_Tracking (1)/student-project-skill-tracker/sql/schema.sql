PRAGMA foreign_keys=ON;
CREATE TABLE student(reg TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, department TEXT NOT NULL);
CREATE TABLE student_skill(reg TEXT REFERENCES student NOT NULL, skill TEXT COLLATE NOCASE NOT NULL, PRIMARY KEY(reg,skill));
CREATE TABLE project(id INTEGER PRIMARY KEY, reg TEXT REFERENCES student NOT NULL, title TEXT NOT NULL, domain TEXT NOT NULL, description TEXT NOT NULL);
CREATE TABLE project_tech(project_id INTEGER REFERENCES project NOT NULL, technology TEXT COLLATE NOCASE NOT NULL, PRIMARY KEY(project_id,technology));
CREATE TABLE milestone(project_id INTEGER REFERENCES project NOT NULL, name TEXT COLLATE NOCASE NOT NULL, due TEXT NOT NULL, submitted TEXT, PRIMARY KEY(project_id,name));
CREATE TABLE component(name TEXT PRIMARY KEY COLLATE NOCASE NOT NULL);
CREATE TABLE evaluation(project_id INTEGER REFERENCES project NOT NULL, component TEXT COLLATE NOCASE REFERENCES component NOT NULL, mark INTEGER NOT NULL CHECK(typeof(mark)='integer' AND mark BETWEEN 0 AND 100), PRIMARY KEY(project_id,component));
CREATE VIEW progress AS
 SELECT p.id,p.title,p.domain,p.reg,COUNT(m.name) AS planned,COUNT(m.submitted) AS finished,
 CASE WHEN COUNT(m.name)=0 THEN 'Unplanned' WHEN COUNT(m.submitted)=COUNT(m.name) THEN 'Complete' ELSE 'In progress' END AS status
 FROM project p LEFT JOIN milestone m ON m.project_id=p.id GROUP BY p.id;
