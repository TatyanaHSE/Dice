from otree.api import *
import random


doc = """
Part 4 — Sender / Receiver
"""


class C(BaseConstants):
    NAME_IN_URL = 'Sender_Receiver'

    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    SEND_PAYMENT_LOW = 100
    SEND_PAYMENT_HIGH = 300
    RECEIVE_PAYMENT_LOW = 100
    RECEIVE_PAYMENT_HIGH = 300


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    part4_pair_id = models.IntegerField()

    part4_partner_id = models.IntegerField()

    part4_role = models.StringField(
        choices=[
            ['sender', 'Sender'],
            ['receiver', 'Receiver'],
        ]
    )

    part4_sender_strategy_table1 = models.StringField(
        choices=[
            [
                'A',
                'Option A will earn you more money than Option B'
            ],
            [
                'B',
                'Option B will earn you more money than Option A'
            ],
        ]
    )

    part4_sender_strategy_table2 = models.StringField(
        choices=[
            [
                'A',
                'Option A will earn you more money than Option B'
            ],
            [
                'B',
                'Option B will earn you more money than Option A'
            ],
        ]
    )

    part4_receiver_choice = models.StringField(
        choices=[
            ['A', 'Option A'],
            ['B', 'Option B'],
        ]
    )

# PART 4
class Part4MatchingPage(WaitPage):

    group_by_arrival_time = True

    @staticmethod
    def after_all_players_arrive(group):

        players = group.get_players()

        if len(players) != 2:
            raise ValueError(
                'Part 4 requires exactly 2 participants per pair.'
            )

        player1 = players[0]
        player2 = players[1]

        pair_id = group.id_in_subsession

        player1.part4_pair_id = pair_id
        player2.part4_pair_id = pair_id

        player1.part4_partner_id = (
            player2.participant.id_in_session
        )

        player2.part4_partner_id = (
            player1.participant.id_in_session
        )


class Part4SenderStrategy(Page):

    form_model = 'player'

    form_fields = [
        'part4_sender_strategy_table1',
        'part4_sender_strategy_table2',
    ]


class Part4SetupWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group):

        players = group.get_players()

        if len(players) != 2:
            raise ValueError(
                'Part 4 requires exactly 2 participants per pair.'
            )

        player1 = players[0]
        player2 = players[1]

        for player in players:

            selected_table = random.choice([1, 2])

            player.participant.vars[
                'part4_selected_table'
            ] = selected_table

            if selected_table == 1:
                selected_message = (
                    player.part4_sender_strategy_table1
                )
            else:
                selected_message = (
                    player.part4_sender_strategy_table2
                )

            player.participant.vars[
                'part4_selected_message'
            ] = selected_message

        if random.choice([True, False]):
            sender = player1
            receiver = player2
        else:
            sender = player2
            receiver = player1

        sender.part4_role = 'sender'
        receiver.part4_role = 'receiver'

        sender_message = (
            sender.participant.vars[
                'part4_selected_message'
            ]
        )

        receiver_message = (
            receiver.participant.vars[
                'part4_selected_message'
            ]
        )

        receiver.participant.vars[
            'part4_message_to_evaluate'
        ] = sender_message

        sender.participant.vars[
            'part4_message_to_evaluate'
        ] = receiver_message

        sender.participant.vars[
            'part4_actual_sender_message'
        ] = sender_message

        receiver.participant.vars[
            'part4_actual_sender_message'
        ] = sender_message

        actual_table = (
            sender.participant.vars[
                'part4_selected_table'
            ]
        )

        sender.participant.vars[
            'part4_actual_table'
        ] = actual_table

        receiver.participant.vars[
            'part4_actual_table'
        ] = actual_table


def get_part4_message_text(message):

    if message == 'A':
        return 'Option A will earn you more money than Option B'
    else:
        return 'Option B will earn you more money than Option A'


class Part4ActualDecisionPage(Page):

    form_model = 'player'

    form_fields = [
        'part4_receiver_choice'
    ]

    @staticmethod
    def vars_for_template(player):

        message = (
            player.participant.vars[
                'part4_message_to_evaluate'
            ]
        )

        return dict(
            sender_message=get_part4_message_text(message)
        )


class Part4ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group):

        players = group.get_players()

        if len(players) != 2:
            raise ValueError(
                'Part 4 requires exactly 2 participants per pair.'
            )

        sender = None
        receiver = None

        for player in players:

            if player.part4_role == 'sender':
                sender = player

            elif player.part4_role == 'receiver':
                receiver = player

        if sender is None or receiver is None:
            raise ValueError(
                'Could not identify Sender and Receiver.'
            )

        choice = receiver.part4_receiver_choice

        table = (
            sender.participant.vars[
                'part4_selected_table'
            ]
        )

        if table == 1:

            if choice == 'A':
                sender_payment = 100
                receiver_payment = 300
            else:
                sender_payment = 300
                receiver_payment = 100

        else:

            if choice == 'A':
                sender_payment = 300
                receiver_payment = 100
            else:
                sender_payment = 100
                receiver_payment = 300

        sender.payoff = sender_payment
        receiver.payoff = receiver_payment

        sender.participant.vars[
            'part4_final_earnings'
        ] = sender_payment

        receiver.participant.vars[
            'part4_final_earnings'
        ] = receiver_payment

# PART 4 RESULTS
class Part4Results(Page):

    @staticmethod
    def vars_for_template(player):

        role = player.part4_role

        table = (
            player.participant.vars[
                'part4_actual_table'
            ]
        )

        sender_message = (
            player.participant.vars[
                'part4_actual_sender_message'
            ]
        )

        partner_id = player.part4_partner_id

        partner = None

        for p in player.subsession.get_players():

            if p.participant.id_in_session == partner_id:
                partner = p
                break

        if partner is None:
            raise ValueError(
                'Could not find the partner.'
            )

        if role == 'receiver':
            receiver_choice = player.part4_receiver_choice
        else:
            receiver_choice = partner.part4_receiver_choice

        return dict(
            pair_id=player.part4_pair_id,
            partner_id=player.part4_partner_id,
            role=role,
            table=table,
            sender_message=get_part4_message_text(
                sender_message
            ),
            receiver_choice=receiver_choice,
            final_earnings=player.participant.vars[
                'part4_final_earnings'
            ],
        )

# ============================================================
# FINAL RESULTS
# ============================================================

class FinalResults(Page):

    @staticmethod
    def vars_for_template(player):

        part1_payoff = player.participant.vars.get(
            'part1_final_earnings',
            0
        )

        part2_payoff = player.participant.vars.get(
            'part2_earnings',
            0
        )

        part3_payoff = player.participant.vars.get(
            'part3_final_earnings',
            0
        )

        part4_payoff = player.participant.vars.get(
            'part4_final_earnings',
            0
        )

        total_earnings = (
            part1_payoff
            + part2_payoff
            + part3_payoff
            + part4_payoff
        )

        player.participant.vars['total_earnings'] = total_earnings

        return dict(
            part1_payoff=part1_payoff,
            part2_payoff=part2_payoff,
            part3_payoff=part3_payoff,
            part4_payoff=part4_payoff,
            total_earnings=total_earnings,
        )

# ============================================================
# PAGE SEQUENCE
# ============================================================

page_sequence = [
    Part4MatchingPage,
    Part4SenderStrategy,
    Part4SetupWaitPage,
    Part4ActualDecisionPage,
    Part4ResultsWaitPage,
    Part4Results,

    FinalResults,
    ]