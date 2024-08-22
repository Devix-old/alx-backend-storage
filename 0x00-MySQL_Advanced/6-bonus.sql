-- QL script that creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name CHAR(255),
    IN score FLOAT
)
BEGIN
  DECLARE project_exists BOOL DEFAULT FALSE;
  
  -- Check if the project exists
  SET project_exists = EXISTS(
      SELECT 1
      FROM projects
      WHERE projects.name = project_name
  );
  
  IF NOT project_exists THEN
      -- Insert the new project
      INSERT INTO projects (name) VALUES (project_name);
      -- Get the new project ID
      SET @project_id = LAST_INSERT_ID();
      -- Insert the correction with the new project ID
      INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, @project_id, score);
  ELSE
      -- Get the existing project ID
      SET @project_id = (SELECT id FROM projects WHERE name = project_name);
      -- Insert the correction with the existing project ID
      INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, @project_id, score);
  END IF;
END //

DELIMITER ;
