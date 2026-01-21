create database quiz__db;
use quiz__db;
-- Categories Table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Sample categories
INSERT INTO categories (name) VALUES ('Maths'), ('Physics'), ('Chemistry'), ('CS');

-- Questions Table
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option1 VARCHAR(255),
    option2 VARCHAR(255),
    option3 VARCHAR(255),
    option4 VARCHAR(255),
    correct_option VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Students Score Table
CREATE TABLE students_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category_id INT NOT NULL,
    score INT DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
delete from questions where category_id='1';
select *from questions;
alter table questions modify column age_group varchar(20) not null;
INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
('1','Under 10','5 + 3 = ?','6','7','8','9','8'),
('1','Under 10','10 - 4 = ?','5','6','7','8','6'),
('1','Under 10','2 × 3 = ?','5','6','7','8','6'),
('1','Under 10','12 ÷ 4 = ?','2','3','4','6','3'),
('1','Under 10','Which number is biggest?','9','4','7','12','12'),
('1','Under 10','7 + 6 = ?','11','12','13','14','13'),
('1','Under 10','15 - 5 = ?','9','10','11','12','10'),
('1','Under 10','How many sides does a triangle have?','2','3','4','5','3'),
('1','Under 10','What comes after 19?','18','20','21','22','20'),
('1','Under 10','4 × 5 = ?','15','18','20','25','20');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(1, '10-15', 'What is 12 × 8?',
 '84', '92', '96', '88',
 '96'),

(1, '10-15', 'What is 144 ÷ 12?',
 '10', '11', '12', '13',
 '12'),

(1, '10-15', 'What is the square of 9?',
 '18', '27', '81', '72',
 '81'),

(1, '10-15', 'Which is a prime number?',
 '9', '15', '17', '21',
 '17'),

(1, '10-15', 'What is 3³?',
 '6', '9', '27', '81',
 '27'),

(1, '10-15', 'Perimeter of a square with side 5?',
 '10', '15', '20', '25',
 '20'),

(1, '10-15', 'What is 45 − 19?',
 '24', '26', '28', '30',
 '26'),

(1, '10-15', 'What is the LCM of 2 and 4?',
 '2', '4', '6', '8',
 '4'),

(1, '10-15', 'Which fraction is equal to 0.5?',
 '1/4', '1/3', '1/2', '2/3',
 '1/2'),

(1, '10-15', 'What is the value of 7 × 6 − 10?',
 '32', '36', '42', '52',
 '32');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(1, '16-24', 'Solve: 2x + 5 = 13',
 'x = 3', 'x = 4', 'x = 5', 'x = 6',
 'x = 4'),

(1, '16-24', 'Area of a circle with radius 7 (π=22/7)?',
 '144', '154', '164', '174',
 '154'),

(1, '16-24', 'What is √144?',
 '10', '11', '12', '13',
 '12'),

(1, '16-24', 'What is 25% of 200?',
 '25', '40', '50', '75',
 '50'),

(1, '16-24', 'Solve: x² = 49',
 'x = 5', 'x = 6', 'x = 7', 'x = 8',
 'x = 7'),

(1, '16-24', 'Sum of angles in a triangle?',
 '90°', '180°', '270°', '360°',
 '180°'),

(1, '16-24', 'What is the cube of 4?',
 '16', '32', '64', '128',
 '64'),

(1, '16-24', 'HCF of 18 and 24?',
 '6', '8', '12', '18',
 '6'),

(1, '16-24', 'If x = 3, value of 2x²?',
 '12', '18', '24', '36',
 '18'),

(1, '16-24', 'Which is an irrational number?',
 '4', '9', '√2', '16',
 '√2');


INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(1, '25+', 'What is the derivative of x²?',
 'x', '2x', 'x²', '2',
 '2x'),

(1, '25+', 'Solve: 3x − 7 = 11',
 'x = 4', 'x = 5', 'x = 6', 'x = 7',
 'x = 6'),

(1, '25+', 'Value of sin 90°?',
 '0', '1', '-1', 'Undefined',
 '1'),

(1, '25+', 'What is the probability of getting head?',
 '0', '1/4', '1/2', '1',
 '1/2'),

