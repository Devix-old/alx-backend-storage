-- Create table

CREATE TABLE IF NOT EXISTS `users`(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email CHAR(255) NOT NULL UNIQUE,
	name char(255)
);

