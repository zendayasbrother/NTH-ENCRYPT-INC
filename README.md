# NTH - ENCRYPT INC: Plugin Creator OS 

**An operating system for the modern creator economy** | Built for Creators, Freelancers, and Talent-First Agencies

---

## 🎯 Overview

Encrypt Inc. is a **Talent-First Agency OS** designed to solve operational challenges faced by content creators and talent-driven media agencies. Inspired by BuzzFeed and Vice, this platform implements fair compensation models, transparent vesting schedules, and robust financial ledger tracking.

### The Problem I Solve

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

- **Typography**: Helvetica (UI), Fira Code (financial figures)
- **Target**: Desktop GUI (Terminal in MVP, Terminal + Web in v1+)
- **Interaction**: Text hover feature with underline
- **Aesthetic**: Utilitarian + Brutalist UI
- **Accessibility**: High contrast, keyboard navigation

📐 **Figma Design Board**: [insert updated]

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
- Backend: Python, PGSQL, TS
- Libraries: Pytest, Django, Faker, asyncio
- Interface: Command-line terminal
- Frontend: Tailwind CSS, React 

**Core Features (DECOUPLED)**
- Plugin + Microkernel Architecture via Decoupling
- In house Insurance
- Financial Ledger
- International Talent + Ops

## 💻 Implementation / Simulation Guide

TBD - Interactive Lens (ROLEPLAY)


---

## 📄 License

Proprietary - Notation 'NTH' Studios © 2026. All rights reserved.

---

## 📞 Contact & Support

- **Founder**: Daniel Onyeakazi 