(1, '25+', 'What is log₁₀ 100?',
 '1', '2', '10', '100',
 '2'),

(1, '25+', 'If a = 2, b = 3, find a² + b²',
 '9', '10', '11', '13',
 '13'),

(1, '25+', 'What is the quadratic formula?',
 '(-b±√b²-4ac)/2a', '(-b±√b²+4ac)/2a',
 '(b±√b²-4ac)/2a', '(b±√b²-4ac)/a',
 '(-b±√b²-4ac)/2a'),

(1, '25+', 'Which angle is obtuse?',
 '45°', '90°', '120°', '60°',
 '120°'),

(1, '25+', 'What is the sum of first 10 natural numbers?',
 '45', '50', '55', '60',
 '55'),

(1, '25+', 'What is ∞?',
 'Largest number', 'Zero', 'Undefined', 'Infinite',
 'Infinite');
 
 INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(2, 'Under 10', 'Which force pulls objects towards the Earth?',
 'Magnetic force', 'Gravitational force', 'Frictional force', 'Electric force',
 'Gravitational force'),

(2, 'Under 10', 'What is the SI unit of length?',
 'Kilogram', 'Meter', 'Second', 'Newton',
 'Meter'),

(2, 'Under 10', 'Which object produces light?',
 'Moon', 'Mirror', 'Sun', 'Table',
 'Sun'),

(2, 'Under 10', 'Which sense organ is used to hear sound?',
 'Eye', 'Nose', 'Ear', 'Skin',
 'Ear'),

(2, 'Under 10', 'What is the shape of the Earth?',
 'Square', 'Flat', 'Spherical', 'Triangular',
 'Spherical'),

(2, 'Under 10', 'Which material is attracted by a magnet?',
 'Plastic', 'Wood', 'Iron', 'Paper',
 'Iron'),

(2, 'Under 10', 'What do we call the force that slows down moving objects?',
 'Gravity', 'Magnetism', 'Friction', 'Push',
 'Friction'),

(2, 'Under 10', 'Which device is used to measure time?',
 'Thermometer', 'Clock', 'Balance', 'Scale',
 'Clock'),

(2, 'Under 10', 'Which part of a plant conducts water?',
 'Leaf', 'Root', 'Stem', 'Flower',
 'Stem'),

(2, 'Under 10', 'Which source of energy comes from the Sun?',
 'Wind energy', 'Solar energy', 'Hydro energy', 'Nuclear energy',
 'Solar energy');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(2, '10-15', 'What is the SI unit of force?',
 'Joule', 'Newton', 'Watt', 'Pascal',
 'Newton'),

(2, '10-15', 'Which law explains action and reaction?',
 'First law of motion', 'Second law of motion', 'Third law of motion', 'Law of gravitation',
 'Third law of motion'),

(2, '10-15', 'Speed is defined as?',
 'Distance × Time', 'Distance ÷ Time', 'Time ÷ Distance', 'Mass ÷ Time',
 'Distance ÷ Time'),

(2, '10-15', 'Which type of energy is possessed by a moving object?',
 'Potential energy', 'Heat energy', 'Kinetic energy', 'Light energy',
 'Kinetic energy'),

(2, '10-15', 'Which instrument is used to measure electric current?',
 'Voltmeter', 'Ammeter', 'Galvanometer', 'Thermometer',
 'Ammeter'),

(2, '10-15', 'What happens to the shadow when an object is moved closer to the light source?',
 'Becomes smaller', 'Disappears', 'Becomes larger', 'Becomes lighter',
 'Becomes larger'),

(2, '10-15', 'Which mirror is used as a rear-view mirror in vehicles?',
 'Plane mirror', 'Concave mirror', 'Convex mirror', 'Cylindrical mirror',
 'Convex mirror'),

(2, '10-15', 'Which material is the best conductor of electricity?',
 'Rubber', 'Glass', 'Copper', 'Plastic',
 'Copper'),

(2, '10-15', 'What form of energy is sound?',
 'Mechanical energy', 'Electrical energy', 'Light energy', 'Chemical energy',
 'Mechanical energy'),

