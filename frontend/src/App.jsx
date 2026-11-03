import React, { useState, useEffect, useMemo } from 'react';
import { API } from './api';

export default function App() {
  const [currentTab, setCurrentTab] = useState('home');
  const [portfolio, setPortfolio] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [digest, setDigest] = useState(null);
  const [digestWindow, setDigestWindow] = useState(24);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  // Research State
  const [researchTicker, setResearchTicker] = useState('TCS');
  const [researchQuery, setResearchQuery] = useState('Analyze financial trajectory, guidance vs actuals, and bull vs bear case');
  const [researchResult, setResearchResult] = useState(null);
  const [researchLoading, setResearchLoading] = useState(false);

  // Source Citation Modal
  const [sourceModal, setSourceModal] = useState({ open: false, docId: '', pageNum: 1, text: '', title: '' });

  // Settings State
  const [alertSettings, setAlertSettings] = useState({
    price_move_threshold: 3.0,
    volume_mult_threshold: 2.0,
    digest_window_hours: 24,
    monitored_categories: []
  });

  const refreshData = async () => {
    try {
      const [portData, alertData, annData, digData, statData, settData] = await Promise.all([
        API.getPortfolio(),
        API.getAlerts(),
        API.getAnnouncements({ window_hours: digestWindow }),
        API.getDigest(digestWindow),
        API.getStatus(),
        API.getAlertSettings()
      ]);
      setPortfolio(portData);
      setAlerts(alertData);
      setAnnouncements(annData);
      setDigest(digData);
      setSystemStatus(statData);
      setAlertSettings(settData);
    } catch (e) {
      console.error("Data fetch failed", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
  }, [digestWindow]);

  useEffect(() => {
    if (!researchResult && !researchLoading) {
      handleExecuteResearch('TCS', 'Analyze financial trajectory, guidance vs actuals, and bull vs bear case');
    }
  }, []);

  const handleExecuteResearch = async (ticker, query) => {
    setResearchLoading(true);
    setResearchTicker(ticker);
    try {
      const res = await API.runResearch(ticker, query || researchQuery);
      setResearchResult(res);
    } catch (e) {
      console.error("Research failed", e);
    } finally {
      setResearchLoading(false);
    }
  };

  const handleAcknowledgeAlert = async (alertId) => {
    await API.acknowledgeAlert(alertId);
    setAlerts(prev => prev.map(a => a.id === alertId ? { ...a, acknowledged: true } : a));
  };

  const openCitation = async (docId, pageNum, title) => {
    try {
      const pageData = await API.getPageText(docId, pageNum);
      setSourceModal({
        open: true,
        docId,
        pageNum,
        title: title || docId,
        text: pageData.text
      });
    } catch (e) {
      alert(`Could not load primary page ${pageNum} for ${docId}`);
    }
  };

  const unacknowledgedAlertCount = useMemo(() => {
    return alerts.filter(a => !a.acknowledged).length;
  }, [alerts]);

  return (
    <div className="flex flex-col min-h-screen pb-20 md:pb-6 bg-finn-bg text-slate-100 font-sans">
      {/* HEADER */}
      <header className="sticky top-0 z-40 bg-finn-surface/90 backdrop-blur-md border-b border-finn-border px-4 py-2.5 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-finn-accent to-indigo-600 flex items-center justify-center font-mono font-bold text-slate-900 text-sm">
            FN
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-mono font-extrabold text-sm tracking-wider text-slate-100">FINN</span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/30">
                ENAM INTELLIGENCE
              </span>
            </div>
          </div>
        </div>

        {portfolio && (
          <div className="text-right">
            <div className="text-[10px] uppercase font-mono text-finn-textMuted">NAV</div>
            <div className="text-xs sm:text-sm font-mono font-bold text-slate-100">
              ₹{(portfolio.total_value_inr / 100000).toFixed(2)}L
              <span className={`ml-1.5 text-[11px] ${portfolio.day_change_pct >= 0 ? 'text-finn-gain' : 'text-finn-loss'}`}>
                {portfolio.day_change_pct >= 0 ? '+' : ''}{portfolio.day_change_pct.toFixed(2)}%
              </span>
            </div>
          </div>
        )}
      </header>

      {/* TICKER TAPE */}
      {portfolio && (
        <div className="bg-finn-bg border-b border-finn-border py-1.5 px-2 overflow-x-auto text-[11px] font-mono flex space-x-3">
          {portfolio.stocks.map(s => (
            <button
              key={s.ticker}
              onClick={() => {
                setCurrentTab('research');
                handleExecuteResearch(s.ticker, 'Recent trajectory & guidance execution');
              }}
              className="flex items-center space-x-1.5 px-2 py-0.5 rounded bg-finn-card border border-finn-border/70 hover:border-finn-accent transition-colors shrink-0"
            >
              <span className="font-bold text-slate-200">{s.ticker}</span>
              <span className="text-slate-400">₹{s.price.toFixed(1)}</span>
              <span className={s.change_pct >= 0 ? 'text-finn-gain' : 'text-finn-loss'}>
                {s.change_pct >= 0 ? '+' : ''}{s.change_pct.toFixed(1)}%
              </span>
            </button>
          ))}
        </div>
      )}

      {/* MAIN CONTAINER */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6">
        {loading ? (
          <div className="text-center py-20 font-mono text-xs text-finn-textMuted">LOADING TERMINAL...</div>
        ) : (
          <div>
            {currentTab === 'home' && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-finn-card border border-finn-border rounded-lg p-3">
                    <div className="text-[10px] font-mono uppercase text-finn-textMuted">Total Value</div>
                    <div className="text-base font-mono font-bold mt-1">₹{(portfolio.total_value_inr / 100000).toFixed(2)}L</div>
                  </div>
                  <div className="bg-finn-card border border-finn-border rounded-lg p-3">
                    <div className="text-[10px] font-mono uppercase text-finn-textMuted">Day Change</div>
                    <div className={`text-base font-mono font-bold mt-1 ${portfolio.day_change_pct >= 0 ? 'text-finn-gain' : 'text-finn-loss'}`}>
                      {portfolio.day_change_pct >= 0 ? '+' : ''}{portfolio.day_change_pct.toFixed(2)}%
                    </div>
                  </div>
                  <div className="bg-finn-card border border-finn-border rounded-lg p-3">
                    <div className="text-[10px] font-mono uppercase text-finn-textMuted">Active Alerts</div>
                    <div className="text-base font-mono font-bold mt-1 text-amber-400">{unacknowledgedAlertCount} Unread</div>
                  </div>
                  <div className="bg-finn-card border border-finn-border rounded-lg p-3">
                    <div className="text-[10px] font-mono uppercase text-finn-textMuted">Top Gainer</div>
                    <div className="text-base font-mono font-bold mt-1 text-finn-gain">
                      {portfolio.top_gainers[0]?.ticker} (+{portfolio.top_gainers[0]?.change_pct}%)
                    </div>
                  </div>
                </div>

                {digest && (
                  <div className="bg-finn-card border border-finn-border rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-mono text-xs font-bold text-sky-400 uppercase">Daily Executive Digest</span>
                      <div className="flex space-x-1 font-mono text-xs">
                        {[24, 72, 168].map(h => (
                          <button
                            key={h}
                            onClick={() => setDigestWindow(h)}
                            className={`px-2 py-0.5 rounded text-[10px] ${digestWindow === h ? 'bg-finn-accent text-slate-900 font-bold' : 'text-slate-400'}`}
                          >
                            {h === 24 ? '24H' : h === 72 ? '3D' : '7D'}
                          </button>
                        ))}
                      </div>
                    </div>
                    <p className="text-xs text-sky-200 bg-sky-950/20 p-2.5 rounded border border-sky-500/20">{digest.executive_takeaway}</p>
                  </div>
                )}
              </div>
            )}

            {currentTab === 'alerts' && (
              <div className="space-y-3">
                <h2 className="text-sm font-mono font-bold text-slate-100 uppercase">Triggered Alerts Feed</h2>
                {alerts.map(a => (
                  <div key={a.id} className="bg-finn-card border border-finn-border rounded-lg p-3 flex justify-between items-center">
                    <div>
                      <div className="text-xs font-bold text-slate-100">{a.ticker} • {a.title}</div>
                      <div className="text-[11px] text-slate-400">{a.description}</div>
                    </div>
                    {!a.acknowledged && (
                      <button
                        onClick={() => handleAcknowledgeAlert(a.id)}
                        className="px-2 py-1 rounded bg-finn-surface border border-finn-border text-[10px] font-mono"
                      >
                        Dismiss
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}

            {currentTab === 'research' && result && (
              <div className="space-y-4">
                <div className="bg-finn-card border border-finn-border rounded-xl p-4 flex justify-between items-center">
                  <div>
                    <h2 className="text-base font-mono font-bold text-slate-100">{result.company_name} ({result.ticker})</h2>
                    <span className="text-[10px] font-mono text-emerald-400">Grounded in Primary Documents • Zero Fabrications</span>
                  </div>
                </div>

                <div className="bg-finn-card border border-finn-border rounded-xl p-4">
                  <h3 className="text-xs font-mono font-bold text-sky-400 uppercase mb-2">Narrative vs Numbers</h3>
                  <div className="text-xs text-slate-200 whitespace-pre-wrap">{result.narrative_vs_numbers.content}</div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-4">
                    <h3 className="text-xs font-mono font-bold text-emerald-400 uppercase mb-2">Bull Thesis</h3>
                    <div className="text-xs text-slate-200 whitespace-pre-wrap">{result.bull_case.content}</div>
                  </div>
                  <div className="bg-rose-950/20 border border-rose-500/30 rounded-xl p-4">
                    <h3 className="text-xs font-mono font-bold text-rose-400 uppercase mb-2">Bear Thesis</h3>
                    <div className="text-xs text-slate-200 whitespace-pre-wrap">{result.bear_case.content}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* FOOTER TAB BAR */}
      <footer className="fixed bottom-0 left-0 right-0 z-40 bg-finn-surface border-t border-finn-border py-2 px-4 flex justify-around md:hidden">
        {['home', 'alerts', 'research', 'settings'].map(tab => (
          <button
            key={tab}
            onClick={() => setCurrentTab(tab)}
            className={`text-xs font-mono uppercase ${currentTab === tab ? 'text-finn-accent font-bold' : 'text-slate-400'}`}
          >
            {tab}
          </button>
        ))}
      </footer>
    </div>
  );
}
