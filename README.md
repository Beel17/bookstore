# 📚 Bookstore Web Application

A complete bookstore management system built with **FastAPI** backend and **Bootstrap** frontend, featuring user authentication, book management, order processing, and Paystack payment integration.

## 🚀 Features

### Core Functionality
- **User Authentication**: JWT-based login/signup system with role-based access (user/admin)
- **Book Management**: Full CRUD operations for books (admin only)
- **Order Processing**: Create and manage orders with inventory tracking
- **Payment Integration**: Paystack payment gateway for secure transactions
- **Responsive Frontend**: Bootstrap-based UI with mobile support
- **API Documentation**: Auto-generated Swagger docs at `/docs`

### Technical Features
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy ORM**: Database abstraction with PostgreSQL support
- **JWT Authentication**: Secure token-based authentication
- **Docker Ready**: Complete containerization with docker-compose
- **Unit Tests**: Comprehensive test coverage with pytest
- **Environment Configuration**: Flexible config management

## 🏗️ Architecture

```
bookstore/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for request/response validation
│   ├── auth/                # Authentication module
│   │   ├── routes.py        # Auth endpoints (login, signup, me)
│   │   └── utils.py         # JWT utilities and password hashing
│   ├── books/               # Book management module
│   │   ├── routes.py        # Book CRUD endpoints
│   │   └── crud.py          # Database operations for books
│   ├── orders/              # Order and payment module
│   │   ├── routes.py        # Order endpoints
│   │   └── payments.py      # Paystack integration
│   ├── tests/               # Unit tests
│   │   └── test_endpoints.py
│   └── templates/           # HTML templates with Bootstrap
│       ├── base.html        # Base template
│       ├── index.html       # Home page with book catalog
│       ├── login.html       # Authentication page
│       ├── admin.html       # Admin panel for book management
│       └── checkout.html    # Payment checkout page
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── nginx.conf              # Nginx reverse proxy config
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for development)
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bookstore
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # For PostgreSQL
   createdb bookstore_db
   
   # Or use SQLite (default for development)
   # No additional setup required
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:8000/index

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - API: http://localhost:8000
   - Frontend: http://localhost (via Nginx)

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/bookstore_db
SQLITE_DATABASE_URL=sqlite:///./bookstore.db

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Paystack
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_public_key

# Environment
ENVIRONMENT=development
```

### Paystack Setup

1. Create an account at [Paystack](https://paystack.com)
2. Get your API keys from the dashboard
3. Update the `.env` file with your keys
4. Configure webhook URLs in Paystack dashboard

## 📖 API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `GET /auth/admin-only` - Admin-only test endpoint

### Books
- `GET /books/` - List all books (with search and pagination)
- `GET /books/{id}` - Get book details
- `POST /books/` - Create book (admin only)
- `PUT /books/{id}` - Update book (admin only)
- `DELETE /books/{id}` - Delete book (admin only)
- `GET /books/isbn/{isbn}` - Get book by ISBN

### Orders
- `POST /orders/` - Create new order
- `GET /orders/` - Get user orders
- `GET /orders/{id}` - Get order details
- `POST /orders/payment/initiate` - Initiate payment
- `POST /orders/payment/verify` - Verify payment

### Frontend Pages
- `GET /` - API root
- `GET /health` - Health check
- `GET /index` - Book catalog page
- `GET /login` - Authentication page
- `GET /admin` - Admin panel
- `GET /checkout/{order_id}` - Checkout page

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest app/tests/

# Run with coverage
pytest --cov=app app/tests/
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export SECRET_KEY=your-secure-secret-key
   export PAYSTACK_SECRET_KEY=sk_live_your_live_key
   ```

2. **Database Migration**
   ```bash
   # The app automatically creates tables on startup
   # For production, consider using Alembic for migrations
   ```

3. **Docker Deployment**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Platform Deployment

#### Render.com
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy with Dockerfile

#### Fly.io
1. Install Fly CLI
2. Run `fly launch`
3. Configure secrets: `fly secrets set SECRET_KEY=...`
4. Deploy: `fly deploy`

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth with configurable expiration
- **Password Hashing**: bcrypt for secure password storage
- **Role-based Access**: Admin and user roles with proper authorization
- **CORS Configuration**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🎨 Frontend Features

- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Real-time Updates**: JavaScript fetch API for dynamic content
- **User Experience**: Loading states, error handling, success messages
- **Admin Panel**: Full CRUD interface for book management
- **Payment Flow**: Seamless Paystack integration with redirect handling

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `hashed_password`: bcrypt hashed password
- `role`: User role (user/admin)
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Books Table
- `id`: Primary key
- `title`: Book title
- `author`: Book author
- `description`: Book description
- `price`: Book price
- `stock_quantity`: Available quantity
- `isbn`: Unique ISBN
- `image_url`: Book cover image
- `is_active`: Book status
- `created_at`, `updated_at`: Timestamps

### Orders Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `total_amount`: Order total
- `status`: Order status (pending/completed/cancelled)
- `payment_status`: Payment status (pending/success/failed)
- `payment_reference`: Unique payment reference
- `created_at`, `updated_at`: Timestamps

### Order Items Table
- `id`: Primary key
- `order_id`: Foreign key to orders
- `book_id`: Foreign key to books
- `quantity`: Item quantity
- `price`: Price at time of order

### Payments Table
- `id`: Primary key
- `order_id`: Foreign key to orders
- `reference`: Unique payment reference
- `amount`: Payment amount
- `status`: Payment status
- `paystack_reference`: Paystack transaction reference
- `gateway_response`: Raw Paystack response
- `created_at`, `updated_at`: Timestamps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test files for usage examples

## 🔮 Future Enhancements

- [ ] Email notifications for orders
- [ ] Advanced search and filtering
- [ ] Book reviews and ratings
- [ ] Inventory alerts
- [ ] Analytics dashboard
- [ ] Mobile app API
- [ ] Multi-language support
- [ ] Advanced payment methods

---

**Built with ❤️ using FastAPI, SQLAlchemy, and Bootstrap**
