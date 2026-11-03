// API Client for FINN Frontend

export const API = {
  getStatus: () => fetch('/api/status').then(r => r.json()),
  getPortfolio: () => fetch('/api/portfolio').then(r => r.json()),
  getStock: (ticker) => fetch(`/api/stocks/${ticker}`).then(r => r.json()),
  getAnnouncements: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return fetch(`/api/announcements?${query}`).then(r => r.json());
  },
  getAlerts: () => fetch('/api/alerts').then(r => r.json()),
  acknowledgeAlert: (id) => fetch(`/api/alerts/acknowledge/${id}`, { method: 'POST' }).then(r => r.json()),
  getAlertSettings: () => fetch('/api/alerts/settings').then(r => r.json()),
  updateAlertSettings: (settings) => fetch('/api/alerts/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings)
  }).then(r => r.json()),
  getDigest: (windowHours = 24) => fetch(`/api/digest?window_hours=${windowHours}`).then(r => r.json()),
  runResearch: (ticker, query) => fetch('/api/research/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker, query })
  }).then(r => r.json()),
  getDocuments: (ticker) => fetch(`/api/research/documents/${ticker}`).then(r => r.json()),
  getPageText: (docId, pageNum) => fetch(`/api/research/document/${docId}/page/${pageNum}`).then(r => r.json())
};

