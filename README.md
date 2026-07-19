# NTH - ENCRYPT INC: Plugin Creator OS 

**An operating system for the modern creator economy** | Built for Creators, Freelancers, and Talent-First Agencies

---

## 🎯 Overview

Encrypt Inc. is a **Talent-First Agency OS** designed to solve operational challenges faced by content creators and talent-driven media agencies. Inspired by BuzzFeed and Vice, this platform implements a **25% Agency / 75% Talent equity model** with an **smart waterfall payment system** that ensures fair compensation while protecting both parties through an escrow-backed contract framework.

### The Problem We Solve

Modern creator economies lack transparent, scalable infrastructure for:
- **Asset & IP Management**: Tracking ownership, vesting, and royalties across multiple projects
- **Fair Compensation**: Implementing tiered payment systems that prioritize talent while maintaining agency viability
- **Contract Enforcement**: Managing 7-year lease structures with vesting cliffs and exit clauses
- **Operational Scaling**: Maintaining the 1:5:10 admin:talent:project ratio across distributed teams

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

## 🚀 Development Roadmap

### Phase 1: MVP (v0) - Terminal-Based (Hardcoded) System

**Status**: COMPLETED 

**Technology Stack**
Frontend:        Terminal/CLI
Backend:         Python
Database:        SQLite3
Auth:            Bcrypt, Hashlib
Libraries:       NumPy, Pandas, Keyboard, Sys, OS

**Core Features (HARDCORDED)**
- ✅ Creator and freelancer records with full profiles
- ✅ Admin authentication + login system (Bcrypt hashing)
- ✅ Admin superiority: full CRUD + search capabilities
- ✅ Talent read-only access to assigned profiles
- ✅ Proposal submission and management (algorithmic priority queue)
- ✅ Immutable Audit logging for compliance
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

## Phase 2: Production MVP (v1) - Django Based System

**Status**: DEVELOPING 


**Technology Stack**
- Backend: Python, PGSQL
- Libraries: Pytest, Django, Faker, asyncio
- Interface: Command-line terminal
- Frontend: Tailwind CSS, React 

**Core Features (DECOUPLED)**
- Basic Plugin Architecture via Decoupling
- In house Insurance
- Financial Ledger
- Currency Conversion and Exchange

## 💻 Implementation / Simulation Guide

TBD


---

## 🤝 Contributing

We welcome contributions from developers, designers, and domain experts. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Development Environment**: Python 3.9+, PostgreSQL 12+

---

## 📄 License

Proprietary - NTH (Encrypt Inc.) © 2024. All rights reserved.

---

## 📞 Contact & Support

- **Founder**: Daniel Onyeakazi 
