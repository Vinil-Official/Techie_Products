import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

export const hasSupabaseConfig = Boolean(supabase)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const requireClient = () => {
  if (!supabase) {
    throw new Error('Supabase is not configured. Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to your .env.local file.')
  }
  return supabase
}

async function qualifiedLeadsRequest(path, options = {}) {
  const client = requireClient()
  const { data: sessionData, error: sessionError } = await client.auth.getSession()
  if (sessionError) throw sessionError

  const accessToken = sessionData.session?.access_token
  const response = await fetch(`${API_BASE_URL}/qualified-leads${path}`, {
    ...options,
    headers: {
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers,
    },
  })
  const data = response.status === 204 ? null : await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = data?.detail
    const detailMessage = typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail.map((issue) => issue.msg).filter(Boolean).join(' ')
        : detail?.message
    const requestError = new Error(
      detailMessage || data?.message || 'Qualified Leads API request failed.',
    )
    requestError.code = typeof detail === 'object' ? detail?.code : undefined
    throw requestError
  }
  return data
}

export async function listQualifiedLeads() {
  return qualifiedLeadsRequest('')
}

export async function saveQualifiedLead(lead, sourceLeadId) {
  return qualifiedLeadsRequest('', {
    method: 'POST',
    body: JSON.stringify({
      source_lead_id: sourceLeadId || null,
      name: lead.name.trim(),
      phone: lead.phone.trim() || null,
      location: lead.location.trim() || null,
      website: lead.website.trim() || null,
      qualification_status: lead.qualification_status,
      lead_score: Number(lead.lead_score),
      notes: lead.notes.trim() || null,
    }),
  })
}

export async function updateQualifiedLead(id, lead) {
  return qualifiedLeadsRequest(`/${encodeURIComponent(id)}`, {
    method: 'PATCH',
    body: JSON.stringify({
      name: lead.name.trim(),
      phone: lead.phone.trim() || null,
      location: lead.location.trim() || null,
      website: lead.website.trim() || null,
      qualification_status: lead.qualification_status,
      lead_score: Number(lead.lead_score),
      notes: lead.notes.trim() || null,
      updated_at: new Date().toISOString(),
    }),
  })
}

export async function deleteQualifiedLead(id) {
  return qualifiedLeadsRequest(`/${encodeURIComponent(id)}`, { method: 'DELETE' })
}