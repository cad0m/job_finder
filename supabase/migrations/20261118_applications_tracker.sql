-- Applied tracker: the columns of the Google Sheet, on job_applications.
-- `status` stays the document-generation status (pending/generating/ready/failed).
-- Run it once in Supabase: Dashboard → SQL Editor → paste → Run.
ALTER TABLE public.job_applications
  ALTER COLUMN job_id DROP NOT NULL,          -- applications added by hand, for offers found elsewhere
  ALTER COLUMN candidate_id DROP NOT NULL,
  ADD COLUMN IF NOT EXISTS company         text,
  ADD COLUMN IF NOT EXISTS role            text,
  ADD COLUMN IF NOT EXISTS city            text,
  ADD COLUMN IF NOT EXISTS job_link        text,
  ADD COLUMN IF NOT EXISTS source          text,
  ADD COLUMN IF NOT EXISTS track_status    text NOT NULL DEFAULT 'Applied',
  ADD COLUMN IF NOT EXISTS date_applied    date,
  ADD COLUMN IF NOT EXISTS first_interview date,
  ADD COLUMN IF NOT EXISTS last_activity   date,
  ADD COLUMN IF NOT EXISTS next_step       text,
  ADD COLUMN IF NOT EXISTS next_step_date  date,
  ADD COLUMN IF NOT EXISTS contact         text,
  ADD COLUMN IF NOT EXISTS pay_range       text,
  ADD COLUMN IF NOT EXISTS notes           text,
  ADD COLUMN IF NOT EXISTS sent_kind       text,          -- 'gen' (made with JobMatcher) or 'own'
  ADD COLUMN IF NOT EXISTS own_subject     text,
  ADD COLUMN IF NOT EXISTS own_body        text,
  ADD COLUMN IF NOT EXISTS own_file_path   text;

ALTER TABLE public.job_applications
  ADD CONSTRAINT ja_track_status_check CHECK (track_status IN ('Saved','Applied','Recruiter screen','Hiring manager','Final loop','Offer','Rejected','Withdrawn','No response')),
  ADD CONSTRAINT ja_sent_kind_check CHECK (sent_kind IS NULL OR sent_kind IN ('gen','own')),
  ADD CONSTRAINT ja_job_or_company CHECK (job_id IS NOT NULL OR company IS NOT NULL);

-- Existing applications were all made with JobMatcher
UPDATE public.job_applications
SET date_applied  = COALESCE(date_applied, created_at::date),
    last_activity = COALESCE(last_activity, updated_at::date),
    sent_kind     = COALESCE(sent_kind, CASE WHEN status = 'ready' THEN 'gen' END);

-- Users can delete their own tracker rows
CREATE POLICY "ja: user deletes own rows" ON public.job_applications
  FOR DELETE TO authenticated USING ((SELECT auth.uid()) = user_id);

-- Files a user attaches as "what I sent": their own folder in generated-cvs
CREATE POLICY "Users upload own sent files" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (bucket_id = 'generated-cvs' AND (SELECT auth.uid())::text = (storage.foldername(name))[1]);
CREATE POLICY "Users update own sent files" ON storage.objects
  FOR UPDATE TO authenticated
  USING (bucket_id = 'generated-cvs' AND (SELECT auth.uid())::text = (storage.foldername(name))[1]);
