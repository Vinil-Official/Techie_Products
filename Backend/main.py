# from graph import app


# # ============================================================
# # TEST LEADS
# # ============================================================

# leads = [

#     {
#         "name": "Pasumpon Restaurant",
#         "phone": "+918401583411",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Padmam Banquet Hall & Wedding Caterers",
#         "phone": "+917048316280",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Stop Five Juice & Snacks",
#         "phone": "+918147316782",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Sri Ganesh Bhavan",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Absolute Barbecues",
#         "phone": "+917337383762",
#         "location": "T Nagar, Chennai"
#         "website": "https://www.absolutebarbecues.com/"
#     },

#     {
#         "name": "Barbeque Nation",
#         "phone": "+918064058059",
#         "location": "T Nagar, Chennai",
#         "website": "https://www.barbequenation.com/"
#     },

#     {
#         "name": "Geetham Veg Restaurant",
#         "phone": "+917397222111",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Mathsya Restaurant",
#         "phone": "+919791006234",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Dindigul Thalappakatti Restaurant",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": "https://thalappakatti.com/"
#     },

#     {
#         "name": "A2 - The Park",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Dindigul Thalappakatti Hotel",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": "https://thalappakatti.com/"
#     },

#     {
#         "name": "Dhaba Estd 1986 Delhi",
#         "phone": "+917338864168",
#         "location": "T Nagar / Nungambakkam, Chennai",
#         "website": "https://dhaba1986.com/"
#     },

#     {
#         "name": "Smoke Hub Barbeque",
#         "phone": "+919840501503",
#         "location": "T Nagar, Chennai",
#         "website": "https://smokehubbbq.com/"
#     },

#     {
#         "name": "Hotel Crescent Restaurant",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Murugan Idli Shop",
#         "phone": "+914442084842",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Madurai Kumar Mess",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Murugan Jigarthanda",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Pakwan Restaurant",
#         "phone": "+914443370888",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "New Woodlands",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "SS Hyderabad Biryani",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Sri Balaji Bhavan",
#         "phone": "+914428151008",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Thalappakatti Biryani",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": "https://thalappakatti.com/"
#     },

#     {
#         "name": "Saravana Bhavan",
#         "phone": None,
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Subhodayam Multi Cuisine Restaurant",
#         "phone": "+914442564600",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Sangeetha Veg Restaurant",
#         "phone": "+919003003090",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Olive Greenz Multicuisine Restaurant",
#         "phone": "+917871711452",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "T Nagar Park Restaurant",
#         "phone": "+919884392801",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Madras Machan's",
#         "phone": "+919342625522",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Basil With a Twist",
#         "phone": "+919841085611",
#         "location": "T Nagar, Chennai",
#         "website": None
#     },

#     {
#         "name": "Paati Veedu - Fine Dining Pure Veg Restaurant",
#         "phone": "+919962577234",
#         "location": "T Nagar, Chennai",
#         "website": None
#     }
# ]


# # ============================================================
# # PROCESS
# # ============================================================

# final_results = []


# for index, lead in enumerate(
#     leads,
#     start=1
# ):

#     print()
#     print("=" * 70)

#     print(
#         f"PROCESSING LEAD {index}/{len(leads)}"
#     )

#     print("=" * 70)

#     state = {

#         "current_lead": lead
#     }

#     result = app.invoke(
#         state
#     )

#     final_lead = {

#         "name":
#             lead.get("name"),

#         "phone":
#             lead.get("phone"),

#         "location":
#             lead.get("location"),

#         "website":
#             result.get("website"),

#         "website_source":
#             result.get("website_source"),

#         "website_exists":
#             result.get("website_exists"),

#         "website_reachable":
#             result.get(
#                 "website_reachable"
#             ),

#         "https":
#             result.get("https"),

#         "mobile_friendly":
#             result.get(
#                 "mobile_friendly"
#             ),

#         "business_information":
#             result.get(
#                 "business_information"
#             ),

#         "contact_information":
#             result.get(
#                 "contact_information"
#             ),

#         "services_listed":
#             result.get(
#                 "services_listed"
#             ),

