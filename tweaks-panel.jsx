/* tweaks-panel.jsx — do not edit */
function TweaksPanel({ children }) {
  const [open, setOpen] = React.useState(false);
  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          background: 'var(--ink)', color: 'var(--bg)',
          border: 'none', cursor: 'pointer',
          padding: '10px 16px', fontSize: '11px',
          letterSpacing: '.1em', textTransform: 'uppercase',
          fontFamily: "'Jost', sans-serif", fontWeight: 500,
          borderRadius: 0,
        }}
        aria-label="Toggle tweaks panel"
      >
        ❊ Tweaks
      </button>
      {open && (
        <div style={{
          position: 'absolute', bottom: '110%', right: 0,
          background: 'var(--bg)', border: '1px solid var(--rule)',
          padding: '1.5rem', minWidth: 240,
          boxShadow: '0 8px 32px rgba(0,0,0,.15)',
        }}>
          {children}
        </div>
      )}
    </div>
  );
}
