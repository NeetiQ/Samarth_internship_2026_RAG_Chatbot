from retrieval.vectordb.connection import DatabaseConnection


def main():
    try:
        conn = DatabaseConnection.connect()
        print("✅ Database connected successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    main()