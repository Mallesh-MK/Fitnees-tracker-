from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://mallekuruga1888:5zGtwXVwk8g52qkG@cluster0.nxgsb3q.mongodb.net/?retryWrites=true&w=majority&tls=true"

client = MongoClient(CONNECTION_STRING)

def get_database():
    return client["fitness_tracker_db"]

db = get_database()

if __name__ == "__main__":
    try:
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Could not connect to MongoDB: {e}")
