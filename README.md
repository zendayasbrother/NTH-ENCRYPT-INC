# ENCRYPT INC - Creator & IP Management Platform

**An algorithmic ERP system for the modern creator economy** | Built for Creators, Freelancers, and Talent-First Agencies

---

## 🎯 Overview

Encrypt Inc. is a **Talent-First Agency OS** designed to solve operational challenges faced by content creators and talent-driven media agencies. Inspired by industry learnings from BuzzFeed and Vice, this platform implements a **25% Agency / 75% Talent equity model** with an **intelligent waterfall payment system** that ensures fair compensation while protecting both parties through an escrow-backed contract framework.

### The Problem We Solve

Modern creator economies lack transparent, scalable infrastructure for:
- **Asset & IP Management**: Tracking ownership, vesting, and royalties across multiple projects
- **Fair Compensation**: Implementing tiered payment systems that prioritize talent while maintaining agency viability
- **Contract Enforcement**: Managing 7-year lease structures with vesting cliffs and exit clauses
- **Operational Scaling**: Maintaining the 1:5:10 admin:talent:project ratio across distributed teams

---

## 📊 Core Architecture

### Business Model

| Metric | Value |
|--------|-------|
| **IP Ownership** | 25% Agency / 75% Talent |
| **Net Revenue Split** | 20% Agency / 80% Talent (waterfall) |
| **Vesting Period** | 7 years (12-month cliff) |
| **Per-Project Vesting** | 20% per qualifying project |
| **Max Portfolio Budget** | £500K per production roster |
| **Admin:Talent:Project Ratio** | 1:5:10 |
| **Max Active Projects** | Approved Talent × Max Concurrent Projects |

### Operational Tiers

1. **Admin Tier**: In-house heads with full CRUD privileges
2. **Talent Tier**: Creators & Freelancers (read own data, submit proposals)
3. **Project Tier**: Production units with budget caps and phase tracking

---

## 🏗️ System Architecture

### Database Schema (SQL)

#### Core Tables

**Users**
- Username, First/Last Name, Email, Hashed Password, Role (Admin/Creator/Freelancer)
- Email routing: `firstname@encrypt.com` (Admin) | `f.lastname@encrypt.com` (Talent)

**Projects**
- Title, Budget Cap (£500K default), Production Costs, Gross Revenue
- Phases: Not Started → Filming & Production → Approved/Complete
- Genres: Action, Anthology, Comedy, Drama, Fantasy, Horror, Documentary, Game Show, Sci-Fi

**Proposals**
- ProposalID, Title, ProjectType, Genre, Budget, SubmittedBy, Priority Score, Status
- FIFO/Priority Queue Logic: TV > Video > Films

**Payroll**
- UserID, Gross Pay, Tax Deduction, National Insurance, Pension, Net Pay (derived)
- Formula: `NET_PAY = Gross - (Tax + Insurance)`

**Financial Ledger**
- TransactionID, ProjectID, Username, Payment Type (Bonus/Equity/Flat Fee)
- Project Balance, Recoupment Threshold, Amount, Timestamp

**IP Registry** (7-Year Master Lease)
- Project, Agency Share (25%), Talent Share (75%)
- Vesting Cliff (12 months), Per-Project Vesting (20%)
- Severability Multiplier for Ex-Talent

**Audit Logs** (Immutable)
- LogID, ProjectID, Change Type, Old/New Values, Timestamp

**Participation Ledger**
- Pod assignments, Project allocations, Performance tracking

#### Leadership Directory

| Name | Role | Email |
|------|------|-------|
| Daniel Onyeakazi | Founder | daniel@encrypt.com |
| Griff Lawson | Chief Operations Officer (Legal) | griff@encrypt.com |
| Teni Olayinka | Chief Financial Officer | teni@encrypt.com |
| Sven Talefson | Chief Brand & Communications | sven@encrypt.com |
| Angela Keith | Head of Product | angela@encrypt.com |
| Jade Zhang | Head of Legal Operations | jade@encrypt.com |
| Willow Youn | Senior Data Scientist | willow@encrypt.com |

---

## 🚀 Development Roadmap

### Phase 1: MVP (Year 1) - Terminal-Based System

**Status**: In Development

**Technology Stack**
- Backend: Python, SQLite3
- Libraries: NumPy, Pandas, Bcrypt, Hashlib, Pwinput, Keyboard, Sys, OS
- Interface: Command-line terminal

