from otree.api import *
import random


doc = """
Parts 1–4
"""

class C(BaseConstants):
    NAME_IN_URL = 'reporting_dice_experiment'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10

    ROLL_MIN = 1
    ROLL_MAX = 6

    YES_PAYMENT = 300
    GUESS_PAYMENT = 300


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # =========================
    # PART 1
    # =========================

    roll_1 = models.IntegerField()
    roll_2 = models.IntegerField()
    roll_3 = models.IntegerField()

    answer = models.StringField(
        choices=[
            ['YES', 'YES'],
            ['NO', 'NO'],
        ],
        label='Did your chosen number appear at least once?'
    )

    # =========================
    # PART 2
    # =========================

    guess = models.IntegerField(
        choices=[
            [i, str(i)]
            for i in range(11)
        ],
        label='Recall the game you have just played. In this game, a “YES” report means that the '
              'participant’s chosen number appeared at least once in the three die rolls. A “NO” report '
              'means that the chosen number did not appear in any of the three die rolls. Each of the other'
              ' two participants in your group has just played 5 rounds and made one report in each round.'
              ' Therefore, they made 10 reports altogether. You do not need to know which numbers they chose. '
              'How many of their 10 reports do you think were “YES” reports in total? Please enter a whole '
              'number from 0 to 10.'
    )

    actual_yes_count = models.IntegerField()

    # =========================
    # CONDITION
    # =========================

    condition = models.StringField(
        choices=[
            ['feedback', 'Feedback'],
            ['control', 'Control'],
        ]
    )

    # =========================
    # PART 3
    # =========================

    part3_roll_1 = models.IntegerField()
    part3_roll_2 = models.IntegerField()
    part3_roll_3 = models.IntegerField()

    part3_answer = models.StringField(
        choices=[
            ['YES', 'YES'],
            ['NO', 'NO'],
        ],
        label='Did your chosen number appear at least once?'
    )

    # =========================
    # PART 4
    # =========================

    part4_pair_id = models.IntegerField()
    part4_partner_id = models.IntegerField()
    part4_role = models.StringField()

    part4_sender_strategy_table1 = models.StringField(
        choices=[
            ['A', 'Option A will earn you more money than Option B'],
            ['B', 'Option B will earn you more money than Option A'],
        ]
    )

    part4_sender_strategy_table2 = models.StringField(
        choices=[
            ['A', 'Option A will earn you more money than Option B'],
            ['B', 'Option B will earn you more money than Option A'],
        ]
    )

    part4_receiver_choice = models.StringField(
        choices=[
            ['A', 'Option A'],
            ['B', 'Option B'],
        ]
    )


def creating_session(subsession):
    if subsession.round_number == 1:

        groups = subsession.get_groups()
        random.shuffle(groups)

        half = len(groups) // 2

        for i, group in enumerate(groups):

            if i < half:
                condition = 'feedback'
            else:
                condition = 'control'

            for player in group.get_players():
                player.condition = condition

    else:
        for player in subsession.get_players():
            player.condition = player.in_round(1).condition