#         "social_links":
#             result.get(
#                 "social_links"
#             ),

#         "website_quality_score":
#             result.get(
#                 "website_quality_score"
#             ),

#         "strengths":
#             result.get(
#                 "strengths",
#                 []
#             ),

#         "weaknesses":
#             result.get(
#                 "weaknesses",
#                 []
#             ),

#         "summary":
#             result.get(
#                 "summary"
#             )
#     }

#     final_results.append(
#         final_lead
#     )


# # ============================================================
# # FINAL OUTPUT
# # ============================================================

# print()
# print()
# print("=" * 70)
# print("                  FINAL RESULTS")
# print("=" * 70)


# for index, lead in enumerate(
#     final_results,
#     start=1
# ):

#     print()

#     print(
#         f"{index}. {lead['name']}"
#     )

#     print(
#         "   Phone   :",
#         lead["phone"]
#     )

#     print(
#         "   Location:",
#         lead["location"]
#     )

#     print(
#         "   Website :",
#         lead["website"]
#     )

#     print(
#         "   Source  :",
#         lead["website_source"]
#     )

#     print(
#         "   Score   :",
#         lead["website_quality_score"]
#     )

#     print(
#         "   Summary :",
#         lead["summary"]
#     )


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseModel, Field
# from typing import List, Optional

# from graph import app


# # ============================================================
# # FASTAPI APP
# # ============================================================

# api = FastAPI(
#     title="AI Lead Quality Analyzer",
#     description="AI-powered lead quality and website analysis API",
#     version="1.0.0"
# )


# # ============================================================
# # CORS
# # ============================================================

# api.add_middleware(
#     CORSMiddleware,

#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173"
#     ],

#     allow_credentials=True,

#     allow_methods=["*"],

#     allow_headers=["*"]
# )


# # ============================================================
# # REQUEST MODELS
# # ============================================================

# class Lead(BaseModel):

#     name: str

#     phone: Optional[str] = None

#     location: str

#     website: Optional[str] = None


# class LeadRequest(BaseModel):

#     leads: List[Lead] = Field(
#         min_length=1,
#         max_length=100
#     )


# # ============================================================
# # ROOT
# # ============================================================

# @api.get("/")
# def root():

#     return {
#         "success": True,
#         "message": "AI Lead Quality Analyzer API is running"
#     }


# # ============================================================
# # HEALTH CHECK
# # ============================================================

# @api.get("/health")
# def health():

#     return {
#         "status": "healthy"
#     }


# # ============================================================
# # PROCESS LEADS
# # ============================================================

# @api.post("/process-leads")
# def process_leads(
#     request: LeadRequest
# ):

#     try:

#         # ----------------------------------------------------
#         # Convert Pydantic objects to dictionaries
#         # ----------------------------------------------------

#         leads = [
#             lead.model_dump()
#             for lead in request.leads
#         ]

#         final_results = []


#         # ====================================================
#         # PROCESS EACH LEAD
#         # ====================================================

#         for index, lead in enumerate(
#             leads,
#             start=1
#         ):

#             print()
#             print("=" * 70)

#             print(
#                 f"PROCESSING LEAD {index}/{len(leads)}"
#             )

#             print(
#                 f"Name     : {lead.get('name')}"
#             )

#             print(
#                 f"Phone    : {lead.get('phone')}"
#             )

#             print(
#                 f"Location : {lead.get('location')}"
#             )

#             print(
#                 f"Website  : {lead.get('website')}"
#             )

#             print("=" * 70)


#             # ------------------------------------------------
#             # LangGraph State
#             # ------------------------------------------------

#             state = {

#                 "leads": [lead],

#                 "current_lead": lead,

#                 "processed_leads": [],

#                 "current_index": index - 1
#             }


#             # ------------------------------------------------
#             # Run LangGraph
#             # ------------------------------------------------

#             result = app.invoke(
#                 state
#             )


#             # ------------------------------------------------
#             # Get website analysis
#             # ------------------------------------------------

#             website_analysis = result.get(
#                 "website_analysis",
#                 {}
#             )


#             # ------------------------------------------------
#             # Create final lead
#             # ------------------------------------------------

