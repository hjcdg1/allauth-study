import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '2a*zlf2b!q$_@@5k=mr3vvxa^dl!n9$xqacq-1$z#h_j(21gsc'

DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'allauth_study.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'allauth_study.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

SITE_ID = 1

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    }
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'test_app',

    # Apps in `allauth` package
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver'
]

# Authentication backend classes to use for authenticating a user
# Note : We don't need allauth-specific authentication backend since we use `allauth' only for social login/signup.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'  # Authenticate by USERNAME_FIELD and password
]

# Custom User model
AUTH_USER_MODEL = 'test_app.User'

# Configuration for using custom User model in `allauth`
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'  # The name of the field representing an email
ACCOUNT_EMAIL_REQUIRED = True  # The field representing an email is required when signing up
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # The name of the field representing an username (!= Django's USERNAME_FIELD)
ACCOUNT_USERNAME_REQUIRED = False  # The field representing an username is required when signing up

# The method to use when performing login
# Note 1 : Actually this configuration is not used since we use `allauth` only for social login/signup.
# Note 2 : But this configuration shouldn't be deleted for migration of `allauth.account`.
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 'email' | 'username' | 'username_email'

# Redirect URL in case that unauthenticated users access a view with login_required() decorator
LOGIN_URL = '/login/'

# Redirect URL in case that unauthenticated users complete login/signup (when 'next' parameter does not exist)
# Note : Social login/signup by `allauth` also uses this configuration.
LOGIN_REDIRECT_URL = '/'

# Email authentication is not required when signing up using social account
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# Custom adapter for social login/signup (EX. Customize how User instances are created and populated with data)
SOCIALACCOUNT_ADAPTER = 'test_app.adapter.CustomSocialAccountAdapter'

# Configuration of Session age
SESSION_COOKIE_AGE = 100 * 24 * 60 * 60  # 100일
