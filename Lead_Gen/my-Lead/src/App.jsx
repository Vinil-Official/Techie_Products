import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { bulkProcessLeads } from './api'
import {
  deleteQualifiedLead,
  hasSupabaseConfig,
  listQualifiedLeads,
  saveQualifiedLead,
  supabase,
  updateQualifiedLead,
} from './supabase'

const STORAGE_KEY = 'ai_lead_generation_leads'
const QUALIFICATION_STATUSES = [
  'Qualified Lead',
  'Partially Qualified Lead',
  'Not Qualified Lead',
  'Meetings',
  'Contacted',
  'Proposals',
  'Deals',
]
const EMPTY_QUALIFIED_DRAFT = {
  name: '', phone: '', location: '', website: '',
  qualification_status: 'Partially Qualified Lead', lead_score: '0', notes: '',
}

const createLeadId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }

  return `lead-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const parseLeadRecord = (entry) => {
  const raw = entry || {}
  const lead = {
    id: raw.id || createLeadId(),
    name: raw.name || '',
    phone: raw.phone ?? '',
    location: raw.location || '',
    website: raw.website ?? null,
    analysis: raw.analysis || {},
    error: raw.error || '',
  }

  if (!lead.name && raw.lead?.name) {
    lead.name = raw.lead.name
  }
  if (!lead.phone && raw.lead?.phone) {
    lead.phone = raw.lead.phone
  }
  if (!lead.location && raw.lead?.location) {
    lead.location = raw.lead.location
  }
  if (lead.website === null && raw.lead?.website) {
    lead.website = raw.lead.website
  }

  return lead
}

const formatWebsiteValue = (value) => {
  if (value === null || value === undefined || value === '') {
    return 'Not Available'
  }
  return value
}

const formatAnalysisLabel = (key) => key
  .replace(/_/g, ' ')
  .replace(/\b\w/g, (letter) => letter.toUpperCase())

const persistLeads = (nextLeads) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextLeads))
  } catch (err) {
    console.error('Unable to save leads to localStorage:', err)
  }
}

function App() {
  const [bulkText, setBulkText] = useState('')
  const [leadCount, setLeadCount] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [leads, setLeads] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
      return Array.isArray(saved) ? saved.map(parseLeadRecord) : []
    } catch {
      return []
    }
  })
  const [editingLeadId, setEditingLeadId] = useState(null)
  const [draftLead, setDraftLead] = useState({ name: '', phone: '', location: '', website: '' })
  const [activeView, setActiveView] = useState('dashboard')
  const [session, setSession] = useState(null)
  const [authReady, setAuthReady] = useState(!supabase)
  const [authMode, setAuthMode] = useState('signin')
  const [authDraft, setAuthDraft] = useState({ email: '', password: '' })
  const [qualifiedLeads, setQualifiedLeads] = useState([])
  const [qualifiedLoading, setQualifiedLoading] = useState(false)
  const [qualifiedError, setQualifiedError] = useState('')
  const [qualifiedSearch, setQualifiedSearch] = useState('')
  const [qualifiedStatusFilter, setQualifiedStatusFilter] = useState('All statuses')
  const [qualifiedPage, setQualifiedPage] = useState(1)
  const [qualifiedModal, setQualifiedModal] = useState(null)
  const [qualifiedDraft, setQualifiedDraft] = useState(EMPTY_QUALIFIED_DRAFT)
  const [formErrors, setFormErrors] = useState({})
  const [savingQualified, setSavingQualified] = useState(false)
  const [detailLead, setDetailLead] = useState(null)
  const [toast, setToast] = useState(null)

  const showToast = (message, kind = 'success') => setToast({ message, kind })

  useEffect(() => {
    if (!supabase) return undefined

    let active = true
    supabase.auth.getSession().then(({ data, error: sessionError }) => {
      if (!active) return
      if (sessionError) showToast(sessionError.message, 'error')
      setSession(data?.session || null)
      setQualifiedLoading(Boolean(data?.session))
      setAuthReady(true)
    })
    const { data: authListener } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession)
      setQualifiedLoading(Boolean(nextSession))
      if (!nextSession) setQualifiedLeads([])
    })

    return () => {
      active = false
      authListener.subscription.unsubscribe()
    }
  }, [])

  useEffect(() => {
    if (!toast) return undefined
    const timer = window.setTimeout(() => setToast(null), 4200)
    return () => window.clearTimeout(timer)
  }, [toast])

  useEffect(() => {
    let active = true
    setQualifiedLoading(true)
    listQualifiedLeads()
      .then((records) => {
        if (active) {
          setQualifiedLeads(records)
          setQualifiedError('')
        }
      })
      .catch((loadError) => {
        if (active) setQualifiedError(loadError.message || 'Unable to load qualified leads.')
      })
      .finally(() => {
        if (active) setQualifiedLoading(false)
      })

    return () => { active = false }
  }, [])

  const savedSourceLeadIds = useMemo(
    () => new Set(qualifiedLeads.map((record) => record.source_lead_id).filter(Boolean)),
    [qualifiedLeads],
  )

  const filteredQualifiedLeads = useMemo(() => {
    const query = qualifiedSearch.trim().toLowerCase()
    return qualifiedLeads.filter((lead) => {
      const matchesStatus = qualifiedStatusFilter === 'All statuses'
        || lead.qualification_status === qualifiedStatusFilter
      const searchable = [lead.name, lead.phone, lead.location, lead.website].filter(Boolean).join(' ').toLowerCase()
      return matchesStatus && (!query || searchable.includes(query))
    })
  }, [qualifiedLeads, qualifiedSearch, qualifiedStatusFilter])
  const qualifiedPageSize = 10
  const qualifiedPageCount = Math.max(1, Math.ceil(filteredQualifiedLeads.length / qualifiedPageSize))
  const visibleQualifiedLeads = filteredQualifiedLeads.slice(
    (qualifiedPage - 1) * qualifiedPageSize,
    qualifiedPage * qualifiedPageSize,
  )

  const metrics = useMemo(() => [
    { label: 'Total Leads', value: leads.length },
    { label: 'Leads Contacted', value: 0 },
    { label: 'Meetings', value: 0 },
    { label: 'Proposals', value: 0 },
    { label: 'Deals', value: 0 },
  ], [leads.length])

  const parseBulkInput = (value) => {
    if (!value.trim()) {
      throw new Error('Please paste at least one lead.')
    }

    const parsed = JSON.parse(value)
    if (!Array.isArray(parsed)) {
      throw new Error('Invalid JSON format. Please check your pasted lead data.')
    }

    if (parsed.length === 0) {
      throw new Error('Please paste at least one lead.')
    }

    parsed.forEach((lead, index) => {
      if (!lead || typeof lead !== 'object') {
        throw new Error(`Lead ${index + 1} is not a valid object.`)
      }

      const hasName = typeof lead.name === 'string' && lead.name.trim()
      const hasLocation = typeof lead.location === 'string' && lead.location.trim()
      const hasPhone = lead.phone === null || lead.phone === undefined || typeof lead.phone === 'string'
      const hasWebsite = lead.website === null || lead.website === undefined || typeof lead.website === 'string'

      if (!hasName || !hasLocation || !hasPhone || !hasWebsite) {
        throw new Error('Each lead must include name, phone, location, and website. Phone and website may be null.')
      }
    })

    return parsed
  }

  const handleBulkChange = (event) => {
    const value = event.target.value
    setBulkText(value)
    setError('')

    if (!value.trim()) {
      setLeadCount(0)
      return
    }

    try {
      const parsed = parseBulkInput(value)
      setLeadCount(parsed.length)
    } catch {
      setLeadCount(0)
    }
  }

  const handleProcessLeads = async () => {
    setError('')

    try {
      const parsed = parseBulkInput(bulkText)
      setLoading(true)
      setError('')

      const response = await bulkProcessLeads(parsed.map((lead) => ({
        name: lead.name?.trim() || '',
        phone: lead.phone ?? null,
        location: lead.location?.trim() || '',
        website: typeof lead.website === 'string' ? lead.website.trim() || null : null,
      })))

      const nextLeads = (response?.results || []).map((result) => {
        if (result?.success === false) {
          return parseLeadRecord({
            id: createLeadId(),
            name: result?.lead?.name || 'Unknown Lead',
            phone: result?.lead?.phone ?? null,
            location: result?.lead?.location || '',
            website: result?.lead?.website ?? null,
            analysis: {},
            error: result?.error || 'Website analysis failed',
          })
        }

        return parseLeadRecord({
          id: createLeadId(),
          name: result?.lead?.name || '',
          phone: result?.lead?.phone ?? null,
          location: result?.lead?.location || '',
          website: result?.lead?.website ?? null,
          analysis: result?.analysis || {},
        })
      })

      setLeads(nextLeads)
      persistLeads(nextLeads)
      setBulkText('')
      setLeadCount(0)
    } catch (err) {
      console.error('Bulk processing failed:', err)

      if (err instanceof TypeError) {
        setError('Unable to connect to backend. Please make sure FastAPI is running.')
      } else if (err instanceof SyntaxError || /JSON/.test(String(err?.message || ''))) {
        setError('Invalid JSON format. Please check your pasted lead data.')
      } else {
        setError(err.message || 'Invalid JSON format. Please check your pasted lead data.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setBulkText('')
    setLeadCount(0)
    setError('')
  }

  const handleClearAllData = () => {
    const shouldClear = window.confirm('Are you sure you want to delete all saved leads?')
    if (!shouldClear) return

    setLeads([])
    persistLeads([])
    setEditingLeadId(null)
    setDraftLead({ name: '', phone: '', location: '', website: '' })
    handleClear()
  }

  const handleOpenEditor = (lead) => {
    setEditingLeadId(lead.id)
    setDraftLead({
      name: lead.name || '',
      phone: lead.phone || '',
      location: lead.location || '',
      website: lead.website || '',
    })
  }

  const handleSaveLead = () => {
    if (!editingLeadId) return

    setLeads((current) => {
      const next = current.map((lead) => {
        if (lead.id !== editingLeadId) {
          return lead
        }

        return {
          ...lead,
          name: draftLead.name.trim() || lead.name,
          phone: draftLead.phone.trim() || null,
          location: draftLead.location.trim() || lead.location,
          website: draftLead.website.trim() || null,
        }
      })

      persistLeads(next)
      return next
    })

    setEditingLeadId(null)
    setDraftLead({ name: '', phone: '', location: '', website: '' })
  }

  const handleDeleteLead = (leadId) => {
    const shouldDelete = window.confirm('Are you sure you want to delete this lead?')
    if (!shouldDelete) return

    setLeads((current) => {
      const next = current.filter((lead) => lead.id !== leadId)
      persistLeads(next)
      return next
    })
    if (editingLeadId === leadId) {
      setEditingLeadId(null)
    }
  }

  const refreshQualifiedLeads = async () => {
    setQualifiedLoading(true)
    try {
      const records = await listQualifiedLeads()
      setQualifiedLeads(records)
      setQualifiedError('')
      return records
    } catch (refreshError) {
      setQualifiedError(refreshError.message || 'Unable to refresh qualified leads.')
      return null
    } finally {
      setQualifiedLoading(false)
    }
  }

  const handleAuthSubmit = async (event) => {
    event.preventDefault()
    if (!supabase) {
      showToast('Add your Supabase URL and anon key to .env, then restart Vite.', 'error')
      return
    }
    setSavingQualified(true)
    try {
      const authRequest = authMode === 'signup'
        ? supabase.auth.signUp({ email: authDraft.email.trim(), password: authDraft.password })
        : supabase.auth.signInWithPassword({ email: authDraft.email.trim(), password: authDraft.password })
      const { data, error: authError } = await authRequest
      if (authError) throw authError
      if (data.session) {
        setSession(data.session)
        showToast(authMode === 'signup' ? 'Account created and signed in.' : 'Signed in successfully.')
      } else {
        showToast('Check your email to confirm the account, then sign in.')
        setAuthMode('signin')
      }
    } catch (authError) {
      showToast(authError.message || 'Authentication failed.', 'error')
    } finally {
      setSavingQualified(false)
    }
  }

  const handleSignOut = async () => {
    const { error: signOutError } = await supabase.auth.signOut()
    if (signOutError) showToast(signOutError.message, 'error')
    else showToast('Signed out.')
  }

  const openQualifiedForm = (lead, mode = 'source') => {
    const sourceId = lead?.source_lead_id || lead?.id || null
    const websiteScore = Number(lead?.analysis?.website_quality_score)
    const defaultScore = Number.isFinite(websiteScore) ? Math.max(0, Math.min(100, Math.round(websiteScore))) : 0
    const existing = mode === 'edit' ? lead : null
    setQualifiedDraft(existing ? {
      name: existing.name || '',
      phone: existing.phone || '',
      location: existing.location || '',
      website: existing.website || '',
      qualification_status: existing.qualification_status,
      lead_score: String(existing.lead_score ?? 0),
      notes: existing.notes || '',
    } : {
      ...EMPTY_QUALIFIED_DRAFT,
      name: lead?.name || '',
      phone: lead?.phone || '',
      location: lead?.location || '',
      website: lead?.website || '',
      qualification_status: defaultScore >= 70 ? 'Qualified Lead' : defaultScore >= 40 ? 'Partially Qualified Lead' : 'Not Qualified Lead',
      lead_score: String(defaultScore),
      notes: lead?.analysis?.summary || '',
    })
    setQualifiedModal({ mode, sourceLeadId: mode === 'source' ? sourceId : null, recordId: existing?.id || null })
    setFormErrors({})
  }

  const validateQualifiedDraft = () => {
    const nextErrors = {}
    if (!qualifiedDraft.name.trim()) nextErrors.name = 'Business name is required.'
    if (qualifiedDraft.phone.trim()) {
      const phone = qualifiedDraft.phone.trim()
      const digitCount = phone.replace(/\D/g, '').length
      if (!/^\+?[\d().\s-]+$/.test(phone) || digitCount < 7 || digitCount > 15) {
        nextErrors.phone = 'Enter a valid phone number with 7 to 15 digits.'
      }
    }
    if (qualifiedDraft.website.trim()) {
      try {
        const normalizedUrl = /^https?:\/\//i.test(qualifiedDraft.website.trim())
          ? qualifiedDraft.website.trim()
          : `https://${qualifiedDraft.website.trim()}`
        const parsedUrl = new URL(normalizedUrl)
        if (!parsedUrl.hostname.includes('.') || !['http:', 'https:'].includes(parsedUrl.protocol)) {
          nextErrors.website = 'Enter a valid website URL.'
        }
      } catch {
        nextErrors.website = 'Enter a valid website URL.'
      }
    }
    const score = Number(qualifiedDraft.lead_score)
    if (qualifiedDraft.lead_score === '' || !Number.isInteger(score) || score < 0 || score > 100) {
      nextErrors.lead_score = 'Lead score must be an integer from 0 to 100.'
    }
    if (!QUALIFICATION_STATUSES.includes(qualifiedDraft.qualification_status)) {
      nextErrors.qualification_status = 'Select a qualification status.'
    }
    setFormErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSaveQualifiedLead = async (event) => {
    event.preventDefault()
    if (!validateQualifiedDraft()) return

    const website = qualifiedDraft.website.trim()
      ? (/^https?:\/\//i.test(qualifiedDraft.website.trim()) ? qualifiedDraft.website.trim() : `https://${qualifiedDraft.website.trim()}`)
      : ''
    const payload = { ...qualifiedDraft, website }
    setSavingQualified(true)
    try {
      if (qualifiedModal.mode === 'edit') {
        await updateQualifiedLead(qualifiedModal.recordId, payload)
      } else {
        await saveQualifiedLead(payload, qualifiedModal.sourceLeadId)
      }
      setQualifiedModal(null)
      showToast(qualifiedModal.mode === 'edit' ? 'Qualified lead updated.' : 'Lead saved to the database.')
      await refreshQualifiedLeads()
    } catch (saveError) {
      if (saveError.code === '23505' && qualifiedModal.sourceLeadId) {
        const records = await refreshQualifiedLeads()
        if (records?.some((record) => record.source_lead_id === qualifiedModal.sourceLeadId)) {
          setQualifiedModal(null)
          showToast('This generated lead is already in the database.')
          return
        }
      }
      showToast(saveError.message || 'Unable to save this lead. Your generated leads are unchanged.', 'error')
    } finally {
      setSavingQualified(false)
    }
  }

  const handleDeleteQualifiedLead = async (lead) => {
    if (!window.confirm(`Delete ${lead.name} from Qualified Leads? This cannot be undone.`)) return
    try {
      await deleteQualifiedLead(lead.id)
      showToast('Qualified lead deleted.')
      await refreshQualifiedLeads()
    } catch (deleteError) {
      showToast(deleteError.message || 'Unable to delete this qualified lead.', 'error')
    }
  }

  const handleQualifiedSignIn = () => {
    setQualifiedModal(null)
    setActiveView('qualified')
    setAuthMode('signin')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <img className="brand-mark" src="/techie-crew-logo.svg" alt="Techie Crew logo" />
          <div className="brand-copy">
            <strong>techieCrew</strong>
            <small>AI PIPELINE</small>
          </div>
        </div>

        <nav className="side-nav" aria-label="Sidebar navigation">
          <button type="button" className={`nav-link ${activeView === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveView('dashboard')}>Dashboard</button>
          <button type="button" className={`nav-link ${activeView === 'qualified' ? 'active' : ''}`} onClick={() => setActiveView('qualified')}>Qualified Leads</button>
        </nav>

        <div className="account">
          <div className="avatar">AD</div>
          <div>
            <strong>Admin</strong>
            <span>Operations</span>
          </div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div className="crumb-brand">
            <img className="mini-mark" src="/techie-crew-logo.svg" alt="" />
            <span>Lead Management</span>
          </div>
        </header>

        <div className="main-content">
          {activeView === 'dashboard' ? (
            <>
          <section className="page-heading">
            <div className="eyebrow">
              <span className="pulse-dot" aria-hidden="true"></span>
              Growth dashboard
            </div>
            <h1>techieCrew Generation Studio</h1>
            <p>Process bulk leads and analyze the business website quality before outreach.</p>
          </section>

          <section className="metrics-grid" aria-label="Dashboard metrics">
            {metrics.map((metric) => (
              <div key={metric.label} className="metric-card">
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
              </div>
            ))}
          </section>

          <section className="card-panel">
            <div className="panel-header">
              <h2>Bulk Lead Input</h2>
            </div>

            <div className="bulk-form">
              <textarea
                value={bulkText}
                onChange={handleBulkChange}
                placeholder="Paste your leads JSON here..."
                rows={14}
                className="bulk-textarea"
              />

              <div className="bulk-meta-row">
                <span className="lead-count">
                  {leadCount > 0 ? `${leadCount} Lead${leadCount === 1 ? '' : 's'} detected` : 'No leads detected'}
                </span>
                <div className="bulk-actions">
                  <button type="button" className="primary-button" onClick={handleProcessLeads} disabled={loading}>
                    {loading ? 'Processing Leads...' : 'Process Leads'}
                  </button>
                  <button type="button" className="secondary-button" onClick={handleClear}>
                    Clear
                  </button>
                </div>
              </div>
            </div>

            {loading ? <div className="feedback info">Processing Leads...</div> : null}
            {error ? <div className="feedback error">{error}</div> : null}
          </section>

          {leads.length > 0 ? (
            <section className="result-panel">
              <div className="result-header">
                <h2>Processed Leads</h2>
                <button type="button" className="danger-button small-button" onClick={handleClearAllData}>
                  Clear All Data
                </button>
              </div>

              <div className="lead-grid">
                {leads.map((lead) => {
                  const isEditing = editingLeadId === lead.id
                  const analysis = lead.analysis || {}
                  const analysisFields = Object.entries(analysis).filter(([key, value]) => {
                    if (key === 'strengths' || key === 'weaknesses' || key === 'summary') {
                      return false
                    }
                    return value !== undefined && value !== null
                  })

                  return (
                    <article key={lead.id} className="lead-card">
                      {isEditing ? (
                        <div className="edit-form">
                          <label>
                            <span>Name</span>
                            <input
                              type="text"
                              value={draftLead.name}
                              onChange={(event) => setDraftLead((prev) => ({ ...prev, name: event.target.value }))}
                            />
                          </label>
                          <label>
                            <span>Phone</span>
                            <input
                              type="text"
                              value={draftLead.phone}
                              onChange={(event) => setDraftLead((prev) => ({ ...prev, phone: event.target.value }))}
                            />
                          </label>
                          <label>
                            <span>Location</span>
                            <input
                              type="text"
                              value={draftLead.location}
                              onChange={(event) => setDraftLead((prev) => ({ ...prev, location: event.target.value }))}
                            />
                          </label>
                          <label>
                            <span>Website</span>
                            <input
                              type="text"
                              value={draftLead.website}
                              onChange={(event) => setDraftLead((prev) => ({ ...prev, website: event.target.value }))}
                            />
                          </label>
                          <div className="card-actions edit-actions">
                            <button type="button" className="primary-button small-button" onClick={handleSaveLead}>Save</button>
                            <button type="button" className="secondary-button small-button" onClick={() => setEditingLeadId(null)}>Cancel</button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="lead-card-header">
                            <h3>{lead.name || 'Unnamed Lead'}</h3>
                          </div>

                          <div className="lead-meta-list">
                            <div className="lead-meta-item"><span>Name</span><strong>{lead.name || 'N/A'}</strong></div>
                            <div className="lead-meta-item"><span>Phone</span><strong>{lead.phone || 'N/A'}</strong></div>
                            <div className="lead-meta-item"><span>Location</span><strong>{lead.location || 'N/A'}</strong></div>
                            <div className="lead-meta-item wide"><span>Website</span><strong>{formatWebsiteValue(lead.website)}</strong></div>
                          </div>

                          {lead.error ? (
                            <div className="lead-error">{lead.error}</div>
                          ) : (
                            <div className="analysis-list">
                              {analysisFields.map(([key, value]) => (
                                <div key={`${lead.id}-${key}`} className="analysis-line">
                                  <span>{formatAnalysisLabel(key)}</span>
                                  <strong>{typeof value === 'boolean' ? (value ? '✓' : '✕') : value}</strong>
                                </div>
                              ))}

                              {analysis.website_quality_score !== undefined ? (
                                <div className="analysis-line">
                                  <span>Website Quality Score</span>
                                  <strong>{analysis.website_quality_score}/100</strong>
                                </div>
                              ) : null}

                              {analysis.summary ? (
                                <div className="summary-box compact">
                                  <strong>Summary:</strong> {analysis.summary}
                                </div>
                              ) : null}
                            </div>
                          )}

                          <div className="card-actions">
                            <button type="button" className="secondary-button small-button" onClick={() => handleOpenEditor(lead)}>Update</button>
                            <button type="button" className="danger-button small-button" onClick={() => handleDeleteLead(lead.id)}>Delete</button>
                            <button
                              type="button"
                              className="primary-button small-button"
                              disabled={savedSourceLeadIds.has(lead.id)}
                              onClick={() => openQualifiedForm(lead)}
                            >
                              {savedSourceLeadIds.has(lead.id) ? 'Already Added' : 'Add to Database'}
                            </button>
                          </div>
                        </>
                      )}
                    </article>
                  )
                })}
              </div>
            </section>
          ) : null}
            </>
          ) : (
            <section className="qualified-section">
              <div className="qualified-heading">
                <div>
                  <div className="eyebrow"><span className="pulse-dot" aria-hidden="true"></span>Persistent workspace</div>
                  <h1>Qualified Leads</h1>
                  <p>Review and manage the leads your team has approved for the database.</p>
                </div>
                {session ? (
                  <div className="account-actions">
                    <span>{session.user.email}</span>
                    <button type="button" className="secondary-button small-button" onClick={handleSignOut}>Sign out</button>
                  </div>
                ) : null}
              </div>

              {!hasSupabaseConfig ? (
                <div className="database-state error-state">
                  <h2>Supabase configuration required</h2>
                  <p>Add <code>VITE_SUPABASE_URL</code> and <code>VITE_SUPABASE_ANON_KEY</code> to a local <code>.env.local</code> file, then restart the frontend.</p>
                </div>
              ) : !authReady ? (
                <div className="database-state">Checking your session...</div>
              ) : (
                <div className="database-panel">
                  <div className="database-toolbar">
                    <div className="table-filters">
                      <label className="search-control">
                        <span className="visually-hidden">Search qualified leads</span>
                        <input type="search" placeholder="Search business, phone, location..." value={qualifiedSearch} onChange={(event) => { setQualifiedSearch(event.target.value); setQualifiedPage(1) }} />
                      </label>
                      <label className="filter-control">
                        <span className="visually-hidden">Filter by qualification status</span>
                        <select value={qualifiedStatusFilter} onChange={(event) => { setQualifiedStatusFilter(event.target.value); setQualifiedPage(1) }}>
                          <option>All statuses</option>
                          {QUALIFICATION_STATUSES.map((status) => <option key={status}>{status}</option>)}
                        </select>
                      </label>
                    </div>
                    <button type="button" className="secondary-button small-button" onClick={refreshQualifiedLeads} disabled={qualifiedLoading}>
                      {qualifiedLoading ? <><span className="loading-spinner" aria-hidden="true"></span> Refreshing...</> : 'Refresh'}
                    </button>
                  </div>
                  {qualifiedError ? <div className="feedback error database-feedback">{qualifiedError}</div> : null}
                  {qualifiedLoading && qualifiedLeads.length === 0 ? (
                    <div className="database-state">Loading qualified leads...</div>
                  ) : qualifiedLeads.length === 0 ? (
                    <div className="database-state">
                      <h2>No qualified leads yet</h2>
                      <p>Add a generated lead to the database after reviewing its details.</p>
                    </div>
                  ) : filteredQualifiedLeads.length === 0 ? (
                    <div className="database-state">No leads match these search filters.</div>
                  ) : (
                    <>
                      <div className="table-scroll">
                        <table className="qualified-table">
                          <thead><tr>
                            <th>Business Name</th><th>Phone</th><th>Location</th><th>Website</th>
                            <th>Qualification Status</th><th>Lead Score</th><th>Created Date</th><th>Actions</th>
                          </tr></thead>
                          <tbody>
                            {visibleQualifiedLeads.map((lead) => (
                              <tr key={lead.id}>
                                <td className="business-cell">{lead.name}</td>
                                <td>{lead.phone || '—'}</td>
                                <td>{lead.location || '—'}</td>
                                <td>{lead.website ? <a href={lead.website} target="_blank" rel="noreferrer">{lead.website}</a> : '—'}</td>
                                <td><span className={`status-badge ${lead.qualification_status === 'Qualified Lead' ? 'qualified' : lead.qualification_status === 'Partially Qualified Lead' ? 'partial' : 'not-qualified'}`}>{lead.qualification_status}</span></td>
                                <td>{lead.lead_score}/100</td>
                                <td>{new Date(lead.created_at).toLocaleDateString()}</td>
                                <td><div className="table-actions">
                                  <button type="button" onClick={() => setDetailLead(lead)}>View</button>
                                  <button type="button" onClick={() => openQualifiedForm(lead, 'edit')}>Edit</button>
                                  <button type="button" className="delete-action" onClick={() => handleDeleteQualifiedLead(lead)}>Delete</button>
                                </div></td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                      <div className="table-footer">
                        <span>{filteredQualifiedLeads.length} record{filteredQualifiedLeads.length === 1 ? '' : 's'}</span>
                        <div className="pagination-controls">
                          <button type="button" className="secondary-button small-button" onClick={() => setQualifiedPage((page) => Math.max(1, page - 1))} disabled={qualifiedPage <= 1}>Previous</button>
                          <span>Page {qualifiedPage} of {qualifiedPageCount}</span>
                          <button type="button" className="secondary-button small-button" onClick={() => setQualifiedPage((page) => Math.min(qualifiedPageCount, page + 1))} disabled={qualifiedPage >= qualifiedPageCount}>Next</button>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}
            </section>
          )}
        </div>
      </main>

      {qualifiedModal ? (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget && !savingQualified) setQualifiedModal(null) }}>
          <form className="lead-modal" role="dialog" aria-modal="true" onSubmit={handleSaveQualifiedLead} aria-labelledby="qualified-modal-title">
            <div className="modal-heading">
              <div><span className="modal-kicker">Lead qualification</span><h2 id="qualified-modal-title">{qualifiedModal.mode === 'edit' ? 'Edit qualified lead' : 'Add to database'}</h2></div>
              <button type="button" className="modal-close" aria-label="Close form" onClick={() => setQualifiedModal(null)} disabled={savingQualified}>×</button>
            </div>
            <div className="modal-fields">
              <label className="field-control"><span>Business Name <b>*</b></span><input autoFocus value={qualifiedDraft.name} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, name: event.target.value }))} aria-invalid={Boolean(formErrors.name)} />{formErrors.name ? <small className="field-error">{formErrors.name}</small> : null}</label>
              <label className="field-control"><span>Phone Number</span><input type="tel" value={qualifiedDraft.phone} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, phone: event.target.value }))} aria-invalid={Boolean(formErrors.phone)} />{formErrors.phone ? <small className="field-error">{formErrors.phone}</small> : null}</label>
              <label className="field-control"><span>Business Location</span><input value={qualifiedDraft.location} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, location: event.target.value }))} /></label>
              <label className="field-control"><span>Website URL</span><input type="text" inputMode="url" placeholder="https://example.com" value={qualifiedDraft.website} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, website: event.target.value }))} aria-invalid={Boolean(formErrors.website)} />{formErrors.website ? <small className="field-error">{formErrors.website}</small> : null}</label>
              <label className="field-control"><span>Qualification Status</span><select value={qualifiedDraft.qualification_status} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, qualification_status: event.target.value }))}>{QUALIFICATION_STATUSES.map((status) => <option key={status}>{status}</option>)}</select></label>
              <label className="field-control"><span>Lead Score (0–100)</span><input type="number" min="0" max="100" step="1" value={qualifiedDraft.lead_score} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, lead_score: event.target.value }))} aria-invalid={Boolean(formErrors.lead_score)} />{formErrors.lead_score ? <small className="field-error">{formErrors.lead_score}</small> : null}</label>
              <label className="field-control full-field"><span>Notes</span><textarea rows="3" value={qualifiedDraft.notes} onChange={(event) => setQualifiedDraft((draft) => ({ ...draft, notes: event.target.value }))} /></label>
            </div>
            <div className="modal-actions">
              <button type="button" className="secondary-button" onClick={() => setQualifiedModal(null)} disabled={savingQualified}>Cancel</button>
              <button type="submit" className="primary-button" disabled={savingQualified}>
                {savingQualified ? <><span className="loading-spinner" aria-hidden="true"></span> Saving...</> : qualifiedModal.mode === 'edit' ? 'Save Changes' : 'Save to Database'}
              </button>
            </div>
          </form>
        </div>
      ) : null}

      {detailLead ? (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setDetailLead(null) }}>
          <section className="lead-modal detail-modal" role="dialog" aria-modal="true" aria-labelledby="detail-modal-title">
            <div className="modal-heading"><div><span className="modal-kicker">Qualified lead</span><h2 id="detail-modal-title">{detailLead.name}</h2></div><button type="button" className="modal-close" aria-label="Close details" onClick={() => setDetailLead(null)}>×</button></div>
            <dl className="detail-list">
              <div><dt>Phone</dt><dd>{detailLead.phone || 'Not provided'}</dd></div>
              <div><dt>Location</dt><dd>{detailLead.location || 'Not provided'}</dd></div>
              <div><dt>Website</dt><dd>{detailLead.website || 'Not provided'}</dd></div>
              <div><dt>Qualification Status</dt><dd>{detailLead.qualification_status}</dd></div>
              <div><dt>Lead Score</dt><dd>{detailLead.lead_score}/100</dd></div>
              <div><dt>Created</dt><dd>{new Date(detailLead.created_at).toLocaleString()}</dd></div>
              <div className="detail-notes"><dt>Notes</dt><dd>{detailLead.notes || 'No notes'}</dd></div>
            </dl>
          </section>
        </div>
      ) : null}

      {toast ? <div className={`toast ${toast.kind}`} role={toast.kind === 'error' ? 'alert' : 'status'}>{toast.message}<button type="button" aria-label="Dismiss notification" onClick={() => setToast(null)}>×</button></div> : null}
    </div>
  )
}

export default App
