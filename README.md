# Thendral City Developers Website

A professional construction company website built with Flask, MySQL, and modern frontend technologies.

## Features

- **Professional Design**: Clean, modern UI inspired by industry standards with green theme
- **Responsive Layout**: Mobile-first design that works on all devices
- **Admin Panel**: Full CRUD operations for projects, services, and content management
- **Authentication**: Secure admin login with password hashing
- **Contact Form**: Functional contact form with email notifications
- **Image Upload**: Secure image upload with validation
- **REST API**: JSON API for dynamic content loading
- **Smooth Animations**: Professional scroll and hover animations

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Werkzeug password hashing
- **Forms**: WTForms for validation

## Project Structure

```
tmconstruction/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/               # SQLAlchemy models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── service.py
│   │   ├── testimonial.py
│   │   ├── contact_message.py
│   │   ├── team_member.py
│   │   └── image_gallery.py
│   ├── routes/               # Flask blueprints
│   │   ├── main.py           # Public routes
│   │   ├── admin.py          # Admin routes
│   │   └── api.py            # REST API
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── company.html
│   │   ├── services.html
│   │   ├── projects.html
│   │   ├── contact.html
│   │   ├── 404.html
│   │   └── 500.html
│   ├── static/               # Static files
│   │   ├── css/
│   │   │   ├── base.css
│   │   │   ├── components.css
│   │   │   ├── animations.css
│   │   │   ├── admin.css
│   │   │   └── responsive.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── animations.js
│   │   │   ├── form-handler.js
│   │   │   └── api-client.js
│   │   └── images/
│   │       └── tclogo.jpg
│   ├── utils/                # Utility functions
│   │   ├── validators.py
│   │   └── decorators.py
│   └── services/             # Business logic
│       ├── auth_service.py
│       ├── image_handler.py
│       ├── project_service.py
│       └── contact_service.py
├── config/
│   ├── config.py             # Configuration settings
│   └── database.py           # Database connection
├── database/
│   └── schema.sql            # MySQL schema
├── uploads/                  # Uploaded files directory
├── requirements.txt          # Python dependencies
├── init_db.py               # Database initialization script
├── run.py                   # Application entry point
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   cd d:\vidhaiProjects\tmconstruction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` file with your database credentials:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=thendral_construction
   SECRET_KEY=your-secret-key
   ```

5. **Create MySQL database**
   ```sql
   CREATE DATABASE thendral_construction;
   ```

6. **Initialize database**
   ```bash
   python init_db.py
   ```
   This will create all tables and insert seed data.

   Default admin credentials:
   - Username: `admin`
   - Password: `admin123`

7. **Run the application**
   ```bash
   python run.py
   ```

8. **Access the website**
   - Public site: http://localhost:5000
   - Admin panel: http://localhost:5000/admin

## Database Schema

The application uses the following tables:

- **users**: Admin users for authentication
- **projects**: Construction projects (current/completed)
- **services**: Services offered by the company
- **testimonials**: Client testimonials
- **contact_messages**: Contact form submissions
- **team_members**: Company team/staff
- **image_gallery**: Uploaded images management

See `database/schema.sql` for detailed schema.

## Admin Panel Features

- **Dashboard**: Overview with statistics
- **Project Management**: Create, edit, delete projects
- **Service Management**: Manage service offerings
- **Message Management**: View and respond to contact messages
- **Image Gallery**: Upload and manage images

## API Endpoints

### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects?category=current` - Filter by category
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create project (admin only)
- `PUT /api/projects/<id>` - Update project (admin only)
- `DELETE /api/projects/<id>` - Delete project (admin only)

### Services
- `GET /api/services` - List all services
- `GET /api/services/<id>` - Get single service
- `POST /api/services` - Create service (admin only)
- `PUT /api/services/<id>` - Update service (admin only)
- `DELETE /api/services/<id>` - Delete service (admin only)

### Images
- `POST /api/images` - Upload image (admin only)
- `DELETE /api/images/<id>` - Delete image (admin only)

## Color Scheme

- Primary Green: `#006B3B`
- Bright Green: `#00AA44`
- Yellow CTA: `#FFC107`
- Dark Blue: `#1A2332`
- White: `#FFFFFF`

## Fonts

- Headings: Montserrat (700 weight)
- Body: Lato (400/700 weight)

## Security Features

- CSRF protection on all forms
- Password hashing with Werkzeug
- SQL injection prevention (ORM)
- File upload validation (size, extension)
- Session timeout (24 hours)
- Input validation on all forms

## Development

### Reset Database
To reset the database (WARNING: deletes all data):
```bash
python init_db.py --reset
```

### Add New Admin User
Use the Flask shell to add new admin users:
```python
from app import create_app, db
from app.models import User
from app.services.auth_service import hash_password

app = create_app()
with app.app_context():
    user = User(
        username='newadmin',
        email='newadmin@example.com',
        password_hash=hash_password('password'),
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use production database credentials
3. Enable HTTPS
4. Configure email settings for notifications
5. Set up proper logging
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Configure CDN for static files
8. Compress images and minify CSS/JS

## License

This project is proprietary software for Thendral City Developers.

## Support

For support, contact:
- Email: info@thendralcity.com
- Phone: +91 90038 68888
