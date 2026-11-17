import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Activity, ArrowDownToLine, ArrowRight, Blocks, BookOpen, BriefcaseBusiness, Check, ChevronDown, ChevronRight, Code2, Command, Compass, Copy, Database, FileText, Filter, GraduationCap, HeartPulse, Layers3, LoaderCircle, Menu, Search, ShieldCheck, Sparkles, Terminal, WandSparkles, X, Zap } from 'lucide-react'
import './styles.css'

const API = import.meta.env.VITE_API_URL || ''
const icons = { productivity: Zap, writing: FileText, learning: GraduationCap, data: Database, business: BriefcaseBusiness, coding: Code2, research: BookOpen, career: Compass, creative: WandSparkles, operations: Layers3 }
const labels = { productivity: 'Productivity', writing: 'Writing & Communication', learning: 'Learning & Education', data: 'Data & Analytics', business: 'Business', coding: 'Software & Development', research: 'Research', career: 'Career & Work', creative: 'Creative Studio', operations: 'Operations' }

function App() {
  const [tools, setTools] = useState([])
  const [categories, setCategories] = useState([])
  const [overview, setOverview] = useState(null)
  const [query, setQuery] = useState('')
  const [activeCategory, setActiveCategory] = useState('all')
  const [selected, setSelected] = useState(null)
  const [payload, setPayload] = useState('{}')
  const [result, setResult] = useState(null)
  const [running, setRunning] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)
  const [mobileMenu, setMobileMenu] = useState(false)

  useEffect(() => {
    Promise.all([fetch(`${API}/api/tools?limit=250`).then(r => { if (!r.ok) throw new Error('Could not load tools'); return r.json() }), fetch(`${API}/api/categories`).then(r => r.json()), fetch(`${API}/api/overview`).then(r => r.json())])
      .then(([toolData, categoryData, overviewData]) => { setTools(toolData.items); setCategories(categoryData); setOverview(overviewData); setError('') })
      .catch(() => setError('Marketplace API is not reachable. Start the backend and refresh this page.'))
      .finally(() => setLoading(false))
  }, [])

  const filtered = useMemo(() => tools.filter(tool => (activeCategory === 'all' || tool.category === activeCategory) && `${tool.title} ${tool.description} ${tool.tool_name} ${tool.category}`.toLowerCase().includes(query.toLowerCase())), [tools, activeCategory, query])

  const openTool = tool => { setSelected(tool); setPayload('{}'); setResult(null); setMobileMenu(false) }
  const execute = async () => {
    let parsed
    try { parsed = JSON.parse(payload) } catch { setResult({ error: 'Payload must be valid JSON.' }); return }
    if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') { setResult({ error: 'Payload must be a JSON object.' }); return }
    setRunning(true)
    setResult(null)
    try {
      const response = await fetch(`${API}/api/tools/${selected.tool_name}/execute`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ payload: parsed }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Execution failed')
      setResult(data)
    } catch (err) { setResult({ error: err.message }) }
    finally { setRunning(false) }
  }
  const copyText = async text => { await navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 1500) }
  const selectedCategory = selected ? labels[selected.category] || selected.category : ''

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#top" onClick={() => { setSelected(null); setActiveCategory('all') }}><span className="brand-mark"><Blocks size={21}/></span><span>agent<span className="brand-accent">forge</span></span><span className="version-pill">MARKETPLACE</span></a>
      <nav className="top-links"><a href="#explore">Explore tools</a><a href="#how-it-works">How it works</a><a href="https://github.com" target="_blank" rel="noreferrer">GitHub <ArrowRight size={13}/></a></nav>
      <button className="mobile-menu-button" onClick={() => setMobileMenu(!mobileMenu)} aria-label="Toggle menu"><Menu size={20}/></button>
      {mobileMenu && <div className="mobile-menu"><a href="#explore" onClick={() => setMobileMenu(false)}>Explore tools</a><a href="#how-it-works" onClick={() => setMobileMenu(false)}>How it works</a></div>}
    </header>

    <main id="top">
      <section className="hero">
        <div className="hero-grid"></div>
        <div className="hero-content">
          <div className="eyebrow"><span className="pulse-dot"></span> OPEN TOOL ECOSYSTEM <span className="eyebrow-line"></span> VERSION 1.1</div>
          <h1>One ecosystem.<br/><span>Infinite capabilities.</span></h1>
          <p className="hero-copy">Practical tools for AI agents and people across every profession. Discover a capability, run it locally, or connect it to your workflow.</p>
          <div className="hero-actions"><a className="primary-button" href="#explore">Explore the marketplace <ArrowRight size={16}/></a><a className="secondary-button" href="#how-it-works">How it works <ChevronDown size={15}/></a></div>
          <div className="hero-stats"><div><strong>{overview?.tool_count ?? '100'}</strong><span>TOOLS</span></div><i></i><div><strong>{overview?.category_count ?? '10'}</strong><span>DOMAINS</span></div><i></i><div><strong>Open</strong><span>ECOSYSTEM</span></div></div>
        </div>
        <div className="hero-art" aria-hidden="true"><div className="orbit orbit-one"></div><div className="orbit orbit-two"></div><div className="orbit orbit-three"></div><div className="core-glow"></div><div className="core-logo"><Blocks size={52}/></div><div className="orbit-node node-a"><Code2 size={18}/></div><div className="orbit-node node-b"><Database size={18}/></div><div className="orbit-node node-c"><Sparkles size={18}/></div><div className="orbit-node node-d"><ShieldCheck size={18}/></div><div className="art-label label-a">MCP READY</div><div className="art-label label-b">100 CAPABILITIES</div></div>
      </section>

      <section className="trust-strip"><div><Activity size={15}/> LOCAL-FIRST UTILITIES</div><span></span><div><ShieldCheck size={15}/> OPEN SOURCE</div><span></span><div><Terminal size={15}/> MCP + CLI + SKILLS</div><span></span><div><HeartPulse size={15}/> BUILT FOR EVERY FIELD</div></section>

      <section className="marketplace-section" id="explore">
        <div className="section-heading"><div><div className="eyebrow">THE TOOL LIBRARY</div><h2>Find your next capability.</h2><p>From classrooms to boardrooms, research labs to creative studios.</p></div><div className="catalog-count"><span>{filtered.length.toString().padStart(3, '0')}</span><small>TOOLS FOUND</small></div></div>
        <div className="market-layout">
          <aside className={`sidebar ${mobileMenu ? 'sidebar-open' : ''}`}><div className="sidebar-title">BROWSE DOMAINS <Filter size={14}/></div><button className={`category-button ${activeCategory === 'all' ? 'active' : ''}`} onClick={() => setActiveCategory('all')}><span className="category-icon"><Blocks size={16}/></span><span>All tools</span><b>{tools.length}</b></button>{categories.map(category => { const Icon = icons[category.name] || Blocks; return <button key={category.name} className={`category-button ${activeCategory === category.name ? 'active' : ''}`} onClick={() => setActiveCategory(category.name)}><span className="category-icon"><Icon size={16}/></span><span>{labels[category.name] || category.name}</span><b>{category.count}</b></button> })}<div className="sidebar-note"><Sparkles size={16}/><strong>Built for everyone</strong><p>Every tool is designed around a focused task, not a specific job title.</p></div></aside>
          <div className="catalog-area">
            <div className="search-row"><div className="search-box"><Search size={18}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search tools, tasks, or professions..."/><kbd>⌘ K</kbd></div><div className="sort-label"><span className="online-dot"></span> ALL CAPABILITIES</div></div>
            {error && <div className="error-banner"><Activity size={17}/>{error}</div>}
            {loading ? <div className="loading-state"><LoaderCircle className="spin" size={25}/> Loading AgentForge tools...</div> : filtered.length === 0 ? <div className="empty-state"><Search size={25}/><h3>No tools found</h3><p>Try another keyword or select a different domain.</p><button onClick={() => { setQuery(''); setActiveCategory('all') }}>Clear filters</button></div> : <div className="tool-grid">{filtered.map(tool => { const Icon = icons[tool.category] || Blocks; return <button className="tool-card" key={tool.tool_name} onClick={() => openTool(tool)}><div className="tool-card-top"><span className="tool-icon"><Icon size={19}/></span><span className="tool-arrow"><ArrowUpRightIcon/></span></div><span className="tool-category">{labels[tool.category] || tool.category}</span><h3>{tool.title}</h3><p>{tool.description}</p><div className="tool-card-bottom"><span>VIEW TOOL <ArrowRight size={13}/></span><span className="tool-code">{tool.tool_name}</span></div></button> })}</div>}
          </div>
        </div>
      </section>

      <section className="how-section" id="how-it-works"><div className="eyebrow">SIMPLE BY DESIGN</div><h2>From discovery to doing.</h2><p className="how-intro">Use a tool directly in the marketplace or connect its capability to your own AI workflow.</p><div className="steps-grid"><div className="step-card"><span>01</span><div className="step-icon"><Search size={21}/></div><h3>Discover</h3><p>Search 100 focused tools across ten professional domains.</p></div><div className="step-card"><span>02</span><div className="step-icon"><Zap size={21}/></div><h3>Run</h3><p>Provide structured input and execute supported utilities through the API.</p></div><div className="step-card"><span>03</span><div className="step-icon"><Command size={21}/></div><h3>Integrate</h3><p>Connect tools to compatible agents through MCP, CLI and Agent Skills.</p></div></div></section>
    </main>

    <footer className="footer"><a className="brand" href="#top"><span className="brand-mark"><Blocks size={18}/></span><span>agent<span className="brand-accent">forge</span></span></a><span>Open capabilities for a more useful AI ecosystem.</span><div><a href="https://github.com" target="_blank" rel="noreferrer">GitHub</a><a href="#explore">Explore</a></div></footer>

    {selected && <div className="modal-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) setSelected(null) }}><section className="tool-modal"><div className="modal-header"><div><span className="tool-category">{selectedCategory}</span><h2>{selected.title}</h2></div><button className="icon-button" onClick={() => setSelected(null)} aria-label="Close"><X size={19}/></button></div><p className="modal-description">{selected.description}</p><div className="tool-meta"><span><span className="online-dot"></span> LOCAL TOOL EXECUTION</span><span>MCP COMPATIBLE</span></div><div className="modal-label"><label htmlFor="payload">INPUT PAYLOAD</label><button onClick={() => setPayload('{}')}><X size={12}/> RESET</button></div><textarea id="payload" className="payload-editor" value={payload} onChange={e => setPayload(e.target.value)} spellCheck="false" aria-label="JSON input payload"/><div className="payload-hint">Provide a JSON object matching this tool's expected inputs. See its Agent Skill for usage guidance.</div><button className="run-button" onClick={execute} disabled={running}><span>{running ? <LoaderCircle className="spin" size={16}/> : <Zap size={16}/>}</span>{running ? 'Running tool...' : 'Run this tool'}<ArrowRight size={16}/></button>{result && <div className="result-panel"><div className="result-heading"><span>EXECUTION RESULT</span><button onClick={() => copyText(JSON.stringify(result, null, 2))}>{copied ? <Check size={14}/> : <Copy size={14}/>} {copied ? 'COPIED' : 'COPY JSON'}</button></div><pre>{JSON.stringify(result, null, 2)}</pre></div>}<div className="modal-footer"><span><ShieldCheck size={14}/> Input is processed by your local AgentForge backend.</span><span className="tool-code">{selected.tool_name}</span></div></section></div>}
  </div>
}

function ArrowUpRightIcon() { return <ArrowRight size={15}/> }

createRoot(document.getElementById('root')).render(<React.StrictMode><App/></React.StrictMode>)
