from sqlalchemy import inspect as sa_inspect


def orm_to_dict(obj) -> dict:
    """Extract column values from a SQLAlchemy ORM instance via getattr,
    which triggers lazy-reload on expired attributes after a flush/commit."""
    return {attr.key: getattr(obj, attr.key) for attr in sa_inspect(obj).mapper.column_attrs}
