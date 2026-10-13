from typing import TypedDict, Optional, List, Dict, Any


class LeadState(TypedDict, total=False):

    # Input
    url: str
    leads: List[Dict[str, Any]]
    current_lead: Dict[str, Any]

    # Website discovery
    website: Optional[str]
    website_source: Optional[str]

    # Website analyzer
    website_exists: bool
    website_reachable: bool
    https: bool
    mobile_friendly: bool
    business_information: bool
    contact_information: bool
    services_listed: bool
    social_links: bool
    website_quality_score: int

    strengths: List[str]
    weaknesses: List[str]
    summary: str

    # Final
    analyzed_leads: List[Dict[str, Any]]