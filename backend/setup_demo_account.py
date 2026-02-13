"""
Create a demo account for easy testing and hackathon demos.
Credentials: demo / demo123
"""

import sys
sys.path.append(".")

from app.database import SessionLocal, init_db
from app.models.db_models import User, InvestorProfile
from app.auth.auth import hash_password
from sqlalchemy import inspect

def create_demo_user():
    """Create a demo user with pre-configured investor profile."""

    print("="*80)
    print("ELIDA - Demo Account Setup")
    print("="*80)

    # Initialize database
    init_db()
    db = SessionLocal()

    try:
        # Check if demo user already exists
        existing_demo = db.query(User).filter(User.username == "demo").first()

        if existing_demo:
            print("\n[INFO] Demo user already exists!")
            print(f"  Username: demo")
            print(f"  Password: demo123")
            print(f"  User ID: {existing_demo.id}")

            # Check if profile exists
            profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == existing_demo.id).first()
            if profile:
                print(f"  Profile: Configured (Risk: {profile.risk_tolerance})")
            else:
                print("  Profile: Missing - Creating...")
                demo_profile = InvestorProfile(
                    user_id=existing_demo.id,
                    risk_tolerance="moderate",
                    time_horizon=5,
                    investment_goals=["growth", "income"],
                    sectors=["Technology", "Healthcare", "Finance"],
                    custom_rules=[]
                )
                db.add(demo_profile)
                db.commit()
                print("  Profile: Created!")

            return existing_demo

        # Create new demo user
        print("\n[CREATING] New demo user...")

        demo_user = User(
            username="demo",
            email="demo@elida.app",
            hashed_password=hash_password("demo123")
        )

        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        print(f"[OK] User created (ID: {demo_user.id})")

        # Create investor profile
        print("[CREATING] Investor profile...")

        demo_profile = InvestorProfile(
            user_id=demo_user.id,
            risk_tolerance="moderate",  # Balanced risk
            time_horizon=5,  # 5 years
            investment_goals=["growth", "income"],
            sectors=["Technology", "Healthcare", "Finance"],
            custom_rules=[]
        )

        db.add(demo_profile)
        db.commit()

        print("[OK] Profile created")

        print("\n" + "="*80)
        print("DEMO ACCOUNT READY!")
        print("="*80)
        print("\nLogin Credentials:")
        print("  Username: demo")
        print("  Password: demo123")
        print("\nInvestor DNA Profile:")
        print(f"  Risk Tolerance: {demo_profile.risk_tolerance}")
        print(f"  Time Horizon: {demo_profile.time_horizon} years")
        print(f"  Goals: {', '.join(demo_profile.investment_goals)}")
        print(f"  Preferred Sectors: {', '.join(demo_profile.sectors)}")
        print("\n" + "="*80)

        return demo_user

    except Exception as e:
        print(f"\n[ERROR] Failed to create demo user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def verify_demo_login():
    """Test that demo login works."""
    from app.auth.auth import verify_password

    print("\n[TEST] Verifying demo login...")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "demo").first()
        if not user:
            print("[ERROR] Demo user not found!")
            return False

        # Test password
        if verify_password("demo123", user.hashed_password):
            print("[OK] Demo login credentials verified!")
            return True
        else:
            print("[ERROR] Password verification failed!")
            return False
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_user()
    verify_demo_login()

    print("\n[READY] You can now login with:")
    print("  http://localhost:5173")
    print("  Username: demo")
    print("  Password: demo123")
