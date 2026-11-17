
/**
 * Match score from 0 to 100, drawn on a highlighter stroke whose length is the
 * score. Pass null when the offer has no score (keyword search, saved list).
 */
const MatchScore = ({ score, size = 'md', className = '' }) => {
  const hasScore = typeof score === 'number' && !Number.isNaN(score);
  const sizeClass = size === 'lg' ? 'score-lg' : '';

  if (!hasScore) {
    return (
      <span className={`score score-none ${sizeClass} ${className}`} title="No match score for this offer">
        <span aria-hidden="true">–</span>
        <span className="sr-only">No match score</span>
      </span>
    );
  }

  const pct = Math.max(0, Math.min(100, Math.round(score)));
  return (
    <span className={`score ${sizeClass} ${className}`} style={{ '--pct': pct }}>
      {pct}
      <span className="score-unit">%</span>
      <span className="sr-only"> match</span>
    </span>
  );
};

export default MatchScore;