#             final_lead = {

#                 "name":
#                     lead.get("name"),

#                 "phone":
#                     lead.get("phone"),

#                 "location":
#                     lead.get("location"),

#                 "website":
#                     lead.get("website"),


#                 # ============================================
#                 # WEBSITE ANALYSIS
#                 # ============================================

#                 "website_exists":
#                     website_analysis.get(
#                         "website_exists",
#                         False
#                     ),

#                 "website_reachable":
#                     website_analysis.get(
#                         "website_reachable",
#                         False
#                     ),

#                 "https":
#                     website_analysis.get(
#                         "https",
#                         False
#                     ),

#                 "mobile_friendly":
#                     website_analysis.get(
#                         "mobile_friendly",
#                         False
#                     ),

#                 "business_information":
#                     website_analysis.get(
#                         "business_information",
#                         False
#                     ),

#                 "contact_information":
#                     website_analysis.get(
#                         "contact_information",
#                         False
#                     ),

#                 "services_listed":
#                     website_analysis.get(
#                         "services_listed",
#                         False
#                     ),

#                 "social_links":
#                     website_analysis.get(
#                         "social_links",
#                         False
#                     ),


#                 # ============================================
#                 # SCORE
#                 # ============================================

#                 "website_quality_score":
#                     website_analysis.get(
#                         "website_quality_score",
#                         0
#                     ),


#                 # ============================================
#                 # AI ANALYSIS
#                 # ============================================

#                 "strengths":
#                     website_analysis.get(
#                         "strengths",
#                         []
#                     ),

#                 "weaknesses":
#                     website_analysis.get(
#                         "weaknesses",
#                         []
#                     ),

#                 "summary":
#                     website_analysis.get(
#                         "summary",
#                         ""
#                     )
#             }


#             # ------------------------------------------------
#             # Add to final results
#             # ------------------------------------------------

#             final_results.append(
#                 final_lead
#             )


#             # ------------------------------------------------
#             # Terminal Output
#             # ------------------------------------------------

#             print()

#             print(
#                 "WEBSITE ANALYSIS"
#             )

#             print(
#                 "Website Exists :",
#                 final_lead[
#                     "website_exists"
#                 ]
#             )

#             print(
#                 "Reachable      :",
#                 final_lead[
#                     "website_reachable"
#                 ]
#             )

#             print(
#                 "HTTPS          :",
#                 final_lead[
#                     "https"
#                 ]
#             )

#             print(
#                 "Mobile Friendly:",
#                 final_lead[
#                     "mobile_friendly"
#                 ]
#             )

#             print(
#                 "Services       :",
#                 final_lead[
#                     "services_listed"
#                 ]
#             )

#             print(
#                 "Social Links   :",
#                 final_lead[
#                     "social_links"
#                 ]
#             )

#             print(
#                 "Quality Score  :",
#                 final_lead[
#                     "website_quality_score"
#                 ]
#             )

#             print(
#                 "Summary        :",
#                 final_lead[
#                     "summary"
#                 ]
#             )


#         # ====================================================
#         # FINAL RESPONSE
#         # ====================================================

#         print()
#         print("=" * 70)

#         print(
#             "ALL LEADS PROCESSED"
#         )

#         print(
#             f"Total Leads     : {len(leads)}"
#         )

#         print(
#             f"Processed Leads : {len(final_results)}"
#         )

#         print("=" * 70)


#         return {

#             "success": True,

#             "total_leads": len(
#                 leads
#             ),

#             "processed_leads": len(
#                 final_results
#             ),

#             "leads": final_results
#         }


#     except Exception as e:

#         print()
#         print("=" * 70)

#         print(
#             "ERROR WHILE PROCESSING LEADS"
#         )

#         print(
#             str(e)
#         )

#         print("=" * 70)


#         raise HTTPException(

#             status_code=500,

#             detail=str(e)
#         )


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from typing import List, Optional, Dict, Any

