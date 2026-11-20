SELECT * FROM progress ORDER BY id;
SELECT s.reg,s.name,coalesce(k.skill,'No recorded skill') AS skill FROM student s LEFT JOIN student_skill k USING(reg) ORDER BY s.reg,k.skill;
SELECT p.id,p.title,m.name,m.due,m.submitted,CASE WHEN m.submitted IS NULL THEN 'Pending' ELSE 'Complete' END AS status FROM project p JOIN milestone m ON m.project_id=p.id ORDER BY p.id,m.due;
SELECT project_id,component,mark FROM evaluation ORDER BY project_id,component;
SELECT project_id,technology FROM project_tech ORDER BY project_id,technology;
