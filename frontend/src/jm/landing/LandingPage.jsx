import { useRef } from 'react';
import LandingMarkup from './LandingMarkup';
import usePauseOffscreen from '../shared/usePauseOffscreen';
import '../shared/jm-base.css';

export default function LandingPage() {
  const ref = useRef(null);
  usePauseOffscreen(ref);
  return <div ref={ref}><LandingMarkup /></div>;
}
