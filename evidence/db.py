from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['EvidenSecure_db']  # Replace 'evidensecure' with your database name

# Define collections (e.g., cases, evidence, etc.)
cases_collection = db['Cases']
evidence_collection = db['Evidence']

def get_case_by_number(court_case_number):
    case = cases_collection.find_one({'court_case_number': court_case_number})
    return case

def get_evidence_by_case_id(case_id):
    evidence_list = list(evidence_collection.find({'case_id': case_id}))
    return evidence_list
