from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['EvidenSecure_db']  # Replace 'evidensecure' with your database name

# Define collections (e.g., cases, evidence, etc.)
cases_collection = db['Cases']
evidence_collection = db['Evidence']
users_collection = db['Users']


