import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '2a*zlf2b!q$_@@5k=mr3vvxa^dl!n9$xqacq-1$z#h_j(21gsc'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'test_app',

    # Packages for using `allauth`
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

SITE_ID = 1

# Custom User model
AUTH_USER_MODEL = 'test_app.User'

# Authentication backend classes to use for authenticating a user
AUTHENTICATION_BACKENDS = [
    # Required to login by username in Django admin (regardless of `allauth`)
    'django.contrib.auth.backends.ModelBackend',

    # Required for allauth-specific authentication (such as login by e-mail)
    'allauth.account.auth_backends.AuthenticationBackend'
]

# Redirect URL in case that unauthenticated users access a view with login_required() decorator
LOGIN_URL = '/accounts/login/'

# Redirect URL in case that unauthenticated users complete login
LOGIN_REDIRECT_URL = '/'

# Flag indicating whether authenticated users accessing login or signup page are redirected to LOGIN_REDIRECT_URL
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

# Redirect URL in case that authenticated users log out (counterpart to LOGIN_REDIRECT_URL)
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Login method to use ('username' | 'email' | 'username_email')
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Require ACCOUNT_EMAIL_REQUIRED = True

# Configuration for custom User model
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # The name of the field containing the username (!= Django's USERNAME_FIELD)
ACCOUNT_USERNAME_REQUIRED = False  # The user is required to enter a username when signing up
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'  # The name of the field containing the email
ACCOUNT_EMAIL_REQUIRED = True  # The user is required to enter an e-mail when signing up

# Email Authentication is not required
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# Custom adapters (Customize logic about how User instances are created and populated with data)  # TODO
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

# Custom forms  # TODO
ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'allauth.account.forms.SignupForm',
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm'
}
SOCIALACCOUNT_FORMS = {
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'signup': 'allauth.socialaccount.forms.SignupForm'
}
