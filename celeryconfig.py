# Broker settings
BROKER_URL = "amqp://guest:guest@localhost:5672//"

# Result store settings
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "sqlite:///files.sqlite"

# Worker settings
CELERYD_CONCURRENCY = 3

CELERY_IMPORTS = ("tasks", )