(2, '10-15', 'Which phenomenon causes the bending of light?',
 'Reflection', 'Refraction', 'Dispersion', 'Diffusion',
 'Refraction');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(2, '16-24', 'Which quantity remains constant in uniform circular motion?',
 'Speed', 'Velocity', 'Acceleration', 'Force',
 'Speed'),

(2, '16-24', 'Which type of current is supplied to homes?',
 'Direct current', 'Alternating current', 'Static current', 'Pulse current',
 'Alternating current'),

(2, '16-24', 'What is the unit of frequency?',
 'Hertz', 'Decibel', 'Joule', 'Watt',
 'Hertz'),

(2, '16-24', 'Which mirror can form a real and inverted image?',
 'Plane mirror', 'Convex mirror', 'Concave mirror', 'None',
 'Concave mirror'),

(2, '16-24', 'What happens to kinetic energy if speed is doubled?',
 'Becomes double', 'Becomes half', 'Becomes four times', 'Remains same',
 'Becomes four times'),

(2, '16-24', 'Which law explains the relation between current and resistance?',
 'Ohms law', 'Faradays law', 'Newton’s law', 'Coulombs law',
 'Ohms law'),

(2, '16-24', 'What is the unit of electric charge?',
 'Ampere', 'Volt', 'Coulomb', 'Ohm',
 'Coulomb'),

(2, '16-24', 'Which phenomenon causes rainbow formation?',
 'Reflection only', 'Refraction only', 'Dispersion and reflection', 'Diffusion',
 'Dispersion and reflection'),

(2, '16-24', 'Which gas is filled in electric bulbs?',
 'Oxygen', 'Nitrogen', 'Hydrogen', 'Carbon dioxide',
 'Nitrogen'),

(2, '16-24', 'What happens to pressure when area decreases?',
 'Decreases', 'Remains same', 'Increases', 'Becomes zero',
 'Increases');


INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(2,'25+', 'Which equation represents Einsteins mass-energy relation?',
 'E = mc', 'E = mc^2', 'E = mv^2', 'E = mgh',
 'E = mc^2'),

(2,'25+', 'What is the unit of electric field?',
 'N/C', 'C/N', 'V/A', 'J/C',
 'N/C'),

(2, '25+', 'Which law gives the direction of induced current?',
 'Ohms law', 'Faradays law', 'Lenz’s law', 'Coulombs law',
 'Lenz’s law'),

(2, '25+', 'What type of motion does a freely falling body have?',
 'Uniform motion', 'Non-uniform motion', 'Circular motion', 'Oscillatory motion',
 'Non-uniform motion'),

(2, '25+', 'Which particle determines the chemical properties of an atom?',
 'Neutron', 'Proton', 'Electron', 'Nucleus',
 'Electron'),

(2, '25+', 'What is the SI unit of capacitance?',
 'Farad', 'Henry', 'Weber', 'Tesla',
 'Farad'),

(2, '25+', 'Which quantity is conserved in elastic collision?',
 'Momentum only', 'Energy only', 'Both momentum and energy', 'Force',
 'Both momentum and energy'),

(2, '25+', 'What happens to resistance if temperature increases in a metal?',
 'Decreases', 'Increases', 'Becomes zero', 'Remains same',
 'Increases'),

(2, '25+', 'Which phenomenon proves the wave nature of light?',
 'Photoelectric effect', 'Interference', 'Compton effect', 'Pair production',
 'Interference'),

(2, '25+', 'What is the power of a lens whose focal length is 0.5 m?',
 '1 D', '2 D', '0.5 D', '5 D',
 '2 D');
 
 INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(3, 'Under 10', 'Which gas do we breathe in?',
 'Oxygen', 'Carbon dioxide', 'Nitrogen', 'Hydrogen',
 'Oxygen'),

(3, 'Under 10', 'What is the chemical symbol for Water?',
 'H2', 'O2', 'H2O', 'HO',
 'H2O'),

(3, 'Under 10', 'Which of these is a solid?',
 'Water', 'Milk', 'Ice', 'Air',
 'Ice'),

(3, 'Under 10', 'Which gas is essential for burning?',
 'Nitrogen', 'Carbon dioxide', 'Oxygen', 'Hydrogen',
 'Oxygen'),

