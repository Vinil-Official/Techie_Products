import requests

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from state import LeadState


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}


# ============================================================
# FETCH WEBSITE
# ============================================================

def fetch_website(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )

        if 200 <= response.status_code < 400:

            return response

    except Exception as e:

        print(
            "Website request error:",
            e
        )

    return None


# ============================================================
# WEBSITE ANALYZER
# ============================================================

def website_analyzer(state: LeadState):

    lead = state.get(
        "current_lead",
        {}
    )

    website = state.get(
        "website"
    )

    print()
    print("=" * 55)
    print("       WEBSITE ANALYZER")
    print("=" * 55)

    print(
        "Lead    :",
        lead.get("name")
    )

    print(
        "Website :",
        website
    )

    # ========================================================
    # NO WEBSITE
    # ========================================================

    if not website:

        return {

            "website_exists": False,

            "website_reachable": False,

            "https": False,

            "mobile_friendly": False,

            "business_information": False,

            "contact_information": False,

            "services_listed": False,

            "social_links": False,

            "website_quality_score": 0,

            "strengths": [],

            "weaknesses": [
                "No official website found"
            ],

            "summary": (
                "No official website was found "
                "for this business."
            )
        }

    # ========================================================
    # FETCH
    # ========================================================

    response = fetch_website(
        website
    )

    if not response:

        return {

            "website_exists": True,

            "website_reachable": False,

            "https": website.startswith(
                "https://"
            ),

            "mobile_friendly": False,

            "business_information": False,

            "contact_information": False,

            "services_listed": False,

            "social_links": False,

            "website_quality_score": 10,

            "strengths": [
                "Website URL exists"
            ],

            "weaknesses": [
                "Website is not reachable"
            ],

            "summary": (
                "Website exists but "
                "could not be reached."
            )
        }

    # ========================================================
    # PARSE
    # ========================================================

    html = response.text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text(
        " ",
        strip=True
    ).lower()

    # ========================================================
    # HTTPS
    # ========================================================

    https = (
        response.url.startswith(
            "https://"
        )
    )

    # ========================================================
    # MOBILE FRIENDLY
    # ========================================================

    viewport = soup.find(
        "meta",
        attrs={
            "name": "viewport"
        }
    )

    mobile_friendly = (
        viewport is not None
    )

    # ========================================================
    # BUSINESS INFORMATION
    # ========================================================

    business_keywords = [
        "about",
        "restaurant",
        "company",
        "business",
        "our story",
        "who we are"
    ]

    business_information = any(
        keyword in text
        for keyword in business_keywords
    )

    # ========================================================
    # CONTACT
    # ========================================================

    phone_exists = bool(
        soup.select(
            'a[href^="tel:"]'
        )
    )

    email_exists = bool(
        soup.select(
            'a[href^="mailto:"]'
        )
    )

    contact_keywords = [
        "contact",
        "phone",
        "call us",
        "email",
        "address"
    ]

    contact_information = (
        phone_exists
        or email_exists
        or any(
            keyword in text
            for keyword in contact_keywords
        )
    )

    # ========================================================
    # SERVICES
    # ========================================================

    service_keywords = [
        "menu",
        "services",
        "products",
        "order",
        "food",
        "restaurant",
        "delivery",
        "catering"
    ]

    services_listed = any(
        keyword in text
        for keyword in service_keywords
    )

    # ========================================================
    # SOCIAL LINKS
    # ========================================================

    social_domains = [
        "facebook.com",
        "instagram.com",
        "linkedin.com",
        "youtube.com",
        "twitter.com",
        "x.com"
    ]

    social_links = False

    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link["href"].lower()

        if any(
            domain in href
            for domain in social_domains
        ):

            social_links = True
            break

    # ========================================================
    # SCORE
    # ========================================================

    checks = {

        "website_exists": True,

        "website_reachable": True,

        "https": https,

        "mobile_friendly": mobile_friendly,

        "business_information":
            business_information,

        "contact_information":
            contact_information,

        "services_listed":
            services_listed,

        "social_links":
            social_links
    }

    score = (
        sum(checks.values())
        / len(checks)
        * 100
    )

    score = round(score)

    # ========================================================
    # STRENGTHS
    # ========================================================

    strengths = []

    if https:
        strengths.append(
            "HTTPS enabled"
        )

    if mobile_friendly:
        strengths.append(
            "Mobile-friendly viewport detected"
        )

    if business_information:
        strengths.append(
            "Business information available"
        )

    if contact_information:
        strengths.append(
            "Contact information available"
        )

    if services_listed:
        strengths.append(
            "Services/menu information available"
        )

    if social_links:
        strengths.append(
            "Social media links available"
        )

    # ========================================================
    # WEAKNESSES
    # ========================================================

    weaknesses = []

    if not https:
        weaknesses.append(
            "HTTPS not detected"
        )

    if not mobile_friendly:
        weaknesses.append(
            "Mobile-friendly viewport not detected"
        )

    if not business_information:
        weaknesses.append(
            "Business information not clearly detected"
        )

    if not contact_information:
        weaknesses.append(
            "Contact information not clearly detected"
        )

    if not services_listed:
        weaknesses.append(
            "Services/menu not clearly detected"
        )

    if not social_links:
        weaknesses.append(
            "Social media links not detected"
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = (
        f"Website analysis completed with "
        f"a quality score of {score}/100."
    )

    print()

    print(
        "Website Score :",
        score
    )

    return {

        "website_exists": True,

        "website_reachable": True,

        "https": https,

        "mobile_friendly": mobile_friendly,

        "business_information":
            business_information,

        "contact_information":
            contact_information,

        "services_listed":
            services_listed,

        "social_links":
            social_links,

        "website_quality_score":
            score,

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "summary":
            summary
    }