CREATE TABLE "Proposals" (
    "ProposalID" INTEGER,
    "Title" TEXT NOT NULL,
    "ProjectType" TEXT,
    "Genre" TEXT,
    "Duration" INTEGER,
    "Desc" TEXT,
    "Budget" REAL,
    "SubmittedBy" TEXT,
    "Status" TEXT DEFAULT 'Pending Validation',
    PRIMARY KEY("ProposalID" AUTOINCREMENT),
    FOREIGN KEY("SubmittedBy") REFERENCES "Users"("Username") ON DELETE CASCADE
);

CREATE TABLE "Users" (
    "UserID" INTEGER,
    "FirstName" NUMERIC NOT NULL,
    "LastName" TEXT NOT NULL,
    "Sex" TEXT CHECK("Sex" IN ('M', 'F')),
    "DOB" DATE,
    "Email" TEXT NOT NULL UNIQUE,
    "Username" TEXT UNIQUE,
    "HashedPassword" TEXT,
    "UserType" TEXT NOT NULL CHECK("UserType" IN ('Admin', 'Creator', 'Freelancer')),
    PRIMARY KEY("UserID" AUTOINCREMENT)
);

CREATE TABLE "AuditLogs" (
    "LogID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "ProjectID" INTEGER,
    "ChangeType" TEXT,
    "OldValue" TEXT,
    "NewValue" TEXT,
    "Timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("ProjectID") REFERENCES "Projects"("ProjectID")
);

CREATE TABLE "Payroll" (
    "PayrollID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserID" INTEGER NOT NULL,
    "GrossPay" REAL NOT NULL,
    "TaxDeduction" REAL DEFAULT 0.0,
    "NationalInsurance" REAL DEFAULT 0.0,
    "PensionContribution" REAL DEFAULT 0.0,
    "OtherDeductions" REAL DEFAULT 0.0,
    "NetPay" REAL GENERATED ALWAYS AS (GrossPay - (TaxDeduction + NationalInsurance + PensionContribution + OtherDeductions)) VIRTUAL,
    "Status" TEXT DEFAULT 'Pending' CHECK("Status" IN ('Paid', 'Pending', 'Cancelled')),
    FOREIGN KEY("UserID") REFERENCES "Users"("UserID")
);

CREATE TABLE "ParticipationLedger" (
    "TransactionID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "ProjectID" INTEGER NOT NULL,
    "UserID" INTEGER NOT NULL,
    "PaymentType" TEXT NOT NULL CHECK("PaymentType" IN ('Bonus', 'Equity_Payout', 'Flat_Fee')),
    "Amount" REAL NOT NULL,
    "Timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("ProjectID") REFERENCES "Projects"("ProjectID"),
    FOREIGN KEY("UserID") REFERENCES "Users"("UserID")
);

