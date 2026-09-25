import React, { useState, useEffect } from 'react';
import './App.css';

const DEFAULT_SAMPLE_TRANSCRIPT = `[00:07] Client: Oh, wonderful, a real human. I'm calling to thank you for the hundred dollar roaming charge on my bill. Truly the highlight of my month.
[00:09] Agent: I'm sorry about the charge, sir. Let me see what happened. Could I have your account number?
[00:12] Client: Sure. It's 8820-423. And I'll save you some time, I bought the unlimited travel pass before my trip. But apparently that's just decoration.
[00:17] Agent: I appreciate that, thank you. Let me check when the pass was activated versus when your data usage began.
[00:22] Client: Take your time. It's not like I have anything better to do than argue over pay-per-megabyte rates I already paid to avoid.
[00:27] Agent: I see it. The pass was set to activate on the wrong time zone, so it started the day after you landed.
[00:32] Client: Ah, so the system decided I arrived tomorrow. Fascinating. Maybe I should ask it for next week's lottery numbers.
[00:37] Agent: I understand the frustration. That was a system error, and I'm crediting the full hundred dollars to your account.
[00:42] Client: The full hundred? Wow, you're giving me my own money back. How generous.
[00:47] Agent: I'm also correcting the pass dates so it covers the whole length of your trip.
[00:52] Client: Great. Because I still have four days left, and I'd hate to accidentally fund your quarterly bonus again.
[00:57] Agent: Understood. I've added a usage alert so you'll get a text before any charges apply.
[01:02] Client: A text about charges. From the company that charged me. The irony is delicious, but okay, I'll take it.
[01:07] Agent: Is there anything else I can help you with today?
[01:12] Client: No, I think you've done enough. Fine, honestly, thanks for actually fixing it. That part I mean sincerely.
[01:17] Agent: I appreciate that, sir. Enjoy the rest of your trip.`;

function generateCallId() {
  const chars = 'abcdef0123456789';
  let rand = '';
  for (let i = 0; i < 6; i++) {
    rand += chars[Math.floor(Math.random() * chars.length)];
  }
  return `call_36min_${rand}`;
}

