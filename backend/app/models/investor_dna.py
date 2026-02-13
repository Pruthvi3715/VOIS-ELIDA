"""
Investor DNA Profile Model
Defines the user's investment preferences, risk tolerance, and constraints.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class RiskTolerance(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class InvestmentStyle(str, Enum):
    VALUE = "value"
    GROWTH = "growth"
    DIVIDEND = "dividend"
    INDEX = "index"
    BLEND = "blend"


class HoldingPeriod(str, Enum):
    SHORT = "short"      # < 1 year
    MEDIUM = "medium"    # 1-5 years
    LONG = "long"        # 5+ years


class InvestorDNA(BaseModel):
    """
    Complete Investor DNA Profile.
    This captures all user preferences for personalized recommendations.
    """
    
    # Basic Info
    user_id: str = Field(default="default_user")
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Risk Profile
    risk_tolerance: RiskTolerance = Field(
        default=RiskTolerance.MODERATE,
        description="Overall risk tolerance level"
    )
    max_single_stock_allocation: float = Field(
        default=10.0,
        ge=1.0,
        le=100.0,
        description="Maximum % of portfolio in single stock"
    )
    max_sector_allocation: float = Field(
        default=30.0,
        ge=5.0,
        le=100.0,
        description="Maximum % of portfolio in single sector"
    )
    
    # Investment Style
    investment_style: InvestmentStyle = Field(
        default=InvestmentStyle.BLEND,
        description="Preferred investment approach"
    )
    holding_period: HoldingPeriod = Field(
        default=HoldingPeriod.LONG,
        description="Typical holding period for investments"
    )
    
    # Ethical Filters (sectors to exclude)
    exclude_tobacco: bool = Field(default=False, description="Exclude tobacco companies")
    exclude_alcohol: bool = Field(default=False, description="Exclude alcohol companies")
    exclude_gambling: bool = Field(default=False, description="Exclude gambling companies")
    exclude_weapons: bool = Field(default=False, description="Exclude weapons/defense companies")
    exclude_fossil_fuels: bool = Field(default=False, description="Exclude oil/gas/coal companies")
    custom_exclusions: List[str] = Field(
        default=[],
        description="Custom sectors or companies to exclude"
    )
    custom_rules: List[str] = Field(
        default=[],
        description="Custom rules or sentences to consider (e.g. 'I hate crypto')"
    )
    
    # Market Preferences
    preferred_markets: List[str] = Field(
        default=["IN", "US"],
        description="Preferred markets (IN=India, US=USA, etc.)"
    )
    nifty_50_only: bool = Field(
        default=False,
        description="Only consider Nifty 50 stocks for Indian equities"
    )
    min_market_cap: Optional[str] = Field(
        default="1B",
        description="Minimum market cap (e.g., 1B, 10B, 100B)"
    )
    
    # Valuation Preferences
    max_pe_ratio: Optional[float] = Field(
        default=50.0,
        description="Maximum acceptable P/E ratio"
    )
    min_dividend_yield: Optional[float] = Field(
        default=0.0,
        description="Minimum dividend yield %"
    )
    prefer_profitable: bool = Field(
        default=True,
        description="Prefer companies with positive earnings"
    )
    
    # Technical Preferences
    avoid_52w_highs: bool = Field(
        default=False,
        description="Avoid stocks at 52-week highs"
    )
    prefer_oversold: bool = Field(
        default=False,
        description="Prefer oversold stocks (RSI < 30)"
    )

    # Fields matching DB Model (Backwards Compatibility/Expansion)
    time_horizon: int = Field(default=5, description="Investment horizon in years")
    investment_goals: List[str] = Field(default=["growth"], description="Investment goals")
    sectors: List[str] = Field(default=[], description="Preferred sectors")
    max_drawdown_tolerance: float = Field(default=20.0, description="Max drawdown tolerance %")
    min_position_size: float = Field(default=1000.0, description="Min position size")
    max_position_size: float = Field(default=10000.0, description="Max position size")
    esg_preference: str = Field(default="neutral", description="ESG preference")
    liquidity_requirement: str = Field(default="medium", description="Liquidity requirement")
    
    def get_excluded_sectors(self) -> List[str]:
        """Get list of excluded sectors based on ethical filters."""
        excluded = []
        if self.exclude_tobacco:
            excluded.extend(["Tobacco", "Cigarettes"])
        if self.exclude_alcohol:
            excluded.extend(["Alcoholic Beverages", "Brewers", "Distillers"])
        if self.exclude_gambling:
            excluded.extend(["Casinos & Gaming", "Gambling"])
        if self.exclude_weapons:
            excluded.extend(["Aerospace & Defense", "Weapons"])
        if self.exclude_fossil_fuels:
            excluded.extend(["Oil & Gas", "Coal", "Fossil Fuels"])
        excluded.extend(self.custom_exclusions)
        return excluded
    
    def get_risk_score_range(self) -> tuple:
        """Get acceptable risk score range based on tolerance."""
        if self.risk_tolerance == RiskTolerance.CONSERVATIVE:
            return (0, 40)  # Only low risk
        elif self.risk_tolerance == RiskTolerance.MODERATE:
            return (20, 70)  # Low to medium risk
        else:  # AGGRESSIVE
            return (40, 100)  # Accept higher risk


class MatchScoreBreakdown(BaseModel):
    """Breakdown of how Match Score was calculated."""
    
    fundamental_score: float = Field(description="Score from Quant Agent (0-100)")
    fundamental_weight: float = 0.35
    
    macro_score: float = Field(description="Score from Macro alignment (0-100)")
    macro_weight: float = 0.10
    
    philosophy_score: float = Field(description="Score from Philosopher Agent (0-100)")
    philosophy_weight: float = 0.10
    
    risk_score: float = Field(description="Inverted risk score (0-100)")
    risk_weight: float = 0.20
    
    dna_match_score: float = Field(description="How well it matches Investor DNA (0-100)")
    dna_weight: float = 0.25
    
    @property
    def total_score(self) -> float:
        """Calculate weighted total score."""
        return (
            self.fundamental_score * self.fundamental_weight +
            self.macro_score * self.macro_weight +
            self.philosophy_score * self.philosophy_weight +
            self.risk_score * self.risk_weight +
            self.dna_match_score * self.dna_weight
        )
    
    @property
    def confidence_level(self) -> str:
        """Get confidence level label."""
        score = self.total_score
        if score >= 80:
            return "Very High"
        elif score >= 65:
            return "High"
        elif score >= 50:
            return "Moderate"
        elif score >= 35:
            return "Low"
        else:
            return "Very Low"


class MatchResult(BaseModel):
    """Final match result for an asset against investor DNA."""
    
    asset_id: str
    match_score: int = Field(ge=0, le=100, description="Overall match percentage")
    breakdown: MatchScoreBreakdown
    
    # Recommendation
    recommendation: str = Field(description="Buy/Hold/Don't Add/Avoid")
    action_if_owned: str = Field(description="Hold/Reduce/Exit")
    action_if_not_owned: str = Field(description="Buy/Wait/Avoid")
    
    # Reasons
    fit_reasons: List[str] = Field(description="Why it fits the investor")
    concern_reasons: List[str] = Field(description="Concerns or mismatches")
    
    # Summary
    summary: str = Field(description="Human-readable summary")


# Default profile for users without customization
DEFAULT_INVESTOR_DNA = InvestorDNA(
    user_id="default",
    name="Default Investor",
    risk_tolerance=RiskTolerance.MODERATE,
    investment_style=InvestmentStyle.BLEND,
    holding_period=HoldingPeriod.LONG,
)
