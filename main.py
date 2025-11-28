from normalizer import Transformer
from load import LoadingPipeline

def main():
    print("\n" + "=" * 60)
    print("JOB DATA LOADING")
    print("=" * 60)
    print()
    
    print("🔄 Transforming data...")
    transformer = Transformer("data/parsed")
    clean_data = transformer.normalize()
    print("✓ Transformation complete\n")
    
    print("📥 Loading into database...")
    pipeline = LoadingPipeline()
    stats = pipeline.run(clean_data)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for table, count in stats.items():
        print(f"  {table:20s}: {count:6d} rows")
    print("=" * 60)

if __name__ == "__main__":
    main()