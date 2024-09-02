from tkinter import *
import random
import threading
import time
from tkinter import ttk
import copy
import math

# adjust DPI to configure text size for different screens
DPI_SCALE = 1.331
# enable / disable input checking for creating club
check_club_input = True

# PLAYER CLASS
# MAX SQUAD SIZE IS 28
class Player:
    def __init__(self, first_name, last_name, ovr, pos, age, day, month):
       self.first_name = first_name
       self.last_name = last_name
       self.ovr = ovr
       self.pos = pos
       self.age = age
       self.day = day
       self.month = month
       self.form = random.randint(45, 55)
       self.morale = 65
       self.fitness = 100
       self.sharpness = 0
       self.contract_expire = year + random.randint(1, 5)
       self.is_transfer_listed = False
       self.club_happiness = 80
       self.training_happiness = 50
       self.playing_time = 50
       self.wage_happiness = 80
       self.negotiation_cooldown = 0
       self.selected_position = StringVar()
       self.actual_position = StringVar()
       # selected position is position currently picked on the option menu, once this is confirmed and the squad is valid, the actual position is updated with the selected position
       self.selected_position.set("SUB")
       self.actual_position.set("SUB")
       self.played_match = False
       self.match_ovr = 0
       self.injured = 0
       self.matches_played = 0
       self.matches_not_played = 0
       self.exact_ovr = 100 - ovr
       # HAPPINESS SYSTEM,
       # club - reputation, division, loyalty - compare player ovr to league ovr
       # squad - relationships, team competitiveness, form - relationships random number, compare player ovr to best 11 avg ovr, form compare league position to predicted
       # playing time - playing time, instructions on pitch, tactics -
       # wage - wage matching expectation - compare current wage to wage player would get from the wage calculator

       # assigns a multiplier to be timesed with the temporary wage to get the players wage, wage in thousand per week
       if self.age == 16 or self.age == 17:
           multiplier = 0.35
       elif self.age == 18 or self.age == 19:
           multiplier = 0.65
       elif self.age == 20 or self.age == 21:
           multiplier = 0.85
       elif self.age == 22 or self.age == 23:
           multiplier = 1.0
       elif self.age == 24 or self.age == 25:
           multiplier = 1.2
       elif self.age == 26 or self.age == 27:
           multiplier = 1.3
       elif self.age == 28 or self.age == 29:
           multiplier = 1.4
       elif self.age == 30 or self.age == 31:
           multiplier = 1.4
       elif self.age == 32 or self.age == 33:
           multiplier = 1.2
       elif self.age == 34 or self.age == 35:
           multiplier = 1.1
       elif self.age > 35:
           multiplier = 1.0
       else:
           multiplier = 0.0

       # gets temporary value to be timesed by multiplier
       if self.ovr < 48:
           temp_wage = 0.1
       elif 50 > self.ovr > 47:
           temp_wage = 0.3
       elif 53 > self.ovr > 49:
           temp_wage = 0.5
       elif 55 > self.ovr > 52:
           temp_wage = 0.7
       elif 57 > self.ovr > 54:
           temp_wage = 1
       elif 58 > self.ovr > 56:
           temp_wage = 1.4
       elif 60 > self.ovr > 57:
           temp_wage = 1.9
       elif 63 > self.ovr > 59:
           temp_wage = 2.7
       elif 65 > self.ovr > 62:
           temp_wage = 4.8
       elif 67 > self.ovr > 64:
           temp_wage = 6.1
       elif 69 > self.ovr > 66:
           temp_wage = 8.9
       elif 71 > self.ovr > 68:
           temp_wage = 9.7
       elif 74 > self.ovr > 70:
           temp_wage = 15.5
       elif 76 > self.ovr > 73:
           temp_wage = 21.3
       elif 78 > self.ovr > 75:
           temp_wage = 27.6
       elif 80 > self.ovr > 77:
           temp_wage = 33.8
       elif 83 > self.ovr > 79:
           temp_wage = 39.7
       elif 85 > self.ovr > 82:
           temp_wage = 48.5
       elif 87 > self.ovr > 84:
           temp_wage = 85.2
       elif 89 > self.ovr > 86:
           temp_wage = 116.3
       elif 91 > self.ovr > 88:
           temp_wage = 180.2
       elif 93 > self.ovr > 90:
           temp_wage = 245.8
       elif 95 > self.ovr > 92:
           temp_wage = 301.4
       elif self.ovr > 94:
           temp_wage = 336.9
       else:
           temp_wage = 0.0

       # gets players actual wage
       value = (round_to_three_sigfigs(round(temp_wage * multiplier, 2)))

       self.wage = value

    def update_ovr(self):
        if self.age < 18:
            multiplier = 0.995
        elif self.age < 20:
            multiplier = 0.9965
        elif self.age < 22:
            multiplier = 0.997
        elif self.age < 24:
            multiplier = 0.9975
        elif self.age < 26:
            multiplier = 0.9985
        elif self.age < 28:
            multiplier = 0.999
        elif self.age < 30:
            multiplier = 1
        elif self.age < 32:
            multiplier = 1.0001
        elif self.age < 34:
            multiplier = 1.0005
        elif self.age < 36:
            multiplier = 1.001
        else:
            multiplier = 1.002

        if self.form < 20:
            multiplier *= 1.002
        elif self.form < 40:
            multiplier *= 1.001
        elif self.form < 60:
            multiplier *= 1
        elif self.form < 80:
            multiplier *= 0.999
        else:
            multiplier *= 0.998

        self.exact_ovr *= multiplier

        self.ovr = int(100 - self.exact_ovr)

    def get_extension_length_offer(self):
        if self.age > 31:
            self.extension_offer = year + 2
        elif self.age > 27:
            if self.morale > 75:
                self.extension_offer = year + random.randint(2, 4)
            else:
                self.extension_offer = year + random.randint(2, 3)
        elif self.age > 23:
            if self.morale > 75:
                self.extension_offer = year + random.randint(3, 5)
            else:
                self.extension_offer = year + random.randint(2, 4)
        else:
            if self.morale > 75:
                self.extension_offer = year + random.randint(4, 6)
            else:
                self.extension_offer = year + random.randint(2, 4)

    def get_wage_offer(self):
        # assigns a multiplier to be timesed with the temporary wage to get the players wage, wage in thousand per week
        if self.age == 16 or self.age == 17:
            multiplier = 0.35
        elif self.age == 18 or self.age == 19:
            multiplier = 0.65
        elif self.age == 20 or self.age == 21:
            multiplier = 0.85
        elif self.age == 22 or self.age == 23:
            multiplier = 1.0
        elif self.age == 24 or self.age == 25:
            multiplier = 1.2
        elif self.age == 26 or self.age == 27:
            multiplier = 1.3
        elif self.age == 28 or self.age == 29:
            multiplier = 1.4
        elif self.age == 30 or self.age == 31:
            multiplier = 1.4
        elif self.age == 32 or self.age == 33:
            multiplier = 1.2
        elif self.age == 34 or self.age == 35:
            multiplier = 1.1
        elif self.age > 35:
            multiplier = 1.0
        else:
            multiplier = 0.0

        # gets temporary value to be timesed by multiplier
        if self.ovr < 48:
            temp_wage = 0.1
        elif 50 > self.ovr > 47:
            temp_wage = 0.3
        elif 53 > self.ovr > 49:
            temp_wage = 0.5
        elif 55 > self.ovr > 52:
            temp_wage = 0.7
        elif 57 > self.ovr > 54:
            temp_wage = 1
        elif 58 > self.ovr > 56:
            temp_wage = 1.4
        elif 60 > self.ovr > 57:
            temp_wage = 1.9
        elif 63 > self.ovr > 59:
            temp_wage = 2.7
        elif 65 > self.ovr > 62:
            temp_wage = 4.8
        elif 67 > self.ovr > 64:
            temp_wage = 6.1
        elif 69 > self.ovr > 66:
            temp_wage = 8.9
        elif 71 > self.ovr > 68:
            temp_wage = 9.7
        elif 74 > self.ovr > 70:
            temp_wage = 15.5
        elif 76 > self.ovr > 73:
            temp_wage = 21.3
        elif 78 > self.ovr > 75:
            temp_wage = 27.6
        elif 80 > self.ovr > 77:
            temp_wage = 33.8
        elif 83 > self.ovr > 79:
            temp_wage = 39.7
        elif 85 > self.ovr > 82:
            temp_wage = 48.5
        elif 87 > self.ovr > 84:
            temp_wage = 85.2
        elif 89 > self.ovr > 86:
            temp_wage = 116.3
        elif 91 > self.ovr > 88:
            temp_wage = 180.2
        elif 93 > self.ovr > 90:
            temp_wage = 245.8
        elif 95 > self.ovr > 92:
            temp_wage = 301.4
        elif self.ovr > 94:
            temp_wage = 336.9
        else:
            temp_wage = 0.0

        # gets players wage offer
        return (round_to_three_sigfigs(round(temp_wage * multiplier, 2)))

    def getValue(self):
        # assigns a multiplier to be timesed with the temporary value to get the players value
        if self.age == 16 or self.age == 17:
            multiplier = 2.5
        elif self.age == 18 or self.age == 19:
            multiplier = 2.3
        elif self.age == 20 or self.age == 21:
            multiplier = 1.9
        elif self.age == 22 or self.age == 23:
            multiplier = 1.6
        elif self.age == 24 or self.age == 25:
            multiplier = 1.4
        elif self.age == 26 or self.age == 27:
            multiplier = 1.1
        elif self.age == 28 or self.age == 29:
            multiplier = 1.0
        elif self.age == 30 or self.age == 31:
            multiplier = 0.9
        elif self.age == 32 or self.age == 33:
            multiplier = 0.7
        elif self.age == 34 or self.age == 35:
            multiplier = 0.45
        elif self.age > 35:
            multiplier = 0.3
        else:
            multiplier = 0.0

        # gets temporary value to be timesed by multiplier
        if self.ovr < 44:
            temp_value = 0.04
        elif 46 > self.ovr > 43:
            temp_value = 0.07
        elif 48 > self.ovr > 45:
            temp_value = 0.1
        elif 50 > self.ovr > 47:
            temp_value = 0.15
        elif 53 > self.ovr > 49:
            temp_value = 0.2
        elif 55 > self.ovr > 52:
            temp_value = 0.3
        elif 57 > self.ovr > 54:
            temp_value = 0.4
        elif 58 > self.ovr > 56:
            temp_value = 0.5
        elif 60 > self.ovr > 57:
            temp_value = 0.7
        elif 63 > self.ovr > 59:
            temp_value = 0.9
        elif 65 > self.ovr > 62:
            temp_value = 1.2
        elif 67 > self.ovr > 64:
            temp_value = 1.5
        elif 69 > self.ovr > 66:
            temp_value = 2.2
        elif 71 > self.ovr > 68:
            temp_value = 2.8
        elif 74 > self.ovr > 70:
            temp_value = 3.7
        elif 76 > self.ovr > 73:
            temp_value = 4.6
        elif 78 > self.ovr > 75:
            temp_value = 5.5
        elif 80 > self.ovr > 77:
            temp_value = 7.4
        elif 83 > self.ovr > 79:
            temp_value = 9.9
        elif 85 > self.ovr > 82:
            temp_value = 18.6
        elif 87 > self.ovr > 84:
            temp_value = 27.1
        elif 89 > self.ovr > 86:
            temp_value = 43.3
        elif 91 > self.ovr > 88:
            temp_value = 70.2
        elif 93 > self.ovr > 90:
            temp_value = 102.7
        elif 95 > self.ovr > 92:
            temp_value = 140.9
        elif self.ovr > 94:
            temp_value = 170.8
        else:
            temp_value = 0.0

        # gets players actual value
        value = (round_to_three_sigfigs(round(temp_value * multiplier, 2)))

        return value

    def release_player(self, update_info_label):
        global release_bg, release_confirm_button, release_cancel_button, squad_size_confirm, squad_size_message, gk_num_message, gk_num_confirm, transfer_listed_players, squad_size_label, squad_confirmed
        def confirm():
            squad_confirmed = False
            if simulate_button.cget("text") == "Go to match":
                simulate_button.config(text="Squad Not Confirmed", command=print, bg="red")
            set_tactics_button.config(bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
            hide_release_popup()
            released_players.append(self)
            squad.remove(self)
            if self in transfer_listed_players:
                transfer_listed_players.remove(self)

            update_squad_display()
            update_youth_frames()
            update_scout_one_frames()
            update_scout_two_frames()
            update_scout_three_frames()
            update_info_label(squad[0])
            squad_size_label.config(text=f"Current Squad Size: {len(squad)}")
            get_team_stats()

        def hide_release_popup():
            release_bg.place_forget()
            release_confirm_button.place_forget()
            release_cancel_button.place_forget()

        def hide_squad_size_popup():
            squad_size_message.place_forget()
            squad_size_confirm.place_forget()

        def hide_gk_amount_popup():
            gk_num_message.place_forget()
            gk_num_confirm.place_forget()

        # gets amount of goalkeepers in the squad
        gk_amount = 0
        for i in squad:
            if i.pos == "GK":
                gk_amount += 1

        if len(squad) < MIN_SQUAD_SIZE + 1:
            # tells player squad is too small to release a player
            squad_size_message = Label(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Squad too small\nto release players")
            squad_size_message.place(relx=0.2, rely=0.55, relwidth=0.3, relheight=0.2)
            squad_size_confirm = Button(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Confirm", command=hide_squad_size_popup)
            squad_size_confirm.place(relx=0.2, rely=0.75, relwidth=0.3, relheight=0.1)
        elif gk_amount < 2 and self.pos == "GK":
            # tells player squad doesn't have enough gks to release player
            gk_num_message = Label(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Not enough goalkeepers in the\nsquad to release a goalkeeper")
            gk_num_message.place(relx=0.2, rely=0.55, relwidth=0.3, relheight=0.2)
            gk_num_confirm = Button(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Confirm", command=hide_gk_amount_popup)
            gk_num_confirm.place(relx=0.2, rely=0.75, relwidth=0.3, relheight=0.1)
        else:
            # prompts player to confirm/cancel releasing the player
            release_bg = Label(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Are you sure you want\nto release this player")
            release_bg.place(relx=0.2, rely=0.55, relwidth=0.3, relheight=0.2)
            release_confirm_button = Button(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Confirm", command=confirm)
            release_confirm_button.place(relx=0.2, rely=0.75, relwidth=0.15, relheight=0.1)
            release_cancel_button = Button(menu_frames[1], bg=TUTORIAL_COLOUR, fg="white", font=("Comic sans", 24), text="Cancel", command=hide_release_popup)
            release_cancel_button.place(relx=0.35, rely=0.75, relwidth=0.15, relheight=0.1)


class Staff():

    def __init__(self):
        self.rating = random.randint(1, 2)

        num = random.randint(1, 100)

        if num <= 35:
            if CLUB_COUNTRY == "England":
                self.region = "1"
            elif CLUB_COUNTRY == "France":
                self.region = "2"
            elif CLUB_COUNTRY == "Germany":
                self.region = "4"
            elif CLUB_COUNTRY == "Italy":
                self.region = "7"
            elif CLUB_COUNTRY == "Spain":
                self.region = "6"
        elif 35 < num <= 78:
            self.region = str(random.randint(0, 9))
        else:
            self.region = str(random.randint(0, 17))

        self.name = f"{random.choice(first_names[self.region])} {random.choice(last_names[self.region])}"

        if self.rating == 1:
            self.wage = random.randint(15, 28) / 100
            self.next_wage = random.randint(25, 39) / 100
        elif self.rating == 2:
            self.wage = random.randint(25, 39) / 100
            self.next_wage = random.randint(40, 65) / 100
        elif self.rating == 3:
            self.wage = random.randint(40, 65) / 100
            self.next_wage = random.randint(90, 140) / 100
        elif self.rating == 4:
            self.wage = random.randint(90, 140) / 100
            self.next_wage = random.randint(180, 245) / 100
        elif self.rating == 5:
            self.wage = random.randint(180, 245) / 100
            self.next_wage = random.randint(390, 600) / 100
        elif self.rating == 6:
            self.wage = random.randint(390, 600) / 100
            self.next_wage = random.randint(900, 1200) / 100
        elif self.rating == 7:
            self.wage = random.randint(900, 1200) / 100
            self.next_wage = random.randint(1700, 2000) / 100
        elif self.rating == 8:
            self.wage = random.randint(1700, 2000) / 100
            self.next_wage = random.randint(2700, 3400) / 100
        elif self.rating == 9:
            self.wage = random.randint(2700, 3400) / 100
            self.next_wage = random.randint(3700, 5500) / 100
        elif self.rating == 10:
            self.wage = random.randint(3700, 5500) / 100

        # calculates cost of next staff upgrade
        self.next_upgrade_cost = int((self.next_wage ** 1.3) * 50000)

    def get_wage(self):
        if self.rating == 1:
            self.wage = random.randint(15, 28) / 100
        elif self.rating == 2:
            self.wage = random.randint(25, 39) / 100
        elif self.rating == 3:
            self.wage = random.randint(40, 65) / 100
        elif self.rating == 4:
            self.wage = random.randint(90, 140) / 100
        elif self.rating == 5:
            self.wage = random.randint(180, 245) / 100
        elif self.rating == 6:
            self.wage = random.randint(390, 600) / 100
        elif self.rating == 7:
            self.wage = random.randint(900, 1200) / 100
        elif self.rating == 8:
            self.wage = random.randint(1700, 2000) / 100
        elif self.rating == 9:
            self.wage = random.randint(2700, 3400) / 100
        elif self.rating == 10:
            self.wage = random.randint(3700, 5500) / 100

    def get_next_wage(self):
        if self.rating + 1 == 1:
            self.next_wage = random.randint(15, 28) / 100
        elif self.rating + 1 == 2:
            self.next_wage = random.randint(25, 39) / 100
        elif self.rating + 1 == 3:
            self.next_wage = random.randint(40, 65) / 100
        elif self.rating + 1 == 4:
            self.next_wage = random.randint(90, 140) / 100
        elif self.rating + 1 == 5:
            self.next_wage = random.randint(180, 245) / 100
        elif self.rating + 1 == 6:
            self.next_wage = random.randint(390, 600) / 100
        elif self.rating + 1 == 7:
            self.next_wage = random.randint(900, 1200) / 100
        elif self.rating + 1 == 8:
            self.next_wage = random.randint(1700, 2000) / 100
        elif self.rating + 1 == 9:
            self.next_wage = random.randint(2700, 3400) / 100
        elif self.rating + 1 == 10:
            self.next_wage = random.randint(3700, 5500) / 100

        # calculates cost of next staff upgrade
        self.next_upgrade_cost = int((self.next_wage ** 1.3) * 50000)

window = Tk()


window.tk.call("tk", "scaling", DPI_SCALE)

# window sized to full screen
window.geometry(f"{int(window.winfo_screenheight()*1.7777)}x{int(window.winfo_screenheight())}")
window.title("Football Club Manager")
window.configure(background="green")

squadContent = None
selected_formation = StringVar()
player_name_info = None
player_ovr_info = None
player_pos_info = None
player_ovr_info = None
player_expire_info = None
player_expire_date = None
player_contract_button = None
player_transfer_list_check = None
player_release_button = None
simulating = False
simulate_button = None
menu_buttons = None
year_label = None
month_label = None
next_match_day = None
next_match_month = None
home_team_name = None
away_team_name = None
competition_name = None
match_date = None
sponsor_name = None
sponsor_revenue = None
league_objective = None
domestic_objective = None
continental_objective = None
club_happiness_label = None
wage_happiness_label = None
playtime_happiness_label = None
squad_happiness_label = None
wage_budget = None
wage_budget_label = None
wage_total = None
gk_num_message = None
gk_num_confirm = None
squad_size_message = None
squad_size_confirm = None
release_bg = None
release_confirm_button = None
release_cancel_button = None
negotiate_player_contract = None
profit_label = None
total_income_label = None
ticket_income_label = None
merch_income_label = None
sales_income_label = None
rights_income_label = None
bonus_income_label = None
sponsor_income_label = None
transfer_budget_label = None
wage_budget_label = None
prev_player_negotiation = None
current_wage_offer = None
wage_renegotiation_attempts = None
wage_paid_label = None
transfer_budget = None
total_loss_label = None
wage_loss_label = None
stwage_loss_label = None
transfer_loss_label = None
stransfer_loss_label = None
cost_loss_label = None
upgrade_loss_label = None
club_rating = None
prev_stadium_attendance = "N/A"
previous_attendance_label = None
wage_pay_day_count = 7
current_youth_maintenance = 0
next_youth_maintenance = 0
current_training_maintenance = 0
next_training_maintenance = 0
next_stadium_maintain_cost = 0
next_training_ground_cost = 0
next_youth_centre_cost = 0
next_stadium_upgrade_cost = 0
next_stadium_capacity = 0
prev_wage_total = 0
transfer_split = 0.5
wage_split = 0.5
league_ticket_price = 30
cup_ticket_price = 20
fan_relations = None
youth_players = []
youth_player_frames = []
update_youth_frames = None
team_avg_rating = 0
league = None
current_transfer_offer = 0
transfer_renegotiation_attempts = 0
scout_one_players = []
scout_two_players = []
scout_three_players = []
scout_one_frames = []
scout_two_frames = []
scout_three_frames = []
transfer_listed_players = []
transfer_offer_frame = None
squad_size_label = None
next_opponent = None
opponents_list = None
qualified_for_europe = False
next_opponent_analysis_label = None
next_opponent_league_label = None
opponent_attack_style_label = None
opponent_mentality_style_label = None
get_team_stats = None
team_attack_avg = 0
team_midfield_avg = 0
team_defence_avg = 0
attack_strength_indicators = None
defence_strength_indicators = None
TD_intensity = None
PM_intensity = None
BM_intensity = None
TD_main_focus = None
PM_main_focus = None
BM_main_focus = None
TD_second_focus = None
PM_second_focus = None
BM_second_focus = None
TD_third_focus = None
PM_third_focus = None
BM_third_focus = None
counter_attacking = 50
high_tempo_passing = 50
wing_play = 50
passing_over_the_top = 50
playing_out_of_press = 50
defending_crosses = 50
defending_deep = 50
pressing = 50
set_pieces = 50
ball_possession = 50
day_of_training = 1
next_opponent_skills = None
update_scout_one_frames = None
update_scout_two_frames = None
update_scout_three_frames = None
opponent_strengths_labels = None
opponent_weaknesses_labels = None
squad_position_vars = None
squad_confirmed = False
starting_goalkeeper = None
starting_defenders = []
starting_midfielders = []
starting_attackers = []
when_ball_lost = None
when_ball_won = None
attacking_area = None
build_up = None
player_crossing_effectiveness = None
player_pressing_effectiveness = None
player_long_ball_effectiveness = None
player_breaking_down_defence_effectiveness = None
player_set_piece_effectiveness = None
player_possession_ability = None
player_fast_counter_effectiveness = None
player_counter_frequency = None
opponent_crossing_effectiveness = None
opponent_pressing_effectiveness = None
opponent_long_ball_effectiveness = None
opponent_breaking_down_defence_effectiveness = None
opponent_set_piece_effectiveness = None
opponent_fast_counter_effectiveness = None
opponent_counter_frequency = None
player_sale_negotiation_attempts = 0
home_team = None
away_team = None
home_team_possession_value = 0
away_team_possession_value = 0
subs_left = 5
TD_warm_up = None
BM_warm_up = None
PM_warm_up = None
player_detail = None
opponent_players = None
career_wins = 0
career_draws = 0
career_losses = 0
career_goals = 0
career_goals_conceded = 0
transfers_open = True
set_tactics_button = None
player_report_widgets = []
player_relations = None
cup_r32_opponent = None
cup_r16_opponent = None
cup_qf_opponent = None
cup_sf_opponent = None
cup_f_opponent = None
cup_div_4 = []
cup_div_3 = []
cup_div_2 = []
cup_div_1 = []
pens_occurred = False
first_leg_home_score = 0
first_leg_away_score = 0
playoffs_winner = None
manager_sackable = True
# length of injuries randomly picked from here
injury_lengths = [8, 9, 10, 11, 12, 14, 15, 18, 22, 26, 30, 37, 45, 55, 65, 80, 110]
scout_one_instructions = ["Any", "Any", "Any"]
scout_two_instructions = ["Any", "Any", "Any"]
scout_three_instructions = ["Any", "Any", "Any"]
sponsor_negotiation_responses = {"Good": ["The sponsors are happy\nwith the quick negotiations", "The sponsors are pleased with\nthe positive negotiations", "The sponsors are happy with\nthe accepted deal", "The sponsors feel positive about\nthe prompt and simple negotiations", "The sponsors are pleased\nto close the deal quickly"],
                              "Medium": ["The sponsors are somewhat content\nwith the accepted deal", "The sponsors are midly content\nwith the negotiations's outcome", "The sponsors feel neutral about\nthe progress of the negotiation", "The sponsors think negotiations could\nhave been shorter but feel satisfied", "The sponsors are glad negotiations\ndidn't go on for longer"],
                              "Bad": ["The sponsors are unsatisfied with\nthe difficult negotiations", "The sponsors are displeased with\nthe prolonged negotiations", "The sponsors are unhappy\nwith the negotiations dragging on", "The sponsors have made it clear\nthe negotiations could've been simpler", "The sponsors are dissatisfied with\nthe length of the negotiations"]}
year = 2024
month = 7
day = 1
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
SCREEN_WIDTH = window.winfo_screenwidth()
LIGHT_UI_COLOUR = "#363440"
DARK_UI_COLOUR = "#26262e"
BUTTON_COLOUR = "#2482d3"
BG_COLOUR = "#3d4659"
TUTORIAL_COLOUR = "#D7CE1D"
# this is the percent of any profit earned that the board takes for themselves, changes based on financial situation
BOARD_PROFIT_CUT = random.randint(16, 25) / 100
FAN_RELATION = 67
TOTAL_MERCH_REVENUE = 0
MAX_SQUAD_SIZE = 28
MIN_SQUAD_SIZE = 19
WHITE = "white"
BLACK = "black"
GREY = "#949594"
RED = "#DF1414"
ORANGE = "#EE8012"
YELLOW = "#FFD816"
LIME = "#63E811"
GREEN = "#0AAC35"
SKY_BLUE = "#4EDFD6"
BLUE = "blue"
PURPLE = "#8516BC"
BROWN = "#4A0B0F"
SLOW_MATCH_SPEED = 1.5
MEDIUM_MATCH_SPEED = 0.7
FAST_MATCH_SPEED = 0.25
#"#F5E910"

# GOES TO SETTING CLUB UP SCREEN, triggered by new game button
def set_up():

   def check_input():
       club_name = club_name_entry.get().strip()
       delete_space = False
       cleaned_name = ""
       for i in club_name:
           if i == " ":
               if delete_space:
                   continue
               delete_space = True
           else:
               delete_space = False

           cleaned_name += i

       club_name = cleaned_name.lower().title()

       manager_name = manager_name_entry.get().strip()
       delete_space = False
       cleaned_name = ""
       for i in manager_name:
           if i == " ":
               if delete_space:
                   continue
               delete_space = True
           else:
               delete_space = False

           cleaned_name += i

       manager_name = cleaned_name.lower().title()

       stadium_name = stadium_name_entry.get().strip()
       delete_space = False
       cleaned_name = ""
       for i in stadium_name:
           if i == " ":
               if delete_space:
                   continue
               delete_space = True
           else:
               delete_space = False

           cleaned_name += i

       stadium_name = cleaned_name.lower().title()

       if check_club_input:

           contains_letter = False
           for i in club_name:
               if i.isalpha():
                   contains_letter = True

           contains_special = False
           for i in club_name:
               if not i.isalpha() and not i.isdigit() and i != " ":
                   contains_special = True

           name_taken = get_team_league(club_name)

           if len(club_name) < 3:
               warning_label.config(text="Club name must be\nat least 3 characters\nlong", bg="red")
               return
           elif len(club_name) > 15:
               warning_label.config(text="Club name must not\nbe longer than 15\ncharacters", bg="red")
               return
           elif not contains_letter:
               warning_label.config(text="Club name must\ncontain a letter", bg="red")
               return
           elif contains_special:
               warning_label.config(text="Club name must\nnot contain\nspecial characters", bg="red")
               return
           elif name_taken != "Non League":
               warning_label.config(text="Club name taken\nTry another name", bg="red")
               return

           if len(manager_name) < 2:
               warning_label.config(text="Manager name must\nbe atleast 2 characters\nlong", bg="red")
               return
           elif len(manager_name) > 18:
               warning_label.config(text="Manager name must not\nbe longer than 18\ncharacters", bg="red")
               return

           contains_non_letter = False
           for i in manager_name:
               if not i.isalpha() and i != " ":
                   contains_non_letter = True
                   warning_label.config(text="Manager name must\nonly contain letters", bg="red")
                   return

           if len(stadium_name) < 3:
               warning_label.config(text="Stadium name must\nbe atleast 3 characters\nlong", bg="red")
               return
           elif len(stadium_name) > 20:
               warning_label.config(text="Stadium name must not\nbe longer than 20\ncharacters", bg="red")
               return

           contains_letter = False
           for i in stadium_name:
               if i.isalpha():
                   contains_letter = True

           if not contains_letter:
               warning_label.config(text="Stadium name must\ncontain a letter", bg="red")
               return

           contains_special = False
           for i in stadium_name:
               if not i.isalpha() and not i.isdigit() and i != " ":
                   contains_special = True
                   warning_label.config(text="Stadium name must\nnot contain\nspecial characters", bg="red")
                   return

           if club_colour_one_selected.get() == "Colour One" or club_colour_two_selected.get() == "Colour Two":
               warning_label.config(text="You must pick\nyour club's colours", bg="red")
               return
           elif club_colour_one_selected.get() == club_colour_two_selected.get():
               warning_label.config(text="Your club colours\ncannot be the same", bg="red")
               return

           if selected_option.get() == "":
               warning_label.config(text="You must pick\nyour club's country", bg="red")
               return

       start_game(club_name, manager_name, selected_option, club_colour_one_selected.get(), club_colour_two_selected.get(), stadium_name)

   for child in window.winfo_children():
       child.destroy()

   warning_label = Label(window, bg=BG_COLOUR, fg="white", font=("Comic sans", 20))
   warning_label.place(relx=0.77, rely=0.5, relwidth=0.21, relheight=0.25)

   # CLUB SET UP LABEL
   set_club_label = Label(window, text="Club Set Up", bg="#26262e", fg="white", font=("Comic Sans", 55, "bold"), bd=10, relief="raised")
   set_club_label.place(relx=0.35, rely=0, relwidth=0.3, relheight=0.15)

   window.configure(background="#3d4659")

   # CLUB NAME ENTRY AND LABEL
   club_name_entry = Entry(window, font=("Comic Sans", 50))
   club_name_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)

   club_name_label = Label(window, text="Club Name", bg="#26262e", fg="white", font=("Comic Sans", 50, "bold"))
   club_name_label.place(relx=0.06, rely=0.2, relwidth=0.28, relheight=0.1)

   # MANAGER NAME ENTRY AND LABEL
   manager_name_entry = Entry(window, font=("Comic Sans", 50))
   manager_name_entry.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)

   manager_name_label = Label(window, text="Manager Name", bg="#26262e", fg="white", font=("Comic Sans", 45, "bold"))
   manager_name_label.place(relx=0.06, rely=0.35, relwidth=0.28, relheight=0.1)

   # STADIUM NAME ENTRY AND LABEL

   stadium_name_entry = Entry(window, font=("Comic Sans", 50))
   stadium_name_entry.place(relx=0.35, rely=0.5, relwidth=0.3, relheight=0.1)

   stadium_name_label = Label(window, text="Stadium Name", bg="#26262e", fg="white", font=("Comic Sans", 45, "bold"))
   stadium_name_label.place(relx=0.06, rely=0.5, relwidth=0.28, relheight=0.1)

   # CLUB CREST SELECTION

   # CLUB COLOUR SELECT
   colour_select = Label(window, text="Club Colours", bg="#26262e", fg="white", font=("Comic Sans", 50, "bold"))
   colour_select.place(relx=0.06, rely=0.65, relwidth=0.28, relheight=0.1)

   club_colour_one_selected = StringVar()
   club_colour_one_select = OptionMenu(window, club_colour_one_selected, *["red", "orange", "yellow", "lime green", "dark green",
                                                                          "sky blue", "blue", "purple", "brown", "white", "gray", "black"])
   club_colour_one_select.config(bg="white", fg="black", font=("Comic Sans", 35, "bold"))
   club_colour_one_select["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12, "bold"))
   club_colour_one_selected.set("Colour One")
   club_colour_one_select.place(relx=0.35, rely=0.65, relwidth=0.2, relheight=0.1)

   club_colour_two_selected = StringVar()
   club_colour_two_select = OptionMenu(window, club_colour_two_selected, *["red", "orange", "yellow", "lime green", "dark green",
                                                                          "sky blue", "blue", "purple", "brown", "white", "gray", "black"])
   club_colour_two_select.config(bg="white", fg="black", font=("Comic Sans", 35, "bold"))
   club_colour_two_select["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12, "bold"))
   club_colour_two_selected.set("Colour Two")
   club_colour_two_select.place(relx=0.56, rely=0.65, relwidth=0.2, relheight=0.1)

   # CLUB NATIONALITY
   club_nation_label = Label(window, text="Club Nationality", bg="#26262e", fg="white", font=("Comic Sans", 40, "bold"))
   club_nation_label.place(relx=0.06, rely=0.8, relwidth=0.28, relheight=0.1)

   options = ["England", "France", "Germany", "Italy", "Spain"]
   selected_option = StringVar()

   dropdown = OptionMenu(window, selected_option, *options)
   dropdown.configure(font=("Comic Sans", 45))
   dropdown["menu"].config(font=("Comic Sans", 25), bg="#26262e", fg="white")
   dropdown.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

   # CONFIRM SET UP BUTTON

   confirm_button = Button(window, text="Confirm", fg="white", bg="#26262e", font=("Comic Sans", 50, "bold"),
                           command=check_input)
   confirm_button.place(relx=0.7, rely=0.8, relwidth=0.25, relheight=0.1)

def update_squad_display():
    global squadContent, all_squad_labels, selected_formation, player_name_info, player_ovr_info, player_pos_info, player_contract_button, player_expire_info, player_expire_date, player_transfer_list_check, player_release_button, playtime_happiness_label, club_happiness_label, squad_happiness_label, wage_happiness_label, squad_position_vars

    # Hide all existing labels
    for row_labels in all_squad_labels:
        for label in row_labels:
            label.grid_forget()

    def transfer_list_player(player_object):
        global transfer_listed_players
        if player_transfer_list_check.cget("bg") == "#26262e":
            player_transfer_list_check.configure(bg="#3F3F4E")
            player_object.is_transfer_listed = True
            transfer_listed_players.append(player_object)
        else:
            player_transfer_list_check.configure(bg="#26262e")
            player_object.is_transfer_listed = False
            if player_object in transfer_listed_players:
                transfer_listed_players.remove(player_object)

    def display_player_info(player_object):

        player_ovr = player_object.ovr
        player_pos = player_object.pos
        player_expiry = player_object.contract_expire
        player_name = f"{player_object.first_name} {player_object.last_name}"

        for message in [release_bg, release_cancel_button, release_confirm_button, squad_size_message, squad_size_confirm, gk_num_message, gk_num_confirm]:
            if message and message.winfo_ismapped():
                message.place_forget()

        if player_object.injured > 0:
            player_detail.config(text=f"Player injured for {player_object.injured} days")
        else:
            player_detail.config(text="Player available for selection")

        player_name_info.configure(text=player_name)
        player_ovr_info.configure(text=player_ovr)
        player_pos_info.configure(text=player_pos)
        player_expire_info.configure(text="Contract Expires:")
        player_expire_date.configure(text=player_expiry)
        player_contract_button.configure(bg="#26262e", text="Negotiate New Contract", command=lambda: negotiate_player_contract(player_object))
        player_transfer_list_check.configure(bg="#3F3F4E" if player_object.is_transfer_listed else "#26262e", text="Transfer List Player", command=lambda: transfer_list_player(player_object))
        player_release_button.configure(bg="#26262e", text="Release Player", command=lambda: player_object.release_player(display_player_info))

        if player_object.club_happiness > 65:
            club_happiness_label.config(text="Good", fg="green")
        elif player_object.club_happiness < 34:
            club_happiness_label.config(text="Bad", fg="red")
        else:
            club_happiness_label.config(text="Okay", fg="yellow")

        if player_object.training_happiness > 65:
            squad_happiness_label.config(text="Good", fg="green")
        elif player_object.training_happiness < 34:
            squad_happiness_label.config(text="Bad", fg="red")
        else:
            squad_happiness_label.config(text="Okay", fg="yellow")

        if player_object.playing_time > 65:
            playtime_happiness_label.config(text="Good", fg="green")
        elif player_object.playing_time < 34:
            playtime_happiness_label.config(text="Bad", fg="red")
        else:
            playtime_happiness_label.config(text="Okay", fg="yellow")

        if player_object.wage_happiness > 65:
            wage_happiness_label.config(text="Good", fg="green")
        elif player_object.wage_happiness < 34:
            wage_happiness_label.config(text="Bad", fg="red")
        else:
            wage_happiness_label.config(text="Okay", fg="yellow")

        club_happiness_label.place(relx=0.12, rely=0.75, relwidth=0.1, relheight=0.03)
        squad_happiness_label.place(relx=0.24, rely=0.75, relwidth=0.1, relheight=0.03)
        playtime_happiness_label.place(relx=0.12, rely=0.81, relwidth=0.1, relheight=0.03)
        wage_happiness_label.place(relx=0.24, rely=0.81, relwidth=0.1, relheight=0.03)

    options1 = ["SUB", "LB", "CB", "RB", "DM", "CM", "AM", "LF", "CF", "RF"]
    options2 = ["SUB", "GK"]

    for i, player in enumerate(squad):
        if i >= len(all_squad_labels):
            all_squad_labels.append([None] * 11)  # Create a new row if it doesn't exist

        option_list = options2 if player.pos == "GK" else options1

        sharpness_colour = get_color_based_on_value(player.sharpness)
        fitness_colour = get_color_based_on_value(player.fitness)
        morale_colour = get_color_based_on_morale(player.morale)

        if player.injured == 0:
            player_name_background = LIGHT_UI_COLOUR
        else:
            player_name_background = "red"

        if all_squad_labels[i][0] is None:
            all_squad_labels[i][0] = Button(squadContent, text=f"{player.first_name} {player.last_name}", bg=player_name_background, fg="white",
                   font=("Comic Sans", round(window.winfo_screenwidth() / 100)), padx=10, borderwidth=0,
                   command=lambda p=player: display_player_info(p),
                   width=round(SCREEN_WIDTH * 0.01))
            all_squad_labels[i][1] = OptionMenu(squadContent, player.selected_position, *option_list)
            all_squad_labels[i][2] = Label(squadContent, text=player.ovr, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                  padx=10, width=round(SCREEN_WIDTH * 0.001))
            all_squad_labels[i][3] = Label(squadContent, text=player.pos, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                  padx=10, width=round(SCREEN_WIDTH * 0.001))
            all_squad_labels[i][4] = Label(squadContent, bg=fitness_colour, width=round(SCREEN_WIDTH * 0.001))
            all_squad_labels[i][5] = Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005))
            all_squad_labels[i][6] = Label(squadContent, bg=sharpness_colour, width=round(SCREEN_WIDTH * 0.001))
            all_squad_labels[i][7] = Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005))
            all_squad_labels[i][8] = Label(squadContent, bg=morale_colour, width=round(SCREEN_WIDTH * 0.001))
            all_squad_labels[i][9] = Label(squadContent, text=player.age, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                  padx=round(SCREEN_WIDTH * 0.001), width=round(SCREEN_WIDTH * 0.0025))
            all_squad_labels[i][10] = Label(squadContent, text=player.getValue(), bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                  padx=round(SCREEN_WIDTH * 0.0005), width=round(SCREEN_WIDTH * 0.002))

        labels = all_squad_labels[i]

        # Update label texts and colors
        labels[0].configure(text=f"{player.first_name} {player.last_name}", command=lambda p=player: display_player_info(p), bg=player_name_background)
        labels[2].configure(text=player.ovr)
        labels[3].configure(text=player.pos)
        labels[4].configure(bg=fitness_colour)
        labels[6].configure(bg=sharpness_colour)
        labels[8].configure(bg=morale_colour)
        labels[9].configure(text=player.age)
        labels[10].configure(text=player.getValue())
        labels[1]["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 14))

        display_player_info(squad[0])

        for j, label in enumerate(labels):
            if label != labels[1]:
                label.grid(row=i + 1, column=j)

        for j, pos_var in enumerate(squad_position_vars):
            if pos_var is player.selected_position:
                all_squad_labels[j][1].grid(row=i+1, column=1)

def get_color_based_on_value(value):
    if value >= 84:
        return "green"
    elif value >= 68:
        return "#84FF00"
    elif value >= 50:
        return "#FFEE00"
    elif value >= 33:
        return "#FF7700"
    else:
        return "red"

def get_color_based_on_morale(value):
    if value >= 70:
        return "green"
    elif value >= 60:
        return "#84FF00"
    elif value >= 45:
        return "#FFEE00"
    elif value >= 35:
        return "#FF7700"
    else:
        return "red"

# sorts the squad list by name and then calls the function to update the squad label
def sort_squad_name():
    global squad
    squad.sort(key=lambda item: item.last_name)
    update_squad_display()

def sort_squad_ovr():
    global squad
    squad.sort(key=lambda item: item.ovr, reverse=True)
    update_squad_display()

def sort_squad_age():
    global squad
    squad.sort(key=lambda item: item.age)
    update_squad_display()

def sort_squad_value():
    global squad
    squad.sort(key=lambda item: item.getValue(), reverse=True)
    update_squad_display()

def sort_squad_pos():
    global squad
    # Define the custom sorting key
    position_order = {"GK": 0, "LB": 1, "RB": 2, "CB": 3, "DM": 4, "CM": 5, "AM": 6, "LF": 7, "CF": 9, "RF": 8}

    # Sort the list based on the custom sorting key
    squad = sorted(squad, key=lambda x: position_order[x.pos])
    update_squad_display()

def sort_squad_wage():
    global squad
    squad.sort(key=lambda item: item.wage, reverse=True)
    update_squad_display()


def get_team_league(search_team_name):
    for i in eng_4:
        if search_team_name == i[0]:
            return "England Division Four"

    for i in eng_3:
        if search_team_name == i[0]:
            return "England Division Three"

    for i in eng_2:
        if search_team_name == i[0]:
            return "England Division Two"

    for i in eng_1:
        if search_team_name == i[0]:
            return "England Division One"

    for i in fra_2:
        if search_team_name == i[0]:
            return "France Division Two"

    for i in fra_1:
        if search_team_name == i[0]:
            return "France Division One"

    for i in ger_2:
        if search_team_name == i[0]:
            return "Germany Division Two"

    for i in ger_1:
        if search_team_name == i[0]:
            return "Germany Division One"

    for i in ita_2:
        if search_team_name == i[0]:
            return "Italy Division Two"

    for i in ita_1:
        if search_team_name == i[0]:
            return "Italy Division One"

    for i in spa_2:
        if search_team_name == i[0]:
            return "Spain Division Two"

    for i in spa_1:
        if search_team_name == i[0]:
            return "Spain Division One"

    return "Non League"


# GETS SET UP INFO AND STARTS MAIN GAME, triggered by confirm button
def start_game(cne, mne, cn, cc1, cc2, sn):
   global CLUB_NAME
   global MANAGER_NAME
   global CLUB_COLOUR
   global CLUB_COUNTRY
   global menu_frames
   global squad
   global squadContent
   global all_squad_labels
   global selected_formation
   global player_name_info
   global player_ovr_info
   global player_pos_info
   global player_contract_button
   global player_expire_date
   global player_expire_info
   global player_transfer_list_check
   global player_release_button
   global menu_buttons
   global club_happiness_label, squad_happiness_label, wage_happiness_label, playtime_happiness_label
   global negotiate_player_contract
   global update_youth_frames
   global league
   global next_opponent, opponents_list, get_team_stats, update_scout_one_frames, update_scout_two_frames, update_scout_three_frames, squad_position_vars, set_tactics_button

   # GET DATA INPUTTED IN PREV SCREEN
   CLUB_NAME = cne
   MANAGER_NAME = mne
   if cc1 == "red":
       CLUB_COLOUR_ONE = RED
   elif cc1 == "orange":
       CLUB_COLOUR_ONE = ORANGE
   elif cc1 == "yellow":
       CLUB_COLOUR_ONE = YELLOW
   elif cc1 == "lime green":
       CLUB_COLOUR_ONE = LIME
   elif cc1 == "dark green":
       CLUB_COLOUR_ONE = GREEN
   elif cc1 == "sky blue":
       CLUB_COLOUR_ONE = SKY_BLUE
   elif cc1 == "blue":
       CLUB_COLOUR_ONE = BLUE
   elif cc1 == "purple":
       CLUB_COLOUR_ONE = PURPLE
   elif cc1 == "brown":
       CLUB_COLOUR_ONE = BROWN
   elif cc1 == "white":
       CLUB_COLOUR_ONE = WHITE
   elif cc1 == "gray":
       CLUB_COLOUR_ONE = GREY
   else:
       CLUB_COLOUR_ONE = BLACK

   if cc2 == "red":
       CLUB_COLOUR_TWO = RED
   elif cc2 == "orange":
       CLUB_COLOUR_TWO = ORANGE
   elif cc2 == "yellow":
       CLUB_COLOUR_TWO = YELLOW
   elif cc2 == "lime green":
       CLUB_COLOUR_TWO = LIME
   elif cc2 == "dark green":
       CLUB_COLOUR_TWO = GREEN
   elif cc2 == "sky blue":
       CLUB_COLOUR_TWO = SKY_BLUE
   elif cc2 == "blue":
       CLUB_COLOUR_TWO = BLUE
   elif cc2 == "purple":
       CLUB_COLOUR_TWO = PURPLE
   elif cc2 == "brown":
       CLUB_COLOUR_TWO = BROWN
   elif cc2 == "white":
       CLUB_COLOUR_TWO = WHITE
   elif cc2 == "gray":
       CLUB_COLOUR_TWO = GREY
   else:
       CLUB_COLOUR_TWO = BLACK

   CLUB_COUNTRY = cn.get()
   STADIUM_NAME = sn

   chief_scout = Staff()
   scout_one = Staff()
   scout_two = Staff()
   scout_three = Staff()
   fitness_coach = Staff()
   physiotherapist = Staff()
   chief_analyst = Staff()
   gk_coach = Staff()
   youth_coach = Staff()

   def get_team_avg_rating():
       global team_avg_rating
       squad.sort(key=lambda item: item.ovr, reverse=True)
       total = 0
       for i in range(11):
           total += squad[i].ovr
           # gets average rating of the 11 best players in the squad
       team_avg_rating = int(total/11)
       if team_avg_rating < 55:
           rating = 1
       elif 58 > team_avg_rating > 54:
           rating = 2
       elif 62 > team_avg_rating > 57:
           rating = 3
       elif 64 > team_avg_rating > 61:
           rating = 4
       elif 66 > team_avg_rating > 63:
           rating = 5
       elif 68 > team_avg_rating > 65:
           rating = 6
       elif 70 > team_avg_rating > 67:
           rating = 7
       elif 71 > team_avg_rating > 69:
           rating = 8
       elif 73 > team_avg_rating > 70:
           rating = 9
       elif 75 > team_avg_rating > 72:
           rating = 10
       elif 77 > team_avg_rating > 74:
           rating = 11
       elif 79 > team_avg_rating > 76:
           rating = 12
       elif 81 > team_avg_rating > 78:
           rating = 13
       elif 83 > team_avg_rating > 80:
           rating = 14
       elif 84 > team_avg_rating > 82:
           rating = 15
       elif 85 > team_avg_rating > 83:
           rating = 16
       elif 86 > team_avg_rating > 84:
           rating = 17
       elif 88 > team_avg_rating > 85:
           rating = 18
       elif 89 > team_avg_rating > 87:
           rating = 19
       else:
           rating = 20

       if club_rating is not None:
           club_rating.config(text=f"{rating}/20")

   for child in window.winfo_children():
       child.destroy()

   # adds created club to the league list, 0, 0, 9, 9, 0 is placeholder for club stats and sets min max ovr for initial squad generation
   if CLUB_COUNTRY == "England":
       # 46, 62
       league = eng_4
       min_ovr, max_ovr = 48, 62
   elif CLUB_COUNTRY == "France":
       league = fra_2
       min_ovr, max_ovr = 59, 76
   elif CLUB_COUNTRY == "Germany":
       league = ger_2
       min_ovr, max_ovr = 56, 75
   elif CLUB_COUNTRY == "Italy":
       league = ita_2
       min_ovr, max_ovr = 58, 76
   elif CLUB_COUNTRY == "Spain":
       league = spa_2
       min_ovr, max_ovr = 60, 76

   league[0] = [CLUB_NAME, 0, 0, 9, 9, 0, 0]
   league.sort(key=lambda x: x[0])

   def create_opponent_list():
       global opponents_list, next_match_month, next_match_day

       opponents_list = []

       shuffled_league = copy.deepcopy(league)

       for i in shuffled_league:
           if i[0] == CLUB_NAME:
               shuffled_league.remove(i)

       random.shuffle(shuffled_league)

       # first half of the season
       for i in shuffled_league:
           # decides whether game is home or away
           next_team = i.copy()
           next_team.append(random.choice(["H", "A"]))
           next_team.append("League")
           opponents_list.append(next_team)

       shuffled_league = copy.deepcopy(league)

       for i in shuffled_league:
           if i[0] == CLUB_NAME:
               shuffled_league.remove(i)

       random.shuffle(shuffled_league)

       # second half of the season
       for i in shuffled_league:
           # Use the home/away status from the first half
           next_team = i.copy()
           if opponents_list[shuffled_league.index(i)][-2] == "H":
               next_team.append("A")
           else:
               next_team.append("H")

           next_team.append("League")

           opponents_list.append(next_team)

       if league == eng_4 or league == eng_3 or league == eng_2:
           print(opponents_list)
           print(len(opponents_list))
           print(len(eng_4_2_dates))
           for i in range(len(opponents_list)):
               opponents_list[i].append(eng_4_2_dates[i][0])
               opponents_list[i].append(eng_4_2_dates[i][1])
           for i in playoff_dates:
               opponents_list.append(i)
       elif league in [eng_1, spa_1, ita_1]:
           for i in range(len(opponents_list)):
               opponents_list[i].append(thirty_eight_league_dates[i][0])
               opponents_list[i].append(thirty_eight_league_dates[i][1])
       elif league == ita_2:
           for i in range(len(opponents_list)):
               opponents_list[i].append(thirty_eight_league_dates_playoffs[i][0])
               opponents_list[i].append(thirty_eight_league_dates_playoffs[i][1])
           for i in playoff_dates:
               opponents_list.append(i)
       elif league in [fra_1, ger_1]:
           for i in range(len(opponents_list)):
               opponents_list[i].append(thirty_four_league_dates[i][0])
               opponents_list[i].append(thirty_four_league_dates[i][1])
       elif league in [ger_2, fra_2]:
           for i in range(len(opponents_list)):
               opponents_list[i].append(thirty_four_league_dates_playoffs[i][0])
               opponents_list[i].append(thirty_four_league_dates_playoffs[i][1])
           for i in playoff_dates:
               opponents_list.append(i)
       else:
           for i in range(len(opponents_list)):
               opponents_list[i].append(fourty_two_league_dates_playoffs[i][0])
               opponents_list[i].append(fourty_two_league_dates_playoffs[i][1])
           for i in playoff_dates:
               opponents_list.append(i)

       # adds cup dates
       for i in nat_cup_dates:
           opponents_list.append(i)

       for index, i in enumerate(opponents_list):
           if i[10] == "Cup Round of 32":
               opponents_list[index] = cup_r32_opponent + ["A", "Cup Round of 32", 12, 9]

       if qualified_for_europe:
           for i in int_cup_dates:
               opponents_list.append(i)

       # ORDER OPPONENTS LIST BY MATCH DATE
       month_order = {7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11}

       opponents_list = sorted(opponents_list, key=lambda x: (month_order.get(x[12]), x[11]))

       next_match_day = opponents_list[0][11]
       next_match_month = opponents_list[0][12]

       match_year = year
       if next_match_month < month:
           match_year += 1

       match_date.config(text=f"{next_match_day} {months[int(next_match_month)-1]} {match_year}")

       for i in range(len(opponents_list)):
           schedule_labels[i].config(text=f"{opponents_list[i][10]} ({opponents_list[i][9]}) {opponents_list[i][0]}, {opponents_list[i][11]} {months[int(opponents_list[i][12])-1]}")

       schedule_labels[0].config(bg=LIGHT_UI_COLOUR)

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "GK"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "LB"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "RB"))

   for i in range(4):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "CB"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "DM"))

   for i in range(random.randint(4,5)):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "CM"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "AM"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "LF"))

   for i in range(2):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "RF"))

   for i in range(random.randint(3,4)):
       squad.append(gen_player(random.randint(min_ovr, max_ovr), "CF"))

   for i in squad:
       print(i.first_name, i.last_name, i.ovr, i.pos, i.age, i.day, i.month)

   get_team_avg_rating()

   menu_buttons = [Button(window, bg="#26262e", fg="white", text="Matches", font=("Comic Sans", 32), relief="flat",
                          activebackground="#26262e", activeforeground="white")]

   # BUTTONS TO GO TO A SUB MENU IN MAIN SCREEN
   menu_buttons[0].place(relx=0, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Squad", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[1].place(relx=0.125, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Training", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[2].place(relx=0.25, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Club", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[3].place(relx=0.375, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Finances", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[4].place(relx=0.5, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Transfers", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[5].place(relx=0.625, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Facilities", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[6].place(relx=0.75, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons.append(Button(window, bg="#26262e", fg="white", text="Profile", font=("Comic Sans", 32), relief="flat", activebackground="#26262e", activeforeground="white"))
   menu_buttons[7].place(relx=0.875, rely=0.85, relwidth=0.125, relheight=0.15)

   menu_buttons[0].configure(command=lambda: change_menu(0), disabledforeground="#3d4659")
   menu_buttons[1].configure(command=lambda: change_menu(1), disabledforeground="#3d4659")
   menu_buttons[2].configure(command=lambda: change_menu(2), disabledforeground="#3d4659")
   menu_buttons[3].configure(command=lambda: change_menu(3), disabledforeground="#3d4659")
   menu_buttons[4].configure(command=lambda: change_menu(4), disabledforeground="#3d4659")
   menu_buttons[5].configure(command=lambda: change_menu(5), disabledforeground="#3d4659")
   menu_buttons[6].configure(command=lambda: change_menu(8), disabledforeground="#3d4659")
   menu_buttons[7].configure(command=lambda: change_menu(11), disabledforeground="#3d4659")

   menu_frames = [Frame(window) for i in range(14)]

   # CHANGES ALL FRAMES BG COLOR
   for frame in menu_frames:
       frame.configure(background=BG_COLOUR)

   menu_frames[7].configure(background=DARK_UI_COLOUR)
   menu_frames[8].configure(background="green")
   menu_frames[9].configure(background=DARK_UI_COLOUR)
   menu_frames[10].configure(background=DARK_UI_COLOUR)
   menu_frames[12].configure(background=DARK_UI_COLOUR)
   menu_frames[13].configure(background=DARK_UI_COLOUR)

   # menu 10 (schedule) widgets
   def leave_schedule_menu():
       change_menu(0)
       show_menu_buttons()

   Label(menu_frames[11], bg=DARK_UI_COLOUR).place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.65)
   Label(menu_frames[11], bg=DARK_UI_COLOUR).place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.65)
   Label(menu_frames[11], bg=LIGHT_UI_COLOUR).place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.35)
   Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="#CBB119", font=("Comic sans", 22, "bold"), text="Trophy Cabinet").place(relx=0.5, rely=0.35, relwidth=0.4, relheight=0.1)

   Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 22, "bold"), text="Career Stats").place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.1)
   Label(menu_frames[11], bg="white").place(relx=0.53, rely=0.2, relwidth=0.34, relheight=0.03)
   career_wins_label = Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="green", font=("Comic sans", 18), text="0 Wins (0%)")
   career_draws_label = Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18), text="0 Draws (0%)")
   career_losses_label = Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="red", font=("Comic sans", 18), text="0 Losses (0%)")

   def exit_popup_message():
       change_menu(0)
       show_menu_buttons()

   Button(menu_frames[12], text="Confirm", fg="white", bg=BUTTON_COLOUR, font=("Comic sans", 24), command=exit_popup_message).place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.15)
   Label(menu_frames[12], text=f"To {MANAGER_NAME},", fg="black", bg="white", font=("Ink Free", 24, "bold")).place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.08)
   popup_message = Label(menu_frames[12], fg="black", bg="white", font=("Ink Free", 20))
   popup_message.place(relx=0.2, rely=0.18, relwidth=0.6, relheight=0.45)

   career_wins_label.place(relx=0.505, rely=0.25, relwidth=0.13, relheight=0.04)
   career_draws_label.place(relx=0.635, rely=0.25, relwidth=0.13, relheight=0.04)
   career_losses_label.place(relx=0.765, rely=0.25, relwidth=0.13, relheight=0.04)

   career_goals_scored_label =  Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18), text="0 Goals Scored")
   career_goals_conceded_label = Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18), text="0 Goals Conceded")

   career_goals_scored_label.place(relx=0.5, rely=0.3, relwidth=0.2, relheight=0.05)
   career_goals_conceded_label.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.05)

   career_wins_bar = Label(menu_frames[11], bg="green")
   career_wins_bar.place(relx=0.53, rely=0.2, relwidth=0, relheight=0.03)
   career_losses_bar = Label(menu_frames[11], bg="red")
   career_losses_bar.place(relx=0.87, rely=0.2, relwidth=0, relheight=0.03)

   Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 22, "bold"), text="Manager Profile").place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)
   Label(menu_frames[11], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 15), text="Name").place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.05)
   Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20), text=MANAGER_NAME).place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.1)
   Label(menu_frames[11], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 15), text="Current Club").place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.05)
   Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20), text=CLUB_NAME).place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
   Label(menu_frames[11], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 15), text="Highest Ever Division").place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)
   if CLUB_COUNTRY == "England":
       highest_div = "England Division Four"
   elif CLUB_COUNTRY == "France":
       highest_div = "France Division Two"
   elif CLUB_COUNTRY == "Germany":
       highest_div = "Germany Division Two"
   elif CLUB_COUNTRY == "Italy":
       highest_div = "Italy Division Two"
   else:
       highest_div = "Spain Division Two"
   highest_div_label = Label(menu_frames[11], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20), text=highest_div)
   highest_div_label.place(relx=0.1, rely=0.55, relwidth=0.3, relheight=0.1)

   def go_to_fortfeit():
       change_menu(13)
       hide_menu_buttons_grey()

   def dont_fortfeit_match():
       change_menu(0)
       show_menu_buttons()

   def fortfeit_match():
       global career_wins, career_draws, career_losses, career_goals, career_goals_conceded, next_opponent, next_opponent_skills, next_match_day, next_match_month, squad_confirmed
       squad_size_label.config(text=f"Current Squad Size: {len(squad)}")

       for i in schedule_labels:
           if i.cget("bg") == LIGHT_UI_COLOUR:
               competition = competition_name.cget("text")
               if next_opponent[9] == "A":
                   i.config(text=f"{competition} 0 - 3 vs {next_opponent[0]} {next_match_day} {months[next_match_month - 1]}", fg="red")
               else:
                   i.config(text=f"{competition} 3 - 0 vs {next_opponent[0]} {next_match_day} {months[next_match_month - 1]}", fg="red")

       career_losses += 1
       career_goals_conceded += 3
       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses)) * 100)}%)")
       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses)) * 100)}%)")
       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses)) * 100)}%)")
       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
       career_wins_bar.place(relx=0.53, rely=0.2, relwidth=0.34 * career_wins / (career_wins + career_draws + career_losses), relheight=0.03)
       losses_width = 0.34 * career_losses / (career_wins + career_draws + career_losses)
       career_losses_bar.place(relx=0.87 - losses_width, rely=0.2, relwidth=losses_width, relheight=0.03)

       simulate_button.config(text="Simulate", command=sim_button, bg=BUTTON_COLOUR)
       reset_match()
       set_tactics_button.config(command=lambda: set_tactics(False), bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
       player_transfer_list_check.config(state="active")
       player_contract_button.config(state="active")
       player_release_button.config(state="active")
       display_player_info(squad[0])
       opponents_list.pop(0)
       move_schedule_labels = 1
       while opponents_list[0][0] == "N/A":
           opponents_list.pop(0)
           move_schedule_labels += 1
       next_opponent = opponents_list[0]
       next_opponent_analysis_label.config(text=next_opponent[0])
       next_opponent_league_label.config(text=get_team_league(next_opponent[0]))
       competition_name.config(text=next_opponent[10])
       calc_opponent_strength()
       next_opponent_skills = get_opponent_skills(next_opponent)

       skill_names = ["Counter Attacking", "High Tempo Passing", "Wing Play", "Passing Over The Top", "Playing Out Of Press", "Defending Crosses", "Defending Deep",
                      "Pressing", "Set Pieces", "Ball Possession"]
       best_skills = []

       for i in enumerate(next_opponent_skills):
           best_skills.append([skill_names[i[0]], i[1]])

       best_skills.sort(key=lambda i: i[1], reverse=True)
       print(best_skills)

       opponent_strengths_labels[0].config(text=best_skills[0][0])
       opponent_strengths_labels[1].config(text=best_skills[1][0])
       opponent_strengths_labels[2].config(text=best_skills[2][0])

       opponent_weaknesses_labels[0].config(text=best_skills[-1][0])
       opponent_weaknesses_labels[1].config(text=best_skills[-2][0])
       opponent_weaknesses_labels[2].config(text=best_skills[-3][0])

       if next_opponent[3] == 0:
           opponent_attack_style_label.config(text="Possession")
       elif next_opponent[3] == 1:
           opponent_attack_style_label.config(text="Counter Attacking")
       elif next_opponent[3] == 2:
           opponent_attack_style_label.config(text="Physical")
       elif next_opponent[3] == 3:
           opponent_attack_style_label.config(text="Direct")
       else:
           opponent_attack_style_label.config(text="Balanced")

       if next_opponent[9] == "H":
           home_team_name.config(text=CLUB_NAME)
           away_team_name.config(text=next_opponent[0])
       else:
           away_team_name.config(text=CLUB_NAME)
           home_team_name.config(text=next_opponent[0])

       for i in range(move_schedule_labels):
           for j in range(len(schedule_labels)):
               if schedule_labels[j].cget("bg") == LIGHT_UI_COLOUR:
                   schedule_labels[j].config(bg=DARK_UI_COLOUR)
                   schedule_labels[j + 1].config(bg=LIGHT_UI_COLOUR)
                   break

       next_match_day = next_opponent[11]
       next_match_month = next_opponent[12]

       match_year = year
       if next_match_month < month:
           match_year += 1
       match_date.configure(text=f"{next_match_day} {months[next_match_month - 1]} {match_year}")
       squad_confirmed = False
       update_squad_display()

       change_menu(0)
       show_menu_buttons()

   Label(menu_frames[13], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 22), text="If you are unable to field a team for this match,\nyou may fortfeit the match. This will result in\na 3-0 loss and you will not receive matchday income\nDo you want to fortfeit the match?").place(relx=0.1, rely=0.1, relheight=0.5, relwidth=0.8)
   Button(menu_frames[13], bg=BUTTON_COLOUR, text="Yes", font=("Comic sans", 22), fg="white", command=fortfeit_match).place(relx=0.2, rely=0.7, relwidth=0.2, relheight=0.1)
   Button(menu_frames[13], bg=BUTTON_COLOUR, text="No", font=("Comic sans", 22), fg="white", command=dont_fortfeit_match).place(relx=0.6, rely=0.7, relwidth=0.2, relheight=0.1)

   Button(menu_frames[10], text="Back", fg="white", bg=BUTTON_COLOUR, font=("Comic sans", 20), command=leave_schedule_menu).place(relx=0.85, rely=0.72, relwidth=0.12, relheight=0.08)
   schedule_labels = []

   for i in range(21):
       schedule_labels.append(Label(menu_frames[10], text="", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 12)))
       schedule_labels[-1].place(relx=0.025, rely=(i*0.04)+0.01, relwidth=0.25, relheight=0.04)

   for i in range(21):
       schedule_labels.append(Label(menu_frames[10], text="", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 12)))
       schedule_labels[-1].place(relx=0.3, rely=(i*0.04)+0.01, relwidth=0.25, relheight=0.04)

   for i in range(21):
       schedule_labels.append(Label(menu_frames[10], text="", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 12)))
       schedule_labels[-1].place(relx=0.575, rely=(i*0.04)+0.01, relwidth=0.25, relheight=0.04)

   schedule_labels[0].config(bg=LIGHT_UI_COLOUR)

   # background for league table
   Label(menu_frames[0], bg="#363440").place(relx=0, rely=0.075, relwidth=0.21, relheight=0.775)

   league_widgets = []

   for i in range(24):
       league_widgets.append([Label(menu_frames[0], bg=LIGHT_UI_COLOUR),
                             Label(menu_frames[0], bg="#363440", fg="white", font=("Comic Sans", 12, "bold")),
                             Label(menu_frames[0], bg="#363440", fg="white", font=("Comic Sans", 12)),
                             Label(menu_frames[0], bg="#363440", fg="white", font=("Comic Sans", 12)),
                             Label(menu_frames[0], bg="#363440", fg="white", font=("Comic Sans", 12))])

       league_widgets[i][0].place(relx=0, rely=i * 0.028 + 0.105, relwidth=0.005, relheight=0.03)
       league_widgets[i][1].place(relx=0.005, rely=i * 0.028 + 0.105, relwidth=0.025, relheight=0.03)
       league_widgets[i][2].place(relx=0.03, rely=i * 0.028 + 0.105, relwidth=0.035, relheight=0.03)
       league_widgets[i][3].place(relx=0.065, rely=i * 0.028 + 0.105, relwidth=0.11, relheight=0.03)
       league_widgets[i][4].place(relx=0.17, rely=i * 0.028 + 0.105, relwidth=0.04, relheight=0.03)

   # CREATES LEAGUE TABLE ON MATCHES SUBMENU

   def create_league_table():

       for i in [eng_1, eng_2, eng_3, eng_4, fra_1, fra_2, ger_1, ger_2, ita_1, ita_2, spa_1, spa_2]:
           i.sort(key=lambda team: team[0])
           # resets points and matches played
           for j in i:
               j[5] = 0
               j[6] = 0

       if league in [eng_2, eng_3, eng_4, fra_2, ger_2, ita_2, spa_2]:
           promotion_spots = 2
       else:
           promotion_spots = 0

       if league in [eng_2, eng_3, eng_4, fra_2, ger_2, ita_2, spa_2]:
           playoff_spots = 4
       else:
           playoff_spots = 0

       if league in [eng_1, eng_2, fra_1, ger_1, ita_1, spa_1, eng_3]:
           relegation_spots = 3
       else:
           relegation_spots = 0

       if league in [eng_1, ger_1, ita_1, spa_1]:
           european_spots = 5
       elif league == fra_1:
           european_spots = 3
       else:
           european_spots = 0

       for i in league_widgets:
           for j in i:
               j.config(text="", bg=LIGHT_UI_COLOUR)

       for i in range(len(league)):
           if i < promotion_spots:
               pos_bg = "green"
           elif i < promotion_spots + playoff_spots:
               pos_bg = "yellow"
           elif i < european_spots:
               pos_bg = "blue"
           elif len(league) - (i+1) < relegation_spots:
               pos_bg = "red"
           else:
               pos_bg = LIGHT_UI_COLOUR

           league_widgets[i][0].config(bg=pos_bg)
           league_widgets[i][1].config(text=i+1)
           league_widgets[i][2].config(text=league[i][6])
           league_widgets[i][3].config(text=league[i][0])
           league_widgets[i][4].config(text=league[i][5])

   def update_league_table():
       if league in [eng_2, eng_3, fra_2, ger_2, ita_2, spa_2, eng_4]:
           promotion_spots = 2
       else:
           promotion_spots = 0

       if league in [eng_2, eng_3, eng_4, fra_2, ger_2, ita_2, spa_2]:
           playoff_spots = 4
       else:
           playoff_spots = 0

       if league in [eng_1, eng_2, fra_1, ger_1, ita_1, spa_1, eng_3]:
           relegation_spots = 3
       else:
           relegation_spots = 0

       if league in [eng_1, ger_1, ita_1, spa_1]:
           european_spots = 5
       elif league == fra_1:
           european_spots = 3
       else:
           european_spots = 0

       for i in league_widgets:
           for j in i:
               j.config(text="", bg=LIGHT_UI_COLOUR)

       for i in range(len(league)):
           if i < promotion_spots:
               pos_bg = "green"
           elif i < promotion_spots + playoff_spots:
               pos_bg = "yellow"
           elif i < european_spots:
               pos_bg = "blue"
           elif len(league) - (i + 1) < relegation_spots:
               pos_bg = "red"
           else:
               pos_bg = LIGHT_UI_COLOUR

           league_widgets[i][0].config(bg=pos_bg)
           league_widgets[i][1].config(text=i + 1)
           league_widgets[i][2].config(text=league[i][6])
           league_widgets[i][3].config(text=league[i][0])
           league_widgets[i][4].config(text=league[i][5])

   # text is chosen at start of each season depending on league
   league_name_label = Label(menu_frames[0], bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"))
   league_name_label.place(relx=0, rely=0, relwidth=0.21, relheight=0.075)
   # subheadings, pos, games played, name, points
   Label(menu_frames[0], text="Pos", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")).place(relx=0.005, rely=0.075, relwidth=0.025, relheight=0.03)
   Label(menu_frames[0], text="Played", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")).place(relx=0.03, rely=0.075, relwidth=0.035, relheight=0.03)
   Label(menu_frames[0], text="Team", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")).place(relx=0.065, rely=0.075, relwidth=0.11, relheight=0.03)
   Label(menu_frames[0], text="Points", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")).place(relx=0.17, rely=0.075, relwidth=0.04, relheight=0.03)

   Label(menu_frames[0], bg="white").place(relx=0, rely=0.7785, relwidth=0.21, relheight=0.0002)

   Label(menu_frames[0], bg="green").place(relx=0.005, rely=0.78, relwidth=0.005, relheight=0.03)
   Label(menu_frames[0], bg=LIGHT_UI_COLOUR, text="Promotion", fg="white", font=("Comic sans", 12)).place(relx=0.01, rely=0.78, relwidth=0.095, relheight=0.03)
   Label(menu_frames[0], bg="yellow").place(relx=0.105, rely=0.78, relwidth=0.005, relheight=0.03)
   Label(menu_frames[0], bg=LIGHT_UI_COLOUR, text="Playoffs", fg="white", font=("Comic sans", 12)).place(relx=0.11, rely=0.78, relwidth=0.095, relheight=0.03)
   Label(menu_frames[0], bg="blue").place(relx=0.005, rely=0.815, relwidth=0.005, relheight=0.03)
   Label(menu_frames[0], bg=LIGHT_UI_COLOUR, text="European Cup", fg="white", font=("Comic sans", 12)).place(relx=0.01, rely=0.815, relwidth=0.095, relheight=0.03)
   Label(menu_frames[0], bg="red").place(relx=0.105, rely=0.815, relwidth=0.005, relheight=0.03)
   Label(menu_frames[0], bg=LIGHT_UI_COLOUR, text="Relegation", fg="white", font=("Comic sans", 12)).place(relx=0.11, rely=0.815, relwidth=0.095, relheight=0.03)

   if CLUB_COUNTRY == "England":
       STADIUM_CAPACITY = random.randint(4, 7) * 1000
   elif CLUB_COUNTRY == "France":
       STADIUM_CAPACITY = random.randint(9, 14) * 1000
   elif CLUB_COUNTRY == "Germany":
       STADIUM_CAPACITY = random.randint(8, 14) * 1000
   elif CLUB_COUNTRY == "Italy":
       STADIUM_CAPACITY = random.randint(10, 15) * 1000
   elif CLUB_COUNTRY == "Spain":
       STADIUM_CAPACITY = random.randint(10, 14) * 1000
   STADIUM_MAINTAIN_COST = int(STADIUM_CAPACITY / 60)

   # CREATES SQUADLIST FOR SQUAD SUBMENU
   # FRAME NEEDED WITH SCROLLBAR TO MAKE IT SCROLLABLE
   # Create the squadFrame
   squadFrame = Frame(menu_frames[1], background="#3d4659")

   # Create a canvas inside the squadFrame
   canvas = Canvas(squadFrame, background="#3d4659")
   canvas.pack(side=LEFT, fill=BOTH, expand=True)

   # headings for squad content
   Button(menu_frames[1], font=("Comic Sans", 18), text="Name▼", bg="#363440", fg="white", command=sort_squad_name, borderwidth=0).place(relx=0, rely=0, relwidth=0.159, relheight=0.1)
   Label(menu_frames[1], font=("Comic Sans", 18), text="Pos", bg="#26262e", fg="white", borderwidth=0).place(relx=0.159, rely=0, relwidth=0.04, relheight=0.1)
   Button(menu_frames[1], font=("Comic Sans", 18), text="Ovr\n▼", bg="#363440", fg="white", command=sort_squad_ovr, borderwidth=0).place(relx=0.199, rely=0, relwidth=0.035, relheight=0.1)
   Button(menu_frames[1], font=("Comic Sans", 18), text="Best\nPos\n▼", bg="#26262e", fg="white", command=sort_squad_pos, borderwidth=0).place(relx=0.234, rely=0, relwidth=0.04, relheight=0.1)
   Label(menu_frames[1], font=("Comic Sans", 15), text="Fitness/\nsharpness/\nmorale", bg="#363440", fg="white", borderwidth=0).place(relx=0.274, rely=0, relwidth=0.065, relheight=0.1)
   Button(menu_frames[1], font=("Comic Sans", 18), text="Age\n▼", bg="#26262e", fg="white", command=sort_squad_age, borderwidth=0).place(relx=0.339, rely=0, relwidth=0.038, relheight=0.1)
   Button(menu_frames[1], font=("Comic Sans", 18), text="Value\n€..M\n▼", bg="#363440", fg="white", command=sort_squad_value, borderwidth=0).place(relx=0.377, rely=0, relwidth=0.041, relheight=0.1)
   Button(menu_frames[1], font=("Comic Sans", 18), text="Wage\n..K/week\n▼", bg="#26262e", fg="white", command=sort_squad_wage, borderwidth=0).place(relx=0.418, rely=0, relwidth=0.062, relheight=0.1)

   # Dropdown to pick formation
   options = [ "4-4-2 DM", "4-4-2 CM", "4-3-3 CM", "4-3-3 DM", "4-3-2-1 DM", "4-3-2-1 CM", "4-2-3-1 DM", "4-2-3-1 CM", "4-1-2-1-2",
               "3-5-2 CM", "3-5-2 DM", "3-4-2-1 DM", "3-4-2-1 CM", "3-2-4-1", "5-3-2 CM", "5-3-2 DM", "5-2-3 DM", "5-2-3 CM", "5-2-1-2 DM", "5-2-1-2 CM"]

   selected_formation.set("4-3-3 CM")

   def extract_digits(s):
       digits = ''.join(filter(str.isdigit, s))
       return digits

   def extract_digits_with_negative(s):
       value = ""
       for i in s:
           if i.isdigit() or i == "-":
               value += i

       return value

   def reset_formation_view():
       cb.place_forget()
       ldm.place_forget()
       rdm.place_forget()
       dm.place_forget()
       lb.place_forget()
       rb.place_forget()
       lcm.place_forget()
       rcm.place_forget()
       cm.place_forget()
       lam.place_forget()
       ram.place_forget()
       am.place_forget()
       lf.place_forget()
       rf.place_forget()
       cf.place_forget()
       rcf.place_forget()
       lcf.place_forget()

   def set_tactics(in_match_menu):
       global squad_confirmed, starting_goalkeeper, starting_defenders, starting_midfielders, starting_attackers, when_ball_lost, when_ball_won, build_up, attacking_area
       global subs_left
       starting_goalkeeper = None
       starting_defenders = []
       starting_midfielders = []
       starting_attackers = []
       # initially done incase squad is not correct
       if not in_match_menu:
           if simulate_button.cget("text") == "Go to match":
               simulate_button.config(text="Squad Not Confirmed", command=go_to_fortfeit, bg="red")
           squad_confirmed = False
       # used to check if correct amount of positions selected when squad selected
       num_cf = 0
       num_lf = 0
       num_rf = 0
       num_am = 0
       num_cm = 0
       num_dm = 0
       num_lb = 0
       num_rb = 0
       num_cb = 0
       # gets tactic settings as variables
       defence_type = selected_defence.get()
       attacking_width = selected_a_width.get()
       defensive_width = selected_d_width.get()
       playstyle = selected_playstyle.get()
       mentality = selected_mentality.get()

       # 0 == BALANCED, 1 == COUNTER PRESS, 2 == DROP BACK
       when_ball_lost = 0

       # IF button is on, when_ball_lost = Counter press
       if counter_press_button.cget("bg") == "#3F3F4E":
           when_ball_lost = 1

       elif drop_back_button.cget("bg") == "#3F3F4E":
           when_ball_lost = 2

       # 0 == BALANCED, 1 == COUNTER, 2 == HOLD SHAPE
       when_ball_won = 0

       if counter_button.cget("bg") == "#3F3F4E":
           when_ball_won = 1

       elif hold_shape_button.cget("bg") == "#3F3F4E":
           when_ball_won = 2

       # 0 == BALANCED, 1 == DIRECT, 2 == PLAY OUT
       build_up = 0

       if direct_button.cget("bg") == "#3F3F4E":
           build_up = 1

       elif play_out_button.cget("bg") == "#3F3F4E":
           build_up = 2

       # 0 == BALANCED, 1 == WIDE, 2 == CENTRAL
       attacking_area = 0

       if attack_wide_button.cget("bg") == "#3F3F4E":
           attacking_area = 1

       elif attack_centrally_button.cget("bg") == "#3F3F4E":
           attacking_area = 2

       # gets the formation
       formation = selected_formation.get()
       # gets formation with only numbers to determine positions in the formation before going formation by formation
       formation_nums = extract_digits(formation)

       # gets rid of any positions not guaranteed in the new formation
       reset_formation_view()

       # decides placement of defenders
       if formation_nums[0] == "3":
           cb.place(relx=0.58, rely=0.59, relwidth=0.04, relheight=0.07)
           lf.place(relx=0.84, rely=0.44, relwidth=0.04, relheight=0.07)
           rf.place(relx=0.84, rely=0.74, relwidth=0.04, relheight=0.07)
           num_cb = 3
           num_lf = 1
           num_rf = 1
       elif formation_nums[0] == "5":
           cb.place(relx=0.58, rely=0.59, relwidth=0.04, relheight=0.07)
           lb.place(relx=0.63, rely=0.44, relwidth=0.04, relheight=0.07)
           rb.place(relx=0.63, rely=0.74, relwidth=0.04, relheight=0.07)
           num_cb = 3
           num_lb = 1
           num_rb = 1
       elif formation_nums[0] == "4":
           lb.place(relx=0.63, rely=0.44, relwidth=0.04, relheight=0.07)
           rb.place(relx=0.63, rely=0.74, relwidth=0.04, relheight=0.07)
           num_cb = 2
           num_lb = 1
           num_rb = 1

       # decides placement of striker(s)
       if formation_nums[-1] == "2":
           lcf.place(relx=0.9, rely=0.55, relwidth=0.04, relheight=0.07)
           rcf.place(relx=0.9, rely=0.64, relwidth=0.04, relheight=0.07)
           num_cf = 2
       elif formation_nums[-1] == "3":
           cf.place(relx=0.9, rely=0.59, relwidth=0.04, relheight=0.07)
           num_cf = 1
       elif formation_nums[-1] == "1":
           cf.place(relx=0.9, rely=0.59, relwidth=0.04, relheight=0.07)
           num_cf = 1

       # decides if wingers placed or not
       if int(formation_nums[1]) > 3 or formation_nums[-1] == "3":
           lf.place(relx=0.84, rely=0.44, relwidth=0.04, relheight=0.07)
           rf.place(relx=0.84, rely=0.74, relwidth=0.04, relheight=0.07)
           num_lf = 1
           num_rf = 1
       # 4-2-3-1 is an exception to the rules above yet still has wingers so has its own logic
       elif formation == "4-2-3-1 DM" or formation == "4-2-3-1 CM":
           lf.place(relx=0.84, rely=0.44, relwidth=0.04, relheight=0.07)
           rf.place(relx=0.84, rely=0.74, relwidth=0.04, relheight=0.07)
           num_lf = 1
           num_rf = 1

       # places all midfield positions based on formation
       if formation == "4-4-2 DM" or formation == "5-2-3 DM":
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           num_dm = 2

       elif formation == "4-4-2 CM" or formation == "5-2-3 CM":
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           num_cm = 2

       elif formation == "4-3-3 CM" or formation == "3-5-2 CM":
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           dm.place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)
           num_dm = 1
           num_cm = 2

       elif formation == "4-3-3 DM" or formation == "3-5-2 DM":
           cm.place(relx=0.72, rely=0.59, relwidth=0.04, relheight=0.07)
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           num_dm = 2
           num_cm = 1

       elif formation == "4-3-2-1 DM":
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           cm.place(relx=0.72, rely=0.59, relwidth=0.04, relheight=0.07)
           lam.place(relx=0.78, rely=0.55, relwidth=0.04, relheight=0.07)
           ram.place(relx=0.78, rely=0.64, relwidth=0.04, relheight=0.07)
           num_dm = 2
           num_cm = 1
           num_am = 2

       elif formation == "4-3-2-1 CM":
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           dm.place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)
           lam.place(relx=0.78, rely=0.55, relwidth=0.04, relheight=0.07)
           ram.place(relx=0.78, rely=0.64, relwidth=0.04, relheight=0.07)
           num_dm = 1
           num_cm = 2
           num_am = 2

       elif formation == "4-2-3-1 DM" or formation == "5-2-1-2 DM":
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           am.place(relx=0.78, rely=0.59, relwidth=0.04, relheight=0.07)
           num_dm = 2
           num_am = 1

       elif formation == "4-2-3-1 CM" or formation == "5-2-1-2 CM":
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           am.place(relx=0.78, rely=0.59, relwidth=0.04, relheight=0.07)
           num_cm = 2
           num_am = 1

       elif formation == "4-1-2-1-2":
           dm.place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           am.place(relx=0.78, rely=0.59, relwidth=0.04, relheight=0.07)
           num_dm = 1
           num_cm = 2
           num_am = 1

       elif formation == "3-4-2-1 DM":
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           lam.place(relx=0.78, rely=0.55, relwidth=0.04, relheight=0.07)
           ram.place(relx=0.78, rely=0.64, relwidth=0.04, relheight=0.07)
           num_dm = 2
           num_am = 2

       elif formation == "3-4-2-1 CM":
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           lam.place(relx=0.78, rely=0.55, relwidth=0.04, relheight=0.07)
           ram.place(relx=0.78, rely=0.64, relwidth=0.04, relheight=0.07)
           num_cm = 2
           num_am = 2

       elif formation == "3-2-4-1":
           ldm.place(relx=0.67, rely=0.55, relwidth=0.04, relheight=0.07)
           rdm.place(relx=0.67, rely=0.64, relwidth=0.04, relheight=0.07)
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           num_dm = 2
           num_cm = 2

       elif formation == "5-3-2 CM":
           cm.place(relx=0.72, rely=0.59, relwidth=0.04, relheight=0.07)
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           num_cm = 3

       elif formation == "5-3-2 DM":
           dm.place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)
           lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
           rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
           num_dm = 1
           num_cm = 2

       if not in_match_menu:
           squad_size_label.config(text=f"Current Squad Size: {len(squad)}")
       get_team_stats()

       actual_num_gk = 0
       actual_num_lb = 0
       actual_num_cb = 0
       actual_num_rb = 0
       actual_num_dm = 0
       actual_num_cm = 0
       actual_num_am = 0
       actual_num_lf = 0
       actual_num_rf = 0
       actual_num_cf = 0

       for i in squad:
           if i.selected_position.get() == "GK":
               actual_num_gk += 1
               starting_goalkeeper = i
           elif i.selected_position.get() == "LB":
               actual_num_lb += 1
               starting_defenders.append(i)
           elif i.selected_position.get() == "CB":
               actual_num_cb += 1
               starting_defenders.append(i)
           elif i.selected_position.get() == "RB":
               actual_num_rb += 1
               starting_defenders.append(i)
           elif i.selected_position.get() == "DM":
               actual_num_dm += 1
               starting_midfielders.append(i)
           elif i.selected_position.get() == "CM":
               actual_num_cm += 1
               starting_midfielders.append(i)
           elif i.selected_position.get() == "AM":
               actual_num_am += 1
               starting_midfielders.append(i)
           elif i.selected_position.get() == "LF":
               actual_num_lf += 1
               starting_attackers.append(i)
           elif i.selected_position.get() == "CF":
               actual_num_cf += 1
               starting_attackers.append(i)
           elif i.selected_position.get() == "RF":
               actual_num_rf += 1
               starting_attackers.append(i)

       num_starting_players = actual_num_gk + actual_num_lb + actual_num_rb + actual_num_cb + actual_num_dm + actual_num_cm + actual_num_am + actual_num_lf + actual_num_cf + actual_num_rf

       injured_player_starting = False
       if num_starting_players > 11:
           set_tactics_button.config(bg="red", text="Too Many\nPlayers Picked")
       elif num_starting_players < 11:
           set_tactics_button.config(bg="red", text="Not Enough\nPlayers Picked")
       else:
           if actual_num_gk != 1:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of GKs")
           elif actual_num_lb != num_lb:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of LBs")
           elif actual_num_rb != num_rb:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of RBs")
           elif actual_num_cb != num_cb:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of CBs")
           elif actual_num_dm != num_dm:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of DMs")
           elif actual_num_cm != num_cm:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of CMs")
           elif actual_num_am != num_am:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of AMs")
           elif actual_num_lf != num_lf:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of LFs")
           elif actual_num_rf != num_rf:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of RFs")
           elif actual_num_cf != num_cf:
               set_tactics_button.config(bg="red", text="Incorrect\nAmount Of CFs")
           else:
               if starting_goalkeeper.injured > 0:
                   injured_player_starting = True
               for i in starting_defenders:
                   if i.injured > 0:
                       injured_player_starting = True
               for i in starting_midfielders:
                   if i.injured > 0:
                       injured_player_starting = True
               for i in starting_attackers:
                   if i.injured > 0:
                       injured_player_starting = True
               if injured_player_starting:
                   set_tactics_button.config(bg="red", text="Can't Start\nInjured Players")
               else:
                   if not in_match_menu:
                       if simulate_button.cget("text") == "Squad Not Confirmed":
                           set_tactics_button.config(bg="green", text="Squad And Tactics\nConfirmed")
                           squad_confirmed = True
                           simulate_button.config(text="Go to match", command=enter_match, bg=BUTTON_COLOUR)
                           for i in squad:
                               i.actual_position.set(i.selected_position.get())
                       else:
                           set_tactics_button.config(bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
                   else:
                       theoretical_subs_left = subs_left
                       if starting_goalkeeper.actual_position.get() == "SUB":
                           theoretical_subs_left -= 1
                       for i in starting_defenders:
                           if i.actual_position.get() == "SUB":
                               theoretical_subs_left -= 1
                       for i in starting_midfielders:
                           if i.actual_position.get() == "SUB":
                               theoretical_subs_left -= 1
                       for i in starting_attackers:
                           if i.actual_position.get() == "SUB":
                               theoretical_subs_left -= 1

                       if theoretical_subs_left < 0:
                           set_tactics_button.config(text="Too Many\nSubs Used", bg="red")
                       else:
                           subs_left = theoretical_subs_left
                           squad_size_label.config(text=f"Subs Left: {subs_left}")
                           set_tactics_button.config(bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
                           for i in squad:
                               i.actual_position.set(i.selected_position.get())

   def counter_press_on():
       # if button is already on, turn it off, else turn it on and turn drop back off
       if counter_press_button.cget("background") == "#3F3F4E":
           counter_press_button.configure(background="#26262e")
       else:
           counter_press_button.configure(background="#3F3F4E")
           drop_back_button.configure(background="#26262e")

   def drop_back_on():
       # if button is already on, turn it off, else turn it on and turn counter press off
       if drop_back_button.cget("background") == "#3F3F4E":
           drop_back_button.configure(background="#26262e")
       else:
           drop_back_button.configure(background="#3F3F4E")
           counter_press_button.configure(background="#26262e")

   def counter_on():
       if counter_button.cget("background") == "#3F3F4E":
           counter_button.configure(background="#26262e")
       else:
           counter_button.configure(background="#3F3F4E")
           hold_shape_button.configure(background="#26262e")

   def hold_shape_on():
       if hold_shape_button.cget("background") == "#3F3F4E":
           hold_shape_button.configure(background="#26262e")
       else:
           hold_shape_button.configure(background="#3F3F4E")
           counter_button.configure(background="#26262e")

   def direct_build_up_on():
       if direct_button.cget("background") == "#3F3F4E":
           direct_button.configure(background="#26262e")
       else:
           direct_button.configure(background="#3F3F4E")
           play_out_button.configure(background="#26262e")

   def play_out_on():
       if play_out_button.cget("background") == "#3F3F4E":
           play_out_button.configure(background="#26262e")
       else:
           play_out_button.configure(background="#3F3F4E")
           direct_button.configure(background="#26262e")

   def wide_attack_on():
       if attack_wide_button.cget("background") == "#3F3F4E":
           attack_wide_button.configure(background="#26262e")
       else:
           attack_wide_button.configure(background="#3F3F4E")
           attack_centrally_button.configure(background="#26262e")

   def central_attack_on():
       if attack_centrally_button.cget("background") == "#3F3F4E":
           attack_centrally_button.configure(background="#26262e")
       else:
           attack_centrally_button.configure(background="#3F3F4E")
           attack_wide_button.configure(background="#26262e")

   global squad_size_label
   # tactics background label
   Label(menu_frames[1], bg="#363440").place(relx=0.5, rely=0.03, relwidth=0.48, relheight=0.36)

   # squad size info
   Label(menu_frames[1], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=f"Min squad size: {MIN_SQUAD_SIZE}\nMax squad size: {MAX_SQUAD_SIZE}").place(relx=0.818, rely=0.33, relwidth=0.15, relheight=0.06)
   squad_size_label = Label(menu_frames[1], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=f"Current Squad Size: {len(squad)}")
   squad_size_label.place(relx=0.51, rely=0.33, relwidth=0.15, relheight=0.06)

   # headings to show different parts of the tactic screen
   Label(menu_frames[1], text="Formation", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.51, rely=0.03, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Team Playstyle", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.51, rely=0.13, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Team Mentality", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.51, rely=0.23, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="When Ball Is Lost", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.635, rely=0.04, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="When Ball Is Won", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.635, rely=0.18, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Build Up Type", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.755, rely=0.04, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Attacking Area", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.755, rely=0.18, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Defensive Style", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.87, rely=0.03, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Attacking Width", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.87, rely=0.13, relwidth=0.1, relheight=0.04)
   Label(menu_frames[1], text="Defensive Width", bg="#363440", font=("Comic Sans", 12), fg="white").place(relx=0.87, rely=0.23, relwidth=0.1, relheight=0.04)

   # formation pick option menu
   formation_pick = OptionMenu(menu_frames[1], selected_formation, *options)
   formation_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   formation_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
   formation_pick.place(relx=0.51, rely=0.07, relwidth=0.1, relheight=0.05)

   # used to cover playstyle pick during matches
   playstyle_cover_label = Label(menu_frames[1], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14, "bold"), text="")

   # team playstyle option menu variables
   playstyles = ["None", "Gegenpress", "Tiki Taka", "Counter Attack", "Route One", "Park The Bus", "Wing Play"]
   selected_playstyle = StringVar()
   selected_playstyle.set("None")

   # team playstyle option menu
   playstyle_pick = OptionMenu(menu_frames[1], selected_playstyle, *playstyles)
   playstyle_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   playstyle_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
   playstyle_pick.place(relx=0.51, rely=0.17, relwidth=0.1, relheight=0.05)

   # team mentality option menu variables
   mentalities = ["Very Defensive", "Defensive", "Balanced", "Attacking", "Very Attacking"]
   selected_mentality = StringVar()
   selected_mentality.set("Balanced")

   # team mentality option menu
   mentality_pick = OptionMenu(menu_frames[1], selected_mentality, *mentalities)
   mentality_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   mentality_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
   mentality_pick.place(relx=0.51, rely=0.27, relwidth=0.1, relheight=0.05)

   # options to counter press or regroup
   # counter-press button
   counter_press_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Counter Press", command=counter_press_on, borderwidth=0)
   counter_press_button.place(relx=0.635, rely=0.08, relwidth=0.1, relheight=0.05)
   # drop back button
   drop_back_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Drop Back", command=drop_back_on, borderwidth=0)
   drop_back_button.place(relx=0.635, rely=0.13, relwidth=0.1, relheight=0.05)

   # options to counter or hold shape
   # counter button
   counter_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Counter", command=counter_on, borderwidth=0)
   counter_button.place(relx=0.635, rely=0.22, relwidth=0.1, relheight=0.05)
   # hold shape button
   hold_shape_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Hold Shape", command=hold_shape_on, borderwidth=0)
   hold_shape_button.place(relx=0.635, rely=0.27, relwidth=0.1, relheight=0.05)

   # options for build up phase
   # direct build up button
   direct_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Direct Long Balls", command=direct_build_up_on, borderwidth=0)
   direct_button.place(relx=0.755, rely=0.08, relwidth=0.1, relheight=0.05)
   # play out button
   play_out_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Play Out Of Defence", command=play_out_on, borderwidth=0)
   play_out_button.place(relx=0.755, rely=0.13, relwidth=0.1, relheight=0.05)

   # attack wide or centrally buttons
   # attack wide button
   attack_wide_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Wide", command=wide_attack_on, borderwidth=0)
   attack_wide_button.place(relx=0.755, rely=0.22, relwidth=0.1, relheight=0.05)
   # attack centrally button
   attack_centrally_button = Button(menu_frames[1], font=("Comic Sans", 11), bg="#26262e", fg="white", text="Central", command=central_attack_on, borderwidth=0)
   attack_centrally_button.place(relx=0.755, rely=0.27, relwidth=0.1, relheight=0.05)

   # defending style option menu variables
   defence_types = ["High Press", "Mid Block", "Low Block"]
   selected_defence = StringVar()
   selected_defence.set("Mid Block")

   # defending style option menu
   defence_pick = OptionMenu(menu_frames[1], selected_defence, *defence_types)
   defence_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   defence_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
   defence_pick.place(relx=0.87, rely=0.07, relwidth=0.1, relheight=0.05)

   # attacking widths option menu variables
   a_widths = ["Balanced", "Narrow", "Wide"]
   selected_a_width = StringVar()
   selected_a_width.set("Balanced")

   # attacking widths option menu
   a_width_pick = OptionMenu(menu_frames[1], selected_a_width, *a_widths)
   a_width_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   a_width_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
   a_width_pick.place(relx=0.87, rely=0.17, relwidth=0.1, relheight=0.05)

   # defensive widths option menu variables
   d_widths = ["Balanced", "Narrow", "Wide"]
   selected_d_width = StringVar()
   selected_d_width.set("Balanced")

   # attacking widths option menu
   d_width_pick = OptionMenu(menu_frames[1], selected_d_width, *d_widths)
   d_width_pick.configure(background="#26262e", foreground="white", borderwidth=0)
   d_width_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
   d_width_pick.place(relx=0.87, rely=0.27, relwidth=0.1, relheight=0.05)

   # button to set tactics
   set_tactics_button = Button(menu_frames[1], bg="#2482d3", fg="white", text="Confirm Tactics\nAnd Squad", font=("comic sans", 14), command=lambda: set_tactics(False))
   set_tactics_button.place(relx=0.665, rely=0.33, relwidth=0.15, relheight=0.06)

   # Create a scrollbar for the canvas
   squadScroll = Scrollbar(squadFrame, command=canvas.yview, background="#26262e")
   squadScroll.pack(side=RIGHT, fill=Y)

   # Configure the canvas to work with the scrollbar
   canvas.configure(yscrollcommand=squadScroll.set)

   # Create a frame to hold the content of the squad
   squadContent = Frame(canvas, background="#3d4659")

   player_names_background = Label(squadContent, bg="#363440", width=17, height=40, font=("Comic Sans", 18))
   player_names_background.grid(row=0, column=0, rowspan=len(squad)+1)

   def transfer_list_player(player_object):
       global transfer_listed_players
       if player_transfer_list_check.cget("bg") == "#26262e":
           player_transfer_list_check.configure(bg="#3F3F4E")
           player_object.is_transfer_listed = True
           transfer_listed_players.append(player_object)
       else:
           player_transfer_list_check.configure(bg="#26262e")
           player_object.is_transfer_listed = False
           if player_object in transfer_listed_players:
               transfer_listed_players.remove(player_object)

   def get_team_stats():
       global team_attack_avg, team_midfield_avg, team_defence_avg
       attackers = []
       team_attack_avg = 0
       midfielders = []
       team_midfield_avg = 0
       defenders = []
       team_defence_avg = 0
       goalkeepers = []
       # store attackers, midfielders and defenders seperately
       for i in squad:
           if i.pos in ["LF", "RF", "CF"]:
               attackers.append(i.ovr)
           elif i.pos in ["DM", "CM", "AM"]:
               midfielders.append(i.ovr)
           elif i.pos in ["LB", "RB", "CB"]:
               defenders.append(i.ovr)
           elif i.pos == "GK":
               goalkeepers.append(i.ovr)

       # order each list by overall
       attackers = sorted(attackers, reverse=True)
       midfielders = sorted(midfielders, reverse=True)
       defenders = sorted(defenders, reverse=True)
       goalkeepers = sorted(goalkeepers, reverse=True)

       if len(attackers) > 6:
           team_attack_depth.config(text="Good Depth", fg="green")
       elif len(attackers) < 4:
           team_attack_depth.config(text="Low Depth", fg="red")
       else:
           team_attack_depth.config(text="Medium Depth", fg="yellow")

       if len(midfielders) > 6:
           team_midfield_depth.config(text="Good Depth", fg="green")
       elif len(midfielders) < 4:
           team_midfield_depth.config(text="Low Depth", fg="red")
       else:
           team_midfield_depth.config(text="Medium Depth", fg="yellow")

       if len(defenders) > 6:
           team_defence_depth.config(text="Good Depth", fg="green")
       elif len(defenders) < 5:
           team_defence_depth.config(text="Low Depth", fg="red")
       else:
           team_defence_depth.config(text="Medium Depth", fg="yellow")

       if len(goalkeepers) > 2:
           team_goalkeepers_depth.config(text="Good Depth", fg="green")
       elif len(goalkeepers) < 2:
           team_goalkeepers_depth.config(text="Low Depth", fg="red")
       else:
           team_goalkeepers_depth.config(text="Medium Depth", fg="yellow")

       # get best possible starting players by getting the formation and picking the best players that fit into the 11
       formation = extract_digits(selected_formation.get())
       attackers = attackers[:int(formation[-1])]
       defenders = defenders[:int(formation[0])]
       num_midfielders = 10 - int(formation[0]) - int(formation[-1])
       midfielders = midfielders[:num_midfielders]
       goalkeepers = goalkeepers[0]

       # gets averages for attack midfield and defence
       for i in attackers:
           team_attack_avg += i
       team_attack_avg = int(team_attack_avg / len(attackers))

       for i in midfielders:
           team_midfield_avg += i
       team_midfield_avg = int(team_midfield_avg / len(midfielders))

       for i in defenders:
           team_defence_avg += i
       team_defence_avg = int(team_defence_avg / len(defenders))

       league_goalkeeper_avg = 0
       league_defence_avg = 0
       league_midfield_avg = 0
       league_attack_avg = 0
       for team in league:
           league_attack_avg += team[1]
           league_defence_avg += team[2]
       league_midfield_avg = league_attack_avg + league_defence_avg

       league_attack_avg = int(league_attack_avg / len(league))
       league_defence_avg = int(league_defence_avg / len(league))
       league_midfield_avg = int(league_midfield_avg / (len(league) * 2))
       league_goalkeeper_avg = league_midfield_avg

       print(f"LEAGUE AVG {league_goalkeeper_avg} {league_defence_avg} {league_midfield_avg} {league_attack_avg}")

       if goalkeepers - league_goalkeeper_avg > 1:
           team_goalkeepers_quality.config(text="Good Quality", fg="green")
       elif goalkeepers - league_goalkeeper_avg < -3:
           team_goalkeepers_quality.config(text="Low Quality", fg="red")
       else:
           team_goalkeepers_quality.config(text="Medium Quality", fg="yellow")

       if team_defence_avg - league_defence_avg > 1:
           team_defence_quality.config(text="Good Quality", fg="green")
       elif team_defence_avg - league_defence_avg < -3:
           team_defence_quality.config(text="Low Quality", fg="red")
       else:
           team_defence_quality.config(text="Medium Quality", fg="yellow")

       if team_midfield_avg - league_midfield_avg > 1:
           team_midfield_quality.config(text="Good Quality", fg="green")
       elif team_midfield_avg - league_midfield_avg < -3:
           team_midfield_quality.config(text="Low Quality", fg="red")
       else:
           team_midfield_quality.config(text="Medium Quality", fg="yellow")

       if team_attack_avg - league_attack_avg > 1:
           team_attack_quality.config(text="Good Quality", fg="green")
       elif team_attack_avg - league_attack_avg < -3:
           team_attack_quality.config(text="Low Quality", fg="red")
       else:
           team_attack_quality.config(text="Medium Quality", fg="yellow")

       calc_opponent_strength()

       print("TEAM STATS")
       print(team_attack_avg, team_midfield_avg, team_defence_avg)

   # NEGOTIATIONS WIDGETS
   negotiation_phase_title = Label(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16, "bold"), text="")
   negotiation_phase_title.place(relx=0.02, rely=0.55, relwidth=0.225, relheight=0.05)
   negotiation_offer_label = Label(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text="")
   negotiation_offer_label.place(relx=0.02, rely=0.62, relwidth=0.225, relheight=0.06)
   more_button = Button(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18), text="", bd=0, state="disabled", activebackground=BUTTON_COLOUR, activeforeground="white", command=lambda: print("Click"))
   more_button.place(relx=0.036, rely=0.7, relwidth=0.0915, relheight=0.04)
   less_button = Button(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18), text="", bd=0, state="disabled", activebackground=BUTTON_COLOUR, activeforeground="white")
   less_button.place(relx=0.1375, rely=0.7, relwidth=0.0915, relheight=0.04)
   confirm_offer_button = Button(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18), text="", bd=0, state="disabled", activebackground=BUTTON_COLOUR, activeforeground="white")
   confirm_offer_button.place(relx=0.036, rely=0.76, relwidth=0.193, relheight=0.04)
   renegotiate_wage_button = Button(menu_frames[5], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18), text="", activebackground=BUTTON_COLOUR, activeforeground="white", bd=0, state="disabled")
   renegotiate_wage_button.place(relx=0.036, rely=0.7, relwidth=0.193, relheight=0.04)
   negotiation_labels = [negotiation_phase_title, negotiation_offer_label]
   negotiation_buttons = [more_button, less_button, confirm_offer_button, renegotiate_wage_button]

   def add_player_to_squad(player):
       global all_squad_labels, squad_position_vars

       player.sharpness = 50
       squad.append(player)
       player.selected_position.set("SUB")

       # decides which list to use for the dropdown based on if the player is a gk or not
       if player.pos == "GK":
           option_list = options2
       else:
           option_list = options1

       sharpness_colour = get_color_based_on_value(player.sharpness)
       fitness_colour = get_color_based_on_value(player.fitness)
       morale_colour = get_color_based_on_morale(player.morale)

       # Create labels for player information if they do not exist
       labels = [
           Button(squadContent, text=f"{player.first_name} {player.last_name}", bg="#363440", fg="white",
                  font=("Comic Sans", round(window.winfo_screenwidth() / 100)), padx=10, borderwidth=0,
                  command=lambda p=player: display_player_info(p),
                  width=round(SCREEN_WIDTH * 0.01)),

           OptionMenu(squadContent, player.selected_position, *option_list),

           Label(squadContent, text=player.ovr, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                 padx=10, width=round(SCREEN_WIDTH * 0.001)),

           Label(squadContent, text=player.pos, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                 padx=10, width=round(SCREEN_WIDTH * 0.001)),

           Label(squadContent, bg=fitness_colour, width=round(SCREEN_WIDTH * 0.001)),
           # makes space between labels
           Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005)),

           Label(squadContent, bg=sharpness_colour, width=round(SCREEN_WIDTH * 0.001)),
           # makes space between labels
           Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005)),

           Label(squadContent, bg=morale_colour, width=round(SCREEN_WIDTH * 0.001)),

           Label(squadContent, text=player.age, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                 padx=round(SCREEN_WIDTH * 0.001), width=round(SCREEN_WIDTH * 0.0025)),
           Label(squadContent, text=player.getValue(), bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                 padx=round(SCREEN_WIDTH * 0.0005), width=round(SCREEN_WIDTH * 0.002)),
           Label(squadContent, text=player.wage, bg="#3d4659", fg="white", font=("Comic Sans", round(window.winfo_screenwidth() / 70)),
                 padx=round(SCREEN_WIDTH * 0.0005), width=round(SCREEN_WIDTH * 0.003))
       ]

       # configures option menu appearance
       labels[1].config(background="#26262e", foreground="white", highlightthickness=0, font=("Comic Sans", round(window.winfo_screenwidth() / 200)))
       labels[1]["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", round(window.winfo_screenwidth() / 114)))

       # Add the new player's labels to the all_squad_labels list
       all_squad_labels.append(labels)
       squad_position_vars.append(player.selected_position)

       # Update squad display with the new player
       update_squad_display()
       update_youth_frames()
       update_scout_one_frames()
       update_scout_two_frames()
       update_scout_three_frames()

       sort_squad_name()
       player_names_background.grid_forget()
       player_names_background.grid(row=0, column=0, rowspan=len(squad) + 1)

       get_team_avg_rating()
       get_team_stats()
       squad_size_label.config(text=f"Current Squad Size: {len(squad)}")

   def negotiate_player_sale(player_object, offer_value):
       global player_sale_negotiation_attempts

       player_sale_negotiation_attempts = 3
       change_menu(5)

       def renegotiate_transfer_offer():
           global player_sale_negotiation_attempts
           nonlocal offer_value
           player_sale_negotiation_attempts -= 1
           offer_value = int(offer_value * (random.randint(95, 105) / 100))
           negotiation_offer_label.config(text="€{:,}".format(offer_value))
           if player_sale_negotiation_attempts == 0:
               renegotiate_wage_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")

       def confirm_sale():
           squad.remove(player_object)
           transfer_listed_players.remove(player_object)
           add_profit(int(extract_digits(negotiation_offer_label.cget("text"))), sales_income_label, True)
           for i in negotiation_labels:
               i.config(text="")
           for i in negotiation_buttons:
               i.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")
           for child in transfer_offer_frame.winfo_children():
               child.destroy()
           get_wage_costs()
           update_budget_labels()
           update_squad_display()
           get_team_stats()
           display_player_info(squad[0])

       negotiation_phase_title.config(text="Transfer Offer")
       negotiation_offer_label.config(text="€{:,}".format(offer_value))
       renegotiate_wage_button.config(text="Renegotiate", bg=BUTTON_COLOUR, state="active", command=renegotiate_transfer_offer)
       renegotiate_wage_button.lift()
       confirm_offer_button.config(text="Accept", bg=BUTTON_COLOUR, state="active", command=confirm_sale, activebackground=BUTTON_COLOUR)

   def negotiate_player_contract(player_object):
       global prev_player_negotiation, wage_renegotiation_attempts

       wage_renegotiation_attempts = 3

       def confirm_extension():
           global current_wage_offer
           # updates player contract length and wage
           is_youth_player = False
           is_scouted_player = False
           if player_object.contract_expire == 0:
               is_youth_player = True
           if player_object in scout_one_players or player_object in scout_two_players or player_object in scout_three_players:
               is_scouted_player = True
           player_object.contract_expire = int(extension_offer)
           player_object.wage = round(current_wage_offer / 1000.0, 2)
           # sets players initial extension offer to their new contract length to avoid extra negotiations ocurring for the rest of the season
           player_object.extension_offer = int(extension_offer)
           for i in negotiation_labels:
               i.config(text="")
           for i in negotiation_buttons:
               i.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")

           if is_youth_player:
               youth_players.remove(player_object)
               add_player_to_squad(player_object)
               update_youth_frames()

           if is_scouted_player:
               if player_object in scout_one_players:
                   scout_one_players.remove(player_object)
                   update_scout_one_frames()
               elif player_object in scout_two_players:
                   scout_two_players.remove(player_object)
                   update_scout_two_frames()
               elif player_object in scout_three_players:
                   scout_three_players.remove(player_object)
                   update_scout_three_frames()

               add_loss(current_transfer_offer, transfer_loss_label, True)
               add_player_to_squad(player_object)

           get_wage_costs()
           update_budget_labels()
           update_morale()

           display_player_info(player_object)
           update_squad_display()

       def wage_negotiation():
           global current_wage_offer
           # updates labels for wage negotiation
           negotiation_phase_title.config(text="Wage Negotiation")
           more_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")
           less_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")

           # gets an opening wage offer and players current wage
           current_wage_offer = special_round(player_object.get_wage_offer() * 1000, 1)
           current_player_wage = special_round(player_object.wage * 1000, 1)

           renegotiate_wage_button.config(text="Renegotiate", bg=BUTTON_COLOUR, state="active", command=renegotiate_wage)
           renegotiate_wage_button.lift()
           if wage_budget >= current_wage_offer:
               confirm_offer_button.config(command=confirm_extension, text="Confirm", bg=BUTTON_COLOUR, activebackground=BUTTON_COLOUR)
           else:
               print("Insufficient budget")
               confirm_offer_button.config(command=print, text="Insufficient budget for offer", bg=DARK_UI_COLOUR, activebackground=DARK_UI_COLOUR)
               #confirm_offer_button.config(command=confirm_extension, text="Confirm", bg=BUTTON_COLOUR, activebackground=BUTTON_COLOUR)

           # shows message of players wage offer and how it compares to their old wage
           if current_wage_offer > current_player_wage:
               negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\n€{:,} more than current wage".format(current_wage_offer - current_player_wage)))
           elif current_wage_offer < current_player_wage:
               negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\n€{:,} less than current wage".format(current_player_wage - current_wage_offer)))
           else:
               negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\nSame as current wage"))
       # between 2% and 7% change
       def renegotiate_wage():
           global current_wage_offer, wage_renegotiation_attempts
           wage_renegotiation_attempts -= 1
           current_player_wage = special_round(player_object.wage * 1000, 1)
           if random.randint(2, 100) % 2 == 0:
               # decreases wage offer by between 2% to 7%
               current_wage_offer = special_round(current_wage_offer * (random.randint(93, 98)/100), 1)
           else:
               # increases wage offer by between 2% to 7%
               current_wage_offer = special_round(current_wage_offer * (random.randint(102, 107) / 100), 1)

           if wage_budget >= current_wage_offer:
               confirm_offer_button.config(command=confirm_extension, text="Confirm", bg=BUTTON_COLOUR, activebackground=BUTTON_COLOUR)
           else:
               confirm_offer_button.config(command=print, text="Insufficient budget for offer", bg=DARK_UI_COLOUR, activebackground=DARK_UI_COLOUR)

           if current_wage_offer > current_player_wage:
                   negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\n€{:,} more than current wage".format(current_wage_offer - current_player_wage)))

           elif current_wage_offer < current_player_wage:
               negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\n€{:,} less than current wage".format(current_player_wage - current_wage_offer)))
           else:
               negotiation_offer_label.config(text="€{:,} per week".format(current_wage_offer) + ("\nSame as current wage"))

           if wage_renegotiation_attempts == 0:
               renegotiate_wage_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")

       def attempt_increase_length():
           nonlocal extension_offer
           if player_object.age > 31 or non_wage_happiness < 50:
               negotiation_phase_title.config(text="Player unwilling to negotiate")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
           elif random.randint(1,100) < 60:
               if player_object.age > 25 and not player_object.extension_offer > year + 4:
                   extension_offer += random.randint(1, 2)
               else:
                   extension_offer += 1

               if player_object in squad:
                   negotiation_offer_label.config(text=f"{extension_offer}\n({extension_offer - player_object.contract_expire} year extension)")
               else:
                   negotiation_offer_label.config(text=f"{extension_offer}")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")

           else:
               negotiation_phase_title.config(text="Player unwilling to negotiate")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")

       def attempt_decrease_length():
           nonlocal extension_offer
           if extension_offer <= year + 2:
               negotiation_phase_title.config(text="Player unwilling to negotiate")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
           elif random.randint(1,100) < 65:
               extension_offer -= random.randint(1,2)
               if extension_offer < player_object.contract_expire:
                   extension_offer = player_object.contract_expire

               if player_object in squad:
                   negotiation_offer_label.config(text=f"{extension_offer}\n({extension_offer - player_object.contract_expire} year extension)")
               else:
                   negotiation_offer_label.config(text=f"{extension_offer}")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")

           else:
               negotiation_phase_title.config(text="Player unwilling to negotiate")
               more_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")
               less_button.config(state="disabled", bg=LIGHT_UI_COLOUR, text="")

       def skip_length_negotiation():
           extension_offer = player_object.contract_expire
           wage_negotiation()

       def contract_length_offer():
           renegotiate_wage_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")
           negotiation_phase_title.config(text="Contract Length Offer")
           if player_object in squad:
               negotiation_offer_label.config(text=f"{extension_offer}\n({extension_offer - player_object.contract_expire} year extension)")
           else:
               negotiation_offer_label.config(text=f"{extension_offer}")
           more_button.config(text="More", bg=BUTTON_COLOUR, state="active", command=attempt_increase_length)
           less_button.config(text="Less", bg=BUTTON_COLOUR, state="active", command=attempt_decrease_length)
           more_button.lift()
           less_button.lift()
           confirm_offer_button.config(text="Accept", bg=BUTTON_COLOUR, state="active", command=wage_negotiation, activebackground=BUTTON_COLOUR)

       def renegotiate_transfer_offer():
           global transfer_renegotiation_attempts, current_transfer_offer
           transfer_renegotiation_attempts -= 1

           current_transfer_offer = int(current_transfer_offer * (random.randint(965, 1035)/1000))
           negotiation_offer_label.config(text="€{:,}".format(current_transfer_offer))

           if transfer_renegotiation_attempts == 0:
               renegotiate_wage_button.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")

       def transfer_negotiation():
           global current_transfer_offer, transfer_renegotiation_attempts
           transfer_renegotiation_attempts = 3
           negotiation_phase_title.config(text="Transfer Offer")
           current_transfer_offer = int(player_object.getValue()*1000000*(random.randint(95, 105)/100))
           negotiation_offer_label.config(text="€{:,}".format(current_transfer_offer))
           renegotiate_wage_button.config(text="Renegotiate", bg=BUTTON_COLOUR, state="active", command=renegotiate_transfer_offer)
           renegotiate_wage_button.lift()
           confirm_offer_button.config(text="Accept", bg=BUTTON_COLOUR, state="active", command=contract_length_offer, activebackground=BUTTON_COLOUR)

       change_menu(5)
       # remembers previous player who was negotiated with, so if it gets interrupted by the player opening new negotiations, can still create negotiation cooldown for player
       if prev_player_negotiation is not None and prev_player_negotiation != player_object:
           prev_player_negotiation.negotiation_cooldown = 14
       for i in negotiation_labels:
           i.lift()
           i.config(text="")
       for i in negotiation_buttons:
           i.lift()
           i.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")
       # gets happiness not including wage happiness, avoids player saying no to negotiation because of bad wage when you are trying to improve it
       non_wage_happiness = int((player_object.club_happiness + player_object.training_happiness + player_object.playing_time) / 3)

       if player_object.negotiation_cooldown != 0:
           negotiation_offer_label.config(text=f"Player was recently in negotiations\nTry again in {player_object.negotiation_cooldown} " + ("days" if player_object.negotiation_cooldown > 1 else "day"))
           print(player_object.negotiation_cooldown)
           prev_player_negotiation = None
           return

       player_object.negotiation_cooldown = 14

       if non_wage_happiness < 50:
           # put label saying player not happy enough to negotiate a new contract
           negotiation_offer_label.config(text="The player is too unhappy\nto extend right now")
           confirm_offer_button.config(text="Negotiate new wage", bg=BUTTON_COLOUR, state="active", command=skip_length_negotiation)
           return
       # decides starting wage offer, calculated ontop of current year so it can then be decided whether the player wants to extend or not based on their current contract length
       # use non_wage_happiness for wage, use morale from player object for contract expiry date
       extension_offer = player_object.extension_offer

       # if the players initial extension offer is not greater than their current contract length, they will say they dont want to extend at the moment but only if the player is in the squad so not transfer offer
       if extension_offer <= player_object.contract_expire  and player_object in squad:
           negotiation_offer_label.config(text="The player thinks his current\ncontract is long enough for now")
           confirm_offer_button.config(text="Negotiate new wage", bg=BUTTON_COLOUR, state="active", command=skip_length_negotiation, activebackground=BUTTON_COLOUR)
           return

       prev_player_negotiation = player_object

       # if player is willing to extend and is already in the squad, updates labels with inital contract length offer
       if player_object in squad or player_object in youth_players:
           contract_length_offer()
       else:
           transfer_negotiation()

   def display_player_info(player_object):
       global club_happiness_label, squad_happiness_label, playtime_happiness_label, wage_happiness_label
       player_ovr = player_object.ovr
       player_pos = player_object.pos
       player_expiry = player_object.contract_expire
       player_name = f"{player_object.first_name} {player_object.last_name}"
       # checks if the messages related to releasing players is placed and exists then hides them when switching between player infos to stop overlapping
       if release_bg is not None and release_bg.winfo_ismapped():
           release_bg.place_forget()
           release_cancel_button.place_forget()
           release_confirm_button.place_forget()

       if squad_size_message is not None and squad_size_message.winfo_ismapped():
           squad_size_message.place_forget()
           squad_size_confirm.place_forget()

       if gk_num_message is not None and gk_num_message.winfo_ismapped():
           gk_num_message.place_forget()
           gk_num_confirm.place_forget()

       if player_object.injured > 0:
           player_detail.config(text=f"Player injured for {player_object.injured} days")
       else:
           player_detail.config(text="Player available for selection")

       player_name_info.configure(text=player_name)
       player_ovr_info.configure(text=player_ovr)
       player_pos_info.configure(text=player_pos)
       player_expire_info.configure(text="Contract Expires:")
       player_expire_date.configure(text=player_expiry)
       player_contract_button.configure(bg="#26262e", text="Negotiate New Contract", command=lambda: negotiate_player_contract(player_object))
       player_transfer_list_check.configure(bg="#3F3F4E" if player_object.is_transfer_listed else "#26262e", text="Transfer List Player", command=lambda: transfer_list_player(player_object))
       player_release_button.configure(bg="#26262e", text="Release Player", command=lambda: player_object.release_player(display_player_info))
       Label(menu_frames[1], text="Club Level", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)).place(relx=0.12, rely=0.72, relwidth=0.1, relheight=0.03)
       Label(menu_frames[1], text="Length of Training", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)).place(relx=0.24, rely=0.72, relwidth=0.1, relheight=0.03)
       Label(menu_frames[1], text="Playing Time", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)).place(relx=0.12, rely=0.78, relwidth=0.1, relheight=0.03)
       Label(menu_frames[1], text="Player Wage", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)).place(relx=0.24, rely=0.78, relwidth=0.1, relheight=0.03)
       club_happiness_label = Label(menu_frames[1], text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow")
       club_happiness_label.place(relx=0.12, rely=0.75, relwidth=0.1, relheight=0.03)
       squad_happiness_label = Label(menu_frames[1], text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow")
       squad_happiness_label.place(relx=0.24, rely=0.75, relwidth=0.1, relheight=0.03)
       playtime_happiness_label = Label(menu_frames[1], text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow")
       playtime_happiness_label.place(relx=0.12, rely=0.81, relwidth=0.1, relheight=0.03)
       wage_happiness_label = Label(menu_frames[1], text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow")
       wage_happiness_label.place(relx=0.24, rely=0.81, relwidth=0.1, relheight=0.03)

       if player_object.club_happiness > 65:
           club_happiness_label.config(text="Good", fg="green")
       elif player_object.club_happiness < 34:
           club_happiness_label.config(text="Bad", fg="red")
       else:
           club_happiness_label.config(text="Okay", fg="yellow")

       if player_object.training_happiness > 65:
           squad_happiness_label.config(text="Good", fg="green")
       elif player_object.training_happiness < 34:
           squad_happiness_label.config(text="Bad", fg="red")
       else:
           squad_happiness_label.config(text="Okay", fg="yellow")

       if player_object.playing_time > 65:
           playtime_happiness_label.config(text="Good", fg="green")
       elif player_object.playing_time < 34:
           playtime_happiness_label.config(text="Bad", fg="red")
       else:
           playtime_happiness_label.config(text="Okay", fg="yellow")

       if player_object.wage_happiness > 65:
           wage_happiness_label.config(text="Good", fg="green")
       elif player_object.wage_happiness < 34:
           wage_happiness_label.config(text="Bad", fg="red")
       else:
           wage_happiness_label.config(text="Okay", fg="yellow")


   options1 = ["SUB", "LB", "CB", "RB", "DM", "CM", "AM", "LF", "CF", "RF"]
   options2 = ["SUB", "GK"]

   squad_position_vars = []
   # Populate the squadContent frame with labels for each player
   for i, player in enumerate(squad):
       player.selected_position.set("SUB")

       # decides which list to use for the dropdown based on if the player is a gk or not
       if player.pos == "GK":
           option_list = options2
       else:
           option_list = options1

       squad_position_vars.append(player.selected_position)

       if player.injured == 0:
           player_name_background = LIGHT_UI_COLOUR
       else:
           player_name_background = "red"

       # Create labels for player information
       labels = [
           Button(squadContent, text=f"{player.first_name} {player.last_name}", bg=player_name_background, fg="white",
                  font=("Comic Sans", 15), padx=10, borderwidth=0,
                  command=lambda player=player: display_player_info(player),
                  width=round(SCREEN_WIDTH*0.01)),

           OptionMenu(squadContent, player.selected_position, *option_list),

           Label(squadContent, text=player.ovr, bg="#3d4659", fg="white", font=("Comic Sans", 22),
                 padx=10, width=round(SCREEN_WIDTH*0.001)),

           Label(squadContent, text=player.pos, bg="#3d4659", fg="white", font=("Comic Sans", 22),
                 padx=10, width=round(SCREEN_WIDTH*0.001)),

           Label(squadContent, bg="green", width=round(SCREEN_WIDTH*0.001)),
           # makes space between labels
           Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH*0.0005)),

           Label(squadContent, bg="red", width=round(SCREEN_WIDTH*0.001)),
           # makes space between labels
           Label(squadContent, bg="#3d4659", width=round(SCREEN_WIDTH*0.0005)),

           Label(squadContent, bg="#84FF00", width=round(SCREEN_WIDTH*0.001)),

           Label(squadContent, text=player.age, bg="#3d4659", fg="white", font=("Comic Sans", 22),
                 padx=round(SCREEN_WIDTH*0.001), width=round(SCREEN_WIDTH*0.0025)),
           Label(squadContent, text=player.getValue(), bg="#3d4659", fg="white", font=("Comic Sans", 22),
                 padx=round(SCREEN_WIDTH*0.0005), width=round(SCREEN_WIDTH*0.002)),
           Label(squadContent, text=player.wage, bg="#3d4659", fg="white", font=("Comic Sans", 22),
                 padx=round(SCREEN_WIDTH*0.0005), width=round(SCREEN_WIDTH*0.003))
       ]

       # configures option menu appearance
       labels[1].config(background="#26262e", foreground="white", highlightthickness=0, font=("Comic Sans", 8))
       labels[1]["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))

       # Grid the labels within the squadContent frame
       for j, label in enumerate(labels):
           label.grid(row=i + 1, column=j)

       # used to unplace all relevant labels when resorting squad list
       all_squad_labels.append(labels)

   # Configure the scrollbar when the squadContent frame is resized
   squadContent.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

   # Create a window for the squadContent frame within the canvas
   canvas.create_window((0, 0), window=squadContent, anchor="nw")

   # Enable scroll wheel functionality
   def _on_mousewheel(event):
       canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

   canvas.bind_all("<MouseWheel>", _on_mousewheel)

   # Place the squadFrame on the screen
   squadFrame.place(relx=0, rely=0.1, relwidth=0.48, relheight=0.585)#0.75

   global player_detail

   # shows extra player info
   player_detail = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 16), text="Player available for selection", anchor="n")
   player_detail.place(relx=0, rely=0.685, relwidth=0.48, relheight=0.165)

   # shows selected player name
   player_name_info = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 13), text="")
   player_name_info.place(relx=0.01, rely=0.7, relwidth=0.12, relheight=0.03)

   # selected player ovr
   player_ovr_info = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 27), text="")
   player_ovr_info.place(relx=0.01, rely=0.73, relwidth=0.12, relheight=0.05)

   # selected player pos
   player_pos_info = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 13), text="")
   player_pos_info.place(relx=0.01, rely=0.78, relwidth=0.12, relheight=0.03)

   # shows player contract expiry date
   player_expire_info = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 11), text="")
   player_expire_info.place(relx=0.01, rely=0.81, relwidth=0.07, relheight=0.03)

   player_expire_date = Label(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 12, "bold"), text="")
   player_expire_date.place(relx=0.08, rely=0.81, relwidth=0.05, relheight=0.03)

   # transfer list player button
   player_transfer_list_check = Button(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 11), text="", borderwidth=0, activebackground=DARK_UI_COLOUR, activeforeground="white")
   player_transfer_list_check.place(relx=0.36, rely=0.69, relwidth=0.12, relheight=0.05)

   # negotiate new contract
   player_contract_button = Button(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 11), text="", borderwidth=0, activebackground=DARK_UI_COLOUR, activeforeground="white")
   player_contract_button.place(relx=0.36, rely=0.74, relwidth=0.12, relheight=0.05)

   player_release_button = Button(menu_frames[1], fg="white", bg="#363440", font=("Comic Sans", 11), text="", borderwidth=0, activebackground=DARK_UI_COLOUR, activeforeground="white")
   player_release_button.place(relx=0.36, rely=0.79, relwidth=0.12, relheight=0.05)


   # FORMATION VIEW LABELS
   #pitch
   Label(menu_frames[1], bg="#363440", fg="white", highlightthickness=5, highlightbackground="white", highlightcolor="white").place(relx=0.5, rely=0.42, relwidth=0.48, relheight=0.41)
   #gk
   gk = Label(menu_frames[1], bg="#26262e", fg="white", text="GK", font=("Comic Sans", 10), highlightbackground="green", highlightthickness=2)
   gk.place(relx=0.52, rely=0.59, relwidth=0.04, relheight=0.07)
   #lcb
   lcb = Label(menu_frames[1], bg="#26262e", fg="white", text="CB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2)
   lcb.place(relx=0.58, rely=0.5, relwidth=0.04, relheight=0.07)
   #cb
   cb = Label(menu_frames[1], bg="#26262e", fg="white", text="CB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2)
   #rcb
   rcb = Label(menu_frames[1], bg="#26262e", fg="white", text="CB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2)
   rcb.place(relx=0.58, rely=0.68, relwidth=0.04, relheight=0.07)
   #lb
   lb = Label(menu_frames[1], bg="#26262e", fg="white", text="LB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2)
   lb.place(relx=0.63, rely=0.44, relwidth=0.04, relheight=0.07)
   #rb
   rb = Label(menu_frames[1], bg="#26262e", fg="white", text="RB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2)
   rb.place(relx=0.63, rely=0.74, relwidth=0.04, relheight=0.07)
   #ldm
   ldm = Label(menu_frames[1], bg="#26262e", fg="white", text="DM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #rdm
   rdm = Label(menu_frames[1], bg="#26262e", fg="white", text="DM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #dm
   dm = Label(menu_frames[1], bg="#26262e", fg="white", text="DM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)
   dm.place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)
   #lcm
   lcm = Label(menu_frames[1], bg="#26262e", fg="white", text="CM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)
   lcm.place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)
   #rcm
   rcm = Label(menu_frames[1], bg="#26262e", fg="white", text="CM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)
   rcm.place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)
   #cm
   cm = Label(menu_frames[1], bg="#26262e", fg="white", text="CM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #lam
   lam = Label(menu_frames[1], bg="#26262e", fg="white", text="AM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #ram
   ram = Label(menu_frames[1], bg="#26262e", fg="white", text="AM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #am
   am = Label(menu_frames[1], bg="#26262e", fg="white", text="AM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2)

   #lf
   lf = Label(menu_frames[1], bg="#26262e", fg="white", text="LF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2)
   lf.place(relx=0.84, rely=0.44, relwidth=0.04, relheight=0.07)
   #rf
   rf = Label(menu_frames[1], bg="#26262e", fg="white", text="RF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2)
   rf.place(relx=0.84, rely=0.74, relwidth=0.04, relheight=0.07)
   #lcf
   lcf = Label(menu_frames[1], bg="#26262e", fg="white", text="CF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2)

   #rcf
   rcf = Label(menu_frames[1], bg="#26262e", fg="white", text="CF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2)

   #cf
   cf = Label(menu_frames[1], bg="#26262e", fg="white", text="CF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2)
   cf.place(relx=0.9, rely=0.59, relwidth=0.04, relheight=0.07)

   # colours used for match menu
   home_colour_one = CLUB_COLOUR_ONE
   home_colour_two = CLUB_COLOUR_TWO
   away_colour_one = "#FFFFFF"
   away_colour_two = "#000000"

   display_player_info(squad[0])

   # MATCH MENU ______________________________________________________________________-

   match_minutes = 0
   match_paused = None
   match_speed = MEDIUM_MATCH_SPEED

   def counter_press(counter_pressing, long_ball_effectiveness, counter_attack_frequency):
       def weighted_random_choice(a, b, c):
           # List of variables with their values
           variables = {'a': a, 'b': b, 'c': c}

           # Step 1: Normalize values to be non-negative
           min_value = min(variables.values())
           normalized_values = {k: v - min_value + 30 for k, v in variables.items()}

           # Step 2: Compute weights
           total_weight = sum(normalized_values.values())
           weights = {k: v / total_weight for k, v in normalized_values.items()}

           # Step 3: Use weighted random selection
           choices = list(weights.keys())
           probabilities = list(weights.values())

           selected_variable = random.choices(choices, probabilities)[0]

           return selected_variable

       counter_press_chance = 0.2
       counter_press_chance -= long_ball_effectiveness / 300
       counter_press_chance -= counter_attack_frequency / 300
       counter_press_chance += counter_pressing / 300
       counter_press_chance += ((0.5 - counter_press_chance) * (random.randint(15, 40) / 100))

       random_chance = random.randint(1, 100) / 100
       if random_chance > counter_press_chance:
           counter_pressing = counter_pressing * -1
           result_of_possession = weighted_random_choice(counter_pressing, long_ball_effectiveness, counter_attack_frequency)
           if result_of_possession == "a":
               return "other team keeps control of the ball"
           elif result_of_possession == "b":
               return "other team tries a long ball"
           elif result_of_possession == "c":
               return "other team starts a counter attack"
           else:
               return ":("
       else:
           return "possession won back"

   def simulate_possession(midfield_rating, possession_ability, pressing_effectiveness, counter_pressing, long_ball_effectiveness, counter_attack_frequency):
       retain_chance = 0.3
       retain_chance += midfield_rating / 400
       retain_chance += possession_ability / 300
       retain_chance -= pressing_effectiveness / 200
       retain_chance += ((0.5 - retain_chance) * (random.randint(30, 55) / 100))

       random_chance = random.randint(1, 100) / 100
       if random_chance > retain_chance:
           result_of_counter_press = counter_press(counter_pressing, long_ball_effectiveness, counter_attack_frequency)
           if result_of_counter_press == "possession won back":
               return 2
           else:
               if result_of_counter_press == "other team keeps control of the ball":
                   return 3
               elif result_of_counter_press == "other team tries a long ball":
                   return 4
               elif result_of_counter_press == "other team starts a counter attack":
                   return 5
       else:
           return 1

   def counter_attack_started(fast_counter_effectiveness, attack_quality, defence_quality):
       chance_of_chance = 0.2
       chance_of_chance += fast_counter_effectiveness / 300
       chance_of_chance += (attack_quality - defence_quality) / 100

       if chance_of_chance > 0.65:
           chance_of_chance = 0.65

       random_chance = random.randint(1, 100) / 100
       if chance_of_chance >= random_chance:
           return "chance"
       else:
           return "no chance"

   def long_ball_started(long_ball_effectiveness, attack_quality, defence_quality):
       chance_of_chance = 0.2
       chance_of_chance += long_ball_effectiveness / 300
       chance_of_chance += (attack_quality - defence_quality) / 100

       if chance_of_chance > 0.65:
           chance_of_chance = 0.65

       random_chance = random.randint(1, 100) / 100
       if chance_of_chance >= random_chance:
           return "chance"
       else:
           return "no chance"

   def break_down_defence_started(break_down_defence_effectiveness, crossing_effectiveness, attack_quality, defence_quality):
       chance_of_chance = 0.2
       chance_of_chance += break_down_defence_effectiveness / 600
       chance_of_chance += crossing_effectiveness / 600
       chance_of_chance += (attack_quality - defence_quality) / 100

       chance_of_chance += (0.5 - chance_of_chance) * 0.2

       if chance_of_chance > 0.65:
           chance_of_chance = 0.65

       random_chance = random.randint(1, 100) / 100
       if chance_of_chance >= random_chance:
           return "chance"
       else:
           return "no chance"

   def chance_created(attack_quality, goalkeeper_quality):
       attack_boost = attack_quality - goalkeeper_quality

       chance_shottarget = 0.3

       chance_shottarget += attack_boost / 200

       chance_shottarget += (0.5 - chance_shottarget) * 0.35

       if (random.randint(1, 100) / 100) <= chance_shottarget:

           chance_goal = 0.2
           chance_goal += attack_boost / 300

           chance_goal += (0.5 - chance_goal) * 0.3

           if (random.randint(1, 100) / 100) <= chance_goal:
               if random.randint(1,100) > 96:
                   return "own goal"
               else:
                   return "goal"
           else:
               return "shot on target"
       else:
           return "shot"

   # pauses/resumes the match
   def pause_match():
       global match_paused
       if match_paused.is_set():
           match_paused.clear()
           start_match_button.configure(text="Continue Match")
       else:
           match_paused.set()
           start_match_button.configure(text="Pause Match")

   # gets current minute in the match
   def current_min():
       if time_label.cget("text") == "HT":
           return 45
       else:
           return int(time_label.cget("text")[:-1])

   # what runs when the match is first starting, when the button is start match
   def match_start():
       global match_minutes, home_team_possession_value, away_team_possession_value
       home_team_possession_value = 0
       away_team_possession_value = 0
       match_minutes = random.randint(90, 98)
       start_match_button.configure(text="Pause Match", command=pause_match)
       threading.Thread(target=minutes, daemon=True).start()
       pause_match()

   def update_match_bars():
       home_team_percent = int(home_team_possession_value / (home_team_possession_value + away_team_possession_value)*100)
       away_team_percent = 100 - home_team_percent
       home_possession_bar.place(relx=0.105, rely=0.3, relwidth=0.3*(home_team_percent/100), relheight=0.04)
       home_possession.config(text=f"{home_team_percent}%")
       away_possession.config(text=f"{away_team_percent}%")

       try:
           home_team_shotstarget_percent = int(int(home_shotstarget.cget("text")) / (int(home_shotstarget.cget("text")) + int(away_shotstarget.cget("text")))*100)
           home_shotstarget_bar.place(relx=0.105, rely=0.575, relwidth=0.3*(home_team_shotstarget_percent/100), relheight=0.04)
       except ZeroDivisionError:
           home_shotstarget_bar.place(relx=0.105, rely=0.575, relwidth=0.15, relheight=0.04)

       try:
           home_team_shots_percent = int(int(home_shots.cget("text")) / (int(home_shots.cget("text")) + int(away_shots.cget("text"))) * 100)
           home_shots_bar.place(relx=0.105, rely=0.455, relwidth=0.3*(home_team_shots_percent/100), relheight=0.04)
       except ZeroDivisionError:
           home_shots_bar.place(relx=0.105, rely=0.455, relwidth=0.15, relheight=0.04)

   def write_commentary(commentary_info):
       commentary_text_three.config(text=commentary_text_two.cget("text"))
       commentary_text_two.config(text=commentary_text.cget("text"))
       commentary_text.config(text=commentary_info)

   def do_set_piece(team_set_piece_effectiveness, team_in_possession, set_piece_type):
       commentary_corner_scored = ["Goal! {} have scored from the\ncorner after a wonderful header",
                                   "Its in! {} score and its poor marking\nthat leaves the player for a free header",
                                   "Goal! It's a brilliant delivery from\nthe {} man and its headed home with ease"]

       commentary_corner_shot = ["The {} man gets his head to the corner\ndelivery but its a tame effort",
                                 "Its a dangerous delivery from the {}\ncorner but the goalkeeper had it covered",
                                 "The delivery from the {} corner finds a\nteamate's head but no goal comes from it"]

       commentary_corner_no_shot = ["The corner is headed away",
                                    "The delivery from the corner fails to find anyone"]

       commentary_free_kick_goal = ["What a goal! The free kick is curled into\nthe top corner and the goalkeeper had no chance",
                                    "Goal! The free kick is delivered\ninto the box and headed home",
                                    "Its a goal! The free kick from 20 yards out\nis curled over the wall and into the net"]

       commentary_free_kick_shot = ["The player has go from the free kick\nbut the shot wasn't good enough",
                                    "The player puts the ball into the box from\nthe free kick but the chance isn't taken",
                                    "The free kick takes a deflection off the wall\n and the goalkeeper claims the ball easily"]

       commentary_free_kick_no_shot = ["The delivery from the free kick is headed away",
                                       "The free kick is put into the box and doesn't find anyone"]

       commentary_penalty_missed = ["Missed! It's an awful penalty by {} and the\nother team breathes a sigh of relief",
                                    "And its completely wide! {} don't\nconvert their massive opportunity",
                                    "Its been missed! Hesitation from\nthe {} penalty taker has cost his team"]

       commentary_penalty_saved = ["Its been saved! The goalkeeper\nguesses the right direction",
                                   "Save! A brilliant moment of goalkeeping\nsaves his team",
                                   "Save! It's not the best of penalties\nand the goalkeeper gets a hold of the ball"]

       commentary_penalty_scored = ["Its been converted! Cool, calm and\ncollected from the {} penalty taker",
                                    "Goal! Its a convincing penalty and\n{} score from the spot",
                                    "Its in! The {} penalty has been\nscored and the opposition defenders look on"]

       if set_piece_type == "Penalty":
           chance_score = random.randint(1, 100)
           if chance_score < 83:
               if team_in_possession == home_team:
                   home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                   home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                   home_shots.config(text=int(home_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_scored).format(home_team_name.cget("text")))
                   if team_in_possession == "Player":
                       random_player_score = random.choice(starting_attackers)
                       home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (P),")
                   else:
                       random_player_score = random.choice(opponent_players)
                       home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score} (P),")

               else:
                   away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                   away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                   away_shots.config(text=int(away_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_scored).format(away_team_name.cget("text")))
                   if team_in_possession == "Player":
                       random_player_score = random.choice(starting_attackers)
                       away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (P),")
                   else:
                       random_player_score = random.choice(opponent_players)
                       away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score} (P),")

           elif chance_score < 93:
               if team_in_possession == home_team:
                   home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                   home_shots.config(text=int(home_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_saved))
               else:
                   away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                   away_shots.config(text=int(away_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_saved))
           else:
               if team_in_possession == home_team:
                   home_shots.config(text=int(home_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_missed).format(home_team_name.cget("text")))
               else:
                   away_shots.config(text=int(away_shots.cget("text")) + 1)
                   write_commentary(random.choice(commentary_penalty_missed).format(away_team_name.cget("text")))

           update_match_bars()

       elif set_piece_type == "Corner" or set_piece_type == "Free Kick":
           if set_piece_type == "Corner":
               # chances multiplied starting with first, shot on target chance = shot_chance * shot_target_chance
               shot_chance = 0.3
               shot_target_chance = 0.5
               goal_chance = 0.2
           else:
               shot_chance = 0.5
               shot_target_chance = 0.3
               goal_chance = 0.2

           shot_chance += team_set_piece_effectiveness / 150
           shot_target_chance += team_set_piece_effectiveness / 150
           goal_chance += team_set_piece_effectiveness / 150

           if shot_chance > 0.9:
               shot_chance = 0.9
           if shot_target_chance > 0.7:
               shot_target_chance = 0.7
           if goal_chance > 0.4:
               goal_chance = 0.4

           random_chance_shot = random.randint(1, 100) / 100

           if random_chance_shot <= shot_chance:
               if team_in_possession == home_team:
                   home_shots.config(text=int(home_shots.cget("text"))+1)
                   if set_piece_type == "Corner":
                       write_commentary(random.choice(commentary_corner_shot).format(home_team_name.cget("text")))
                   else:
                       write_commentary(random.choice(commentary_free_kick_shot).format(home_team_name.cget("text")))
               else:
                   away_shots.config(text=int(away_shots.cget("text"))+1)
                   if set_piece_type == "Corner":
                       write_commentary(random.choice(commentary_corner_shot).format(away_team_name.cget("text")))
                   else:
                       write_commentary(random.choice(commentary_free_kick_shot).format(away_team_name.cget("text")))

               random_chance_shot = random.randint(1, 100) / 100

               if random_chance_shot <= shot_target_chance:
                   if team_in_possession == home_team:
                       home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                   else:
                       away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)

                   random_chance_shot = random.randint(1, 100) / 100

                   if random_chance_shot <= goal_chance:
                       if team_in_possession == home_team:
                           home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           if team_in_possession == "Player":
                               random_position_score = random.randint(1, 9)
                               if random_position_score < 4:
                                   random_position_score = starting_attackers
                               elif random_position_score < 7:
                                   random_position_score = starting_midfielders
                               else:
                                   random_position_score = starting_defenders

                               random_player_score = random.choice(random_position_score)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")

                           else:
                               random_player_score = random.choice(opponent_players)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score},")

                           if set_piece_type == "Corner":
                               write_commentary(random.choice(commentary_corner_scored).format(home_team_name.cget("text")))
                           else:
                               write_commentary(random.choice(commentary_free_kick_goal).format(home_team_name.cget("text")))
                       else:
                           away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                           if team_in_possession == "Player":
                               random_position_score = random.randint(1, 9)
                               if random_position_score < 4:
                                   random_position_score = starting_attackers
                               elif random_position_score < 7:
                                   random_position_score = starting_midfielders
                               else:
                                   random_position_score = starting_defenders
                               random_player_score = random.choice(random_position_score)
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                           else:
                               random_player_score = random.choice(opponent_players)
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score},")

                           if set_piece_type == "Corner":
                               write_commentary(random.choice(commentary_corner_scored).format(away_team_name.cget("text")))
                           else:
                               write_commentary(random.choice(commentary_free_kick_goal).format(away_team_name.cget("text")))
           else:
               if team_in_possession == home_team:
                   if set_piece_type == "Corner":
                       write_commentary(random.choice(commentary_corner_no_shot).format(home_team_name.cget("text")))
                   else:
                       write_commentary(random.choice(commentary_free_kick_no_shot).format(home_team_name.cget("text")))
               else:
                   if set_piece_type == "Corner":
                       write_commentary(random.choice(commentary_corner_no_shot).format(away_team_name.cget("text")))
                   else:
                       write_commentary(random.choice(commentary_free_kick_no_shot).format(away_team_name.cget("text")))

           update_match_bars()

   # main function for match sim activated by threads
   def minutes():
       global home_team_possession_value, away_team_possession_value
       global match_minutes
       global match_paused
       global match_speed, pens_occurred, first_leg_home_score, first_leg_away_score, playoffs_winner

       commentary_corner = ["{} now have a corner and a chance to test the\nopposition defenders",
                            "Corner to {}, as they search for a goal",
                            "Now a chance for {} through a corner"]

       commentary_free_kick = ["The referee has given {} a free kick for a foul.\nThat looked like a dive!",
                                "{} have a free kick in a dangerous position.\nCan they make it count?",
                                "That's a foul, and a free kick to {}",
                                "It's a free kick to {}, the fouled player\nhas set the ball down and looks ready to take it!",
                                "The referee says its a foul and a free kick to {},\nthe other team are not happy with the decision!",
                                "{} have a free kick in a dangerous position.\nCan they make it count?",
                                "That's a foul, and a free kick to {}",
                                "It's a free kick to {}, the fouled player\nhas set the ball down and looks ready to take it!",
                                "The referee says its a foul and a free kick to {},\nthe other team are not happy with the decision!"]

       commentary_penalty = ["And the referee has pointed to the spot, its a penalty to {}!",
                             "The other team can't believe it, its a penalty to {}!",
                             "The player goes down inside the box, and\n the referee's given {} a penalty!"]

       commentary_ball_lost = ["{} lose possession in the middle of the pitch",
                               "Its a slip up in possession by {}",
                               "{} lose the ball rather unnecessarily",
                               "It's a misplaced pass and {} lose the ball",
                               "{} lose control of the ball",
                               "The ball's been given away by {}"]

       commentary_counter_press = ["But it's won back with a counter press",
                                   "However an effective counter press gets them back on the ball",
                                   "But it's given right back to them after some poor play"]

       commentary_counter = ["The other team takes the opportunity and starts a counter attack!",
                             "This looks dangerous as the other team goes on the counter!",
                             "The other team rush the ball forward and start a counter!"]

       commentary_long_ball = ["The ball has been hit long in search of a forward",
                               "Now the ball goes forward with a long ball",
                               "Straight away, the other team play it long"]

       commentary_keep_possession = ["The other team calm it down and pass the ball around",
                                     "And now the counter press has been played out of",
                                     "The other team now look to hold possession"]

       commentary_counter_wasted = ["Nothing comes of {}'s counter",
                                    "{} waste the counter and no chance comes from it",
                                    "{} can't get the counter quite right\nand no chance comes"]

       commentary_counter_shot = ["And the counter's lead to a dangerous shot but\nit's not met well enough by the forward",
                                  "In the end the counter leads to a shot comfortably off target",
                                  "The ball is put into a dangerous area from the counter\nbut the shot is well wide"]

       commentary_counter_shottarget = ["Its a brilliant counter but an\neven better save from the goalkeeper!",
                                        "From the counter, the attack has\na go but its right at the keeper",
                                        "Save! The counter looked promising and the goalkeeper\nneeded to intervene after a good shot"]

       commentary_counter_goal = ["Goal! The counter attack is executed perfectly and\nit ends with an easy goal for the attacker",
                                  "Its a goal! The ball is brought forward with speed on the counter,\nthe defenders were left exposed and it was put into the net",
                                  "Goal! The counter has been taken advantage of after a\nclinical strike that the goalkeeper could do nothing about"]

       commentary_long_ball_wasted = ["{}'s long ball is dealt with by some solid defending",
                                      "Nothing comes of {}'s long ball, not enough accuracy that time",
                                      "The long ball is put too far for any {}\nplayer to reach it and nothing comes of it"]

       commentary_long_ball_shot = ["Its a pin-point long ball but the attacker is\nunder too much pressure to get a convincing shot off",
                                    "The long ball cut the defence open but\nthe attacker couldn't score from the chance",
                                    "The long ball finds an attacker who shoots it just over"]

       commentary_long_ball_shottarget = ["The long ball finds an attacker in space\nbut he is denied by the goalkeeper",
                                          "Its a brilliant long ball that falls to the attacking team\nbut the shot is tame and right at the goalkeeper",
                                          "The long ball ends with a shot on target after\nsome intricate passing from the attacking team"]

       commentary_long_ball_goal = ["Its a goal! Its a defence-splitting long ball\nand a brilliant shot too to finish",
                                    "Goal! The long ball puts the attacker\nthrough on goal who finishes calmly",
                                    "What a goal! The defender couldn't get his head to the long ball and\nit insteads find an attacker who scores with a brilliant shot!"]

       commentary_breaking_defence_shot = ["A cross finds the attacker's head\nwho puts it just wide of the post!",
                                           "Some nice combination play in the box leads to\na dissapointing finish that went well wide",
                                           "A cross is put into the box at speed and\nflicked on just wide at the near post",
                                           "Its a defence-splitting through ball into space\nbut the attacker fails to get a shot on target"]

       commentary_breaking_defence_shottarget = ["The attacking team try a cross which is\nflicked on and into the goalkeeper's arms",
                                                 "The attackers get bodies into the box and an\nattempted cross forces a good save from the goalkeeper",
                                                 "A brilliant pass forward finds an attacker in\nspace who puts his shot right at the keeper",
                                                 "The attacker dribbles past not one but two defenders\nand his shot required quick reflexes from the keeper"]

       commentary_breaking_defence_goal = ["Its a goal! The attacking team put a cross into a dangerous\narea and it meets an attacker's head who thumps it in",
                                           "Goal! Its a moment of brilliant quality as some intricate passing\ninside the box unlocks the defence and is finished cooly",
                                           "Goal! The attacking team try a cross into the edge of\nthe box where its volleyed in with some power!",
                                           "Its a goal! A dangerous through ball find the attacker\nwho puts it past the goalkeeper at the near post"]

       commentary_own_goal = ["Own goal! After chaos inside the box, the ball is struck into the\ndefender who could only watch as the ball deflects in",
                              "Its an own goal! In trying to defend the cross, the defenders\naccidently put the ball past his goalkeeper in chaotic fashion",
                              "Own goal! The defender blocks the attempted shot but could only\nwatch as the ball ricochets off him and into his own net"]

       team_in_possession = None
       set_piece_type = None
       counter_attack = False
       long_ball = False
       opponent_match_attack = int(next_opponent[1] * (random.randint(90, 105) / 100))
       opponent_match_defence = int(next_opponent[2] * (random.randint(90, 105) / 100))
       opponent_match_midfield = int((opponent_match_attack + opponent_match_defence) / 2)
       opponent_match_goalkeeper = int(opponent_match_midfield * (random.randint(95, 105) / 100))
       while current_min() < match_minutes:
           match_paused.wait()
           new_value = current_min() + 1
           time_label.configure(text=f"{new_value}\'")
           if current_min() == 45:
               pause_match()
               time_label.configure(text="HT")

           # simulates opponent fatigue as match carries on
           opponent_match_attack = opponent_match_attack * 0.9985
           opponent_match_defence = opponent_match_defence * 0.9985
           opponent_match_midfield = opponent_match_midfield * 0.9985
           opponent_match_goalkeeper = opponent_match_goalkeeper * 0.9995

           # randomly picks team to have the ball if neither team has it
           if team_in_possession is None:
               team_in_possession == random.choice([home_team, away_team])
               if team_in_possession == home_team:
                   home_team_possession_value += 1
               else:
                   away_team_possession_value += 1

               update_match_bars()

           for i in squad:
               if i.actual_position.get() != "SUB" and i.actual_position.get() != "GK":
                   i.fitness -= (random.randint(2, 5) / 10)
                   i.sharpness += (random.randint(1, 2) / 10)
               elif i.actual_position.get() == "GK":
                   i.fitness -= (random.randint(0, 3) / 10)
                   i.sharpness += (random.randint(0, 2) / 10)

               i.match_ovr = int(i.ovr * ((((i.sharpness/100)*1.2)+((i.fitness/100)*0.7)+((i.form/100)*1.1))/2))

               if i.actual_position.get() != i.pos:
                   if i.actual_position.get()[-1] == i.pos[-1]:
                       i.match_ovr -= 3
                   else:
                       i.match_ovr -= 10

           if set_piece_type is not None:
               do_set_piece(player_set_piece_effectiveness if team_in_possession == "Player" else opponent_set_piece_effectiveness, team_in_possession, set_piece_type)
               set_piece_type = None
               update_match_bars()
               time.sleep(match_speed)
               continue

           if counter_attack:
               if team_in_possession == "Player":
                   attack_quality = 0
                   for i in starting_attackers:
                       attack_quality += i.match_ovr
                   attack_quality = int(attack_quality / len(starting_attackers))
                   result_of_counter_attack = counter_attack_started(player_fast_counter_effectiveness, attack_quality, opponent_match_defence)
                   if result_of_counter_attack == "chance":
                       result_of_chance = chance_created(attack_quality, opponent_match_goalkeeper)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_counter_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_counter_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           random_position_score = random.randint(1, 9)
                           if random_position_score < 6:
                               random_position_score = starting_attackers
                           elif random_position_score < 9:
                               random_position_score = starting_midfielders
                           else:
                               random_position_score = starting_defenders

                           random_player_score = random.choice(random_position_score)
                           write_commentary(random.choice(commentary_counter_goal))
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(opponent_players)
                           if team_in_possession == home_team:
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score} (OG),")
                           else:
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score} (OG),")

                       update_match_bars()
                   else:
                       if team_in_possession == home_team:
                           write_commentary(random.choice(commentary_counter_wasted).format(home_team_name.cget("text")))
                       else:
                           write_commentary(random.choice(commentary_counter_wasted).format(away_team_name.cget("text")))
               else:
                   defence_quality = 0
                   for i in starting_defenders:
                       defence_quality += i.match_ovr
                   defence_quality = int(defence_quality / len(starting_defenders))
                   result_of_counter_attack = counter_attack_started(opponent_fast_counter_effectiveness, opponent_match_attack, defence_quality)
                   if result_of_counter_attack == "chance":
                       result_of_chance = chance_created(opponent_match_attack, starting_goalkeeper.match_ovr)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_counter_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text"))+1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_counter_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text"))+1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           random_player_score = random.choice(opponent_players)
                           write_commentary(random.choice(commentary_counter_goal))
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score},")
                               home_shots.config(text=int(home_shots.cget("text"))+1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(starting_defenders)
                           if team_in_possession == home_team:
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")
                           else:
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")

                       update_match_bars()
                   else:
                       if team_in_possession == home_team:
                           write_commentary(random.choice(commentary_counter_wasted).format(home_team_name.cget("text")))
                       else:
                           write_commentary(random.choice(commentary_counter_wasted).format(away_team_name.cget("text")))
               counter_attack = False
               time.sleep(match_speed)

           elif long_ball:
               if team_in_possession == "Player":
                   attack_quality = 0
                   for i in starting_attackers:
                       attack_quality += i.match_ovr
                   attack_quality = int(attack_quality / len(starting_attackers))
                   result_of_long_ball = long_ball_started(player_long_ball_effectiveness, attack_quality, opponent_match_defence)
                   if result_of_long_ball == "chance":
                       result_of_chance = chance_created(attack_quality, opponent_match_goalkeeper)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_long_ball_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_long_ball_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           write_commentary(random.choice(commentary_long_ball_goal))
                           random_position_score = random.randint(1, 9)
                           if random_position_score < 6:
                               random_position_score = starting_attackers
                           elif random_position_score < 9:
                               random_position_score = starting_midfielders
                           else:
                               random_position_score = starting_defenders

                           random_player_score = random.choice(random_position_score)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(opponent_players)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score} (OG),")
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score} (OG),")
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)

                       update_match_bars()
                   else:
                       if team_in_possession == home_team:
                           write_commentary(random.choice(commentary_long_ball_wasted).format(home_team_name.cget("text")))
                       else:
                           write_commentary(random.choice(commentary_long_ball_wasted).format(away_team_name.cget("text")))

               else:
                   defence_quality = 0
                   for i in starting_defenders:
                       defence_quality += i.match_ovr
                   defence_quality = int(defence_quality / len(starting_defenders))
                   result_of_long_ball = long_ball_started(opponent_long_ball_effectiveness, opponent_match_attack, defence_quality)
                   if result_of_long_ball == "chance":
                       result_of_chance = chance_created(opponent_match_attack, starting_goalkeeper.match_ovr)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_long_ball_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_long_ball_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           write_commentary(random.choice(commentary_long_ball_goal))
                           random_player_score = random.choice(opponent_players)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score},")
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(starting_defenders)
                           if team_in_possession == home_team:
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")
                           else:
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")

                       update_match_bars()
                   else:
                       if team_in_possession == home_team:
                           write_commentary(random.choice(commentary_long_ball_wasted).format(home_team_name.cget("text")))
                       else:
                           write_commentary(random.choice(commentary_long_ball_wasted).format(away_team_name.cget("text")))
               long_ball = False
               time.sleep(match_speed)

           else:
               if team_in_possession == "Player":
                   attack_quality = 0
                   for i in starting_attackers:
                       attack_quality += i.match_ovr
                   attack_quality = int(attack_quality / len(starting_attackers))
                   result_of_break_down_defence = break_down_defence_started(player_breaking_down_defence_effectiveness, player_crossing_effectiveness, attack_quality, opponent_match_defence)
                   if result_of_break_down_defence == "chance":
                       result_of_chance = chance_created(attack_quality, opponent_match_goalkeeper)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_breaking_defence_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_breaking_defence_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           write_commentary(random.choice(commentary_breaking_defence_goal))
                           random_position_score = random.randint(1, 9)
                           if random_position_score < 6:
                               random_position_score = starting_attackers
                           elif random_position_score < 9:
                               random_position_score = starting_midfielders
                           else:
                               random_position_score = starting_defenders

                           random_player_score = random.choice(random_position_score)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(opponent_players)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score} (OG),")
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score} (OG),")
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)

                       update_match_bars()
               else:
                   defence_quality = 0
                   for i in starting_defenders:
                       defence_quality += i.match_ovr
                   defence_quality = int(defence_quality / len(starting_defenders))
                   result_of_break_down_defence = break_down_defence_started(opponent_breaking_down_defence_effectiveness, opponent_crossing_effectiveness, opponent_match_attack, defence_quality)
                   if result_of_break_down_defence == "chance":
                       result_of_chance = chance_created(opponent_match_attack, starting_goalkeeper.match_ovr)
                       if result_of_chance == "shot":
                           write_commentary(random.choice(commentary_breaking_defence_shot))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                       elif result_of_chance == "shot on target":
                           write_commentary(random.choice(commentary_breaking_defence_shottarget))
                           if team_in_possession == home_team:
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                           else:
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                       elif result_of_chance == "goal":
                           write_commentary(random.choice(commentary_breaking_defence_goal))
                           random_player_score = random.choice(opponent_players)
                           if team_in_possession == home_team:
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score},")
                               home_shots.config(text=int(home_shots.cget("text")) + 1)
                               home_shotstarget.config(text=int(home_shotstarget.cget("text")) + 1)
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                           else:
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score},")
                               away_shots.config(text=int(away_shots.cget("text")) + 1)
                               away_shotstarget.config(text=int(away_shotstarget.cget("text")) + 1)
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                       elif result_of_chance == "own goal":
                           write_commentary(random.choice(commentary_own_goal))
                           random_player_score = random.choice(starting_defenders)
                           if team_in_possession == home_team:
                               home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                               home_scorers_label.config(text=home_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")
                           else:
                               away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                               away_scorers_label.config(text=away_scorers_label.cget("text") + f" {random_player_score.first_name[0]}. {random_player_score.last_name} (OG),")

                       update_match_bars()
                       time.sleep(match_speed)

           # simulates what happens to team on possession
           if (team_in_possession == home_team and home_team == "Player") or (team_in_possession == away_team and away_team == "Player") :
               midfield_rating = 0
               for i in starting_midfielders:
                   midfield_rating += i.match_ovr
               midfield_rating = int(midfield_rating/len(starting_midfielders))
               result_of_possession = simulate_possession(midfield_rating, player_possession_ability, opponent_pressing_effectiveness, player_pressing_effectiveness, opponent_long_ball_effectiveness, opponent_counter_frequency)
           else:
               midfield_rating = opponent_match_midfield
               result_of_possession = simulate_possession(midfield_rating, player_possession_ability*-1, player_pressing_effectiveness, opponent_pressing_effectiveness, player_long_ball_effectiveness,
                                                          player_counter_frequency)

           possession_overturn = False
           if team_in_possession == home_team:
               team_format_name = home_team_name.cget("text")
           else:
               team_format_name = away_team_name.cget("text")

           if result_of_possession == 2:
               write_commentary(f"{random.choice(commentary_ball_lost).format(team_format_name)}\n{random.choice(commentary_counter_press)}")
           elif result_of_possession == 3:
               write_commentary(f"{random.choice(commentary_ball_lost).format(team_format_name)}\n{random.choice(commentary_keep_possession)}")
               possession_overturn = True
           elif result_of_possession == 4:
               write_commentary(f"{random.choice(commentary_ball_lost).format(team_format_name)}\n{random.choice(commentary_long_ball)}")
               possession_overturn = True
               long_ball = True
           elif result_of_possession == 5:
               write_commentary(f"{random.choice(commentary_ball_lost).format(team_format_name)}\n{random.choice(commentary_counter)}")
               counter_attack = True
               possession_overturn = True

           if possession_overturn:
               if team_in_possession == home_team:
                   team_in_possession = away_team
               else:
                   team_in_possession = home_team

           if team_in_possession == home_team:
               home_team_possession_value += 1
               team_format_name = home_team_name.cget("text")
           else:
               away_team_possession_value += 1
               team_format_name = away_team_name.cget("text")

           set_piece_type = None
           # set piece 1 in 10 chance
           if random.randint(1, 15) == 2:
               set_piece_type = random.randint(1, 100)
               if set_piece_type <= 45:
                   set_piece_type = "Free Kick"
                   write_commentary(random.choice(commentary_free_kick).format(team_format_name))
               elif 50 >= set_piece_type > 45:
                   set_piece_type = "Penalty"
                   write_commentary(random.choice(commentary_penalty).format(team_format_name))
               else:
                   set_piece_type = "Corner"
                   write_commentary(random.choice(commentary_corner).format(team_format_name))

           update_match_bars()

           time.sleep(match_speed)

       if competition_name.cget("text") == "League":
           playoffs_next = True
           for i in opponents_list[1:]:
               if i[10] == "League":
                   playoffs_next = False

           qualified_for_playoffs = False
           if playoffs_next and opponents_list[-1][10] == "Playoffs Final":
               for i in league[2:6]:
                   if i[0] == CLUB_NAME:
                       qualified_for_playoffs = True

           if qualified_for_playoffs:
               for i in range(opponents_list):
                   if opponents_list[i][10] == "Playoffs Semi Final Leg 1":
                       for j in league[2:6]:
                           if j[1] != CLUB_NAME:
                               opponents_list[i] = j + ["A", "Playoffs Semi Final Leg 1", 16, 5]
                   if opponents_list[i][10] == "Playoffs Semi Final Leg 1":
                       for j in league[2:6]:
                           if j[1] != CLUB_NAME:
                               opponents_list[i] = j + ["H", "Playoffs Semi Final Leg 2", 21, 5]

           tactics_button.place_forget()
           start_match_button.configure(text="Exit Match", command=leave_match)
           time_label.configure(text="FT")
       elif competition_name.cget("text") == "Playoffs Semi Final Leg 1":
           first_leg_home_score = int(home_score_label.cget("text"))
           first_leg_away_score = int(away_score_label.cget("text"))

           tactics_button.place_forget()
           start_match_button.configure(text="Exit Match", command=leave_match)
           time_label.configure(text="FT")
       elif competition_name.cget("text") == "Playoffs Semi Final Leg 2":
           full_home_score = int(home_score_label.cget("text"))
           full_away_score = int(away_score_label.cget("text"))
           if full_home_score == full_away_score:
               write_commentary("The two sides can't be seperated and\nit will be penalties that decide who goes through")
               home_team_name_pens = home_team_name.cget("text")
               away_team_name_pens = away_team_name.cget("text")

               pens_occurred = True

               for i in range(5):

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} score")
                       home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} miss")

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                       away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

               full_home_score = int(home_score_label.cget("text"))
               full_away_score = int(away_score_label.cget("text"))

               i = 5
               while full_home_score == full_away_score:
                   time.sleep(match_speed)
                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} score")
                       home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} miss")

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                       away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

                   i += 1
                   full_home_score = int(home_score_label.cget("text"))
                   full_away_score = int(away_score_label.cget("text"))

           if full_home_score < full_away_score:
               for i in league:
                   if i[0] == away_team_name.cget("text"):
                       playoff_winner = i
           else:
               for i in league[2:6]:
                   if i[0] not in [CLUB_NAME, away_team_name.cget("text")]:
                       opponents_list[-1] = i + ["H", "Playoffs Final", 27, 5]
                       for i in schedule_labels:
                           if i.cget("text").split("(")[0].strip() == "Playoffs Final":
                               for index, j in enumerate(opponents_list):
                                   if j[10] == "Playoffs Final":
                                       i.config(text=f"{opponents_list[index][10]} ({opponents_list[index][9]}) {opponents_list[index][0]}, {opponents_list[index][11]} {months[int(opponents_list[index][12]) - 1]}")

           tactics_button.place_forget()
           start_match_button.configure(text="Exit Match", command=leave_match)
           time_label.configure(text="FT")
       elif competition_name.cget("text") == "Playoffs Final":
           if int(home_score_label.cget("text")) > int(away_score_label.cget("text")):
               for i in league:
                   if i[0] == CLUB_NAME:
                       playoffs_winner = i
               tactics_button.place_forget()
               start_match_button.configure(text="Exit Match", command=leave_match)
               time_label.configure(text="FT")
           elif int(home_score_label.cget("text")) < int(away_score_label.cget("text")):
               for i in league:
                   if i[0] == away_team_name.cget("text"):
                       playoffs_winner = i
               tactics_button.place_forget()
               start_match_button.configure(text="Exit Match", command=leave_match)
               time_label.configure(text="FT")
           else:
               write_commentary("The two sides can't be seperated and\nit will be penalties that decide who goes through")
               home_team_name_pens = home_team_name.cget("text")
               away_team_name_pens = away_team_name.cget("text")

               pens_occurred = True

               for i in range(5):

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} score")
                       home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} miss")

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                       away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

               i = 5
               while home_score_label.cget("text") == away_score_label.cget("text"):
                   time.sleep(match_speed)
                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} score")
                       home_score_label.config(text=int(home_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {home_team_name_pens} miss")

                   time.sleep(match_speed)

                   random_pens = random.randint(1, 100)
                   if random_pens < 80:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                       away_score_label.config(text=int(away_score_label.cget("text")) + 1)
                   else:
                       write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

                   i += 1

               if int(home_score_label.cget("text")) > int(away_score_label.cget("text")):
                   for i in league:
                       if i[0] == CLUB_NAME:
                           playoffs_winner = i
                   tactics_button.place_forget()
                   start_match_button.configure(text="Exit Match", command=leave_match)
                   time_label.configure(text="FT")
               elif int(home_score_label.cget("text")) < int(away_score_label.cget("text")):
                   for i in league:
                       if i[0] == away_team_name.cget("text"):
                           playoffs_winner = i
                   tactics_button.place_forget()
                   start_match_button.configure(text="Exit Match", command=leave_match)
                   time_label.configure(text="FT")
       elif home_score_label.cget("text") == away_score_label.cget("text"):
           write_commentary("The two sides can't be seperated and\nit will be penalties that decide who goes through")
           home_team_name_pens = home_team_name.cget("text")
           away_team_name_pens = away_team_name.cget("text")

           pens_occurred = True

           for i in range(5):

               time.sleep(match_speed)

               random_pens = random.randint(1, 100)
               if random_pens < 80:
                   write_commentary(f"Round {i+1}: {home_team_name_pens} score")
                   home_score_label.config(text=int(home_score_label.cget("text")) + 1)
               else:
                   write_commentary(f"Round {i+1}: {home_team_name_pens} miss")

               time.sleep(match_speed)

               random_pens = random.randint(1, 100)
               if random_pens < 80:
                   write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                   away_score_label.config(text=int(away_score_label.cget("text")) + 1)
               else:
                   write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

           i = 5
           while home_score_label.cget("text") == away_score_label.cget("text"):
               time.sleep(match_speed)
               random_pens = random.randint(1, 100)
               if random_pens < 80:
                   write_commentary(f"Round {i + 1}: {home_team_name_pens} score")
                   home_score_label.config(text=int(home_score_label.cget("text")) + 1)
               else:
                   write_commentary(f"Round {i + 1}: {home_team_name_pens} miss")

               time.sleep(match_speed)

               random_pens = random.randint(1, 100)
               if random_pens < 80:
                   write_commentary(f"Round {i + 1}: {away_team_name_pens} score")
                   away_score_label.config(text=int(away_score_label.cget("text")) + 1)
               else:
                   write_commentary(f"Round {i + 1}: {away_team_name_pens} miss")

               i += 1

           tactics_button.place_forget()
           start_match_button.configure(text="Exit Match", command=leave_match)
           time_label.configure(text="FT")
       else:
           tactics_button.place_forget()
           start_match_button.configure(text="Exit Match", command=leave_match)
           time_label.configure(text="FT")

   def hide_menu_buttons():
       global menu_buttons
       for i in menu_buttons:
           i["state"] = "disabled"
           i.configure(bg="#3d4659")

   def hide_menu_buttons_grey():
       global menu_buttons
       for i in menu_buttons:
           i["state"] = "disabled"
           i["disabledforeground"] = DARK_UI_COLOUR
           i.configure(bg=DARK_UI_COLOUR)

   def show_menu_buttons():
       global menu_buttons
       for i in menu_buttons:
           i["state"] = "active"
           i.configure(bg="#26262e")
           i["disabledforeground"] = "#3d4659"

   def tactics_match_config():
       set_tactics(True)
       if not set_tactics_button.cget("bg") == "red":
           modified_wing_play = wing_play
           modified_pressing = pressing
           modified_playing_out_of_press = playing_out_of_press
           modified_passing_over_the_top = passing_over_the_top
           modified_high_tempo_passing = high_tempo_passing
           modified_defending_deep = defending_deep
           modified_defending_crosses = defending_crosses
           modified_set_pieces = set_pieces
           modified_ball_possession = ball_possession
           modified_counter_attacking = counter_attacking

           player_playstyle = selected_playstyle.get()

           if player_playstyle == "Tiki Taka":
               modified_wing_play = modified_wing_play * 0.9
               modified_pressing = modified_pressing * 1.1
               modified_playing_out_of_press = modified_playing_out_of_press * 1.2
               modified_passing_over_the_top = modified_passing_over_the_top * 0.8
               modified_high_tempo_passing = modified_high_tempo_passing * 1.2
               modified_defending_deep = modified_defending_deep * 0.8
               modified_ball_possession = modified_ball_possession * 1.2
               modified_counter_attacking = modified_counter_attacking * 0.8
           elif player_playstyle == "Gegenpress":
               modified_pressing = modified_pressing * 1.2
               modified_passing_over_the_top = modified_passing_over_the_top * 0.9
               modified_high_tempo_passing = modified_high_tempo_passing * 1.1
               modified_defending_deep = modified_defending_deep * 0.8
           elif player_playstyle == "Counter Attack":
               modified_wing_play = modified_wing_play * 0.9
               modified_pressing = modified_pressing * 0.8
               modified_passing_over_the_top = modified_passing_over_the_top * 1.1
               modified_high_tempo_passing = modified_high_tempo_passing * 1.1
               modified_defending_deep = modified_defending_deep * 1.1
               modified_ball_possession = modified_ball_possession * 0.8
               modified_counter_attacking = modified_counter_attacking * 1.2
           elif player_playstyle == "Route One":
               modified_wing_play = modified_wing_play * 1.1
               modified_defending_crosses = modified_defending_crosses * 1.1
               modified_pressing = modified_pressing * 0.8
               modified_playing_out_of_press = modified_playing_out_of_press * 0.8
               modified_passing_over_the_top = modified_passing_over_the_top * 1.3
               modified_high_tempo_passing = modified_high_tempo_passing * 0.9
               modified_ball_possession = modified_ball_possession * 0.9
               modified_counter_attacking = modified_counter_attacking * 1.1
           elif player_playstyle == "Park The Bus":
               modified_defending_crosses = modified_defending_crosses * 1.1
               modified_pressing = modified_pressing * 0.8
               modified_playing_out_of_press = modified_playing_out_of_press * 0.9
               modified_passing_over_the_top = modified_passing_over_the_top * 1.2
               modified_high_tempo_passing = modified_high_tempo_passing * 0.8
               modified_defending_deep = modified_defending_deep * 1.3
               modified_ball_possession = modified_ball_possession * 0.8
               modified_counter_attacking = modified_counter_attacking * 1.1
           elif player_playstyle == "Wing Play":
               modified_wing_play = modified_wing_play * 1.2
               modified_defending_crosses = modified_defending_crosses * 1.1
               modified_playing_out_of_press = modified_playing_out_of_press * 0.9
               modified_ball_possession = modified_ball_possession * 0.9
               modified_counter_attacking = modified_counter_attacking * 0.9

           player_crossing_effectiveness = modified_wing_play - next_opponent_skills[5]
           player_pressing_effectiveness = modified_pressing - next_opponent_skills[4]
           player_long_ball_effectiveness = modified_passing_over_the_top - next_opponent_skills[5]
           player_breaking_down_defence_effectiveness = modified_high_tempo_passing - next_opponent_skills[6]
           player_set_piece_effectiveness = modified_set_pieces - next_opponent_skills[8]
           player_possession_ability = modified_ball_possession - next_opponent_skills[9]
           player_fast_counter_effectiveness = modified_counter_attacking - next_opponent_skills[7]
           player_counter_frequency = modified_counter_attacking - next_opponent_skills[9]

           opponent_crossing_effectiveness = player_crossing_effectiveness * - 1
           opponent_pressing_effectiveness = player_pressing_effectiveness * -1
           opponent_long_ball_effectiveness = player_long_ball_effectiveness * -1
           opponent_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * -1
           opponent_set_piece_effectiveness = player_set_piece_effectiveness * -1
           opponent_fast_counter_effectiveness = player_fast_counter_effectiveness * -1
           opponent_counter_frequency = player_counter_frequency * -1

           if when_ball_lost == 1:
               opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 1.2
               player_pressing_effectiveness = player_pressing_effectiveness * 1.2
           elif when_ball_lost == 2:
               opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 0.8
               player_pressing_effectiveness = player_pressing_effectiveness * 0.8

           if when_ball_won == 1:
               player_fast_counter_effectiveness = player_fast_counter_effectiveness * 1.2
               player_possession_ability = player_possession_ability * 0.8
           elif when_ball_won == 2:
               player_fast_counter_effectiveness = player_fast_counter_effectiveness * 0.8
               player_possession_ability = player_possession_ability * 1.2

           if build_up == 1:
               player_long_ball_effectiveness = player_long_ball_effectiveness * 1.2
               opponent_pressing_effectiveness = opponent_pressing_effectiveness * 0.8
               player_possession_ability = player_possession_ability * 0.8
               opponent_fast_counter_effectiveness = opponent_fast_counter_effectiveness * 1.2
           elif build_up == 2:
               opponent_pressing_effectiveness = opponent_pressing_effectiveness * 1.2
               player_long_ball_effectiveness = player_long_ball_effectiveness * 0.8
               player_possession_ability = player_possession_ability * 1.2
               opponent_fast_counter_effectiveness = opponent_fast_counter_effectiveness * 0.8

           if attacking_area == 1:
               player_crossing_effectiveness = player_crossing_effectiveness * 1.1
               player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 0.9
           elif attacking_area == 2:
               player_crossing_effectiveness = player_crossing_effectiveness * 0.9
               player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 1.1

           if selected_defence.get() == "High Press":
               player_pressing_effectiveness = player_pressing_effectiveness * 1.2
               opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 1.2
           elif selected_defence.get() == "Low Block":
               opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 1.2
               opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 0.8
               opponent_counter_frequency = opponent_counter_frequency * 0.8
               player_fast_counter_effectiveness = player_fast_counter_effectiveness * 1.2
               player_counter_frequency = player_counter_frequency * 0.8
               player_pressing_effectiveness = player_pressing_effectiveness * 0.8

           if selected_a_width.get() == "Wide":
               player_crossing_effectiveness = player_crossing_effectiveness * 1.1
               player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 0.9
           elif selected_a_width.get() == "Narrow":
               player_crossing_effectiveness = player_crossing_effectiveness * 0.9
               player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 1.1

           if selected_d_width.get() == "Wide":
               opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 1.2
               opponent_crossing_effectiveness = opponent_crossing_effectiveness * 0.8
               player_counter_frequency = player_counter_frequency * 1.2
               player_pressing_effectiveness = player_pressing_effectiveness * 0.8
           elif selected_d_width.get() == "Narrow":
               opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 0.8
               opponent_crossing_effectiveness = opponent_crossing_effectiveness * 1.2
               player_counter_frequency = player_counter_frequency * 0.8
               player_pressing_effectiveness = player_pressing_effectiveness * 1.2

           change_menu(6)
           for i in squad:
               if i.actual_position.get() != "SUB":
                   i.played_match = True

   def simulate_ai_match(team_one, team_two):
       team_one_attack = team_one[1]
       team_two_attack = team_two[1]

       total_value = int((team_one_attack + team_two_attack) * 1.25)

       one = 0
       two = 0
       three = 0
       for i in range(3):
           random_value = random.randint(1, total_value)
           if random_value < team_one_attack:
               one += 1
           elif random_value < team_one_attack + team_two_attack:
               two += 1
           else:
               one += 1
               two += 1

       if one > two:
           return 1
       elif two > one:
           return 2
       else:
           return 3

   def add_trophy(trophy_name):
       pass

   def leave_match():
       global next_match_day, next_match_month, match_date, next_opponent, next_opponent_analysis_label, next_opponent_skills, squad_confirmed, career_wins, career_draws, career_losses, career_goals, career_goals_conceded

       squad_size_label.config(text=f"Current Squad Size: {len(squad)}")
       if competition_name.cget("text") == "League":
           other_teams = []
           for i in league:
               if i[0] != CLUB_NAME and i[0] != next_opponent[0]:
                   other_teams.append(i)
               elif i[0] == next_opponent[0]:
                   i[6] += 1
                   if home_team == "Player":
                       if int(away_score_label.cget("text")) > int(home_score_label.cget("text")):
                           i[5] += 3
                       elif int(away_score_label.cget("text")) == int(home_score_label.cget("text")):
                           i[5] += 1
                   else:
                       if int(away_score_label.cget("text")) < int(home_score_label.cget("text")):
                           i[5] += 3
                       elif int(away_score_label.cget("text")) == int(home_score_label.cget("text")):
                           i[5] += 1
               elif i[0] == CLUB_NAME:
                   i[6] += 1
                   if home_team == "Player":
                       if int(away_score_label.cget("text")) < int(home_score_label.cget("text")):
                           i[5] += 3
                       elif int(away_score_label.cget("text")) == int(home_score_label.cget("text")):
                           i[5] += 1
                   else:
                       if int(away_score_label.cget("text")) > int(home_score_label.cget("text")):
                           i[5] += 3
                       elif int(away_score_label.cget("text")) == int(home_score_label.cget("text")):
                           i[5] += 1

           random.shuffle(other_teams)

           for i in range(0, len(other_teams), 2):
               team_one = other_teams[i]
               team_two = other_teams[i+1]

               result = simulate_ai_match(team_one, team_two)

               for j in league:
                   if j[0] == team_one[0]:
                       j[6] += 1
                       if result == 1:
                           j[5] += 3
                       elif result == 3:
                           j[5] += 1

                   if j[0] == team_two[0]:
                       j[6] += 1
                       if result == 2:
                           j[5] += 3
                       elif result == 3:
                           j[5] += 1

           league.sort(key=lambda i: i[5], reverse=True)
           update_league_table()
       elif competition_name.cget("text") == "Cup Round of 32":
           if (home_team == "Player" and int(away_score_label.cget("text")) < int(home_score_label.cget("text"))) or (away_team == "Player" and int(away_score_label.cget("text")) > int(home_score_label.cget("text"))):
               for i in schedule_labels:
                   if i.cget("text").split("(")[0].strip() == "Cup Round of 16":
                       for index, j in enumerate(opponents_list):
                           if j[10] == "Cup Round of 16":
                               opponents_list[index] = cup_r16_opponent + ["H", "Cup Round of 16", 24, 11]
                               i.config(text=f"{opponents_list[index][10]} ({opponents_list[index][9]}) {opponents_list[index][0]}, {opponents_list[index][11]} {months[int(opponents_list[index][12])-1]}")

       elif competition_name.cget("text") == "Cup Round of 16":
           if (home_team == "Player" and int(away_score_label.cget("text")) < int(home_score_label.cget("text"))) or (away_team == "Player" and int(away_score_label.cget("text")) > int(home_score_label.cget("text"))):
               for i in schedule_labels:
                   if i.cget("text").split("(")[0].strip() == "Cup Quarter Final":
                       for index, j in enumerate(opponents_list):
                           if j[10] == "Cup Quarter Final":
                               opponents_list[index] = cup_qf_opponent + ["A", "Cup Quarter Final", 5, 2]
                               i.config(text=f"{opponents_list[index][10]} ({opponents_list[index][9]}) {opponents_list[index][0]}, {opponents_list[index][11]} {months[int(opponents_list[index][12])-1]}")
       elif competition_name.cget("text") == "Cup Quarter Final":
           if (home_team == "Player" and int(away_score_label.cget("text")) < int(home_score_label.cget("text"))) or (away_team == "Player" and int(away_score_label.cget("text")) > int(home_score_label.cget("text"))):
               for i in schedule_labels:
                   if i.cget("text").split("(")[0].strip() == "Cup Semi Final":
                       for index, j in enumerate(opponents_list):
                           if j[10] == "Cup Semi Final":
                               opponents_list[index] = cup_sf_opponent + ["H", "Cup Semi Final", 9, 3]
                               i.config(text=f"{opponents_list[index][10]} ({opponents_list[index][9]}) {opponents_list[index][0]}, {opponents_list[index][11]} {months[int(opponents_list[index][12])-1]}")
       elif competition_name.cget("text") == "Cup Semi Final":
           if (home_team == "Player" and int(away_score_label.cget("text")) < int(home_score_label.cget("text"))) or (away_team == "Player" and int(away_score_label.cget("text")) > int(home_score_label.cget("text"))):
               for i in schedule_labels:
                   if i.cget("text").split("(")[0].strip() == "Cup Final":
                       for index, j in enumerate(opponents_list):
                           if j[10] == "Cup Final":
                               opponents_list[index] = cup_f_opponent + ["H", "Cup Final", 18, 4]
                               i.config(text=f"{opponents_list[index][10]} ({opponents_list[index][9]}) {opponents_list[index][0]}, {opponents_list[index][11]} {months[int(opponents_list[index][12])-1]}")
       elif competition_name.cget("text") == "Cup Final":
           if (home_team == "Player" and int(away_score_label.cget("text")) < int(home_score_label.cget("text"))) or (away_team == "Player" and int(away_score_label.cget("text")) > int(home_score_label.cget("text"))):
               popup_message.config(text="The board congratulates you on winning the national\ncup. We believe it is a true reflection of your\noutstanding leadership skils and that you are taking\nthe club on the right path.\n\nCongratulations and keep it up!")
               change_menu(12)
               hide_menu_buttons_grey()
               add_trophy(f"{CLUB_COUNTRY} National Cup")
           else:
               popup_message.config(text="The board understands the dissappointment of losing\nthe cup final. However we belive you have proven\nyour worth to the club by advancing so far in the tournament\n\nThe board continues to back you as manager and hopes to\nsee success in the future")
               change_menu(12)
               hide_menu_buttons_grey()

       for index, i in enumerate(schedule_labels):
           if i.cget("bg") == LIGHT_UI_COLOUR:
               competition = competition_name.cget("text")
               if home_team == "Player":
                   home_score = home_score_label.cget("text")
                   away_score = away_score_label.cget("text")
                   if int(home_score) > int(away_score):
                       fg_colour = "green"
                       career_wins += 1
                       career_goals += int(home_score)
                       career_goals_conceded += int(away_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
                   elif int(home_score) == int(away_score):
                       fg_colour = "yellow"
                       career_draws += 1
                       career_goals += int(home_score)
                       career_goals_conceded += int(away_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
                   else:
                       fg_colour = "red"
                       career_losses += 1
                       career_goals += int(home_score)
                       career_goals_conceded += int(away_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
               else:
                   home_score = home_score_label.cget("text")
                   away_score = away_score_label.cget("text")
                   if int(home_score) > int(away_score):
                       fg_colour = "red"
                       career_losses += 1
                       career_goals += int(away_score)
                       career_goals_conceded += int(home_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
                   elif int(home_score) == int(away_score):
                       fg_colour = "yellow"
                       career_draws += 1
                       career_goals += int(away_score)
                       career_goals_conceded += int(home_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")
                   else:
                       fg_colour = "green"
                       career_wins += 1
                       career_goals += int(away_score)
                       career_goals_conceded += int(home_score)
                       career_wins_label.config(text=f"{career_wins} Wins ({int((career_wins / (career_wins + career_draws + career_losses))*100)}%)")
                       career_draws_label.config(text=f"{career_draws} Draws({int((career_draws / (career_wins + career_draws + career_losses))*100)}%)")
                       career_losses_label.config(text=f"{career_losses} Losses ({int((career_losses / (career_wins + career_draws + career_losses))*100)}%)")
                       career_goals_scored_label.config(text=f"{career_goals} Goals Scored")
                       career_goals_conceded_label.config(text=f"{career_goals_conceded} Goals Conceded")

               if not pens_occurred:
                   i.config(text=f"{competition} {home_score} - {away_score} vs {next_opponent[0]} {next_match_day} {months[next_match_month-1]}", fg=fg_colour)
               else:
                   i.config(text=f"{competition} {home_score} - {away_score}(P) vs {next_opponent[0]} {next_match_day} {months[next_match_month - 1]}", fg=fg_colour)
               career_wins_bar.place(relx=0.53, rely=0.2, relwidth=0.34 * career_wins / (career_wins + career_draws + career_losses), relheight=0.03)
               losses_width = 0.34 * career_losses / (career_wins + career_draws + career_losses)
               career_losses_bar.place(relx=0.87 - losses_width, rely=0.2, relwidth=losses_width, relheight=0.03)

       commentary_text.config(text="")
       commentary_text_two.config(text="")
       commentary_text_three.config(text="")

       playstyle_cover_label.place_forget()

       for i in squad:
           if i.played_match:
               i.matches_played += 1
           elif i.injured == 0:
               i.matches_not_played += 1
           i.sharpness = int(i.sharpness)
           i.fitness = int(i.fitness)
           if i.played_match:
               injury_chance = random.randint(1, 80+(physiotherapist.rating*3))
               if injury_chance == 15 and i.injured == 0 and i.pos != "GK":
                   i.injured = random.choice(injury_lengths)
                   i.injured = int(i.injured * ((100 - (physiotherapist.rating*2))/100))
               i.form += (random.randint(0, 20) - 10)
               if i.morale > 83:
                   i.form += 5
               elif i.morale > 67:
                   i.form += 2
               elif i.morale > 49:
                   i.form += 0
               elif i.morale > 32:
                   i.form -= 2
               else:
                   i.form -= 5

           else:
               i.form -= 2

           if i.sharpness > 100:
               i.sharpness = 100
           if i.sharpness < 0:
               i.sharpness = 0
           if i.fitness > 100:
               i.fitness = 100
           if i.fitness < 0:
               i.fitness = 0
           if i.form > 100:
               i.form = 100
           if i.form < 0:
               i.form = 0

       update_player_report()

       change_menu(0)
       show_menu_buttons()
       simulate_button.config(text="Simulate", command=sim_button)
       reset_match()
       set_tactics_button.config(command=lambda: set_tactics(False), bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
       player_transfer_list_check.config(state="active")
       player_contract_button.config(state="active")
       player_release_button.config(state="active")
       display_player_info(squad[0])
       try:
           opponents_list.pop(0)
           move_schedule_labels = 1
           while opponents_list[0][0] == "N/A":
               opponents_list.pop(0)
               move_schedule_labels += 1
           next_opponent = opponents_list[0]
           next_opponent_analysis_label.config(text=next_opponent[0])
           next_opponent_league_label.config(text=get_team_league(next_opponent[0]))
           competition_name.config(text=next_opponent[10])
           calc_opponent_strength()
           next_opponent_skills = get_opponent_skills(next_opponent)
       except IndexError:
           squad_confirmed = False
           update_squad_display()

           if league in [eng_2, eng_3, eng_4, fra_2, ger_2, ita_2, spa_2]:
               for i in league[2:6]:
                   pass

           for i in schedule_labels:
               i.config(bg=DARK_UI_COLOUR)
           next_match_month = 0
           next_match_day = 0

           # empty next opponent analysis and next opponent things
           return

       skill_names = ["Counter Attacking", "High Tempo Passing", "Wing Play", "Passing Over The Top", "Playing Out Of Press", "Defending Crosses", "Defending Deep",
                      "Pressing", "Set Pieces", "Ball Possession"]
       best_skills = []

       for i in enumerate(next_opponent_skills):
           best_skills.append([skill_names[i[0]], i[1]])

       best_skills.sort(key=lambda i: i[1], reverse=True)

       opponent_strengths_labels[0].config(text=best_skills[0][0])
       opponent_strengths_labels[1].config(text=best_skills[1][0])
       opponent_strengths_labels[2].config(text=best_skills[2][0])

       opponent_weaknesses_labels[0].config(text=best_skills[-1][0])
       opponent_weaknesses_labels[1].config(text=best_skills[-2][0])
       opponent_weaknesses_labels[2].config(text=best_skills[-3][0])

       if next_opponent[3] == 0:
           opponent_attack_style_label.config(text="Possession")
       elif next_opponent[3] == 1:
           opponent_attack_style_label.config(text="Counter Attacking")
       elif next_opponent[3] == 2:
           opponent_attack_style_label.config(text="Physical")
       elif next_opponent[3] == 3:
           opponent_attack_style_label.config(text="Direct")
       else:
           opponent_attack_style_label.config(text="Balanced")

       if next_opponent[9] == "H":
           home_team_name.config(text=CLUB_NAME)
           away_team_name.config(text=next_opponent[0])
       else:
           away_team_name.config(text=CLUB_NAME)
           home_team_name.config(text=next_opponent[0])

       for i in range(move_schedule_labels):
           for j in range(len(schedule_labels)):
               if schedule_labels[j].cget("bg") == LIGHT_UI_COLOUR:
                   schedule_labels[j].config(bg=DARK_UI_COLOUR)
                   schedule_labels[j+1].config(bg=LIGHT_UI_COLOUR)
                   break

       next_match_day = next_opponent[11]
       next_match_month = next_opponent[12]
       match_year = year
       if next_match_month < month:
           match_year += 1
       match_date.configure(text=f"{next_match_day} {months[next_match_month - 1]} {match_year}")
       squad_confirmed = False
       update_squad_display()

   def enter_match():
       global match_paused
       global match_speed
       global prev_stadium_attendance, previous_attendance_label, ticket_income_label
       global player_crossing_effectiveness, player_pressing_effectiveness, player_long_ball_effectiveness, player_breaking_down_defence_effectiveness, player_set_piece_effectiveness, player_possession_ability, player_fast_counter_effectiveness, player_counter_frequency
       global opponent_crossing_effectiveness, opponent_pressing_effectiveness, opponent_long_ball_effectiveness, opponent_breaking_down_defence_effectiveness, opponent_set_piece_effectiveness, opponent_fast_counter_effectiveness, opponent_counter_frequency
       global home_team, away_team
       global subs_left, opponent_players, pens_occurred

       opponent_players = []
       for i in range(5):
           player_region = str(random.randint(0, 17))

           player_first_name = random.choice(first_names[player_region])
           player_last_name = random.choice(last_names[player_region])
           opponent_players.append(f"{player_first_name[0]}. {player_last_name}")

       pens_occurred = False

       subs_left = 5

       squad_size_label.config(text=f"Subs Left: {subs_left}")

       commentary_home_name = home_team_name.cget("text")
       commentary_away_name = away_team_name.cget("text")

       if competition_name.cget("text") == "Playoffs Semi Final Leg 2":
           home_score_label.config(text=first_leg_away_score)
           away_score_label.config(text=first_leg_home_score)

       playstyle_cover_label.config(text=selected_playstyle.get())
       playstyle_cover_label.place(relx=0.51, rely=0.17, relwidth=0.1, relheight=0.05)
       playstyle_cover_label.lift()


       commentary_greetings = [f"Hello and welcome to today's thrilling encounter between {commentary_home_name}\nand {commentary_away_name}. An exciting match is expected!",
                               f"Good afternoon, football fans, and get ready for an electrifying match\nbetween {commentary_home_name} and {commentary_away_name}!",
                               f"Welcome, everyone, to a beautiful day of football as {commentary_home_name}\ntakes on {commentary_away_name}, with the excitement palpable!",
                               f"Good evening and thank you for joining us for this clash between {commentary_home_name}\nand {commentary_away_name}, where the atmosphere is buzzing with anticipation!",
                               f"Hello and thank you for joining us for what promises to be a thrilling\ncontest as {commentary_home_name} takes on {commentary_away_name}!",
                               f"Hello and welcome to this highly anticipated face-off between\n{commentary_home_name} and {commentary_away_name}!"]

       commentary_text.config(text=random.choice(commentary_greetings))

       for i in squad:
           if i.actual_position.get() != "SUB":
               i.played_match = True
           else:
               i.played_match = False

       modified_wing_play = wing_play
       modified_pressing = pressing
       modified_playing_out_of_press = playing_out_of_press
       modified_passing_over_the_top = passing_over_the_top
       modified_high_tempo_passing = high_tempo_passing
       modified_defending_deep = defending_deep
       modified_defending_crosses = defending_crosses
       modified_set_pieces = set_pieces
       modified_ball_possession = ball_possession
       modified_counter_attacking = counter_attacking

       player_playstyle = selected_playstyle.get()

       if player_playstyle == "Tiki Taka":
           modified_wing_play = modified_wing_play * 0.9
           modified_pressing = modified_pressing * 1.1
           modified_playing_out_of_press = modified_playing_out_of_press * 1.2
           modified_passing_over_the_top = modified_passing_over_the_top * 0.8
           modified_high_tempo_passing = modified_high_tempo_passing * 1.2
           modified_defending_deep = modified_defending_deep * 0.8
           modified_ball_possession = modified_ball_possession * 1.2
           modified_counter_attacking = modified_counter_attacking * 0.8
       elif player_playstyle == "Gegenpress":
           modified_pressing = modified_pressing * 1.2
           modified_passing_over_the_top = modified_passing_over_the_top * 0.9
           modified_high_tempo_passing = modified_high_tempo_passing * 1.1
           modified_defending_deep = modified_defending_deep * 0.8
       elif player_playstyle == "Counter Attack":
           modified_wing_play = modified_wing_play * 0.9
           modified_pressing = modified_pressing * 0.8
           modified_passing_over_the_top = modified_passing_over_the_top * 1.1
           modified_high_tempo_passing = modified_high_tempo_passing * 1.1
           modified_defending_deep = modified_defending_deep * 1.1
           modified_ball_possession = modified_ball_possession * 0.8
           modified_counter_attacking = modified_counter_attacking * 1.2
       elif player_playstyle == "Route One":
           modified_wing_play = modified_wing_play * 1.1
           modified_defending_crosses = modified_defending_crosses * 1.1
           modified_pressing = modified_pressing * 0.8
           modified_playing_out_of_press = modified_playing_out_of_press * 0.8
           modified_passing_over_the_top = modified_passing_over_the_top * 1.3
           modified_high_tempo_passing = modified_high_tempo_passing * 0.9
           modified_ball_possession = modified_ball_possession * 0.9
           modified_counter_attacking = modified_counter_attacking * 1.1
       elif player_playstyle == "Park The Bus":
           modified_defending_crosses = modified_defending_crosses * 1.1
           modified_pressing = modified_pressing * 0.8
           modified_playing_out_of_press = modified_playing_out_of_press * 0.9
           modified_passing_over_the_top = modified_passing_over_the_top * 1.2
           modified_high_tempo_passing = modified_high_tempo_passing * 0.8
           modified_defending_deep = modified_defending_deep * 1.3
           modified_ball_possession = modified_ball_possession * 0.8
           modified_counter_attacking = modified_counter_attacking * 1.1
       elif player_playstyle == "Wing Play":
           modified_wing_play = modified_wing_play * 1.2
           modified_defending_crosses = modified_defending_crosses * 1.1
           modified_playing_out_of_press = modified_playing_out_of_press * 0.9
           modified_ball_possession = modified_ball_possession * 0.9
           modified_counter_attacking = modified_counter_attacking * 0.9

       player_crossing_effectiveness = modified_wing_play - next_opponent_skills[5]
       player_pressing_effectiveness = modified_pressing - next_opponent_skills[4]
       player_long_ball_effectiveness = modified_passing_over_the_top - next_opponent_skills[5]
       player_breaking_down_defence_effectiveness = modified_high_tempo_passing - next_opponent_skills[6]
       player_set_piece_effectiveness = modified_set_pieces - next_opponent_skills[8]
       player_possession_ability = modified_ball_possession - next_opponent_skills[9]
       player_fast_counter_effectiveness = modified_counter_attacking - next_opponent_skills[7]
       player_counter_frequency = modified_counter_attacking - next_opponent_skills[9]

       opponent_crossing_effectiveness = next_opponent_skills[2] - modified_defending_crosses
       opponent_pressing_effectiveness = next_opponent_skills[7] - modified_playing_out_of_press
       opponent_long_ball_effectiveness = next_opponent_skills[3] - modified_defending_crosses
       opponent_breaking_down_defence_effectiveness = next_opponent_skills[1] - modified_defending_deep
       opponent_set_piece_effectiveness = player_set_piece_effectiveness * -1
       opponent_fast_counter_effectiveness = next_opponent_skills[0] - modified_pressing
       opponent_counter_frequency = next_opponent_skills[0] - modified_ball_possession

       if when_ball_lost == 1:
           opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 1.2
           player_pressing_effectiveness = player_pressing_effectiveness * 1.2
       elif when_ball_lost == 2:
           opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 0.8
           player_pressing_effectiveness = player_pressing_effectiveness * 0.8

       if when_ball_won == 1:
           player_fast_counter_effectiveness = player_fast_counter_effectiveness * 1.2
           player_possession_ability = player_possession_ability * 0.8
       elif when_ball_won == 2:
           player_fast_counter_effectiveness = player_fast_counter_effectiveness * 0.8
           player_possession_ability = player_possession_ability * 1.2

       if build_up == 1:
           player_long_ball_effectiveness = player_long_ball_effectiveness * 1.2
           opponent_pressing_effectiveness = opponent_pressing_effectiveness * 0.8
           player_possession_ability = player_possession_ability * 0.8
           opponent_fast_counter_effectiveness = opponent_fast_counter_effectiveness * 1.2
       elif build_up == 2:
           opponent_pressing_effectiveness = opponent_pressing_effectiveness * 1.2
           player_long_ball_effectiveness = player_long_ball_effectiveness * 0.8
           player_possession_ability = player_possession_ability * 1.2
           opponent_fast_counter_effectiveness = opponent_fast_counter_effectiveness * 0.8

       if attacking_area == 1:
           player_crossing_effectiveness = player_crossing_effectiveness * 1.1
           player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 0.9
       elif attacking_area == 2:
           player_crossing_effectiveness = player_crossing_effectiveness * 0.9
           player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 1.1

       if selected_defence.get() == "High Press":
           player_pressing_effectiveness = player_pressing_effectiveness * 1.2
           opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 1.2
       elif selected_defence.get() == "Low Block":
           opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 1.2
           opponent_long_ball_effectiveness = opponent_long_ball_effectiveness * 0.8
           opponent_counter_frequency = opponent_counter_frequency * 0.8
           player_fast_counter_effectiveness = player_fast_counter_effectiveness * 1.2
           player_counter_frequency = player_counter_frequency * 0.8
           player_pressing_effectiveness = player_pressing_effectiveness * 0.8

       if selected_a_width.get() == "Wide":
           player_crossing_effectiveness = player_crossing_effectiveness * 1.1
           player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 0.9
       elif selected_a_width.get() == "Narrow":
           player_crossing_effectiveness = player_crossing_effectiveness * 0.9
           player_breaking_down_defence_effectiveness = player_breaking_down_defence_effectiveness * 1.1

       if selected_d_width.get() == "Wide":
           opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 1.2
           opponent_crossing_effectiveness = opponent_crossing_effectiveness * 0.8
           player_counter_frequency = player_counter_frequency * 1.2
           player_pressing_effectiveness = player_pressing_effectiveness * 0.8
       elif selected_d_width.get() == "Narrow":
           opponent_breaking_down_defence_effectiveness = opponent_breaking_down_defence_effectiveness * 0.8
           opponent_crossing_effectiveness = opponent_crossing_effectiveness * 1.2
           player_counter_frequency = player_counter_frequency * 0.8
           player_pressing_effectiveness = player_pressing_effectiveness * 1.2

       set_tactics_button.config(bg=BUTTON_COLOUR, text="Confirm Tactics\nAnd Squad")
       match_paused = threading.Event()
       set_match_speed(MEDIUM_MATCH_SPEED)
       change_menu(6)
       hide_menu_buttons()
       set_tactics_button.config(command=tactics_match_config)
       player_transfer_list_check.config(state="disabled")
       player_contract_button.config(state="disabled")
       player_release_button.config(state="disabled")
       # gets attendance and adds profit from tickets
       if home_team_name.cget("text") == CLUB_NAME:
           home_team = "Player"
           away_team = next_opponent_skills
           prev_stadium_attendance = calculate_attendance()
           previous_attendance_label.config(text="Previous Match Attendance: {:,}".format(prev_stadium_attendance))
           if competition_name.cget("text") == "League":
               ticket_profit = prev_stadium_attendance * league_ticket_price
           else:
               ticket_profit = prev_stadium_attendance * cup_ticket_price
           add_profit(ticket_profit, ticket_income_label, False)

           # sets colours for home and away teams
           home_colour_one = CLUB_COLOUR_ONE
           home_colour_two = CLUB_COLOUR_TWO
           away_colour_one = next_opponent[7]
           away_colour_two = next_opponent[8]

           home_name_label.config(text=CLUB_NAME)
           away_name_label.config(text=next_opponent[0])

       else:
           home_team = next_opponent_skills
           away_team = "Player"
           home_colour_one = next_opponent[7]
           home_colour_two = next_opponent[8]
           away_colour_one = CLUB_COLOUR_ONE
           away_colour_two = CLUB_COLOUR_TWO

           away_name_label.config(text=CLUB_NAME)
           home_name_label.config(text=next_opponent[0])

       for i in home_team_labels:
           i.config(bg=home_colour_one, fg=home_colour_two)

       for i in away_team_labels:
           i.config(bg=away_colour_one, fg=away_colour_two)

       tactics_button.place(relx=0.51, rely=0.25, relwidth=0.235, relheight=0.1)

   def go_to_tactics():
       global match_paused
       update_squad_display()
       change_menu(1)
       if match_paused.is_set():
           pause_match()

   def set_match_speed(speed):
       global match_speed
       match_speed = speed
       for i in [slow_speed_button, medium_speed_button, fast_speed_button]:
           i.configure(font=("Comic sans", 16))
       if speed == FAST_MATCH_SPEED:
           fast_speed_button.configure(font=("Comic sans", 18, "bold"))
       elif speed == MEDIUM_MATCH_SPEED:
           medium_speed_button.configure(font=("Comic sans", 18, "bold"))
       elif speed == SLOW_MATCH_SPEED:
           slow_speed_button.configure(font=("Comic sans", 18, "bold"))

   def reset_match():
       time_label.configure(text="0'")
       start_match_button.config(text="Start Match", command=match_start)
       commentary_text.config(text="")
       commentary_text_two.config(text="")
       commentary_text_three.config(text="")
       assistant_text.config(text="")
       home_score_label.config(text="0")
       away_score_label.config(text="0")
       home_possession.config(text="50%")
       away_possession.config(text="50%")
       home_possession_bar.place(relx=0.105, rely=0.3, relwidth=0.15, relheight=0.04)
       home_shots.config(text="0")
       away_shots.config(text="0")
       home_shots_bar.place(relx=0.105, rely=0.455, relwidth=0.15, relheight=0.04)
       home_shotstarget.config(text="0")
       away_shotstarget.config(text="0")
       home_shotstarget_bar.place(relx=0.105, rely=0.575, relwidth=0.15, relheight=0.04)
       home_scorers_label.config(text="")
       away_scorers_label.config(text="")

   def do_swap_home_colours():
       for i in home_team_labels:
           i.config(bg=i.cget("fg"), fg=i.cget("bg"))

   def do_swap_away_colours():

       for i in away_team_labels:
           i.config(bg=i.cget("fg"), fg=i.cget("bg"))

   # BACKGROUNDS
   Label(menu_frames[6], bg="#26262e").place(relx=0.02, rely=0.25, relwidth=0.47, relheight=0.12)
   Label(menu_frames[6], bg="#26262e").place(relx=0.02, rely=0.405, relwidth=0.47, relheight=0.24)
   away_team_labels = []
   for i in range(3):
       away_team_labels.append(Label(menu_frames[6], bg=away_colour_one))
   away_team_labels[0].place(relx=0.105, rely=0.3, relwidth=0.3, relheight=0.04)
   away_team_labels[1].place(relx=0.105, rely=0.455, relwidth=0.3, relheight=0.04)
   away_team_labels[2].place(relx=0.105, rely=0.575, relwidth=0.3, relheight=0.04)

   # HEADINGS
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Possession").place(relx=0.02, rely=0.25, relwidth=0.47, relheight=0.05)
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Shots").place(relx=0.02, rely=0.405, relwidth=0.47, relheight=0.05)
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Shots On Target").place(relx=0.02, rely=0.525, relwidth=0.47, relheight=0.05)
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Commentary").place(relx=0.51, rely=0.5, relwidth=0.47, relheight=0.04)
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Assistant Manager").place(relx=0.765, rely=0.25, relwidth=0.215, relheight=0.04)
   Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Match Speed").place(relx=0.51, rely=0.37, relwidth=0.235, relheight=0.04)

   # VALUES
   home_name_label = Label(menu_frames[6], bg=home_colour_one, fg=home_colour_two, text="Home Team Name", font=("Comic Sans", 32, "bold"))
   home_name_label.place(relx=0.1, rely=0.045, relwidth=0.3, relheight=0.12)
   away_name_label = Label(menu_frames[6], bg=away_colour_one, fg=away_colour_two, text="Away Team Name", font=("Comic Sans", 32, "bold"))
   away_name_label.place(relx=0.6, rely=0.045, relwidth=0.3, relheight=0.12)
   home_score_label = Label(menu_frames[6], bg=home_colour_one, fg=home_colour_two, text="0", font=("Comic Sans", 80))
   home_score_label.place(relx=0.4, rely=0.045, relwidth=0.1, relheight=0.12)
   away_score_label = Label(menu_frames[6], bg=away_colour_one, fg=away_colour_two, text="0", font=("Comic Sans", 80))
   away_score_label.place(relx=0.5, rely=0.045, relwidth=0.1, relheight=0.12)
   time_label = Label(menu_frames[6], bg="#26262e", fg="white", text="0'", font=("Comic Sans", 25))
   time_label.place(relx=0.1, rely=0.165, relwidth=0.8, relheight=0.05)
   home_possession = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="50%")
   home_possession.place(relx=0.02, rely=0.29, relwidth=0.08, relheight=0.06)
   away_possession = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="50%")
   away_possession.place(relx=0.41, rely=0.29, relwidth=0.08, relheight=0.06)
   home_shots = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="0")
   home_shots.place(relx=0.02, rely=0.445, relwidth=0.08, relheight=0.06)
   away_shots = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="0")
   away_shots.place(relx=0.41, rely=0.445, relwidth=0.08, relheight=0.06)
   home_shotstarget = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="0")
   home_shotstarget.place(relx=0.02, rely=0.565, relwidth=0.08, relheight=0.06)
   away_shotstarget = Label(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 40), text="0")
   away_shotstarget.place(relx=0.41, rely=0.565, relwidth=0.08, relheight=0.06)
   home_possession_bar = Label(menu_frames[6], bg=home_colour_one)
   home_possession_bar.place(relx=0.105, rely=0.3, relwidth=0.15, relheight=0.04)
   home_shots_bar = Label(menu_frames[6], bg=home_colour_one)
   home_shots_bar.place(relx=0.105, rely=0.455, relwidth=0.15, relheight=0.04)
   home_shotstarget_bar = Label(menu_frames[6], bg=home_colour_one)
   home_shotstarget_bar.place(relx=0.105, rely=0.575, relwidth=0.15, relheight=0.04)
   commentary_text = Label(menu_frames[6], bg="#363440", text="", fg="white", font=("Comic sans", 14, "bold"))
   commentary_text.place(relx=0.51, rely=0.54, relwidth=0.47, relheight=0.1)
   commentary_text_two = Label(menu_frames[6], bg="#413F4B", text="", fg="white", font=("Comic sans", 11))
   commentary_text_two.place(relx=0.51, rely=0.64, relwidth=0.47, relheight=0.1)
   commentary_text_three = Label(menu_frames[6], bg="#363440", text="", fg="white", font=("Comic sans", 11))
   commentary_text_three.place(relx=0.51, rely=0.74, relwidth=0.47, relheight=0.1)
   assistant_text = Label(menu_frames[6], bg="#363440", text="", fg="white", font=("Comic sans", 15))
   assistant_text.place(relx=0.765, rely=0.29, relwidth=0.215, relheight=0.175)

   home_scorers_label = Label(menu_frames[6], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 14))
   away_scorers_label = Label(menu_frames[6], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 14))
   home_scorers_label.place(relx=0.1, rely=0.165, relwidth=0.35, relheight=0.05)
   away_scorers_label.place(relx=0.55, rely=0.165, relwidth=0.35, relheight=0.05)

   home_team_labels = [home_name_label, home_score_label, home_possession_bar, home_shots_bar, home_shotstarget_bar]
   away_team_labels.append(away_name_label)
   away_team_labels.append(away_score_label)

   # BUTTONS
   start_match_button = Button(menu_frames[6], bg="#2482d3", fg="white", font=("Comic Sans", 28), text="Start Match", command=match_start)
   start_match_button.place(relx=0.105, rely=0.73, relwidth=0.3, relheight=0.12)
   tactics_button = Button(menu_frames[6], bg="#26262e", fg="white", font=("Comic sans", 20), text="Change tactics\nand subs", command=go_to_tactics)
   tactics_button.place(relx=0.51, rely=0.25, relwidth=0.235, relheight=0.1)
   slow_speed_button = Button(menu_frames[6], bg="#363440", fg="white", font=("Comic sans", 16), text="Slow", bd=0, command=lambda: set_match_speed(SLOW_MATCH_SPEED))
   slow_speed_button.place(relx=0.51, rely=0.41, relwidth=0.0783, relheight=0.08)
   medium_speed_button = Button(menu_frames[6], bg="#363440", fg="white", font=("Comic sans", 16, "bold"), text="Medium", bd=0, command=lambda: set_match_speed(MEDIUM_MATCH_SPEED))
   medium_speed_button.place(relx=0.5883, rely=0.41, relwidth=0.0783, relheight=0.08)
   fast_speed_button = Button(menu_frames[6], bg="#363440", fg="white", font=("Comic sans", 16), text="Fast", bd=0, command=lambda: set_match_speed(FAST_MATCH_SPEED))
   fast_speed_button.place(relx=0.6666, rely=0.41, relwidth=0.0783, relheight=0.08)
   Button(menu_frames[6], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), text="Swap home\ncolours", command=do_swap_home_colours).place(relx=0.01, rely=0.08, relwidth=0.08, relheight=0.1)
   Button(menu_frames[6], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), text="Swap away\ncolours", command=do_swap_away_colours).place(relx=0.91, rely=0.08, relwidth=0.08, relheight=0.1)

   # function is initially called right after club submenu is placed as that is where club rating is done, also needs to be called after every match
   def calculate_attendance():
       club_rating_value = int(club_rating.cget("text").split("/")[0])

       # gets an initial attendance value before it is timesed by a value detemined by fan happiness
       if club_rating_value == 1:
           temp_attendance = random.randint(1000, 3000)
       elif club_rating_value == 2:
           temp_attendance = random.randint(2000, 4500)
       elif club_rating_value == 3:
           temp_attendance = random.randint(2500, 7000)
       elif club_rating_value == 4:
           temp_attendance = random.randint(3000, 8000)
       elif club_rating_value == 5:
           temp_attendance = random.randint(3500, 9000)
       elif club_rating_value == 6:
           temp_attendance = random.randint(4000, 11000)
       elif club_rating_value == 7:
           temp_attendance = random.randint(6000, 12500)
       elif club_rating_value == 8:
           temp_attendance = random.randint(7000, 13500)
       elif club_rating_value == 9:
           temp_attendance = random.randint(8000, 14500)
       elif club_rating_value == 10:
           temp_attendance = random.randint(8500, 15500)
       elif club_rating_value == 11:
           temp_attendance = random.randint(9000, 17000)
       elif club_rating_value == 12:
           temp_attendance = random.randint(1000, 19500)
       elif club_rating_value == 13:
           temp_attendance = random.randint(12500, 23500)
       elif club_rating_value == 14:
           temp_attendance = random.randint(14500, 26000)
       elif club_rating_value == 15:
           temp_attendance = random.randint(16500, 30000)
       elif club_rating_value == 16:
           temp_attendance = random.randint(19500, 35000)
       elif club_rating_value == 17:
           temp_attendance = random.randint(24000, 41000)
       elif club_rating_value == 18:
           temp_attendance = random.randint(38000, 48500)
       elif club_rating_value == 19:
           temp_attendance = random.randint(49000, 65000)
       elif club_rating_value == 20:
           temp_attendance = random.randint(70000, 95000)

       # adjusts attendance based on fan relations with the club
       if FAN_RELATION > 85:
           temp_attendance = int(temp_attendance * random.randint(106, 115) / 100)
       elif FAN_RELATION > 66:
           temp_attendance = int(temp_attendance * (random.randint(103, 108) / 100))
       elif FAN_RELATION < 5:
           temp_attendance = int(temp_attendance * 0.05)
       elif FAN_RELATION < 10:
           temp_attendance = int(temp_attendance * 0.15)
       elif FAN_RELATION < 15:
           temp_attendance = int(temp_attendance * 0.3)
       elif FAN_RELATION < 20:
           temp_attendance = int(temp_attendance * 0.55)
       elif FAN_RELATION < 33:
           temp_attendance = int(temp_attendance * (random.randint(65, 80) / 100))
       elif FAN_RELATION < 50:
           temp_attendance = int(temp_attendance * 0.9)

       # if capacity is more than stadium capacity or almost as much, assigns a value close to the stadium maximum capacity
       if temp_attendance > int(STADIUM_CAPACITY * 0.97):
           temp_attendance = int(STADIUM_CAPACITY * (random.randint(968, 985) / 1000))

       return temp_attendance

   simulate_lock = threading.Lock()

   def sim_button():
       global simulating, prev_player_negotiation

       sim_thread = threading.Thread(target=simulate)
       global simulate_button
       if simulating:
           simulating = False
           simulate_button.config(text="Simulate")
           update_squad_display()
           show_menu_buttons()

       elif not simulating:
           simulating = True
           simulate_button.config(text="Stop Simulating")
           hide_menu_buttons()
           # stops any ongoing negotiations and gives player negotiation cooldown
           for i in negotiation_labels:
               i.lift()
               i.config(text="")
           for i in negotiation_buttons:
               i.lift()
               i.config(text="", bg=LIGHT_UI_COLOUR, state="disabled")
           if prev_player_negotiation is not None:
               prev_player_negotiation.negotiation_cooldown = 14
               prev_player_negotiation = None

           sim_thread.start()

   def calc_opponent_strength():
       attack_strength = next_opponent[1] - team_defence_avg
       defence_strength = next_opponent[2] - team_attack_avg

       print("ATTACK STRENGTH, DEFENCE STRENGTH")
       print(attack_strength, defence_strength)

       for i in attack_strength_indicators:
           i.config(fg=LIGHT_UI_COLOUR)

       for i in defence_strength_indicators:
           i.config(fg=LIGHT_UI_COLOUR)

       if attack_strength > 6:
           attack_strength_indicators[4].config(fg="#00FF00")
       elif attack_strength > 2:
           attack_strength_indicators[3].config(fg="#BBFF00")
       elif attack_strength > -3:
           attack_strength_indicators[2].config(fg="#FFEE00")
       elif attack_strength > -7:
           attack_strength_indicators[1].config(fg="#FF7700")
       else:
           attack_strength_indicators[0].config(fg="#FF0000")

       if defence_strength > 6:
           defence_strength_indicators[4].config(fg="#00FF00")
       elif defence_strength > 2:
           defence_strength_indicators[3].config(fg="#BBFF00")
       elif defence_strength > -3:
           defence_strength_indicators[2].config(fg="#FFEE00")
       elif defence_strength > -7:
           defence_strength_indicators[1].config(fg="#FF7700")
       else:
           defence_strength_indicators[0].config(fg="#FF0000")

   def place_matches():
       global simulate_button
       global year_label
       global month_label
       global next_match_day
       global next_match_month
       global home_team_name
       global away_team_name
       global competition_name
       global match_date
       global next_opponent
       global next_opponent_analysis_label, next_opponent_league_label, opponent_attack_style_label, opponent_mentality_style_label, attack_strength_indicators, defence_strength_indicators
       global opponent_strengths_labels, opponent_weaknesses_labels

       next_match_day = 28
       next_match_month = 7

       def go_to_schedule():
           # stops simulating if it is ongoing
           if simulate_button.cget("text") == "Stop Simulating":
               sim_button()
           change_menu(10)
           hide_menu_buttons_grey()

       # BACKGROUNDS
       Label(menu_frames[0], bg="#363440").place(relx=0.23, rely=0.02, relwidth=0.75, relheight=0.3)
       Label(menu_frames[0], bg="#363440").place(relx=0.23, rely=0.34, relwidth=0.375, relheight=0.49)
       Label(menu_frames[0], bg="#363440").place(relx=0.625, rely=0.34, relwidth=0.355, relheight=0.49)

       # LABELS
       Label(menu_frames[0], bg="#363440", text="Today\n▼", font=("Comic Sans", 15), fg="white").place(relx=0.58, rely=0.103, relwidth=0.05, relheight=0.05)
       Label(menu_frames[0], bg="#26262e", text="Next Match", font=("Comic Sans", 24), fg="white").place(relx=0.23, rely=0.34, relwidth=0.375, relheight=0.08)
       Label(menu_frames[0], bg="#26262e", text="Opponent Overview", font=("Comic Sans", 24), fg="white").place(relx=0.625, rely=0.34, relwidth=0.355, relheight=0.08)
       Label(menu_frames[0], bg="#363440", text="vs", font=("Comic Sans", 19), fg="white").place(relx=0.41, rely=0.48, relwidth=0.015, relheight=0.03)
       simulate_button = Button(menu_frames[0], bg="#2482d3", fg="white", font=("Comic Sans", 20), text="Simulate", command=sim_button)
       simulate_button.place(relx=0.505, rely=0.26, relwidth=0.2, relheight=0.05)
       # next team attack strength
       Label(menu_frames[0], bg="#FF0000").place(relx=0.635, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#FF7700").place(relx=0.6665, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#FFEE00").place(relx=0.698, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#BBFF00").place(relx=0.7295, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#00FF00").place(relx=0.761, rely=0.56, relwidth=0.0315, relheight=0.051)
       attack_strength_indicators = []
       attack_strength_indicators.append(Label(menu_frames[0], fg="#FF0000", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       attack_strength_indicators.append(Label(menu_frames[0], fg="#FF7700", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       attack_strength_indicators.append(Label(menu_frames[0], fg="#FFEE00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       attack_strength_indicators.append(Label(menu_frames[0], fg="#BBFF00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       attack_strength_indicators.append(Label(menu_frames[0], fg="#00FF00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))

       attack_strength_indicators[0].place(relx=0.635, rely=0.615, relwidth=0.0315, relheight=0.03)
       attack_strength_indicators[1].place(relx=0.6665, rely=0.615, relwidth=0.0315, relheight=0.03)
       attack_strength_indicators[2].place(relx=0.698, rely=0.615, relwidth=0.0315, relheight=0.03)
       attack_strength_indicators[3].place(relx=0.7295, rely=0.615, relwidth=0.0315, relheight=0.03)
       attack_strength_indicators[4].place(relx=0.761, rely=0.615, relwidth=0.0315, relheight=0.03)

       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 10), text="Weak\nAttack").place(relx=0.635, rely=0.52, relwidth=0.0315, relheight=0.04)
       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 10), text="Strong\nAttack").place(relx=0.761, rely=0.52, relwidth=0.0315, relheight=0.04)

       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14, "bold"), text="Play Style").place(relx=0.625, rely=0.68, relwidth=0.1183, relheight=0.04)
       opponent_attack_style_label = Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 12), text="")
       opponent_attack_style_label.place(relx=0.625, rely=0.74, relwidth=0.1183, relheight=0.04)

       # opponent strengths and weaknesses
       opponent_strengths_labels = []
       opponent_weaknesses_labels = []

       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14, "bold"), text="Strengths").place(relx=0.7433, rely=0.68, relwidth=0.1183, relheight=0.04)
       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14, "bold"), text="Weaknesses").place(relx=0.8616, rely=0.68, relwidth=0.1183, relheight=0.04)

       opponent_strengths_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="green", font=("Comic sans", 12), text="Hi"))
       opponent_strengths_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="green", font=("Comic sans", 12), text="Hi"))
       opponent_strengths_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="green", font=("Comic sans", 12), text="Hi"))

       opponent_weaknesses_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="red", font=("Comic sans", 12), text="Hi"))
       opponent_weaknesses_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="red", font=("Comic sans", 12), text="Hi"))
       opponent_weaknesses_labels.append(Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="red", font=("Comic sans", 12), text="Hi"))

       opponent_strengths_labels[0].place(relx=0.7433, rely=0.725, relwidth=0.1183, relheight=0.03)
       opponent_strengths_labels[1].place(relx=0.7433, rely=0.755, relwidth=0.1183, relheight=0.03)
       opponent_strengths_labels[2].place(relx=0.7433, rely=0.785, relwidth=0.1183, relheight=0.03)

       opponent_weaknesses_labels[0].place(relx=0.8616, rely=0.725, relwidth=0.1183, relheight=0.03)
       opponent_weaknesses_labels[1].place(relx=0.8616, rely=0.755, relwidth=0.1183, relheight=0.03)
       opponent_weaknesses_labels[2].place(relx=0.8616, rely=0.785, relwidth=0.1183, relheight=0.03)

       # next team defence strength
       Label(menu_frames[0], bg="#00FF00").place(relx=0.8125, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#BBFF00").place(relx=0.844, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#FFEE00").place(relx=0.8755, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#FF7700").place(relx=0.907, rely=0.56, relwidth=0.0315, relheight=0.051)
       Label(menu_frames[0], bg="#FF0000").place(relx=0.9385, rely=0.56, relwidth=0.0315, relheight=0.051)
       defence_strength_indicators = []
       defence_strength_indicators.append(Label(menu_frames[0], fg="#FF0000", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       defence_strength_indicators.append(Label(menu_frames[0], fg="#FF7700", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       defence_strength_indicators.append(Label(menu_frames[0], fg="#FFEE00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       defence_strength_indicators.append(Label(menu_frames[0], fg="#BBFF00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))
       defence_strength_indicators.append(Label(menu_frames[0], fg="#00FF00", bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic sans", 15)))

       defence_strength_indicators[0].place(relx=0.9385, rely=0.615, relwidth=0.0315, relheight=0.03)
       defence_strength_indicators[1].place(relx=0.907, rely=0.615, relwidth=0.0315, relheight=0.03)
       defence_strength_indicators[2].place(relx=0.8755, rely=0.615, relwidth=0.0315, relheight=0.03)
       defence_strength_indicators[3].place(relx=0.844, rely=0.615, relwidth=0.0315, relheight=0.03)
       defence_strength_indicators[4].place(relx=0.8125, rely=0.615, relwidth=0.0315, relheight=0.03)

       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 10), text="Weak\nDefence").place(relx=0.9385, rely=0.52, relwidth=0.0315, relheight=0.04)
       Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 10), text="Strong\nDefence").place(relx=0.8125, rely=0.52, relwidth=0.0315, relheight=0.04)
       # view match schedule button
       Button(menu_frames[0], text="View Schedule", fg="white", bg=BUTTON_COLOUR, font=("Comic sans", 20), command=go_to_schedule).place(relx=0.3275, rely=0.72, relwidth=0.18, relheight=0.08)

       # VALUES
       year_label = Label(menu_frames[0], bg="#26262e", text=f"Year: {year}", font=("Comic Sans", 22, "bold"), fg="white")
       year_label.place(relx=0.23, rely=0.02, relwidth=0.75, relheight=0.05)
       month_label = Label(menu_frames[0], bg="#26262e", text=f"Month: {months[month-1]}", font=("Comic Sans", 18), fg="white")
       month_label.place(relx=0.23, rely=0.07, relwidth=0.75, relheight=0.035)
       home_team_name = Label(menu_frames[0], bg="#363440", text="", font=("Comic Sans", 18, "bold"), fg="white")
       home_team_name.place(relx=0.23, rely=0.47, relwidth=0.18, relheight=0.05)
       away_team_name = Label(menu_frames[0], bg="#363440", text="", font=("Comic Sans", 18, "bold"), fg="white")
       away_team_name.place(relx=0.425, rely=0.47, relwidth=0.18, relheight=0.05)
       competition_name = Label(menu_frames[0], bg="#363440", text="League", font=("Comic Sans", 18), fg="white")
       competition_name.place(relx=0.23, rely=0.56, relwidth=0.375, relheight=0.05)
       match_date = Label(menu_frames[0], bg="#363440", text=f"{next_match_day} {months[next_match_month-1]} {year}", font=("Comic Sans", 18), fg="white")
       match_date.place(relx=0.23, rely=0.62, relwidth=0.375, relheight=0.03)
       match_televised = Label(menu_frames[0], bg="#363440", text="This match will not be televised", font=("Comic Sans", 15), fg="white")
       match_televised.place(relx=0.23, rely=0.67, relwidth=0.375, relheight=0.03)
       next_opponent_analysis_label = Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18, "bold"), text="")
       next_opponent_analysis_label.place(relx=0.65, rely=0.42, relwidth=0.305, relheight=0.04)
       next_opponent_league_label = Label(menu_frames[0], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text="")
       next_opponent_league_label.place(relx=0.65, rely=0.46, relwidth=0.305, relheight=0.03)
   place_matches()

   def get_min_youth_value():
       club_rating_value = int(club_rating.cget("text").split("/")[0])
       if club_rating_value == 1:
           min_value = 35
       elif club_rating_value == 2:
           min_value = 40
       elif club_rating_value == 3:
           min_value = 50
       elif club_rating_value == 4:
           min_value = 60
       elif club_rating_value == 5:
           min_value = 75
       elif club_rating_value == 6:
           min_value = 85
       elif club_rating_value == 7:
           min_value = 95
       elif club_rating_value == 8:
           min_value = 110
       elif club_rating_value == 9:
           min_value = 120
       elif club_rating_value == 10:
           min_value = 135
       elif club_rating_value == 11:
           min_value = 150
       elif club_rating_value == 12:
           min_value = 165
       elif club_rating_value == 13:
           min_value = 180
       elif club_rating_value == 14:
           min_value = 195
       elif club_rating_value == 15:
           min_value = 210
       elif club_rating_value == 16:
           min_value = 235
       elif club_rating_value == 17:
           min_value = 245
       elif club_rating_value == 18:
           min_value = 265
       elif club_rating_value == 19:
           min_value = 285
       elif club_rating_value == 20:
           min_value = 300

       return min_value

   def remove_youth_player(youth_player):
       youth_players.remove(youth_player)
       update_youth_frames()

   def display_youth_frame_info(youth_player, frame):

       Label(frame, text=youth_player.first_name + " " + youth_player.last_name, font=("Comic sans", 15), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0, rely=0, relwidth=0.3, relheight=1)
       Label(frame, text="Ovr", font=("Comic sans", 13), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.3, rely=0, relwidth=0.05, relheight=1)
       Label(frame, text=youth_player.ovr, font=("Comic sans", 20, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.35, rely=0, relwidth=0.07, relheight=1)
       Label(frame, text="Age", font=("Comic sans", 13), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.42, rely=0, relwidth=0.05, relheight=1)
       Label(frame, text=youth_player.age, font=("Comic sans", 20, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.47, rely=0, relwidth=0.07, relheight=1)
       Label(frame, text="Pos", font=("Comic sans", 13), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.54, rely=0, relwidth=0.05, relheight=1)
       Label(frame, text=youth_player.pos, font=("Comic sans", 20, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.59, rely=0, relwidth=0.07, relheight=1)
       if len(squad) < MAX_SQUAD_SIZE:
           Button(frame, text="Promote", bg="lime", fg="white", font=("Comic sans", 17), bd=0, command=lambda: negotiate_player_contract(youth_player)).place(relx=0.66, rely=0, relwidth=0.17, relheight=1)
       else:
           Label(frame, text="Main squad\nfull", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 17), bd=0).place(relx=0.66, rely=0, relwidth=0.17, relheight=1)
       Button(frame, text="Remove", bg="red", fg="white", font=("Comic sans", 17), bd=0, command=lambda: remove_youth_player(youth_player)).place(relx=0.83, rely=0, relwidth=0.17, relheight=1)

   def update_youth_frames():
       # clears all frames
       for i in youth_player_frames:
           for child in i.winfo_children():
               child.destroy()


       # populates frames with all youth players
       for i in range(len(youth_players)):
           display_youth_frame_info(youth_players[i], youth_player_frames[i])

   # used to get value for deciding how often a scout finds a player
   scout_search_value = {"Any": 10, "Squad Depth Player": 10, "Rotation Player": 9, "Competitive Starter": 8, "Strong Starter": 6, "Team Superstar": 5}

   def scout_new_player(scout, scout_search_type):
       if scout == scout_one:
           scout_age_search = scout_one_instructions[0]
           scout_pos_search = scout_one_instructions[2]
       elif scout == scout_two:
           scout_age_search = scout_two_instructions[0]
           scout_pos_search = scout_two_instructions[2]
       else:
           scout_age_search = scout_three_instructions[0]
           scout_pos_search = scout_three_instructions[2]

       # gets an age for the player
       if scout_age_search == "Older Cheaper Players":
           scouted_player_age = random.randint(30, 35)
       elif scout_age_search == "Experienced Developed Players":
           scouted_player_age = random.randint(24, 29)
       elif scout_age_search == "Young Talents":
           scouted_player_age = random.randint(17, 23)
       else:
           scouted_player_age = random.randint(17, 35)

       # gets an ovr for the player
       if scout_search_type == "Team Superstar":
           scouted_player_ovr = team_avg_rating + random.randint(2, 6)
       elif scout_search_type == "Strong Starter":
           scouted_player_ovr = team_avg_rating + random.randint(0, 2)
       elif scout_search_type == "Competitive Starter":
           scouted_player_ovr = team_avg_rating - random.randint(0, 3)
       elif scout_search_type == "Rotation Player":
           scouted_player_ovr = team_avg_rating - random.randint(4, 6)
       elif scout_search_type == "Squad Depth Player":
           scouted_player_ovr = team_avg_rating - random.randint(7, 11)
       else:
           scouted_player_ovr = team_avg_rating + random.randint(-11, 6)

       # gets a pos for the player
       if scout_pos_search == "Any":
           scouted_player_pos = random.choice(["GK", "LB", "CB", "RB", "DM", "CM", "AM", "LF", "RF", "CF"])
       elif scout_pos_search == "Defence":
           scouted_player_pos = random.choice(["LB", "CB", "RB"])
       elif scout_pos_search == "Midfield":
           scouted_player_pos = random.choice(["DM", "CM", "AM"])
       elif scout_pos_search == "Attack":
           scouted_player_pos = random.choice(["LF", "RF", "CF"])
       else:
           scouted_player_pos = scout_pos_search

       # generates the scouted player
       scouted_player = gen_player_custom_age(scouted_player_ovr, scouted_player_pos, scouted_player_age)
       # gets extension length offer for player transfer negotiations
       scouted_player.get_extension_length_offer()
       if scout == scout_one:
           scout_one_players.append(scouted_player)
           update_scout_one_frames()
       elif scout == scout_two:
           scout_two_players.append(scouted_player)
           update_scout_two_frames()
       elif scout == scout_three:
           scout_three_players.append(scouted_player)
           update_scout_three_frames()

   def decline_transfer_offer():
       for child in transfer_offer_frame.winfo_children():
           child.destroy()

   def attempt_transfer_offer():
       pick_squad_player = False
       if not len(transfer_listed_players) == 0:
           chosen_listed_player = random.choice(transfer_listed_players)
           min_value = ((chosen_listed_player.age / 3) * 8) + 3
           if random.randint(1, 100) > min_value:
               transfer_offer_for_player(chosen_listed_player, int(chosen_listed_player.getValue() * (random.randint(93, 102) / 100) * 1000000))
           else:
               pick_squad_player = True
       else:
           pick_squad_player = True

       if pick_squad_player:
           chosen_listed_player = random.choice(squad)
           min_value = ((chosen_listed_player.age/3) * 8) + 3
           if random.randint(1,100) > min_value:
               if random.randint(1, 100) > 65:
                   transfer_offer_for_player(chosen_listed_player, int(chosen_listed_player.getValue() * (random.randint(93, 102) / 100) * 1000000))

   focus_variables = {"Counter Attacking": counter_attacking, "High Tempo Passing": high_tempo_passing, "Wing Play": wing_play, "Passing Over The Top": passing_over_the_top,
                      "Playing Out Of Press": playing_out_of_press, "Defending Crosses": defending_crosses, "Defending Deep": defending_deep, "Pressing": pressing,
                      "Set Pieces": set_pieces, "Ball Possession": ball_possession}

   def update_training_globals():
       global counter_attacking, high_tempo_passing, wing_play, passing_over_the_top, playing_out_of_press, defending_crosses, defending_deep, pressing, set_pieces, ball_possession
       for key, value in focus_variables.items():
           globals()[key.lower().replace(" ", "_")] = value

   def training_day(type):
       focuses = [None, None, None]
       intensity = None
       warm_up = None

       def do_tactical_training():
           for key in focus_variables:
               focus_variables[key] -= 1

           focus_variables[focuses[0]] += 4
           focus_variables[focuses[1]] += 3
           focus_variables[focuses[2]] += 3

           # stops variables from going over 100
           overflow_occured = False
           if focus_variables[focuses[0]] > 100:
               difference = focus_variables[focuses[0]] - 100
               focus_variables[focuses[0]] = 100
               overflow_occured = True
           elif focus_variables[focuses[1]] > 100:
               difference = focus_variables[focuses[1]] - 100
               focus_variables[focuses[1]] = 100
               overflow_occured = True
           elif focus_variables[focuses[2]] > 100:
               difference = focus_variables[focuses[0]] - 100
               focus_variables[focuses[0]] = 100
               overflow_occured = True

           # randomly distributes excess points if needed
           if overflow_occured:
               while difference != 0:
                   chosen_value = random.choice(list(focus_variables.keys()))
                   while chosen_value in [focuses[0], focuses[1], focuses[2]]:
                       chosen_value = random.choice(list(focus_variables.keys()))
                   focus_variables[chosen_value] += 1
                   difference -= 1

           update_training_globals()

       if type == "TD":
           warm_up = TD_warm_up.get()
           intensity = TD_intensity.get()
           focuses = [TD_main_focus.get(), TD_second_focus.get(), TD_third_focus.get()]
       elif type == "BM":
           warm_up = BM_warm_up.get()
           intensity = BM_intensity.get()
           focuses = [BM_main_focus.get(), BM_second_focus.get(), BM_third_focus.get()]
       elif type == "PM":
           warm_up = PM_warm_up.get()
           intensity = PM_intensity.get()
           focuses = [PM_main_focus.get(), PM_second_focus.get(), PM_third_focus.get()]

       do_tactical_training()

       if intensity == "High":
           for i in squad:
               if i.injured == 0:
                   i.sharpness += random.randint(3, 5)
                   i.fitness -= random.randint(1, 3)
               else:
                   i.sharpness -= 4
                   i.fitness = 20
               if i.sharpness > 100:
                   i.sharpness = 100
               if i.fitness < 0:
                   i.fitness = 0
       elif intensity == "Medium":
           for i in squad:
               if i.sharpness > 60:
                   if i.injured == 0:
                       i.sharpness -= random.randint(2, 5)
                       i.fitness += random.randint(5, 8)
                   else:
                       i.sharpness -= 4
                       i.fitness = 20
               else:
                   if i.injured == 0:
                       i.sharpness += random.randint(1, 2)
                       i.fitness += random.randint(5, 8)
                   else:
                       i.sharpness -= 4
                       i.fitness = 20

               if i.sharpness < 0:
                   i.sharpness = 0
               elif i.sharpness > 100:
                   i.sharpness = 100

               if i.fitness > 100:
                   i.fitness = 100
       elif intensity == "Low":
           for i in squad:
               if i.injured == 0:
                   i.sharpness -= random.randint(9, 15)
                   i.fitness += random.randint(14, 17)
               else:
                   i.sharpness -= 4
                   i.fitness = 20
               if i.sharpness < 0:
                   i.sharpness = 0
               if i.fitness > 100:
                   i.fitness = 100

       if warm_up == "Short":
           for i in squad:
               if i.training_happiness < 99:
                   i.training_happiness += random.randint(1, 2)

               if random.randint(1, 350 + (physiotherapist.rating * 5)) == 2 and i.injured == 0 and i.pos != "GK":
                   i.injured = random.choice(injury_lengths)
                   i.injured = int(i.injured * ((100 - (physiotherapist.rating * 2)) / 100))
       elif warm_up == "Medium":
           for i in squad:
               if i.training_happiness > 50:
                   i.training_happiness -= random.randint(1, 2)
               elif i.training_happiness < 50:
                   i.training_happiness += random.randint(1, 2)
               if random.randint(1, 470 + (physiotherapist.rating * 5)) == 15 and i.injured == 0 and i.pos != "GK":
                   i.injured = random.choice(injury_lengths)
                   i.injured = int(i.injured * ((100 - (physiotherapist.rating * 2)) / 100))
       elif warm_up == "Long":
           for i in squad:
               if i.training_happiness > 1:
                   i.training_happiness -= random.randint(1, 2)
               if random.randint(1, 630 + (physiotherapist.rating * 5)) == 15 and i.injured == 0 and i.pos != "GK":
                   i.injured = random.choice(injury_lengths)
                   i.injured = int(i.injured * ((100 - (physiotherapist.rating * 2)) / 100))

   def update_morale():
       avg_morale = 0
       for i in squad:
           wage_difference = i.get_wage_offer() - i.wage
           wage_difference = wage_difference / i.wage
           if wage_difference > 0.8:
               i.wage_happiness = 20
           elif wage_difference > 0.6:
               i.wage_happiness = 40
           elif wage_difference > 0.5:
               i.wage_happiness = 60
           else:
               i.wage_happiness = 80
           club_difference = 0
           for j in sorted(squad, key=lambda player_object: player_object.ovr, reverse=True)[:11]:
               club_difference += j.ovr
           club_starting_rating = club_difference / 11
           club_difference = int(i.ovr - club_starting_rating)

           if club_difference > 10 and not club_starting_rating > 85:
               i.club_happiness = 20
           elif club_difference > 6 and not club_starting_rating > 87:
               i.club_happiness = 40
           elif club_difference > 3 and not club_starting_rating > 90:
               i.club_happiness = 60
           else:
               i.club_happiness = 80

           try:
               played_match_percent = int((i.matches_played / (i.matches_played + i.matches_not_played))*100)
               if club_difference > 3:
                   if played_match_percent < 50:
                       i.playing_time = 20
                   elif played_match_percent < 60:
                       i.playing_time = 40
                   elif played_match_percent < 70:
                       i.playing_time = 60
                   else:
                       i.playing_time = 80

               elif club_difference > -3:
                   if played_match_percent < 35:
                       i.playing_time = 20
                   elif played_match_percent < 45:
                       i.playing_time = 40
                   elif played_match_percent < 55:
                       i.playing_time = 60
                   else:
                       i.playing_time = 80

               elif club_difference > -9:
                   if played_match_percent < 10:
                       i.playing_time = 20
                   elif played_match_percent < 20:
                       i.playing_time = 40
                   elif played_match_percent < 25:
                       i.playing_time = 60
                   else:
                       i.playing_time = 80

               else:
                   if played_match_percent < 5:
                       i.playing_time = 20
                   elif played_match_percent < 10:
                       i.playing_time = 40
                   elif played_match_percent < 15:
                       i.playing_time = 60
                   else:
                       i.playing_time = 80

           except ZeroDivisionError:
               i.playing_time = 50

           if (i.matches_played + i.matches_not_played) < 8:
               i.playing_time = 50
           total_morale = i.training_happiness + i.club_happiness + i.wage_happiness + i.playing_time
           i.morale = int(total_morale/4)
           avg_morale += i.morale

       avg_morale = int(avg_morale/len(squad))

       if avg_morale > 60:
           player_relations.config(text="Good", fg="green")
       elif avg_morale > 30:
           player_relations.config(text="Okay", fg="yellow")
       else:
           player_relations.config(text="Bad", fg="red")

   def clear_scout_frames():
       for i in scout_one_frames:
           for j in i.winfo_children():
               j.destroy()

       for i in scout_two_frames:
           for j in i.winfo_children():
               j.destroy()

       for i in scout_three_frames:
           for j in i.winfo_children():
               j.destroy()

       for child in transfer_offer_frame.winfo_children():
           child.destroy()

       scout_one_players.clear()
       scout_two_players.clear()
       scout_three_players.clear()

   def update_player_report():
       ordered_squad = squad
       ordered_squad = sorted(ordered_squad, key=lambda i: i.form, reverse=True)

       player_report_widgets[3].config(text=f"{ordered_squad[0].first_name} {ordered_squad[0].last_name}")
       player_report_widgets[5].config(text=f"{ordered_squad[1].first_name} {ordered_squad[1].last_name}")
       player_report_widgets[7].config(text=f"{ordered_squad[2].first_name} {ordered_squad[2].last_name}")

       player_report_widgets[4].config(text=f"{ordered_squad[-1].first_name} {ordered_squad[-1].last_name}")
       player_report_widgets[6].config(text=f"{ordered_squad[-2].first_name} {ordered_squad[-2].last_name}")
       player_report_widgets[8].config(text=f"{ordered_squad[-3].first_name} {ordered_squad[-3].last_name}")

       for i in squad:
           print(i.form, i.first_name, i.last_name)

       sort_squad_pos()

   def simulate():
       global year_label, month_label, month, year, simulate_button, next_match_day, next_match_month, simulating, wage_pay_day_count, wage_loss_label, stwage_loss_label, cost_loss_label, TOTAL_MERCH_REVENUE, youth_centre_heading, youth_players, youth_player_frames, day_of_training, transfers_open
       # simulation process
       # lock stops while loop from activating simultaneously with itself leading to incorrectly timed spaces in simulation
       with simulate_lock:
           while simulating:
               time.sleep(1)
               # first stops simulation if button is meant to, then next if statement stops simulation if it is matchday
               if simulate_button.cget("text") == "Simulate":
                   break
               elif day_curr.cget("text") == next_match_day and month == next_match_month:
                   if squad_confirmed:
                       simulate_button.config(text="Go to match", command=enter_match, bg=BUTTON_COLOUR)
                   else:
                       simulate_button.config(text="Squad Not Confirmed", command=go_to_fortfeit, bg="red")
                   simulating = False
                   show_menu_buttons()
                   update_squad_display()
                   break
               elif day_curr.cget("text") == 1 and month == 1 and not transfers_open:
                   popup_message.config(text="The board is informing you that the transfer window is now open.\nDuring this time you may negotiate with other clubs to\nbuy and sell players.\n\nThe window is open from today and will close on February 1st.")
                   change_menu(12)
                   hide_menu_buttons_grey()
                   transfers_open = True
                   break
               elif day_curr.cget("text") == 1 and month == 9 and transfers_open:
                   popup_message.config(text="The board is informing you that the transfer window is now closed.\nThe squad you will work with is now decided until the next transfer window\nKeep in mind, you may still promote players from the youth academy.\n\nThe next transfer window will open on January 1st.")
                   change_menu(12)
                   hide_menu_buttons_grey()
                   transfers_open = False
                   clear_scout_frames()
                   break
               elif day_curr.cget("text") == 1 and month == 2 and transfers_open:
                   popup_message.config(text="The board is informing you that the transfer window is now closed.\nThe squad you will work with is now decided until the next transfer window\nKeep in mind, you may still promote players from the youth academy.\n\nThe next transfer window will open on July 1st.")
                   change_menu(12)
                   hide_menu_buttons_grey()
                   transfers_open = False
                   clear_scout_frames()
                   break
               elif day_curr.cget("text") == 1 and month == 7 and not transfers_open:
                   season_start_menu()
                   transfers_open = True
                   break

               print("-----------")

               for i in squad:
                   if i.negotiation_cooldown != 0:
                       i.negotiation_cooldown -= 1

                   if i.injured > 0:
                       i.injured -= 1

                   if month == i.month and int(day_curr.cget("text")) == i.day:
                       i.age += 1

               for i in youth_players:
                   if i.negotiation_cooldown != 0:
                       i.negotiation_cooldown -= 1

               for i in scout_one_players:
                   if i.negotiation_cooldown != 0:
                       i.negotiation_cooldown -= 1

               for i in scout_two_players:
                   if i.negotiation_cooldown != 0:
                       i.negotiation_cooldown -= 1

               for i in scout_three_players:
                   if i.negotiation_cooldown != 0:
                       i.negotiation_cooldown -= 1

               if day_of_training == 1:
                   training_day("TD")
                   day_of_training = 2
               elif day_of_training == 2:
                   training_day("BM")
                   day_of_training = 3
               elif day_of_training == 3:
                   training_day("PM")
                   day_of_training = 1

               update_morale()

               team_report = get_team_training_report()
               strengths = team_report[1]
               weaknesses = team_report[0]
               team_strength_one.config(text=strengths[0])
               team_strength_two.config(text=strengths[1])
               team_strength_three.config(text=strengths[2])
               team_weakness_one.config(text=weaknesses[0])
               team_weakness_two.config(text=weaknesses[1])
               team_weakness_three.config(text=weaknesses[2])

               # decides for each scout whether or not they find a new player
               for scout in scouts:
                   player_scoutable = True
                   if scout == scout_one:
                       search_type = scout_one_instructions[1]
                       if len(scout_one_players) >= 4:
                           player_scoutable = False
                   elif scout == scout_two:
                       search_type = scout_two_instructions[1]
                       if len(scout_two_players) >= 4:
                           player_scoutable = False
                   else:
                       search_type = scout_two_instructions[1]
                       if len(scout_three_players) >= 4:
                           player_scoutable = False

                   random_scout_new_player = random.randint(1, 100)
                   max_scout_new_player_value = (chief_scout.rating + scout.rating) / 2 + scout_search_value[search_type]
                   print(f"Scout search type: {scout_search_value[search_type]}")

                   print(f"Scout random value:{random_scout_new_player} maximum value: {max_scout_new_player_value}")

                   if random_scout_new_player < max_scout_new_player_value and player_scoutable and transfers_open:
                       # scout a player for that scout
                       scout_new_player(scout, search_type)

               if len(squad) > MIN_SQUAD_SIZE and transfers_open:
                   attempt_transfer_offer()

               # pays players and staff wages every 7 days
               wage_pay_day_count -= 1
               if wage_pay_day_count == 0:
                   wage_pay_day_count = 7
                   total_wage_paid = int(extract_digits(wage_paid_label.cget("text")))
                   players_wage_paid = 0
                   for i in squad:
                       players_wage_paid += int(i.wage * 1000)
                       if i.injured == 0:
                           i.update_ovr()
                   for i in released_players:
                       players_wage_paid += int(i.wage * 1000)
                   staff_wage_paid = total_wage_paid - players_wage_paid
                   total_facility_wage = current_training_maintenance + current_youth_maintenance + STADIUM_MAINTAIN_COST
                   # gets amount of merch profit for the week out of the total merch profit for the season
                   merch_profit = int(TOTAL_MERCH_REVENUE * (random.randint(3, 12) / 100))
                   TOTAL_MERCH_REVENUE -= merch_profit
                   add_loss(players_wage_paid, wage_loss_label, False)
                   add_loss(staff_wage_paid, stwage_loss_label, False)
                   add_loss(total_facility_wage, cost_loss_label, False)
                   add_profit(merch_profit, merch_income_label, False)

                   # YOUTH ACADEMY PLAYER GENERATION
                   club_rating_value = int(club_rating.cget("text").split("/")[0])
                   youth_centre_level = int(extract_digits(youth_centre_heading.cget("text")))

                   youth_player_random_value = (club_rating_value * random.randint(5, 10)) + (youth_centre_level * random.randint(5, 10)) + (youth_coach.rating * random.randint(5, 10))
                   min_value = get_min_youth_value()

                   if youth_player_random_value >= min_value and not len(youth_players) > 5:
                       # generates youth player and gets random overall and position
                       youth_ovr = int((youth_player_random_value - 170) * 0.1 + 54) # 54
                       youth_pos = random.choice(["GK", "LB", "CB", "RB", "DM", "CM", "AM", "LF", "RF", "CF"])
                       youth_players.append(gen_youth_player(youth_ovr, youth_pos))

                       update_youth_frames()

               day_prev_2.config(text=int(day_prev_1.cget("text")))
               day_prev_1.config(text=int(day_curr.cget("text")))
               day_curr.config(text=int(day_next_1.cget("text")))
               day_next_1.config(text=int(day_next_2.cget("text")))
               day_next_2.config(text=int(day_next_2.cget("text")) + 1)
               if month == 2:
                   feb_length = 29 if year % 4 == 0 else 28
                   if int(day_next_2.cget("text")) > feb_length:
                       day_next_2.config(text="1")

               elif month in [4, 6, 9, 11]:
                   if int(day_next_2.cget("text")) > 30:
                       day_next_2.config(text="1")

               else:
                   if int(day_next_2.cget("text")) > 31:
                       day_next_2.config(text="1")

               if int(day_curr.cget("text")) == 1:
                   month += 1
                   if month > 12:
                       month = 1
                       year += 1
                       year_label.config(text=f"Year: {year}")
                   month_label.config(text=f"Month: {months[month - 1]}")

   day_prev_2 = Label(menu_frames[0], text=29, font=("Comic Sans", 38), fg="white", bg="#363440")
   day_prev_2.place(relx=0.32, rely=0.15, relwidth=0.05, relheight=0.08)
   day_prev_1 = Label(menu_frames[0], text=30, font=("Comic Sans", 38), fg="white", bg="#363440")
   day_prev_1.place(relx=0.45, rely=0.15, relwidth=0.05, relheight=0.08)
   day_curr = Label(menu_frames[0], text=1, font=("Comic Sans", 38), fg="white", bg="#26262e")
   day_curr.place(relx=0.58, rely=0.15, relwidth=0.05, relheight=0.08)
   day_next_1 = Label(menu_frames[0], text=2, font=("Comic Sans", 38), fg="white", bg="#363440")
   day_next_1.place(relx=0.71, rely=0.15, relwidth=0.05, relheight=0.08)
   day_next_2 = Label(menu_frames[0], text=3, font=("Comic Sans", 38), fg="white", bg="#363440")
   day_next_2.place(relx=0.84, rely=0.15, relwidth=0.05, relheight=0.08)

   simulate()

   # upgrade staff message submenu
   upgrade_staff_button = Button(menu_frames[9], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade")
   upgrade_staff_button.place(relx=0.25, rely=0.75, relwidth=0.2, relheight=0.1)
   cancel_upgrade_staff_button = Button(menu_frames[9], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Cancel")
   cancel_upgrade_staff_button.place(relx=0.55, rely=0.75, relwidth=0.2, relheight=0.1)
   confirm_staff_upgrade_label = Label(menu_frames[9], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 16))
   confirm_staff_upgrade_label.place(relx=0, rely=0, relwidth=1, relheight=0.2)

   upgrade_staff_labels = []
   upgrade_staff_labels.append(Label(menu_frames[9], text="Upgrade cost:", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20)))
   upgrade_staff_labels[0].place(relx=0.2, rely=0.2, relwidth=0.25, relheight=0.08)
   upgrade_staff_labels.append(Label(menu_frames[9], text="Current rating:", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20)))
   upgrade_staff_labels[1].place(relx=0.2, rely=0.3, relwidth=0.25, relheight=0.08)
   upgrade_staff_labels.append(Label(menu_frames[9], text="Current wage:", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20)))
   upgrade_staff_labels[2].place(relx=0.2, rely=0.4, relwidth=0.25, relheight=0.08)
   upgrade_staff_labels.append(Label(menu_frames[9], text="New rating", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20)))
   upgrade_staff_labels[3].place(relx=0.2, rely=0.5, relwidth=0.25, relheight=0.08)
   upgrade_staff_labels.append(Label(menu_frames[9], text="New wage", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20)))
   upgrade_staff_labels[4].place(relx=0.2, rely=0.6, relwidth=0.25, relheight=0.08)

   staff_upgrade_cost_label = Label(menu_frames[9], text="N/A", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"))
   staff_upgrade_cost_label.place(relx=0.6, rely=0.2, relwidth=0.15, relheight=0.08)
   staff_current_rating_label = Label(menu_frames[9], text="N/A", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"))
   staff_current_rating_label.place(relx=0.6, rely=0.3, relwidth=0.15, relheight=0.08)
   staff_current_wage_label = Label(menu_frames[9], text="N/A", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"))
   staff_current_wage_label.place(relx=0.6, rely=0.4, relwidth=0.15, relheight=0.08)
   staff_new_rating_label = Label(menu_frames[9], text="N/A", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"))
   staff_new_rating_label.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.08)
   staff_new_wage_label = Label(menu_frames[9], text="N/A", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"))
   staff_new_wage_label.place(relx=0.6, rely=0.6, relwidth=0.15, relheight=0.08)

   def place_club():
       global sponsor_name, sponsor_revenue, league_objective, domestic_objective, continental_objective, club_rating, fan_relations, player_relations

       sponsor_names = ["Apex Fitness", "Velocity Gear", "Stellar Entertainment", "Horizon Banking", "Fusion Automotive",
                        "PowerUp Electronics", "Nova Healthcare", "Quantum Gaming", "Alpine Tours", "Zenith Insurance", "Virtuoso Music", "Spectrum Finance"]
       # BACKGROUNDS
       Label(menu_frames[3], bg="#363440").place(relx=0.02, rely=0.07, relwidth=0.192, relheight=0.2)
       Label(menu_frames[3], bg="#302E39").place(relx=0.212, rely=0.07, relwidth=0.192, relheight=0.2)
       Label(menu_frames[3], bg="#363440").place(relx=0.404, rely=0.07, relwidth=0.192, relheight=0.2)
       Label(menu_frames[3], bg="#302E39").place(relx=0.596, rely=0.07, relwidth=0.192, relheight=0.2)
       Label(menu_frames[3], bg="#363440").place(relx=0.788, rely=0.07, relwidth=0.192, relheight=0.2)
       Label(menu_frames[3], bg="#363440").place(relx=0.02, rely=0.29, relwidth=0.3, relheight=0.35)
       Label(menu_frames[3], bg="#26262e").place(relx=0.32, rely=0.29, relwidth=0.18, relheight=0.35)
       Label(menu_frames[3], bg="#363440").place(relx=0.52, rely=0.29, relwidth=0.46, relheight=0.525)
       Label(menu_frames[3], bg="#363440").place(relx=0.02, rely=0.66, relwidth=0.23, relheight=0.155)
       Label(menu_frames[3], bg="#363440").place(relx=0.27, rely=0.66, relwidth=0.23, relheight=0.155)

       youth_main_frame = Frame(menu_frames[3], bg=LIGHT_UI_COLOUR)
       youth_main_frame.place(relx=0.52, rely=0.34, relwidth=0.46, relheight=0.475)

       for i in range(6):
           youth_player_frames.append(Frame(youth_main_frame, bg=LIGHT_UI_COLOUR, width=SCREEN_WIDTH * 0.46, height=window.winfo_screenheight()*0.079))
           youth_player_frames[-1].grid(row=i, column=0)

       # HEADINGS
       Label(menu_frames[3], bg="#26262e", text="Staff", fg="white", font=("Comic Sans", 20)).place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text="Fitness Coach", fg="white", font=("Comic Sans", 18)).place(relx=0.02, rely=0.07, relwidth=0.192, relheight=0.03)
       Label(menu_frames[3], bg="#302E39", text="Physiotherapist", fg="white", font=("Comic Sans", 18)).place(relx=0.212, rely=0.07, relwidth=0.192, relheight=0.03)
       Label(menu_frames[3], bg="#363440", text="Chief Analyst", fg="white", font=("Comic Sans", 18)).place(relx=0.404, rely=0.07, relwidth=0.192, relheight=0.03)
       Label(menu_frames[3], bg="#302E39", text="Goalkeeper Coach", fg="white", font=("Comic Sans", 18)).place(relx=0.596, rely=0.07, relwidth=0.192, relheight=0.03)
       Label(menu_frames[3], bg="#363440", text="Youth Coach", fg="white", font=("Comic Sans", 18)).place(relx=0.788, rely=0.07, relwidth=0.192, relheight=0.03)
       Label(menu_frames[3], bg="#363440", text="Conditions players' fitness and sharpness\nand helps them avoid injuries", fg="white", font=("Comic Sans", 11)).place(relx=0.02, rely=0.21, relwidth=0.192, relheight=0.06)
       Label(menu_frames[3], bg="#302E39", text="Helps players recover from injuries\nand avoid a recurring injury", fg="white", font=("Comic Sans", 11)).place(relx=0.212, rely=0.21, relwidth=0.192, relheight=0.06)
       Label(menu_frames[3], bg="#363440", text="Helps prepare your players tactically for\nmatches to give your team an upper hand", fg="white", font=("Comic Sans", 11)).place(relx=0.404, rely=0.21, relwidth=0.192, relheight=0.06)
       Label(menu_frames[3], bg="#302E39", text="Trains your goalkeepers and prepares\nthem properly for matches", fg="white", font=("Comic Sans", 11)).place(relx=0.596, rely=0.21, relwidth=0.192, relheight=0.06)
       Label(menu_frames[3], bg="#363440", text="Works with the youth team to improve the\nplayers and maximise talents coming through", fg="white", font=("Comic Sans", 11)).place(relx=0.788, rely=0.21, relwidth=0.192, relheight=0.06)
       Label(menu_frames[3], bg="#363440", text="Board Expectations", fg="white", font=("Comic Sans", 18)).place(relx=0.02, rely=0.29, relwidth=0.3, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Relations", fg="white", font=("Comic Sans", 18)).place(relx=0.32, rely=0.29, relwidth=0.18, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text="Manager Rating", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.02, rely=0.38, relwidth=0.14, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text="League", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.16, rely=0.33, relwidth=0.16, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text="Domestic Cup", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.16, rely=0.43, relwidth=0.16, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text="Continental Cup", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.16, rely=0.53, relwidth=0.16, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Player Relations", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.32, rely=0.37, relwidth=0.18, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Player Relations", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.32, rely=0.355, relwidth=0.18, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Fan Relations", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.32, rely=0.465, relwidth=0.18, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Youth Intake", fg="white", font=("Comic Sans", 18, "bold")).place(relx=0.52, rely=0.29, relwidth=0.46, relheight=0.05)
       Label(menu_frames[3], bg="#26262e", text="Club Reputation", fg="white", font=("Comic Sans", 18)).place(relx=0.02, rely=0.66, relwidth=0.23, relheight=0.035)
       Label(menu_frames[3], bg="#26262e", text="Sponsor", fg="white", font=("Comic Sans", 18)).place(relx=0.27, rely=0.66, relwidth=0.23, relheight=0.035)
       Label(menu_frames[3], bg="#363440", text="Predicted Finish", fg="white", font=("Comic Sans", 16)).place(relx=0.02, rely=0.7, relwidth=0.115, relheight=0.035)
       Label(menu_frames[3], bg="#363440", text="Club Rating", fg="white", font=("Comic Sans", 16)).place(relx=0.135, rely=0.7, relwidth=0.115, relheight=0.035)
       Label(menu_frames[3], bg="#363440", text="Sponsor Name", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.27, rely=0.7, relwidth=0.115, relheight=0.035)
       Label(menu_frames[3], bg="#363440", text="Sponsor Revenue\n€M/year", fg="white", font=("Comic Sans", 14, "bold")).place(relx=0.385, rely=0.7, relwidth=0.115, relheight=0.05)
       Label(menu_frames[3], bg="#363440", text=fitness_coach.name, fg="white", font=("Comic Sans", 16)).place(relx=0.02, rely=0.11, relwidth=0.192, relheight=0.03)
       fitness_coach_wage_label = Label(menu_frames[3], bg="#363440", text=f"Wage: €{int(fitness_coach.wage*1000)}/w", fg="white", font=("Comic Sans", 13))
       fitness_coach_wage_label.place(relx=0.116, rely=0.14, relwidth=0.096, relheight=0.03)
       fitness_coach_rating_label = Label(menu_frames[3], bg="#363440", text=f"Rating: {fitness_coach.rating}/10", fg="white", font=("Comic Sans", 13))
       fitness_coach_rating_label.place(relx=0.02, rely=0.14, relwidth=0.096, relheight=0.03)
       Label(menu_frames[3], bg="#302E39", text=physiotherapist.name, fg="white", font=("Comic Sans", 16)).place(relx=0.212, rely=0.11, relwidth=0.192, relheight=0.03)
       physiotherapist_wage_label = Label(menu_frames[3], bg="#302E39", text=f"Wage: €{int(physiotherapist.wage * 1000)}/w", fg="white", font=("Comic Sans", 13))
       physiotherapist_wage_label.place(relx=0.308, rely=0.14, relwidth=0.096, relheight=0.03)
       physiotherapist_rating_label = Label(menu_frames[3], bg="#302E39", text=f"Rating: {physiotherapist.rating}/10", fg="white", font=("Comic Sans", 13))
       physiotherapist_rating_label.place(relx=0.212, rely=0.14, relwidth=0.096, relheight=0.03)
       Label(menu_frames[3], bg="#363440", text=chief_analyst.name, fg="white", font=("Comic Sans", 16)).place(relx=0.404, rely=0.11, relwidth=0.192, relheight=0.03)
       chief_analyst_wage_label = Label(menu_frames[3], bg="#363440", text=f"Wage: €{int(chief_analyst.wage * 1000)}/w", fg="white", font=("Comic Sans", 13))
       chief_analyst_wage_label.place(relx=0.5, rely=0.14, relwidth=0.096, relheight=0.03)
       chief_analyst_rating_label = Label(menu_frames[3], bg="#363440", text=f"Rating: {chief_analyst.rating}/10", fg="white", font=("Comic Sans", 13))
       chief_analyst_rating_label.place(relx=0.404, rely=0.14, relwidth=0.096, relheight=0.03)
       Label(menu_frames[3], bg="#302E39", text=gk_coach.name, fg="white", font=("Comic Sans", 16)).place(relx=0.596, rely=0.11, relwidth=0.192, relheight=0.03)
       gk_coach_wage_label = Label(menu_frames[3], bg="#302E39", text=f"Wage: €{int(gk_coach.wage * 1000)}/w", fg="white", font=("Comic Sans", 13))
       gk_coach_wage_label.place(relx=0.692, rely=0.14, relwidth=0.096, relheight=0.03)
       gk_coach_rating_label = Label(menu_frames[3], bg="#302E39", text=f"Rating: {gk_coach.rating}/10", fg="white", font=("Comic Sans", 13))
       gk_coach_rating_label.place(relx=0.596, rely=0.14, relwidth=0.096, relheight=0.03)
       Label(menu_frames[3], bg="#363440", text=youth_coach.name, fg="white", font=("Comic Sans", 16)).place(relx=0.788, rely=0.11, relwidth=0.192, relheight=0.03)
       youth_coach_wage_label = Label(menu_frames[3], bg="#363440", text=f"Wage: €{int(youth_coach.wage * 1000)}/w", fg="white", font=("Comic Sans", 13))
       youth_coach_wage_label.place(relx=0.884, rely=0.14, relwidth=0.096, relheight=0.03)
       youth_coach_rating_label = Label(menu_frames[3], bg="#363440", text=f"Rating: {youth_coach.rating}/10", fg="white", font=("Comic Sans", 13))
       youth_coach_rating_label.place(relx=0.788, rely=0.14, relwidth=0.096, relheight=0.03)

       # MANAGER OBJECTIVES
       manager_rating = Label(menu_frames[3], bg="#363440", text="50/100", fg="white", font=("Comic Sans", 18))
       manager_rating.place(relx=0.02, rely=0.43, relwidth=0.14, relheight=0.05)
       manager_security = Label(menu_frames[3], bg="#363440", text="Okay", fg="yellow", font=("Comic Sans", 18))
       manager_security.place(relx=0.02, rely=0.48, relwidth=0.14, relheight=0.05)
       league_objective = Label(menu_frames[3], bg="#363440", text="Fight for Playoffs", fg="white", font=("Comic Sans", 15))
       league_objective.place(relx=0.16, rely=0.38, relwidth=0.16, relheight=0.05)
       domestic_objective = Label(menu_frames[3], bg="#363440", text="Reach Round of 16", fg="white", font=("Comic Sans", 15))
       domestic_objective.place(relx=0.16, rely=0.48, relwidth=0.16, relheight=0.05)
       continental_objective = Label(menu_frames[3], bg="#363440", text="N/A", fg="white", font=("Comic Sans", 15))
       continental_objective.place(relx=0.16, rely=0.58, relwidth=0.16, relheight=0.05)
       player_relations = Label(menu_frames[3], bg="#26262e", text="Good", fg="green", font=("Comic Sans", 18))
       player_relations.place(relx=0.32, rely=0.405, relwidth=0.18, relheight=0.05)
       fan_relations = Label(menu_frames[3], bg="#26262e", text="Good", fg="green", font=("Comic Sans", 18))
       fan_relations.place(relx=0.32, rely=0.515, relwidth=0.18, relheight=0.05)
       predicted_finish = Label(menu_frames[3], bg="#363440", text=f"{random.randint(1, 24)}", fg="white", font=("Comic Sans", 18))
       predicted_finish.place(relx=0.02, rely=0.735, relwidth=0.115, relheight=0.04)
       club_rating = Label(menu_frames[3], bg="#363440", text=f"{random.randint(2, 3)}/20", fg="white", font=("Comic Sans", 18))
       club_rating.place(relx=0.135, rely=0.735, relwidth=0.115, relheight=0.04)
       get_team_avg_rating()
       sponsor_name = Label(menu_frames[3], bg="#363440", text=f"{random.choice(sponsor_names)}", fg="white", font=("Comic Sans", 14))
       sponsor_name.place(relx=0.27, rely=0.735, relwidth=0.115, relheight=0.04)
       sponsor_revenue = Label(menu_frames[3], bg="#363440", fg="white", font=("Comic Sans", 14))
       sponsor_revenue.place(relx=0.385, rely=0.75, relwidth=0.115, relheight=0.04)

       def upgrade_staff(staff_object):
           global stransfer_loss_label
           remove_button = False
           staff_object.wage = staff_object.next_wage
           add_loss(staff_object.next_upgrade_cost, stransfer_loss_label, True)
           staff_object.rating += 1
           get_wage_costs()
           update_budget_labels()
           if staff_object.rating >= 10:
               remove_button = True
           staff_object.get_next_wage()

           # updates labels with staffs new wages and ratings and removes the upgrade button if their rating has been maxed out
           if staff_object == fitness_coach:
               fitness_coach_wage_label.config(text=f"Wage: €{int(fitness_coach.wage*1000)}/w")
               fitness_coach_rating_label.config(text=f"Rating: {fitness_coach.rating}/10")
               if remove_button:
                   staff_buttons[0].place_forget()
           elif staff_object == physiotherapist:
               physiotherapist_wage_label.config(text=f"Wage: €{int(physiotherapist.wage*1000)}/w")
               physiotherapist_rating_label.config(text=f"Rating: {physiotherapist.rating}/10")
               if remove_button:
                   staff_buttons[1].place_forget()
           elif staff_object == chief_analyst:
               chief_analyst_wage_label.config(text=f"Wage: €{int(chief_analyst.wage*1000)}/w")
               chief_analyst_rating_label.config(text=f"Rating: {chief_analyst.rating}/10")
               if remove_button:
                   staff_buttons[2].place_forget()
           elif staff_object == gk_coach:
               gk_coach_wage_label.config(text=f"Wage: €{int(gk_coach.wage*1000)}/w")
               gk_coach_rating_label.config(text=f"Rating: {gk_coach.rating}/10")
               if remove_button:
                   staff_buttons[3].place_forget()
           elif staff_object == youth_coach:
               youth_coach_wage_label.config(text=f"Wage: €{int(youth_coach.wage * 1000)}/w")
               youth_coach_rating_label.config(text=f"Rating: {youth_coach.rating}/10")
               if remove_button:
                   staff_buttons[4].place_forget()

           change_menu(3)
           show_menu_buttons()

       def cancel_upgrade_staff():
           change_menu(3)
           show_menu_buttons()

       def show_staff_upgrade_message(staff_object):
           change_menu(9)
           hide_menu_buttons_grey()
           upgrade_staff_button.config(command=lambda: upgrade_staff(staff_object))
           cancel_upgrade_staff_button.config(command=cancel_upgrade_staff)
           confirm_staff_upgrade_label.config(text=f"Are you sure you want to upgrade {staff_object.name}?")
           staff_current_rating_label.config(text=staff_object.rating)
           staff_current_wage_label.config(text="€{:,} /week".format(int(staff_object.wage*1000)))
           staff_new_rating_label.config(text=staff_object.rating+1)
           staff_new_wage_label.config(text="€{:,} /week".format(int(staff_object.next_wage*1000)))
           staff_upgrade_cost_label.config(text="€{:,}".format(staff_object.next_upgrade_cost))

       staff_buttons = []
       staff_buttons.append(Button(menu_frames[3], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(fitness_coach)))
       staff_buttons[0].place(relx=0.06, rely=0.18, relwidth=0.112, relheight=0.04)
       staff_buttons.append(Button(menu_frames[3], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(physiotherapist)))
       staff_buttons[1].place(relx=0.252, rely=0.18, relwidth=0.112, relheight=0.04)
       staff_buttons.append(Button(menu_frames[3], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(chief_analyst)))
       staff_buttons[2].place(relx=0.444, rely=0.18, relwidth=0.112, relheight=0.04)
       staff_buttons.append(Button(menu_frames[3], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(gk_coach)))
       staff_buttons[3].place(relx=0.636, rely=0.18, relwidth=0.112, relheight=0.04)
       staff_buttons.append(Button(menu_frames[3], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(youth_coach)))
       staff_buttons[4].place(relx=0.828, rely=0.18, relwidth=0.112, relheight=0.04)
   place_club()

   def remove_scouted_player(player_object):
       if player_object in scout_one_players:
           scout_one_players.remove(player_object)
           update_scout_one_frames()
       elif player_object in scout_two_players:
           scout_two_players.remove(player_object)
           update_scout_two_frames()
       elif player_object in scout_three_players:
           scout_three_players.remove(player_object)
           update_scout_three_frames()

   def display_scouted_player_info(player_object, frame):
       Label(frame, text=f"{player_object.first_name}\n{player_object.last_name}", font=("Comic Sans", 11), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0, rely=0, relwidth=0.3,
                                                                                                                                                                relheight=1)
       Label(frame, text="Ovr", font=("Comic sans", 12, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.3, rely=0, relwidth=0.1, relheight=0.5)
       Label(frame, text=player_object.ovr, font=("Comic sans", 12), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.5)
       Label(frame, text="Pos", font=("Comic sans", 12, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.4, rely=0, relwidth=0.1, relheight=0.5)
       Label(frame, text=player_object.pos, font=("Comic sans", 12), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.5)
       Label(frame, text="Age", font=("Comic sans", 12, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.5, rely=0, relwidth=0.1, relheight=0.5)
       Label(frame, text=player_object.age, font=("Comic sans", 12), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.5)
       Label(frame, text="Value", font=("Comic sans", 12, "bold"), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.6, rely=0, relwidth=0.15, relheight=0.5)
       Label(frame, text=f"€{player_object.getValue()}M", font=("Comic sans", 12), fg="white", bg=LIGHT_UI_COLOUR).place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.5)
       if len(squad) < MAX_SQUAD_SIZE:
           Button(frame, text="Make Offer", font=("Comic sans", 12), fg="white", bg="lime", bd=0, command=lambda:negotiate_player_contract(player_object) ).place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5)
       else:
           Label(frame, text="Squad Full", font=("Comic sans", 12), fg="white", bg=DARK_UI_COLOUR, bd=0).place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5)
       Button(frame, text="Remove", font=("Comic sans", 12), fg="white", bg="red", bd=0, command=lambda: remove_scouted_player(player_object)).place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5)

   def update_scout_one_frames():
       for frame in scout_one_frames:
           for child in frame.winfo_children():
               child.destroy()

       for i, player_object in enumerate(scout_one_players):
           display_scouted_player_info(player_object, scout_one_frames[i])

   def update_scout_two_frames():
       for frame in scout_two_frames:
           for child in frame.winfo_children():
               child.destroy()

       for i, player_object in enumerate(scout_two_players):
           display_scouted_player_info(player_object, scout_two_frames[i])

   def update_scout_three_frames():
       for frame in scout_three_frames:
           for child in frame.winfo_children():
               child.destroy()

       for i, player_object in enumerate(scout_three_players):
           display_scouted_player_info(player_object, scout_three_frames[i])

   def transfer_offer_for_player(player_object, offer_value):
       global transfer_offer_frame
       for child in transfer_offer_frame.winfo_children():
           child.destroy()

       Label(transfer_offer_frame, text=f"{player_object.first_name} {player_object.last_name}", fg="white", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16)).place(relx=0, rely=0, relwidth=0.6, relheight=0.3)
       Label(transfer_offer_frame, text="Ovr", fg="white", bg=LIGHT_UI_COLOUR, font=("Comic sans", 15, "bold")).place(relx=0.62, rely=0, relwidth=0.12, relheight=0.3)
       Label(transfer_offer_frame, text=f"{player_object.ovr}", fg="white", bg=LIGHT_UI_COLOUR, font=("Comic sans", 18)).place(relx=0.74, rely=0, relwidth=0.26, relheight=0.3)
       Label(transfer_offer_frame, text="Offer", fg="white", bg=LIGHT_UI_COLOUR, font=("Comic sans", 15, "bold")).place(relx=0.15, rely=0.35, relwidth=0.2, relheight=0.3)
       Label(transfer_offer_frame, text="€{:,}".format(offer_value), fg="white", bg=LIGHT_UI_COLOUR, font=("Comic sans", 15)).place(relx=0.35, rely=0.35, relwidth=0.55, relheight=0.3)
       Button(transfer_offer_frame, text="Negotiate", bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), command=lambda: negotiate_player_sale(player_object, offer_value)).place(relx=0.05, rely=0.68, relwidth=0.425, relheight=0.22)
       Button(transfer_offer_frame, text="Decline", bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), command=decline_transfer_offer).place(relx=0.525, rely=0.68, relwidth=0.425, relheight=0.22)

   def place_transfers():
       global scout_one_frames, scout_two_frames, scout_three_frames, transfer_offer_frame
       def confirm_scout_one_instructions():
           global scout_one_instructions
           scout_one_instructions[0] = search_type_one.get()
           scout_one_instructions[1] = quality_level_one.get()
           scout_one_instructions[2] = pos_focus_one.get()

       def confirm_scout_two_instructions():
           global scout_two_instructions
           scout_two_instructions[0] = search_type_two.get()
           scout_two_instructions[1] = quality_level_two.get()
           scout_two_instructions[2] = pos_focus_two.get()

       def confirm_scout_three_instructions():
           global scout_one_instructions
           scout_three_instructions[0] = search_type_three.get()
           scout_three_instructions[1] = quality_level_three.get()
           scout_three_instructions[2] = pos_focus_three.get()

       # BACKGROUNDS
       Label(menu_frames[5], bg="#363440").place(relx=0.02, rely=0.02, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.265, rely=0.02, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.51, rely=0.02, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.755, rely=0.02, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.02, rely=0.24, relwidth=0.225, relheight=0.22)
       Label(menu_frames[5], bg="#363440").place(relx=0.02, rely=0.485, relwidth=0.225, relheight=0.33)
       Label(menu_frames[5], bg="#363440").place(relx=0.265, rely=0.22, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.51, rely=0.22, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.755, rely=0.22, relwidth=0.225, relheight=0.2)
       Label(menu_frames[5], bg="#363440").place(relx=0.265, rely=0.44, relwidth=0.225, relheight=0.375)
       Label(menu_frames[5], bg="#363440").place(relx=0.51, rely=0.44, relwidth=0.225, relheight=0.375)
       Label(menu_frames[5], bg="#363440").place(relx=0.755, rely=0.44, relwidth=0.225, relheight=0.375)

       transfer_offer_frame = Frame(menu_frames[5], bg=LIGHT_UI_COLOUR)
       transfer_offer_frame.place(relx=0.02, rely=0.29, relwidth=0.225, relheight=0.17)

       # headings
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Chief Scout").place(relx=0.02, rely=0.02, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout One").place(relx=0.265, rely=0.02, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout Two").place(relx=0.51, rely=0.02, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout Three").place(relx=0.755, rely=0.02, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20), text="Transfer Offers").place(relx=0.02, rely=0.24, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20), text="Negotiations").place(relx=0.02, rely=0.485, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players").place(relx=0.265, rely=0.44, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players").place(relx=0.51, rely=0.44, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players").place(relx=0.755, rely=0.44, relwidth=0.225, relheight=0.05)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus").place(relx=0.265, rely=0.22, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus").place(relx=0.51, rely=0.22, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus").place(relx=0.755, rely=0.22, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level").place(relx=0.265, rely=0.265, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level").place(relx=0.51, rely=0.265, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level").place(relx=0.755, rely=0.265, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus").place(relx=0.265, rely=0.32, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus").place(relx=0.51, rely=0.32, relwidth=0.075, relheight=0.04)
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus").place(relx=0.755, rely=0.32, relwidth=0.075, relheight=0.04)
       # scout attributes
       scout_buttons = []
       # chief scout
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=chief_scout.name).place(relx=0.02, rely=0.07, relwidth=0.225, relheight=0.05)
       chief_scout_rating_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Rating: {chief_scout.rating}/10")
       chief_scout_rating_label.place(relx=0.02, rely=0.12, relwidth=0.1125, relheight=0.035)
       chief_scout_wage_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Wage: €{int(chief_scout.wage*1000)} /w")
       chief_scout_wage_label.place(relx=0.1325, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_buttons.append(Button(menu_frames[5], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(chief_scout)))
       scout_buttons[0].place(relx=0.06, rely=0.16, relwidth=0.145, relheight=0.04)
       # scout one
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=scout_one.name).place(relx=0.265, rely=0.07, relwidth=0.225, relheight=0.05)
       scout_one_rating_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Rating: {scout_one.rating}/10")
       scout_one_rating_label.place(relx=0.265, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_one_wage_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Wage: €{int(scout_one.wage * 1000)} /w")
       scout_one_wage_label.place(relx=0.3775, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_buttons.append(Button(menu_frames[5], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(scout_one)))
       scout_buttons[1].place(relx=0.305, rely=0.16, relwidth=0.145, relheight=0.04)
       # scout two
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=scout_two.name).place(relx=0.51, rely=0.07, relwidth=0.225, relheight=0.05)
       scout_two_rating_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Rating: {scout_two.rating}/10")
       scout_two_rating_label.place(relx=0.51, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_two_wage_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Wage: €{int(scout_two.wage * 1000)} /w")
       scout_two_wage_label.place(relx=0.6225, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_buttons.append(Button(menu_frames[5], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(scout_two)))
       scout_buttons[2].place(relx=0.55, rely=0.16, relwidth=0.145, relheight=0.04)
       # scout three
       Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=scout_three.name).place(relx=0.755, rely=0.07,  relwidth=0.225, relheight=0.05)
       scout_three_rating_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Rating: {scout_three.rating}/10")
       scout_three_rating_label.place(relx=0.755, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_three_wage_label = Label(menu_frames[5], bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Wage: €{int(scout_three.wage * 1000)} /w")
       scout_three_wage_label.place(relx=0.8675, rely=0.12, relwidth=0.1125, relheight=0.035)
       scout_buttons.append(Button(menu_frames[5], fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade", command=lambda: show_staff_upgrade_message(scout_three)))
       scout_buttons[3].place(relx=0.795, rely=0.16, relwidth=0.145, relheight=0.04)

       def upgrade_staff(staff_object):
           global stransfer_loss_label
           remove_button = False
           staff_object.wage = staff_object.next_wage
           add_loss(staff_object.next_upgrade_cost, stransfer_loss_label, True)
           staff_object.rating += 1
           get_wage_costs()
           update_budget_labels()
           if staff_object.rating >= 10:
               remove_button = True
           staff_object.get_next_wage()

           # updates labels with staffs new wages and ratings and removes the upgrade button if their rating has been maxed out
           if staff_object == chief_scout:
               chief_scout_wage_label.config(text=f"Wage: €{int(chief_scout.wage*1000)}/w")
               chief_scout_rating_label.config(text=f"Rating: {chief_scout.rating}/10")
               if remove_button:
                   scout_buttons[0].place_forget()
           elif staff_object == scout_one:
               scout_one_wage_label.config(text=f"Wage: €{int(scout_one.wage*1000)}/w")
               scout_one_rating_label.config(text=f"Rating: {scout_one.rating}/10")
               if remove_button:
                   scout_buttons[1].place_forget()
           elif staff_object == scout_two:
               scout_two_wage_label.config(text=f"Wage: €{int(scout_two.wage*1000)}/w")
               scout_two_rating_label.config(text=f"Rating: {scout_two.rating}/10")
               if remove_button:
                   scout_buttons[2].place_forget()
           elif staff_object == scout_three:
               scout_three_wage_label.config(text=f"Wage: €{int(scout_three.wage*1000)}/w")
               scout_three_rating_label.config(text=f"Rating: {scout_three.rating}/10")
               if remove_button:
                   scout_buttons[3].place_forget()

           change_menu(5)
           show_menu_buttons()

       def cancel_upgrade_staff():
           change_menu(5)
           show_menu_buttons()

       def show_staff_upgrade_message(staff_object):
           change_menu(9)
           hide_menu_buttons_grey()
           upgrade_staff_button.config(command=lambda: upgrade_staff(staff_object))
           cancel_upgrade_staff_button.config(command=cancel_upgrade_staff)
           confirm_staff_upgrade_label.config(text=f"Are you sure you want to upgrade {staff_object.name}?")
           staff_current_rating_label.config(text=staff_object.rating)
           staff_current_wage_label.config(text="€{:,} /week".format(int(staff_object.wage*1000)))
           staff_new_rating_label.config(text=staff_object.rating+1)
           staff_new_wage_label.config(text="€{:,} /week".format(int(staff_object.next_wage*1000)))
           staff_upgrade_cost_label.config(text="€{:,}".format(staff_object.next_upgrade_cost))

       # scout one instructions
       search_type_one = StringVar()
       search_type_one.set("Any")
       search_type_pick_one = OptionMenu(menu_frames[5], search_type_one, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
       search_type_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       search_type_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       search_type_pick_one.place(relx=0.34, rely=0.21, relwidth=0.145, relheight=0.04)
       quality_level_one = StringVar()
       quality_level_one.set("Any")
       quality_level_pick_one = OptionMenu(menu_frames[5], quality_level_one, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
       quality_level_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       quality_level_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       quality_level_pick_one.place(relx=0.34, rely=0.265, relwidth=0.145, relheight=0.04)
       pos_focus_one = StringVar()
       pos_focus_one.set("Any")
       pos_focus_pick_one = OptionMenu(menu_frames[5], pos_focus_one, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
       pos_focus_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       pos_focus_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       pos_focus_pick_one.place(relx=0.34, rely=0.32, relwidth=0.145, relheight=0.04)
       # scout two instructions
       search_type_two = StringVar()
       search_type_two.set("Any")
       search_type_pick_two = OptionMenu(menu_frames[5], search_type_two, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
       search_type_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       search_type_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       search_type_pick_two.place(relx=0.585, rely=0.21, relwidth=0.145, relheight=0.04)
       quality_level_two = StringVar()
       quality_level_two.set("Any")
       quality_level_pick_two = OptionMenu(menu_frames[5], quality_level_two, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
       quality_level_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       quality_level_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       quality_level_pick_two.place(relx=0.585, rely=0.265, relwidth=0.145, relheight=0.04)
       pos_focus_two = StringVar()
       pos_focus_two.set("Any")
       pos_focus_pick_two = OptionMenu(menu_frames[5], pos_focus_two, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
       pos_focus_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       pos_focus_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       pos_focus_pick_two.place(relx=0.585, rely=0.32, relwidth=0.145, relheight=0.04)
       # scout three instructions
       search_type_three = StringVar()
       search_type_three.set("Any")
       search_type_pick_three = OptionMenu(menu_frames[5], search_type_three, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
       search_type_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       search_type_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       search_type_pick_three.place(relx=0.83, rely=0.21, relwidth=0.145, relheight=0.04)
       quality_level_three = StringVar()
       quality_level_three.set("Any")
       quality_level_pick_three = OptionMenu(menu_frames[5], quality_level_three, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
       quality_level_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       quality_level_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       quality_level_pick_three.place(relx=0.83, rely=0.265, relwidth=0.145, relheight=0.04)
       pos_focus_three = StringVar()
       pos_focus_three.set("Any")
       pos_focus_pick_three = OptionMenu(menu_frames[5], pos_focus_three, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
       pos_focus_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
       pos_focus_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
       pos_focus_pick_three.place(relx=0.83, rely=0.32, relwidth=0.145, relheight=0.04)

       # buttons to confirm scouts search criteria
       confirm_scout_one_button = Button(menu_frames[5], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm", command=confirm_scout_one_instructions)
       confirm_scout_one_button.place(relx=0.305, rely=0.375, relwidth=0.145, relheight=0.04)
       confirm_scout_two_button = Button(menu_frames[5], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm", command=confirm_scout_two_instructions)
       confirm_scout_two_button.place(relx=0.55, rely=0.375, relwidth=0.145, relheight=0.04)
       confirm_scout_one_button = Button(menu_frames[5], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm", command=confirm_scout_three_instructions)
       confirm_scout_one_button.place(relx=0.795, rely=0.375, relwidth=0.145, relheight=0.04)

       # FRAMES FOR SCOUTS SCOUTED PLAYERS
       for i in range(4):
           scout_one_frames.append(Frame(menu_frames[5], bg=LIGHT_UI_COLOUR))
           scout_one_frames[-1].place(relx=0.265, rely= (i*0.08125) + 0.49, relwidth=0.225, relheight=0.08125)

       for i in range(4):
           scout_two_frames.append(Frame(menu_frames[5], bg=LIGHT_UI_COLOUR))
           scout_two_frames[-1].place(relx=0.51, rely= (i*0.08125) + 0.49, relwidth=0.225, relheight=0.08125)

       for i in range(4):
           scout_three_frames.append(Frame(menu_frames[5], bg=LIGHT_UI_COLOUR))
           scout_three_frames[-1].place(relx=0.755, rely= (i*0.08125) + 0.49, relwidth=0.225, relheight=0.08125)

   place_transfers()

   def update_budget_labels():
       global wage_total, transfer_budget
       wage_budget_label.config(text="€ {:,}".format(int(wage_budget)))
       wage_paid_label.config(text="€ {:,}".format(int(wage_total)))
       transfer_budget_label.config(text="€ {:,}".format(transfer_budget))


   def get_wage_costs():
       global wage_budget, wage_total, prev_wage_total
       # gets squads total wage value
       wage_total = 0
       for i in squad:
           wage_total += i.wage

       wage_total += chief_scout.wage + scout_one.wage + scout_two.wage + scout_three.wage + physiotherapist.wage + youth_coach.wage + gk_coach.wage + fitness_coach.wage + chief_analyst.wage

       # takes away prev wage total from current wage total so the difference gets taken away
       wage_total = round(wage_total*1000, 2)
       wage_difference = (wage_total - prev_wage_total)
       prev_wage_total = round(wage_total, 2)

       # takes wage total away from the wage budget, if its less than 0 then makes it equal 0
       wage_budget -= wage_difference
       if wage_budget < 0:
           wage_budget = 0

   def add_profit(profit, profit_type, is_added_to_budget):
       global transfer_split, wage_split, profit_label, total_income_label, ticket_income_label, bonus_income_label, merch_income_label, rights_income_label, sales_income_label, sponsor_income_label, transfer_budget_label, wage_budget_label, wage_budget, transfer_budget
       # gets current total profit from the profit label
       total_profit = int(extract_digits_with_negative(profit_label.cget("text")))
       total_profit_of_type = int(extract_digits_with_negative(profit_type.cget("text")))
       total_income = int(extract_digits_with_negative(total_income_label.cget("text")))
       # adds on new profit to total profit and updates the profit label
       total_profit += profit
       total_profit_of_type += profit
       total_income += profit
       profit_label.config(text="€ {:,}".format(total_profit))
       profit_type.config(text="€{:,}".format(total_profit_of_type))
       total_income_label.config(text="€{:,}".format(total_income))

       if is_added_to_budget:
           # gets the amount of cash available to the player after the board has taken their cut of the profit
           manager_profit = profit - (profit * BOARD_PROFIT_CUT)
           # splits profit into transfer and wage budgets
           transfer_profit = special_round(manager_profit * transfer_split, 1)
           wage_profit = (special_round((manager_profit * wage_split)/52, 1))
           # adds on profit to current budgets and updates transfer budget and wage budget_labels
           transfer_budget = int(extract_digits_with_negative(transfer_budget_label.cget("text")))
           wage_budget = int(extract_digits_with_negative(wage_budget_label.cget("text")))
           transfer_budget += transfer_profit
           wage_budget += wage_profit
           transfer_budget_label.config(text="€ {:,}".format(transfer_budget))
           wage_budget_label.config(text="€ {:,}".format(wage_budget))
           get_wage_costs()


   def add_loss(loss, loss_type, is_taken_from_budget):
       global transfer_split, wage_split, profit_label, transfer_budget_label, wage_budget_label, wage_budget, transfer_budget, total_loss_label, wage_loss_label, stwage_loss_label, transfer_loss_label, stransfer_loss_label, cost_loss_label, upgrade_loss_label
       # gets current total profit from the profit label
       total_profit = int(extract_digits_with_negative(profit_label.cget("text")))
       total_loss_of_type = int(extract_digits_with_negative(loss_type.cget("text")))
       total_loss = int(extract_digits_with_negative(total_loss_label.cget("text")))
       # adds on new profit to total profit and updates the profit label
       total_profit -= loss
       total_loss_of_type += loss
       total_loss += loss
       profit_label.config(text="€ {:,}".format(total_profit))
       loss_type.config(text="€{:,}".format(total_loss_of_type))
       total_loss_label.config(text="€{:,}".format(total_loss))

       # adds on profit to current budgets and updates transfer budget and wage budget_labels
       transfer_budget = int(extract_digits_with_negative(transfer_budget_label.cget("text")))
       if is_taken_from_budget:
           transfer_budget -= loss
       transfer_budget_label.config(text="€ {:,}".format(transfer_budget))


   def place_finances():
       global wage_budget, transfer_budget, wage_budget_label, wage_total, profit_label, total_income_label, ticket_income_label, bonus_income_label, merch_income_label, rights_income_label, sales_income_label, sponsor_income_label, transfer_budget_label, wage_budget_label, wage_paid_label, total_loss_label, wage_loss_label, stwage_loss_label, transfer_loss_label, stransfer_loss_label, cost_loss_label, upgrade_loss_label
       # gets income split from income split option menu
       def get_income_split():
           global transfer_split
           global wage_split
           income_split_value = income_split.get()
           transfer_split = int(income_split_value[:2])/100
           wage_split = int(income_split_value[3:])/100

       def get_league_ticket_price():
           global league_ticket_price, FAN_RELATION
           club_rating_value = int(club_rating.cget("text").split("/")[0])
           league_ticket_price = int(extract_digits(league_ticket_price_picked.get()))
           cup_ticket_price = int(extract_digits(league_ticket_price_picked.get()))
           # gets maximum amount fans expect to pay for tickets in order to calculate fan happiness
           if club_rating_value in [1, 2]:
               max_expected_price = 20
           elif club_rating_value in [3, 4, 5]:
               max_expected_price = 30
           elif club_rating_value in [6, 7, 8, 9, 10]:
               max_expected_price = 40
           elif club_rating_value in [11, 12, 13, 14, 15, 16]:
               max_expected_price = 50
           else:
               max_expected_price = 100

           price_difference = max_expected_price - league_ticket_price

           if price_difference >= 40:
               FAN_RELATION = 100
           elif price_difference >= 30:
               FAN_RELATION = 90
           elif price_difference >= 20:
               FAN_RELATION = 80
           elif price_difference >= 10:
               FAN_RELATION = 70
           elif price_difference >= 0:
               FAN_RELATION = 67
           elif price_difference >= -10:
               FAN_RELATION = 50
           elif price_difference >= -20:
               FAN_RELATION = 35
           elif price_difference >= -30:
               FAN_RELATION = 15
           elif price_difference >= -40:
               FAN_RELATION = 5
           else:
               FAN_RELATION = 0

           if FAN_RELATION > 66:
               fan_relations.config(text="Good", fg="green")
               fan_happiness_label.config(text="Good", fg="green")
           elif FAN_RELATION > 33:
               fan_relations.config(text="Okay", fg="yellow1")
               fan_happiness_label.config(text="Okay", fg="yellow1")
           else:
               fan_relations.config(text="Bad", fg="red")
               fan_happiness_label.config(text="Bad", fg="red")

       # gets transfer and wage budgets based on region
       if CLUB_COUNTRY == "England":
           transfer_budget = random.randint(525000, 950000)
           wage_budget = (random.randint(32, 45)) * 1000
       elif CLUB_COUNTRY == "France":
           transfer_budget = random.randint(1700000, 2600000)
           wage_budget = (random.randint(140, 180)) * 1000
       elif CLUB_COUNTRY == "Germany":
           transfer_budget = random.randint(3500000, 6000000)
           wage_budget = (random.randint(125, 160)) * 1000
       elif CLUB_COUNTRY == "Italy":
           transfer_budget = random.randint(3100000, 5900000)
           wage_budget = (random.randint(145, 180)) * 1000
       elif CLUB_COUNTRY == "Spain":
           transfer_budget = random.randint(3000000, 5800000)
           wage_budget = (random.randint(145, 175)) * 1000

       get_wage_costs()

       if wage_budget == 0:
           wage_budget += random.randint(500, 3000)

       # BACKGROUNDS
       Label(menu_frames[4], bg="#363440").place(relx=0.72, rely=0.05, relwidth=0.26, relheight=0.48)
       Label(menu_frames[4], bg="#363440").place(relx=0.72, rely=0.6, relwidth=0.26, relheight=0.2)
       Label(menu_frames[4], bg="#26262e").place(relx=0.33, rely=0.05, relwidth=0.33, relheight=0.36)
       Label(menu_frames[4], bg="#26262e").place(relx=0.33, rely=0.44, relwidth=0.33, relheight=0.36)
       Label(menu_frames[4], bg="#363440").place(relx=0.02, rely=0.05, relwidth=0.26, relheight=0.36)
       Label(menu_frames[4], bg="#363440").place(relx=0.02, rely=0.44, relwidth=0.26, relheight=0.36)

       # SUBHEADINGS
       Label(menu_frames[4], text="Remaining Transfer Budget", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.75, rely=0.06, relwidth=0.2, relheight=0.04)

       Label(menu_frames[4], text="Remaining Wage Budget", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.75, rely=0.21, relwidth=0.2, relheight=0.04)

       Label(menu_frames[4], text="Current Wage Expenditure", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.75, rely=0.36, relwidth=0.2, relheight=0.04)

       Label(menu_frames[4], text="Current Wage Expenditure", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.75, rely=0.36, relwidth=0.2, relheight=0.04)

       Label(menu_frames[4], text="Income Split\nTransfer/Wage", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.75, rely=0.6, relwidth=0.2, relheight=0.08)

       Label(menu_frames[4], text="Income", bg="#26262e", fg="white",
             font=("Comic Sans", 20)).place(relx=0.38, rely=0.05, relwidth=0.15, relheight=0.09)
       Label(menu_frames[4], text="Total:", bg="#26262e", fg="white",
             font=("Comic Sans", 15)).place(relx=0.53, rely=0.05, relwidth=0.05, relheight=0.09)
       Label(menu_frames[4], text="Home and Away Tickets:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.14, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Merchandise Sales:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.185, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Player Sales:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.23, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Broadcasting rights:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.275, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Competition Bonuses:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.32, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Sponsorships:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.365, relwidth=0.25, relheight=0.045)

       Label(menu_frames[4], text="Losses", bg="#26262e", fg="white",
             font=("Comic Sans", 20)).place(relx=0.38, rely=0.44, relwidth=0.15, relheight=0.09)
       Label(menu_frames[4], text="Total:", bg="#26262e", fg="white",
             font=("Comic Sans", 15)).place(relx=0.53, rely=0.44, relwidth=0.05, relheight=0.09)
       Label(menu_frames[4], text="Player Wages:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.53, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Staff Wages:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.575, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Player Signings:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.62, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Staff Signings:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.665, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Facility Costs:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.71, relwidth=0.25, relheight=0.045)
       Label(menu_frames[4], text="Facility Upgrades:", bg="#363440", fg="white",
             font=("Comic Sans", 15)).place(relx=0.33, rely=0.755, relwidth=0.25, relheight=0.045)

       Label(menu_frames[4], text="Total Profit", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.02, rely=0.06, relwidth=0.26, relheight=0.04)
       Label(menu_frames[4], text="Board's Profit Expectation", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.02, rely=0.21, relwidth=0.26, relheight=0.04)

       Label(menu_frames[4], text="Ticket Price", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.02, rely=0.46, relwidth=0.26, relheight=0.07)
       Label(menu_frames[4], text="Fan Relations", bg="#363440", fg="white",
             font=("Comic Sans", 17)).place(relx=0.02, rely=0.63, relwidth=0.26, relheight=0.05)

       fan_happiness_label = Label(menu_frames[4], text="Good", fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 20))
       fan_happiness_label.place(relx=0.02, rely=0.68, relwidth=0.26, relheight=0.07)

       # label that shows transfer budget
       transfer_budget_label = Label(menu_frames[4], text="€ {:,}".format(transfer_budget), bg="#26262e", fg="white", font=("Comic Sans", 25))
       transfer_budget_label.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)
       # label that shows wage budget
       wage_budget_label = Label(menu_frames[4], text="€ {:,}".format(int(wage_budget)), bg="#26262e", fg="white", font=("Comic Sans", 25))
       wage_budget_label.place(relx=0.75, rely=0.25, relwidth=0.2, relheight=0.1)
       # label that shows wage being paid
       wage_paid_label = Label(menu_frames[4], text="€ {:,}".format(int(wage_total)), bg="#26262e", fg="white", font=("Comic Sans", 25))
       wage_paid_label.place(relx=0.75, rely=0.4, relwidth=0.2, relheight=0.1)
       # option menu for income split between transfer and wage budget
       income_split = StringVar()
       income_split.set("50/50")
       income_split_pick = OptionMenu(menu_frames[4], income_split, *["90/10", "80/20", "70/30", "60/40", "50/50", "40/60", "30/70",
                                                                     "20/80", "10/90"])
       income_split_pick.config(bg="#26262e", fg="white", font=("Comic Sans", 19))
       income_split_pick["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 15))
       income_split_pick.place(relx=0.775, rely=0.7, relwidth=0.15, relheight=0.07)

       income_split_button = Button(menu_frames[4], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), text="Confirm", command=get_income_split)
       income_split_button.place(relx=0.925, rely=0.7, relwidth=0.05, relheight=0.07)
       # label that shows total income
       total_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 14))
       total_income_label.place(relx=0.58, rely=0.05, relwidth=0.08, relheight=0.09)
       # label that shows tickets income
       ticket_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       ticket_income_label.place(relx=0.58, rely=0.14, relwidth=0.08, relheight=0.045)
       # label that shows merch income
       merch_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       merch_income_label.place(relx=0.58, rely=0.185, relwidth=0.08, relheight=0.045)
       # label that shows player sales income
       sales_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       sales_income_label.place(relx=0.58, rely=0.23, relwidth=0.08, relheight=0.045)
       # label that shows broadcasting rights income
       rights_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       rights_income_label.place(relx=0.58, rely=0.275, relwidth=0.08, relheight=0.045)
       # label that shows competition bonuses income
       bonus_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       bonus_income_label.place(relx=0.58, rely=0.32, relwidth=0.08, relheight=0.045)
       # label that shows sponsors income
       sponsor_income_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12))
       sponsor_income_label.place(relx=0.58, rely=0.365, relwidth=0.08, relheight=0.045)
       # label that shows total profit
       profit_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="white", font=("Comic Sans", 25))
       profit_label.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.1)
       # label that shows profit expectation
       expected_profit_label = Label(menu_frames[4], text="€ {:,}".format(special_round(random.randint(700000, 1200000), 100000)), bg="#26262e", fg="white", font=("Comic Sans", 25))
       expected_profit_label.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.1)
       league_ticket_price_picked = StringVar()
       league_ticket_price_picked.set("€20")
       league_ticket_price_pick = OptionMenu(menu_frames[4], league_ticket_price_picked, *["€10", "€20", "€30", "€40", "€50", "€60", "€70", "€80",
                                                                                    "€90", "€100", "€110", "€120", "€130", "€140", "€150"])
       league_ticket_price_pick.config(bg="#26262e", fg="white", font=("Comic Sans", 19))
       league_ticket_price_pick["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 16))
       league_ticket_price_pick.place(relx=0.075, rely=0.53, relwidth=0.15, relheight=0.07)

       league_price_button = Button(menu_frames[4], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 16), text="Confirm", command=get_league_ticket_price)
       league_price_button.place(relx=0.225, rely=0.53, relwidth=0.05, relheight=0.07)

       # label that shows total losses
       total_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 14))
       total_loss_label.place(relx=0.58, rely=0.44, relwidth=0.08, relheight=0.09)
       # label that shows wage losses for players
       wage_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       wage_loss_label.place(relx=0.58, rely=0.53, relwidth=0.08, relheight=0.045)
       # label that shows wage losses for staff
       stwage_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       stwage_loss_label.place(relx=0.58, rely=0.575, relwidth=0.08, relheight=0.045)
       # label that shows losses from buying players
       transfer_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       transfer_loss_label.place(relx=0.58, rely=0.62, relwidth=0.08, relheight=0.045)
       # label that shows losses from upgrading staff
       stransfer_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       stransfer_loss_label.place(relx=0.58, rely=0.665, relwidth=0.08, relheight=0.045)
       # label that shows loss from facility maintaining
       cost_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       cost_loss_label.place(relx=0.58, rely=0.71, relwidth=0.08, relheight=0.045)
       # label that shows loss from upgrading facilities
       upgrade_loss_label = Label(menu_frames[4], text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12))
       upgrade_loss_label.place(relx=0.58, rely=0.755, relwidth=0.08, relheight=0.045)

   place_finances()

   def get_opponent_skills(team):
       def generate_opponent_skills(ranges):
           # Generate initial random numbers within the specified ranges
           random_numbers = [random.randint(low, high) for low, high in ranges]

           # Calculate the initial sum of the generated numbers
           initial_sum = sum(random_numbers)

           print("Counter attacking, High tempo passing, wing play, passing over the top, playing out of press, defending crosses, defending deep, pressing, set pieces, ball possession")

           print(f"Initial Sum: {initial_sum}")
           print(f"Random numbers: {random_numbers}")

           # Scale the numbers to make the sum equal to the target sum
           scaled_numbers = [int(num * 500 / initial_sum) for num in random_numbers]

           # Calculate the sum of the scaled numbers
           scaled_sum = sum(scaled_numbers)

           print(f"Scaled numbers: {scaled_numbers}")
           print(f"Scaled sum: {scaled_sum}")

           # Distribute the difference to ensure the sum is exactly the target sum
           difference = 500 - scaled_sum
           while difference != 0:
               index = random.choice(range(len(ranges)))
               if difference > 0 and scaled_numbers[index] < ranges[index][1]:
                   scaled_numbers[index] += 1
                   difference -= 1
               elif difference < 0 and scaled_numbers[index] > ranges[index][0]:
                   scaled_numbers[index] -= 1
                   difference += 1

           return scaled_numbers

       # "Counter Attacking", "High Tempo Passing", "Wing Play", "Passing Over The Top", "Playing Out Of Press", "Defending Crosses",
       # "Defending Deep", "Pressing", "Set Pieces", "Ball Possession"
       opponent_playstyle = team[3]
       if opponent_playstyle == 0:
           opponent_skill_ranges = [[30, 60], [50, 70], [40, 60], [35, 55], [50, 65], [40, 60], [30, 70], [45, 70], [30, 65], [45, 70]]
       elif opponent_playstyle == 1:
           opponent_skill_ranges = [[45, 70], [45, 60], [40, 60], [45, 65], [40, 60], [30, 65], [50, 70], [30, 60], [45, 65], [35, 52]]
       elif opponent_playstyle == 2:
           opponent_skill_ranges = [[45, 65], [50, 65], [40, 70], [45, 60], [40, 60], [45, 60], [35, 50], [50, 70], [35, 60], [45, 60]]
       elif opponent_playstyle == 3:
           opponent_skill_ranges = [[40, 70], [35, 50], [40, 60], [50, 70], [35, 50], [40, 60], [40, 70], [35, 55], [45, 60], [30, 55]]

       return generate_opponent_skills(opponent_skill_ranges)


   def get_team_training_report():
       weaknesses = []
       strengths = []
       sorted_focus_variables = sorted(focus_variables.items(), key=lambda item: item[1])
       for key, value in sorted_focus_variables[:3]:
           if value < 40:
               weaknesses.append(key)
           else:
               weaknesses.append("")

       sorted_focus_variables = sorted(focus_variables.items(), key=lambda item: item[1], reverse=True)
       for key, value in sorted_focus_variables[:3]:
           if value > 60:
               strengths.append(key)
           else:
               strengths.append("")

       return weaknesses, strengths

   def place_training():
       global TD_intensity, PM_intensity, BM_intensity, TD_main_focus, PM_main_focus, BM_main_focus, TD_second_focus, PM_second_focus, BM_second_focus, TD_third_focus, PM_third_focus, BM_third_focus, TD_warm_up, PM_warm_up, BM_warm_up, player_report_widgets

       def switch_to_training_report():
           training_heading.config(text="Training Report")
           for i in player_report_widgets:
               i.place_forget()
           player_report_button.config(text="Players Report >", command=switch_to_player_report)

       def switch_to_player_report():
           training_heading.config(text="Players Report")
           player_report_widgets[0].place(relx=0.02, rely=0.7, relwidth=0.455, relheight=0.13)
           for i in range(4):
               player_report_widgets[i*2+1].place(relx=0.02, rely=i*0.03+0.7, relwidth=0.2275, relheight=0.03)
               player_report_widgets[i*2+2].place(relx=0.2475, rely=i*0.03+0.7, relwidth=0.2275, relheight=0.03)
           player_report_button.config(text="Training Report >", command=switch_to_training_report)
           for i in player_report_widgets:
               i.lift()

       # training day bg
       Label(menu_frames[2], bg="#363440").place(relx=0.02, rely=0.05, relwidth=0.3, relheight=0.59)
       Label(menu_frames[2], bg="#26262e", text="Training One", font=("Comic Sans", 25), fg="white").place(relx=0.02, rely=0.05, relwidth=0.3, relheight=0.1)
       # day before matchday training bg
       Label(menu_frames[2], bg="#363440").place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.59)
       Label(menu_frames[2], bg="#26262e", text="Training Two", font=("Comic Sans", 25), fg="white").place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
       # pre match training bg
       Label(menu_frames[2], bg="#363440").place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.59)
       Label(menu_frames[2], bg="#26262e", text="Training Three", font=("Comic Sans", 25), fg="white").place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.1)

       # TEAM TRAINING REPORT
       training_heading = Label(menu_frames[2], text="Training Report", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18))
       training_heading.place(relx=0.02, rely=0.66, relwidth=0.455, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR).place(relx=0.02, rely=0.7, relwidth=0.455, relheight=0.13)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Strengths", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.02, rely=0.7, relwidth=0.2275, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Weaknesses", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.2475, rely=0.7, relwidth=0.2275, relheight=0.04)
       player_report_button = Button(menu_frames[2], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 18), text="Players Report >", command=switch_to_player_report)
       player_report_button.place(relx=0.34, rely=0.66, relwidth=0.135, relheight=0.04)

       player_report_widgets = [Label(menu_frames[2], bg=LIGHT_UI_COLOUR),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16, "bold"), text="Best Training Performers"),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16, "bold"), text="Worst Training Performers"),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16)),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16)),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16)),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16)),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16)),
                                Label(menu_frames[2], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16))]

       # SQUAD REPORT
       Label(menu_frames[2], text="Your Squad Report", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18)).place(relx=0.525, rely=0.66, relwidth=0.455, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR).place(relx=0.525, rely=0.7, relwidth=0.455, relheight=0.13)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Goalkeepers", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.525, rely=0.7, relwidth=0.11375, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Defence", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.63875, rely=0.7, relwidth=0.11375, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Midfield", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.7525, rely=0.7, relwidth=0.11375, relheight=0.04)
       Label(menu_frames[2], bg=LIGHT_UI_COLOUR, text="Attack", fg="white", font=("Comic Sans", 16, "bold")).place(relx=0.86625, rely=0.7, relwidth=0.11375, relheight=0.04)

       #TRAINING:
       # - WARM UP LENGTH
       # - INTENSITY
       # - MAIN FOCUS - defending crosses, setpieces, pressing, playing out of press, defending deep, passing, breaking down low block, passing over the top, wing play
       # - FOCUS 2 - none, defending crosses, setpieces, pressing, playing out of initial press, defending deep, passing, breaking down low block
       # - FOCUS 3 - none, defending crosses, setpieces, pressing, playing out of initial press, defending deep, passing, breaking down low block
       # longer warm up - less likely injuries but leads to longer training sessions
       # players can get unhappy from training sessions being too long

       # TD = TRAINING DAY
       # BM = DAY BEFORE MATCHDAY
       # PM = PRE MATCH TRAINING

       # text for training
       Label(menu_frames[2], text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.02, rely=0.17, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.35, rely=0.17, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.68, rely=0.17, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.02, rely=0.27, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.35, rely=0.27, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.68, rely=0.28, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.02, rely=0.37, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.35, rely=0.37, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.68, rely=0.37, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.02, rely=0.47, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.35, rely=0.47, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.68, rely=0.47, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.02, rely=0.57, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.35, rely=0.57, relwidth=0.15, relheight=0.05)
       Label(menu_frames[2], text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)).place(relx=0.68, rely=0.57, relwidth=0.15, relheight=0.05)

       # stat boost is decided by priority of focus and type of training, each stats is /100
       # 1st focus +5?
       # 2nd focus +3?
       # 3rd focus +1?
       # matchday training X2? boost
       # matchday training gives larger boost to stats but only lasts for that match then goes back to what it was before
       # pre-matchday training is same as scheduled training but happens day before matchday and allows player to organise different training for matches
       # scheduled training happens every day that is simmed, stats which are not trained decrease by 2? each time
       # longer warm up length means injuries are less likely but players will be unhappier with the length of training
       # higher intensity increases sharpness by more but injuries are more likely and stamina recovers by less

       training_focus_options = ["Counter Attacking", "High Tempo Passing", "Wing Play", "Passing Over The Top", "Playing Out Of Press", "Defending Crosses", "Defending Deep", "Pressing", "Set Pieces", "Ball Possession"]

       TD_warm_up = StringVar()
       TD_warm_up.set("Medium")
       TD_warm_up_pick = OptionMenu(menu_frames[2], TD_warm_up, *["Short", "Medium", "Long"])
       TD_warm_up_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       TD_warm_up_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       TD_warm_up_pick.place(relx=0.17, rely=0.17, relwidth=0.1, relheight=0.05)


       BM_warm_up = StringVar()
       BM_warm_up.set("Medium")
       BM_warm_up_pick = OptionMenu(menu_frames[2], BM_warm_up, *["Short", "Medium", "Long"])
       BM_warm_up_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       BM_warm_up_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       BM_warm_up_pick.place(relx=0.5, rely=0.17, relwidth=0.1, relheight=0.05)

       PM_warm_up = StringVar()
       PM_warm_up.set("Medium")
       PM_warm_up_pick = OptionMenu(menu_frames[2], PM_warm_up, *["Short", "Medium", "Long"])
       PM_warm_up_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       PM_warm_up_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       PM_warm_up_pick.place(relx=0.83, rely=0.17, relwidth=0.1, relheight=0.05)

       TD_intensity = StringVar()
       TD_intensity.set("Medium")
       TD_intensity_pick = OptionMenu(menu_frames[2], TD_intensity, *["Low", "Medium", "High"])
       TD_intensity_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       TD_intensity_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       TD_intensity_pick.place(relx=0.17, rely=0.27, relwidth=0.1, relheight=0.05)

       BM_intensity = StringVar()
       BM_intensity.set("Medium")
       BM_intensity_pick = OptionMenu(menu_frames[2], BM_intensity, *["Low", "Medium", "High"])
       BM_intensity_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       BM_intensity_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       BM_intensity_pick.place(relx=0.5, rely=0.27, relwidth=0.1, relheight=0.05)

       PM_intensity = StringVar()
       PM_intensity.set("Medium")
       PM_intensity_pick = OptionMenu(menu_frames[2], PM_intensity, *["Low", "Medium", "High"])
       PM_intensity_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       PM_intensity_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
       PM_intensity_pick.place(relx=0.83, rely=0.27, relwidth=0.1, relheight=0.05)

       TD_main_focus = StringVar()
       TD_main_focus.set("Pressing")
       TD_main_focus_pick = OptionMenu(menu_frames[2], TD_main_focus,
                                       *training_focus_options)
       TD_main_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       TD_main_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       TD_main_focus_pick.place(relx=0.17, rely=0.37, relwidth=0.1, relheight=0.05)

       BM_main_focus = StringVar()
       BM_main_focus.set("Wing Play")
       BM_main_focus_pick = OptionMenu(menu_frames[2], BM_main_focus,
                                       *training_focus_options)
       BM_main_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       BM_main_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       BM_main_focus_pick.place(relx=0.5, rely=0.37, relwidth=0.1, relheight=0.05)

       PM_main_focus = StringVar()
       PM_main_focus.set("Wing Play")
       PM_main_focus_pick = OptionMenu(menu_frames[2], PM_main_focus,
                                       *training_focus_options)
       PM_main_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       PM_main_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       PM_main_focus_pick.place(relx=0.83, rely=0.37, relwidth=0.1, relheight=0.05)

       TD_second_focus = StringVar()
       TD_second_focus.set("Defending Crosses")
       TD_second_focus_pick = OptionMenu(menu_frames[2], TD_second_focus,
                                       *training_focus_options)
       TD_second_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       TD_second_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       TD_second_focus_pick.place(relx=0.17, rely=0.47, relwidth=0.1, relheight=0.05)

       BM_second_focus = StringVar()
       BM_second_focus.set("Set Pieces")
       BM_second_focus_pick = OptionMenu(menu_frames[2], BM_second_focus,
                                       *training_focus_options)
       BM_second_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       BM_second_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       BM_second_focus_pick.place(relx=0.5, rely=0.47, relwidth=0.1, relheight=0.05)

       PM_second_focus = StringVar()
       PM_second_focus.set("Ball Possession")
       PM_second_focus_pick = OptionMenu(menu_frames[2], PM_second_focus,
                                       *training_focus_options)
       PM_second_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       PM_second_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       PM_second_focus_pick.place(relx=0.83, rely=0.47, relwidth=0.1, relheight=0.05)

       TD_third_focus = StringVar()
       TD_third_focus.set("High Tempo Passing")
       TD_third_focus_pick = OptionMenu(menu_frames[2], TD_third_focus,
                                         *training_focus_options)
       TD_third_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       TD_third_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       TD_third_focus_pick.place(relx=0.17, rely=0.57, relwidth=0.1, relheight=0.05)

       BM_third_focus = StringVar()
       BM_third_focus.set("Counter Attacking")
       BM_third_focus_pick = OptionMenu(menu_frames[2], BM_third_focus,
                                         *training_focus_options)
       BM_third_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       BM_third_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       BM_third_focus_pick.place(relx=0.5, rely=0.57, relwidth=0.1, relheight=0.05)

       PM_third_focus = StringVar()
       PM_third_focus.set("Defending Deep")
       PM_third_focus_pick = OptionMenu(menu_frames[2], PM_third_focus,
                                         *training_focus_options)
       PM_third_focus_pick.configure(background="#26262e", foreground="white", borderwidth=0)
       PM_third_focus_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))
       PM_third_focus_pick.place(relx=0.83, rely=0.57, relwidth=0.1, relheight=0.05)

   place_training()

   team_strength_one = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_strength_one.place(relx=0.02, rely=0.74, relwidth=0.2275, relheight=0.03)
   team_strength_two = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_strength_two.place(relx=0.02, rely=0.77, relwidth=0.2275, relheight=0.03)
   team_strength_three = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_strength_three.place(relx=0.02, rely=0.8, relwidth=0.2275, relheight=0.03)
   team_weakness_one = Label(menu_frames[2], fg="red", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_weakness_one.place(relx=0.2475, rely=0.74, relwidth=0.2275, relheight=0.03)
   team_weakness_two = Label(menu_frames[2], fg="red", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_weakness_two.place(relx=0.2475, rely=0.77, relwidth=0.2275, relheight=0.03)
   team_weakness_three = Label(menu_frames[2], fg="red", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_weakness_three.place(relx=0.2475, rely=0.8, relwidth=0.2275, relheight=0.03)

   team_goalkeepers_quality = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_goalkeepers_quality.place(relx=0.525, rely=0.74, relwidth=0.11375, relheight=0.03)
   team_goalkeepers_depth = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_goalkeepers_depth.place(relx=0.525, rely=0.78, relwidth=0.11375, relheight=0.03)
   team_defence_quality = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_defence_quality.place(relx=0.63875, rely=0.74, relwidth=0.11375, relheight=0.03)
   team_defence_depth = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_defence_depth.place(relx=0.63875, rely=0.78, relwidth=0.11375, relheight=0.03)
   team_midfield_quality = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_midfield_quality.place(relx=0.7525, rely=0.74, relwidth=0.11375, relheight=0.03)
   team_midfield_depth = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_midfield_depth.place(relx=0.7525, rely=0.78, relwidth=0.11375, relheight=0.03)
   team_attack_quality = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_attack_quality.place(relx=0.86625, rely=0.74, relwidth=0.11375, relheight=0.03)
   team_attack_depth = Label(menu_frames[2], fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 16))
   team_attack_depth.place(relx=0.86625, rely=0.78, relwidth=0.11375, relheight=0.03)

   # called after each stadium upgrade to work out values for next upgrade
   def next_stadium_upgrade():
       global next_stadium_capacity, next_stadium_upgrade_cost, next_stadium_maintain_cost
       next_stadium_capacity = STADIUM_CAPACITY + random.randint(4500, 12000)
       added_cost = 0
       if 30000 > STADIUM_CAPACITY >= 20000:
           added_cost = 15000000
       elif 40000 > STADIUM_CAPACITY >= 30000:
           added_cost = 30000000
       elif 50000 > STADIUM_CAPACITY >= 40000:
           added_cost = 45000000
       elif 60000 > STADIUM_CAPACITY >= 50000:
           added_cost = 60000000
       elif 70000 > STADIUM_CAPACITY >= 60000:
           added_cost = 70000000
       elif STADIUM_CAPACITY >= 70000:
           added_cost = 93000000
       next_stadium_upgrade_cost = int(((STADIUM_CAPACITY * 1.6) * 2 * (next_stadium_capacity - STADIUM_CAPACITY)) / 28) + added_cost
       next_stadium_maintain_cost = int(next_stadium_capacity / 60)

   def next_facility_upgrade(facility_type, new_rating):
       global next_training_ground_cost, next_youth_centre_cost

       cost = 0

       if new_rating == 2:
           cost = random.randint(2000000, 3500000)
       elif new_rating == 3:
           cost = random.randint(4500000, 6000000)
       elif new_rating == 4:
           cost = random.randint(7000000, 9000000)
       elif new_rating == 5:
           cost = random.randint(11000000, 13000000)
       elif new_rating == 6:
           cost = random.randint(15000000, 17000000)
       elif new_rating == 7:
           cost = random.randint(19000000, 23000000)
       elif new_rating == 8:
           cost = random.randint(25000000, 27000000)
       elif new_rating == 9:
           cost = random.randint(29000000, 32000000)
       elif new_rating == 10:
           cost = random.randint(36000000, 39000000)

       if facility_type == "training ground":
           next_training_ground_cost = cost
       elif facility_type == "youth centre":
           next_youth_centre_cost = cost

   # gets intital values for each facilites first upgrades, 2 is level of facility after first upgrade
   next_stadium_upgrade()
   next_facility_upgrade("youth centre", 2)
   next_facility_upgrade("training ground", 2)

   def place_facilities():
       global current_youth_maintenance, current_training_maintenance, next_youth_maintenance, next_training_maintenance, prev_stadium_attendance, previous_attendance_label, youth_centre_heading
       def get_facility_maintenance_cost(rating):
           cost = 0
           if rating == 1:
               cost = random.randint(9, 16) * 10
           elif rating == 2:
               cost = random.randint(18, 23) * 10
           elif rating == 3:
               cost = random.randint(24, 29) * 10
           elif rating == 4:
               cost = random.randint(31, 35) * 10
           elif rating == 5:
               cost = random.randint(37, 40) * 10
           elif rating == 6:
               cost = random.randint(41, 45) * 10
           elif rating == 7:
               cost = random.randint(47, 51) * 10
           elif rating == 8:
               cost = random.randint(52, 56) * 10
           elif rating == 9:
               cost = random.randint(59, 64) * 10
           elif rating == 10:
               cost = random.randint(67, 70) * 10

           return cost

       def show_upgrade_message(facility_type):
           confirm_staff_upgrade_label.config(text=f"Are you sure you want to upgrade your {facility_type}?")
           upgrade_staff_labels[2].config(text="Current maintenance cost")
           upgrade_staff_labels[4].config(text="New maintenance cost")
           if facility_type == "stadium":
               upgrade_staff_labels[1].config(text="Current capacity")
               upgrade_staff_labels[3].config(text="New capacity")
               staff_current_rating_label.config(text="{:,}".format(STADIUM_CAPACITY))
               staff_current_wage_label.config(text="€{:,}".format(STADIUM_MAINTAIN_COST))
               staff_new_rating_label.config(text="{:,}".format(next_stadium_capacity))
               staff_new_wage_label.config(text="€{:,}".format(next_stadium_maintain_cost))
               staff_upgrade_cost_label.config(text="€{:,}".format(next_stadium_upgrade_cost))
           elif facility_type == "training ground":
               rating = int(extract_digits(training_ground_heading.cget("text")))
               staff_current_rating_label.config(text=rating)
               staff_new_rating_label.config(text=rating+1)
               staff_upgrade_cost_label.config(text="€{:,}".format(next_training_ground_cost))
               staff_current_wage_label.config(text="€{:,}".format(current_training_maintenance))
               staff_new_wage_label.config(text="€{:,}".format(next_training_maintenance))
           elif facility_type == "youth centre":
               rating = int(extract_digits(youth_centre_heading.cget("text")))
               staff_current_rating_label.config(text=rating)
               staff_new_rating_label.config(text=rating + 1)
               staff_upgrade_cost_label.config(text="€{:,}".format(next_youth_centre_cost))
               staff_current_wage_label.config(text="€{:,}".format(current_youth_maintenance))
               staff_new_wage_label.config(text="€{:,}".format(next_youth_maintenance))

           upgrade_staff_button.config(command=lambda: upgrade_facility(facility_type))
           cancel_upgrade_staff_button.config(command=cancel_upgrade)
           hide_menu_buttons_grey()
           change_menu(9)

       def upgrade_facility(facility_type):
           global upgrade_loss_label, STADIUM_CAPACITY, STADIUM_MAINTAIN_COST, current_youth_maintenance, current_training_maintenance, next_youth_maintenance, next_training_maintenance
           if facility_type == "stadium":
               STADIUM_CAPACITY = next_stadium_capacity
               STADIUM_MAINTAIN_COST = next_stadium_maintain_cost
               add_loss(next_stadium_upgrade_cost, upgrade_loss_label, False)
               stadium_capacity_label.config(text="Capacity: {:,}".format(STADIUM_CAPACITY))
               next_stadium_upgrade()
               change_menu(8)
               show_menu_buttons()
           elif facility_type == "training ground":
               rating = int(extract_digits(training_ground_heading.cget("text"))) + 1
               current_training_maintenance = next_training_maintenance
               add_loss(next_training_ground_cost, upgrade_loss_label, False)
               training_ground_heading.config(text=f"Training ground LVL {rating}")
               next_training_maintenance = get_facility_maintenance_cost(int(extract_digits(training_ground_heading.cget("text")))+1)
               if rating == 10:
                   upgrade_training_button.place_forget()
               else:
                   next_facility_upgrade("training ground", rating + 1)
               change_menu(8)
               show_menu_buttons()
           elif facility_type == "youth centre":
               rating = int(extract_digits(youth_centre_heading.cget("text"))) + 1
               current_youth_maintenance = next_youth_maintenance
               add_loss(next_youth_centre_cost, upgrade_loss_label, False)
               youth_centre_heading.config(text=f"Youth centre LVL {rating}")
               next_youth_maintenance = get_facility_maintenance_cost(int(extract_digits(youth_centre_heading.cget("text")))+1)
               if rating == 10:
                   upgrade_youth_button.place_forget()
               else:
                   next_facility_upgrade("youth centre", rating + 1)
               change_menu(8)
               show_menu_buttons()


       def cancel_upgrade():
           upgrade_staff_labels[2].config(text="Current wage")
           upgrade_staff_labels[4].config(text="New wage")
           upgrade_staff_labels[1].config(text="Current rating")
           upgrade_staff_labels[3].config(text="New rating")
           change_menu(8)
           show_menu_buttons()
       # BACKGROUND
       # stadium
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.12, rely=0.2, relwidth=0.3, relheight=0.1)
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.12, rely=0.3, relwidth=0.06, relheight=0.17)
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.36, rely=0.3, relwidth=0.06, relheight=0.17)
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.12, rely=0.47, relwidth=0.3, relheight=0.1)
       # centre circle
       Label(menu_frames[8], bg="green", fg="white", text="O", font=("Comic sans", 40)).place(relx=0.219, rely=0.343, relwidth=0.1, relheight=0.08)
       # border lines
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.3, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.268, rely=0.3, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.358, rely=0.3, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.3, relwidth=0.18, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.466, relwidth=0.18, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.34, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.426, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.208, rely=0.34, relwidth=0.002, relheight=0.09)
       Label(menu_frames[8], bg="white").place(relx=0.33, rely=0.34, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.33, rely=0.426, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.33, rely=0.34, relwidth=0.002, relheight=0.09)
       Label(menu_frames[8], bg="white").place(relx=0.33, rely=0.34, relwidth=0.028, relheight=0.004)
       # goalkeeper boxes (boxes inside pen boxes)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.365, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.18, rely=0.401, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.192, rely=0.365, relwidth=0.002, relheight=0.04)
       Label(menu_frames[8], bg="white").place(relx=0.346, rely=0.365, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.346, rely=0.401, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.346, rely=0.365, relwidth=0.002, relheight=0.04)

       # training ground
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.1)
       # centre circle
       Label(menu_frames[8], bg="green", fg="white", text="O", font=("Comic sans", 40)).place(relx=0.789, rely=0.193, relwidth=0.1, relheight=0.08)
       # border lines
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.15, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.838, rely=0.15, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.928, rely=0.15, relwidth=0.002, relheight=0.17)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.15, relwidth=0.18, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.316, relwidth=0.18, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.19, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.276, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.778, rely=0.19, relwidth=0.002, relheight=0.09)
       Label(menu_frames[8], bg="white").place(relx=0.9, rely=0.19, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.9, rely=0.276, relwidth=0.028, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.9, rely=0.19, relwidth=0.002, relheight=0.09)
       Label(menu_frames[8], bg="white").place(relx=0.9, rely=0.19, relwidth=0.028, relheight=0.004)
       # goalkeeper boxes (boxes inside pen boxes)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.215, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.251, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.762, rely=0.215, relwidth=0.002, relheight=0.04)
       Label(menu_frames[8], bg="white").place(relx=0.916, rely=0.215, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.916, rely=0.251, relwidth=0.012, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.916, rely=0.215, relwidth=0.002, relheight=0.04)

       # youth centre
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.53, rely=0.5, relwidth=0.06, relheight=0.1)
       Label(menu_frames[8], bg=LIGHT_UI_COLOUR).place(relx=0.59, rely=0.5, relwidth=0.09, relheight=0.2)
       Label(menu_frames[8], bg="#787777").place(relx=0.68, rely=0.5, relwidth=0.09, relheight=0.154)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.5, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.53, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.56, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.59, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.62, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.68, rely=0.65, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.5, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.53, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.56, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.59, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.62, relwidth=0.02, relheight=0.004)
       Label(menu_frames[8], bg="white").place(relx=0.75, rely=0.65, relwidth=0.02, relheight=0.004)

       # LABELS
       stadium_heading = Label(menu_frames[8], bg="green", fg="white", font=("Comic sans", 20), text=STADIUM_NAME)
       stadium_heading.place(relx=0.12, rely=0.1, relwidth=0.3, relheight=0.1)
       training_ground_heading = Label(menu_frames[8], bg="green", fg="white", font=("Comic sans", 20), text="Training ground LVL 1")
       training_ground_heading.place(relx=0.65, rely=0.05, relwidth=0.3, relheight=0.1)
       youth_centre_heading = Label(menu_frames[8], bg="green", fg="white", font=("Comic sans", 20), text="Youth centre LVL 1")
       youth_centre_heading.place(relx=0.5, rely=0.43, relwidth=0.3, relheight=0.06)

       # VALUE LABELS
       stadium_capacity_label = Label(menu_frames[8], bg="green", fg="white", font=("Comic sans", 23), text="Capacity: {:,}".format(STADIUM_CAPACITY))
       stadium_capacity_label.place(relx=0.12, rely=0.57, relwidth=0.3, relheight=0.08)
       previous_attendance_label = Label(menu_frames[8], bg="green", fg="white", font=("Comic sans", 18), text=f"Previous Match Attendance: {prev_stadium_attendance}")
       previous_attendance_label.place(relx=0.12, rely=0.65, relwidth=0.3, relheight=0.08)

       # BUTTONS
       upgrade_stadium_button = Button(menu_frames[8], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade", command=lambda:show_upgrade_message("stadium"))
       upgrade_stadium_button.place(relx=0.16, rely=0.73, relwidth=0.22, relheight=0.08)
       upgrade_training_button = Button(menu_frames[8], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade", command=lambda:show_upgrade_message("training ground"))
       upgrade_training_button.place(relx=0.69, rely=0.33, relwidth=0.22, relheight=0.08)
       upgrade_youth_button = Button(menu_frames[8], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade", command=lambda:show_upgrade_message("youth centre"))
       upgrade_youth_button.place(relx=0.54, rely=0.715, relwidth=0.22, relheight=0.08)

       current_youth_maintenance = get_facility_maintenance_cost(int(extract_digits(youth_centre_heading.cget("text"))))
       current_training_maintenance = get_facility_maintenance_cost(int(extract_digits(training_ground_heading.cget("text"))))
       next_youth_maintenance = get_facility_maintenance_cost(int(extract_digits(youth_centre_heading.cget("text")))+1)
       next_training_maintenance = get_facility_maintenance_cost(int(extract_digits(training_ground_heading.cget("text")))+1)


   place_facilities()

   # appears at start of a season
   def season_start_menu():
       global league, next_opponent, counter_attacking, high_tempo_passing, wing_play, passing_over_the_top, playing_out_of_press, defending_deep, defending_crosses, pressing, set_pieces, ball_possession, next_opponent_skills, qualified_for_europe, cup_div_4, cup_div_3, cup_div_2, cup_div_1, cup_r32_opponent, cup_r16_opponent, cup_qf_opponent, cup_sf_opponent, cup_f_opponent
       for i in squad:
           i.get_extension_length_offer()
           i.fitness = 100
           i.sharpness = 0
           i.form = random.randint(45, 55)
           i.matches_played = 0
           i.matches_not_played = 0
           i.training_happiness = 50

       update_morale()
       update_player_report()

       counter_attacking = 50
       high_tempo_passing = 50
       wing_play = 50
       passing_over_the_top = 50
       playing_out_of_press = 50
       defending_crosses = 50
       defending_deep = 50
       pressing = 50
       set_pieces = 50
       ball_possession = 50

       qualified_for_europe = False

       for i in schedule_labels:
           i.config(fg="white")

       if year != 2024:
           for i in eng_1 + eng_2 + eng_3 + eng_4 + fra_1 + fra_2 + ger_1 + ger_2 + ita_1 + ita_2 + spa_1 + spa_2:
               i[1] += random.randint(0, 6) - 3
               if i[1] > 93:
                   i[1] = 93
               elif i[1] < 53:
                   i[1] = 53

           for i in [eng_1, eng_2, eng_3, eng_4, fra_1, fra_2, ger_1, ger_2, ita_1, ita_2, spa_1, spa_2]:
               if i[0][6] == 0:
                   i.sort(key=lambda j: j[1] + j[2], reverse=True)

           counter = 0
           # Promotion/Relegation logic
           for leagues in [(eng_1, eng_2), (eng_2, eng_3), (eng_3, eng_4),
                           (fra_1, fra_2), (ger_1, ger_2), (ita_1, ita_2), (spa_1, spa_2)]:

               top_league, lower_league = leagues

               # Check if the current leagues are part of the English leagues
               if top_league in [eng_1, eng_2, eng_3, eng_4]:
                   # Calculate the start and end indices for slicing
                   start_idx = -3 * (counter + 1)
                   end_idx = -3 * counter if counter > 0 else None

               print("RELEGATED")
               for i in top_league[start_idx:end_idx]:
                   print(i)
                   lower_league.append(i)
                   top_league.remove(i)
                   if i[0] == CLUB_NAME:
                       league = lower_league
                   else:
                       i[1] -= random.randint(0, 4)
                       i[2] -= random.randint(0, 4)

               print("PROMOTED")
               playoffs_simmed = True
               for i in league[2:6]:
                   if i[0] == CLUB_NAME:
                       playoffs_simmed = False
               if lower_league != league or playoffs_simmed:
                   for i in lower_league[:3]:
                       print(i)
                       top_league.append(i)
                       lower_league.remove(i)
                       if i[0] == CLUB_NAME:
                           league = top_league
                       else:
                           i[1] += random.randint(0, 4)
                           i[2] += random.randint(0, 4)
               else:
                   for i in lower_league[:2]:
                       print(i)
                       top_league.append(i)
                       lower_league.remove(i)
                       if i[0] == CLUB_NAME:
                           league = top_league
                       else:
                           i[1] += random.randint(0, 4)
                           i[2] += random.randint(0, 4)
                   print(playoffs_winner)
                   lower_league.remove(playoffs_winner)
                   if playoffs_winner[0] == CLUB_NAME:
                       league = top_league
                   else:
                       playoffs_winner[1] += random.randint(0, 4)
                       playoffs_winner[2] += random.randint(0, 4)
                   top_league.append(playoffs_winner)

               counter += 1

           if league == eng_1:
               for i in eng_1[:5]:
                   if i[0] == CLUB_NAME:
                       qualified_for_europe = True
           elif league == fra_1:
               for i in fra_1[:3]:
                   if i[0] == CLUB_NAME:
                       qualified_for_europe = True
           elif league == ger_1:
               for i in ger_1[:5]:
                   if i[0] == CLUB_NAME:
                       qualified_for_europe = True
           elif league == ita_1:
               for i in ita_1[:5]:
                   if i[0] == CLUB_NAME:
                       qualified_for_europe = True
           elif league == spa_1:
               for i in spa_1[:5]:
                   if i[0] == CLUB_NAME:
                        qualified_for_europe = True

       cup_div_4 = []
       cup_div_3 = []
       cup_div_2 = []
       cup_div_1 = []

       if CLUB_COUNTRY == "England":
           for i in eng_4 + eng_3:
               if i[0] != CLUB_NAME:
                   cup_div_4.append(i)
           for i in eng_2:
               if i[0] != CLUB_NAME:
                   cup_div_3.append(i)
           eng_1.sort(key=lambda i: i[1])
           for i in eng_1[:13]:
               if i[0] != CLUB_NAME:
                   cup_div_2.append(i)
           for i in eng_1[13:]:
               if i[0] != CLUB_NAME:
                   cup_div_1.append(i)
           random_chance = random.randint(1, 100)
           if random_chance < 50:
               cup_r32_opponent = random.choice(cup_div_4)
               cup_div_4.remove(cup_r32_opponent)
           elif random_chance < 85:
               cup_r32_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r32_opponent)
           elif random_chance < 95:
               cup_r32_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r32_opponent)
           else:
               cup_r32_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r32_opponent)

           random_chance = random.randint(1, 100)
           if random_chance < 40:
               cup_r16_opponent = random.choice(cup_div_4)
               cup_div_4.remove(cup_r16_opponent)
           elif random_chance < 75:
               cup_r16_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r16_opponent)
           elif random_chance < 90:
               cup_r16_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r16_opponent)
           else:
               cup_r16_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r16_opponent)

           random_chance = random.randint(1, 100)
           if random_chance < 15:
               cup_qf_opponent = random.choice(cup_div_4)
               cup_div_4.remove(cup_qf_opponent)
           elif random_chance < 40:
               cup_qf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_qf_opponent)
           elif random_chance < 80:
               cup_qf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_qf_opponent)
           else:
               cup_qf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_qf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 5:
               cup_sf_opponent = random.choice(cup_div_4)
               cup_div_4.remove(cup_sf_opponent)
           elif random_chance < 15:
               cup_sf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_sf_opponent)
           elif random_chance < 45:
               cup_sf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_sf_opponent)
           else:
               cup_sf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_sf_opponent)

           random_chance = random.randint(1, 100)
           if random_chance < 2:
               cup_f_opponent = random.choice(cup_div_4)
               cup_div_4.remove(cup_f_opponent)
           elif random_chance < 8:
               cup_f_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_f_opponent)
           elif random_chance < 16:
               cup_f_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_f_opponent)
           else:
               cup_f_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_f_opponent)

       elif CLUB_COUNTRY == "France":
           for i in fra_2:
               if i[0] != CLUB_COUNTRY:
                   cup_div_3.append(i)
           fra_1.sort(key=lambda i: i[1])
           for i in fra_1[:13]:
               if i[0] != CLUB_NAME:
                   cup_div_2.append(i)
           for i in fra_1[13:]:
               if i[0] != CLUB_NAME:
                   cup_div_1.append(i)

           random_chance = random.randint(1, 100)

           if random_chance < 80:
               cup_r32_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r32_opponent)
           elif random_chance < 95:
               cup_r32_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r32_opponent)
           else:
               cup_r32_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r32_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 65:
               cup_r16_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r16_opponent)
           elif random_chance < 85:
               cup_r16_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r16_opponent)
           else:
               cup_r16_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r16_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 40:
               cup_qf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_qf_opponent)
           elif random_chance < 75:
               cup_qf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_qf_opponent)
           else:
               cup_qf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_qf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 15:
               cup_sf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_sf_opponent)
           elif random_chance < 40:
               cup_sf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_sf_opponent)
           else:
               cup_sf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_sf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 2:
               cup_f_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_f_opponent)
           elif random_chance < 15:
               cup_f_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_f_opponent)
           else:
               cup_f_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_f_opponent)

       elif CLUB_COUNTRY == "Germany":
           for i in ger_2:
               if i[0] != CLUB_COUNTRY:
                   cup_div_3.append(i)
           ger_1.sort(key=lambda i: i[1])
           for i in ger_1[:13]:
               if i[0] != CLUB_NAME:
                   cup_div_2.append(i)
           for i in ger_1[13:]:
               if i[0] != CLUB_NAME:
                   cup_div_1.append(i)

           random_chance = random.randint(1, 100)

           if random_chance < 80:
               cup_r32_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r32_opponent)
           elif random_chance < 95:
               cup_r32_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r32_opponent)
           else:
               cup_r32_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r32_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 65:
               cup_r16_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r16_opponent)
           elif random_chance < 85:
               cup_r16_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r16_opponent)
           else:
               cup_r16_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r16_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 40:
               cup_qf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_qf_opponent)
           elif random_chance < 75:
               cup_qf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_qf_opponent)
           else:
               cup_qf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_qf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 15:
               cup_sf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_sf_opponent)
           elif random_chance < 40:
               cup_sf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_sf_opponent)
           else:
               cup_sf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_sf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 2:
               cup_f_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_f_opponent)
           elif random_chance < 15:
               cup_f_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_f_opponent)
           else:
               cup_f_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_f_opponent)

       elif CLUB_COUNTRY == "Italy":
           for i in ita_2:
               if i[0] != CLUB_COUNTRY:
                   cup_div_3.append(i)
           ita_1.sort(key=lambda i: i[1])
           for i in ita_1[:13]:
               if i[0] != CLUB_NAME:
                   cup_div_2.append(i)
           for i in ita_1[13:]:
               if i[0] != CLUB_NAME:
                   cup_div_1.append(i)

           random_chance = random.randint(1, 100)

           if random_chance < 80:
               cup_r32_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r32_opponent)
           elif random_chance < 95:
               cup_r32_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r32_opponent)
           else:
               cup_r32_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r32_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 65:
               cup_r16_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r16_opponent)
           elif random_chance < 85:
               cup_r16_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r16_opponent)
           else:
               cup_r16_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r16_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 40:
               cup_qf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_qf_opponent)
           elif random_chance < 75:
               cup_qf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_qf_opponent)
           else:
               cup_qf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_qf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 15:
               cup_sf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_sf_opponent)
           elif random_chance < 40:
               cup_sf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_sf_opponent)
           else:
               cup_sf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_sf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 2:
               cup_f_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_f_opponent)
           elif random_chance < 15:
               cup_f_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_f_opponent)
           else:
               cup_f_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_f_opponent)
       else:
           for i in spa_2:
               if i[0] != CLUB_COUNTRY:
                   cup_div_3.append(i)
           spa_1.sort(key=lambda i: i[1])
           for i in spa_1[:13]:
               if i[0] != CLUB_NAME:
                   cup_div_2.append(i)
           for i in spa_1[13:]:
               if i[0] != CLUB_NAME:
                   cup_div_1.append(i)

           random_chance = random.randint(1, 100)

           if random_chance < 80:
               cup_r32_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r32_opponent)
           elif random_chance < 95:
               cup_r32_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r32_opponent)
           else:
               cup_r32_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r32_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 65:
               cup_r16_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_r16_opponent)
           elif random_chance < 85:
               cup_r16_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_r16_opponent)
           else:
               cup_r16_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_r16_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 40:
               cup_qf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_qf_opponent)
           elif random_chance < 75:
               cup_qf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_qf_opponent)
           else:
               cup_qf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_qf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 15:
               cup_sf_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_sf_opponent)
           elif random_chance < 40:
               cup_sf_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_sf_opponent)
           else:
               cup_sf_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_sf_opponent)

           random_chance = random.randint(1, 100)

           if random_chance < 2:
               cup_f_opponent = random.choice(cup_div_3)
               cup_div_3.remove(cup_f_opponent)
           elif random_chance < 15:
               cup_f_opponent = random.choice(cup_div_2)
               cup_div_2.remove(cup_f_opponent)
           else:
               cup_f_opponent = random.choice(cup_div_1)
               cup_div_1.remove(cup_f_opponent)

       create_league_table()

       create_opponent_list()
       next_opponent = opponents_list[0]
       next_opponent_analysis_label.config(text=next_opponent[0])
       next_opponent_league_label.config(text=get_team_league(next_opponent[0]))
       get_team_stats()
       next_opponent_skills = get_opponent_skills(next_opponent)
       competition_name.config(text=next_opponent[10])
       match_year = year
       if next_match_month < month:
           match_year += 1
       match_date.configure(text=f"{next_match_day} {months[next_match_month - 1]} {match_year}")

       skill_names = ["Counter Attacking", "High Tempo Passing", "Wing Play", "Passing Over The Top", "Playing Out Of Press", "Defending Crosses", "Defending Deep",
                      "Pressing", "Set Pieces", "Ball Possession"]
       best_skills = []

       for i in enumerate(next_opponent_skills):
           best_skills.append([skill_names[i[0]], i[1]])

       best_skills.sort(key=lambda i: i[1], reverse=True)

       opponent_strengths_labels[0].config(text=best_skills[0][0])
       opponent_strengths_labels[1].config(text=best_skills[1][0])
       opponent_strengths_labels[2].config(text=best_skills[2][0])

       opponent_weaknesses_labels[0].config(text=best_skills[-1][0])
       opponent_weaknesses_labels[1].config(text=best_skills[-2][0])
       opponent_weaknesses_labels[2].config(text=best_skills[-3][0])

       if next_opponent[3] == 0:
           opponent_attack_style_label.config(text="Possession")
       elif next_opponent[3] == 1:
           opponent_attack_style_label.config(text="Counter Attacking")
       elif next_opponent[3] == 2:
           opponent_attack_style_label.config(text="Physical")
       elif next_opponent[3] == 3:
           opponent_attack_style_label.config(text="Direct")
       else:
           opponent_attack_style_label.config(text="Balanced")

       if next_opponent[9] == "H":
           home_team_name.config(text=CLUB_NAME)
           away_team_name.config(text=next_opponent[0])
       else:
           away_team_name.config(text=CLUB_NAME)
           home_team_name.config(text=next_opponent[0])

       labels = []

       def go_to_menu(old_labels):
           for i in old_labels:
               i.destroy()
           popup_message.config(text="The board is informing you that the transfer window is now open.\nDuring this time you may negotiate with other clubs to\nbuy and sell players.\n\nThe window is open from today and will close on September 1st.")
           change_menu(12)
           hide_menu_buttons_grey()

       def get_merch_total_income():
           global TOTAL_MERCH_REVENUE
           # gets club's rating out of 20
           club_rating_value = int(club_rating.cget("text").split("/")[0])
           # decides total merchandise income to be made across the whole season
           if club_rating_value == 1:
               TOTAL_MERCH_REVENUE = random.randint(115, 170) * 1000
           elif club_rating_value == 2:
               TOTAL_MERCH_REVENUE = random.randint(190, 250) * 1000
           elif club_rating_value == 3:
               TOTAL_MERCH_REVENUE = random.randint(250, 310) * 1000
           elif club_rating_value == 4:
               TOTAL_MERCH_REVENUE = random.randint(320, 380) * 1000
           elif club_rating_value == 5:
               TOTAL_MERCH_REVENUE = random.randint(410, 460) * 1000
           elif club_rating_value == 6:
               TOTAL_MERCH_REVENUE = random.randint(500, 570) * 1000
           elif club_rating_value == 7:
               TOTAL_MERCH_REVENUE = random.randint(630, 690) * 1000
           elif club_rating_value == 8:
               TOTAL_MERCH_REVENUE = random.randint(750, 850) * 1000
           elif club_rating_value == 9:
               TOTAL_MERCH_REVENUE = random.randint(920, 1050) * 1000
           elif club_rating_value == 10:
               TOTAL_MERCH_REVENUE = random.randint(1150, 1300) * 1000
           elif club_rating_value == 11:
               TOTAL_MERCH_REVENUE = random.randint(1500, 1800) * 1000
           elif club_rating_value == 12:
               TOTAL_MERCH_REVENUE = random.randint(2100, 2500) * 1000
           elif club_rating_value == 13:
               TOTAL_MERCH_REVENUE = random.randint(2900, 3350) * 1000
           elif club_rating_value == 14:
               TOTAL_MERCH_REVENUE = random.randint(3800, 4500) * 1000
           elif club_rating_value == 15:
               TOTAL_MERCH_REVENUE = random.randint(5000, 6000) * 1000
           elif club_rating_value == 16:
               TOTAL_MERCH_REVENUE = random.randint(6800, 8000) * 1000
           elif club_rating_value == 17:
               TOTAL_MERCH_REVENUE = random.randint(9100, 12000) * 1000
           elif club_rating_value == 18:
               TOTAL_MERCH_REVENUE = random.randint(17000, 24000) * 1000
           elif club_rating_value == 19:
               TOTAL_MERCH_REVENUE = random.randint(30000, 56000) * 1000
           elif club_rating_value == 20:
               TOTAL_MERCH_REVENUE = random.randint(88000, 140000) * 1000


       def objective_overview(old_labels):
           global league_objective, domestic_objective, continental_objective
           club_rating_value =  int(club_rating.cget("text").split("/")[0])

           if club_rating_value < 5:
               domestic_objective.config(text="Reach Round of 32")
           elif club_rating_value < 11:
               domestic_objective.config(text="Reach Round of 16")
           elif club_rating_value < 17:
               domestic_objective.config(text="Reach Quarter Final")
           elif club_rating_value < 19:
               domestic_objective.config(text="Reach Semi Final")
           else:
               domestic_objective.config(text="Win The Cup")

           if not qualified_for_europe:
               continental_objective.config(text="N/A")
           elif club_rating_value < 16:
               continental_objective.config(text="Fight in League Phase")
           elif club_rating_value < 19:
               continental_objective.config(text="Reach Round of 16")
           elif club_rating_value == 19:
               continental_objective.config(text="Reach Semi Final")
           else:
               continental_objective.config(text="Win The Cup")

           for i in old_labels:
               i.destroy()
           labels = [Label(menu_frames[7], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18), bd=5, relief="raised", text="These are the goals set by the board for this season's competitions.\nAchieving them enhances your job security and maintains your position as manager.\nHowever, keep in mind that the board will also assess other areas such as\nsquad morale and your financial management of the club "),
                     Label(menu_frames[7], bg=LIGHT_UI_COLOUR),
                     Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18, "bold"), text="League Objective"),
                     Label(menu_frames[7], bg="#3F3F4E", fg="white", font=("Comic sans", 18, "bold"), text="Domestic Objective"),
                     Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 18, "bold"), text="Continental Objective"),
                     Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=league_objective.cget("text")),
                     Label(menu_frames[7], bg="#3F3F4E", fg="white", font=("Comic sans", 16), text=domestic_objective.cget("text")),
                     Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=continental_objective.cget("text")),
                     Button(menu_frames[7], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Next", command=lambda: go_to_menu(labels))]
           labels[0].place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.2)
           labels[1].place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.3)
           labels[2].place(relx=0.25, rely=0.4, relwidth=0.166, relheight=0.05)
           labels[3].place(relx=0.416, rely=0.35, relwidth=0.166, relheight=0.15)
           labels[4].place(relx=0.582, rely=0.4, relwidth=0.166, relheight=0.05)
           labels[5].place(relx=0.25, rely=0.55, relwidth=0.166, relheight=0.05)
           labels[6].place(relx=0.416, rely=0.495, relwidth=0.166, relheight=0.15)
           labels[7].place(relx=0.582, rely=0.55, relwidth=0.166, relheight=0.05)
           labels[8].place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)
           get_merch_total_income()

       # negotiate wage with sponsor
       def sponsor_negotiation():
           global sponsor_name, sponsor_revenue
           nonlocal labels

           def accept_wage():
               nonlocal wage
               global sponsor_income_label
               # checks if label has already been destroyed due to 3 renegotiations
               if labels[5].winfo_exists():
                   labels[5].destroy()
               labels[6].destroy()
               labels[7].place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.08)
               if renegotiations < 2:
                   response = sponsor_negotiation_responses["Good"][random.randint(0,4)]
                   labels[8].configure(fg="green", text=response)
               elif renegotiations == 2:
                   response = sponsor_negotiation_responses["Medium"][random.randint(0,4)]
                   labels[8].configure(fg="yellow1", text=response)
               else:
                   response = sponsor_negotiation_responses["Bad"][random.randint(0,4)]
                   labels[8].configure(fg="orange", text=response)

               labels[8].place(relx=0.25, rely=0.55, relwidth=0.5, relheight=0.15)
               add_profit(wage, sponsor_income_label, False)

           def renegotiate():
               nonlocal renegotiations
               nonlocal wage
               renegotiations += 1
               if random.randint(2, 1000) % 2 == 0:
                   # increases wage by random amount between 1.05 and 1.2 and rounds it to the nearest 10k
                   wage = special_round(wage * (random.randint(105, 120) / 100), 10000)
                   labels[4].config(text="€{:,} per year".format(wage))
               else:
                   # decreases wage by random amount between 0.75 and 0.9 and rounds it to the nearest 10k
                   wage = special_round(wage * (random.randint(75, 90) / 100), 10000)
                   labels[4].config(text="€{:,} per year".format(wage))

               sponsor_revenue.config(text=wage/1000000)

               # checks if less than 3 renegotiations have been attempted
               if renegotiations > 2:
                   labels[5].destroy()

           # decides sponsor's starting offer
           if CLUB_COUNTRY == "England":
               if league == eng_4:
                   sponsor_revenue.config(text=f"{random.randint(8, 15) / 100}")
               elif league == eng_3:
                   sponsor_revenue.config(text=f"{random.randint(29, 52) / 100}")
               elif league == eng_2:
                   sponsor_revenue.config(text=f"{random.randint(88, 175) / 100}")
               elif league == eng_1:
                   if int(club_rating.cget("text").split("/")[0]) == 20:
                       sponsor_revenue.config(text=f"{random.randint(5200, 7800) / 100}")
                   else:
                       sponsor_revenue.config(text=f"{random.randint(1100, 3200) / 100}")
           elif CLUB_COUNTRY == "France":
               if league == fra_2:
                   sponsor_revenue.config(text=f"{random.randint(6, 10) / 100}")
               elif league == fra_1:
                   if int(club_rating.cget("text").split("/")[0]) == 20:
                       sponsor_revenue.config(text=f"{random.randint(3600, 5300) / 100}")
                   else:
                       sponsor_revenue.config(text=f"{random.randint(900, 2000) / 100}")
           elif CLUB_COUNTRY == "Germany":
               if league == ger_2:
                   sponsor_revenue.config(text=f"{random.randint(11, 24) / 100}")
               elif league == ger_1:
                   if int(club_rating.cget("text").split("/")[0]) == 20:
                       sponsor_revenue.config(text=f"{random.randint(5000, 7200) / 100}")
                   else:
                       sponsor_revenue.config(text=f"{random.randint(1000, 2700) / 100}")
           elif CLUB_COUNTRY == "Italy":
               if league == ita_2:
                   sponsor_revenue.config(text=f"{random.randint(12, 26) / 100}")
               elif league == ita_1:
                   if int(club_rating.cget("text").split("/")[0]) == 20:
                       sponsor_revenue.config(text=f"{random.randint(4000, 6100) / 100}")
                   else:
                       sponsor_revenue.config(text=f"{random.randint(1000, 2300) / 100}")
           elif CLUB_COUNTRY == "Spain":
               if league == spa_2:
                   sponsor_revenue.config(text=f"{random.randint(11, 25) / 100}")
               elif league == spa_1:
                   if int(club_rating.cget("text").split("/")[0]) == 20:
                       sponsor_revenue.config(text=f"{random.randint(6200, 8000) / 100}")
                   else:
                       sponsor_revenue.config(text=f"{random.randint(900, 2100) / 100}")

           renegotiations = 0
           sponsor = sponsor_name.cget("text")
           wage = special_round(float(sponsor_revenue.cget("text")) * 1000000, 1)

           for i in labels:
               i.destroy()
           labels = [Label(menu_frames[7], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 18), bd=5, relief="raised", text="The club's sponsor has made an offer for the upcoming season.\nYou can accept their offer or try to renegotiate a higher price.\nHowever there is a risk they might lower their offer if they don't agree.\nYou can renegotiate 3 times in total."),
                         Label(menu_frames[7], bg=LIGHT_UI_COLOUR),
                         Label(menu_frames[7], bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 20, "bold"), text="Sponsor"),
                         Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 20), text=sponsor),
                         Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 20), text="€{:,} per year".format(wage)),
                         Button(menu_frames[7], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Renegotiate", command=renegotiate),
                         Button(menu_frames[7], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Accept", command=accept_wage),
                         Button(menu_frames[7], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Next", command=lambda: objective_overview(labels)),
                         Label(menu_frames[7], bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text="")
                         ]
           labels[0].place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.2)
           labels[1].place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.3)
           labels[2].place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.05)
           labels[3].place(relx=0.375, rely=0.42, relwidth=0.25, relheight=0.05)
           labels[4].place(relx=0.375, rely=0.5, relwidth=0.25, relheight=0.05)
           labels[5].place(relx=0.55, rely=0.6, relwidth=0.15, relheight=0.08)
           labels[6].place(relx=0.3, rely=0.6, relwidth=0.15, relheight=0.08)

       change_menu(7)
       hide_menu_buttons_grey()
       get_wage_costs()

       # changes text based on league
       division_text = ""
       div_4 = "Division Four Table"
       div_3 = "Division Three Table"
       div_2 = "Division Two Table"
       div_1 = "Division One Table"
       if CLUB_COUNTRY == "England":
           if league == eng_4:
               division_text = div_4
           elif league == eng_3:
               division_text = div_3
           elif league == eng_2:
               division_text = div_2
           elif league == eng_1:
               division_text = div_1
           league_name_label.config(text=f"England\n{division_text}")
       elif CLUB_COUNTRY == "France":
           if league == fra_2:
               division_text = div_2
           elif league == fra_1:
               division_text = div_1
           league_name_label.config(text=f"France\n{division_text}")
       elif CLUB_COUNTRY == "Germany":
           if league == ger_2:
               division_text = div_2
           elif league == ger_1:
               division_text = div_1
           league_name_label.config(text=f"Germany\n{division_text}")
       elif CLUB_COUNTRY == "Italy":
           if league == ita_2:
               division_text = div_2
           elif league == ita_1:
               division_text = div_1
           league_name_label.config(text=f"Italy\n{division_text}")
       elif CLUB_COUNTRY == "Spain":
           if league == spa_2:
               division_text = div_2
           elif league == spa_1:
               division_text = div_1
           league_name_label.config(text=f"Spain\n{division_text}")

       # does introduction message if it is first season, else skips it
       if year == 2024:
           labels = [Button(menu_frames[7], bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Next", command=sponsor_negotiation),
                     Label(menu_frames[7], bg="white", fg="black", font=("Ink Free", 25, "bold"), text=f"To {MANAGER_NAME},"),
                     Label(menu_frames[7], bg="white", fg="black", font=("Ink Free", 18), text=f"Welcome to your new club, {MANAGER_NAME}.\nThis is your assistant writing. Me and the board can't\nwait to welcome you to the club!\nAs manager of {CLUB_NAME}, you will lead\nyour players on a journey starting from the very bottom to the top divisons.\nEach decision you make will have an impact.\n\nBut first we need to go through a few things.")]
           labels[0].place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)
           labels[2].place(relx=0.18, rely=0.2, relwidth=0.64, relheight=0.35)
           labels[1].place(relx=0.18, rely=0.15, relwidth=0.64, relheight=0.05)
       else:
           sponsor_negotiation()

   scouts = [scout_one, scout_two, scout_three]

   # DEFAULT ACTIVE FRAME
   menu_frames[7].place(relx=0, rely=0, relwidth=1, relheight=1)
   season_start_menu()

   # MAKES MENU BUTTONS APPEAR ABOVE FRAME
   for button in menu_buttons:
       button.lift()

# CHANGES SUB MENU, ACTIVATED BY ANY SUB MENU BUTTON
def change_menu(menu):
   global menu_frames
   global menu_buttons
   for message in [release_bg, release_cancel_button, release_confirm_button, squad_size_message, squad_size_confirm, gk_num_message, gk_num_confirm]:
       if message and message.winfo_ismapped():
           message.place_forget()
   for frame in menu_frames:
       frame.place_forget()
   menu_frames[menu].place(relx=0, rely=0, relwidth=1, relheight=1)

# rounds n to the nearest multiple of rounder e.g. if rounder is 100 then to the nearest 100
def special_round(n, rounder):
    return round(n/rounder)*rounder

def round_to_three_sigfigs(number):
    if number == 0:
        return 0  # Handle special case for zero
    else:
        try:
            value = int('{:.3g}'.format(number))
        except ValueError:
            value = float('{:.3g}'.format(number))
        return value

# GENERATES SQUAD FOR TEAM
def gen_player(ovr, pos):
    for i in range(5):
        # CREATES PLAYER
        # SELECTS RANDOM REGION TO GET PLAYER NAME FROM
        num = random.randint(0, 100)

        if num <= 35:
            if CLUB_COUNTRY == "England":
                region = "1"
            elif CLUB_COUNTRY == "France":
                region = "2"
            elif CLUB_COUNTRY == "Germany":
                region = "4"
            elif CLUB_COUNTRY == "Italy":
                region = "7"
            elif CLUB_COUNTRY == "Spain":
                region = "6"
            else:
                region = "0"
        elif 35 < num <= 78:
            region = str(random.randint(0, 9))
        else:
            region = str(random.randint(0, 17))

        # GETS FIRST AND LAST NAME
        first_name = random.choice(first_names[region])
        last_name = random.choice(last_names[region])
        full_name = f"{first_name} {last_name}"

        # Check for duplicates in all squads
        is_duplicate = False
        all_players = squad + youth_players + scout_one_players + scout_two_players + scout_three_players
        for i in all_players:
            if f"{i.first_name} {i.last_name}" == full_name:
                is_duplicate = True
                break

        # If the name is not a duplicate, break out of the loop
        if not is_duplicate:
            break


    # returns player object
    return Player(first_name, last_name, ovr, pos, random.randint(16, 36), random.randint(1, 28),
                               random.randint(1, 12))

def gen_youth_player(ovr, pos):
    for i in range(5):
        # CREATES PLAYER
        # SELECTS RANDOM REGION TO GET PLAYER NAME FROM
        num = random.randint(0, 100)

        if num <= 35:
            if CLUB_COUNTRY == "England":
                region = "1"
            elif CLUB_COUNTRY == "France":
                region = "2"
            elif CLUB_COUNTRY == "Germany":
                region = "4"
            elif CLUB_COUNTRY == "Italy":
                region = "7"
            elif CLUB_COUNTRY == "Spain":
                region = "6"
            else:
                region == "0"
        elif 35 < num <= 78:
            region = str(random.randint(0, 9))
        else:
            region = str(random.randint(0, 17))

        # GETS FIRST AND LAST NAME
        first_name = random.choice(first_names[region])
        last_name = random.choice(last_names[region])
        full_name = f"{first_name} {last_name}"

        # Check for duplicates in all squads
        is_duplicate = False
        all_players = squad + youth_players + scout_one_players + scout_two_players + scout_three_players
        for i in all_players:
            if f"{i.first_name} {i.last_name}" == full_name:
                is_duplicate = True
                break

        # If the name is not a duplicate, break out of the loop
        if not is_duplicate:
            break

    player = Player(first_name, last_name, ovr, pos, random.randint(16, 19), random.randint(1, 28),
                               random.randint(1, 12))

    player.contract_expire = 0
    player.extension_offer = year + random.randint(3, 6)

    # returns player object
    return player

def gen_player_custom_age(ovr, pos, age):
    for i in range(5):
        # CREATES PLAYER
        # SELECTS RANDOM REGION TO GET PLAYER NAME FROM
        num = random.randint(0, 100)

        if num <= 35:
            if CLUB_COUNTRY == "England":
                region = "1"
            elif CLUB_COUNTRY == "France":
                region = "2"
            elif CLUB_COUNTRY == "Germany":
                region = "4"
            elif CLUB_COUNTRY == "Italy":
                region = "7"
            elif CLUB_COUNTRY == "Spain":
                region = "6"
            else:
                region = "0"
        elif 35 < num <= 78:
            region = str(random.randint(0, 9))
        else:
            region = str(random.randint(0, 17))

        # GETS FIRST AND LAST NAME
        first_name = random.choice(first_names[region])
        last_name = random.choice(last_names[region])
        full_name = f"{first_name} {last_name}"

        # Check for duplicates in all squads
        is_duplicate = False
        all_players = squad + youth_players + scout_one_players + scout_two_players + scout_three_players
        for i in all_players:
            if f"{i.first_name} {i.last_name}" == full_name:
                is_duplicate = True
                break

        # If the name is not a duplicate, break out of the loop
        if not is_duplicate:
            break

    # returns player object
    return Player(first_name, last_name, ovr, pos, age, random.randint(1, 28),
                               random.randint(1, 12))

squad = []
released_players = []

all_squad_labels = []


# LEAGUES AND CLUBS
# Name, Attack, Defense, play style, mentality, points, games played, first_colour, second_colour
# playstyle: 0 = possession, 1 = counter attack, 2 = physical, 3 = direct
# mentality: 0 = offensive, 1 = defensive, 2 = balanced
# 55 - 65
# 1, 2, 3, 4
eng_4 = [["Accrington United", 60, 60, 0, 0, 0, 0, RED, WHITE], ["Barrow Town", 55, 65, 3, 1, 0, 0, BLUE, WHITE], ["Bradford FC", 65, 55, 2, 1, 0, 0, YELLOW, ORANGE], ["Bromley", 59, 56, 1, 2, 0, 0, WHITE, BLACK], ["Carlisle Town", 61, 64, 1, 1, 0, 0, BLUE, RED], ["Cheltenham", 62, 63, 1, 1, 0, 0, RED, BLACK], ["Chesterfield", 57, 58, 3, 1, 0, 0, BLUE, WHITE], ["Colchester City", 60, 60, 1, 0, 0, 0, BLUE, WHITE],
        ["Crewe Town", 55, 65, 2, 1, 0, 0, RED, WHITE], ["Doncaster FC", 55, 60, 1, 1, 0, 0, RED, BLACK], ["Fleetwood Rovers", 59, 64, 1, 1, 0, 0, RED, WHITE],
        ["Gillingham", 60, 60, 1, 1, 0, 0, BLUE, WHITE], ["Grimsby", 55, 65, 3, 1, 0, 0, BLACK, WHITE], ["Harrogate", 60, 60, 1, 0, 0, 0, YELLOW, BLACK], ["Milton Keynes", 65, 55, 0, 1, 0, 0, WHITE, RED],
        ["Morecambe", 55, 65, 1, 1, 0, 0, RED, WHITE], ["Newport", 65, 65, 0, 0, 0, 0, ORANGE, BLACK], ["Nottingham Rovers", 60, 60, 2, 0, 0, 0, BLACK, WHITE], ["Port Town", 63, 62, 3, 0, 0, 0, BLACK, YELLOW],
        ["Salford", 60, 60, 1, 1, 0, 0, RED, WHITE], ["Swindon", 65, 55, 0, 0, 0, 0, RED, WHITE], ["Tranmere", 57, 65, 3, 1, 0, 0, WHITE, BLUE],
        ["Walsall", 55, 60, 2, 0, 0, 0, RED, WHITE], ["Wimbledon", 60, 65, 1, 1, 0, 0, BLUE, YELLOW]]

# 65 - 75
# 5, 6, 7, 8, 9
eng_3 = [["Barnsley City", 67, 73, 1, 1, 0, 0, RED, WHITE], ["Birmingham FC", 74, 75, 1, 0, 0, 0, BLUE, WHITE], ["Blackpool Rovers", 75, 66, 0, 2, 0, 0, ORANGE, WHITE], ["Bolton", 71, 69, 3, 0, 0, 0, WHITE, BLUE], ["Bristol Blues", 67, 71, 1, 1, 0, 0, BLUE, WHITE],
        ["Burton Town", 65, 75, 3, 0, 0, 0, YELLOW, BLACK], ["Cambridge", 67, 73, 0, 2, 0, 0, YELLOW, BLACK], ["Charlton United", 71, 69, 0, 2, 0, 0, RED, WHITE],
         ["Crawley FC", 67, 69, 0, 0, 0, 0, RED, WHITE], ["Exeter United", 71, 69, 0, 2, 0, 0, RED, BLACK], ["Huddersfield Rovers", 73, 74, 1, 0, 0, 0, BLUE, WHITE],
         ["Leyton Town", 65, 70, 1, 2, 0, 0, RED, WHITE], ["Lincoln", 67, 70, 1, 2, 0, 0, RED, WHITE], ["Mansfield", 66, 70, 2, 0, 0, 0, YELLOW, BLUE], ["Northampton United", 67, 67, 2, 0, 0, 0, ORANGE, WHITE],
         ["Peterborough FC", 67, 67, 3, 2, 0, 0, BLUE, WHITE], ["Reading", 72, 72, 2, 1, 0, 0, BLUE, WHITE], ["Rotherham FC", 71, 73, 2, 0, 0, 0, RED, WHITE],
         ["Shrewsbury United", 67, 67, 1, 2, 0, 0, BLUE, YELLOW], ["Stevenage Rovers", 67, 67, 3, 2, 0, 0, RED, WHITE], ["Stockport", 67, 67, 2, 1, 0, 0, BLUE, WHITE], ["Wigan United", 68, 69, 1, 2, 0, 0, BLUE, WHITE], ["Wrexham", 70, 69, 3, 0, 0, 0, RED, WHITE], ["Wycombe FC", 67, 67, 2, 0, 0, 0, SKY_BLUE, BLUE]]

# 75 - 81
# 10, 11, 12, 13, 14 ,15
eng_2 = [["Blackburn Town", 77, 77, 2, 0, 0, 0, BLUE, WHITE], ["Bristol Reds", 79, 79, 1, 0, 0, 0, RED, WHITE], ["Burnley United", 80, 80, 3, 1, 0, 0, BROWN, SKY_BLUE], ["Cardiff FC", 77, 76, 1, 1, 0, 0, BLUE, WHITE],
         ["Coventry", 80, 78, 0, 0, 0, 0, SKY_BLUE, WHITE], ["Derby", 77, 75, 3, 0, 0, 0, WHITE, BLACK], ["Hull United", 77, 78, 2, 0, 0, 0, ORANGE, BLACK],
         ["Leeds FC", 81, 79, 1, 0, 0, 0, WHITE, BLUE], ["Luton Rovers", 80, 77, 2, 1, 0, 0, ORANGE, WHITE], ["Middlesbrough", 79, 77, 2, 2, 0, 0, RED, WHITE], ["Millwall", 78, 78, 3, 0, 0, 0, BLUE, WHITE],
         ["Norwich FC", 77, 78, 0, 2, 0, 0, YELLOW, GREEN], ["Oxford Rovers", 76, 76, 0, 2, 0, 0, YELLOW, BLUE], ["Plymouth United", 76, 75, 1, 2, 0, 0, GREEN, ORANGE], ["Portsmouth", 75, 77, 1, 0, 0, 0, BLUE, WHITE], ["Preston Town", 78, 78, 3, 2, 0, 0, WHITE, BLUE], ["QPR", 77, 77, 2, 0, 0, 0, WHITE, BLUE],
         ["Sheffield Blues", 77, 76, 0, 2, 0, 0, BLUE, WHITE], ["Sheffield Reds", 80, 79, 1, 1, 0, 0, RED, BLACK], ["Stoke FC", 78, 78, 2, 0, 0, 0, RED, WHITE],
         ["Sunderland Rovers", 79, 79, 0, 2, 0, 0, RED, WHITE], ["Swansea United", 78, 79, 0, 2, 0, 0, WHITE, BLACK], ["Watford Town", 78, 77, 1, 0, 0, 0, YELLOW, BLACK], ["West Bromwich FC", 77, 77, 2, 0, 0, 0, WHITE, BLUE]]

# 82 - 92
# 16, 17, 18, 19, 20
eng_1 = [["Armoury FC", 91, 88, 1, 0, 0, 0, RED, WHITE], ["Aston United", 88, 87, 0, 2, 0, 0, BROWN, SKY_BLUE], ["Bournemouth Town", 86, 85, 3, 2, 0, 0, RED, BLACK], ["Brentford Town", 84, 83, 1, 0, 0, 0, RED, BLACK],
         ["Brighton and Hove", 85, 84, 1, 2, 0, 0, BLUE, WHITE], ["Chelsea Rovers", 87, 86, 0, 2, 0, 0, BLUE, WHITE], ["Crystal Palace", 87, 84, 2, 2, 0, 0, BLUE, RED],
         ["Everton United", 85, 87, 1, 1, 0, 0, BLUE, WHITE], ["Fulham", 84, 85, 2, 2, 0, 0, BLACK, WHITE], ["Ipswich", 82, 82, 0, 2, 0, 0, BLUE, WHITE], ["Leicester United", 84, 82, 0, 0, 0, 0, BLUE, WHITE], ["Liverpool", 91, 87, 2, 0, 0, 0, RED, ORANGE],
         ["Manchester Blues", 92, 88, 0, 0, 0, 0, SKY_BLUE, WHITE], ["Manchester Reds", 89, 86, 0, 0, 0, 0, RED, BLACK], ["Newcastle Town", 86, 85, 1, 0, 0, 0, BLACK, WHITE], ["Nottingham FC", 83, 84, 2, 1, 0, 0, RED, WHITE],
        ["Southampton Town", 82, 83, 2, 0, 0, 0, RED, WHITE], ["Tottenham Rovers", 88, 86, 1, 2, 0, 0, WHITE, BLUE], ["West Ham Town", 87, 87, 2, 0, 0, 0, BROWN, SKY_BLUE], ["Wolverhampton Rovers", 85, 85, 3, 2, 0, 0, ORANGE, BLACK]]

# 72 - 78
# 7, 8, 9, 10, 11, 12
# Avg squad ratings: 72, 69, 71, 70, 72, 73
fra_2 = [["Ajaccio", 74, 75, 3, 2, 0, 0, WHITE, RED], ["Amiens", 74, 77, 3, 1, 0, 0, WHITE, BLACK], ["Annecy", 75, 73, 1, 0, 0, 0, RED, BROWN],
         ["Bastia", 74, 74, 3, 2, 0, 0, BLUE, WHITE], ["Caen", 76, 74, 3, 0, 0, 0, BLUE, RED], ["Clermont", 76, 76, 2, 2, 0, 0, RED, BLUE],
         ["Dunkerque", 74, 73, 2, 2, 0, 0, BLUE, WHITE], ["Grenoble", 75, 75, 3, 2, 0, 0, BLUE, WHITE], ["Guingamp", 76, 76, 3, 2, 0, 0, RED, BLACK], ["Laval", 75, 76, 3, 2, 0, 0, ORANGE, BLACK], ["Lorient", 78, 75, 3, 0, 0, 0, ORANGE, BLACK], ["Martigues", 74, 73, 3, 2, 0, 0, YELLOW, RED], ["Metz", 76, 77, 3, 2, 0, 0, BROWN, WHITE],
         ["Paris BL", 75, 76, 0, 2, 0, 0, BLUE, SKY_BLUE], ["Paris Etoiles Vertes", 75, 73, 1, 0, 0, 0, LIME, WHITE], ["Pau", 76, 74, 3, 0, 0, 0, YELLOW, BLUE], ["Rodez", 78, 73, 3, 0, 0, 0, RED, YELLOW],
         ["Troyes", 75, 74, 1, 2, 0, 0, BLUE, WHITE]]

# 78 - 90
# 13, 14, 15, 16, 17, 18, 19, 20
fra_1 = [["Angers", 81, 79, 0, 0, 0, 0, WHITE, BLACK], ["Auxerre", 82, 79, 2, 2, 0, 0, WHITE, BLUE], ["Brest", 84, 86, 0, 1, 0, 0, RED, WHITE], ["Le Havre", 82, 83, 3, 2, 0, 0, SKY_BLUE, BLUE], ["Lens", 84, 84, 0, 2, 0, 0, YELLOW, ORANGE], ["Lille", 84, 85, 2, 2, 0, 0, RED, BLUE],
        ["Lyon", 83, 81, 0, 0, 0, 0, WHITE, BLUE], ["Marseille", 85, 84, 2, 2, 0, 0, WHITE, SKY_BLUE], ["Monaco", 86, 82, 2, 0, 0, 0, RED, WHITE],
         ["Montpellier", 83, 81, 3, 0, 0, 0, ORANGE, BLUE], ["Nantes", 81, 80, 0, 2, 0, 0, YELLOW, GREEN], ["Nice", 82, 86, 2, 1, 0, 0, RED, BLACK], ["Paris BR", 89, 85, 0, 0, 0, 0, BLUE, RED],
         ["Reims", 84, 82, 2, 0, 0, 0, RED, WHITE], ["Rennes", 85, 83, 1, 0, 0, 0, RED, BLACK], ["Saint-Étienne", 78, 81, 2, 1, 0, 0, GREEN, WHITE], ["Strasbourg", 82, 81, 1, 2, 0, 0, BLUE, WHITE], ["Toulouse", 82, 82, 0, 2, 0, 0, PURPLE, WHITE]]

# 70 - 76
# 7, 8, 9, 10, 11, 12, 13
ger_2 = [["Berlin BW", 75, 72, 0, 0, 0, 0, BLUE, WHITE], ["Braunschweig", 70, 73, 3, 1, 0, 0, YELLOW, BLUE], ["Darmstadt", 76, 74, 2, 2, 0, 0, BLUE, WHITE], ["Duesseldorf", 76, 74, 2, 0, 0, 0, RED, WHITE], ["Elversberg", 72, 72, 2, 2, 0, 0, WHITE, BLACK],
         ["Fuerth", 72, 73, 2, 2, 0, 0, WHITE, LIME], ["Gelsenkirchen", 73, 70, 2, 0, 0, 0, BLUE, WHITE], ["Hamburg BL", 75, 73, 0, 0, 0, 0, BLUE, WHITE],
         ["Hannover", 74, 74, 1, 2, 0, 0, GREEN, BLACK], ["Kaiserslautern", 73, 70, 3, 0, 0, 0, RED, WHITE], ["Karlsruhe", 76, 72, 1, 0, 0, 0, BLUE, WHITE], ["Koeln", 75, 74, 3, 1, 0, 0, WHITE, RED],
         ["Magdeburg", 72, 72, 2, 2, 0, 0, WHITE, BLUE], ["Muenster", 73, 72, 0, 2, 0, 0, WHITE, RED], ["Nuernberg", 72, 71, 3, 2, 0, 0, RED, BLACK], ["Paderborn", 72, 72, 1, 2, 0, 0, BLACK, WHITE], ["Regensburg", 72, 71, 2, 2, 0, 0, WHITE, RED], ["Ulm", 71, 72, 1, 2, 0, 0, WHITE, BLACK]]

# 81 - 92
ger_1 = [["Augsburg", 84, 84, 3, 2, 0, 0, RED, GREEN], ["Berlin R", 81, 84, 3, 1, 0, 0, RED, WHITE], ["Bochum", 82, 82, 3, 2, 0, 0, BLUE, WHITE], ["Bremen", 83, 84, 2, 2, 0, 0, GREEN, WHITE],
         ["Dortmund", 88, 86, 2, 2, 0, 0, YELLOW, BLACK], ["Frankfurt", 85, 85, 0, 2, 0, 0, WHITE, RED], ["Freiburg", 83, 83, 0, 2, 0, 0, BLACK, WHITE],
         ["Gladbach", 85, 83, 1, 0, 0, 0, WHITE, BLACK], ["Hamburg R", 81, 82, 0, 1, 0, 0, BROWN, WHITE], ["Heidenheim", 83, 83, 3, 2, 0, 0, RED, BLUE], ["Hoffenheim", 85, 83, 2, 0, 0, 0, BLUE, WHITE], ["Kiel", 82, 82, 1, 2, 0, 0, BLUE, RED],
         ["Leipzig", 88, 86, 2, 2, 0, 0, WHITE, RED], ["Leverkusen", 89, 88, 0, 2, 0, 0, BLACK, RED], ["Mainz", 81, 83, 3, 1, 0, 0, WHITE, RED], ["Muenchen", 91, 86, 2, 0, 0, 0, RED, WHITE],
         ["Stuttgart", 86, 86, 2, 2, 0, 0, WHITE, RED], ["Wolfsburg", 84, 83, 0, 2, 0, 0, LIME, WHITE]]

# 73 - 78
ita_2 = [["Bari", 73, 75, 3, 1, 0, 0, WHITE, RED], ["Bolzano", 75, 75, 3, 2, 0, 0, WHITE, RED], ["Brescia", 74, 77, 0, 1, 0, 0, BLUE, WHITE], ["Carrara", 73, 72, 1, 1, 0, 0, BLUE, YELLOW], ["Catanzaro", 77, 75, 1, 0, 0, 0, RED, YELLOW], ["Cesena", 73, 73, 2, 0, 0, 0, WHITE, BLACK],
         ["Cittadella", 74, 75, 3, 2, 0, 0, BROWN, SKY_BLUE], ["Cosenza", 73, 76, 3, 1, 0, 0, BLUE, RED], ["Cremona", 76, 78, 3, 1, 0, 0, RED, GREY], ["Frosinone", 77, 76, 1, 0, 0, 0, YELLOW, BLUE], ["Genoa BL", 76, 74, 1, 0, 0, 0, BLUE, WHITE],
         ["La Spezia", 73, 75, 1, 1, 0, 0, WHITE, BLACK], ["Mantova", 73, 75, 1, 2, 0, 0, WHITE, RED], ["Modena", 74, 75, 0, 2, 0, 0, YELLOW, BLUE], ["Napoli YB", 73, 74, 0, 2, 0, 0, BLUE, YELLOW], ["Palermo", 77, 75, 0, 0, 0, 0, RED, BLACK],
         ["Pisa", 75, 75, 1, 2, 0, 0, BLUE, BLACK], ["Reggio Emilia", 73, 76, 0, 1, 0, 0, BROWN, WHITE], ["Salerno", 76, 76, 1, 2, 0, 0, BROWN, WHITE], ["Sassuolo", 78, 75, 2, 0, 0, 0, GREEN, BLACK]]

# 81 - 88
ita_1 = [["Bergamo", 86, 85, 2, 2, 0, 0, BLUE, BLACK], ["Bologna", 87, 85, 0, 2, 0, 0, RED, BLUE], ["Cagliari", 82, 82, 3, 2, 0, 0, RED, BLUE], ["Como", 81, 82, 0, 2, 0, 0, SKY_BLUE, BLUE], ["Empoli", 81, 83, 0, 1, 0, 0, BLUE, WHITE], ["Firenze", 85, 86, 1, 2, 0, 0, PURPLE, WHITE],
         ["Genoa BR", 83, 84, 2, 2, 0, 0, BLUE, RED], ["Lecce", 81, 83, 1, 1, 0, 0, RED, YELLOW], ["Milano BB", 87, 87, 1, 2, 0, 0, BLUE, BLACK], ["Milano R", 85, 87, 1, 2, 0, 0, RED, BLACK],
         ["Monza", 83, 84, 0, 2, 0, 0, RED, WHITE], ["Napoli", 86, 85, 1, 2, 0, 0, SKY_BLUE, WHITE], ["Parma", 83, 81, 3, 2, 0, 0, YELLOW, BLACK], ["Roma BW", 84, 85, 2, 2, 0, 0, SKY_BLUE, WHITE], ["Roma R", 86, 85, 0, 2, 0, 0, RED, ORANGE],
         ["Torina R", 82, 86, 2, 1, 0, 0, BROWN, WHITE], ["Torino BW", 85, 86, 3, 2, 0, 0, WHITE, BLACK], ["Udine", 82, 83, 3, 2, 0, 0, WHITE, BLACK], ["Venezia", 82, 82, 2, 0, 0, 0, BLACK, BROWN], ["Verona", 81, 84, 3, 1, 0, 0, BLUE, YELLOW]]

# 73 - 78
spa_2 = [["Albacete", 75, 73, 1, 0, 0, 0, WHITE, YELLOW], ["Almeria", 77, 76, 0, 2, 0, 0, WHITE, RED],
         ["Burgos", 75, 74, 3, 2, 0, 0, WHITE, BLACK], ["Cadiz", 77, 78, 3, 1, 0, 0, YELLOW, BLUE], ["Cartagena", 74, 74, 2, 2, 0, 0, WHITE, BLACK], ["Castellon", 73, 74, 0, 2, 0, 0, WHITE, BLACK], ["Cordoba", 73, 73, 2, 1, 0, 0, WHITE, GREEN], ["Coruna", 74, 74, 3, 2, 0, 0, WHITE, BLUE], ["Eibar", 78, 76, 0, 0, 0, 0, BLUE, RED], ["Elche", 74, 77, 3, 1, 0, 0, WHITE, GREEN], ["Elda", 75, 73, 3, 0, 0, 0, RED, BLUE],
         ["Ferrol", 75, 76, 1, 2, 0, 0, GREEN, WHITE], ["Gijon", 75, 76, 1, 2, 0, 0, RED, WHITE], ["Granada", 76, 76, 1, 2, 0, 0, RED, WHITE], ["Huesca", 73, 78, 1, 1, 0, 0, BLUE, RED], ["Malaga", 74, 75, 1, 0, 0, 0, BLUE, WHITE],
         ["Miranda", 75, 73, 2, 0, 0, 0, RED, BLACK], ["Oviedo", 77, 77, 0, 2, 0, 0, BLUE, WHITE], ["Santander", 78, 73, 1, 0, 0, 0, GREEN, WHITE], ["Tenerife", 74, 76, 2, 1, 0, 0, WHITE, BLUE], ["Valencia BR", 75, 76, 2, 2, 0, 0, BLUE, RED],
         ["Zaragoza", 74, 77, 0, 1, 0, 0, WHITE, BLUE]]

# 81 - 92
spa_1 = [["Alava", 81, 85, 3, 1, 0, 0, BLUE, WHITE], ["Barcelona BR", 91, 85, 0, 0, 0, 0, BLUE, RED], ["Barcelona BW", 83, 81, 1, 2, 0, 0, BLUE, WHITE], ["Bilbao", 87, 87, 2, 2, 0, 0, RED, WHITE],
         ["Getafe", 83, 84, 1, 2, 0, 0, BLUE, WHITE], ["Girona", 87, 85, 0, 0, 0, 0, RED, WHITE], ["Las Palmas", 84, 86, 0, 1, 0, 0, YELLOW, BLUE], ["Leganes", 82, 82, 3, 1, 0, 0, WHITE, BLUE], ["Madrid Blancos", 92, 89, 2, 0, 0, 0, WHITE, YELLOW],
         ["Madrid Rojos", 89, 85, 2, 0, 0, 0, RED, WHITE], ["Mallorca", 81, 85, 3, 1, 0, 0, RED, BLACK], ["Pamplona", 83, 84, 1, 2, 0, 0, RED, BLUE], ["San Sebastian", 85, 86, 0, 2, 0, 0, SKY_BLUE, WHITE], ["Sevilla GW", 87, 86, 0, 2, 0, 0, GREEN, WHITE],
         ["Sevilla WR", 84, 85, 0, 2, 0, 0, WHITE, RED], ["Valencia WB", 85, 85, 3, 1, 0, 0, WHITE, BLACK], ["Valladolid", 82, 82, 1, 1, 0, 0, WHITE, PURPLE], ["Vallecas", 84, 85, 2, 1, 0, 0, WHITE, RED], ["Vigo", 82, 84, 2, 1, 0, 0, SKY_BLUE, RED], ["Villarreal", 86, 82, 1, 0, 0, 0, YELLOW, BLUE]]

nat_cup_dates = [["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "Cup Round of 32", 12, 9], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "Cup Round of 16", 24, 11], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "Cup Quarter Final", 5, 2], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "Cup Semi Final", 9, 3], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "Cup Final", 18, 4]]

int_cup_dates = [["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup League Phase", 21, 9], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup League Phase", 2, 10], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup League Phase", 23, 10], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup League Phase", 4, 11],
                 ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup League Phase", 28, 11], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup League Phase", 10, 12], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup League Phase", 22, 1], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup League Phase", 28, 1],
                 ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup Round of 16 Leg 1", 5, 3], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup Round of 16 Leg 2", 13, 3], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup Quarter Final Leg 1", 6, 4], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup Quarter Final Leg 2", 14, 4],
                 ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "European Cup Semi Final Leg 1", 28, 4], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup Semi Final Leg 2", 8, 5], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "European Cup Final", 5, 6]]

playoff_dates = [["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "A", "Playoffs Semi Final Leg 1", 16, 5], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "Playoffs Semi Final Leg 2", 21, 5], ["N/A", 9, 9, 9, 9, 9, 9, WHITE, WHITE, "H", "Playoffs Final", 27, 5]]

eng_4_2_dates = [[5, 8], [11, 8], [16, 8], [20, 8], [25, 8], [2, 9], [7, 9], [16, 9],
                 [21, 9], [26, 9], [3, 10], [7, 10], [13, 10], [18, 10], [25, 10], [1, 11],
                 [8, 11], [14, 11], [20, 11], [2, 12], [8, 12], [13, 12], [17, 12], [2, 1],
                 [7, 1], [13, 1], [19, 1], [24, 1], [1, 2], [11, 2], [16, 2], [21, 2],
                 [27, 2], [3, 3], [13, 3], [17, 3], [22, 3], [27, 3], [1, 4], [5, 4],
                 [9, 4], [13, 4], [23, 4], [27, 4], [1, 5], [6, 5]]

thirty_eight_league_dates = [[7, 8], [11, 8], [17, 8], [23, 8], [28, 8], [2, 9], [7, 9], [16, 9], [27, 9], [7, 10], [12, 10], [18, 10], [28, 10],
                             [10, 11], [15, 11], [20, 11], [3, 12], [17, 12], [1, 1], [7, 1], [13, 1], [17, 1], [12, 2], [18, 2], [23, 2], [28, 2],
                             [17, 3], [22, 3], [27, 3], [1, 4], [10, 4], [23, 4], [3, 5], [12, 5], [16, 5], [21, 5], [25, 5], [29, 5]]

thirty_eight_league_dates_playoffs = [[7, 8], [12, 8], [19, 8], [26, 8], [1, 9], [7, 9], [20, 9], [28, 9], [3, 10], [9, 10], [16, 10], [23, 10], [29, 10],
                             [4, 11], [11, 11], [16, 11], [28, 11], [6, 12], [13, 12], [20, 12], [1, 1], [8, 1], [14, 1], [20, 1], [25, 1], [1, 2],
                             [12, 2], [19, 2], [26, 2], [2, 3], [15, 3], [21, 3], [27, 3], [4, 4], [11, 4], [24, 4], [29, 4], [5, 5]]

thirty_four_league_dates = [[8, 8], [14, 8], [19, 8], [25, 8], [1, 9], [7, 9], [16, 9], [27, 9], [7, 10], [13, 10], [18, 10],
                            [28, 10], [10, 11], [15, 11], [19, 11], [3, 12], [15, 12], [19, 12], [1, 1], [8, 1], [13, 1], [18, 1],
                            [12, 2], [17, 2], [23, 2], [28, 2], [20, 3], [27, 3], [1, 4], [10, 4], [23, 4], [3, 5], [15, 5], [22, 5]]

thirty_four_league_dates_playoffs = [[8, 8], [15, 8], [21, 8], [28, 8], [5, 9], [7, 9], [19, 9], [26, 9], [2, 10], [9, 10], [16, 10],
                            [22, 10], [29, 10], [4, 11], [11, 11], [18, 11], [15, 11], [1, 12], [8, 12], [15, 12], [1, 1], [8, 1],
                            [15, 1], [21, 1], [28, 1], [12, 2], [18, 2], [25, 2], [2, 3], [18, 3], [27, 3], [4, 4], [11, 4], [26, 4]]

fourty_two_league_dates = [[5, 8], [11, 8], [16, 8], [22, 8], [28, 8], [2, 9], [7, 9], [18, 9], [23, 9], [28, 9], [3, 10], [9, 10], [14, 10], [20, 10], [27, 10],
                           [2, 11], [7, 11], [12, 11], [18, 11], [1, 12], [7, 12], [14, 12], [2, 1], [8, 1], [14, 1], [21, 1], [26, 1], [1, 2], [11, 2], [17, 2],
                           [22, 2], [28, 2], [4, 3], [15, 3], [21, 3], [28, 3], [4, 4], [11, 4], [25, 4], [1, 5], [7, 5], [13, 5]]

fourty_two_league_dates_playoffs = [[5, 8], [11, 8], [16, 8], [22, 8], [28, 8], [2, 9], [7, 9], [18, 9], [23, 9], [28, 9], [3, 10], [9, 10], [14, 10], [20, 10], [27, 10],
                           [2, 11], [7, 11], [12, 11], [18, 11], [1, 12], [7, 12], [14, 12], [2, 1], [8, 1], [14, 1], [21, 1], [26, 1], [1, 2], [11, 2], [17, 2],
                           [22, 2], [28, 2], [4, 3], [15, 3], [21, 3], [28, 3], [4, 4], [11, 4], [23, 4], [28, 4], [4, 5], [9, 5]]

# Calculate the average of the second and third elements for each team in each division
eng_4_avg = [[team[0], (team[1] + team[2]) / 2] for team in eng_4]
eng_3_avg = [[team[0], (team[1] + team[2]) / 2] for team in eng_3]
eng_2_avg = [[team[0], (team[1] + team[2]) / 2] for team in eng_2]
eng_1_avg = [[team[0], (team[1] + team[2]) / 2] for team in eng_1]
fra_2_avg = [[team[0], (team[1] + team[2]) / 2] for team in fra_2]
fra_1_avg = [[team[0], (team[1] + team[2]) / 2] for team in fra_1]
ger_2_avg = [[team[0], (team[1] + team[2]) / 2] for team in ger_2]
ger_1_avg = [[team[0], (team[1] + team[2]) / 2] for team in ger_1]
ita_2_avg = [[team[0], (team[1] + team[2]) / 2] for team in ita_2]
ita_1_avg = [[team[0], (team[1] + team[2]) / 2] for team in ita_1]
spa_2_avg = [[team[0], (team[1] + team[2]) / 2] for team in spa_2]
spa_1_avg = [[team[0], (team[1] + team[2]) / 2] for team in spa_1]

# Combine all the teams and their averages into one list
all_teams_avg = eng_4_avg + eng_3_avg + eng_2_avg + eng_1_avg + fra_2_avg + ger_2_avg + ger_1_avg + ita_2_avg + ita_1_avg + spa_1_avg + spa_2_avg

# Sort the combined list based on the calculated averages in descending order
sorted_teams = sorted(all_teams_avg, key=lambda x: x[1], reverse=True)

# Print the sorted list
for team in sorted_teams:
    print(team)

def get_league_ovr(league_name):
    total_ovr = 0
    teams = 0
    for i in league_name:
        team_ovr = int((i[1] + i[2]) / 2)
        total_ovr += team_ovr
        teams += 1
    return (total_ovr/teams)

print(f"Prem: {get_league_ovr(eng_1)}")
print(f"Ligue 1: {get_league_ovr(fra_1)}")
print(f"Bundesliga: {get_league_ovr(ger_1)}")
print(f"Serie A: {get_league_ovr(ita_1)}")
print(f"La Liga: {get_league_ovr(spa_1)}")
print(f"Championship: {get_league_ovr(eng_2)}")
print(f"Ligue 2: {get_league_ovr(fra_2)}")
print(f"Zwei Liga: {get_league_ovr(ger_2)}")
print(f"Serie B: {get_league_ovr(ita_2)}")
print(f"La Liga 2: {get_league_ovr(spa_2)}")
print(f"League One: {get_league_ovr(eng_3)}")
print(f"League Two: {get_league_ovr(eng_4)}")

# Name, Attack, Defense, play style, mentality, points, games played
# playstyle: 0 = possession, 1 = counter attack, 2 = physical, 3 = direct
# mentality: 0 = offensive, 1 = defensive, 2 = balanced

first_names = {
    '0': ['James', 'William', 'Liam', 'Benjamin', 'Alexander', 'Henry', 'Elijah', 'Daniel', 'Samuel', 'Matthew', 'Harrison', 'Owen',
          'Finn', 'Archer', 'Silas', 'Emmett', 'Ryder', 'Winston', 'Caspian', 'Dashiell', 'Atticus', 'Soren', 'Cormac', 'Lachlan',
          'Magnus'],
    '1': ['Oliver', 'George', 'Harry', 'Jack', 'William', 'Henry', 'Thomas', 'Arthur', 'Edward', 'Freddie', 'Alfie', 'Oscar', 'Max',
          'Rory', 'Louis', 'Ezra', 'Felix', 'Hugo', 'Jasper', 'Theo', 'Caspian', 'Sebastian', 'Rupert', 'Kit', 'Percival'],
    '2': ['Liam', 'Noah', 'Ethan', 'Lucas', 'Logan', 'Benjamin', 'Henry', 'Caleb', 'Levi', 'Nathan', 'Connor', 'Oscar', 'Felix', 'Tristan',
          'Hudson', 'Dominic', 'Xavier', 'Gideon', 'Maximus', 'Malachi', 'Augustus', 'Phineas', 'Caspian', 'Dorian', 'Ezekiel'],
    '3': ['William', 'Jack', 'Oliver', 'Noah', 'James', 'Ethan', 'Mason', 'Lachlan', 'Cooper', 'Xavier', 'Harrison', 'Levi', 'Zachary',
          'Finn', 'Archer', 'Jasper', 'Oscar', 'Hamish', 'Angus', 'Flynn', 'Atticus', 'Fletcher', 'Huxley', 'Rafferty', 'Sullivan'],
    '4': ['Maximilian', 'Benjamin', 'Paul', 'Leon', 'Felix', 'Jonas', 'Anton', 'Matthias', 'Emil', 'Lukas', 'Nico', 'Julian', 'David',
          'Simon', 'Elias', 'Moritz', 'Vincent', 'Jakob', 'Fabian', 'Lennard', 'Finnian', 'Matthis', 'Kilian', 'Niklas', 'Leonidas'],
    '5': ['Gabriel', 'Louis', 'Raphael', 'Antoine', 'Julien', 'Lucas', 'Hugo', 'Théo', 'Alexandre', 'Maxime', 'Noah', 'Jules', 'Gaspard',
          'Étienne', 'Matthieu', 'Timothée', 'Baptiste', 'Tristan', 'Adrien', 'Benoît', 'Célestin', 'Olivier', 'Sébastien', 'Valentin',
          'Victorien'],
    '6': ['Hugo', 'Pablo', 'Daniel', 'Álvaro', 'Alejandro', 'Adrián', 'Diego', 'Carlos', 'Javier', 'Mario', 'Sergio', 'Iván', 'Gonzalo',
          'Manuel', 'Martín', 'Luis', 'David', 'Rubén', 'Jorge', 'José', 'Bruno', 'Enrique', 'Fernando', 'Nicolás', 'Ricardo'],
    '7': ['Lorenzo', 'Leonardo', 'Gabriele', 'Francesco', 'Matteo', 'Alessandro', 'Davide', 'Riccardo', 'Andrea', 'Tommaso', 'Giovanni',
          'Nicola', 'Antonio', 'Simone', 'Federico', 'Luca', 'Marco', 'Gianluca', 'Mattia', 'Daniele', 'Ettore', 'Raffaele', 'Stefano',
          'Teodoro', 'Valerio'],
    '8': ['Miguel', 'Arthur', 'Davi', 'Pedro', 'Gabriel', 'Bernardo', 'Lucas', 'Matheus', 'Rafael', 'Heitor', 'Enzo', 'Felipe', 'Guilherme',
          'Gustavo', 'Samuel', 'Vitor', 'Nicolas', 'Daniel', 'João', 'Henrique', 'Isaac', 'Cauã', 'Otávio', 'Bento', 'Sebastião'],
    '9': ['Santiago', 'Mateo', 'Sebastián', 'Emiliano', 'Diego', 'Javier', 'Daniel', 'Pedro', 'Carlos', 'Alejandro', 'José', 'Andrés',
          'Miguel', 'Fernando', 'Jorge', 'Adrián', 'Ricardo', 'Eduardo', 'Xavier', 'Mario', 'Máximo', 'Gael', 'Joaquín', 'Leonardo',
          'Ezequiel'],
    '10': ['Aarav', 'Arjun', 'Aryan', 'Vihaan', 'Reyansh', 'Advait', 'Mohammed', 'Kabir', 'Vivaan', 'Aryan', 'Ishaan', 'Rudra', 'Shaurya',
           'Aryan', 'Dhruv', 'Vihaan', 'Atharva', 'Darsh', 'Dev', 'Ayaan', 'Kian', 'Rohan', 'Karan', 'Kavya', 'Aditya'],
    '11': ['Liang', 'Chen', 'Wei', 'Hao', 'Yifan', 'Kai', 'Jing', 'Jia', 'Ming', 'Xin', 'Xiang', 'Chang', 'Zhi', 'Lei', 'Yi', 'Tian', 'Guo',
           'Jun', 'Yang', 'Han', 'Huan', 'Sheng', 'Yuan', 'Bo', 'Qiang'],
    '12': ['Hugo', 'Pablo', 'Daniel', 'Álvaro', 'Alejandro', 'Adrián', 'Diego', 'Carlos', 'Javier', 'Mario', 'Sergio', 'Iván', 'Gonzalo',
           'Manuel', 'Martín', 'Luis', 'David', 'Rubén', 'Jorge', 'José', 'Bruno', 'Enrique', 'Fernando', 'Nicolás', 'Ricardo'],
    '13': ['Minho', 'Jihoon', 'Yoon', 'Hansol', 'Seojin', 'Hyun', 'Jun', 'Jaemin', 'Minseok', 'Hyeon', 'Seojun', 'Seojin', 'Hak', 'Gyu',
           'Jiho', 'Woosung', 'Kyu', 'Jinwoo', 'Sang', 'Min', 'Siwon', 'Donghyun', 'Jaejin', 'Seungyeon', 'Seungho'],
    '14': ['Ivan', 'Alexander', 'Maxim', 'Artyom', 'Dmitry', 'Vladimir', 'Andrey', 'Nikolay', 'Yaroslav', 'Denis', 'Konstantin', 'Sergey',
           'Mikhail', 'Anton', 'Pavel', 'Roman', 'Egor', 'Timofey', 'Bogdan', 'Igor', 'Fyodor', 'Leonid', 'Anatoly', 'Nikita', 'Boris'],
    '15': ['Ade', 'Chinedu', 'Emeka', 'Obi', 'Kingsley', 'Chukwu', 'Olu', 'Ola', 'Nosa', 'Osagie', 'Oluwatobi', 'Adebayo', 'Olumide',
           'Olalekan', 'Eze', 'Azubuike', 'Uche', 'Chidi', 'Ndubisi', 'Oluwaseun', 'Oluwaseyi', 'Oluwafemi', 'Oluwaseyi', 'Oluwafemi',
           'Oluwatoyin', 'Olawale'],
    '16': ['Luthando', 'Sipho', 'Kagiso', 'Thabo', 'Tshepo', 'Mandla', 'Sizwe', 'Bongani', 'Themba', 'Musa', 'Siphiwe', 'Phumlani',
           'Zweli', 'Nhlanhla', 'Sello', 'Thulani', 'Khaya', 'Mthokozisi', 'Muzi', 'Sibusiso', 'Bhekizizwe', 'Luzuko', 'Thamsanqa',
           'Mncedisi', 'Nkosinathi'],
    '17': ['Mwangi', 'Odhiambo', 'Ochieng', 'Waweru', 'Maina', 'Gichuhi', 'Njoroge', 'Kariuki', 'Njau', 'Kamau', 'Macharia', 'Njeri',
           'Wairimu', 'Akinyi', 'Muthoni', 'Wanjiku', 'Wambui', 'Nkatha', 'Wambua', 'Nyambura', 'Oduor', 'Onyango', 'Nyaga', 'Odongo', 'Ogutu']
}
last_names = {
    "0": ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson', 'Martinez', 'Anderson', 'Taylor',
          'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez', 'Harris', 'Clark'],
    "1": ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Robinson', 'Wright', 'Thompson', 'Evans', 'Walker',
          'White', 'Roberts', 'Green', 'Hall', 'Wood', 'Jackson', 'Clarke', 'Hill', 'Cooper', 'Lewis', 'Turner', 'Adams'],
    "2": ['Smith', 'Johnson', 'Brown', 'Tremblay', 'Martin', 'Roy', 'Wilson', 'Lee', 'Gagnon', 'Taylor', 'Campbell', 'Anderson', 'Clark', 'Morin',
          'Leblanc', 'Young', 'King', 'Côté', 'Wright', 'Gauthier', 'Lavoie', 'Bouchard', 'Scott', 'Williams', 'Bell'],
    "3": ['Smith', 'Jones', 'Brown', 'Taylor', 'Wilson', 'Johnson', 'Williams', 'White', 'Thomas', 'Anderson', 'Thompson', 'Walker', 'Harris',
          'Clark', 'Lewis', 'Martin', 'Davis', 'Lee', 'Moore', 'Robinson', 'Hall', 'Young', 'Turner', 'King', 'Wright'],
    "4": ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Schäfer', 'Koch', 'Bauer',
          'Richter', 'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz', 'Zimmermann', 'Braun', 'Krüger', 'Hofmann', 'Hartmann', 'Lange'],
    "5": ['Martin', 'Bernard', 'Thomas', 'Dubois', 'Durand', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'Roux', 'David',
          'Bertrand', 'Morel', 'Fournier', 'Leroy', 'Girard', 'Bonnet', 'Dupont', 'Lambert', 'Fontaine', 'Rousseau', 'Vincent', 'Muller'],
    "6": ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Hernández',
          'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro', 'Torres', 'Domínguez', 'Vargas', 'Ramos', 'Castro'],
    "7": ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco', 'Bruno', 'Gallo', 'Conti',
          'De Luca', 'Mancini', 'Costa', 'Giordano', 'Rizzo', 'Lombardi', 'Moretti', 'Barbieri', 'Fontana', 'Santoro', 'Mariani', 'Rinaldi'],
    "8": ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Almeida', 'Lima', 'Ferreira', 'Pereira', 'Carvalho', 'Costa', 'Gomes', 'Martins',
          'Rocha', 'Ramos', 'Mendes', 'Castro', 'Sousa', 'Fernandes', 'Nascimento', 'Cunha', 'Pinto', 'Barbosa', 'Melo', 'Cardoso'],
    "9": ['García', 'Hernández', 'Martínez', 'López', 'González', 'Rodríguez', 'Pérez', 'Sánchez', 'Ramírez', 'Flores', 'Torres', 'Rivera',
          'Gómez', 'Díaz', 'Reyes', 'Morales', 'Cruz', 'Ortega', 'Castillo', 'Chávez', 'Romero', 'Mendoza', 'Herrera', 'Medina', 'Aguilar'],
    "10": ['Patel', 'Sharma', 'Singh', 'Kumar', 'Joshi', 'Shah', 'Desai', 'Gupta', 'Gandhi', 'Mehta', 'Malhotra', 'Chopra', 'Lal', 'Rao',
           'Mishra', 'Agarwal', 'Jain', 'Agarwal', 'Verma', 'Chauhan', 'Reddy', 'Nair', 'Khan', 'Mathew', 'Thomas'],
    "11": ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang', 'Wu', 'Zhou', 'Xu', 'Sun', 'Ma', 'Hu', 'Gao', 'Lin', 'He', 'Guo', 'Luo',
           'Li', 'Xie', 'Wang', 'Tang', 'Cheng'],
    "12": ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Hernández',
           'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro', 'Torres', 'Domínguez', 'Vargas', 'Ramos', 'Castro'],
    "13": ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Oh', 'Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Oh',
           'Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang'],
    "14": ['Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Sokolov', 'Lebedev', 'Kozlov', 'Novikov', 'Morozov', 'Petrov', 'Volkov', 'Solovyov',
           'Vasilyev', 'Zaitsev', 'Golubev', 'Vinogradov', 'Bogdanov', 'Vorobyov', 'Kuzmin', 'Mironov', 'Kondratiev', 'Kudryavtsev', 'Baranov',
           'Tarasov', 'Belov'],
    "15": ['Okafor', 'Oluwaseyi', 'Nwachukwu', 'Adeboye', 'Onwuka', 'Adeyemi', 'Ogunleye', 'Ajayi', 'Osagie', 'Uzoma', 'Eze', 'Onyekachi',
           'Okafor', 'Ani', 'Ezeh', 'Okeke', 'Okonkwo', 'Ugwu', 'Orji', 'Okafor', 'Ejiofor', 'Nnamani', 'Okonkwo', 'Eze', 'Emeka'],
    "16": ['Mkhize', 'Zulu', 'Ndlovu', 'Nguyen', 'Nkosi', 'Dlamini', 'Sibiya', 'Khumalo', 'Mthembu', 'Nkomo', 'Zuma', 'Mokoena', 'Moore',
           'Van Wyk', 'Muller', 'Jansen', 'Gumede', 'Joubert', 'Du Plessis', 'Van Der Merwe', 'Naidoo', 'Viljoen', 'Coetzee', 'Smith', 'Venter'],
    "17": ['Mwangi', 'Kimani', 'Njoroge', 'Odhiambo', 'Omondi', 'Ochieng', 'Onyango', 'Muthoni', 'Wanjiku', 'Mwangi', 'Kimani', 'Njoroge',
           'Odhiambo', 'Omondi', 'Ochieng', 'Onyango', 'Muthoni', 'Wanjiku', 'Mwangi', 'Kimani', 'Njoroge', 'Odhiambo', 'Omondi', 'Ochieng',
           'Onyango']
}

# CREATES LIST OF SIX FRAMES, ONE FOR EACH MENU
menu_frames = []

def toggle_sack():
    global manager_sackable
    if sackable_button.cget("text") == "":
        manager_sackable = True
        sackable_button.config(text="✔")
    else:
        manager_sackable = False
        sackable_button.config(text="")

tutorial_league_widgets = []

def start_tutorial():
    global tutorial_pos, tutorial_labels, tutorial_league_widgets
    tutorial_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    tutorial_frame.lift()
    tutorial_message_label.config(text=tutorial_messages[0])
    tutorial_pos = 0

    for i in tutorial_labels:
        i.destroy()

    for i in tutorial_league_widgets:
        for j in i:
            j.destroy()

    # Append each Label widget to the list and then place it on the frame
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR))
    tutorial_labels[-1].place(relx=0, rely=0, relwidth=0.21, relheight=0.85)

    # League name label
    tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="England\nDivision Four"))
    tutorial_labels[-1].place(relx=0, rely=0, relwidth=0.21, relheight=0.075)

    # Subheadings: Pos, Played, Team, Points
    tutorial_labels.append(Label(tutorial_frame, text="Pos", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")))
    tutorial_labels[-1].place(relx=0.005, rely=0.075, relwidth=0.025, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, text="Played", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")))
    tutorial_labels[-1].place(relx=0.03, rely=0.075, relwidth=0.035, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, text="Team", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")))
    tutorial_labels[-1].place(relx=0.065, rely=0.075, relwidth=0.11, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, text="Points", bg="#363440", fg="white", font=("Comic Sans", 12, "bold")))
    tutorial_labels[-1].place(relx=0.17, rely=0.075, relwidth=0.04, relheight=0.03)

    # Divider line
    tutorial_labels.append(Label(tutorial_frame, bg="white"))
    tutorial_labels[-1].place(relx=0, rely=0.7785, relwidth=0.21, relheight=0.0002)

    # Promotion label
    tutorial_labels.append(Label(tutorial_frame, bg="green"))
    tutorial_labels[-1].place(relx=0.005, rely=0.78, relwidth=0.005, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Promotion", fg="white", font=("Comic sans", 12)))
    tutorial_labels[-1].place(relx=0.01, rely=0.78, relwidth=0.095, relheight=0.03)

    # Playoffs label
    tutorial_labels.append(Label(tutorial_frame, bg="yellow"))
    tutorial_labels[-1].place(relx=0.105, rely=0.78, relwidth=0.005, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Playoffs", fg="white", font=("Comic sans", 12)))
    tutorial_labels[-1].place(relx=0.11, rely=0.78, relwidth=0.095, relheight=0.03)

    # European Cup label
    tutorial_labels.append(Label(tutorial_frame, bg="blue"))
    tutorial_labels[-1].place(relx=0.005, rely=0.815, relwidth=0.005, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="European Cup", fg="white", font=("Comic sans", 12)))
    tutorial_labels[-1].place(relx=0.01, rely=0.815, relwidth=0.095, relheight=0.03)

    # Relegation label
    tutorial_labels.append(Label(tutorial_frame, bg="red"))
    tutorial_labels[-1].place(relx=0.105, rely=0.815, relwidth=0.005, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Relegation", fg="white", font=("Comic sans", 12)))
    tutorial_labels[-1].place(relx=0.11, rely=0.815, relwidth=0.095, relheight=0.03)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
    tutorial_labels[-1].place(relx=0.23, rely=0.02, relwidth=0.75, relheight=0.3)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
    tutorial_labels[-1].place(relx=0.23, rely=0.34, relwidth=0.375, relheight=0.49)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
    tutorial_labels[-1].place(relx=0.625, rely=0.34, relwidth=0.355, relheight=0.49)

    # Other Labels
    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Today\n▼", font=("Comic Sans", 15), fg="white"))
    tutorial_labels[-1].place(relx=0.58, rely=0.103, relwidth=0.05, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Next Match", font=("Comic Sans", 24), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.34, relwidth=0.375, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Opponent Overview", font=("Comic Sans", 24), fg="white"))
    tutorial_labels[-1].place(relx=0.625, rely=0.34, relwidth=0.355, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="vs", font=("Comic Sans", 19), fg="white"))
    tutorial_labels[-1].place(relx=0.41, rely=0.48, relwidth=0.015, relheight=0.03)

    # Simulate Button
    tutorial_labels.append(Label(tutorial_frame, bg="#2482d3", fg="white", font=("Comic Sans", 20), text="Simulate"))
    tutorial_labels[-1].place(relx=0.505, rely=0.26, relwidth=0.2, relheight=0.05)

    # Attack Strength Indicators
    colors = ["#FF0000", "#FF7700", "#FFEE00", "#BBFF00", "#00FF00"]
    for i, color in enumerate(colors):
        tutorial_labels.append(Label(tutorial_frame, bg=color))
        tutorial_labels[-1].place(relx=0.635 + i * 0.0315, rely=0.56, relwidth=0.0315, relheight=0.051)

    tutorial_labels.append(Label(tutorial_frame, fg=colors[3], bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic Sans", 15)))
    tutorial_labels[-1].place(relx=0.635 + 3 * 0.0315, rely=0.615, relwidth=0.0315, relheight=0.03)

    # Attack Strength Labels
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 10), text="Weak\nAttack"))
    tutorial_labels[-1].place(relx=0.635, rely=0.52, relwidth=0.0315, relheight=0.04)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 10), text="Strong\nAttack"))
    tutorial_labels[-1].place(relx=0.761, rely=0.52, relwidth=0.0315, relheight=0.04)

    # Play Style Label
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 14, "bold"), text="Play Style"))
    tutorial_labels[-1].place(relx=0.625, rely=0.68, relwidth=0.1183, relheight=0.04)

    # Opponent Attack Style Label
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 12), text="Counter Attacking"))
    tutorial_labels[-1].place(relx=0.625, rely=0.74, relwidth=0.1183, relheight=0.04)

    # Opponent Strength and Weakness Labels
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 14, "bold"), text="Strengths"))
    tutorial_labels[-1].place(relx=0.7433, rely=0.68, relwidth=0.1183, relheight=0.04)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 14, "bold"), text="Weaknesses"))
    tutorial_labels[-1].place(relx=0.8616, rely=0.68, relwidth=0.1183, relheight=0.04)

    tutorial_strengths = ["Passing Over The Top", "Counter Attacking", "Defending Deep"]
    tutorial_weaknesses = ["Pressing", "High Tempo Passing", "Set Pieces"]

    for i in range(3):
        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="green", font=("Comic Sans", 12), text=tutorial_strengths[i]))
        tutorial_labels[-1].place(relx=0.7433, rely=0.725 + i * 0.03, relwidth=0.1183, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="red", font=("Comic Sans", 12), text=tutorial_weaknesses[i]))
        tutorial_labels[-1].place(relx=0.8616, rely=0.725 + i * 0.03, relwidth=0.1183, relheight=0.03)

    # Defense Strength Indicators
    for i, color in enumerate(reversed(colors)):
        tutorial_labels.append(Label(tutorial_frame, bg=color))
        tutorial_labels[-1].place(relx=0.9385 - i * 0.0315, rely=0.56, relwidth=0.0315, relheight=0.051)

    tutorial_labels.append(Label(tutorial_frame, fg=colors[2], bg=LIGHT_UI_COLOUR, text="🔼", font=("Comic Sans", 15)))
    tutorial_labels[-1].place(relx=0.9385 - 2 * 0.0315, rely=0.615, relwidth=0.0315, relheight=0.03)

    # Defense Strength Labels
    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 10), text="Weak\nDefence"))
    tutorial_labels[-1].place(relx=0.9385, rely=0.52, relwidth=0.0315, relheight=0.04)

    tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 10), text="Strong\nDefence"))
    tutorial_labels[-1].place(relx=0.8125, rely=0.52, relwidth=0.0315, relheight=0.04)

    # View Match Schedule Button
    tutorial_labels.append(Label(tutorial_frame, text="View Schedule", fg="white", bg=BUTTON_COLOUR, font=("Comic Sans", 20)))
    tutorial_labels[-1].place(relx=0.3275, rely=0.72, relwidth=0.18, relheight=0.08)

    # Values
    tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text=f"Year: 2024", font=("Comic Sans", 22, "bold"), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.02, relwidth=0.75, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text=f"Month: August", font=("Comic Sans", 18), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.07, relwidth=0.75, relheight=0.035)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Morcambe", font=("Comic Sans", 18, "bold"), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.47, relwidth=0.18, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Fleetwood Rovers", font=("Comic Sans", 18, "bold"), fg="white"))
    tutorial_labels[-1].place(relx=0.425, rely=0.47, relwidth=0.18, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="League", font=("Comic Sans", 18), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.56, relwidth=0.375, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="12 September 2024", font=("Comic Sans", 18), fg="white"))
    tutorial_labels[-1].place(relx=0.23, rely=0.66, relwidth=0.375, relheight=0.05)

    tutorial_labels.append(Label(tutorial_frame, text=29, font=("Comic Sans", 38), fg="white", bg="#363440"))
    tutorial_labels[-1].place(relx=0.32, rely=0.15, relwidth=0.05, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, text=30, font=("Comic Sans", 38), fg="white", bg="#363440"))
    tutorial_labels[-1].place(relx=0.45, rely=0.15, relwidth=0.05, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, text=1, font=("Comic Sans", 38), fg="white", bg="#26262e"))
    tutorial_labels[-1].place(relx=0.58, rely=0.15, relwidth=0.05, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, text=2, font=("Comic Sans", 38), fg="white", bg="#363440"))
    tutorial_labels[-1].place(relx=0.71, rely=0.15, relwidth=0.05, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, text=3, font=("Comic Sans", 38), fg="white", bg="#363440"))
    tutorial_labels[-1].place(relx=0.84, rely=0.15, relwidth=0.05, relheight=0.08)

    tutorial_labels.append(Label(tutorial_frame, text="Fleetwood Rovers", font=("Comic Sans", 19, "bold"), fg="white", bg="#363440"))
    tutorial_labels[-1].place(relx=0.7, rely=0.43, relwidth=0.2, relheight=0.08)


    tutorial_league_widgets = []
    for i in range(24):
        tutorial_league_widgets.append([Label(tutorial_frame, bg=LIGHT_UI_COLOUR),
                               Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 12, "bold")),
                               Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 12)),
                               Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 12)),
                               Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 12))])

        tutorial_league_widgets[i][0].place(relx=0, rely=i * 0.028 + 0.105, relwidth=0.005, relheight=0.03)
        tutorial_league_widgets[i][1].place(relx=0.005, rely=i * 0.028 + 0.105, relwidth=0.025, relheight=0.03)
        tutorial_league_widgets[i][2].place(relx=0.03, rely=i * 0.028 + 0.105, relwidth=0.035, relheight=0.03)
        tutorial_league_widgets[i][3].place(relx=0.065, rely=i * 0.028 + 0.105, relwidth=0.11, relheight=0.03)
        tutorial_league_widgets[i][4].place(relx=0.17, rely=i * 0.028 + 0.105, relwidth=0.04, relheight=0.03)

    promotion_spots = 2
    playoff_spots = 4

    for i in tutorial_league_widgets:
        for j in i:
            j.config(text="", bg=LIGHT_UI_COLOUR)

    for i in range(24):
        if i < promotion_spots:
            pos_bg = "green"
        elif i < promotion_spots + playoff_spots:
            pos_bg = "yellow"
        else:
            pos_bg = LIGHT_UI_COLOUR

        tutorial_league_widgets[i][0].config(bg=pos_bg)
        tutorial_league_widgets[i][1].config(text=i + 1)
        tutorial_league_widgets[i][2].config(text=eng_4[i][6])
        tutorial_league_widgets[i][3].config(text=eng_4[i][0])
        tutorial_league_widgets[i][4].config(text=eng_4[i][5])

def exit_tutorial():
    tutorial_frame.place_forget()

tutorial_pos = 0
tutorial_labels = []

def next_tutorial():
    global tutorial_pos, tutorial_labels
    tutorial_pos += 1
    if tutorial_pos >= len(tutorial_messages):
        exit_tutorial()
        return
    elif tutorial_pos == 4:
        for widget in tutorial_labels:
            widget.destroy()
        for i in tutorial_league_widgets:
            for j in i:
                j.destroy()

        # Headings for squad content
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Name▼", bg="#363440", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0, rely=0, relwidth=0.159, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Pos", bg="#26262e", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.159, rely=0, relwidth=0.04, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Ovr\n▼", bg="#363440", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.199, rely=0, relwidth=0.035, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Best\nPos\n▼", bg="#26262e", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.234, rely=0, relwidth=0.04, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 15), text="Fitness/\nsharpness/\nmorale", bg="#363440", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.274, rely=0, relwidth=0.065, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Age\n▼", bg="#26262e", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.339, rely=0, relwidth=0.038, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Value\n€..M\n▼", bg="#363440", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.377, rely=0, relwidth=0.041, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 18), text="Wage\n..K/week\n▼", bg="#26262e", fg="white", borderwidth=0))
        tutorial_labels[-1].place(relx=0.418, rely=0, relwidth=0.062, relheight=0.1)

        # Dropdown to pick formation
        options = [
            "4-4-2 DM", "4-4-2 CM", "4-3-3 CM", "4-3-3 DM", "4-3-2-1 DM", "4-3-2-1 CM",
            "4-2-3-1 DM", "4-2-3-1 CM", "4-1-2-1-2", "3-5-2 CM", "3-5-2 DM", "3-4-2-1 DM",
            "3-4-2-1 CM", "3-2-4-1", "5-3-2 CM", "5-3-2 DM", "5-2-3 DM", "5-2-3 CM",
            "5-2-1-2 DM", "5-2-1-2 CM"
        ]

        selected_formation.set("4-3-3 CM")

        # Tactics background label
        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.5, rely=0.03, relwidth=0.48, relheight=0.36)

        # Squad size info
        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=f"Min squad size: {MIN_SQUAD_SIZE}\nMax squad size: {MAX_SQUAD_SIZE}"))
        tutorial_labels[-1].place(relx=0.818, rely=0.33, relwidth=0.15, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 16), text=f"Current Squad Size: 27"))
        tutorial_labels[-1].place(relx=0.51, rely=0.33, relwidth=0.15, relheight=0.06)

        # Headings to show different parts of the tactic screen
        tutorial_labels.append(Label(tutorial_frame, text="Formation", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.51, rely=0.03, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Team Playstyle", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.51, rely=0.13, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Team Mentality", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.51, rely=0.23, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="When Ball Is Lost", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.635, rely=0.04, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="When Ball Is Won", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.635, rely=0.18, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Build Up Type", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.755, rely=0.04, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Attacking Area", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.755, rely=0.18, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Defensive Style", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.87, rely=0.03, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Attacking Width", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.87, rely=0.13, relwidth=0.1, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Defensive Width", bg="#363440", font=("Comic Sans", 12), fg="white"))
        tutorial_labels[-1].place(relx=0.87, rely=0.23, relwidth=0.1, relheight=0.04)

        # Formation pick option menu
        formation_pick = OptionMenu(tutorial_frame, selected_formation, *options)
        formation_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        formation_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
        formation_pick.place(relx=0.51, rely=0.07, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(formation_pick)

        # Used to cover playstyle pick during matches
        playstyle_cover_label = Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14, "bold"), text="")

        # Team playstyle option menu variables
        playstyles = ["None", "Gegenpress", "Tiki Taka", "Counter Attack", "Route One", "Park The Bus", "Wing Play"]
        selected_playstyle = StringVar()
        selected_playstyle.set("None")

        # Team playstyle option menu
        playstyle_pick = OptionMenu(tutorial_frame, selected_playstyle, *playstyles)
        playstyle_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        playstyle_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
        playstyle_pick.place(relx=0.51, rely=0.17, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(playstyle_pick)

        # Team mentality option menu variables
        mentalities = ["Very Defensive", "Defensive", "Balanced", "Attacking", "Very Attacking"]
        selected_mentality = StringVar()
        selected_mentality.set("Balanced")

        # Team mentality option menu
        mentality_pick = OptionMenu(tutorial_frame, selected_mentality, *mentalities)
        mentality_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        mentality_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 11))
        mentality_pick.place(relx=0.51, rely=0.27, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(mentality_pick)

        # Options to counter press or regroup
        # Counter-press button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Counter Press"))
        tutorial_labels[-1].place(relx=0.635, rely=0.08, relwidth=0.1, relheight=0.05)

        # Drop back button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Drop Back"))
        tutorial_labels[-1].place(relx=0.635, rely=0.13, relwidth=0.1, relheight=0.05)

        # Options to counter or hold shape
        # Counter button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Counter"))
        tutorial_labels[-1].place(relx=0.635, rely=0.22, relwidth=0.1, relheight=0.05)

        # Hold shape button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Hold Shape"))
        tutorial_labels[-1].place(relx=0.635, rely=0.27, relwidth=0.1, relheight=0.05)

        # Options for build-up phase
        # Direct build-up button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Direct Long Balls"))
        tutorial_labels[-1].place(relx=0.755, rely=0.08, relwidth=0.1, relheight=0.05)

        # Play out button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Play Out Of Defence"))
        tutorial_labels[-1].place(relx=0.755, rely=0.13, relwidth=0.1, relheight=0.05)

        # Attack wide or centrally buttons
        # Attack wide button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Wide"))
        tutorial_labels[-1].place(relx=0.755, rely=0.22, relwidth=0.1, relheight=0.05)

        # Attack centrally button replaced with a label
        tutorial_labels.append(Label(tutorial_frame, font=("Comic Sans", 11), bg="#26262e", fg="white", text="Central"))
        tutorial_labels[-1].place(relx=0.755, rely=0.27, relwidth=0.1, relheight=0.05)

        # Defending style option menu variables
        defence_types = ["High Press", "Mid Block", "Low Block"]
        selected_defence = StringVar()
        selected_defence.set("Mid Block")

        # Defending style option menu
        defence_pick = OptionMenu(tutorial_frame, selected_defence, *defence_types)
        defence_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        defence_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
        defence_pick.place(relx=0.87, rely=0.07, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(defence_pick)

        # Attacking widths option menu variables
        a_widths = ["Balanced", "Narrow", "Wide"]
        selected_a_width = StringVar()
        selected_a_width.set("Balanced")

        # Attacking widths option menu
        a_width_pick = OptionMenu(tutorial_frame, selected_a_width, *a_widths)
        a_width_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        a_width_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
        a_width_pick.place(relx=0.87, rely=0.17, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(a_width_pick)

        # Defensive widths option menu variables
        d_widths = ["Balanced", "Narrow", "Wide"]
        selected_d_width = StringVar()
        selected_d_width.set("Balanced")

        # Defensive widths option menu
        d_width_pick = OptionMenu(tutorial_frame, selected_d_width, *d_widths)
        d_width_pick.configure(background="#26262e", foreground="white", borderwidth=0, state="disabled")
        d_width_pick["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 15))
        d_width_pick.place(relx=0.87, rely=0.27, relwidth=0.1, relheight=0.05)

        tutorial_labels.append(d_width_pick)

        # Button to set tactics replaced with a label
        tutorial_labels.append(Label(tutorial_frame, bg="#2482d3", fg="white", text="Confirm Tactics\nAnd Squad", font=("comic sans", 14)))
        tutorial_labels[-1].place(relx=0.665, rely=0.33, relwidth=0.15, relheight=0.06)

        # Adding widgets to the tutorial_widgets list
        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 16), text="Player available for selection", anchor="n"))
        tutorial_labels[-1].place(relx=0, rely=0.685, relwidth=0.48, relheight=0.165)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 13), text="Adam Taylor"))
        tutorial_labels[-1].place(relx=0.01, rely=0.7, relwidth=0.12, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 27), text="68"))
        tutorial_labels[-1].place(relx=0.01, rely=0.73, relwidth=0.12, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 13), text="GK"))
        tutorial_labels[-1].place(relx=0.01, rely=0.78, relwidth=0.12, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 11), text="Contract Expires:"))
        tutorial_labels[-1].place(relx=0.01, rely=0.81, relwidth=0.07, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg="#363440", font=("Comic Sans", 12, "bold"), text="2027"))
        tutorial_labels[-1].place(relx=0.08, rely=0.81, relwidth=0.05, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg=DARK_UI_COLOUR, font=("Comic Sans", 11), text="Transfer List Player", borderwidth=0))
        tutorial_labels[-1].place(relx=0.36, rely=0.69, relwidth=0.12, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg=DARK_UI_COLOUR, font=("Comic Sans", 11), text="Negotiate New Contract", borderwidth=0))
        tutorial_labels[-1].place(relx=0.36, rely=0.74, relwidth=0.12, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, fg="white", bg=DARK_UI_COLOUR, font=("Comic Sans", 11), text="Release Player", borderwidth=0))
        tutorial_labels[-1].place(relx=0.36, rely=0.79, relwidth=0.12, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", fg="white", highlightthickness=5, highlightbackground="white", highlightcolor="white"))
        tutorial_labels[-1].place(relx=0.5, rely=0.42, relwidth=0.48, relheight=0.41)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="GK", font=("Comic Sans", 10), highlightbackground="green", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.52, rely=0.59, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="CB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.58, rely=0.5, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="CB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.58, rely=0.68, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="LB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.63, rely=0.44, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="RB", font=("Comic Sans", 10), highlightbackground="yellow", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.63, rely=0.74, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="DM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.67, rely=0.59, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="CM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.72, rely=0.5, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="CM", font=("Comic Sans", 10), highlightbackground="blue", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.72, rely=0.68, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="LF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.84, rely=0.44, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="RF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.84, rely=0.74, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", fg="white", text="CF", font=("Comic Sans", 10), highlightbackground="red", highlightthickness=2))
        tutorial_labels[-1].place(relx=0.9, rely=0.59, relwidth=0.04, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, text="Club Level", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)))
        tutorial_labels[-1].place(relx=0.12, rely=0.72, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Length of Training", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)))
        tutorial_labels[-1].place(relx=0.24, rely=0.72, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Playing Time", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)))
        tutorial_labels[-1].place(relx=0.12, rely=0.78, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Player Wage", bg=LIGHT_UI_COLOUR, fg="white", font=("Comic sans", 14)))
        tutorial_labels[-1].place(relx=0.24, rely=0.78, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Good", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="green"))
        tutorial_labels[-1].place(relx=0.12, rely=0.75, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow"))
        tutorial_labels[-1].place(relx=0.24, rely=0.75, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Okay", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="yellow"))
        tutorial_labels[-1].place(relx=0.12, rely=0.81, relwidth=0.1, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, text="Good", font=("Comic sans", 12), bg=LIGHT_UI_COLOUR, fg="green"))
        tutorial_labels[-1].place(relx=0.24, rely=0.81, relwidth=0.1, relheight=0.03)

        tutorial_squad_frame = Frame(tutorial_frame, bg=BG_COLOUR)
        tutorial_labels.append(tutorial_squad_frame)
        tutorial_labels[-1].place(relx=0, rely=0.1, relwidth=0.48, relheight=0.585)

        tutorial_players = [["Adam", "Taylor", 68, "GK", 25, 1.71, 2.1], ["Luis", "Lopez", 64, "LB", 22, 1.8, 0.88], ["Daniel", "Smith", 67, "CB", 33, 0.53, 2.4], ["Kit", "Moore", 66, "DM", 17, 2.4, 1.1], ["Oliver", "Clark", 62, "CM", 21, 1.4, 0.64], ["Raul", "Navarro", 69, "CM", 29, 1.5, 5.4], ["Lorenzo", "De Luca", 65, "AM", 26, 0.9, 1.2], ["George", "Hall", 62, "LF", 20, 2.3, 0.66],
                            ["William", "Lewis", 59, "LF", 16, 1.69, 0.4], ["Ricardo", "Colombo", 66, "RF", 24, 1.66, 1.3], ["Liam", "Morin", 67, "RF", 28, 1.9, 1.5], ["Ondrej", "Vamos", 74, "CF", 16, 10.1, 1.9], ["Alexandro", "De Marco", 64, "CF", 28, 0.8, 1.74]]

        tutorial_option_value = StringVar()
        tutorial_option_value.set("SUB")

        tutorial_labels.append(Label(tutorial_squad_frame, bg=LIGHT_UI_COLOUR, width=33, height=33))
        tutorial_labels[-1].grid(row=0, column=0, rowspan=13)

        for i in tutorial_players:

            labels = [
                Label(tutorial_squad_frame, text=f"{i[0]} {i[1]}", bg=LIGHT_UI_COLOUR, fg="white",
                   font=("Comic Sans", 15), padx=10, borderwidth=0,
                   width=round(SCREEN_WIDTH * 0.0132)),

                OptionMenu(tutorial_squad_frame, tutorial_option_value, ["SUB"]),

                Label(tutorial_squad_frame, text=i[2], bg="#3d4659", fg="white", font=("Comic Sans", 22),
                  padx=10, width=round(SCREEN_WIDTH * 0.001)),

                Label(tutorial_squad_frame, text=i[3], bg="#3d4659", fg="white", font=("Comic Sans", 22),
                  padx=10, width=round(SCREEN_WIDTH * 0.001)),

                Label(tutorial_squad_frame, bg="green", width=round(SCREEN_WIDTH * 0.001)),
                # makes space between labels
                Label(tutorial_squad_frame, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005)),

                Label(tutorial_squad_frame, bg="red", width=round(SCREEN_WIDTH * 0.001)),
                # makes space between labels
                Label(tutorial_squad_frame, bg="#3d4659", width=round(SCREEN_WIDTH * 0.0005)),

                Label(tutorial_squad_frame, bg="#84FF00", width=round(SCREEN_WIDTH * 0.001)),

                Label(tutorial_squad_frame, text=i[4], bg="#3d4659", fg="white", font=("Comic Sans", 22),
                  padx=round(SCREEN_WIDTH * 0.001), width=round(SCREEN_WIDTH * 0.0025)),
                Label(tutorial_squad_frame, text=i[5], bg="#3d4659", fg="white", font=("Comic Sans", 22),
                  padx=round(SCREEN_WIDTH * 0.0005), width=round(SCREEN_WIDTH * 0.002)),
                Label(tutorial_squad_frame, text=i[6], bg="#3d4659", fg="white", font=("Comic Sans", 22),
                  padx=round(SCREEN_WIDTH * 0.0005), width=round(SCREEN_WIDTH * 0.003))
            ]

            # configures option menu appearance
            labels[1].config(background="#26262e", foreground="white", highlightthickness=0, font=("Comic Sans", 8), state="disabled")
            labels[1]["menu"].config(background="#26262e", foreground="white", font=("Comic Sans", 12))

            # Grid the labels within the squadContent frame
            for j, label in enumerate(labels):
                label.grid(row=tutorial_players.index(i) + 1, column=j)
                tutorial_labels.append(label)

    elif tutorial_pos == 13:
        for widget in tutorial_labels:
            widget.destroy()

        # TRAINING DAY BG
        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.05, relwidth=0.3, relheight=0.59)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Training One", font=("Comic Sans", 25), fg="white"))
        tutorial_labels[-1].place(relx=0.02, rely=0.05, relwidth=0.3, relheight=0.1)

        # DAY BEFORE MATCHDAY TRAINING BG
        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.59)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Training Two", font=("Comic Sans", 25), fg="white"))
        tutorial_labels[-1].place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)

        # PRE MATCH TRAINING BG
        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.59)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Training Three", font=("Comic Sans", 25), fg="white"))
        tutorial_labels[-1].place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.1)

        # TEAM TRAINING REPORT
        tutorial_labels.append(Label(tutorial_frame, text="Training Report", bg=DARK_UI_COLOUR, fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.66, relwidth=0.455, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR))
        tutorial_labels[-1].place(relx=0.02, rely=0.7, relwidth=0.455, relheight=0.13)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Strengths", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.02, rely=0.7, relwidth=0.2275, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Playing Out Of Press", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.02, rely=0.74, relwidth=0.2275, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Pressing", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.02, rely=0.77, relwidth=0.2275, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Set Pieces", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.02, rely=0.8, relwidth=0.2275, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Weaknesses", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.2475, rely=0.7, relwidth=0.2275, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Counter Attacking", fg="red", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.2475, rely=0.74, relwidth=0.2275, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Defending Crosses", fg="red", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.2475, rely=0.77, relwidth=0.2275, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Wing Play", fg="red", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.2475, rely=0.8, relwidth=0.2275, relheight=0.03)

        # PLAYER REPORT BUTTON (REPLACED BY LABEL)
        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic Sans", 18), text="Players Report >"))
        tutorial_labels[-1].place(relx=0.34, rely=0.66, relwidth=0.135, relheight=0.04)

        # PLAYER REPORT WIDGETS
        for _ in range(9):
            tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-9].config(text="Best Training Performers")
        tutorial_labels[-8].config(text="Worst Training Performers")

        # SQUAD REPORT
        tutorial_labels.append(Label(tutorial_frame, text="Your Squad Report", bg=DARK_UI_COLOUR, fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.525, rely=0.66, relwidth=0.455, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR))
        tutorial_labels[-1].place(relx=0.525, rely=0.7, relwidth=0.455, relheight=0.13)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Goalkeepers", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.525, rely=0.7, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Good Quality", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.525, rely=0.74, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Medium Depth", fg="yellow", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.525, rely=0.78, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Defence", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.63875, rely=0.7, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Medium Quality", fg="yellow", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.63875, rely=0.74, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Good Depth", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.63875, rely=0.78, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Midfield", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.7525, rely=0.7, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Good Quality", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.7525, rely=0.74, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Good Depth", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.7525, rely=0.78, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Attack", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.86625, rely=0.7, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Good Quality", fg="green", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.86625, rely=0.74, relwidth=0.11375, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=LIGHT_UI_COLOUR, text="Low Depth", fg="red", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.86625, rely=0.78, relwidth=0.11375, relheight=0.04)

        # TRAINING TEXT
        tutorial_labels.append(Label(tutorial_frame, text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.17, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.35, rely=0.17, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Warm Up Length", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.68, rely=0.17, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.27, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.35, rely=0.27, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Training intensity", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.68, rely=0.28, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.37, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.35, rely=0.37, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Main Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.68, rely=0.37, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.47, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.35, rely=0.47, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Secondary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.68, rely=0.47, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.57, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.35, rely=0.57, relwidth=0.15, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Tertiary Focus", fg="white", bg="#363440", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.68, rely=0.57, relwidth=0.15, relheight=0.05)

        # Options Menu
        option_vars = []
        for relx, rely, text in [(0.17, 0.18, "Long"), (0.5, 0.18, "Medium"), (0.83, 0.18, "Medium"),
                           (0.17, 0.28, "High"), (0.5, 0.28, "High"), (0.83, 0.28, "Medium"),
                           (0.17, 0.38, "Passing Over The Top"), (0.5, 0.38, "Pressing"), (0.83, 0.38, "Playing Out Of Press"),
                           (0.17, 0.48, "Wing Play"), (0.5, 0.48, "Ball Possession"), (0.83, 0.48, "Set Pieces"),
                           (0.17, 0.58, "High Tempo Passing"), (0.5, 0.58, "Defending Crosses"), (0.83, 0.58, "Defending Deep")]:
            var = StringVar(tutorial_frame)
            option_vars.append(var)
            var.set(text)
            tutorial_labels.append(OptionMenu(tutorial_frame, var, ""))
            tutorial_labels[-1].place(relx=relx, rely=rely, relwidth=0.14, relheight=0.04)
            tutorial_labels[-1].config(bg=DARK_UI_COLOUR, state="disabled")
    elif tutorial_pos == 20:
        for i in tutorial_labels:
            i.destroy()

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.07, relwidth=0.192, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39"))
        tutorial_labels[-1].place(relx=0.212, rely=0.07, relwidth=0.192, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.404, rely=0.07, relwidth=0.192, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39"))
        tutorial_labels[-1].place(relx=0.596, rely=0.07, relwidth=0.192, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.788, rely=0.07, relwidth=0.192, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.29, relwidth=0.3, relheight=0.35)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e"))
        tutorial_labels[-1].place(relx=0.32, rely=0.29, relwidth=0.18, relheight=0.35)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.52, rely=0.29, relwidth=0.46, relheight=0.525)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.66, relwidth=0.23, relheight=0.155)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.27, rely=0.66, relwidth=0.23, relheight=0.155)

        # HEADINGS Section
        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Staff", fg="white", font=("Comic Sans", 20)))
        tutorial_labels[-1].place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Fitness Coach", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.07, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Physiotherapist", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.212, rely=0.07, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Chief Analyst", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.404, rely=0.07, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Goalkeeper Coach", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.596, rely=0.07, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Youth Coach", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.788, rely=0.07, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Conditions players' fitness and sharpness\nand helps them avoid injuries", fg="white", font=("Comic Sans", 11)))
        tutorial_labels[-1].place(relx=0.02, rely=0.21, relwidth=0.192, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Helps players recover from injuries\nand avoid a recurring injury", fg="white", font=("Comic Sans", 11)))
        tutorial_labels[-1].place(relx=0.212, rely=0.21, relwidth=0.192, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Helps prepare your players tactically for\nmatches to give your team an upper hand", fg="white", font=("Comic Sans", 11)))
        tutorial_labels[-1].place(relx=0.404, rely=0.21, relwidth=0.192, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Trains your goalkeepers and prepares\nthem properly for matches", fg="white", font=("Comic Sans", 11)))
        tutorial_labels[-1].place(relx=0.596, rely=0.21, relwidth=0.192, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Works with the youth team to improve the\nplayers and maximise talents coming through", fg="white", font=("Comic Sans", 11)))
        tutorial_labels[-1].place(relx=0.788, rely=0.21, relwidth=0.192, relheight=0.06)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Board Expectations", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.29, relwidth=0.3, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Relations", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.32, rely=0.29, relwidth=0.18, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Manager Rating", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.02, rely=0.38, relwidth=0.14, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="League", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.16, rely=0.33, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Domestic Cup", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.16, rely=0.43, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Continental Cup", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.16, rely=0.53, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Player Relations", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.32, rely=0.37, relwidth=0.18, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Fan Relations", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.32, rely=0.465, relwidth=0.18, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Youth Intake", fg="white", font=("Comic Sans", 18, "bold")))
        tutorial_labels[-1].place(relx=0.52, rely=0.29, relwidth=0.46, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Club Reputation", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.66, relwidth=0.23, relheight=0.035)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Sponsor", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.27, rely=0.66, relwidth=0.23, relheight=0.035)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Predicted Finish", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.02, rely=0.7, relwidth=0.115, relheight=0.035)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Club Rating", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.135, rely=0.7, relwidth=0.115, relheight=0.035)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Sponsor Name", fg="white", font=("Comic Sans", 16, "bold")))
        tutorial_labels[-1].place(relx=0.27, rely=0.7, relwidth=0.115, relheight=0.035)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Sponsor Revenue\n€M/year", fg="white", font=("Comic Sans", 14, "bold")))
        tutorial_labels[-1].place(relx=0.385, rely=0.7, relwidth=0.115, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Harry Jones", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.02, rely=0.11, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Wage: €780/w", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.116, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Rating: 2/10", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.02, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Alejandro De Marco", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.212, rely=0.11, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text=f"Wage: €550/w", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.308, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text=f"Rating: 1/10", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.212, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Liam Johnson", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.404, rely=0.11, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Wage: €490/w", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.5, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Rating: 1/10", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.404, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text="Luis Anderson", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.596, rely=0.11, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text=f"Wage: €930/w", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.692, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#302E39", text=f"Rating: 2/10", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.596, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Rory Smith", fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.788, rely=0.11, relwidth=0.192, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Wage: €1010/w", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.884, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Rating: 3/10", fg="white", font=("Comic Sans", 13)))
        tutorial_labels[-1].place(relx=0.788, rely=0.14, relwidth=0.096, relheight=0.03)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="50/100", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.43, relwidth=0.14, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Okay", fg="yellow", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.48, relwidth=0.14, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Fight for Playoffs", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.16, rely=0.38, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="Reach Round of 16", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.16, rely=0.48, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text="N/A", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.16, rely=0.58, relwidth=0.16, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Good", fg="green", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.32, rely=0.405, relwidth=0.18, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e", text="Good", fg="green", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.32, rely=0.515, relwidth=0.18, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"6", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.02, rely=0.735, relwidth=0.115, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"{random.randint(2, 3)}/20", fg="white", font=("Comic Sans", 18)))
        tutorial_labels[-1].place(relx=0.135, rely=0.735, relwidth=0.115, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", text=f"Aqua Resorts", fg="white", font=("Comic Sans", 14)))
        tutorial_labels[-1].place(relx=0.27, rely=0.735, relwidth=0.115, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 14), text=0.21))
        tutorial_labels[-1].place(relx=0.385, rely=0.75, relwidth=0.115, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade"))
        tutorial_labels[-1].place(relx=0.045, rely=0.17, relwidth=0.15, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade"))
        tutorial_labels[-1].place(relx=0.235, rely=0.17, relwidth=0.15, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade"))
        tutorial_labels[-1].place(relx=0.43, rely=0.17, relwidth=0.15, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade"))
        tutorial_labels[-1].place(relx=0.62, rely=0.17, relwidth=0.15, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 20), text="Upgrade"))
        tutorial_labels[-1].place(relx=0.815, rely=0.17, relwidth=0.15, relheight=0.04)
    elif tutorial_pos == 23:
        for i in tutorial_labels:
            i.destroy()

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.72, rely=0.05, relwidth=0.26, relheight=0.48)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.72, rely=0.6, relwidth=0.26, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e"))
        tutorial_labels[-1].place(relx=0.33, rely=0.05, relwidth=0.33, relheight=0.36)

        tutorial_labels.append(Label(tutorial_frame, bg="#26262e"))
        tutorial_labels[-1].place(relx=0.33, rely=0.44, relwidth=0.33, relheight=0.36)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.05, relwidth=0.26, relheight=0.36)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.44, relwidth=0.26, relheight=0.36)

        # SUBHEADINGS
        tutorial_labels.append(Label(tutorial_frame, text="Remaining Transfer Budget", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.75, rely=0.06, relwidth=0.2, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Remaining Wage Budget", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.75, rely=0.21, relwidth=0.2, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Current Wage Expenditure", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.75, rely=0.36, relwidth=0.2, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Income Split\nTransfer/Wage", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.75, rely=0.6, relwidth=0.2, relheight=0.08)

        tutorial_labels.append(Label(tutorial_frame, text="Income", bg="#26262e", fg="white", font=("Comic Sans", 20)))
        tutorial_labels[-1].place(relx=0.38, rely=0.05, relwidth=0.15, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="Total:", bg="#26262e", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.53, rely=0.05, relwidth=0.05, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="Home and Away Tickets:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.14, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Merchandise Sales:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.185, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Player Sales:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.23, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Broadcasting rights:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.275, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Competition Bonuses:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.32, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Sponsorships:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.365, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Losses", bg="#26262e", fg="white", font=("Comic Sans", 20)))
        tutorial_labels[-1].place(relx=0.38, rely=0.44, relwidth=0.15, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="Total:", bg="#26262e", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.53, rely=0.44, relwidth=0.05, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="Player Wages:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.53, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Staff Wages:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.575, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Player Signings:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.62, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Staff Signings:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.665, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Facility Costs:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.71, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Facility Upgrades:", bg="#363440", fg="white", font=("Comic Sans", 15)))
        tutorial_labels[-1].place(relx=0.33, rely=0.755, relwidth=0.25, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="Total Profit", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.02, rely=0.06, relwidth=0.26, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Board's Profit Expectation", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.02, rely=0.21, relwidth=0.26, relheight=0.04)

        tutorial_labels.append(Label(tutorial_frame, text="Ticket Price", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.02, rely=0.46, relwidth=0.26, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, text="Fan Relations", bg="#363440", fg="white", font=("Comic Sans", 17)))
        tutorial_labels[-1].place(relx=0.02, rely=0.63, relwidth=0.26, relheight=0.05)

        tutorial_labels.append(Label(tutorial_frame, text="Good", fg="green", bg=LIGHT_UI_COLOUR, font=("Comic sans", 20)))
        tutorial_labels[-1].place(relx=0.02, rely=0.68, relwidth=0.26, relheight=0.07)

        tutorial_labels.append(Label(tutorial_frame, text="€ 1,090,243", bg="#26262e", fg="white", font=("Comic Sans", 25)))
        tutorial_labels[-1].place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, text="€ 2,190", bg="#26262e", fg="white", font=("Comic Sans", 25)))
        tutorial_labels[-1].place(relx=0.75, rely=0.25, relwidth=0.2, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, text="€ 34,170", bg="#26262e", fg="white", font=("Comic Sans", 25)))
        tutorial_labels[-1].place(relx=0.75, rely=0.4, relwidth=0.2, relheight=0.1)

        # Replacing the income split OptionMenu with a Label and appending to tutorial_labels
        tutorial_labels.append(Label(tutorial_frame, text="50/50", bg="#26262e", fg="white", font=("Comic Sans", 19)))
        tutorial_labels[-1].place(relx=0.775, rely=0.7, relwidth=0.15, relheight=0.07)

        # Replacing the income split button with a Label and appending to tutorial_labels
        tutorial_labels.append(Label(tutorial_frame, text="Confirm", bg=BUTTON_COLOUR, fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.925, rely=0.7, relwidth=0.05, relheight=0.07)

        # Replacing the league ticket price OptionMenu with a Label and appending to tutorial_labels
        tutorial_labels.append(Label(tutorial_frame, text="€20", bg="#26262e", fg="white", font=("Comic Sans", 19)))
        tutorial_labels[-1].place(relx=0.075, rely=0.53, relwidth=0.15, relheight=0.07)

        # Replacing the league ticket price button with a Label and appending to tutorial_labels
        tutorial_labels.append(Label(tutorial_frame, text="Confirm", bg=BUTTON_COLOUR, fg="white", font=("Comic Sans", 16)))
        tutorial_labels[-1].place(relx=0.225, rely=0.53, relwidth=0.05, relheight=0.07)

        # Replacing all the other labels that show financial data with their respective Label widgets and appending to tutorial_labels
        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 14)))
        tutorial_labels[-1].place(relx=0.58, rely=0.05, relwidth=0.08, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.14, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.185, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.23, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.275, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.32, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="green", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.365, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="white", font=("Comic Sans", 25)))
        tutorial_labels[-1].place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, text="€ {:,}".format(special_round(random.randint(700000, 1200000), 100000)), bg="#26262e", fg="white", font=("Comic Sans", 25)))
        tutorial_labels[-1].place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.1)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 14)))
        tutorial_labels[-1].place(relx=0.58, rely=0.44, relwidth=0.08, relheight=0.09)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.53, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.575, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.62, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.665, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.71, relwidth=0.08, relheight=0.045)

        tutorial_labels.append(Label(tutorial_frame, text="€0", bg="#26262e", fg="red", font=("Comic Sans", 12)))
        tutorial_labels[-1].place(relx=0.58, rely=0.755, relwidth=0.08, relheight=0.045)
    elif tutorial_pos == 27:
        for i in tutorial_labels:
            i.destroy()

        # Add labels with tutorial_frame as master
        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.02, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.265, rely=0.02, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.51, rely=0.02, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.755, rely=0.02, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.24, relwidth=0.225, relheight=0.22)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.02, rely=0.485, relwidth=0.225, relheight=0.33)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.265, rely=0.22, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.51, rely=0.22, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.755, rely=0.22, relwidth=0.225, relheight=0.2)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.265, rely=0.44, relwidth=0.225, relheight=0.375)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.51, rely=0.44, relwidth=0.225, relheight=0.375)

        tutorial_labels.append(Label(tutorial_frame, bg="#363440"))
        tutorial_labels[-1].place(relx=0.755, rely=0.44, relwidth=0.225, relheight=0.375)

        # Chief Scout Label
        chief_scout_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Chief Scout")
        chief_scout_label.place(relx=0.02, rely=0.02, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(chief_scout_label)

        # Scout One Label
        scout_one_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout One")
        scout_one_label.place(relx=0.265, rely=0.02, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_one_label)

        # Scout Two Label
        scout_two_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout Two")
        scout_two_label.place(relx=0.51, rely=0.02, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_two_label)

        # Scout Three Label
        scout_three_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20, "bold"), text="Scout Three")
        scout_three_label.place(relx=0.755, rely=0.02, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_three_label)

        # Transfer Offers Label
        transfer_offers_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20), text="Transfer Offers")
        transfer_offers_label.place(relx=0.02, rely=0.24, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(transfer_offers_label)

        # Negotiations Label
        negotiations_label = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20), text="Negotiations")
        negotiations_label.place(relx=0.02, rely=0.485, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(negotiations_label)

        # Scouted Players Labels
        scouted_players_label_1 = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players")
        scouted_players_label_1.place(relx=0.265, rely=0.44, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scouted_players_label_1)

        scouted_players_label_2 = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players")
        scouted_players_label_2.place(relx=0.51, rely=0.44, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scouted_players_label_2)

        scouted_players_label_3 = Label(tutorial_frame, bg="#26262e", fg="white", font=("Comic Sans", 20), text="Scouted Players")
        scouted_players_label_3.place(relx=0.755, rely=0.44, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scouted_players_label_3)

        # Search Focus Labels
        search_focus_label_1 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus")
        search_focus_label_1.place(relx=0.265, rely=0.22, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(search_focus_label_1)

        search_focus_label_2 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus")
        search_focus_label_2.place(relx=0.51, rely=0.22, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(search_focus_label_2)

        search_focus_label_3 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Search Focus")
        search_focus_label_3.place(relx=0.755, rely=0.22, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(search_focus_label_3)

        # Quality Level Labels
        quality_level_label_1 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level")
        quality_level_label_1.place(relx=0.265, rely=0.265, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(quality_level_label_1)

        quality_level_label_2 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level")
        quality_level_label_2.place(relx=0.51, rely=0.265, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(quality_level_label_2)

        quality_level_label_3 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Quality Level")
        quality_level_label_3.place(relx=0.755, rely=0.265, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(quality_level_label_3)

        # Position Focus Labels
        position_focus_label_1 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus")
        position_focus_label_1.place(relx=0.265, rely=0.32, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(position_focus_label_1)

        position_focus_label_2 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus")
        position_focus_label_2.place(relx=0.51, rely=0.32, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(position_focus_label_2)

        position_focus_label_3 = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 13), text="Position Focus")
        position_focus_label_3.place(relx=0.755, rely=0.32, relwidth=0.075, relheight=0.04)
        tutorial_labels.append(position_focus_label_3)

        # Chief Scout Attributes
        chief_scout_name_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Archer Brown")
        chief_scout_name_label.place(relx=0.02, rely=0.07, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(chief_scout_name_label)

        chief_scout_rating_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Rating: 2/10")
        chief_scout_rating_label.place(relx=0.02, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(chief_scout_rating_label)

        chief_scout_wage_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Wage: €1050 /w")
        chief_scout_wage_label.place(relx=0.1325, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(chief_scout_wage_label)

        chief_scout_upgrade_label = Label(tutorial_frame, fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade")
        chief_scout_upgrade_label.place(relx=0.06, rely=0.16, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(chief_scout_upgrade_label)

        # Scout One Attributes
        scout_one_name_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Liam Evans")
        scout_one_name_label.place(relx=0.265, rely=0.07, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_one_name_label)

        scout_one_rating_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Rating: 2/10")
        scout_one_rating_label.place(relx=0.265, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_one_rating_label)

        scout_one_wage_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Wage: €870 /w")
        scout_one_wage_label.place(relx=0.3775, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_one_wage_label)

        scout_one_upgrade_label = Label(tutorial_frame, fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade")
        scout_one_upgrade_label.place(relx=0.305, rely=0.16, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(scout_one_upgrade_label)

        # Scout Two Attributes
        scout_two_name_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Atticus Wilson")
        scout_two_name_label.place(relx=0.51, rely=0.07, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_two_name_label)

        scout_two_rating_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Rating: 1/10")
        scout_two_rating_label.place(relx=0.51, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_two_rating_label)

        scout_two_wage_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Wage: €680 /w")
        scout_two_wage_label.place(relx=0.6225, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_two_wage_label)

        scout_two_upgrade_label = Label(tutorial_frame, fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade")
        scout_two_upgrade_label.place(relx=0.55, rely=0.16, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(scout_two_upgrade_label)

        # Scout Three Attributes
        scout_three_name_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text="Oliver Harris")
        scout_three_name_label.place(relx=0.755, rely=0.07, relwidth=0.225, relheight=0.05)
        tutorial_labels.append(scout_three_name_label)

        scout_three_rating_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Rating: 2/10")
        scout_three_rating_label.place(relx=0.755, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_three_rating_label)

        scout_three_wage_label = Label(tutorial_frame, bg="#363440", fg="white", font=("Comic Sans", 16), text=f"Wage: €900 /w")
        scout_three_wage_label.place(relx=0.8675, rely=0.12, relwidth=0.1125, relheight=0.035)
        tutorial_labels.append(scout_three_wage_label)

        scout_three_upgrade_label = Label(tutorial_frame, fg="white", bg="#2482d3", font=("Comic Sans", 15), text="Upgrade")
        scout_three_upgrade_label.place(relx=0.795, rely=0.16, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(scout_three_upgrade_label)

        # Scout one instructions
        search_type_one = StringVar()
        search_type_one.set("Any")
        search_type_pick_one = OptionMenu(tutorial_frame, search_type_one, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
        search_type_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        search_type_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        search_type_pick_one.place(relx=0.34, rely=0.21, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(search_type_pick_one)

        quality_level_one = StringVar()
        quality_level_one.set("Any")
        quality_level_pick_one = OptionMenu(tutorial_frame, quality_level_one, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
        quality_level_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        quality_level_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        quality_level_pick_one.place(relx=0.34, rely=0.265, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(quality_level_pick_one)

        pos_focus_one = StringVar()
        pos_focus_one.set("Any")
        pos_focus_pick_one = OptionMenu(tutorial_frame, pos_focus_one, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
        pos_focus_pick_one.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        pos_focus_pick_one["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        pos_focus_pick_one.place(relx=0.34, rely=0.32, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(pos_focus_pick_one)

        # Scout two instructions
        search_type_two = StringVar()
        search_type_two.set("Any")
        search_type_pick_two = OptionMenu(tutorial_frame, search_type_two, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
        search_type_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        search_type_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        search_type_pick_two.place(relx=0.585, rely=0.21, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(search_type_pick_two)

        quality_level_two = StringVar()
        quality_level_two.set("Any")
        quality_level_pick_two = OptionMenu(tutorial_frame, quality_level_two, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
        quality_level_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        quality_level_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        quality_level_pick_two.place(relx=0.585, rely=0.265, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(quality_level_pick_two)

        pos_focus_two = StringVar()
        pos_focus_two.set("Any")
        pos_focus_pick_two = OptionMenu(tutorial_frame, pos_focus_two, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
        pos_focus_pick_two.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        pos_focus_pick_two["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        pos_focus_pick_two.place(relx=0.585, rely=0.32, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(pos_focus_pick_two)

        # Scout three instructions
        search_type_three = StringVar()
        search_type_three.set("Any")
        search_type_pick_three = OptionMenu(tutorial_frame, search_type_three, *["Any", "Young Talents", "Experienced Developed Players", "Older Cheaper Players"])
        search_type_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        search_type_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        search_type_pick_three.place(relx=0.83, rely=0.21, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(search_type_pick_three)

        quality_level_three = StringVar()
        quality_level_three.set("Any")
        quality_level_pick_three = OptionMenu(tutorial_frame, quality_level_three, *["Any", "Team Superstar", "Strong Starter", "Competitive Starter", "Rotation Player", "Squad Depth Player"])
        quality_level_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        quality_level_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        quality_level_pick_three.place(relx=0.83, rely=0.265, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(quality_level_pick_three)

        pos_focus_three = StringVar()
        pos_focus_three.set("Any")
        pos_focus_pick_three = OptionMenu(tutorial_frame, pos_focus_three, *["Any", "GK", "LB", "RB", "CB", "DM", "CM", "AM", "LF", "RF", "CF", "Defence", "Midfield", "Attack"])
        pos_focus_pick_three.config(bg="#26262e", fg="white", font=("Comic Sans", 10))
        pos_focus_pick_three["menu"].config(bg="#26262e", fg="white", font=("Comic Sans", 12))
        pos_focus_pick_three.place(relx=0.83, rely=0.32, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(pos_focus_pick_three)

        # Buttons to confirm scouts search criteria
        confirm_scout_one_button = Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm")
        confirm_scout_one_button.place(relx=0.305, rely=0.375, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(confirm_scout_one_button)

        confirm_scout_two_button = Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm")
        confirm_scout_two_button.place(relx=0.55, rely=0.375, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(confirm_scout_two_button)

        confirm_scout_three_button = Label(tutorial_frame, bg=BUTTON_COLOUR, fg="white", font=("Comic sans", 19), text="Confirm")
        confirm_scout_three_button.place(relx=0.795, rely=0.375, relwidth=0.145, relheight=0.04)
        tutorial_labels.append(confirm_scout_three_button)


    tutorial_message_label.config(text=tutorial_messages[tutorial_pos])

tutorial_messages = ["This is the match menu. On the left you can see the league table. The first column of numbers show each team's position in the league,\nthe next shows the amount of matches played and the last column of numbers shows each teams points, teams are sorted by points they earn through matches.",
                     "The \"View Schedule\" button allows you to see what teams you will face, in what order, in what competition and whether you are\nthe home or away team",
                     "The Opponent Overview label allows you to see the strengths and weaknesses of your next opponent to allow you to adapt\nyour tactics and training schedule before each matchday.",
                     "The Simulate button allows you to simulate forward in time. This allows you to simulate up to the next matchday where you will\nthen be given the option to start the match.",
                     "This is the squad menu. On the left you can see all your players and their attributes, ovr gives you an idea of the player's\nquality. When players are younger, their ovr will grow, once they become older their ovr will start to decrease.",
                     "The three coloured squares show your player's fitness, sharpness and happiness in that order, a player's fitness decreases\nduring matches and training and increases with rest, sharpness increases by training. All 3 determine how well your player will perform.",
                     "You can order your players by different attributes by clicking on the labels at the top, for example clicking on ovr willl sort\nyour players by their ovr rating.",
                     "Clicking on a player's name allows you to see more details about that player. You can see a breakdown of their happiness,\nwhen their contract with you expires and a button to negotiate a new contract. You can also transfer list and release players.",
                     "On the right you can set your team's tactics, simply select your tactics however make sure to press the confirm squad and\ntactics button to save changes. Under the tactics area you can see a view of your team's formation and what positions are included.",
                     "Before each match, you must confirm your squad by pressing the confirm squad and tactics button. To do this, you must\nselect a valid squad by using the dropdown menus next to the player's names, the positions must match the selected formation to be able to submit your squad.",
                     "Keep in mind, you cannot start an injured player. You can tell if a player is injured as their name on the squad list\nwill have a red background, clicking on their name allows you to see how long their injury is.",
                     "It is possible to play a player out of position, however this will decrease their ability, positions with the same\nlast letter as the player's best position will reduce your player's ability less than other positions, but players will prefer to play their exact best position.",
                     "You can make substitutions and tactical changes during matches so players that start as a subsitute may still\nplay. You can make 5 substitutions per match.",
                     "This is the training menu, training can impact your player's performance, their happiness, their chance of getting injured\nand your team's playstyle.",
                     "There are three distinct training routines that rotate each day. On any given day, your players will only complete one\nof the routines: Training One, Training Two, or Training Three. After finishing the third routine, the cycle resets, starting again with Training One.",
                     "The warm up length can affect how likely your players are to get injured in training, a longer warm up reduces\ninjury risk however players will be unhappy to have to train for longer, a shorter warm up length does the opposite so try to find a balance.",
                     "Training Intensity affects player sharpness and fitness. High intensity training helps get your players sharp for matches\nhowever it will reduce your players fitness, low intensity does the opposite. It is up to you to find a balance between the two.",
                     "Keep in mind that players gain sharpness from matches so it is likely a good idea to lower training intensity\nwhen your match calendar gets busy to make sure your players are fit enough for the next match.",
                     "Training focuses are crucial to execute your tactical vision. The most important aspects of you tactical plan should be put as\nmain focuses. For example if you are playing a Tiki Taka style, you would need your players to be good at ball possession and high tempo passing.",
                     "Try to keep a balance of all areas in training as any weak spots in you team tactically may be exploited by the opposition.\nYou can also adjust training depending on the opponent. For example if you are playing a team that plays direct football, your team need to be ready to deal with crosses.",
                     "This is the club menu. At the top of the menu, you can see your club's staff, each one has a description of their role\nyou can upgrade your staff to improve their ability however there is an upgrade cost and their wage will increase.",
                     "The Board Expectations label allows you to see what the club expects of you as manager in the league, in the cup (domestic)\nand the european cup (continental) if you have qualified. These objectives affect your manager rating, if it becomes too low, you might be sacked.",
                     "The Youth Intake label allows you to promote any promising youth players from your youth academy, these players do not\nrequire transfer fees and have low wages making them ideal for a low budget, give them some game time and their ovr rating will grow quickly, making them into a top player.",
                     "This is the finances menu, in the top left you can see your total profit, this is your total income subtracted by your total losses.\nThe board's profit expectation is the profit your board expect you to have at the end of the season, achieving this improves your manager rating.",
                     "In the middle, you can see a breakdown of your profits and losses to see where you are gaining and losing money. You can split the money\nyou gain into your transfer budget for buying players and staff or into your wage budget for paying wages by using the dropdown in the bottom right.",
                     "You can see your transfer and wage budget in the top right. When you buy a player, this money is taken from your transfer budget, you cannot buy a player if\nyou do not have enough, the same goes for the wage budget and the player's wage. Wage is taken once from the wage budget instead of each week.",
                     "In the bottom left, you can pick your club's ticket prices. This and your stadium's attendance determines how much money you make\nfrom tickets sold for home games, however if you set it too high, you may upset your fans.",
                     "This is the transfers menu, at the top of the screen you can see your 4 scouts, upgrading the chief scout improves the ability\nof all scouts meanwhile upgrading each scout improves their ability individually, a better scout will be able to find more players that you want, faster.",
                     "Under each scout you can pick the search criteria for the players you want to find, you can pick their age range, their ovr range compared to your squad\nand their position. After confirming these, scouts will find players meeting this criteria that you can then negotiate with to sign them.",
                     "The transfer offer labels will show offers from other clubs for your players, clubs will be more interested in younger players and be\nwilling to pay more for them than older players. You can also transfer list a player to make an offer more likely to come in for them.",
                     "The negotiations label is where all negotiations with your players, youth academy players and other players will occur, you can renegotiate transfer fees\nwhere applicable, wages and contract lengths."]

# PITCH LINES
halfway_line = Label(window, bg="white")
halfway_line.place(relx=0.497, rely=0, relwidth=0.006, relheight=1)

tutorial_frame = Frame(window, bg=BG_COLOUR)
Label(tutorial_frame, bg=DARK_UI_COLOUR).place(relx=0, rely=0.85, relwidth=1, relheight=0.15)
Button(tutorial_frame, bg="red", text="Exit", fg="#AC0E0E", font=("Comic sans", 30, "bold"), command=exit_tutorial).place(relx=0.02, rely=0.88, relwidth=0.065, relheight=0.09)
Button(tutorial_frame, bg=BUTTON_COLOUR, text="Next", fg="#1A5589", font=("Comic sans", 30, "bold"), command=next_tutorial).place(relx=0.915, rely=0.88, relwidth=0.065, relheight=0.09)
tutorial_message_label = Label(tutorial_frame, bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 13), text="")
tutorial_message_label.place(relx=0.085, rely=0.85, relwidth=0.83, relheight=0.15)

left_box_top = Label(window, bg="white")
left_box_top.place(relx=0, rely=0.2, relwidth=0.17, relheight=0.01)
left_box_bot = Label(window, bg="white")
left_box_bot.place(relx=0, rely=0.79, relwidth=0.17, relheight=0.01)
left_box_len = Label(window, bg="white")
left_box_len.place(relx=0.17, rely=0.2, relwidth=0.006, relheight=0.6)
inleft_box_top = Label(window, bg="white")
inleft_box_top.place(relx=0, rely=0.37, relwidth=0.06, relheight=0.01)
inleft_box_bot = Label(window, bg="white")
inleft_box_bot.place(relx=0, rely=0.62, relwidth=0.06, relheight=0.01)
inleft_box_len = Label(window, bg="white")
inleft_box_len.place(relx=0.06, rely=0.37, relwidth=0.006, relheight=0.26)

right_box_top = Label(window, bg="white")
right_box_top.place(relx=0.83, rely=0.2, relwidth=0.17, relheight=0.01)
right_box_bot = Label(window, bg="white")
right_box_bot.place(relx=0.83, rely=0.79, relwidth=0.17, relheight=0.01)
right_box_len = Label(window, bg="white")
right_box_len.place(relx=0.83, rely=0.2, relwidth=0.006, relheight=0.6)
inright_box_top = Label(window, bg="white")
inright_box_top.place(relx=0.94, rely=0.37, relwidth=0.07, relheight=0.01)
inright_box_bot = Label(window, bg="white")
inright_box_bot.place(relx=0.94, rely=0.62, relwidth=0.07, relheight=0.01)
inright_box_len = Label(window, bg="white")
inright_box_len.place(relx=0.94, rely=0.37, relwidth=0.006, relheight=0.26)

left_pen_spot = Label(window, bg="green", fg="white", text=" .", font=("Calibri", 100))
left_pen_spot.place(relx=0.076, rely=0.36, relwidth=0.09, relheight=0.2)
right_pen_spot = Label(window, bg="green", fg="white", text=".", font=("Calibri", 100))
right_pen_spot.place(relx=0.836, rely=0.36, relwidth=0.09, relheight=0.2)

# BACKGROUND
background = Label(window, background="#26262e")
background.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.6)

background_two = Label(window, background="#26262e")
background_two.place(relx=0.25, rely=0.82, relwidth=0.5, relheight=0.14)

title = Label(window, background="green", font=("Comic sans", 65, "bold"), text="Strategy F.C.", fg="white")
title.place(relx=0.2, rely=0, relwidth=0.6, relheight=0.15)

halfway_line_bg = Label(window, bg="#4A4A60")
halfway_line_bg.place(relx=0.497, rely=0.15, relwidth=0.006, relheight=0.6)

# NEW GAME BUTTON
new_game = Button(window, text="New Career", compound="center", font=("Comic Sans", 45, "bold"), relief="flat", fg="white",
                 command=set_up, background="#3d4659")
new_game.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.1)

# LOAD GAME BUTTON
load_game = Label(window, text="Coming Soon", compound="center", font=("Comic Sans", 45, "bold"), relief="flat", fg="white",
                   background="#3d4659")
load_game.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)

# EXIT GAME BUTTON
exit_game = Button(window, text="Exit Game", compound="center", font=("Comic Sans", 45, "bold"), relief="flat", fg="white",
                  command=window.destroy, background="#3d4659")
exit_game.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.1)

settings_button = Button(window, text="Settings", bg=DARK_UI_COLOUR, fg="white", font=("Comic sans", 28, "bold"), bd=0, activebackground=DARK_UI_COLOUR, activeforeground="white", command=lambda: settings_frame.place(relx=0, rely=0, relwidth=1, relheight=1))
settings_button.place(relx=0.25, rely=0.82, relwidth=0.25, relheight=0.14)

tutorial_button = Button(window, text="Tutorial", bg=DARK_UI_COLOUR, fg=TUTORIAL_COLOUR, font=("Comic sans", 28, "bold"), bd=0, activebackground=DARK_UI_COLOUR, activeforeground="white", command=start_tutorial)
tutorial_button.place(relx=0.5, rely=0.82, relwidth=0.25, relheight=0.14)

halfway_line_bg_2 = Label(window, bg="#4A4A60")
halfway_line_bg_2.place(relx=0.497, rely=0.82, relwidth=0.006, relheight=0.14)

settings_frame = Frame(window, bg=DARK_UI_COLOUR)

Button(settings_frame, fg="white", bg=BUTTON_COLOUR, text="Confirm", font=("Comic sans", 20), command=lambda: settings_frame.place_forget()).place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.1)
Label(settings_frame ,fg="White", bg=GREEN, font=("Comic sans", 245), text="O").place(relx=0.175, rely=0.35, relwidth=0.15, relheight=0.3)
Label(settings_frame, bg=DARK_UI_COLOUR).place(relx=0.175, rely=0.642, relwidth=0.15, relheight=0.008)
Label(settings_frame, text="Adjust DPI scaling so that the white circle\nfits perfectly in the green square", fg="white", bg=DARK_UI_COLOUR, font=("Comic sans", 16)).place(relx=0.075, rely=0.28, relwidth=0.35, relheight=0.07)

Label(settings_frame, fg="white", bg=DARK_UI_COLOUR, font=("Comic Sans", 20), text="Manager can\nbe sacked").place(relx=0.575, rely=0.38, relwidth=0.35, relheight=0.08)
sackable_button = Button(settings_frame, fg="black", bg="white", font=("Comic Sans", 25), command=toggle_sack, text="✔")
sackable_button.place(relx=0.725, rely=0.46, relwidth=0.05, relheight=0.08)
# constants set by setting up club
CLUB_NAME = ""
MANAGER_NAME = ""
CLUB_COLOUR = ""
CLUB_COUNTRY = ""

window.mainloop()