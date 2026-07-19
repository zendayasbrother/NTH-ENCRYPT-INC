BEGIN;

-- "Notation"."Countries" definition

-- Drop table

-- DROP TABLE "Notation"."Countries";

CREATE TABLE "Notation"."Countries" (
	"CountryID" serial4 NOT NULL,
	"Country" text NOT NULL,
	"Currency" varchar(3) NOT NULL,
	"TaxRate" numeric(5, 2) DEFAULT 0.00 NULL,
	"OpenFiscaID" text NULL,
	CONSTRAINT "Countries_Country_key" UNIQUE ("Country"),
	CONSTRAINT "Countries_pkey" PRIMARY KEY ("CountryID")
);


-- "Notation"."Niches" definition

-- Drop table

-- DROP TABLE "Notation"."Niches";

CREATE TABLE "Notation"."Niches" (
	"NicheID" serial4 NOT NULL,
	"NicheName" text NOT NULL,
	CONSTRAINT "Niches_NicheName_key" UNIQUE ("NicheName"),
	CONSTRAINT "Niches_pkey" PRIMARY KEY ("NicheID")
);


-- "Notation"."Projects" definition

-- Drop table

-- DROP TABLE "Notation"."Projects";

CREATE TABLE "Notation"."Projects" (
	"ProjectID" serial4 NOT NULL,
	"ProjectType" text NOT NULL,
	"Title" text NOT NULL,
	"Description" text NULL,
	"Genre" text NOT NULL,
	"TargetAudience" text NULL,
	"Budget" numeric(12, 2) NOT NULL,
	"ProductionCosts" numeric(12, 2) DEFAULT 0.00 NULL,
	"GrossRevenue" numeric(12, 2) DEFAULT 0.00 NULL,
	"Phase" text NOT NULL,
	"Status" text DEFAULT 'Active'::text NULL,
	"StartDate" date NULL,
	"EndDate" date NULL,
	"ReleaseDate" date NULL,
	"ROI" numeric(12, 2) GENERATED ALWAYS AS (
CASE
    WHEN "ProductionCosts" > 0::numeric THEN ("GrossRevenue" - "ProductionCosts") / "ProductionCosts"
    ELSE 0.00
END) STORED NULL,
	CONSTRAINT "Projects_Budget_check" CHECK (("Budget" <= 500000.00)),
	CONSTRAINT "Projects_Genre_check" CHECK (("Genre" = ANY (ARRAY['Action'::text, 'Anthology'::text, 'Comedy'::text, 'Drama'::text, 'Fantasy'::text, 'Horror'::text, 'Documentary'::text, 'Game Show'::text, 'Sci-Fi'::text]))),
	CONSTRAINT "Projects_Phase_check" CHECK (("Phase" = ANY (ARRAY['Not Started'::text, 'Filming and Production'::text, 'Approved'::text]))),
	CONSTRAINT "Projects_ProjectType_check" CHECK (("ProjectType" = ANY (ARRAY['TV Series'::text, 'Film'::text]))),
	CONSTRAINT "Projects_pkey" PRIMARY KEY ("ProjectID")
);


-- "Notation"."AuditLogs" definition

-- Drop table

-- DROP TABLE "Notation"."AuditLogs";

CREATE TABLE "Notation"."AuditLogs" (
	"LogID" serial4 NOT NULL,
	"ProjectID" int4 NULL,
	"TableAffected" text NULL,
	"ChangeType" text NOT NULL,
	"OldValue" text NULL,
	"NewValue" text NULL,
	"Timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "AuditLogs_pkey" PRIMARY KEY ("LogID"),
	CONSTRAINT "AuditLogs_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE SET NULL
);


-- "Notation"."RightsIPRegistry" definition

-- Drop table

-- DROP TABLE "Notation"."RightsIPRegistry";

