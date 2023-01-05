FLASK_ENV=development
FLASK_APP=spotagent.app:create_app
SECRET_KEY=secretsecret
DATABASE_URI=sqlite:////tmp/spotagent.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=rpc://
