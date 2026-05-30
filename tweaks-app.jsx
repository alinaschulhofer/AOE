/* tweaks-app.jsx — theme & accent controls */
function TweaksApp() {
  const saved = key => (typeof localStorage !== 'undefined' ? localStorage.getItem(key) : null);

  const [direction, setDirection] = React.useState(saved('aoe-direction') || 'ivory');
  const [accent, setAccent] = React.useState(saved('aoe-accent') || '#A8824E');
  const [motion, setMotion] = React.useState(saved('aoe-motion') !== 'off');

  React.useEffect(() => {
    document.documentElement.setAttribute('data-theme', direction);
    localStorage.setItem('aoe-direction', direction);
  }, [direction]);

  React.useEffect(() => {
    document.documentElement.style.setProperty('--accent', accent);
    localStorage.setItem('aoe-accent', accent);
  }, [accent]);

  React.useEffect(() => {
    localStorage.setItem('aoe-motion', motion ? 'on' : 'off');
    if (!motion) {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    }
  }, [motion]);

  const label = {
    fontSize: '10px', letterSpacing: '.12em', textTransform: 'uppercase',
    color: 'var(--ink2)', fontFamily: "'Jost', sans-serif", fontWeight: 500,
    display: 'block', marginBottom: '6px',
  };
  const row = { marginBottom: '1.25rem' };

  return (
    <TweaksPanel>
      <div style={row}>
        <span style={label}>Direction</span>
        {['ivory', 'luxe'].map(d => (
          <label key={d} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, cursor: 'pointer', fontSize: 13, fontFamily: "'Jost', sans-serif", color: 'var(--ink)' }}>
            <input type="radio" name="dir" value={d} checked={direction === d} onChange={() => setDirection(d)} />
            {d === 'ivory' ? 'Editorial Ivory' : 'Midnight Luxe'}
          </label>
        ))}
      </div>
      <div style={row}>
        <span style={label}>Accent</span>
        <input type="color" value={accent} onChange={e => setAccent(e.target.value)}
          style={{ width: '100%', height: 32, border: '1px solid var(--rule)', cursor: 'pointer', background: 'none', padding: 0 }} />
      </div>
      <div style={row}>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 13, fontFamily: "'Jost', sans-serif", color: 'var(--ink)' }}>
          <input type="checkbox" checked={motion} onChange={e => setMotion(e.target.checked)} />
          Animations
        </label>
      </div>
    </TweaksPanel>
  );
}

const tweaksRoot = document.getElementById('tweaks-root');
if (tweaksRoot) {
  ReactDOM.createRoot(tweaksRoot).render(React.createElement(TweaksApp));
}
