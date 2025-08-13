
def chunk_size(df, chunk_size=20):
    for i in range(0, len(df), chunk_size):
        print(df.iloc[i:i + chunk_size])
        print("-" * 40)
