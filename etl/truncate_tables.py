from etl.core.databaseConnection import DatabaseConnection


def main() -> None:
    db = DatabaseConnection()
    db.connect()
    try:
        print("=== TRUNCATING JOB-RELATED TABLES ===")
        # Truncate all related tables in a single statement with CASCADE to
        # satisfy foreign key constraints between them.
        db.execute(
            "TRUNCATE TABLE job_industry, jobs, job_function, industry, "
            "location, company, job_source RESTART IDENTITY CASCADE;"
        )
        db.commit()
        print("✓ Truncate completed.")
    except Exception as e:
        print("❌ Error while truncating tables:", e)
        raise
    finally:
        db.close()
        print("✓ Database connection closed.")


if __name__ == "__main__":
    main()

