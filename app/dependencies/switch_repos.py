from app.core.config_settings import settings

if settings.BACKEND_REPO == "memory":
    from app.dependencies.inmemory_repos import *
else:
    from app.dependencies.postgres_repos import *
