import { useEffect } from 'react';

/** Pause the looping CSS animations of sections that are off screen (saves battery on phones). */
export default function usePauseOffscreen(rootRef, selector = 'section, aside.host, .hero, .stage') {
  useEffect(() => {
    const root = rootRef.current;
    if (!root || !('IntersectionObserver' in window)) return undefined;
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.target.classList.toggle('zz', !e.isIntersecting)),
      { rootMargin: '120px' },
    );
    root.querySelectorAll(selector).forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [rootRef, selector]);
}
