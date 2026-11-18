import { supabase } from '../../lib/supabaseClient';
import { refreshFileLinks } from '../../services/supabaseDB';

/* Data for the dashboard: matches, saved offers and the applications tracker. */

export const TODAY = () => new Date().toISOString().slice(0, 10);
export const STATUSES = ['Saved', 'Applied', 'Recruiter screen', 'Hiring manager', 'Final loop', 'Offer', 'Rejected', 'Withdrawn', 'No response'];
export const INT = ['Recruiter screen', 'Hiring manager', 'Final loop'];
export const SOURCES = ['LinkedIn', 'ANAPEC', 'Jobzyn', 'Job board', 'Company site', 'Referral', 'Other'];

export const initials = (name = '') => {
  const w = String(name).replace(/[^\p{L}\p{N} ]/gu, ' ').trim().split(/\s+/).filter(Boolean);
  if (!w.length) return '?';
  return (w[0][0] + (w[1] ? w[1][0] : (w[0][1] || ''))).toUpperCase();
};
export const logoClass = (name = '') => `l${1 + ([...String(name)].reduce((a, c) => a + c.charCodeAt(0), 0) % 4)}`;

export const jobType = (title = '') => {
  if (/\b(stage|stagiaire|intern(ship)?|pfe|alternance|apprenti)/i.test(title)) return 'Internship';
  if (/\b(cdd|freelance|contract|mission|temporaire|int[ée]rim)/i.test(title)) return 'Contract';
  return 'Full-time';
};
export const levelName = (s) => {
  const v = String(s || '').toLowerCase();
  if (!v) return '';
  if (v.startsWith('jun')) return 'Junior';
  if (v.startsWith('mid') || v.includes('conf')) return 'Mid';
  if (v.startsWith('sen')) return 'Senior';
  if (v.startsWith('lead') || v.startsWith('exec')) return 'Lead';
  if (v.startsWith('int') || v.includes('stag')) return 'Intern';
  return s;
};

export const ago = (d) => {
  if (!d) return '';
  const days = Math.floor((Date.now() - new Date(d).getTime()) / 864e5);
  if (days <= 0) return 'Today';
  if (days === 1) return '1 day ago';
  if (days < 7) return `${days} days ago`;
  if (days < 14) return '1 week ago';
  if (days < 60) return `${Math.floor(days / 7)} weeks ago`;
  return new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
};

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export const skillsIn = (skills, text) => {
  const t = ` ${String(text || '').toLowerCase()} `;
  return skills.filter((s) => new RegExp(`(^|[^a-z0-9+#])${esc(s.toLowerCase())}([^a-z0-9+#]|$)`).test(t));
};
const asNames = (xs) => (Array.isArray(xs) ? xs : []).map((x) => (typeof x === 'string' ? x : x?.name)).filter(Boolean);

/** The signed-in user's CV row (skills, level, city) or null. */
export async function loadCandidate(userId) {
  const { data } = await supabase.from('candidates').select('id, full_name, skills, seniority_level, location').eq('user_id', userId).maybeSingle();
  return data ? { ...data, skills: asNames(data.skills) } : null;
}

/** Matches for the user, enriched with source, description skills and type. */
export async function loadMatches(userId, candidate, count = 150) {
  const { data, error } = await supabase.rpc('match_jobs_for_user', { p_user_id: userId, p_match_count: count, p_min_score: 0 });
  if (error) throw error;
  const rows = data || [];
  if (!rows.length) return [];
  const { data: extra } = await supabase
    .from('jobs')
    .select('id, job_description, job_url, source:source_id ( name ), function:function_id ( name )')
    .in('id', rows.map((r) => r.id));
  const byId = Object.fromEntries((extra || []).map((e) => [e.id, e]));
  const skills = candidate?.skills || [];
  return rows.map((r) => {
    const e = byId[r.id] || {};
    const hits = skillsIn(skills, `${r.title} ${e.job_description || ''}`);
    return {
      id: r.id,
      title: r.title,
      company: r.company || 'Company',
      city: (r.location || '').split(',')[0].trim(),
      location: r.location || '',
      source: e.source?.name || '',
      url: r.job_url || e.job_url || '',
      level: levelName(r.seniority_level),
      type: jobType(r.title),
      posted: r.posted_date,
      salary: r.salary,
      score: Math.round((r.match_score || 0) * 100),
      hits,
      description: e.job_description || '',
      fn: e.function?.name || '',
    };
  });
}

/** One job, for the drawer when it is not in the matches (e.g. saved earlier). */
export async function loadJob(id, candidate) {
  const { data } = await supabase
    .from('jobs')
    .select('id, title, job_description, job_url, posted_date, salary, seniority_level, company:company_id ( name ), location:location_id ( city, country ), source:source_id ( name )')
    .eq('id', id)
    .maybeSingle();
  if (!data) return null;
  return {
    id: data.id, title: data.title, company: data.company?.name || 'Company', city: data.location?.city || '',
    location: [data.location?.city, data.location?.country].filter(Boolean).join(', '), source: data.source?.name || '',
    url: data.job_url || '', level: levelName(data.seniority_level), type: jobType(data.title), posted: data.posted_date,
    salary: data.salary, score: null, hits: skillsIn(candidate?.skills || [], `${data.title} ${data.job_description || ''}`),
    description: data.job_description || '',
  };
}

