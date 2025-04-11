# Gas Cylinder Tracking System

A comprehensive system for tracking gas cylinders, their movements, and maintenance. This system includes a backend API built with FastAPI and a frontend web application.

## Features

- User authentication and authorization with role-based access control
- Cylinder management with barcode and QR code generation
- Customer and location management
- Movement tracking for cylinders
- Transaction management
- Maintenance scheduling and tracking
- Analytics and reporting

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pandas for data analysis
- Matplotlib and Seaborn for visualization

### Frontend (Coming Soon)
- React
- TypeScript
- Material-UI
- Redux Toolkit

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Node.js 16+ (for frontend)

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost/gas_tracker
SECRET_KEY=your-secret-key-here
```

4. Run the database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Frontend Setup (Coming Soon)

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/token` - Get access token
- `GET /api/users/me` - Get current user info

### Cylinders
- `POST /api/cylinders/` - Create a new cylinder
- `GET /api/cylinders/` - List all cylinders
- `GET /api/cylinders/{cylinder_id}` - Get cylinder details
- `PUT /api/cylinders/{cylinder_id}` - Update cylinder
- `DELETE /api/cylinders/{cylinder_id}` - Delete cylinder
- `GET /api/cylinders/{cylinder_id}/qr-code` - Get cylinder QR code

### Customers
- `POST /api/customers/` - Create a new customer
- `GET /api/customers/` - List all customers
- `GET /api/customers/{customer_id}` - Get customer details
- `PUT /api/customers/{customer_id}` - Update customer
- `DELETE /api/customers/{customer_id}` - Delete customer
- `POST /api/customers/{customer_id}/locations` - Add customer location
- `GET /api/customers/{customer_id}/locations` - List customer locations

### Movements
- `POST /api/movements/cylinder` - Create cylinder movement
- `GET /api/movements/cylinder` - List all movements
- `GET /api/movements/cylinder/{cylinder_id}` - Get cylinder movement history
- `POST /api/movements/transaction` - Create transaction
- `GET /api/movements/transaction` - List all transactions
- `GET /api/movements/transaction/{transaction_id}` - Get transaction details

### Maintenance
- `POST /api/maintenance/` - Create maintenance record
- `GET /api/maintenance/` - List all maintenance records
- `GET /api/maintenance/cylinder/{cylinder_id}` - Get cylinder maintenance history
- `PUT /api/maintenance/{record_id}` - Update maintenance record
- `GET /api/maintenance/upcoming` - Get upcoming maintenance
- `GET /api/maintenance/overdue` - Get overdue maintenance

### Analytics
- `GET /api/analytics/dashboard` - Get dashboard metrics
- `GET /api/analytics/cylinder-status` - Get cylinder status analytics
- `GET /api/analytics/movement-trends` - Get movement trends
- `GET /api/analytics/maintenance-analytics` - Get maintenance analytics
- `GET /api/analytics/customer-analytics` - Get customer analytics
- `GET /api/analytics/export/report` - Export analytics report

## User Roles

- Admin: Full access to all features
- Manager: Can manage cylinders, customers, and transactions
- Driver: Can perform cylinder movements
- Technician: Can perform maintenance
- Customer: Limited access to their own data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 