CREATE TABLE "Projects" (
    "ProjectID" INTEGER,
    "ProjectName" TEXT NOT NULL,
    "ProjectType" TEXT NOT NULL CHECK("ProjectType" IN ('TV Series', 'Film')),
    "Desc" TEXT,
    "Genre" TEXT NOT NULL CHECK("Genre" IN ('Action', 'Anthology', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Documentary', 'Game Show', 'Sci-Fi')),
    "Status" TEXT NOT NULL CHECK("Status" IN ('Not Started', 'Filming and Production', 'Approved')),
    "Budget" REAL NOT NULL,
    "StartDate" DATE,
    "ExpectedEndDate" DATE,
    PRIMARY KEY("ProjectID" AUTOINCREMENT)
);

CREATE TABLE "Niches" (
    "NicheID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NicheName" TEXT UNIQUE NOT NULL
); 


-- ====================================================================
-- 1. INSERT STATEMENTS FOR THE 'Niches' TABLE
-- ====================================================================
INSERT INTO "Niches" ("NicheName") VALUES 
('Lifestyle'),
('Food'),
('Fashion'),
('Comedy'),
('Art'),
('Tech');

-- ====================================================================
-- 2. INSERT STATEMENTS FOR THE 'Users' TABLE
-- ====================================================================
INSERT INTO "Users" ("FirstName", "LastName", "Sex", "DOB", "Email", "Username", "UserType") VALUES 
-- Admins
('Daniel', 'Onyeakazi', NULL, NULL, 'daniel@encrypt.com', 'do3005', 'Admin'),
('Willow', 'Youn', NULL, NULL, 'willow@encrypt.com', NULL, 'Admin'),
('Jade', 'Zhang', NULL, NULL, 'jade@encrypt.com', NULL, 'Admin'),
('Angela', 'Keith', NULL, NULL, 'angela@encrypt.com', NULL, 'Admin'),
('Sven', 'Talefson', NULL, NULL, 'sven@encrypt.com', NULL, 'Admin'),
('Teni', 'Olayinka', NULL, NULL, 'teni@encrypt.com', NULL, 'Admin'),
('Griff', 'Lawson', NULL, NULL, 'griff@encrypt.com', NULL, 'Admin'),

-- Creators
('Alex', 'Crimson', NULL, NULL, 'a.crimson@encrypt.com', 'acronims', 'Creator'),
('Michela', 'Giordano', NULL, '2007-09-07', 'm.gior@encrypt.com', NULL, 'Creator'),
('Will', 'Keith', NULL, '2006-02-01', 'w.kieth@encrypt.com', NULL, 'Creator'),
('Sarah', 'Tall', NULL, '2006-08-20', 's.tall@encrypt.com', NULL, 'Creator'),
('Ji-hyun', 'Lee', NULL, '2000-02-04', 'j.lee@encrypt.com', NULL, 'Creator'),
('Luca', 'Evels', NULL, '2005-10-18', 'l.evels@encrypt.com', NULL, 'Creator'),
('Yas', 'Ahava', NULL, '1998-09-24', 'y.ahava@encrypt.com', NULL, 'Creator'),
('Chiara', 'Riso', NULL, '2004-05-21', 'c.riso@encrypt.com', NULL, 'Creator'),
('Jason', 'Wang', NULL, '1998-04-09', 'j.wang@encrypt.com', NULL, 'Creator'),
('Henry', 'Draper', NULL, '2002-02-25', 'h.draper@encrypt.com', NULL, 'Creator'),
('Ilana', 'Raj', NULL, '2004-07-14', 'i.raj@encrypt.com', NULL, 'Creator'),
('Adrian', 'Rossi', NULL, '2000-04-28', 'a.rossi@encrypt.com', NULL, 'Creator'),
('Grace', 'Venn', NULL, '2003-08-19', 'g.venn@encrypt.com', NULL, 'Creator'),

-- Freelancers
('Jack', 'Edison', NULL, NULL, 'j.edison@encrypt.com', NULL, 'Freelancer'),
('Michael', 'Wong-Martinez', NULL, NULL, 'm.wong-martinez@encrypt.com', NULL, 'Freelancer'),
('Lily', 'Tall', NULL, NULL, 'l.tall@encrypt.com', NULL, 'Freelancer'),
('Tyler', 'Watt', NULL, NULL, 't.watt@encrypt.com', NULL, 'Freelancer'),
('Lucy', 'Evans', NULL, NULL, 'l.evans@encrypt.com', NULL, 'Freelancer'),
('Avery', 'Ferreira', NULL, NULL, 'a.ferreira@encrypt.com', NULL, 'Freelancer'),
('Pamela', 'Gray', NULL, NULL, 'p.gray@encrypt.com', NULL, 'Freelancer'),
('Grayson', 'Renn', NULL, NULL, 'g.renn@encrypt.com', NULL, 'Freelancer'),
('Winona', 'Lough', NULL, NULL, 'w.lough@encrypt.com', NULL, 'Freelancer'),
('Allison', 'Drake', NULL, NULL, 'a.drake@encrypt.com', NULL, 'Freelancer'),
('Kieran', 'Reel', NULL, NULL, 'k.reel@encrypt.com', NULL, 'Freelancer'),
('Chidi', 'Okonkwo', NULL, NULL, 'c.okonkwo@encrypt.com', NULL, 'Freelancer'),
('Samantha', 'Rye', NULL, NULL, 's.rye@encrypt.com', NULL, 'Freelancer');