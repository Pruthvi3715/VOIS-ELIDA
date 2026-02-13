"""
Fix demo account password
"""

import sys
sys.path.append(".")

from app.database import SessionLocal
from app.models.db_models import User
from app.auth.auth import hash_password, verify_password

db = SessionLocal()

try:
    # Find demo user
    demo_user = db.query(User).filter(User.username == "demo").first()

    if demo_user:
        print(f"Found demo user (ID: {demo_user.id})")

        # Update password
        new_password = "demo123"
        demo_user.hashed_password = hash_password(new_password)

        db.commit()

        print("[OK] Password updated!")

        # Verify it works
        if verify_password(new_password, demo_user.hashed_password):
            print("[OK] Password verified successfully!")
            print("\nDemo Login Credentials:")
            print("  Username: demo")
            print("  Password: demo123")
        else:
            print("[ERROR] Password verification still failing!")
    else:
        print("[ERROR] Demo user not found!")

finally:
    db.close()
