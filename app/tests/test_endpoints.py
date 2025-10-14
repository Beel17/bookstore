import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models import User, Book
from app.auth.utils import get_password_hash
from app.config import settings

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(setup_database):
    """Create a test user"""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def test_admin(setup_database):
    """Create a test admin user"""
    db = TestingSessionLocal()
    admin = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("adminpassword"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    yield admin
    db.delete(admin)
    db.commit()
    db.close()

@pytest.fixture
def test_book(setup_database):
    """Create a test book"""
    db = TestingSessionLocal()
    book = Book(
        title="Test Book",
        author="Test Author",
        description="A test book description",
        price=29.99,
        stock_quantity=10,
        isbn="1234567890"
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    yield book
    db.delete(book)
    db.commit()
    db.close()

def get_auth_headers(email: str, password: str):
    """Get authentication headers for a user"""
    response = client.post("/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {}

class TestAuth:
    def test_signup(self, setup_database):
        """Test user signup"""
        response = client.post("/auth/signup", json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"

    def test_signup_duplicate_email(self, test_user):
        """Test signup with duplicate email"""
        response = client.post("/auth/signup", json={
            "email": "test@example.com",
            "username": "differentuser",
            "password": "password"
        })
        assert response.status_code == 400

    def test_login(self, test_user):
        """Test user login"""
        response = client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "testpassword"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_get_current_user(self, test_user):
        """Test getting current user info"""
        headers = get_auth_headers("test@example.com", "testpassword")
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"

    def test_protected_route_without_token(self):
        """Test accessing protected route without token"""
        response = client.get("/auth/me")
        assert response.status_code == 401

class TestBooks:
    def test_get_books(self):
        """Test getting all books"""
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_book_admin(self, test_admin):
        """Test creating a book as admin"""
        headers = get_auth_headers("admin@example.com", "adminpassword")
        book_data = {
            "title": "New Book",
            "author": "New Author",
            "description": "A new book",
            "price": 19.99,
            "stock_quantity": 5,
            "isbn": "9876543210"
        }
        response = client.post("/books/", json=book_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Book"

    def test_create_book_user(self, test_user):
        """Test creating a book as regular user (should fail)"""
        headers = get_auth_headers("test@example.com", "testpassword")
        book_data = {
            "title": "Unauthorized Book",
            "author": "Unauthorized Author",
            "price": 15.99,
            "stock_quantity": 3
        }
        response = client.post("/books/", json=book_data, headers=headers)
        assert response.status_code == 403

    def test_get_book_by_id(self, test_book):
        """Test getting a book by ID"""
        response = client.get(f"/books/{test_book.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_book.id
        assert data["title"] == "Test Book"

    def test_update_book_admin(self, test_admin, test_book):
        """Test updating a book as admin"""
        headers = get_auth_headers("admin@example.com", "adminpassword")
        update_data = {"price": 35.99}
        response = client.put(f"/books/{test_book.id}", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 35.99

    def test_delete_book_admin(self, test_admin, test_book):
        """Test deleting a book as admin"""
        headers = get_auth_headers("admin@example.com", "adminpassword")
        response = client.delete(f"/books/{test_book.id}", headers=headers)
        assert response.status_code == 200

class TestOrders:
    def test_create_order(self, test_user, test_book):
        """Test creating an order"""
        headers = get_auth_headers("test@example.com", "testpassword")
        order_data = {
            "order_items": [
                {
                    "book_id": test_book.id,
                    "quantity": 2
                }
            ]
        }
        response = client.post("/orders/", json=order_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user.id
        assert len(data["order_items"]) == 1

    def test_get_user_orders(self, test_user):
        """Test getting user orders"""
        headers = get_auth_headers("test@example.com", "testpassword")
        response = client.get("/orders/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_order_insufficient_stock(self, test_user, test_book):
        """Test creating an order with insufficient stock"""
        headers = get_auth_headers("test@example.com", "testpassword")
        order_data = {
            "order_items": [
                {
                    "book_id": test_book.id,
                    "quantity": 999  # More than available stock
                }
            ]
        }
        response = client.post("/orders/", json=order_data, headers=headers)
        assert response.status_code == 400

class TestRoot:
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