# ============================================================
# PART 1
# ============================================================
class Welcome(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Part1ChooseNumberPage(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Part1ReminderPage(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Part1RollPage(Page):

    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def is_displayed(player):
        return 1 <= player.round_number <= 5

    @staticmethod
    def vars_for_template(player):

        if player.field_maybe_none('roll_1') is None:
            player.roll_1 = random.randint(
                C.ROLL_MIN,
                C.ROLL_MAX
            )

        if player.field_maybe_none('roll_2') is None:
            player.roll_2 = random.randint(
                C.ROLL_MIN,
                C.ROLL_MAX
            )

        if player.field_maybe_none('roll_3') is None:
            player.roll_3 = random.randint(
                C.ROLL_MIN,
                C.ROLL_MAX
            )

        return dict(
            roll_1=player.roll_1,
            roll_2=player.roll_2,
            roll_3=player.roll_3,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
            player.payoff = 0


class Part1Results(Page):

    @staticmethod
    def is_displayed(player):
        return 1 <= player.round_number <= 5


class Part1FinalResults(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 5

    @staticmethod
    def vars_for_template(player):

        if 'part1_selected_round' not in player.participant.vars:

            selected_round = random.randint(1, 5)

            player.participant.vars['part1_selected_round'] = selected_round

            selected_player = player.in_round(selected_round)

            if selected_player.answer == 'YES':
                selected_earnings = C.YES_PAYMENT
            else:
                selected_earnings = 0

            player.participant.vars['part1_final_earnings'] = selected_earnings

            for round_number in range(1, 6):
                round_player = player.in_round(round_number)

                if round_number == selected_round:
                    round_player.payoff = selected_earnings
                else:
                    round_player.payoff = 0

        rounds = []

        for round_number in range(1, 6):

            round_player = player.in_round(round_number)

            if round_player.answer == 'YES':
                earnings = C.YES_PAYMENT
            else:
                earnings = 0

            rounds.append(
                dict(
                    round_number=round_number,
                    earnings=earnings,
                )
            )

        return dict(
            rounds=rounds,
            selected_round=player.participant.vars['part1_selected_round'],
            final_earnings=player.participant.vars['part1_final_earnings'],
        )

# ============================================================
# WAIT AFTER PART 1
# ============================================================

class Part1WaitPage(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 5


# ============================================================
# PART 2
# ============================================================

class Part2GuessPage(Page):

    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 5

def get_other_yes_count(player):
    other_yes_count = 0

    for other_player in player.group.get_players():
        if other_player.id_in_group != player.id_in_group:
            for round_number in range(1, 6):
                round_player = other_player.in_round(round_number)

                if round_player.answer == 'YES':
                    other_yes_count += 1

    return other_yes_count

class Part2GuessResults(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 5

    @staticmethod
    def vars_for_template(player):

        other_yes_count = get_other_yes_count(player)

        return dict(
            other_yes_count=other_yes_count,
            correct=player.in_round(5).guess == other_yes_count,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):

        other_yes_count = get_other_yes_count(player)

        player.actual_yes_count = other_yes_count

        if player.in_round(5).guess == other_yes_count:
            player.participant.vars['part2_earnings'] = C.GUESS_PAYMENT
            player.payoff = C.GUESS_PAYMENT
        else:
            player.participant.vars['part2_earnings'] = 0
            player.payoff = 0

# ============================================================
# PART 3
# ============================================================

class Part3ChooseNumberPage(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 6

class Part3ReminderPage(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 6

class Part3RollPage(Page):
    form_model = 'player'
    form_fields = ['part3_answer']

    @staticmethod
    def is_displayed(player):
        return 6 <= player.round_number <= 10

    @staticmethod
    def vars_for_template(player):
        if player.field_maybe_none('part3_roll_1') is None:
            player.part3_roll_1 = random.randint(C.ROLL_MIN, C.ROLL_MAX)

        if player.field_maybe_none('part3_roll_2') is None:
            player.part3_roll_2 = random.randint(C.ROLL_MIN, C.ROLL_MAX)

        if player.field_maybe_none('part3_roll_3') is None:
            player.part3_roll_3 = random.randint(C.ROLL_MIN, C.ROLL_MAX)

        return dict(
            roll_1=player.part3_roll_1,
            roll_2=player.part3_roll_2,
            roll_3=player.part3_roll_3,
            part3_round=player.round_number - 5,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
            player.payoff = 0


class Part3Results(Page):
    @staticmethod
    def is_displayed(player):
        return 6 <= player.round_number <= 10

    @staticmethod
    def vars_for_template(player):
        return dict(
            part3_round=player.round_number - 5
        )


class Part3FinalResults(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 10

    @staticmethod
    def vars_for_template(player):

        if 'part3_selected_round' not in player.participant.vars:

            selected_round = random.randint(6, 10)

            player.participant.vars['part3_selected_round'] = selected_round

            selected_player = player.in_round(selected_round)

            if selected_player.part3_answer == 'YES':
                selected_earnings = C.YES_PAYMENT
            else:
                selected_earnings = 0

            player.participant.vars['part3_final_earnings'] = selected_earnings

            for round_number in range(6, 11):
                round_player = player.in_round(round_number)

                if round_number == selected_round:
                    round_player.payoff = selected_earnings
                else:
                    round_player.payoff = 0

        rounds = []

        for round_number in range(6, 11):

            round_player = player.in_round(round_number)

            if round_player.part3_answer == 'YES':
                earnings = C.YES_PAYMENT
            else:
                earnings = 0

            rounds.append(
                dict(
                    round_number=round_number - 5,
                    earnings=earnings,
                )
            )

        return dict(
            rounds=rounds,
            selected_round=player.participant.vars['part3_selected_round'] - 5,
            final_earnings=player.participant.vars['part3_final_earnings'],
        )

class Part4Instructions(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 10

# ============================================================
# PAGE SEQUENCE
# ============================================================

page_sequence = [
    Welcome,

    # Part 1
    Part1ChooseNumberPage,
    Part1ReminderPage,
    Part1RollPage,
    Part1Results,

    # After Part 1
    Part1FinalResults,
    Part1WaitPage,

    # Part 2
    Part2GuessPage,
    Part2GuessResults,

    # Part 3
    Part3ChooseNumberPage,
    Part3ReminderPage,
    Part3RollPage,
    Part3Results,
    Part3FinalResults,

    # Part 4 instructions
    Part4Instructions,
    ]