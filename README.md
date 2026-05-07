<img width="1039" height="696" alt="Screenshot 2026-05-07 at 6 29 14 AM" src="https://github.com/user-attachments/assets/b378672d-564b-4e2f-b332-7396bddd4b76" /># 🏢 Job Portal REST API

A production-ready **Job Portal Backend API** built with **Django REST Framework**, **PostgreSQL**, and **Redis Caching** — featuring complete job posting, application tracking, and intelligent caching for high-performance responses.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?style=flat)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-Cache-red?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange?style=flat)](https://jwt.io)
[![Render](https://img.shields.io/badge/Deployed-Render-purple?style=flat)](YOUR_RENDER_LINK_HERE)

## 🌐 Live Demo

> **Base URL:** https://job-portal-api-with-redis-caching.onrender.com/api/register/

---

## 🚀 What Makes This Project Different?

Unlike basic CRUD projects, this API solves **real non-functional challenges**:

| Challenge | Solution | Impact |
|-----------|----------|--------|
| Slow database queries | Redis Caching | 10x faster response |
| Repeated API calls | Cache invalidation | Reduced DB load |
| Search performance | Cached search results | 5ms vs 50ms response |
| Concurrent users | Optimized ORM queries | Handles scale |

---

## ✨ Features

- ✅ **JWT Authentication** — Register, Login, Token Refresh
- ✅ **Company Management** — Post and manage company profiles
- ✅ **Job Posting** — Full CRUD with job type, salary, skills
- ✅ **Smart Application System** — Apply, track status (Pending → Hired)
- ✅ **Redis Caching** — Jobs list cached for 5 min, search results for 2 min
- ✅ **Cache Invalidation** — Auto cache clear when new job posted
- ✅ **Advanced Search** — Filter by title, location, job type
- ✅ **Resume Upload** — File upload support
- ✅ **Duplicate Prevention** — One application per job per user
- ✅ **PostgreSQL** — Production database

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3.11 | Core Language |
| Django 4.2 | Web Framework |
| Django REST Framework | API Development |
| PostgreSQL | Primary Database |
| Redis | Caching Layer |
| django-redis | Redis Integration |
| SimpleJWT | Authentication |
| django-filter | Search & Filtering |
| python-decouple | Environment Variables |
| Render | Cloud Deployment |

---

## 🏗️ Architecture

```
Client Request
      ↓
   Django API
      ↓
  Redis Cache ← Cache Hit → Return Response (5ms)
      ↓ Cache Miss
  PostgreSQL Database
      ↓
  Store in Cache
      ↓
  Return Response (50ms)
```

---

## 📁 Project Structure

```
job-portal-api/
├── jobs/
│   ├── models.py        # Company, Job, Application models
│   ├── serializers.py   # Data serialization
│   ├── views.py         # Business logic + Redis caching
│   ├── urls.py          # URL routing
│   └── admin.py         # Admin configuration
├── core/
│   ├── settings.py      # Redis + DB configuration
│   └── urls.py          # Main URLs
├── Procfile             # Render deployment
├── requirements.txt     # Dependencies
└── README.md
```

---

## 🔗 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/register/` | Register new user | ❌ |
| POST | `/api/login/` | Login — JWT token | ❌ |
| POST | `/api/token/refresh/` | Refresh token | ❌ |

### 🏢 Companies
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/companies/` | All companies (cached) | ❌ |
| POST | `/api/companies/` | Create company | ✅ |

### 💼 Jobs
| Method | Endpoint | Description | Auth | Cache |
|--------|----------|-------------|------|-------|
| GET | `/api/jobs/` | All jobs (cached 5 min) | ❌ | ✅ Redis |
| POST | `/api/jobs/` | Post new job | ✅ | Invalidates |
| GET | `/api/jobs/{id}/` | Job detail (cached) | ❌ | ✅ Redis |
| PUT | `/api/jobs/{id}/` | Update job | ✅ | Invalidates |
| DELETE | `/api/jobs/{id}/` | Delete job | ✅ | Invalidates |

### 🔍 Search
| Method | Endpoint | Description | Cache |
|--------|----------|-------------|-------|
| GET | `/api/jobs/search/?q=python` | Search by title/skills | ✅ 2 min |
| GET | `/api/jobs/search/?location=delhi` | Search by location | ✅ 2 min |
| GET | `/api/jobs/search/?type=full_time` | Filter by type | ✅ 2 min |

### 📋 Applications
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/jobs/{id}/apply/` | Apply for job | ✅ |
| GET | `/api/applications/my/` | My applications | ✅ |

---

## ⚡ Redis Caching Demo

```bash
# First request — hits database
GET /api/jobs/
Response: {"source": "database", "data": [...]}  # ~50ms

# Second request — hits Redis cache
GET /api/jobs/
Response: {"source": "cache", "data": [...]}  # ~5ms
```

**Cache Strategy:**
```python
# Cache set — 5 minutes
cache.set('all_jobs', data, timeout=300)

# Auto invalidation on new job
cache.delete('all_jobs')
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Mr-SHAAD/job-portal-api.git
cd job-portal-api

# 2. Virtual environment
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
touch .env
```

Add to `.env`:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=jobportal
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/1
```

```bash
# 5. Start Redis
brew services start redis  # Mac
sudo service redis start   # Linux

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Start server
python manage.py runserver
```

---

## 🧪 API Testing (Postman)

**Step 1 — Register:**
```json
POST /api/register/
{
    "username": "testuser",
    "email": "test@gmail.com",
    "password": "pass123"
}
```

**Step 2 — Login & get token:**
```json
POST /api/login/
{
    "username": "testuser",
    "password": "pass123"
}
```

**Step 3 — Post a Job:**
```json
POST /api/jobs/
Authorization: Bearer <token>
{
    "title": "Python Developer",
    "description": "Django developer needed",
    "company": 1,
    "location": "Delhi",
    "salary": "50000",
    "job_type": "full_time",
    "skills_required": "Python, Django, PostgreSQL"
}
```

**Step 4 — See Cache in Action:**
```bash
GET /api/jobs/  # source: "database"
GET /api/jobs/  # source: "cache" ← Redis working!
```

---

## 📸 API Screenshots

### Register API
<img width="1039" height="696" alt="Screenshot 2026-05-07 at 6 29 14 AM" src="https://github.com/user-attachments/assets/1dc46f3b-5f01-48e9-a43a-1279e635f337" />

### Jobs List — Database vs Cache
<img width="1030" height="698" alt="Screenshot 2026-05-07 at 6 33 36 AM" src="https://github.com/user-attachments/assets/8ed3a23d-c233-418a-9a0f-0d520fbe3e66" />


### Search API
<img width="1031" height="688" alt="Screenshot 2026-05-07 at 6 35 19 AM" src="https://github.com/user-attachments/assets/56288bbe-e963-445d-9cae-9ac4e360de18" />
<img width="1027" height="702" alt="Screenshot 2026-05-07 at 6 34 47 AM" src="https://github.com/user-attachments/assets/acea7a49-c9ce-4d1d-87a5-966ec97cf907" />
<img width="1030" height="707" alt="Screenshot 2026-05-07 at 6 35 04 AM" src="https://github.com/user-attachments/assets/2dfdfb33-5c10-4f8e-b434-6a34f63e2ce6" />


---

## 💡 Key Technical Decisions

**Why Redis?**
- Database queries are expensive at scale
- Job listings don't change every second
- Caching reduces DB load by 80%+

**Why Cache Invalidation?**
- Stale data is worse than no cache
- Auto-delete on write ensures consistency

**Why unique_together?**
- Prevents duplicate applications at DB level
- More reliable than application-level checks

---

## 👨‍💻 Author

**Mohammad Shaad (iamshaadgour)**
- 🐙 GitHub: [@Mr-SHAAD](https://github.com/Mr-SHAAD)
- 💼 LinkedIn: [Mohammad Shaad](https://linkedin.com/in/mohammad-shaad-672334204)
- 📧 Email: knowmore8126@gmail.com

---

## 🔗 My Other Projects

| Project | Description | Live |
|---------|-------------|------|
| [Blog REST API](https://github.com/Mr-SHAAD/blog-api) | JWT Auth, Posts, Comments, Likes | [Live](https://blog-api-production-b09d.up.railway.app) |
| [E-Commerce API](https://github.com/Mr-SHAAD/ecommerce-api) | Cart, Orders, Reviews, Search | [Live](https://web-production-746fb.up.railway.app) |

---

⭐ **Star this repo if you found it helpful!**
