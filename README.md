# Astrology Project - Backend

FastAPI backend for the Astrology project with real-time asteroid tracking using NASA's NeoWs API.

## Features

- **User Authentication**: JWT-based authentication with bcrypt password hashing
- **Real-time Asteroid Data**: Server-Sent Events (SSE) streaming of near-Earth objects
- **MongoDB Integration**: User data and asteroid information storage
- **NASA API Integration**: Live data from NASA's Near Earth Object Web Service

## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (or local MongoDB instance)
- NASA API key (get one at https://api.nasa.gov/)

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# MongoDB Configuration
MONGO_URI=your_mongodb_connection_string

# NASA API Configuration
NASA_API_KEY=your_nasa_api_key

# JWT Authentication Configuration
SECRET_KEY=your_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (comma-separated origins)
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Important:** Replace the placeholder values with your actual credentials.

### 5. Run the Server

**Development mode with auto-reload:**
```bash
python -m uvicorn main:app --reload
```

**Production mode:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start at `http://127.0.0.1:8000`

## API Endpoints

### Authentication

- `POST /register` - Register a new user
- `POST /login` - Login and receive JWT token
- `GET /protected` - Protected endpoint (requires authentication)

### Asteroid Data

- `GET /asteroids` - SSE stream of real-time asteroid data

## Project Structure

```
backend/
├── database/
│   └── db.py              # MongoDB connection
├── middleware/
│   └── auth.py            # JWT authentication
├── models/                # Data models
├── routes/
│   ├── userroute.py       # User authentication routes
│   └── astroidshow.py     # Asteroid data SSE endpoint
├── schemas/
│   └── UserSchema.py      # Pydantic schemas
├── .env                   # Environment variables (not in git)
├── main.py                # FastAPI application entry point
└── requirements.txt       # Python dependencies
```

## Security Notes

- Never commit `.env` file to version control
- Use strong, randomly generated SECRET_KEY in production
- Update ALLOWED_ORIGINS to match your frontend domain in production
- Keep your NASA API key private

## Troubleshooting

**Import errors:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**MongoDB connection errors:**
- Verify MONGO_URI in `.env` is correct
- Check MongoDB Atlas IP whitelist settings
- Ensure network connectivity

**SSE connection issues:**
- Verify CORS settings allow your frontend origin
- Check that NASA API key is valid
- Monitor server logs for errors
