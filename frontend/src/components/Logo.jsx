
/** The mark is a line of text with a highlighter stroke across it. */
const Logo = ({ className = '', markOnly = false }) => (
  <span className={`inline-flex items-center gap-2.5 ${className}`}>
    <svg viewBox="0 0 32 32" className="h-7 w-7 shrink-0" aria-hidden="true">
      <rect width="32" height="32" rx="7" fill="#14172B" />
      <path d="M7.5 11.5h12.5" stroke="#F3F4F7" strokeWidth="2.4" strokeLinecap="round" opacity=".55" />
      <path d="M8.4 14.6 24.6 13.4 23.6 21.4 7.4 22.6Z" fill="#FFE04A" />
    </svg>
    {!markOnly && (
      <span className="font-display text-[1.1875rem] font-bold tracking-tight text-ink" style={{ fontVariationSettings: '"wdth" 90' }}>
        JobMatcher
      </span>
    )}
  </span>
);

export default Logo;
