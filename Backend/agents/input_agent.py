from state import LeadState


def input_agent(state: LeadState):

    lead = state.get("current_lead", {})

    name = lead.get("name", "")
    phone = lead.get("phone", "")
    location = lead.get("location", "")
    website = lead.get("website")

    # Clean website
    if isinstance(website, str):

        website = website.strip()

        if website.lower() in [
            "",
            "none",
            "null",
            "n/a",
            "not available",
            "no website"
        ]:
            website = None

    else:
        website = None

    return {
        "current_lead": {
            "name": name,
            "phone": phone,
            "location": location,
            "website": website
        },
        "website": website
    }