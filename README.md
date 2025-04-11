# Gas Tracker Application

A full-stack application for tracking gas usage and expenses, built with FastAPI and React.

## Features

- User authentication and authorization
- Gas usage tracking and analytics
- QR code generation for quick data entry
- Data visualization and reporting
- Responsive web interface

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Alembic for database migrations

### Frontend
- React
- TypeScript
- Material-UI
- Chart.js for visualizations

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Evanevoo/evass.git
cd evass
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost/gas_tracker
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
```

### Running the Application

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm start
```

## Deployment

The application is configured for deployment on Render. The `render.yaml` file contains all necessary configuration for:
- PostgreSQL database setup
- Backend service deployment
- Environment variable configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- FastAPI team for the amazing framework
- React team for the frontend library
- All contributors who have helped shape this project 