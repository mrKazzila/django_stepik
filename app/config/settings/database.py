from os import environ
# https://postgresapp.com/

DATABASES = {
    'default': {
        'ENGINE': environ['DATABASE_ENGINE'],
        'NAME': environ['DATABASE_NAME'],
        'USER': environ['DATABASE_USER'],
        'PASSWORD': environ['DATABASE_PASSWORD'],
        'HOST': environ['DATABASE_HOST'],
        'PORT': environ['DATABASE_PORT'],
    },
}
