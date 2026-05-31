
CREATE DATABASE GymManagement;

-- Use the Database
USE GymManagement;


-- Create Members Table


CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT , 
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(15),
    MembershipStartDate DATE NOT NULL,
    MembershipEndDate DATE NOT NULL
);

---------------------------------------------------
-- Create Trainers Table
---------------------------------------------------

CREATE TABLE Trainers (
    TrainerID INT PRIMARY KEY AUTO_INCREMENT , 
    Name VARCHAR(100) NOT NULL,
    Specialty VARCHAR(100),
    Email VARCHAR(100) UNIQUE NOT NULL
);

---------------------------------------------------
-- Create Fitness Programs Table
---------------------------------------------------

CREATE TABLE FitnessPrograms (
    ProgramID INT PRIMARY KEY AUTO_INCREMENT , 
    ProgramName VARCHAR(100) NOT NULL,
    DurationInWeeks INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL
);

---------------------------------------------------
-- Indexing
---------------------------------------------------

-- Create index on MembershipEndDate
CREATE INDEX idx_membership_end
ON Members(MembershipEndDate);

---------------------------------------------------
-- Insert Data into Members Table
---------------------------------------------------

INSERT INTO Members
(Name, Email, PhoneNumber, MembershipStartDate, MembershipEndDate)

VALUES
('Alice Smith', 'alice.smith@example.com', '1234567890', '2023-01-01', '2024-01-01'),

('Bob Johnson', 'bob.johnson@example.com', '2345678901', '2023-02-01', '2024-02-01'),

('Charlie Brown', 'charlie.brown@example.com', '3456789012', '2023-03-01', '2024-03-01');

---------------------------------------------------
-- Insert Data into Trainers Table
---------------------------------------------------

INSERT INTO Trainers
(Name, Specialty, Email)

VALUES
('John Doe', 'Weightlifting', 'john.doe@example.com'),

('Jane Smith', 'Yoga', 'jane.smith@example.com'),

('Mike Lee', 'Cardio', 'mike.lee@example.com');

---------------------------------------------------
-- Add New Fitness Programs
---------------------------------------------------

INSERT INTO FitnessPrograms
(ProgramName, DurationInWeeks, Price)

VALUES
('Yoga Basics', 8, 150.00),

('Advanced Weightlifting', 12, 250.00),

('Cardio Blast', 6, 100.00);

---------------------------------------------------
-- CRUD OPERATIONS
---------------------------------------------------

-- Retrieve All Members
SELECT * FROM Members;

-- Retrieve All Trainers
SELECT * FROM Trainers;

-- Retrieve All Fitness Programs
SELECT * FROM FitnessPrograms;

---------------------------------------------------
-- Retrieve Members with Trainers and Programs
---------------------------------------------------

SELECT
    m.Name AS MemberName,
    t.Name AS TrainerName,
    p.ProgramName

FROM Attendance a

JOIN Members m
ON a.MemberID = m.MemberID

JOIN Trainers t
ON a.TrainerID = t.TrainerID

JOIN FitnessPrograms p
ON a.ProgramID = p.Program ID;

---------------------------------------------------
-- Retrieve Attendance Records
---------------------------------------------------

SELECT
    a.AttendanceDate,
    m.Name AS MemberName,
    t.Name AS TrainerName,
    p.ProgramName

FROM Attendance a

JOIN Members m
ON a.MemberID = m.MemberID

JOIN Trainers t
ON a.TrainerID = t.TrainerID

JOIN FitnessPrograms p
ON a.ProgramID = p.ProgramID;

---------------------------------------------------
-- Update Member Phone Number
---------------------------------------------------

UPDATE Members
SET PhoneNumber = '0987654321'
WHERE MemberID = 1;

---------------------------------------------------
-- Update Trainer Specialty
---------------------------------------------------

UPDATE Trainers
SET Specialty = 'Pilates'
WHERE TrainerID = 2;

---------------------------------------------------
-- Update Fitness Program Price
---------------------------------------------------

UPDATE FitnessPrograms
SET Price = 175.00
WHERE ProgramID = 1;

---------------------------------------------------
-- Update Membership End Date
---------------------------------------------------

UPDATE Members
SET MembershipEndDate = '2024-06-01'
WHERE MemberID = 2;

---------------------------------------------------
-- Delete Members with Expired Membership
---------------------------------------------------

DELETE FROM Members
WHERE MembershipEndDate < GETDATE();
---------------------------------------------------
-- Delete a Cancelled Fitness Program
---------------------------------------------------

DELETE FROM FitnessPrograms
WHERE ProgramID = 2;
-- Assuming this program is cancelled

---------------------------------------------------
-- VIEWS
---------------------------------------------------

-- Create View for Membership Details

CREATE VIEW MembershipDetails AS

SELECT
    m.MemberID,
    m.Name,
    m.Email,
    m.MembershipStartDate,
    m.MembershipEndDate

FROM Members m;

---------------------------------------------------
-- Create View for Trainer Schedules
---------------------------------------------------

CREATE VIEW TrainerSchedules AS

SELECT
    t.TrainerID,
    t.Name AS TrainerName,
    a.AttendanceDate,
    m.Name AS MemberName,
    p.ProgramName

FROM Attendance a

JOIN Trainers t
ON a.TrainerID = t.TrainerID

JOIN Members m
ON a.MemberID = m.MemberID

JOIN FitnessPrograms p
ON a.ProgramID = p.ProgramID;

---------------------------------------------------
-- TRIGGER
---------------------------------------------------
--++++--
-- Trigger for Membership Renewal Reminder
CREATE TRIGGER MembershipRenewalReminder
ON Members
AFTER INSERT
AS
BEGIN
    DECLARE @msg VARCHAR(255);
    DECLARE @MemberName VARCHAR(100);
    DECLARE @MembershipEndDate DATE;



    -- Get Newly Inserted Member Details

    SELECT
        @MemberName = Name,
        @MembershipEndDate = MembershipEndDate

    FROM inserted;
    -- 'inserted' stores newly added rows

    SET @msg = CONCAT(
    'Reminder: Your membership for ',
    @MemberName,
    ' is expiring on ',
    @MembershipEndDate
);

-- Placeholder for Email / Notification

SELECT @msg;

END $$----++-- problrm acha 
