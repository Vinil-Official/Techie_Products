import os
import re
import requests

from urllib.parse import urlparse

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from state import LeadState


load_dotenv()


# ============================================================
# LLM
# ============================================================

api_key = os.getenv("GROQ_API_KEY", "").strip()

if api_key and api_key.lower() != "your_api_key_here":
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0
    )
else:
    llm = None


# ============================================================
# CONFIG
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}


# ============================================================
# CLEAN URL
# ============================================================

def clean_url(url):

    if not url:
        return None

    url = url.strip()

    url = url.strip(".,;:()[]{}<>")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    return url


# ============================================================
# DOMAIN
# ============================================================

def get_domain(url):

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except:

        return ""


# ============================================================
# VERIFY WEBSITE
# ============================================================

def verify_website(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        if response.status_code >= 200 and response.status_code < 400:

            return True, response.url

    except Exception:
        pass

    return False, None


# ============================================================
# DUCKDUCKGO SEARCH
# ============================================================

def duckduckgo_search(query):

    try:

        search_url = (
            "https://html.duckduckgo.com/html/"
            "?q=" + requests.utils.quote(query)
        )

        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for result in soup.select(".result"):

            link = result.select_one(
                ".result__a"
            )

            if not link:
                continue

            href = link.get("href")

            title = link.get_text(
                " ",
                strip=True
            )

            if href:

                results.append({
                    "title": title,
                    "url": href
                })

        return results

    except Exception as e:

        print(
            "DuckDuckGo error:",
            e
        )

        return []


# ============================================================
# DOMAIN BLACKLIST
# ============================================================

BLACKLIST_DOMAINS = {

    "justdial.com",
    "www.justdial.com",

    "facebook.com",
    "www.facebook.com",

    "instagram.com",
    "www.instagram.com",

    "linkedin.com",
    "www.linkedin.com",

    "youtube.com",
    "www.youtube.com",

    "zomato.com",
    "www.zomato.com",

    "swiggy.com",
    "www.swiggy.com",

    "tripadvisor.com",
    "www.tripadvisor.com",

    "magicpin.in",
    "www.magicpin.in",

    "sulekha.com",
    "www.sulekha.com",

    "google.com",
    "www.google.com"
}


# ============================================================
# DISCOVER WEBSITE USING LLM
# ============================================================

def choose_official_website(
    business_name,
    location,
    results
):

    if not results:
        return None

    if llm is None:
        for result in results:
            url = result.get("url")
            title = result.get("title", "")
            if not url:
                continue
            domain = get_domain(url)
            if domain in BLACKLIST_DOMAINS:
                continue
            if business_name.lower() in title.lower() or business_name.lower() in url.lower():
                return clean_url(url)
        return clean_url(results[0].get("url"))

    formatted_results = ""

    for index, result in enumerate(results[:10]):

        formatted_results += (
            f"\nRESULT {index + 1}\n"
            f"TITLE: {result['title']}\n"
            f"URL: {result['url']}\n"
        )

    prompt = f"""
You are an official business website detection agent.

Business:
{business_name}

Location:
{location}

Search results:
{formatted_results}

Find the most likely OFFICIAL WEBSITE of this business.

Rules:

1. Prefer the company's own domain.
2. Do NOT select Justdial.
3. Do NOT select Facebook.
4. Do NOT select Instagram.
5. Do NOT select Zomato.
6. Do NOT select Swiggy.
7. Do NOT select LinkedIn.
8. Do NOT select Tripadvisor.
9. Do NOT select directory websites.
10. Return ONLY the URL.
11. If there is no official website, return NONE.

Answer:
"""

    try:

        response = llm.invoke(prompt)

        answer = response.content.strip()

        # Remove markdown
        answer = answer.replace(
            "```",
            ""
        ).strip()

        if answer.upper() == "NONE":
            return None

        # Extract URL
        match = re.search(
            r'https?://[^\s<>"\']+',
            answer
        )

        if not match:
            return None

        url = clean_url(
            match.group(0)
        )

        if not url:
            return None

        domain = get_domain(url)

        if domain in BLACKLIST_DOMAINS:
            return None

        return url

    except Exception as e:

        print(
            "LLM website selection error:",
            e
        )

        return None


# ============================================================
# WEBSITE DISCOVERY NODE
# ============================================================

def website_discovery(state: LeadState):

    lead = state.get(
        "current_lead",
        {}
    )

    business_name = lead.get(
        "name",
        ""
    )

    location = lead.get(
        "location",
        ""
    )

    existing_website = lead.get(
        "website"
    )

    print()
    print("=" * 55)
    print("       WEBSITE DISCOVERY")
    print("=" * 55)

    print(
        "Business :",
        business_name
    )

    print(
        "Location :",
        location
    )

    print(
        "Existing :",
        existing_website
    )

    # ========================================================
    # STEP 1
    # Existing website
    # ========================================================

    if existing_website:

        existing_website = clean_url(
            existing_website
        )

        reachable, final_url = verify_website(
            existing_website
        )

        if reachable:

            print(
                "Verified :",
                final_url
            )

            return {
                "website": final_url,
                "website_source": "lead"
            }

    # ========================================================
    # STEP 2
    # Search official website
    # ========================================================

    query = (
        f'"{business_name}" '
        f'"{location}" official website'
    )

    print(
        "Search :",
        query
    )

    results = duckduckgo_search(
        query
    )

    print(
        "Search results:",
        len(results)
    )

    # ========================================================
    # STEP 3
    # Filter results
    # ========================================================

    valid_results = []

    for result in results:

        url = result.get(
            "url",
            ""
        )

        domain = get_domain(url)

        if not domain:
            continue

        if domain in BLACKLIST_DOMAINS:
            continue

        valid_results.append(
            result
        )

    # ========================================================
    # STEP 4
    # LLM selection
    # ========================================================

    website = choose_official_website(
        business_name,
        location,
        valid_results
    )

    # ========================================================
    # STEP 5
    # Verify selected website
    # ========================================================

    if website:

        reachable, final_url = verify_website(
            website
        )

        if reachable:

            print(
                "Official website:",
                final_url
            )

            return {
                "website": final_url,
                "website_source": "duckduckgo"
            }

    print(
        "Official website: None"
    )

    return {
        "website": None,
        "website_source": None
    }


