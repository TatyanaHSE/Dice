from os import environ

DEBUG = 0

SESSION_CONFIGS = [
    dict(
        name='reporting_dice_experiment',
        display_name="Experiment",
        app_sequence=['reporting_dice_experiment', 'Sender_Receiver', 'survey'],
        num_demo_participants=6,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'RUB'
USE_POINTS = False

ROOMS = [
    dict(
        name='experiment',
        display_name='Dice Experiment',
        participant_label_file='_rooms/participants.txt',
        use_secure_urls=False,
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '5900042893466'

INSTALLED_APPS = ['otree']
