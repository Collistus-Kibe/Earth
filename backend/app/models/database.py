import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# 1. Load Env
TIDB_CONNECTION_STRING = os.getenv("TIDB_CONNECTION_STRING")

# 2. SSL Cert Path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CA_CERT_PATH = os.path.join(BACKEND_DIR, "ca.pem")

# 3. Parse Connection String
try:
    parsed_url = urlparse(TIDB_CONNECTION_STRING)
    query_params = parse_qs(parsed_url.query)
    query_params['ssl_ca'] = [CA_CERT_PATH]
    
    new_query = urlencode(query_params, doseq=True)
    new_url_parts = parsed_url._replace(query=new_query)
    FULL_CONNECTION_STRING = urlunparse(new_url_parts)
    
except Exception as e:
    print(f"Error parsing TiDB connection string: {e}")
    FULL_CONNECTION_STRING = ""

# 4. Create Engine with CONNECTION RECYCLING (The Fix)
engine = create_engine(
    FULL_CONNECTION_STRING,
    pool_pre_ping=True,   # Check connection before using
    pool_recycle=300,     # Recycle connections every 5 minutes (prevents TiDB timeouts)
    pool_size=10,         # Keep 10 connections open
    max_overflow=20       # Allow spikes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 5. Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()