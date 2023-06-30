# CREATE TABLES
create_college_table = """
CREATE TABLE IF NOT EXISTS college_v2(
    college_code VARCHAR(10) PRIMARY KEY,
    college_desc VARCHAR(50) NOT NULL
);
"""

create_course_table = """
CREATE TABLE IF NOT EXISTS course_v2(
    course_code VARCHAR(10) PRIMARY KEY,
    course_desc VARCHAR(50) NOT NULL,
    college_key VARCHAR(10) NOT NULL,
    FOREIGN KEY (college_key) REFERENCES college (college_code) ON DELETE CASCADE
);
"""

create_student_table = """
CREATE TABLE IF NOT EXISTSstudent_v2(
    student_id INT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    year_level VARCHAR(10) NOT NULL,
    gender VARCHAR(6),
    college_key VARCHAR(10) NOT NULL,
    course_key VARCHAR(10) NOT NULL,
    FOREIGN KEY (college_key) REFERENCES college (college_code) ON DELETE CASCADE,
    FOREIGN KEY (course_key) REFERENCES course (course_code) ON DELETE CASCADE
);
"""

# POPULATE TABLES
populate_college = """
INSERT INTO college_v2 VALUES
('CSM', 'College of Science and Mathematics'),
('CASS', 'College of Arts and Social Sciences'),
('CCS', 'College of Computer Studies'),
('COET', 'College of Engineering Technology'),
('CEBA', 'College of Economics, Business and Accountancy'),
('COE', 'College of Education');
"""

populate_course = """
INSERT INTO course_v2 VALUES
('BSCS', 'Bachelor of Science in Computer Science', 'CCS'),
('BSIT', 'Bachelor of Science in Information Technology', 'CCS'),
('BSIS', 'Bachelor of Science in Information Systems', 'CCS'),
('BSCA', 'Bachelor of Science in Computer Application', 'CCS'),
('BSA', 'Bachelor of Science in Accountancy', 'CEBA'),
('BSHM', 'Bachelor of Science in Hospitality Management', 'CEBA'),
('BSChem', 'Bachelor of Science in Chemistry', 'CSM'),
('BAPolSci', 'Bachelor of Science in Political Science', 'CASS'),
('BAPsych', 'Bachelor of Science in Psychology', 'CASS'),
('BSM', 'Bachelor of Science in Mathematics', 'CSM');
"""

populate_student = """
INSERT INTO student_v2 VALUES
(101, 'Marina', 'Berg','1st Year', 'Female', 'CCS', 'BSIT'),
(102, 'Andrea', 'Duerr', '1st Year', 'Female', 'CASS', 'BAPsych'),
(103, 'Philipp', 'Probst',  '1st Year', 'Male', 'CCS', 'BSIT'),
(104, 'René',  'Brandt',  '1st Year',  'Male', 'CCS', 'BSCS'),
(105, 'Susanne', 'Shuster', '2nd Year', 'Female', 'CASS', 'BAPsych'),
(106, 'Christian', 'Schreiner', '2nd Year', 'Female', 'CASS', 'BAPolSci'),
(107, 'Harry', 'Kim', '3rd Year', 'Male', 'CSM', 'BSM'),
(108, 'Jan', 'Nowak', '3rd Year', 'Male', 'CCS', 'BSCS'),
(109, 'Pablo', 'Garcia',  '3rd Year', 'Male', 'CCS', 'BSCS'),
(110, 'Melanie', 'Dreschler', '3rd Year', 'Female', 'CSM', 'BSM'),
(111, 'Dieter', 'Durr',  '4th Year', 'Female', 'CSM', 'BSM'),
(112, 'Max', 'Mustermann', '4th Year', 'Male', 'CSM', 'BSM'),
(113, 'Maxine', 'Mustermann', '4th Year', 'Male', 'CSM', 'BSM'),
(114, 'Heiko', 'Fleischer', '4th Year', 'Male', 'CASS', 'BAPolSci'),
(115, 'Marina', 'Berg', '1st Year', 'Female', 'CASS', 'BAPolSci'),
(116, 'John', 'Smith', '2nd Year', 'Male', 'CEBA', 'BSA'),
(117, 'Emily', 'Johnson', '3rd Year', 'Female', 'CEBA', 'BSA'),
(118, 'David', 'Lee', '4th Year', 'Male', 'CASS', 'BAPsych'),
(119, 'Sophia', 'Garcia', '1st Year', 'Female', 'CEBA', 'BSA'),
(120, 'Michael', 'Martinez', '2nd Year', 'Male', 'CSM', 'BSM'),
(121, 'Marina', 'Smith', '3rd Year', 'Female', 'CCS', 'BSCS'),
(122, 'John', 'Berg', '4th Year', 'Male', 'CSM', 'BSM'),
(123, 'Emily', 'Garcia', '1st Year', 'Female', 'CSM', 'BSM'),
(124, 'David', 'Johnson', '2nd Year', 'Male', 'CCS', 'BSCA'),
(125, 'Sophia', 'Martinez', '3rd Year', 'Female', 'CCS', 'BSCS'),
(126, 'Michael', 'Lee', '4th Year', 'Male', 'CCS', 'BSIS'),
(127, 'Marina', 'Johnson', '1st Year', 'Female', 'CSM', 'BSM'),
(128, 'John', 'Martinez', '2nd Year', 'Male', 'CSM', 'BSM'),
(129, 'Emily', 'Berg', '3rd Year', 'Female', 'CEBA', 'BSA'),
(130, 'David', 'Garcia', '4th Year', 'Male', 'CSM', 'BSM'),
(131, 'Sophia', 'Lee', '1st Year', 'Female', 'CCS', 'BSIT'),
(132, 'Michael', 'Johnson', '2nd Year', 'Male', 'CASS', 'BAPolSci'),
(133, 'Marina', 'Martinez', '3rd Year', 'Female', 'CASS', 'BAPolSci'),
(134, 'John', 'Garcia', '4th Year', 'Male', 'CASS', 'BAPolSci'),
(135, 'Emily', 'Lee', '1st Year', 'Female', 'CASS', 'BAPolSci'),
(136, 'David', 'Johnson', '2nd Year', 'Male', 'CCS', 'BSCA'),
(137, 'Sophia', 'Berg', '3rd Year', 'Female', 'CCS', 'BSIS'),
(138, 'Michael', 'Smith', '4th Year', 'Male', 'CCS', 'BSIS'),
(139, 'Marina', 'Garcia', '1st Year', 'Female', 'CSM', 'BSM'),
(140, 'John', 'Lee', '2nd Year', 'Male', 'CSM', 'BSM'),
(141, 'Emily', 'Martinez', '3rd Year', 'Female', 'CSM', 'BSM'),
(142, 'David', 'Johnson', '4th Year', 'Male', 'CSM', 'BSM'),
(143, 'Sophia', 'Berg', '1st Year', 'Female', 'CEBA', 'BSA'),
(144, 'Michael', 'Garcia', '2nd Year', 'Male', 'CSM', 'BSM'),
(145, 'Marina', 'Johnson', '3rd Year', 'Female', 'CASS', 'BAPolSci'),
(146, 'John', 'Martinez', '4th Year', 'Male', 'CASS', 'BAPolSci'),
(147, 'Emily', 'Lee', '1st Year', 'Female', 'CCS', 'BSCS'),
(148, 'David', 'Smith', '2nd Year', 'Male', 'CSM', 'BSM'),
(149, 'Sophia', 'Garcia', '3rd Year', 'Female', 'CSM', 'BSM'),
(150, 'Michael', 'Berg', '4th Year', 'Male', 'CSM', 'BSM');
"""
