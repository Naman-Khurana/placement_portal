from placementportalcode.extensions import db

def save(instance,commit=False):
    try:
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance
    except Exception:
        db.session.rollback()
        raise

def commit_session():
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
