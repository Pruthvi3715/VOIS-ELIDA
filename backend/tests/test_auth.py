"""
Tests for authentication and authorization.
"""
import pytest
from app.auth.auth import hash_password, verify_password, create_access_token, decode_token


class TestPasswordHashing:
    """Tests for password hashing utilities."""
    
    def test_hash_password_returns_hash(self):
        """Hash function should return a bcrypt hash."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert hashed.startswith("$2b$")  # bcrypt prefix
    
    def test_verify_correct_password(self):
        """Correct password should verify successfully."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_wrong_password(self):
        """Wrong password should fail verification."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert verify_password("wrong_password", hashed) is False


class TestJWTTokens:
    """Tests for JWT token handling."""
    
    def test_create_token(self):
        """Token creation should return a valid JWT string."""
        token = create_access_token({"sub": "123"})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are typically long
    
    def test_decode_valid_token(self):
        """Valid token should decode successfully."""
        data = {"sub": "user_123"}
        token = create_access_token(data)
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == "user_123"
    
    def test_decode_invalid_token(self):
        """Invalid token should return None."""
        payload = decode_token("invalid.token.here")
        
        assert payload is None
    
    def test_token_contains_expiry(self):
        """Token payload should contain expiry time."""
        token = create_access_token({"sub": "123"})
        payload = decode_token(token)
        
        assert "exp" in payload


class TestUserRegistration:
    """Tests for user registration logic via DB."""
    
    def test_create_user(self, test_db):
        """Should be able to create a user with username and email."""
        from app.models.db_models import User
        
        user = User(
            username="newuser",
            email="new@example.com",
            hashed_password="hashed_secret"
        )
        test_db.add(user)
        test_db.commit()
        
        saved = test_db.query(User).filter_by(username="newuser").first()
        assert saved is not None
        assert saved.email == "new@example.com"

    def test_duplicate_username_fails(self, test_db, sample_user):
        """Duplicate username should raise IntegrityError."""
        from app.models.db_models import User
        from sqlalchemy.exc import IntegrityError
        
        user = User(
            username=sample_user.username,  # Duplicate
            email="another@example.com",
            hashed_password="pass"
        )
        test_db.add(user)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
            
    def test_duplicate_email_fails(self, test_db, sample_user):
        """Duplicate email should raise IntegrityError."""
        from app.models.db_models import User
        from sqlalchemy.exc import IntegrityError
        
        user = User(
            username="unique_user",
            email=sample_user.email,  # Duplicate
            hashed_password="pass"
        )
        test_db.add(user)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
