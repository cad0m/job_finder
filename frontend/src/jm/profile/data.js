import { supabase } from '../../lib/supabaseClient';

/* Profile data: user_profile, the CV row, preferences (link tables) and counts. */

export async function loadProfile(user) {
  let { data: prof } = await supabase.from('user_profile').select('*').eq('user_id', user.id).maybeSingle();
  if (!prof) {
    const { data } = await supabase.from('user_profile').insert({ user_id: user.id, full_name: user.user_metadata?.full_name || null }).select().single();
    prof = data;
  }
  const { data: cand } = await supabase.from('candidates').select('*').eq('user_id', user.id).maybeSingle();
  const pid = prof?.id;
  const [loc, ind, fn, apps, saved] = await Promise.all([
    pid ? supabase.from('user_desired_location').select('location_id, location:location_id ( city )').eq('user_profile_id', pid) : { data: [] },
    pid ? supabase.from('user_desired_industry').select('industry_id, industry:industry_id ( name )').eq('user_profile_id', pid) : { data: [] },
    pid ? supabase.from('user_preferred_function').select('function_id, job_function:function_id ( name )').eq('user_profile_id', pid) : { data: [] },
    supabase.from('job_applications').select('id', { count: 'exact', head: true }).eq('user_id', user.id).not('date_applied', 'is', null),
    supabase.from('user_job_interactions').select('id', { count: 'exact', head: true }).eq('user_id', user.id).eq('action', 'saved'),
  ]);
  return {
    prof,
    cand,
    cities: (loc.data || []).map((r) => ({ id: r.location_id, name: r.location?.city })).filter((x) => x.name),
    industries: (ind.data || []).map((r) => ({ id: r.industry_id, name: r.industry?.name })).filter((x) => x.name),
    roles: (fn.data || []).map((r) => ({ id: r.function_id, name: r.job_function?.name })).filter((x) => x.name),
    applied: apps.count || 0,
    saved: saved.count || 0,
  };
}

/** Suggestions for the preference chips: the names that exist in the offers. */
export async function loadSuggestions() {
  const [c, i, f] = await Promise.all([
    supabase.from('location').select('id, city').not('city', 'is', null).order('city').limit(400),
    supabase.from('industry').select('id, name').order('name').limit(400),
    supabase.from('job_function').select('id, name').order('name').limit(400),
  ]);
  const uniq = (rows, k) => [...new Map((rows || []).filter((r) => r[k]).map((r) => [r[k].trim().toLowerCase(), { id: r.id, name: r[k].trim() }])).values()];
  return { cities: uniq(c.data, 'city'), industries: uniq(i.data, 'name'), roles: uniq(f.data, 'name') };
}

const LINKS = {
  cities: ['user_desired_location', 'location_id'],
  industries: ['user_desired_industry', 'industry_id'],
  roles: ['user_preferred_function', 'function_id'],
};
export async function addPref(kind, profileId, id) {
  const [table, col] = LINKS[kind];
  const { error } = await supabase.from(table).insert({ user_profile_id: profileId, [col]: id });
  if (error && !/duplicate/i.test(error.message)) throw error;
}
export async function removePref(kind, profileId, id) {
  const [table, col] = LINKS[kind];
  const { error } = await supabase.from(table).delete().eq('user_profile_id', profileId).eq(col, id);
  if (error) throw error;
}

export async function saveProfileRow(profileId, patch) {
  const { error } = await supabase.from('user_profile').update({ ...patch, updated_at: new Date().toISOString() }).eq('id', profileId);
  if (error) throw error;
}
export async function saveCandidate(userId, patch) {
  const { error } = await supabase.from('candidates').update({ ...patch, updated_at: new Date().toISOString() }).eq('user_id', userId);
  if (error) throw error;
}

export async function uploadAvatar(userId, file) {
  const ext = (file.name.split('.').pop() || 'jpg').toLowerCase();
  const path = `${userId}/${userId}-${Date.now()}.${ext}`;
  const { error } = await supabase.storage.from('avatars').upload(path, file, { upsert: true, contentType: file.type });
  if (error) throw error;
  return supabase.storage.from('avatars').getPublicUrl(path).data.publicUrl;
}

export async function cvFileUrl(path) {
  if (!path) return null;
  const { data } = await supabase.storage.from('cvs').createSignedUrl(path, 3600);
  return data?.signedUrl || null;
}