**Core Features**
- ✅ Creator and freelancer records with full profiles
- ✅ Admin authentication + login system (Bcrypt hashing)
- ✅ Admin superiority: full CRUD + search capabilities
- ✅ Talent read-only access to assigned profiles
- ✅ Proposal submission and management (algorithmic priority queue)
- ✅ Audit logging for compliance
- ✅ Basic payroll calculations

**Key Files**
```
├── database.py        # SQLite schema & initialization
├── auth.py           # Bcrypt authentication & session management
├── engine.py         # Core business logic (proposals, payroll)
├── main.py           # CLI entry point
└── config.py         # Hardcoded Encrypt Inc. data
```

**Proposal Priority Algorithm**
```
Priority Score Calculation:
1. Project Type Weight: TV (100) > Video (75) > Films (50)
2. Budget Factor: -(Budget ÷ 500,000) × 30 points
3. Duration Penalty: -(Months ÷ 12) × 15 points
4. Genre Coefficient: Applied per category
5. Title Length Adjustment: Title char count ÷ 50
Final Score: Type + Budget + Duration + Genre + Title (Ascending = Higher Priority)
```

---

## 🎨 Design System

### Visual Identity

**Color Palette** (Navy + Tech Blue + Corporate Accents)
```
Primary Blues:
- Navy: #000814 (Primary background)
- Dark Navy: #001d3d
- Core Blue: #012F7B
- Tech Teal: #0da9c8

Neutrals:
- Light Blue: #bfdbf7
- Light Gray: #e1e5f2
- White: #ffffff

Status Indicators:
- Success: #2E7D32 (Green) → Completed tasks, positive ROI
- Warning: #F57C00 (Amber) → Pending status, warnings
- Critical: #D32F2F (Red) → Negative balances, blocked tasks
```

### Interface Guidelines

- **Typography**: Helvetica (UI), Courier New (financial figures)
- **Target**: Desktop GUI (Terminal in MVP, Web in v1+)
- **Interaction**: Text hover feature with underline
- **Aesthetic**: Utilitarian + Tactical/C2 control panel style
- **Accessibility**: High contrast, keyboard navigation

