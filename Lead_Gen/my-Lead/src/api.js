const API_BASE_URL = 'http://127.0.0.1:8000';

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  return contentType.includes('application/json')
    ? await response.json().catch(() => ({}))
    : {};
}

export async function runLeadAnalysis(lead) {
  const response = await fetch(`${API_BASE_URL}/process-leads`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ leads: [lead] }),
  });

  const data = await parseResponse(response);

  if (!response.ok) {
    const message =
      data?.detail?.message ||
      data?.message ||
      data?.detail ||
      'Something went wrong while analyzing the lead.';

    throw new Error(message);
  }

  if (data?.results && data.results.length > 0) {
    return data.results[0];
  }

  return data;
}

export async function bulkProcessLeads(leads) {
  const response = await fetch(`${API_BASE_URL}/process-leads`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ leads }),
  });

  const data = await parseResponse(response);

  if (!response.ok) {
    const message =
      data?.detail?.message ||
      data?.message ||
      data?.detail ||
      'Something went wrong while processing the leads.';

    throw new Error(message);
  }

  return data;
}
