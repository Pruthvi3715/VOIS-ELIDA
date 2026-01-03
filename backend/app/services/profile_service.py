"""
Profile Service - Manages investor profiles.
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.db_models import InvestorProfile
from app.models.investor_dna import DEFAULT_INVESTOR_DNA


class ProfileService:
    """Service for managing investor profiles."""
    
    def get_profile_by_user_id(self, db: Session, user_id: str) -> Dict[str, Any]:
        """
        Get investor profile by user ID.
        Returns default profile if user not found.
        """
        try:
            user_id_int = int(user_id)
        except ValueError:
            return DEFAULT_INVESTOR_DNA.model_dump()
        
        profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == user_id_int).first()
        
        if not profile:
            return DEFAULT_INVESTOR_DNA.model_dump()
        
        return {
            "risk_tolerance": profile.risk_tolerance,
            "time_horizon": profile.time_horizon,
            "investment_goals": profile.investment_goals or [],
            "sectors": profile.sectors or [],
            "custom_rules": profile.custom_rules or []
        }
    
    def update_profile(self, db: Session, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update investor profile."""
        profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == user_id).first()
        
        if not profile:
            # Create new profile
            profile = InvestorProfile(user_id=user_id, **data)
            db.add(profile)
        else:
            # Update existing
            for key, value in data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
        
        db.commit()
        db.refresh(profile)
        
        return self.get_profile_by_user_id(db, str(user_id))


profile_service = ProfileService()
