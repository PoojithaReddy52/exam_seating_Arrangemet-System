# Exam Seating Arrangement System (Flask Version)

A web application developed to help students find their examination halls and seat numbers during semester exams. This is a Flask-based implementation of the original PHP version.

## Features

- Search by roll number to find examination classroom
- Search by class, year, and branch to see complete class allocation
- View examination hall allocations
- Admin panel for managing seating arrangements
- CSV import for student and subject data
- Responsive design using Bootstrap

## Technology Stack

- **Backend**: Python Flask
- **Database**: MongoDB Atlas
- **Frontend**: HTML, Bootstrap 5
- **Authentication**: Flask-Login

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd exam_seating_flask
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
MONGODB_URI=your_mongodb_atlas_connection_string
SECRET_KEY=your_secret_key_here
```

5. Initialize the database:
```bash
python app.py
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Default admin credentials:
   - Username: admin
   - Password: admin123

## Project Structure

```
exam_seating_flask/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── models/               # Database models
│   ├── models.py        # Data models
│   └── database.py      # Database connection and utilities
├── controllers/          # Route controllers
│   ├── admin_controller.py
│   └── student_controller.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── admin/
│   └── student/
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── uploads/             # Uploaded files
```

## CSV Import Format

### Student Data (students.csv)
```
roll_number,name,branch,year
```

### Subject Data (subjects.csv)
```
code,name,semester
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Change the default admin password in production
- Use environment variables for sensitive data
- Implement proper password hashing
- Use HTTPS in production

## Support

For support, please open an issue in the repository or contact the maintainers. 