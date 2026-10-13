import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).with_name('.env'))

router = APIRouter(prefix='/qualified-leads', tags=['qualified-leads'])


class QualifiedLeadInput(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    qualification_status: Literal[
        'Qualified Lead',
        'Partially Qualified Lead',
        'Not Qualified Lead',
        'Meetings',
        'Contacted',
        'Proposals',
        'Deals',
    ]
    lead_score: int = Field(default=0, ge=0, le=100)
    notes: Optional[str] = None


class QualifiedLeadCreate(QualifiedLeadInput):
    source_lead_id: Optional[str] = None


def _supabase_request(method, path='', authorization=None, params=None, payload=None):
    supabase_url = os.getenv('SUPABASE_URL', '').rstrip('/')
    supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
    if not supabase_url or not supabase_anon_key:
        raise HTTPException(
            status_code=503,
            detail={'message': 'Supabase is not configured on the backend.'},
        )

    headers = {
        'apikey': supabase_anon_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    }
    if authorization and authorization.startswith('Bearer '):
        headers['Authorization'] = authorization
    url = f'{supabase_url}/rest/v1/qualified_leads{path}'

    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=payload,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail={'message': 'Unable to reach the Supabase database.'},
        ) from exc

    if not response.ok:
        try:
            database_error = response.json()
        except ValueError:
            database_error = {}

        error_code = database_error.get('code')
        if error_code == '23505':
            raise HTTPException(
                status_code=409,
                detail={
                    'message': 'This generated lead has already been saved.',
                    'code': error_code,
                },
            )

        status_code = response.status_code
        if status_code not in (400, 401, 403, 404, 422):
            status_code = 502
        message = database_error.get('message') or 'Supabase rejected the database request.'
        raise HTTPException(
            status_code=status_code,
            detail={'message': message, 'code': error_code},
        )

    if not response.content:
        return None
    return response.json()


def _lead_payload(lead):
    payload = lead.model_dump()
    payload['name'] = payload['name'].strip()
    if not payload['name']:
        raise HTTPException(status_code=422, detail={'message': 'Business name is required.'})
    for field in ('phone', 'location', 'website', 'notes', 'source_lead_id'):
        if isinstance(payload.get(field), str):
            payload[field] = payload[field].strip() or None
    return payload


@router.get('')
def list_qualified_leads(authorization: Optional[str] = Header(default=None)):
    return _supabase_request(
        'GET',
        authorization=authorization,
        params={'select': '*', 'order': 'created_at.desc'},
    )


@router.post('', status_code=201)
def create_qualified_lead(
    lead: QualifiedLeadCreate,
    authorization: Optional[str] = Header(default=None),
):
    records = _supabase_request(
        'POST',
        authorization=authorization,
        payload=_lead_payload(lead),
    )
    return records[0] if records else None


@router.patch('/{lead_id}')
def edit_qualified_lead(
    lead_id: UUID,
    lead: QualifiedLeadInput,
    authorization: Optional[str] = Header(default=None),
):
    payload = _lead_payload(lead)
    payload['updated_at'] = datetime.now(timezone.utc).isoformat()
    records = _supabase_request(
        'PATCH',
        authorization=authorization,
        params={'id': f'eq.{lead_id}'},
        payload=payload,
    )
    if not records:
        raise HTTPException(status_code=404, detail={'message': 'Qualified lead not found.'})
    return records[0]


@router.delete('/{lead_id}', status_code=204)
def remove_qualified_lead(
    lead_id: UUID,
    authorization: Optional[str] = Header(default=None),
):
    records = _supabase_request(
        'DELETE',
        authorization=authorization,
        params={'id': f'eq.{lead_id}'},
    )
    if not records:
        raise HTTPException(status_code=404, detail={'message': 'Qualified lead not found.'})
    return None