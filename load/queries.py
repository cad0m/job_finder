# SQL Queries

UPSERT_SOURCE = """
    INSERT INTO job_source (name) VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
"""

UPSERT_COMPANY = """
    INSERT INTO company (name, logo_url, website) VALUES (%s, %s, %s)
    ON CONFLICT (name) DO UPDATE
    SET logo_url = EXCLUDED.logo_url, website = EXCLUDED.website;
"""

UPSERT_LOCATION = """
    INSERT INTO location (city) VALUES (%s)
    ON CONFLICT (city) DO NOTHING;
"""

UPSERT_FUNCTION = """
    INSERT INTO job_function (name) VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
"""

UPSERT_INDUSTRY = """
    INSERT INTO industry (name) VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
"""

UPSERT_JOB = """
    INSERT INTO jobs (
        source_id, external_id, company_id, location_id, function_id,
        title, job_description, job_url, posted_date, scraped_at,
        salary, num_application, seniority_level
    )
    VALUES (
        (SELECT id FROM job_source WHERE name = %s),
        %s,
        (SELECT id FROM company WHERE name = %s),
        (SELECT id FROM location WHERE city = %s),
        (SELECT id FROM job_function WHERE name = %s),
        %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (source_id, external_id) DO UPDATE
    SET company_id = EXCLUDED.company_id,
        location_id = EXCLUDED.location_id,
        function_id = EXCLUDED.function_id,
        title = EXCLUDED.title,
        job_description = EXCLUDED.job_description,
        job_url = EXCLUDED.job_url,
        posted_date = EXCLUDED.posted_date,
        scraped_at = EXCLUDED.scraped_at,
        salary = EXCLUDED.salary,
        num_application = EXCLUDED.num_application,
        seniority_level = EXCLUDED.seniority_level;
"""

# CRITICAL FIX: Uses composite key (source + external_id) to avoid linking wrong jobs
INSERT_JOB_INDUSTRY = """
    INSERT INTO job_industry (job_id, industry_id)
    SELECT j.id, i.id
    FROM jobs j
    JOIN job_source s ON j.source_id = s.id
    JOIN industry i ON i.name = %s
    WHERE s.name = %s AND j.external_id = %s
    ON CONFLICT DO NOTHING;
"""