from app.core.database import Base, engine
from app.models.user import User # Import models to register them
print("Dropping tables...")
Base.metadata.drop_all(bind=engine)
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
