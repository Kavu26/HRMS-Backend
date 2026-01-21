# HRMS Lite - Human Resource Management System

A lightweight, full-stack web application for managing employee records and tracking daily attendance.

## Project Overview

HRMS Lite is a modern Human Resource Management System designed to handle essential HR operations. The application consists of a Python FastAPI backend and a React frontend, providing a clean and efficient solution for employee and attendance management.

### Key Features

- ✅ **Employee Management**: Add, view, and delete employee records
- ✅ **Attendance Management**: Mark attendance, view records, edit, and delete entries
- ✅ **Date Filtering**: Filter attendance records by date or date range
- ✅ **Employee Filtering**: Filter attendance by specific employee
- ✅ **Dashboard**: Summary statistics and attendance overview
- ✅ **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- ✅ **RESTful API**: Clean API design with proper error handling
- ✅ **Production Ready**: Deployed and accessible online

## Live Application

- **Frontend**: [https://hrms-frontend-alpha-one.vercel.app/](https://hrms-frontend-alpha-one.vercel.app/)
- **Backend API**: [https://hrms-backend-lite.onrender.com/](https://hrms-backend-lite.onrender.com/)
- **API Documentation**: [https://hrms-backend-lite.onrender.com/docs](https://hrms-backend-lite.onrender.com/docs)

## Tech Stack

### Backend
- **Framework**: FastAPI 0.128.0
- **Database**: SQLite (production-ready, can switch to PostgreSQL)
- **ORM**: SQLAlchemy 2.0.45
- **Validation**: Pydantic 2.12.5
- **Server**: Uvicorn 0.40.0
- **Python**: 3.11+

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Routing**: React Router DOM 6.21.1
- **HTTP Client**: Axios 1.6.5
- **Styling**: Custom CSS with responsive design
- **Node.js**: 18+

## Project Structure

```
HRMS Lite/
├── Backend- HRMS/          # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── database.py     # Database configuration
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Application entry point
│   └── README.md          # Backend documentation
│
└── Frontend-HRMS/          # React frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── services/       # API service layer
    │   ├── App.jsx         # Main app component
    │   └── index.css       # Global styles
    ├── package.json        # Node dependencies
    └── README.md           # Frontend documentation
```

## Steps to Run the Project Locally

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- pip (Python package manager)
- npm or yarn (Node package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd "Backend- HRMS"
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
   ```bash
   python run.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd Frontend-HRMS
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables (optional):**
   
   Create a `.env` file:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Run the frontend development server:**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

### Running Both Services

1. Start the backend server first (Terminal 1):
   ```bash
   cd "Backend- HRMS"
   python run.py
   ```

2. Start the frontend server (Terminal 2):
   ```bash
   cd Frontend-HRMS
   npm run dev
   ```

3. Open your browser and visit `http://localhost:3000`

## API Documentation

Once the backend is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)
- **Health Check**: `http://localhost:8000/health`

## Features in Detail

### Employee Management
- Add new employees with validation (ID, name, email, department)
- View all employees in a responsive table
- Delete employees with confirmation dialog
- Real-time updates after operations

### Attendance Management
- Mark attendance for employees (date and status)
- View all attendance records
- Filter by employee (dropdown selection)
- Filter by date (single date or date range)
- Edit existing attendance records
- Delete attendance records with confirmation
- Real-time updates after operations

### Dashboard
- Total employees count
- Total attendance records count
- Employee attendance summary with:
  - Present days per employee
  - Absent days per employee
  - Total records per employee

## Database

The application uses SQLite by default, which creates a `hrms.db` file automatically. For production, you can switch to PostgreSQL by setting the `DATABASE_URL` environment variable.

## Assumptions & Limitations

### Assumptions

1. **Single Admin User**: No authentication required (single admin assumed)
2. **Unique Identifiers**: Employee IDs and emails must be unique
3. **One Record Per Day**: Only one attendance record per employee per date
4. **Modern Browser**: Users have modern browsers with JavaScript enabled

### Limitations

1. **No Authentication**: No user login or role-based access control
2. **No Employee Editing**: Employees can only be created or deleted (not edited)
3. **Limited Status Types**: Attendance supports only "Present" and "Absent"
4. **No Payroll Features**: Payroll management is out of scope
5. **No Leave Management**: Leave management features not included
6. **No Pagination**: All records loaded at once (may be slow with large datasets)
7. **No Data Export**: Cannot export data to CSV/Excel
8. **No Offline Support**: Requires active backend connection

## Deployment

### Backend Deployment (Render)

1. Connect GitHub repository
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables if needed (e.g., `DATABASE_URL`)

### Frontend Deployment (Vercel)

1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variable: `VITE_API_URL` = your backend URL
5. Deploy

## Development

### Backend Development

- API follows RESTful principles
- Comprehensive error handling
- Input validation with Pydantic
- SQLAlchemy ORM for database operations

### Frontend Development

- Component-based architecture
- Responsive design with mobile-first approach
- API service layer for clean separation
- Modern React hooks (useState, useEffect)

## Testing the Application

1. **Add Employees**: Navigate to Employees page and add test employees
2. **Mark Attendance**: Go to Attendance page and mark attendance for employees
3. **View Dashboard**: Check the Dashboard for summary statistics
4. **Test Filters**: Use employee and date filters in Attendance page
5. **Edit/Delete**: Test editing and deleting attendance records

## License

This project is developed as part of an HRMS Lite assignment.

## Contact & Support

For issues or questions, please refer to the individual README files in the backend and frontend directories.
