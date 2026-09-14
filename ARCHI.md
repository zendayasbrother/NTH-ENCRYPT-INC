# NTH - ENCRYPT INC: Architecture & Workflows

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
---

## 📋 User Workflows

### Envisioned Admin Workflow

```
LOGIN (Bcrypt > Django JWT Auth)
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
