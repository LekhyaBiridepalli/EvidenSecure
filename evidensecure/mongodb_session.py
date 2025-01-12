from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
import pymongo
from django.utils import timezone
from bson import ObjectId
from datetime import datetime, timedelta


class MongoDBSession(SessionBase):
    def __init__(self, session_key=None):
        """Initialize the session by connecting to MongoDB."""
        self.client = pymongo.MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DATABASE]
        self.collection = self.db['sessions']

        # If session_key exists, use it; otherwise, generate a new one.
        if session_key:
            self.session_key = session_key
        else:
            self.session_key = self._get_new_session_key()

        self._session_cache = {}
        self.modified = False

        # Load the existing session if it exists
        self._load()
    
    @property
    def session_key(self):
        """Return the session key."""
        return self._session_key

    @session_key.setter
    def session_key(self, value):
        """Set the session key."""
        if not value:
            raise ValueError("Session key cannot be empty")
        self._session_key = value

    def _load(self):
        """Load session data from MongoDB."""
        session_data = self.collection.find_one({'session_key': self.session_key})
        if session_data:
            self._session_cache = session_data.get('data', {})
            self.modified = False
        else:
            self.create()  # Create a new session if none exists

    def create(self):
        """Create a new session if it does not exist."""
        if not self.collection.find_one({'session_key': self.session_key}):
            self._session_cache = {}  # Make sure the cache starts empty
            self.modified = True
            self.save()

    def save(self):
        """Save session data to MongoDB."""
        self.collection.replace_one(
            {'session_key': self.session_key},
            {
                'session_key': self.session_key,
                'data': self._session_cache,  # Store the session data here
                'expiry': timezone.now() + timedelta(hours=1),  # Set expiry time
            },
            upsert=True,  # Ensures that the session is updated, not overwritten
        )
        self.modified = False

    def delete(self):
        """Delete the session from MongoDB."""
        self.collection.delete_one({'session_key': self.session_key})
        self._session_cache = {}
        self.modified = False

    def exists(self, session_key):
        """Check if a session exists in MongoDB."""
        return self.collection.find_one({'session_key': session_key}) is not None

    def __setitem__(self, key, value):
        """Allow item assignment (e.g., request.session['key'] = value)"""
        self._session_cache[key] = value
        self.modified = True  # Mark the session as modified

    def __getitem__(self, key):
        """Allow item retrieval (e.g., request.session['key'])"""
        return self._session_cache[key]

    def __delitem__(self, key):
        """Allow item deletion (e.g., del request.session['key'])"""
        del self._session_cache[key]
        self.modified = True  # Mark the session as modified

    def get(self, key, default=None):
        """Get a session value, similar to dictionary get() method."""
        return self._session_cache.get(key, default)



class SessionStore:
    """Wrapper around MongoDBSession to be used by Django's session framework."""
    
    def __init__(self, session_key=None):
        """Initialize the session store."""
        self.session = MongoDBSession(session_key)

    def load(self):
        """Load the session data."""
        self.session._load()

    def create(self):
        """Create a new session."""
        self.session.create()

    def save(self):
        """Save the session data."""
        self.session.save()

    def delete(self):
        """Delete the session."""
        self.session.delete()

    def exists(self, session_key):
        """Check if the session exists."""
        return self.session.exists(session_key)

    def __getitem__(self, key):
        """Allow item retrieval (e.g., request.session['key'])"""
        return self.session._session_cache[key]

    def __setitem__(self, key, value):
        """Allow item assignment (e.g., request.session['key'] = value)"""
        self.session._session_cache[key] = value
        self.session.modified = True  # Mark the session as modified

    def __delitem__(self, key):
        """Allow item deletion (e.g., del request.session['key'])"""
        del self.session._session_cache[key]
        self.session.modified = True  # Mark the session as modified

    def get(self, key, default=None):
        """Get a session value, similar to dictionary get() method."""
        return self.session._session_cache.get(key, default)