export async function loadSaved(userId) {
  const { data } = await supabase
    .from('user_job_interactions')
    .select('job_id, created_at, match_score, job:jobs ( id, title, job_url, posted_date, company:company_id ( name ), location:location_id ( city ), source:source_id ( name ) )')
    .eq('user_id', userId)
    .eq('action', 'saved')
    .order('created_at', { ascending: false });
  return (data || []).filter((r) => r.job).map((r) => ({
    id: r.job.id, title: r.job.title, company: r.job.company?.name || 'Company', city: r.job.location?.city || '',
    source: r.job.source?.name || '', url: r.job.job_url || '', savedAt: r.created_at,
    score: r.match_score != null ? Math.round(r.match_score * 100) : null, posted: r.job.posted_date,
  }));
}

/** Save or unsave an offer. The table keeps one row per (user, job). */
export async function setSaved(userId, job, saved) {
  if (saved) {
    const { error } = await supabase.from('user_job_interactions').upsert(
      { user_id: userId, job_id: job.id, action: 'saved', positive_signal: true, match_score: job.score != null ? job.score / 100 : null },
      { onConflict: 'user_id,job_id' },
    );
    if (error) throw error;
  } else {
    const { error } = await supabase.from('user_job_interactions').delete().eq('user_id', userId).eq('job_id', job.id).eq('action', 'saved');
    if (error) throw error;
  }
}

/* ── Applications tracker ─────────────────────────────────────────────────── */

const appSelect = `id, job_id, status, track_status, company, role, city, job_link, source, date_applied, first_interview, last_activity,
  next_step, next_step_date, contact, pay_range, notes, sent_kind, own_subject, own_body, own_file_path,
  cv_url, cover_letter_url, email_url, data_email, created_at,
  job:jobs ( id, title, job_url, company:company_id ( name ), location:location_id ( city ), source:source_id ( name ) )`;

const toRow = (a) => ({
  key: `a${a.id}`,
  appId: a.id,
  jobId: a.job_id,
  co: a.company || a.job?.company?.name || 'Company',
  role: a.role || a.job?.title || '',
  city: a.city || a.job?.location?.city || '',
  link: a.job_link || a.job?.job_url || '',
  src: a.source || a.job?.source?.name || '',
  st: a.track_status || 'Applied',
  ap: a.date_applied || '',
  fi: a.first_interview || '',
  last: a.last_activity || a.date_applied || '',
  next: a.next_step || '',
  nextd: a.next_step_date || '',
  contact: a.contact || '',
  pay: a.pay_range || '',
  notes: a.notes || '',
  sent: a.status === 'pending' || a.status === 'generating' ? 'writing' : a.sent_kind || null,
  gen: { cv: a.cv_url, cover_letter: a.cover_letter_url, email: a.email_url, data_email: a.data_email },
  own: { subject: a.own_subject || '', body: a.own_body || '', file: a.own_file_path || '' },
});

/** Applications plus saved offers that were not applied to yet (as "Saved" rows). */
export async function loadTracker(userId) {
  const [{ data: apps, error }, saved] = await Promise.all([
    supabase.from('job_applications').select(appSelect).eq('user_id', userId).order('created_at', { ascending: false }),
    loadSaved(userId),
  ]);
  if (error) throw error;
  const withLinks = await refreshFileLinks(apps || []);
  const rows = withLinks.map(toRow);
  const appliedJobs = new Set(rows.map((r) => r.jobId).filter(Boolean));
  saved.filter((s) => !appliedJobs.has(s.id)).forEach((s) => rows.push({
    key: `s${s.id}`, appId: null, jobId: s.id, co: s.company, role: s.title, city: s.city, link: s.url, src: s.source,
    st: 'Saved', ap: '', fi: '', last: '', next: '', nextd: '', contact: '', pay: '', notes: '', sent: null, gen: {}, own: {},
  }));
  return rows;
}

const toDb = (r, userId) => ({
  user_id: userId,
  job_id: r.jobId || null,
  company: r.co || null,
  role: r.role || null,
  city: r.city || null,
  job_link: r.link || null,
  source: r.src || null,
  track_status: r.st,
  date_applied: r.ap || null,
  first_interview: r.fi || null,
  last_activity: r.last || null,
  next_step: r.next || null,
  next_step_date: r.nextd || null,
  contact: r.contact || null,
  pay_range: r.pay || null,
  notes: r.notes || null,
  sent_kind: r.sent === 'writing' ? 'gen' : r.sent || null,
  own_subject: r.own?.subject || null,
  own_body: r.own?.body || null,
  own_file_path: r.own?.file || null,
});

/** Insert or update a tracker row. A "Saved" offer becomes an application the first time it changes. */
export async function saveRow(userId, r) {
  const body = toDb(r, userId);
  if (r.appId) {
    const { data, error } = await supabase.from('job_applications').update({ ...body, updated_at: new Date().toISOString() }).eq('id', r.appId).select(appSelect).single();
    if (error) throw error;
    return toRow((await refreshFileLinks([data]))[0]);
  }
  const { data, error } = await supabase.from('job_applications').insert({ ...body, status: 'ready' }).select(appSelect).single();
  if (error) throw error;
  return toRow(data);
}

export async function deleteRow(r) {
  if (!r.appId) return;
  const { error } = await supabase.from('job_applications').delete().eq('id', r.appId);
  if (error) throw error;
}

/** Upload the file the user sent by themselves; returns its storage path. */
export async function uploadOwnFile(userId, file) {
  const safe = file.name.replace(/[^a-zA-Z0-9._-]/g, '_').slice(0, 120);
  const path = `${userId}/own/${Date.now()}-${safe}`;
  const { error } = await supabase.storage.from('generated-cvs').upload(path, file, { contentType: file.type || 'application/octet-stream' });
  if (error) throw error;
  return path;
}
export async function fileUrl(path) {
  if (!path) return null;
  const { data } = await supabase.storage.from('generated-cvs').createSignedUrl(path, 3600);
  return data?.signedUrl || null;
}