from graph import app as graph_app
from qualified_leads import router as qualified_leads_router


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Lead Quality Analyzer",
    description="AI-powered lead quality and website analysis API",
    version="1.0.0",
)
api = app
app.include_router(qualified_leads_router)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_origins=[origin.strip() for origin in os.getenv('FRONTEND_ORIGINS', '').split(',') if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class LeadInput(BaseModel):
    name: str = Field(..., min_length=1)
    phone: Optional[str] = None
    location: str = Field(..., min_length=1)
    website: Optional[str] = None


class LeadRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    leads: Optional[List[LeadInput]] = None


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Lead Quality Analyzer API is running",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy",
        "service": "AI Lead Quality Analyzer",
    }


# ============================================================
# HELPERS
# ============================================================

def _normalize_lead_data(lead: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "name": (lead or {}).get("name") or "",
        "phone": (lead or {}).get("phone"),
        "location": (lead or {}).get("location") or "",
        "website": (lead or {}).get("website"),
    }
    if isinstance(normalized["website"], str):
        normalized["website"] = normalized["website"].strip() or None
    return normalized


def _normalize_analysis(result: Dict[str, Any]) -> Dict[str, Any]:
    analysis = {
        "website_exists": bool(result.get("website_exists", False)),
        "website_reachable": bool(result.get("website_reachable", False)),
        "https": bool(result.get("https", False)),
        "mobile_friendly": bool(result.get("mobile_friendly", False)),
        "business_information": bool(result.get("business_information", False)),
        "contact_information": bool(result.get("contact_information", False)),
        "services_listed": bool(result.get("services_listed", False)),
        "social_links": bool(result.get("social_links", False)),
        "website_quality_score": result.get("website_quality_score", 0),
        "strengths": result.get("strengths", []),
        "weaknesses": result.get("weaknesses", []),
        "summary": result.get("summary", ""),
    }
    return analysis


# ============================================================
# PROCESS LEADS
# ============================================================

@app.post("/run-agent")
@app.post("/process-leads")
def process_lead(payload: LeadRequest):
    try:
        lead_entries = []

        if payload.leads:
            lead_entries = [lead.model_dump() for lead in payload.leads]
        else:
            lead_entries = [{
                "name": payload.name,
                "phone": payload.phone,
                "location": payload.location,
                "website": payload.website,
            }]

        if not lead_entries or all(not (lead or {}).get("name") and not (lead or {}).get("location") for lead in lead_entries):
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Name and location are required.",
                },
            )

        results = []
        processed_count = 0

        for index, raw_lead in enumerate(lead_entries, start=1):
            try:
                lead = _normalize_lead_data(raw_lead)
                if not lead.get("name") or not lead.get("location"):
                    raise ValueError("Name and location are required.")

                state = {"current_lead": lead}
                result = graph_app.invoke(state)
                current_lead = result.get("current_lead", lead)
                normalized_lead = _normalize_lead_data(current_lead)
                normalized_lead["website"] = normalized_lead.get("website") or lead.get("website")

                final_result = {
                    "name": normalized_lead.get("name"),
                    "phone": normalized_lead.get("phone"),
                    "location": normalized_lead.get("location"),
                    "website": normalized_lead.get("website"),
                }

                analysis = _normalize_analysis(result)
                result_payload = {
                    "success": True,
                    "lead": final_result,
                    "analysis": analysis,
                    "website_source": result.get("website_source"),
                    "summary": analysis.get("summary"),
                    "index": index,
                }
                results.append(result_payload)
                processed_count += 1
            except Exception as exc:
                results.append({
                    "success": False,
                    "lead": _normalize_lead_data(raw_lead),
                    "error": str(exc) or "Website analysis failed",
                    "index": index,
                })

        if len(lead_entries) == 1:
            first = results[0]
            if first.get("success") is False:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "success": False,
                        "message": first.get("error") or "Something went wrong while analyzing the lead.",
                    },
                )
            return first

        return {
            "success": True,
            "total": len(lead_entries),
            "processed": processed_count,
            "failed": len(lead_entries) - processed_count,
            "results": results,
        }

    except HTTPException:
        raise
    except Exception as exc:
        print(f"ERROR WHILE PROCESSING LEAD: {exc}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": "Something went wrong while analyzing the lead.",
                "error": str(exc),
            },
        )
