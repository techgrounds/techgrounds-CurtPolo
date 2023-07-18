-- Connect to the MySQL database
USE Cloud10WSDatabase;

-- Create Table 1
CREATE TABLE IF NOT EXISTS table1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    column1 VARCHAR(255),
    column2 INT,
    column3 DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Table 2
CREATE TABLE IF NOT EXISTS table2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    column1 VARCHAR(255),
    column2 DATE,
    column3 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Table 3
CREATE TABLE IF NOT EXISTS table3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    column1 INT,
    column2 VARCHAR(255),
    column3 ENUM('Option 1', 'Option 2', 'Option 3'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add any additional tables here

-- Commit the changes
COMMIT;
