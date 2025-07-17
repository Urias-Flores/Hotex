# Hotex

Hotex is a hotel management system built with Django. It provides a web-based interface for managing reservations, guests, rooms, buildings, and maintenance operations. The system is designed for hotel staff and administrators to streamline daily operations and improve guest experience.

## Features

- Dashboard with daily arrivals, departures, and quick actions
- Manage reservations: create, edit, delete, and view bookings
- Manage guests: add, edit, and remove guest information
- Manage rooms and buildings: add, edit, delete, and view details
- Room availability tracking and status display
- Maintenance management for rooms
- Authentication for secure access
- Responsive web interface with modern UI

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Urias-Flores/Hotex.git
   cd Hotex
   ```

2. **Create and activate a virtual environment (recommended):**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install django
   pip install django-browser-reload
   ```
   *(Add any other dependencies found in the code as needed)*

4. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin account):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the app:**
   Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

- Log in with your admin or staff account.
- Use the dashboard to view arrivals, departures, and quick actions.
- Navigate to Reservations, Guests, Rooms, or Maintenance to manage each entity.
- Use the settings page for additional configuration.

## Project Structure

- `Hotex/` – Django project configuration
- `hotex_app/` – Main application logic (models, views, forms, templates, static files)
- `manage.py` – Django management script
- `db.sqlite3` – SQLite database (default)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- Built with [Django](https://www.djangoproject.com/)
- UI inspired by modern hotel management systems

---

*For any questions or support, please open an issue on GitHub.*