(3, 'Under 10', 'What is the colour of copper sulphate solution?',
 'Green', 'Blue', 'Red', 'Yellow',
 'Blue'),

(3, 'Under 10', 'Which material is attracted by a magnet?',
 'Plastic', 'Wood', 'Iron', 'Rubber',
 'Iron'),

(3, 'Under 10', 'Which of the following is an acid?',
 'Soap', 'Salt', 'Lemon juice', 'Water',
 'Lemon juice'),

(3, 'Under 10', 'Which gas is used in balloons?',
 'Oxygen', 'Nitrogen', 'Helium', 'Carbon dioxide',
 'Helium'),

(3, 'Under 10', 'What happens to ice when heated?',
 'Freezes', 'Evaporates', 'Melts', 'Condenses',
 'Melts'),

(3, 'Under 10', 'Which of these is used to put out fire?',
 'Water', 'Oil', 'Petrol', 'Alcohol',
 'Water');


INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(3, '10-15', 'What is the chemical symbol of Sodium?',
 'So', 'Na', 'Sn', 'S',
 'Na'),

(3, '10-15', 'Which gas is released during photosynthesis?',
 'Carbon dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen',
 'Oxygen'),

(3, '10-15', 'What is the pH value of pure water?',
 '5', '6', '7', '8',
 '7'),

(3, '10-15', 'Which substance turns blue litmus red?',
 'Base', 'Salt', 'Acid', 'Water',
 'Acid'),

(3, '10-15', 'Which metal is liquid at room temperature?',
 'Iron', 'Mercury', 'Aluminium', 'Copper',
 'Mercury'),

(3, '10-15', 'What is the chemical formula of carbon dioxide?',
 'CO', 'CO2', 'C2O', 'C2O2',
 'CO2'),

(3, '10-15', 'Which acid is present in lemon?',
 'Acetic acid', 'Citric acid', 'Lactic acid', 'Sulphuric acid',
 'Citric acid'),

(3, '10-15', 'Which gas is used in fire extinguishers?',
 'Oxygen', 'Hydrogen', 'Carbon dioxide', 'Nitrogen',
 'Carbon dioxide'),

(3, '10-15', 'What type of reaction releases heat?',
 'Endothermic', 'Exothermic', 'Neutral', 'Reversible',
 'Exothermic'),

(3, '10-15', 'Which element is essential for combustion?',
 'Nitrogen', 'Hydrogen', 'Oxygen', 'Carbon',
 'Oxygen');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(3, '16-24', 'Which compound is used in the manufacture of glass?',
 'Sodium chloride', 'Calcium carbonate', 'Sodium carbonate', 'Potassium nitrate',
 'Sodium carbonate'),

(3, '16-24', 'What is the valency of oxygen?',
 '1', '2', '3', '4',
 '2'),

(3, '16-24', 'Which metal is most reactive?',
 'Copper', 'Iron', 'Sodium', 'Gold',
 'Sodium'),

(3, '16-24', 'Which process is used to separate crude oil?',
 'Filtration', 'Distillation', 'Fractional distillation', 'Evaporation',
 'Fractional distillation'),

(3, '16-24', 'Which salt is used in baking powder?',
 'Sodium chloride', 'Sodium carbonate', 'Sodium bicarbonate', 'Calcium carbonate',
 'Sodium bicarbonate'),

(3, '16-24', 'Which gas causes acid rain?',
 'Oxygen', 'Nitrogen', 'Sulphur dioxide', 'Hydrogen',
 'Sulphur dioxide'),

(3, '16-24', 'Which acid is present in vinegar?',
 'Citric acid', 'Lactic acid', 'Acetic acid', 'Formic acid',
 'Acetic acid'),

(3, '16-24', 'What is rust chemically?',
 'Iron oxide', 'Iron sulphide', 'Iron nitrate', 'Iron carbonate',
 'Iron oxide'),

(3, '16-24', 'Which element is used in galvanization?',
 'Copper', 'Aluminium', 'Zinc', 'Lead',
 'Zinc'),

