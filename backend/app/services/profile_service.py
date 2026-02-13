"""
Profile Service - Manages investor profiles.
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.db_models import InvestorProfile
from app.models.investor_dna import InvestorDNA, RiskTolerance, DEFAULT_INVESTOR_DNA


# Mapping from UI ethical filter names to InvestorDNA field names
ETHICAL_FILTER_MAP = {
    "No Tobacco": "exclude_tobacco",
    "No Alcohol": "exclude_alcohol",
    "No Gambling": "exclude_gambling",
    "No Weapons": "exclude_weapons",
    "ESG Focused": "exclude_fossil_fuels",  # ESG typically excludes fossil fuels
    "Renewable Energy Only": "exclude_fossil_fuels",  # Also excludes fossil fuels
}

# Mapping from UI risk tolerance to InvestorDNA RiskTolerance enum
RISK_TOLERANCE_MAP = {
    "conservative": RiskTolerance.CONSERVATIVE,
    "medium": RiskTolerance.MODERATE,
    "moderate": RiskTolerance.MODERATE,
    "aggressive": RiskTolerance.AGGRESSIVE,
}


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
            "investment_horizon": profile.investment_horizon or "3-5 years",
            "investment_goals": profile.investment_goals or [],
            "sectors": profile.sectors or [],
            "ethical_filters": profile.ethical_filters or [],
            "custom_rules": profile.custom_rules or []
        }
    
    def get_investor_dna(self, db: Session, user_id: str) -> InvestorDNA:
        """
        Get InvestorDNA object for a user, properly mapped from DB fields.
        This converts ethical_filters list to exclude_* booleans.
        """
        try:
            user_id_int = int(user_id)
        except ValueError:
            return DEFAULT_INVESTOR_DNA
        
        profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == user_id_int).first()
        
        if not profile:
            return DEFAULT_INVESTOR_DNA
        
        # Map risk tolerance string to enum
        risk_str = (profile.risk_tolerance or "moderate").lower()
        risk_tolerance = RISK_TOLERANCE_MAP.get(risk_str, RiskTolerance.MODERATE)
        
        # Map ethical filters list to individual booleans
        ethical_filters = profile.ethical_filters or []
        exclude_tobacco = any(f in ethical_filters for f in ["No Tobacco", "no tobacco"])
        exclude_alcohol = any(f in ethical_filters for f in ["No Alcohol", "no alcohol"])
        exclude_gambling = any(f in ethical_filters for f in ["No Gambling", "no gambling"])
        exclude_weapons = any(f in ethical_filters for f in ["No Weapons", "no weapons"])
        exclude_fossil = any(f in ethical_filters for f in ["ESG Focused", "Renewable Energy Only", "esg focused", "renewable energy only"])
        
        # Build InvestorDNA
        return InvestorDNA(
            user_id=str(user_id_int),
            risk_tolerance=risk_tolerance,
            time_horizon=profile.time_horizon or 5,
            custom_rules=profile.custom_rules or [],
            exclude_tobacco=exclude_tobacco,
            exclude_alcohol=exclude_alcohol,
            exclude_gambling=exclude_gambling,
            exclude_weapons=exclude_weapons,
            exclude_fossil_fuels=exclude_fossil,
        )
    
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

