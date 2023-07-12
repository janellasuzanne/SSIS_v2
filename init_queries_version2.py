create_database_query = 'CREATE DATABASE IF NOT EXISTS version2'

create_course_ver2_table_query = """
CREATE TABLE IF NOT EXISTS course_ver2(
    code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255) NOT NULL
);
"""

create_student_ver2_table_query = """
CREATE TABLE IF NOT EXISTS student_ver2 (
    id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    year_level ENUM('1st Year', '2nd Year', '3rd Year', '4th Year'),
    gender ENUM('Not Stated', 'Female', 'Male') DEFAULT 'Not Stated',
    course_key VARCHAR(20),
    FOREIGN KEY (course_key)
        REFERENCES course_ver2 (code)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
"""

populate_coursesv2 = """
INSERT INTO course_ver2 VALUES
('BSCS', 'Bachelor of Science in Computer Science'),
('BSIT', 'Bachelor of Science in Information Technology'),
('BSIS', 'Bachelor of Science in Information Systems'),
('BSCA', 'Bachelor of Science in Computer Application'),
('BSA', 'Bachelor of Science in Accountancy'),
('BSHM', 'Bachelor of Science in Hospitality Management'),
('BSChem', 'Bachelor of Science in Chemistry'),
('BAPolSci', 'Bachelor of Science in Political Science'),
('BAPsych', 'Bachelor of Science in Psychology'),
('BSM', 'Bachelor of Science in Mathematics');
"""

populate_studentsv2 = """
INSERT INTO student_ver2 VALUES
(101, 'Marina', 'Berg','1st Year', 'Female', 'BSIT'),
(102, 'Andrea', 'Duerr', '1st Year', 'Female', 'BAPsych'),
(103, 'Philipp', 'Probst',  '1st Year', 'Male', 'BSIT'),
(104, 'René',  'Brandt',  '1st Year',  'Male', 'BSCS'),
(105, 'Susanne', 'Shuster', '2nd Year', 'Female', 'BAPsych'),
(106, 'Christian', 'Schreiner', '2nd Year', 'Female', 'BAPolSci'),
(107, 'Harry', 'Kim', '3rd Year', 'Male', 'BSM'),
(108, 'Jan', 'Nowak', '3rd Year', 'Male', 'BSHM'),
(109, 'Pablo', 'Garcia',  '3rd Year', 'Male', 'BSCS'),
(110, 'Melanie', 'Dreschler', '3rd Year', 'Female', 'BSM'),
(111, 'Dieter', 'Durr',  '4th Year', 'Female', 'BSM'),
(112, 'Max', 'Mustermann', '4th Year', 'Male', 'BSHM'),
(113, 'Maxine', 'Mustermann', '4th Year', 'Male', 'BSM'),
(114, 'Heiko', 'Fleischer', '4th Year', 'Male', 'BAPolSci'),
(115, 'Marina', 'Berg', '1st Year', 'Female', 'BAPolSci'),
(116, 'John', 'Smith', '2nd Year', 'Male', 'BSA'),
(117, 'Emily', 'Johnson', '3rd Year', 'Female', 'BSA'),
(118, 'David', 'Lee', '4th Year', 'Male', 'BAPsych'),
(119, 'Sophia', 'Garcia', '1st Year', 'Female', 'BSA'),
(120, 'Michael', 'Martinez', '2nd Year', 'Male', 'BSM'),
(121, 'Marina', 'Smith', '3rd Year', 'Female', 'BSCS'),
(122, 'John', 'Berg', '4th Year', 'Male', 'BSM'),
(123, 'Emily', 'Garcia', '1st Year', 'Female', 'BSM'),
(124, 'David', 'Johnson', '2nd Year', 'Male', 'BSCA'),
(125, 'Sophia', 'Martinez', '3rd Year', 'Female', 'BSCS'),
(126, 'Michael', 'Lee', '4th Year', 'Male', 'BSIS'),
(127, 'Marina', 'Johnson', '1st Year', 'Female', 'BSM'),
(128, 'John', 'Martinez', '2nd Year', 'Male', 'BSM'),
(129, 'Emily', 'Berg', '3rd Year', 'Female', 'BSA'),
(130, 'David', 'Garcia', '4th Year', 'Male', 'BSM'),
(131, 'Sophia', 'Lee', '1st Year', 'Female', 'BSIT'),
(132, 'Michael', 'Johnson', '2nd Year', 'Male', 'BAPolSci'),
(133, 'Marina', 'Martinez', '3rd Year', 'Female', 'BAPolSci'),
(134, 'John', 'Garcia', '4th Year', 'Male', 'BSHM'),
(135, 'Emily', 'Lee', '1st Year', 'Female', 'BSHM'),
(136, 'David', 'Johnson', '2nd Year', 'Male', 'BSCA'),
(137, 'Sophia', 'Berg', '3rd Year', 'Female', 'BSIS'),
(138, 'Michael', 'Smith', '4th Year', 'Male', 'BSIS'),
(139, 'Marina', 'Garcia', '1st Year', 'Female', 'BSM'),
(140, 'John', 'Lee', '2nd Year', 'Male', 'BSM'),
(141, 'Emily', 'Martinez', '3rd Year', 'Female', 'BSM'),
(142, 'David', 'Johnson', '4th Year', 'Male', 'BSM'),
(143, 'Sophia', 'Berg', '1st Year', 'Female', 'BSA'),
(144, 'Michael', 'Garcia', '2nd Year', 'Male', 'BSM'),
(145, 'Marina', 'Johnson', '3rd Year', 'Female', 'BAPolSci'),
(146, 'John', 'Martinez', '4th Year', 'Male', 'BAPolSci'),
(147, 'Emily', 'Lee', '1st Year', 'Female', 'BSChem'),
(148, 'David', 'Smith', '2nd Year', 'Male', 'BSChem'),
(149, 'Sophia', 'Garcia', '3rd Year', 'Female', 'BSChem'),
(150, 'Michael', 'Berg', '4th Year', 'Male', 'BSChem');
"""