(3, '16-24', 'Which type of bond involves sharing of electrons?',
 'Ionic bond', 'Metallic bond', 'Covalent bond', 'Hydrogen bond',
 'Covalent bond');


INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(3, '25+', 'What is the molecular formula of glucose?',
 'C6H6', 'C6H12O6', 'C12H22O11', 'CH2O',
 'C6H12O6'),

(3, '25+', 'Which law states that mass is neither created nor destroyed?',
 'Boyles law', 'Charles law', 'Law of conservation of mass', 'Avogadros law',
 'Law of conservation of mass'),

(3, '25+', 'Which electrode is positive in an electrolytic cell?',
 'Cathode', 'Anode', 'Neutral', 'Both',
 'Anode'),

(3, '25+', 'Which chemical is used in photography?',
 'Silver nitrate', 'Copper sulphate', 'Sodium chloride', 'Potassium bromide',
 'Silver nitrate'),

(3, '25+', 'Which reaction absorbs heat?',
 'Exothermic', 'Endothermic', 'Neutral', 'Oxidation',
 'Endothermic'),

(3, '25+', 'What is the oxidation state of oxygen in H2O2?',
 '-2', '-1', '0', '+1',
 '-1'),

(3, '25+', 'Which compound shows homologous series?',
 'Salts', 'Acids', 'Alkanes', 'Oxides',
 'Alkanes'),

(3, '25+', 'What is the pH of a strong base?',
 'Less than 7', 'Equal to 7', 'Greater than 7', 'Zero',
 'Greater than 7'),

(3, '25+', 'Which element has atomic number 17?',
 'Sulphur', 'Chlorine', 'Argon', 'Fluorine',
 'Chlorine'),

(3, '25+', 'Which process converts ore into metal?',
 'Refining', 'Concentration', 'Smelting', 'Roasting',
 'Smelting');
 
 INSERT INTO questions
