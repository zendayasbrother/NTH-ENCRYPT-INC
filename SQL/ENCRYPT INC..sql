BEGIN;

-- ====================================================================
-- 1. INITIALIZE SCHEMA ENVIRONMENT & FORCE PATHS
-- ====================================================================
CREATE SCHEMA IF NOT EXISTS "Notation";
SET search_path TO "Notation", public;

DROP TABLE IF EXISTS "Notation"."RightsIPRegistry" CASCADE;
DROP TABLE IF EXISTS "Notation"."Contracts" CASCADE;
DROP TABLE IF EXISTS "Notation"."Notifications" CASCADE;
DROP TABLE IF EXISTS "Notation"."AuditLogs" CASCADE;
DROP TABLE IF EXISTS "Notation"."Payroll" CASCADE;
DROP TABLE IF EXISTS "Notation"."ParticipationLedger" CASCADE;
DROP TABLE IF EXISTS "Notation"."Payments" CASCADE;
DROP TABLE IF EXISTS "Notation"."Assets" CASCADE;
DROP TABLE IF EXISTS "Notation"."Deliverables" CASCADE;
DROP TABLE IF EXISTS "Notation"."Tasks" CASCADE;
DROP TABLE IF EXISTS "Notation"."Pods" CASCADE;
DROP TABLE IF EXISTS "Notation"."Proposals" CASCADE;
DROP TABLE IF EXISTS "Notation"."Niches" CASCADE;
DROP TABLE IF EXISTS "Notation"."Projects" CASCADE;
DROP TABLE IF EXISTS "Notation"."Users" CASCADE;
DROP TABLE IF EXISTS "Notation"."Countries" CASCADE;

-- ====================================================================
-- 2. CREATE MASTER REFERENCE DATA TABLES
-- ====================================================================
CREATE TABLE "Notation"."Countries" (
    "CountryID" SERIAL PRIMARY KEY,
    "Country" TEXT NOT NULL UNIQUE,
    "Currency" VARCHAR(3) NOT NULL,
    "TaxRate" NUMERIC(5, 2) DEFAULT 0.00,
    "OpenFiscaID" TEXT
);

CREATE TABLE "Notation"."Users" (
    "UserID" SERIAL PRIMARY KEY,
    "Username" TEXT UNIQUE, 
    "FirstName" TEXT NOT NULL,
    "LastName" TEXT NOT NULL,
    "Sex" TEXT CHECK ("Sex" IN ('M', 'F')),             
    "DOB" DATE,
    "Email" TEXT NOT NULL UNIQUE,
    "HashedPassword" TEXT,
    "UserType" TEXT NOT NULL CHECK ("UserType" IN ('Admin', 'Creator', 'Freelancer')),
    "CountryID" INTEGER REFERENCES "Notation"."Countries"("CountryID") ON DELETE SET NULL,
    "Active" BOOLEAN DEFAULT TRUE
);