CREATE TABLE "Notation"."RightsIPRegistry" (
	"RegistryID" serial4 NOT NULL,
	"ProjectID" int4 NULL,
	"AgencyShare" numeric(4, 3) DEFAULT 0.250 NULL,
	"TalentShare" numeric(4, 3) DEFAULT 0.750 NULL,
	"Territory" varchar(50) DEFAULT 'Worldwide'::character varying NULL,
	"LicenceType" text DEFAULT '7-Year Master Lease'::text NULL,
	"Expiry" date NULL,
	CONSTRAINT "RightsIPRegistry_ProjectID_key" UNIQUE ("ProjectID"),
	CONSTRAINT "RightsIPRegistry_pkey" PRIMARY KEY ("RegistryID"),
	CONSTRAINT "RightsIPRegistry_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);


-- "Notation"."Users" definition

-- Drop table

-- DROP TABLE "Notation"."Users";

CREATE TABLE "Notation"."Users" (
	"UserID" serial4 NOT NULL,
	"Username" text NULL,
	"FirstName" text NOT NULL,
	"LastName" text NOT NULL,
	"Sex" text NULL,
	"DOB" date NULL,
	"Email" text NOT NULL,
	"HashedPassword" text NULL,
	"UserType" text NOT NULL,
	"CountryID" int4 NULL,
	"Active" bool DEFAULT true NULL,
	CONSTRAINT "Users_Email_key" UNIQUE ("Email"),
	CONSTRAINT "Users_Sex_check" CHECK (("Sex" = ANY (ARRAY['M'::text, 'F'::text]))),
	CONSTRAINT "Users_UserType_check" CHECK (("UserType" = ANY (ARRAY['Admin'::text, 'Creator'::text, 'Freelancer'::text]))),
	CONSTRAINT "Users_Username_key" UNIQUE ("Username"),
	CONSTRAINT "Users_pkey" PRIMARY KEY ("UserID"),
	CONSTRAINT "Users_CountryID_fkey" FOREIGN KEY ("CountryID") REFERENCES "Notation"."Countries"("CountryID") ON DELETE SET NULL
);


-- "Notation"."Assets" definition

-- Drop table

-- DROP TABLE "Notation"."Assets";

CREATE TABLE "Notation"."Assets" (
	"AssetID" serial4 NOT NULL,
	"ProjectID" int4 NOT NULL,
	"AssetType" text NOT NULL,
	"Version" varchar(10) DEFAULT 'v1.0'::character varying NULL,
	"Owner" text NULL,
	"FileLocation" text NOT NULL,
	"UploadDate" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "Assets_pkey" PRIMARY KEY ("AssetID"),
	CONSTRAINT "Assets_Owner_fkey" FOREIGN KEY ("Owner") REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
	CONSTRAINT "Assets_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);


-- "Notation"."Contracts" definition

-- Drop table

-- DROP TABLE "Notation"."Contracts";

CREATE TABLE "Notation"."Contracts" (
	"ContractID" serial4 NOT NULL,
	"Username" text NULL,
	"StartDate" date NOT NULL,
	"EndDate" date NOT NULL,
	"RevenueSplit" numeric(4, 3) DEFAULT 0.800 NULL,
	"OwnershipShare" numeric(4, 3) DEFAULT 0.750 NULL,
	"Signed" bool DEFAULT false NULL,
	CONSTRAINT "Contracts_pkey" PRIMARY KEY ("ContractID"),
	CONSTRAINT "Contracts_Username_fkey" FOREIGN KEY ("Username") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."Deliverables" definition

-- Drop table

-- DROP TABLE "Notation"."Deliverables";

CREATE TABLE "Notation"."Deliverables" (
	"DeliverableID" serial4 NOT NULL,
	"ProjectID" int4 NOT NULL,
	"Title" text NOT NULL,
	"AssignedUser" text NULL,
	"Status" text DEFAULT 'Awaiting Asset'::text NULL,
	"DueDate" date NULL,
	CONSTRAINT "Deliverables_Status_check" CHECK (("Status" = ANY (ARRAY['Awaiting Asset'::text, 'Under Review'::text, 'Approved'::text]))),
	CONSTRAINT "Deliverables_pkey" PRIMARY KEY ("DeliverableID"),
	CONSTRAINT "Deliverables_AssignedUser_fkey" FOREIGN KEY ("AssignedUser") REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
	CONSTRAINT "Deliverables_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);


-- "Notation"."Notifications" definition

-- Drop table

-- DROP TABLE "Notation"."Notifications";

CREATE TABLE "Notation"."Notifications" (
	"NotificationID" serial4 NOT NULL,
	"User" text NULL,
	"Message" text NOT NULL,
	"Status" text DEFAULT 'Unread'::text NULL,
	"CreatedAt" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "Notifications_Status_check" CHECK (("Status" = ANY (ARRAY['Unread'::text, 'Read'::text]))),
	CONSTRAINT "Notifications_pkey" PRIMARY KEY ("NotificationID"),
	CONSTRAINT "Notifications_User_fkey" FOREIGN KEY ("User") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."ParticipationLedger" definition

-- Drop table

-- DROP TABLE "Notation"."ParticipationLedger";

CREATE TABLE "Notation"."ParticipationLedger" (
	"TransactionID" serial4 NOT NULL,
	"ProjectID" int4 NOT NULL,
	"Username" text NULL,
	"PaymentType" text NOT NULL,
	"Amount" numeric(12, 2) NOT NULL,
	"ProjectBalance" numeric(12, 2) DEFAULT 0.00 NULL,
	"RecoupmentThreshold" numeric(12, 2) DEFAULT 0.00 NULL,
	"Timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "ParticipationLedger_PaymentType_check" CHECK (("PaymentType" = ANY (ARRAY['Bonus'::text, 'Equity_Payout'::text, 'Flat_Fee'::text]))),
	CONSTRAINT "ParticipationLedger_pkey" PRIMARY KEY ("TransactionID"),
	CONSTRAINT "ParticipationLedger_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE,
	CONSTRAINT "ParticipationLedger_Username_fkey" FOREIGN KEY ("Username") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."Payments" definition

-- Drop table

-- DROP TABLE "Notation"."Payments";

CREATE TABLE "Notation"."Payments" (
	"PaymentID" serial4 NOT NULL,
	"Username" text NULL,
	"ProjectID" int4 NULL,
	"PaymentType" text NULL,
	"Amount" numeric(12, 2) NOT NULL,
	"Timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "Payments_PaymentType_check" CHECK (("PaymentType" = ANY (ARRAY['Escrow Deposit'::text, 'Flat Fee'::text, 'Bonus Drawdown'::text, 'Refund'::text]))),
	CONSTRAINT "Payments_pkey" PRIMARY KEY ("PaymentID"),
	CONSTRAINT "Payments_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE SET NULL,
	CONSTRAINT "Payments_Username_fkey" FOREIGN KEY ("Username") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."Payroll" definition

-- Drop table

-- DROP TABLE "Notation"."Payroll";

CREATE TABLE "Notation"."Payroll" (
	"PayrollID" serial4 NOT NULL,
	"Username" text NULL,
	"GrossPay" numeric(12, 2) DEFAULT 0.00 NOT NULL,
	"Tax" numeric(12, 2) DEFAULT 0.00 NULL,
	"Insurance" numeric(12, 2) DEFAULT 0.00 NULL,
	"PensionContribution" numeric(12, 2) DEFAULT 0.00 NULL,
	"OtherDeductions" numeric(12, 2) DEFAULT 0.00 NULL,
	"NetPay" numeric(12, 2) GENERATED ALWAYS AS (("GrossPay" - ("Tax" + "Insurance" + "PensionContribution" + "OtherDeductions"))) STORED NULL,
	"Bonus" numeric(12, 2) DEFAULT 0.00 NULL,
	"PhantomEquity" numeric(5, 4) DEFAULT 0.0000 NULL,
	"Status" text DEFAULT 'Pending'::text NULL,
	CONSTRAINT "Payroll_Status_check" CHECK (("Status" = ANY (ARRAY['Paid'::text, 'Pending'::text, 'Cancelled'::text]))),
	CONSTRAINT "Payroll_Username_key" UNIQUE ("Username"),
	CONSTRAINT "Payroll_pkey" PRIMARY KEY ("PayrollID"),
	CONSTRAINT "Payroll_Username_fkey" FOREIGN KEY ("Username") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."Pods" definition

-- Drop table

-- DROP TABLE "Notation"."Pods";

CREATE TABLE "Notation"."Pods" (
	"PodID" serial4 NOT NULL,
	"AdminID" int4 NULL,
	"CreatorID" int4 NULL,
	"FreelancerID" int4 NULL,
	"ProjectID" int4 NULL,
	CONSTRAINT "Pods_ProjectID_key" UNIQUE ("ProjectID"),
	CONSTRAINT "Pods_pkey" PRIMARY KEY ("PodID"),
	CONSTRAINT "Pods_AdminID_fkey" FOREIGN KEY ("AdminID") REFERENCES "Notation"."Users"("UserID") ON DELETE RESTRICT,
	CONSTRAINT "Pods_CreatorID_fkey" FOREIGN KEY ("CreatorID") REFERENCES "Notation"."Users"("UserID") ON DELETE RESTRICT,
	CONSTRAINT "Pods_FreelancerID_fkey" FOREIGN KEY ("FreelancerID") REFERENCES "Notation"."Users"("UserID") ON DELETE SET NULL,
	CONSTRAINT "Pods_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);


-- "Notation"."Proposals" definition

-- Drop table

-- DROP TABLE "Notation"."Proposals";

CREATE TABLE "Notation"."Proposals" (
	"ProposalID" serial4 NOT NULL,
	"Title" text NOT NULL,
	"Description" text NULL,
	"Genre" text NULL,
	"ProjectType" text NULL,
	"EstBudget" numeric(12, 2) NULL,
	"EstRuntime" int4 NULL,
	"SubmittedBy" text NULL,
	"Status" text DEFAULT 'Pending Validation'::text NULL,
	"CreatedAt" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT "Proposals_pkey" PRIMARY KEY ("ProposalID"),
	CONSTRAINT "Proposals_SubmittedBy_fkey" FOREIGN KEY ("SubmittedBy") REFERENCES "Notation"."Users"("Username") ON DELETE CASCADE
);


-- "Notation"."Tasks" definition

-- Drop table

-- DROP TABLE "Notation"."Tasks";

CREATE TABLE "Notation"."Tasks" (
	"TaskID" serial4 NOT NULL,
	"ProjectID" int4 NOT NULL,
	"AssignedUser" text NULL,
	"Title" text NOT NULL,
	"Description" text NULL,
	"Priority" text NULL,
	"Status" text DEFAULT 'Pending'::text NULL,
	"Deadline" date NULL,
	"CompletedAt" timestamp NULL,
	CONSTRAINT "Tasks_Priority_check" CHECK (("Priority" = ANY (ARRAY['Low'::text, 'Medium'::text, 'High'::text, 'Critical'::text]))),
	CONSTRAINT "Tasks_Status_check" CHECK (("Status" = ANY (ARRAY['Pending'::text, 'In Progress'::text, 'Blocked'::text, 'Completed'::text]))),
	CONSTRAINT "Tasks_pkey" PRIMARY KEY ("TaskID"),
	CONSTRAINT "Tasks_AssignedUser_fkey" FOREIGN KEY ("AssignedUser") REFERENCES "Notation"."Users"("Username") ON DELETE SET NULL,
	CONSTRAINT "Tasks_ProjectID_fkey" FOREIGN KEY ("ProjectID") REFERENCES "Notation"."Projects"("ProjectID") ON DELETE CASCADE
);

COMMIT;