(category_id,age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(4, 'Under 10', 'What does CPU stand for?',
 'Central Processing Unit', 'Computer Processing Unit', 'Central Program Unit', 'Control Processing Unit',
 'Central Processing Unit'),

(4, 'Under 10', 'Which device is used to input text?',
 'Monitor', 'Keyboard', 'Printer', 'Speaker',
 'Keyboard'),

(4, 'Under 10', 'Which of these is an output device?',
 'Mouse', 'Keyboard', 'Monitor', 'Scanner',
 'Monitor'),

(4,'Under 10', 'What is the brain of the computer?',
 'RAM', 'Hard Disk', 'CPU', 'Monitor',
 'CPU'),

(4, 'Under 10', 'Which one is an operating system?',
 'MS Word', 'Windows', 'Chrome', 'Paint',
 'Windows'),

(4, 'Under 10', 'Which key is used to create space?',
 'Enter', 'Shift', 'Spacebar', 'Tab',
 'Spacebar'),

(4, 'Under 10', 'What does RAM stand for?',
 'Random Access Memory', 'Read Access Memory', 'Run Access Memory', 'Real Access Memory',
 'Random Access Memory'),

(4, 'Under 10', 'Which device prints documents?',
 'Scanner', 'Printer', 'Monitor', 'Mouse',
 'Printer'),

(4, 'Under 10', 'Which of these is a computer language?',
 'English', 'Hindi', 'Python', 'Tamil',
 'Python'),

(4, 'Under 10', 'Which part stores data permanently?',
 'RAM', 'Cache', 'Hard Disk', 'CPU',
 'Hard Disk');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(4, '10-15', 'Which language is used for web development?',
 'Python', 'HTML', 'C', 'Java',
 'HTML'),

(4, '10-15', 'Which symbol is used for comments in Python?',
 '//', '#', '/* */', '--',
 '#'),

(4, '10-15', 'What is the full form of URL?',
 'Uniform Resource Locator', 'Universal Resource Link', 'Uniform Resource Link', 'Universal Resource Locator',
 'Uniform Resource Locator'),

(4, '10-15', 'Which data type stores true or false?',
 'int', 'string', 'boolean', 'float',
 'boolean'),

(4, '10-15', 'Which loop runs at least once?',
 'for', 'while', 'do-while', 'foreach',
 'do-while'),

(4, '10-15', 'What does HTML stand for?',
 'Hyper Text Markup Language', 'High Text Machine Language',
 'Hyperlinks Text Mark Language', 'Hyper Tool Markup Language',
 'Hyper Text Markup Language'),

(4, '10-15', 'Which operator is used for equality?',
 '=', '==', '!=', '<>',
 '=='),

(4, '10-15', 'Which storage is faster?',
 'Hard Disk', 'RAM', 'SSD', 'Pen Drive',
 'SSD'),

(4, '10-15', 'Which tag is used for a button in HTML?',
 '<btn>', '<button>', '<input>', '<click>',
 '<button>'),

(4, '10-15', 'What is the extension of Python files?',
 '.pt', '.py', '.python', '.pyt',
 '.py');

INSERT INTO questions
(category_id, age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
(4, '16-24', 'Time complexity of binary search?',
 'O(n)', 'O(log n)', 'O(n log n)', 'O(1)',
 'O(log n)'),

(4, '16-24', 'Which normal form removes transitive dependency?',
 '1NF', '2NF', '3NF', 'BCNF',
 '3NF'),

(4, '16-24', 'Which data structure is used in BFS?',
 'Stack', 'Queue', 'Heap', 'Tree',
 'Queue'),

(4, '16-24', 'Deadlock occurs when?',
 'CPU idle', 'Processes wait indefinitely',
 'Memory overflow', 'Disk failure',
 'Processes wait indefinitely'),

(4, '16-24', 'Which scheduling algorithm may cause starvation?',
 'FCFS', 'Round Robin', 'Priority Scheduling', 'FIFO',
 'Priority Scheduling'),

(4, '16-24', 'Which SQL join returns all records?',
 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN',
 'FULL OUTER JOIN'),

(4, '16-24', 'What is polymorphism?',
 'One class many objects', 'Many forms of same function',
 'Multiple inheritance', 'Data hiding',
 'Many forms of same function'),

(4, '16-24', 'Which is NOT ACID property?',
 'Atomicity', 'Consistency', 'Isolation', 'Availability',
 'Availability'),

(4, '16-24', 'Which algorithm is used in shortest path?',
 'DFS', 'BFS', 'Dijkstra', 'Merge Sort',
 'Dijkstra'),

(4, '16-24', 'Which layer handles encryption in OSI?',
 'Network', 'Transport', 'Session', 'Presentation',
 'Presentation'),
 
 (4, '16-24', 'What is recursion?',
 'Loop inside loop', 'Function calling itself',
 'Infinite loop', 'Conditional loop',
 'Function calling itself');

INSERT INTO questions 
(category_id,age_group, question_text, option1, option2, option3, option4, correct_option)
VALUES
('4','25+','Which problem is NOT known to be NP-Complete?',
 'Traveling Salesman Problem','Boolean Satisfiability Problem','Shortest Path Problem','Vertex Cover','Shortest Path Problem'),

('4','25+','Which scheduling algorithm may cause starvation?',
 'Round Robin','First Come First Serve','Shortest Job First','Multilevel Queue','Shortest Job First'),

('4','25+','Which memory allocation technique suffers from external fragmentation?',
 'Paging','Segmentation','Hashing','Virtual Memory','Segmentation'),

('4','25+','Which normal form eliminates transitive dependency?',
 '1NF','2NF','3NF','4NF','3NF'),

('4','25+','Which data structure is used internally by recursion?',
 'Queue','Heap','Stack','Graph','Stack'),

('4','25+','What is the worst-case time complexity of Quick Sort?',
 'O(n log n)','O(log n)','O(n)','O(n^2)','O(n^2)'),

('4','25+','Which page replacement algorithm suffers from Belady’s anomaly?',
 'LRU','Optimal','FIFO','LFU','FIFO'),

('4','25+','Which protocol resolves IP address to MAC address?',
 'RARP','DNS','ARP','ICMP','ARP'),

('4','25+','Which is NOT a deadlock condition?',
 'Mutual Exclusion','Hold and Wait','Preemption','Circular Wait','Preemption'),

('4','25+','Which traversal of BST gives sorted output?',
 'Preorder','Postorder','Level Order','Inorder','Inorder');