export default function App() {
  // Navigation & Settings
  const [activeTab, setActiveTab] = useState('criteria'); // 'criteria' or 'evaluate'
  const [targetPort, setTargetPort] = useState('8000'); // '8000' (App) or '8005' (Gateway)
  const apiBase = `http://localhost:${targetPort}/api`;

  // Tenants & Criteria state
  const [tenants, setTenants] = useState([]);
  const [selectedTenant, setSelectedTenant] = useState('');
  const [criteriaData, setCriteriaData] = useState({ categories: [], category_weights: {} });
  const [loadingCriteria, setLoadingCriteria] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState('');

  // Add Tenant Modal
  const [showAddTenant, setShowAddTenant] = useState(false);
  const [newTenantId, setNewTenantId] = useState('');
  const [newTenantName, setNewTenantName] = useState('');

  // Add Criterion Modal
  const [showAddCriterion, setShowAddCriterion] = useState(false);
  const [critCategoryId, setCritCategoryId] = useState('');
  const [critName, setCritName] = useState('');
  const [critDeduction, setCritDeduction] = useState(15);
  const [critDescription, setCritDescription] = useState('');

  // Evaluate View State
  const [callId, setCallId] = useState(generateCallId());
  const [channel, setChannel] = useState('Call');
  const [customerName, setCustomerName] = useState('');
  const [transcript, setTranscript] = useState(DEFAULT_SAMPLE_TRANSCRIPT);
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [evalError, setEvalError] = useState('');

  // Fetch tenants on mount
  useEffect(() => {
    fetchTenants();
  }, [targetPort]);

  // Fetch criteria when tenant changes
  useEffect(() => {
    if (selectedTenant) {
      fetchCriteria(selectedTenant);
    }
  }, [selectedTenant, targetPort]);

  const showNotification = (msg) => {
    setFeedbackMsg(msg);
    setTimeout(() => setFeedbackMsg(''), 4000);
  };

  const fetchTenants = async () => {
    try {
      const res = await fetch(`${apiBase}/tenants`);
      if (res.ok) {
        const data = await res.json();
        setTenants(data);
        if (data.length > 0) {
          setSelectedTenant(prev => prev && data.some(t => t.tenant_id === prev) ? prev : data[0].tenant_id);
        }
      }
    } catch (err) {
      console.error('Failed to fetch tenants:', err);
    }
  };

  const fetchCriteria = async (tenantId) => {
    setLoadingCriteria(true);
    try {
      const res = await fetch(`${apiBase}/tenants/${tenantId}/criteria`);
      if (res.ok) {
        const data = await res.json();
        setCriteriaData(data);
        if (data.categories && data.categories.length > 0 && !critCategoryId) {
          setCritCategoryId(data.categories[0].category_id);
        }
      }
    } catch (err) {
      console.error('Failed to fetch criteria:', err);
    } finally {
      setLoadingCriteria(false);
    }
  };

  const handleToggle = async (lineItemId, currentStatus) => {
    const nextStatus = !currentStatus;
    // Optimistic UI update
    setCriteriaData(prev => ({
      ...prev,
      categories: prev.categories.map(cat => ({
        ...cat,
        line_items: cat.line_items.map(item =>
          item.line_item_id === lineItemId ? { ...item, is_active: nextStatus } : item
        )
      }))
    }));

    try {
      const res = await fetch(`${apiBase}/tenants/${selectedTenant}/criteria/${lineItemId}/toggle`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: nextStatus })
      });
      if (res.ok) {
        showNotification(`Criterion "${lineItemId}" ${nextStatus ? 'enabled' : 'disabled'} for ${selectedTenant}`);
      } else {
        // Rollback on error
        fetchCriteria(selectedTenant);
      }
    } catch (err) {
      console.error('Toggle error:', err);
      fetchCriteria(selectedTenant);
    }
  };

  const handleCreateTenant = async (e) => {
    e.preventDefault();
    if (!newTenantId.trim() || !newTenantName.trim()) return;
    try {
      const res = await fetch(`${apiBase}/tenants`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: newTenantId.trim(), name: newTenantName.trim() })
      });
      if (res.ok) {
        showNotification(`Created tenant ${newTenantId}`);
        setShowAddTenant(false);
        setNewTenantId('');
        setNewTenantName('');
        await fetchTenants();
        setSelectedTenant(newTenantId.trim());
      }
    } catch (err) {
      console.error('Create tenant error:', err);
    }
  };

  const handleCreateCriterion = async (e) => {
    e.preventDefault();
    if (!critName.trim() || !critCategoryId) return;
    try {
      const res = await fetch(`${apiBase}/criteria`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category_id: critCategoryId,
          name: critName.trim(),
          description: critDescription.trim(),
          deduction_value: parseInt(critDeduction, 10) || 10
        })
      });
      if (res.ok) {
        showNotification(`Created criterion "${critName}"`);
        setShowAddCriterion(false);
        setCritName('');
        setCritDescription('');
        fetchCriteria(selectedTenant);
      }
    } catch (err) {
      console.error('Create criterion error:', err);
    }
  };

  const handleDeleteCriterion = async (lineItemId, name) => {
    if (!window.confirm(`Delete criterion "${name}"?`)) return;
    try {
      const res = await fetch(`${apiBase}/criteria/${lineItemId}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        showNotification(`Deleted "${name}"`);
        fetchCriteria(selectedTenant);
      }
    } catch (err) {
      console.error('Delete criterion error:', err);
    }
  };

  const handleEvaluate = async () => {
    setEvaluating(true);
    setEvalError('');
    setEvaluationResult(null);

    const payload = {
      callId: callId,
      tenantId: selectedTenant,
      channel: channel,
      transcript: transcript
    };
    if (customerName && customerName.trim()) {
      payload.customer_name = customerName.trim();
    }

    try {
      const res = await fetch(`${apiBase}/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const data = await res.json();
        setEvaluationResult(data);
      } else {
        const errText = await res.text();
        setEvalError(`Evaluation failed (${res.status}): ${errText}`);
      }
    } catch (err) {
      setEvalError(`Connection error: ${err.message}. Make sure the backend server or API Gateway is running.`);
    } finally {
      setEvaluating(false);
    }
  };

  // Stats calculation
  const allItems = criteriaData.categories.flatMap(c => c.line_items || []);
  const activeItems = allItems.filter(i => i.is_active);
  const inactiveItems = allItems.filter(i => !i.is_active);

  return (
    <div className="qa-app">
      {/* Top Navbar */}
      <header className="navbar">
        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button
            className={`tab-btn ${activeTab === 'criteria' ? 'active' : ''}`}
            onClick={() => setActiveTab('criteria')}
          >
            Criteria Manager
          </button>
          <button
            className={`tab-btn ${activeTab === 'evaluate' ? 'active' : ''}`}
            onClick={() => setActiveTab('evaluate')}
          >
            Evaluate Transcript
          </button>
        </nav>

        <div className="nav-controls">
          {/* Target port selector */}
          <div className="port-selector">
            <span className="control-label">API Target:</span>
            <select
              value={targetPort}
              onChange={(e) => setTargetPort(e.target.value)}
              className="port-select"
            >
              <option value="8000">Port 8000 (Main App)</option>
              <option value="8005">Port 8005 (API Gateway)</option>
            </select>
          </div>
        </div>
      </header>

      {/* Notification Toast */}
      {feedbackMsg && <div className="toast-notification">{feedbackMsg}</div>}

      {/* Main Content Area */}
      <main className="main-container">
        {/* VIEW 1: CRITERIA MANAGEMENT */}
        {activeTab === 'criteria' && (
          <section className="view-section">
            {/* Tenant Toolbar */}
            <div className="toolbar-card">
              <div className="toolbar-left">
                <label className="toolbar-label">Select Tenant:</label>
                <select
                  value={selectedTenant}
                  onChange={(e) => setSelectedTenant(e.target.value)}
                  className="tenant-select"
                >
                  {tenants.map(t => (
                    <option key={t.tenant_id} value={t.tenant_id}>
                      {t.name} ({t.tenant_id})
                    </option>
                  ))}
                </select>
                <button
                  className="btn btn-secondary"
                  onClick={() => setShowAddTenant(true)}
                >
                  + Add Tenant
                </button>
              </div>

              <div className="toolbar-right">
                <div className="stat-pill stat-total">Total: {allItems.length}</div>
                <div className="stat-pill stat-active">Active: {activeItems.length}</div>
                <div className="stat-pill stat-disabled">Disabled: {inactiveItems.length}</div>
                <button
                  className="btn btn-primary"
                  onClick={() => setShowAddCriterion(true)}
                >
                  + Add Criterion
                </button>
              </div>
            </div>

            {loadingCriteria ? (
              <div className="loading-state">Loading criteria from PostgreSQL...</div>
            ) : (
              <div className="categories-grid">
                {criteriaData.categories.map(cat => (
                  <div key={cat.category_id} className="category-card">
                    <div className="category-header">
                      <div>
                        <h2 className="category-name">{cat.name}</h2>
                        <span className="category-weight">
                          Weight: {(cat.category_weight * 100).toFixed(1)}%
                        </span>
                      </div>
                      <span className="category-count">
                        {cat.line_items.filter(i => i.is_active).length}/{cat.line_items.length} Active
                      </span>
                    </div>

                    <div className="criteria-list">
                      {cat.line_items.map(item => (
                        <div
                          key={item.line_item_id}
                          className={`criterion-row ${item.is_active ? 'active-row' : 'disabled-row'}`}
                        >
                          <div className="criterion-info">
                            <div className="criterion-title-line">
                              <span className="criterion-name">{item.name}</span>
                              <span className="deduction-badge">-{item.deduction_value} pts</span>
                            </div>
                            <p className="criterion-desc">{item.description}</p>
                          </div>

                          <div className="criterion-actions">
                            {/* Toggle Switch */}
                            <label className="switch" title="Toggle criterion active/inactive">
                              <input
                                type="checkbox"
                                checked={item.is_active}
                                onChange={() => handleToggle(item.line_item_id, item.is_active)}
                              />
                              <span className="slider round"></span>
                            </label>

                            {/* Delete button */}
                            <button
                              className="btn-icon delete-btn"
                              title="Delete criterion"
                              onClick={() => handleDeleteCriterion(item.line_item_id, item.name)}
                            >
                              ✕
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {/* VIEW 2: TRANSCRIPT EVALUATION */}
        {activeTab === 'evaluate' && (
          <section className="view-section evaluate-grid">
            {/* Input Panel */}
            <div className="eval-input-panel">
              <div className="panel-header">
                <h2>Interaction Input</h2>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => setTranscript(DEFAULT_SAMPLE_TRANSCRIPT)}
                >
                  Load Sample Roaming Call
                </button>
              </div>

              {/* Form Controls */}
              <div className="form-row">
                <div className="form-group flex-1">
                  <label>Tenant ID:</label>
                  <select
                    value={selectedTenant}
                    onChange={(e) => setSelectedTenant(e.target.value)}
                    className="input-control"
                  >
                    {tenants.map(t => (
                      <option key={t.tenant_id} value={t.tenant_id}>
                        {t.name} ({t.tenant_id})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group flex-1">
                  <label>Call ID:</label>
                  <div className="input-with-button">
                    <input
                      type="text"
                      value={callId}
                      onChange={(e) => setCallId(e.target.value)}
                      className="input-control"
                    />
                    <button
                      className="btn btn-secondary btn-icon-only"
                      onClick={() => setCallId(generateCallId())}
                      title="Generate new Call ID"
                    >
                      🎲
                    </button>
                  </div>
                </div>

                <div className="form-group flex-sm">
                  <label>Channel:</label>
                  <select
                    value={channel}
                    onChange={(e) => setChannel(e.target.value)}
                    className="input-control"
                  >
                    <option value="Call">Call</option>
                    <option value="Chat">Chat</option>
                  </select>
                </div>
              </div>

              {/* Transcript Textarea */}
              <div className="form-group transcript-group">
                <div className="textarea-header">
                  <label>Transcript:</label>
                  <span className="character-count">{transcript.split('\n').length} turns</span>
                </div>
                <textarea
                  className="transcript-textarea"
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Enter [00:00] Speaker: Text transcript lines..."
                  rows={14}
                />
              </div>

              {/* Action Button */}
              <div className="action-row">
                <div className="active-summary">
                  <span>Evaluating against <strong>{activeItems.length} active criteria</strong> for {selectedTenant}</span>
                </div>
                <button
                  className="btn btn-primary btn-large"
                  onClick={handleEvaluate}
                  disabled={evaluating || !transcript.trim()}
                >
                  {evaluating ? 'Evaluating via LLM & Rules...' : '🚀 Send to /api/evaluate'}
                </button>
              </div>

              {evalError && <div className="error-alert">{evalError}</div>}
            </div>

            {/* Result Panel */}
            <div className="eval-result-panel">
              <div className="panel-header">
                <h2>Evaluation Scorecard</h2>
                {evaluationResult && (
                  <span className="call-id-tag">ID: {evaluationResult.call_id}</span>
                )}
              </div>

              {!evaluationResult && !evaluating && (
                <div className="empty-state">
                  <div className="empty-icon">📊</div>
                  <h3>No Evaluation Ran Yet</h3>
                  <p>Click "Send to /api/evaluate" to score this interaction against active criteria in PostgreSQL.</p>
                </div>
              )}

              {evaluating && (
                <div className="evaluating-state">
                  <div className="spinner"></div>
                  <h3>Evaluating Interaction...</h3>
                  <p>Running deterministic rule engine and LLM verification models.</p>
                </div>
              )}

              {evaluationResult && evaluationResult.result && (
                <div className="scorecard-container">
                  {/* Score Hero */}
                  <div className={`score-hero ${evaluationResult.result.is_auto_fail ? 'auto-fail' : ''}`}>
                    <div className="score-value">
                      {evaluationResult.result.final_score !== undefined
                        ? `${evaluationResult.result.final_score}%`
                        : 'N/A'}
                    </div>
                    <div className="score-meta">
                      <div className="score-title">
                        {evaluationResult.result.is_auto_fail ? 'CRITICAL AUTO-FAIL' : 'FINAL AUDIT SCORE'}
                      </div>
                      <div className="score-subtitle">
                        {evaluationResult.result.is_auto_fail
                          ? evaluationResult.result.auto_fail_reason
                          : `Evaluated ${evaluationResult.result.scorecard?.length || 0} Criteria`}
                      </div>
                    </div>
                  </div>

                  {/* Criteria Breakdown Table */}
                  <div className="scorecard-table-wrapper">
                    <table className="scorecard-table">
                      <thead>
                        <tr>
                          <th>Criterion</th>
                          <th>Category</th>
                          <th>Verdict</th>
                          <th>Coaching & Details</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(evaluationResult.result.scorecard || []).map((row, idx) => (
                          <tr key={idx} className={row.rating === 'PASS' ? 'pass-row' : 'fail-row'}>
                            <td className="row-name">{row.name}</td>
                            <td className="row-cat">{row.category}</td>
                            <td>
                              <span className={`badge ${row.rating === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>
                                {row.rating}
                              </span>
                            </td>
                            <td className="row-coaching">{row.coaching}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </section>
        )}
      </main>

      {/* Modal: Add Tenant */}
      {showAddTenant && (
        <div className="modal-backdrop">
          <div className="modal-card">
            <h3>Add New Tenant</h3>
            <form onSubmit={handleCreateTenant}>
              <div className="form-group">
                <label>Tenant ID (e.g. tenant-xyz):</label>
                <input
                  type="text"
                  required
                  value={newTenantId}
                  onChange={(e) => setNewTenantId(e.target.value)}
                  className="input-control"
                />
              </div>
              <div className="form-group">
                <label>Tenant Display Name:</label>
                <input
                  type="text"
                  required
                  value={newTenantName}
                  onChange={(e) => setNewTenantName(e.target.value)}
                  className="input-control"
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddTenant(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Tenant
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Criterion */}
      {showAddCriterion && (
        <div className="modal-backdrop">
          <div className="modal-card">
            <h3>Add New Criterion</h3>
            <form onSubmit={handleCreateCriterion}>
              <div className="form-group">
                <label>Category:</label>
                <select
                  value={critCategoryId}
                  onChange={(e) => setCritCategoryId(e.target.value)}
                  className="input-control"
                >
                  {criteriaData.categories.map(c => (
                    <option key={c.category_id} value={c.category_id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Criterion Name:</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Tone of Voice"
                  value={critName}
                  onChange={(e) => setCritName(e.target.value)}
                  className="input-control"
                />
              </div>
              <div className="form-group">
                <label>Deduction Value (points):</label>
                <input
                  type="number"
                  required
                  min="5"
                  max="100"
                  value={critDeduction}
                  onChange={(e) => setCritDeduction(e.target.value)}
                  className="input-control"
                />
              </div>
              <div className="form-group">
                <label>Description / Verification Instructions:</label>
                <textarea
                  rows={3}
                  value={critDescription}
                  onChange={(e) => setCritDescription(e.target.value)}
                  placeholder="Describe evaluation logic..."
                  className="input-control"
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddCriterion(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save Criterion
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
