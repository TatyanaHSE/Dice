from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # =========================
    # DEMOGRAPHICS
    # =========================

    gender = models.StringField(
        choices=[
            ['Male', 'Male'],
            ['Female', 'Female'],
            ['Do not want to disclose', 'Do not want to disclose'],
        ],
        label='What is your gender?'
    )

    age = models.IntegerField(
        min=15,
        max=90,
        label='What is your age?'
    )

    # =========================
    # PERSONALITY QUESTIONS
    # =========================

    q1 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q2 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q3 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q4 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q5 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q6 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q7 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q8 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q9 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    q10 = models.IntegerField(
        choices=[
            [5, '5'],
            [4, '4'],
            [3, '3'],
            [2, '2'],
            [1, '1'],
        ]
    )

    open_question = models.LongStringField(
        label=''
    )


class SurveyPage(Page):

    form_model = 'player'

    form_fields = [
        'gender',
        'age',
        'q1',
        'q2',
        'q3',
        'q4',
        'q5',
        'q6',
        'q7',
        'q8',
        'q9',
        'q10',
        'open_question',
    ]

class Final(Page):

    @staticmethod
    def vars_for_template(player):
        return dict(
            total_earnings=player.participant.vars.get(
                'total_earnings',
                0
            )
        )

# ============================================================
# PAGE SEQUENCE
# ============================================================

page_sequence = [
    SurveyPage,
    Final,
]