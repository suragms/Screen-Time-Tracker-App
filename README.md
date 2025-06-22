---

# 𝖲𝖢𝖱𝖤𝖤𝖭𝖳𝖨𝖬𝖤 𝖳𝖱𝖠𝖢𝖪𝖤𝖱 𝖠𝖯𝖯

**👨‍💼 CEO**: Surag M S
**📧 Email**: [suraagms@gmail.com](mailto:suraagms@gmail.com)
**🔗 GitHub**: [@suragms](https://github.com/suragms)
**🔗 LinkedIn**: [Surag Sunil](https://linkedin.com/in/suragsunil)

---

A **full-stack productivity and wellness application** designed to **track, manage, and analyze digital habits**. Ideal for developers, students, and digital professionals, it encourages **mindful technology usage** through insightful analytics, integrated tools, and a seamless user experience.

---

## 📌 Table of Contents

* [📖 About the Project](#-about-the-project)
* [🚀 Key Features](#-key-features)
* [🛠 Tech Stack](#-tech-stack)
* [📁 Project Structure](#-project-structure)
* [⚙️ Installation](#-installation)
* [📋 Usage](#-usage)
* [🔗 API Endpoints](#-api-endpoints)
* [🤝 Contributing](#-contributing)
* [📝 License](#-license)
* [📞 Contact](#-contact)

---

## 📖 About the Project

The **Screen Time Tracker App** is a comprehensive platform built with **Django** and **REST APIs** that allows users to:

* Log and track daily screen time
* Visualize digital habits and trends
* Set personal usage goals
* Manage productivity boosters such as alarms, sticky notes, and an in-app music player

Its modular architecture ensures scalability and customization for future enhancements.

---

## 🚀 Key Features

* ⏱ **Screen Time Logging** – Real-time tracking of daily activities
* 🧭 **Multiple Concurrent Timers** – Switch between tasks seamlessly
* 📈 **Analytics Dashboard** – Interactive charts for weekly/monthly trends
* ⏰ **Custom Alarms** – Set reminders to optimize productivity
* 📝 **Sticky Notes** – With color-coded tags for better organization
* 🎧 **Built-in Music Player** – Upload and play focus-enhancing tracks
* 👤 **Profile Customization** – Personalized user experience
* 🎯 **Daily Usage Goals** – Set, track, and achieve your screen time goals

---

## 🛠 Tech Stack

| Layer        | Technologies                              |
| ------------ | ----------------------------------------- |
| **Frontend** | HTML5, CSS3, Bootstrap, JavaScript        |
| **Backend**  | Python, Django, Django REST Framework     |
| **Database** | SQLite3                                   |
| **Auth**     | Django Authentication System              |
| **Others**   | JSON, Django Signals, File Upload Support |

---

## 📁 Project Structure

```
screen_time_project/
├── manage.py
├── requirements.txt
├── README.md
├── screentime_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/
│   ├── __init__.py
│   ├── admin.py
│   ├── admin_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── static/
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       └── ...
│   ├── management/
│   │   └── commands/
│   │       └── custom_command.py
│   └── migrations/
│       └── 0001_initial.py
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.8+
* pip
* Virtualenv (recommended)
* Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/suragms/screen-time-tracker.git
cd screen-time-tracker

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate         # On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create an admin user (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Access the app at: `http://127.0.0.1:8000`

---

## 📋 Usage

### Workflow Overview

1. 🔐 Register or Log in
2. 👤 Set up your profile
3. ⏱ Track screen time with start/stop buttons
4. 📊 Analyze digital habits through the dashboard
5. ⏰ Set alarms or 📝 create sticky notes
6. 🎵 Upload and listen to music
7. 🎯 Monitor and achieve personal usage goals

---

## 🔗 API Endpoints

**Base URL**: `http://localhost:8000/api/`

### Screen Time

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| GET    | `/screentime/`      | Retrieve all entries    |
| POST   | `/screentime/`      | Create new entry        |
| GET    | `/screentime/<id>/` | Retrieve specific entry |
| PUT    | `/screentime/<id>/` | Update entry            |
| DELETE | `/screentime/<id>/` | Delete entry            |

#### Example Request Payload

```json
{
  "activity": "Reading Docs",
  "category": "Study",
  "start_time": "2025-06-22T10:00:00Z",
  "end_time": "2025-06-22T11:00:00Z",
  "notes": "Reading Django Docs"
}
```

---

## 🤝 Contributing

We welcome community contributions!
To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to GitHub: `git push origin feature/your-feature-name`
5. Submit a Pull Request

Please follow PEP8 coding standards and include tests where appropriate.

---

## 📝 License

This project is licensed under the **MIT License**.
See the full license [here](LICENSE).

---

## 📞 Contact

**Surag M S**
📧 [suraagms@gmail.com](mailto:suraagms@gmail.com)
🔗 [GitHub: @suragms](https://github.com/suragms)
🔗 [LinkedIn: Surag Sunil](https://linkedin.com/in/suragsunil)
🔗 [Linktree: SuragDevStudio](https://linktr.ee/suragdevstudio)

---