📐 **Figma Design Board**: [ENCRYPT-INC Project](https://www.figma.com/board/dib4MShNrXPhTTwbja7IIQ/ENCRYPT-INC?node-id=2001-44)

---

## 📋 User Workflows

### Admin Workflow

```
LOGIN (Bcrypt Auth)
│
├─ DASHBOARD
│  ├─ View all projects & metrics
│  ├─ View all talent profiles
│  └─ Monitor audit logs
│
├─ TALENT MANAGEMENT
│  ├─ Search by email, name, ID
│  ├─ View proposal queue (priority-sorted)
│  ├─ Approve/Reject proposals
│  └─ Manage team assignments
│
├─ PROJECT MANAGEMENT
│  ├─ Create new projects
│  ├─ Update phases (Not Started → Production → Approved)
│  ├─ Adjust budgets
│  └─ View production metrics
│
└─ FINANCIAL OPERATIONS
   ├─ View payroll calculations
   ├─ Trigger waterfall distributions
   ├─ Manage escrow deposits
   └─ Generate tax reports
```

### Talent Workflow

```
LOGIN (Bcrypt Auth)
│
├─ PROFILE VIEW
│  ├─ View personal data
│  ├─ Check current assignments
│  └─ View vesting progress (v2+)
│
├─ PROPOSAL SUBMISSION
│  ├─ Fill algorithmic proposal form
│  ├─ Set title, genre, budget, duration
│  └─ Submit for admin review
│
├─ PROJECT DASHBOARD
│  ├─ View assigned projects
│  ├─ Track production phases
│  └─ Monitor payment schedules (v2+)
│
└─ EARNINGS VIEW (v2+)
   ├─ View payment history
   ├─ Check equity vesting schedule
   └─ Review transaction ledger
```

---

## 💻 Implementation Guide

### Phase 1 Setup (Terminal MVP)

```bash
# Clone repository
git clone https://github.com/zendayasbrother/ENCRYPT-INC.git
cd ENCRYPT-INC

# Install dependencies
pip install -r requirements.txt

# Initialize database with seed data
python database.py --init

# Run application
python main.py
```

### Phase 2 Setup (Django Web)

```bash
# Install Django dependencies
pip install django djangorestframework django-cors-headers python-decouple dj-database-url psycopg2-binary

# Set environment variables
export DATABASE_URL=postgres://user:pass@localhost:5432/encrypt_db
export SECRET_KEY=your-secret-key

# Run migrations
python manage.py migrate

# Load seed data
python manage.py loaddata fixtures/teams.json fixtures/projects.json

# Start development server
python manage.py runserver
```

### Testing & Quality Assurance

```bash
# Unit tests
pytest tests/ -v

# Integration tests with Faker
python manage.py test apps.core.tests --verbosity=2

# Load testing with threading
locust -f loadtests/locustfile.py

# Coverage reporting
coverage run -m pytest && coverage report
```

---

## 🔐 Security & Compliance

### Authentication & Authorization

- **Password Hashing**: Bcrypt (MVP) → Django PBKDF2 (v2+)
- **Session Management**: Secure cookies with CSRF protection
- **Multi-tenancy**: Data isolation at database row level
- **RBAC**: Role-based access control (Admin/Talent/Freelancer)

### Data Protection

- **Audit Logging**: Immutable log table tracks all changes (LogID, ProjectID, Change_Type, Timestamp)
- **Escrow Mechanism**: Risk mitigation deposits held in trust
- **IP Protection**: 7-year master lease with vesting cliffs
- **Compliance**: UK tax calculations (expandable to international via OpenFisca)

---

## 📈 Key Metrics & KPIs

### System Health

| Metric | Target | Status |
|--------|--------|--------|
| Admin:Talent Ratio | 1:5 | 🟢 |
| Admin:Project Ratio | 1:10 | 🟢 |
| Avg Project Budget Utilization | 80-95% | 📊 |
| Payment Distribution Time | <48hrs | 🚀 |
| Proposal Approval Rate | 60-70% | 📊 |

### Financial Tracking

- **Gross Revenue**: Platform-wide total
- **Platform Fees**: YouTube, Patreon, etc. (45% default)
- **Production Costs**: Team salaries, equipment, licenses
- **Net Receipts**: Gross Revenue - Platform Fees
- **Waterfall Distribution**: (Net Receipts - Production Costs) × [20% Agency / 80% Talent]

### Talent Metrics

- **Vesting Progress**: % of 7-year cliff completed
- **Project Success Rate**: % of on-budget, on-time projects
- **Equity Accrual**: Phantom shares accumulated (v2+)
- **Severability Score**: Payout multiplier if departing

---

## 🛠️ Technology Stack by Phase

### Phase 1 (Current - MVP)
```
Frontend:        Terminal/CLI
Backend:         Python
Database:        SQLite3
Auth:            Bcrypt
Libraries:       NumPy, Pandas, Keyboard, Sys, OS
```


## 📖 Documentation

- **[Database Schema](./docs/schema.md)** - Detailed SQL structure
- **[API Reference](./docs/api.md)** - REST endpoints (v2+)
- **[Business Logic](./docs/logic.md)** - Waterfall, vesting, equity calculations
- **[Deployment Guide](./docs/deployment.md)** - Docker, K8s, CI/CD (v2+)
- **[Contributing](./CONTRIBUTING.md)** - Development guidelines

---

## 🎬 Showcase Projects

### TV Series
- **Crocodile Tears** - Drama | Status: Approved
- **Agege and Strangers** - Comedy/ComDrama | Status: Production
- **It Was Only Pad Thai** - Comedy Drama/Anthology | Status: Approved

### Films
- **Herr Johannes** - Action | Budget: £250K | Status: Production
- **T Minus Dream** - Fantasy | Budget: £180K | Status: Not Started
- **Ananas** - Horror | Budget: £150K | Status: Approved
- **Normalisation** - Sci-Fi | Budget: £220K | Status: Production

### Content Niches
Art, Comedy, Fashion, Food, Lifestyle, Technology

---

## 🤝 Contributing

We welcome contributions from developers, designers, and domain experts. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Development Environment**: Python 3.9+, PostgreSQL 12+, Node.js 16+

---

## 📄 License

Proprietary - NTH (Encrypt Inc.) © 2024. All rights reserved.

---

## 📞 Contact & Support

- **Founder**: Daniel Onyeakazi