CREATE TABLE "Notation"."Projects" (
    "ProjectID" SERIAL PRIMARY KEY,
    "ProjectType" TEXT NOT NULL CHECK ("ProjectType" IN ('TV Series', 'Film')),
    "Title" TEXT NOT NULL,
    "Description" TEXT,
    "Genre" TEXT NOT NULL CHECK ("Genre" IN ('Action', 'Anthology', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Documentary', 'Game Show', 'Sci-Fi')),
    "TargetAudience" TEXT,
    "Budget" NUMERIC(12, 2) NOT NULL CHECK ("Budget" <= 500000.00), 
    "ProductionCosts" NUMERIC(12, 2) DEFAULT 0.00,
    "GrossRevenue" NUMERIC(12, 2) DEFAULT 0.00,
    "Phase" TEXT NOT NULL CHECK ("Phase" IN ('Not Started', 'Filming and Production', 'Approved')),
    "Status" TEXT DEFAULT 'Active',
    "StartDate" DATE,
    "EndDate" DATE,
    "ReleaseDate" DATE,
    "ROI" NUMERIC(12, 2) GENERATED ALWAYS AS (
        CASE WHEN "ProductionCosts" > 0 
             THEN ("GrossRevenue" - "ProductionCosts") / "ProductionCosts" 
             ELSE 0.00 
        END
    ) STORED
);

CREATE TABLE "Notation"."Niches" (
    "NicheID" SERIAL PRIMARY KEY,
    "NicheName" TEXT UNIQUE NOT NULL
);

-- ====================================================================
-- 3. CREATE OPERATION & PIPELINE TABLES
-- ====================================================================
CREATE TABLE "Notation"."Proposals" (
    "ProposalID" SERIAL PRIMARY KEY,
    "Title" TEXT NOT NULL,
    "Description" TEXT,
    "Genre" TEXT,
    "ProjectType" TEXT,
    "EstBudget" NUMERIC(12, 2),
    "EstRuntime" INTEGER, 
    "SubmittedBy" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "Status" TEXT DEFAULT 'Pending Validation',
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Notation"."Pods" (
    "PodID" SERIAL PRIMARY KEY,
    "AdminID" INTEGER REFERENCES "Notation"."Users"("UserID") ON DELETE RESTRICT,
    "CreatorID" INTEGER REFERENCES "Notation"."Users"("UserID") ON DELETE RESTRICT,
    "FreelancerID" INTEGER REFERENCES "Notation"."Users"("UserID") ON DELETE SET NULL, 
    "ProjectID" INTEGER UNIQUE REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);

CREATE TABLE "Notation"."Tasks" (
    "TaskID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER NOT NULL REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
    "AssignedUser" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
    "Title" TEXT NOT NULL,
    "Description" TEXT,
    "Priority" TEXT CHECK ("Priority" IN ('Low', 'Medium', 'High', 'Critical')),
    "Status" TEXT DEFAULT 'Pending' CHECK ("Status" IN ('Pending', 'In Progress', 'Blocked', 'Completed')),
    "Deadline" DATE,
    "CompletedAt" TIMESTAMP
);

CREATE TABLE "Notation"."Deliverables" (
    "DeliverableID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER NOT NULL REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
    "Title" TEXT NOT NULL,
    "AssignedUser" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
    "Status" TEXT DEFAULT 'Awaiting Asset' CHECK ("Status" IN ('Awaiting Asset', 'Under Review', 'Approved')),
    "DueDate" DATE
);

CREATE TABLE "Notation"."Assets" (
    "AssetID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER NOT NULL REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
    "AssetType" TEXT NOT NULL, 
    "Version" VARCHAR(10) DEFAULT 'v1.0',
    "Owner" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
    "FileLocation" TEXT NOT NULL,
    "UploadDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- 4. CREATE FINANCIALS & REVENUE DISTRIBUTIONS
-- ====================================================================
CREATE TABLE "Notation"."Payments" (
    "PaymentID" SERIAL PRIMARY KEY,
    "Username" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "ProjectID" INTEGER REFERENCES "Notation"."Projects"("ProjectID") ON DELETE SET NULL,
    "PaymentType" TEXT CHECK ("PaymentType" IN ('Escrow Deposit', 'Flat Fee', 'Bonus Drawdown', 'Refund')),
    "Amount" NUMERIC(12, 2) NOT NULL,
    "Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Notation"."ParticipationLedger" (
    "TransactionID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER NOT NULL REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
    "Username" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "PaymentType" TEXT NOT NULL CHECK ("PaymentType" IN ('Bonus', 'Equity_Payout', 'Flat_Fee')),
    "Amount" NUMERIC(12, 2) NOT NULL,
    "ProjectBalance" NUMERIC(12, 2) DEFAULT 0.00,
    "RecoupmentThreshold" NUMERIC(12, 2) DEFAULT 0.00,
    "Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Notation"."Payroll" (
    "PayrollID" SERIAL PRIMARY KEY,
    "Username" TEXT UNIQUE REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "GrossPay" NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    "Tax" NUMERIC(12, 2) DEFAULT 0.00,
    "Insurance" NUMERIC(12, 2) DEFAULT 0.00,
    "PensionContribution" NUMERIC(12, 2) DEFAULT 0.00,
    "OtherDeductions" NUMERIC(12, 2) DEFAULT 0.00,
    "NetPay" NUMERIC(12, 2) GENERATED ALWAYS AS ("GrossPay" - ("Tax" + "Insurance" + "PensionContribution" + "OtherDeductions")) STORED,
    "Bonus" NUMERIC(12, 2) DEFAULT 0.00,
    "PhantomEquity" NUMERIC(5, 4) DEFAULT 0.0000,
    "Status" TEXT DEFAULT 'Pending' CHECK ("Status" IN ('Paid', 'Pending', 'Cancelled'))
);

-- ====================================================================
-- 5. LEGAL CONTROLLERS, AUDITS, AND LOGISTICS
-- ====================================================================
CREATE TABLE "Notation"."Contracts" (
    "ContractID" SERIAL PRIMARY KEY,
    "Username" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "StartDate" DATE NOT NULL,
    "EndDate" DATE NOT NULL,
    "RevenueSplit" NUMERIC(4, 3) DEFAULT 0.800, 
    "OwnershipShare" NUMERIC(4, 3) DEFAULT 0.750, 
    "Signed" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "Notation"."RightsIPRegistry" (
    "RegistryID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER UNIQUE REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
    "AgencyShare" NUMERIC(4, 3) DEFAULT 0.250, 
    "TalentShare" NUMERIC(4, 3) DEFAULT 0.750, 
    "Territory" VARCHAR(50) DEFAULT 'Worldwide',
    "LicenceType" TEXT DEFAULT '7-Year Master Lease',
    "Expiry" DATE
);

CREATE TABLE "Notation"."AuditLogs" (
    "LogID" SERIAL PRIMARY KEY,
    "ProjectID" INTEGER REFERENCES "Notation"."Projects"("ProjectID") ON DELETE SET NULL,
    "TableAffected" TEXT,
    "ChangeType" TEXT NOT NULL,
    "OldValue" TEXT,
    "NewValue" TEXT,
    "Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Notation"."Notifications" (
    "NotificationID" SERIAL PRIMARY KEY,
    "User" TEXT REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE,
    "Message" TEXT NOT NULL,
    "Status" TEXT DEFAULT 'Unread' CHECK ("Status" IN ('Unread', 'Read')),
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- 6. DATA POPULATION
-- ====================================================================
INSERT INTO "Notation"."Niches" ("NicheName") VALUES ('Lifestyle'), ('Food'), ('Fashion'), ('Comedy'), ('Art'), ('Tech');

INSERT INTO "Notation"."Users" ("FirstName", "LastName", "Sex", "DOB", "Email", "Username", "UserType") VALUES 
('Daniel', 'Onyeakazi', 'M', NULL, 'daniel@nth.com', 'do3005', 'Admin'),
('Willow', 'Youn', 'F', NULL, 'willow@nth.com', NULL, 'Admin'),
('Jade', 'Zhang', 'F', NULL, 'jade@nth.com', NULL, 'Admin'),
('Angela', 'Keith', 'F', NULL, 'angela@nth.com', NULL, 'Admin'),
('Sven', 'Talefson', 'M', NULL, 'sven@nth.com', NULL, 'Admin'),
('Teni', 'Olayinka', 'F', NULL, 'teni@nth.com', NULL, 'Admin'),
('Griff', 'Lawson', 'M', NULL, 'griff@nth.com', NULL, 'Admin'),
('Alex', 'Crimson', 'M', NULL, 'a.crimson@nth.com', 'acronims', 'Creator'),
('Michela', 'Giordano', 'F', '2007-09-07', 'm.gior@nth.com', NULL, 'Creator'),
('Will', 'Keith', 'M', '2006-02-01', 'w.kieth@nth.com', NULL, 'Creator'),
('Sarah', 'Tall', 'F', '2006-08-20', 's.tall@nth.com', NULL, 'Creator'),
('Ji-hyun', 'Lee', 'F', '2000-02-04', 'j.lee@nth.com', NULL, 'Creator'),
('Luca', 'Evels', 'M', '2005-10-18', 'l.evels@nth.com', NULL, 'Creator'),
('Yas', 'Ahava', 'M', '1998-09-24', 'y.ahava@nth.com', NULL, 'Creator'),
('Chiara', 'Riso', 'F', '2004-05-21', 'c.riso@nth.com', NULL, 'Creator'),
('Jason', 'Wang', 'M', '1998-04-09', 'j.wang@nth.com', NULL, 'Creator'),
('Henry', 'Draper', 'M', '2002-02-25', 'h.draper@nth.com', NULL, 'Creator'),
('Ilana', 'Raj', 'F', '2004-07-14', 'i.raj@nth.com', NULL, 'Creator'),
('Adrian', 'Rossi', 'M', '2000-04-28', 'a.rossi@nth.com', NULL, 'Creator'),
('Grace', 'Venn', 'F', '2003-08-19', 'g.venn@nth.com', NULL, 'Creator'),
('Jack', 'Edison', 'M', NULL, 'j.edison@nth.com', NULL, 'Freelancer'),
('Michael', 'Wong-Martinez', 'M', NULL, 'm.wong-martinez@nth.com', NULL, 'Freelancer'),
('Lily', 'Tall', 'F', NULL, 'l.tall@nth.com', NULL, 'Freelancer'),
('Tyler', 'Watt', 'M', NULL, 't.watt@nth.com', NULL, 'Freelancer'),
('Lucy', 'Evans', 'F', NULL, 'l.evans@nth.com', NULL, 'Freelancer'),
('Avery', 'Ferreira', 'F', NULL, 'a.ferreira@nth.com', NULL, 'Freelancer'),
('Pamela', 'Gray', 'F', NULL, 'p.gray@nth.com', NULL, 'Freelancer'),
('Grayson', 'Renn', 'M', NULL, 'g.renn@nth.com', NULL, 'Freelancer'),
('Winona', 'Lough', 'F', NULL, 'w.lough@nth.com', NULL, 'Freelancer'),
('Allison', 'Drake', 'F', NULL, 'a.drake@nth.com', NULL, 'Freelancer'),
('Kieran', 'Reel', 'M', NULL, 'k.reel@nth.com', NULL, 'Freelancer'),
('Chidi', 'Okonkwo', 'M', NULL, 'c.okonkwo@nth.com', NULL, 'Freelancer'),
('Samantha', 'Rye', 'F', NULL, 's.rye@nth.com', NULL, 'Freelancer');

COMMIT;