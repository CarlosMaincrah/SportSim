import json
import random
import time
import os
from smtplib import SMTP
import src.email_credentials as ec

path = os.path.dirname(os.path.abspath(__file__))

#"EQUIPO": [ATACK, DEFENSE, REPUTATION]
with open(path + r"\src\fut.json","r") as file:
    statsfut = json.load(file)
with open(path + r"\src\basq.json", "r") as archivo:
    statsbasq = json.load(archivo)
with open(path + r"\src\logins.json","r") as login_data:
    login_info = json.load(login_data)

debug = False #Set to True if debugging

sport_day = []
user = ""
money = 0
cont = 0
log = 0
bets = []
code = ""

def correo_verif(email):
    """Function to send a verification email when creating an account"""
    global code, user
    try:
        for i in range(6):
            piece_of_code = str(random.randint(0,10))
            code = code + piece_of_code
        message = f"""
            Subject: Verification email
            Hey {user}!\nWelcome to FRIO MX, to start using our betting service you must verify your email.
            Enter this code in the application to verify yourself:\n{code}
            """
        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(ec.email, ec.password)
        server.sendmail(ec.email, email, message)
        server.quit()
    except:
        print("There was an error when sending the verification email, check your details and try again")

def deposit():
    """Function to add more money to your account"""
    print(f"You currently have ${money} credit, you have the option to buy 4 packages.\n1- $1000 credit\n2- $5000 credit\n3- $10000 credit\n4- $50000 credit")
    e = input("Which package do you want to buy? ")
    while e != "q":
        dumpling = login_info["logins"]
        dumpling = dumpling[log]
        if e == "1":
            dumpling["money"] += 1000
            time.sleep(2)
            print("Authorized transaction")
            return True
        elif e == "2":
            dumpling["money"] += 5000
            time.sleep(2)
            print("Authorized transaction")
            return True
        elif e == "3":
            dumpling["money"] += 10000
            time.sleep(2)
            print("Authorized transaction")
            return True
        elif e == "4":
            dumpling["money"] += 50000
            time.sleep(2)
            print("Authorized transaction")
            return True

def results():
    """Function that shows final results of the matches and pays the won bets"""
    for i in sport_day:
        print(f"Match #{i['numpartido']}:\n{i['team1']} vs {i['team2']}: {i['score1']}-{i['score2']}")

    for i in bets:
        print(f"You bet ${i['monto']} to {i['equipo']} in match #{i['partido']}")
        for r in sport_day:
            if i["partido"] == r["numpartido"]:
                if i["equipo"] == r["team1"]:
                    if r["score1"] > r["score2"]:
                        dif = ((abs(r["stats1"][2] - 100) + 10 )/100) + 1
                        print(f"You won the bet, your team won match #{r['numpartido']}")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]*dif
                        print(f"We've added ${i['monto']*dif} to your account!\n")
                    elif r["team1"] < r["team2"]:
                        print(f"You lost the bet, your team lost match #{r['numpartido']}\n")
                    elif r["team1"] == r["team2"]:
                        print(f"Your team has drawn in match #{r['numpartido']}, your bet will be returned\n")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]
                elif i["equipo"] == r["team2"]:
                    if r["score2"] > r["score1"]:
                        dif = ((abs(r["stats2"][2] - 100) + 10 )/100) + 1
                        print(f"You won the bet, your team won match #{r['numpartido']}")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]*dif
                        print(f"We've added ${i['monto']*dif} to your account!\n")
                    elif r["score2"] < r["score1"]:
                        print(f"You lost the bet, your team lost match #{r['numpartido']}\n")
                    elif r["team1"] == r["team2"]:
                        print(f"Your team has drawn in match #{r['numpartido']}, your bet will be returned\n")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]

def apostar(usuario):
    """Funtion to enter bets on certain matches"""
    global money
    print(f"\n\nWelcome {usuario}")
    e = input("Would you like to bet in any of today's matches? ")
    while e not in "yes no":
        print("Error, invalid answer")
        e = input("Would you like to bet in any of today's matches? ")
    if e == "yes" or e == "y":
        print(f"You have ${money} available to bet")
        f = str(input(f"In which match(es) you want to bet in? (Separate with ',' and without spaces) "))
        f = f.split(",")
        for i in f:
            dumpling = sport_day[int(i)-1]
            print(f"Match #{i}:\n{dumpling['team1']} vs {dumpling['team2']}")
            print("(LOCAL vs VISITING)")
            r = input("Which team are you betting on? ")
            if r == "VISITING" or r == "visiting" or r == "v":
                g = int(input(f"How much are you betting for {dumpling['team2']}? "))
                while g > money:
                    print("You can't bet more money than you have, try a lower bet.")
                    e = input("Would you like to add more credit to your account? ")
                    while e not in "yes no":
                        print("Error, invalid answer")
                        e = input("Would you like to add more credit to your account? ")
                    
                    if e == "yes" or e == "y":
                        deposit()
                        break
                    elif e == "no" or e == "n":
                        print("It's impossible to submit the bet\n")
                    g = int(input(f"How much are you betting for {dumpling['team2']}? "))
                r = input(f"Are you sure you want to bet ${g} for {dumpling['team2']} in match #{i}? ")
                if r == "yes" or r == "y":
                    print("Bet submitted")
                    bets.append({"equipo": dumpling['team2'], "monto": g, "partido": i})
                    dumpling = login_info["logins"]
                    dumpling = dumpling[log]
                    dumpling["money"] -= g
                else:
                    pass
            elif r == "LOCAL" or r == "local" or r == "l":
                g = int(input(f"How much are you betting for {dumpling['team1']}? "))
                while g > money:
                    print("You can't bet more money than you have, try a lower bet.")
                    e = input("Would you like to add more credit to your account? ")
                    if e == "yes" or e == "y":
                        deposit()
                        break
                    else:
                        break
                    g = int(input(f"How much are you betting for {dumpling['team1']}? "))
                r = input(f"Are you sure you want to bet ${g} for {dumpling['team1']} in match #{i}? ")
                if r == "yes" or r == "y":
                    print("Bet submitted")
                    bets.append({"equipo": dumpling['team1'], "monto": g, "partido": i})
                    dumpling = login_info["logins"]
                    dumpling = dumpling[log]
                    dumpling["money"] -= g
                else:
                    pass
    elif e == "no" or e == "n":
        f = input("Would you like to see all the game results? ")
        while f not in "si no":
            print("Error, invalid answer")
            f = input("Would you like to see all the game results? ")
        if f == "yes" or f == "y":
            return True
        elif f == "no" or f == "n":
            exit()


def login():
    """Login with user and password or create a new account"""
    global user, money, log
    dumpling = login_info["logins"]
    e = input("Already have a FRIO MX account? ")
    while e not in "yes no":
        print("Error, invalid answer")
        e = input("Already have a FRIO MX account? ")

    if e == "yes" or e == "y":
        e = input("Enter your user: ")
        f = input("Enter your password: ")
        for i in dumpling:
            if i["user"] == e and i["password"] == f:
                user = i["user"]
                money = i["money"]
                log = dumpling.index(i)
                return True
    elif e == "no" or e == "n":
        e = input("Would you like to create a new account? ")
        while e not in "yes no":
            print("Error, invalid answer")
            e = input("Would you like to create a new account? ")
        if e == "yes" or e == "s":
            f = ""
            g = " "
            r = ""
            while f != g:
                for i in dumpling:
                    if i["user"] == e:
                        print("Error, username is already in use")
                r = input("Enter your email: ")
                for i in dumpling:
                    if i["correo"] == r:
                        print("Error, email already in use")
                e = input("Enter your new user: ")
                f = input("Enter your new password: ")
                g = input("Repeat your password: ")
                if f != g:
                    print("Error, passwords don't match")
            dumpling.append({"user": e, "password": f, "perms": 0, "money": 0, "correo": r})
            correo_verif(dumpling[-1]["correo"])
            print("We sent you a verification email")
            le = input("Enter the code you received: ")
            conta = 0
            if le == code:
                login()
            else:
                print("Error, incorrect verification code, try again")
                dumpling.pop()
        elif e == "no" or e == "n":
            return False
    with open(path + r"\src\logins.json","w") as login_data:
                json.dump(login_info, login_data)
    
def finalizar_ciclo_fut(partidos_jugados):
    """This function does tweaks in team stats depending on its performance in past matches (Only for football)"""
    dumpling = statsfut["equipos"]
    dumpling = dumpling[0]
    for i in partidos_jugados:
        if i["score1"] > i["score2"]:
            dumpling[i["team1"]][2] += random.randint(1,3)
            dumpling[i["team2"]][2] -= random.randint(2,5)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team1"]]
            estadisticas2 = dumpling[i["team2"]]
            dif = i["score1"] - i["score2"] + 1
            if aleatorio == 1:
                estadisticas1[1] += random.randint(1,3)
                estadisticas2[1] -= random.randint(1,dif)
            elif aleatorio == 0:
                estadisticas1[0] += random.randint(1,3)
                estadisticas2[0] -= random.randint(1,dif)
            
        elif i["score1"] < i["score2"]:
            dumpling[i["team2"]][2] += random.randint(1,3)
            dumpling[i["team1"]][2] -= random.randint(2,5)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team2"]]
            estadisticas2 = dumpling[i["team1"]]
            dif = i["score2"] - i["score1"] + 1
            if aleatorio == 1:
                estadisticas1[1] += random.randint(1,3)
                estadisticas2[1] -= random.randint(1,dif)
            elif aleatorio == 0:
                estadisticas1[0] += random.randint(1,3)
                estadisticas2[0] -= random.randint(1,dif)
        elif i["score1"] == i["score2"]:
            dumpling[i["team2"]][2] -= random.randint(1,4)
            dumpling[i["team1"]][2] -= random.randint(1,4)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team2"]]
            estadisticas2 = dumpling[i["team1"]]
            if aleatorio == 1:
                estadisticas1[1] -= random.randint(1,3)
                estadisticas2[1] -= random.randint(1,3)
            elif aleatorio == 0:
                estadisticas1[0] -= random.randint(1,3)
                estadisticas2[0] -= random.randint(1,3)

    for i in dumpling.values():
        for f in i:
            if f > 100:
                r = i.index(f)
                i[r] = 100
            if f < 0:
                r = i.index(f)
                i[r] = 0
    
    with open(path + r"\src\fut.json","w") as file:
        json.dump(statsfut, file)

def finalizar_ciclo_basq(partidos_jugados):
    """This function does tweaks in team stats depending on its performance in past matches (Only for basketball)"""
    dumpling = statsbasq["equipos"]
    dumpling = dumpling[0]
    for i in partidos_jugados:
        if i["score1"] > i["score2"]:
            dumpling[i["team1"]][2] += random.randint(1,3)
            dumpling[i["team2"]][2] -= random.randint(2,5)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team1"]]
            estadisticas2 = dumpling[i["team2"]]
            dif = i["score1"] - i["score2"] + 1
            if aleatorio == 1:
                estadisticas1[1] += random.randint(1,3)
                estadisticas2[1] -= random.randint(1,dif)
            elif aleatorio == 0:
                estadisticas1[0] += random.randint(1,3)
                estadisticas2[0] -= random.randint(1,dif)
            
        elif i["score1"] < i["score2"]:
            dumpling[i["team2"]][2] += random.randint(1,3)
            dumpling[i["team1"]][2] -= random.randint(2,5)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team2"]]
            estadisticas2 = dumpling[i["team1"]]
            dif = i["score2"] - i["score1"] + 1
            if aleatorio == 1:
                estadisticas1[1] += random.randint(1,3)
                estadisticas2[1] -= random.randint(1,dif)
            elif aleatorio == 0:
                estadisticas1[0] += random.randint(1,3)
                estadisticas2[0] -= random.randint(1,dif)
        elif i["score1"] == i["score2"]:
            dumpling[i["team2"]][2] -= random.randint(1,4)
            dumpling[i["team1"]][2] -= random.randint(1,4)
            aleatorio = random.randint(0,2)
            estadisticas1 = dumpling[i["team2"]]
            estadisticas2 = dumpling[i["team1"]]
            if aleatorio == 1:
                estadisticas1[1] -= random.randint(1,3)
                estadisticas2[1] -= random.randint(1,3)
            elif aleatorio == 0:
                estadisticas1[0] -= random.randint(1,3)
                estadisticas2[0] -= random.randint(1,3)

    for i in dumpling.values():
        for f in i:
            if f > 100:
                r = i.index(f)
                i[r] = 100
            if f < 0:
                r = i.index(f)
                i[r] = 0
    
    with open(path + r"\src\basq.json","w") as file:
        json.dump(statsbasq, file)

def score_basq(team1, team2):
    """Function to emulate whenever a team scores (Only for basketball)"""
    prob1 = 0
    prob2 = 0
    if team1[0] > team2[1]:
        prob1 += random.randint(30,41)
    elif team1[0] == team2[1]:
        prob1 += random.randint(10,21)
    elif team1[0] < team2[1]:
        prob1 += random.randint(8,10)
    
    if team2[0] > team1[1]:
        prob2 += random.randint(30,41)
    elif team2[0] == team1[1]:
        prob2 += random.randint(10,21)
    elif team2[0] < team1[1]:
        prob2 += random.randint(8,10)

    aleatorio = random.randint(0,71)
    if prob1 >= aleatorio and prob2 >= aleatorio:
        if prob1 > prob2:
            return 2, 0
        elif prob2 > prob1:
            return 0, 2
        elif prob1 == prob2:
            return [random.randint(0,3), random.randint(0,3)]
    
    elif prob1 < aleatorio and prob2 < aleatorio:
        return 0, 0
    elif prob1 >= aleatorio and prob2 < aleatorio:
        return 3, 0
    elif prob2 >= aleatorio and prob1 < aleatorio:
        return 0, 3
    else:
        return 0, 0

def score_fut(team1, team2):
    """Function to emulate whenever a team scores (Only for football)"""
    prob1 = 0
    prob2 = 0
    if team1[0] > team2[1]:
        prob1 += random.randint(15,30)
    elif team1[0] == team2[1]:
        prob1 += random.randint(5,11)
    elif team1[0] < team2[1]:
        prob1 += random.randint(0,8)
    
    if team2[0] > team1[1]:
        prob2 += random.randint(15,30)
    elif team2[0] == team1[1]:
        prob2 += random.randint(5,11)
    elif team2[0] < team1[1]:
        prob2 += random.randint(0,8)
    
    aleatorio = random.randint(0,101)
    if prob1 >= aleatorio and prob2 >= aleatorio:
        if prob1 >= prob2:
            return 1, 0
        elif prob2 >= prob1:
            return 0, 1
        elif prob1 == prob2:
            return [random.randint(0,2), random.randint(0,2)]

    elif prob1 < aleatorio and prob2 < aleatorio:
        return 0, 0
    elif prob1 >= aleatorio and prob2 < aleatorio:
        return 1, 0
    elif prob2 >= aleatorio and prob1 < aleatorio:
        return 0, 1
    else:
        return 0, 0

def team_selection(team_list):
    """Function that creates random matches based on available teams"""
    team_dict = team_list[0]
    count = len(team_dict.keys())
    team_dictt = []
    for i in team_dict.keys():
        team_dictt.append(i)
    selected_teams = []
    for f in range(count*60//100):
        selection = random.randint(0,count-1)
        selected_teams.append(team_dictt[selection])
    for i in selected_teams:
        if selected_teams.count(i) >= 2:
            if selected_teams.index(i) % 2 == 0:
                selected_teams.pop(selected_teams.index(i)+1)
                selected_teams.remove(i)
            else:
                selected_teams.pop(selected_teams.index(i)-1)
                selected_teams.remove(i)
    return selected_teams

def partido_basq(equipo1, equipo2):
    """Emulates a match between two teams (Only for basketball)"""
    global cont
    dumpling = statsbasq["equipos"]
    dumpling = dumpling[0]
    team1 = dumpling[equipo1]
    team2 = dumpling[equipo2]
    scoretotal1 = 0
    scoretotal2 = 0
    scores = []
    for i in range(random.randint(80, 91)):
        score1, score2 = score_basq(team1, team2)
        scoretotal1 += score1
        scoretotal2 += score2
    cont += 1
    scoretotal1 += random.randint(10,32)
    scoretotal2 += random.randint(10,32)
    dif = abs(scoretotal1 - scoretotal2)
    if dif >= 50:
        if scoretotal1 > scoretotal2:
            scoretotal1 -= random.randint(10,21)
            scoretotal2 += random.randint(20,41)
        elif scoretotal2 > scoretotal1:
            scoretotal2 -= random.randint(10,21)
            scoretotal1 += random.randint(20,41)

    scores.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2})
    print(f"Match #{cont}:\n{equipo1}: {team1[2]} vs {equipo2}: {team2[2]}")
    sport_day.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2, "numpartido": str(cont)})
    return scores

def partido_fut(equipo1, equipo2):
    """Emulates a match between two teams (Only for football)"""
    global cont
    dumpling = statsfut["equipos"]
    dumpling = dumpling[0]
    team1 = dumpling[equipo1]
    team2 = dumpling[equipo2]
    scoretotal1 = 0
    scoretotal2 = 0
    scores = []
    for i in range(random.randint(10,21)):
        score1, score2 = score_fut(team1, team2)
        scoretotal1 += score1
        scoretotal2 += score2
    cont += 1
    scores.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2})
    print(f"Match #{cont}:\n{equipo1}: {team1[2]} vs {equipo2}: {team2[2]}")
    sport_day.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2, "numpartido": str(cont)})
    return scores

def main():
    with open(path + r"\src\fut.json","r") as file:
        statsfut = json.load(file)
    with open(path + r"\src\basq.json", "r") as archivo:
        statsbasq = json.load(archivo)
    with open(path + r"\src\logins.json","r") as login_data:
        login_info = json.load(login_data)
    if login():
        e = input("Which sport would you like to see? ")
        while e not in "football basketball":
            print("Error, invalid answer")
            e = input("Which sport would you like to see? ")
        if e in "football":
            teams = team_selection(statsfut["equipos"])
            for i in teams:
                if teams.index(i) % 2 == 0:
                    ind1 = teams.index(i)
                    ind2 = int(teams.index(i))+1
                    
                    partidos_jugados = partido_fut(teams[ind1], teams[ind2])
                    finalizar_ciclo_fut(partidos_jugados)
            apostar(user)
            time.sleep(5)
            results()
        elif e in "basketball":
            teams = team_selection(statsbasq["equipos"])
            for i in teams:
                if teams.index(i) % 2 == 0:
                    ind1 = teams.index(i)
                    ind2 = int(teams.index(i))+1

                    partidos_jugados = partido_basq(teams[ind1], teams[ind2])
                    finalizar_ciclo_basq(partidos_jugados)
            apostar(user)
            time.sleep(5)
            results()
    else:
        print("Access denied")

#END OF DEBUGGING
#START OF GUI
import itertools
from tkinter import *
from PIL import ImageTk, Image
from time import *

images = ["mainpage1.jpg", "mainpage2.jpg", "mainpage3.jpg", "mainpage4.jpg"]
images = itertools.cycle(images)
window = ""
username = ""
password = ""
email = ""
sec_password = ""
verif = ""
mainpage = False
#For mainpage ->
soccer = team_selection(statsfut["equipos"])
basket = team_selection(statsbasq["equipos"])
games_played = partido_fut(soccer[0], soccer[1])
games_played2 = partido_basq(basket[0], basket[1])

def about_page():
    """About FRIO MX page, where the user will find how to use FRIO MX software"""
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    window.title("About FRIO MX")
    with open(path + r"\src\about.txt") as file:
        message = file.read()
    Label(window, text=message, font=("Courier", 13)).place(x=20, y=0)
    Button(window, text="Back", command=reload_gui).place(x=490, y=590)

def fut_page():
    """Mainpage for betting in football matches"""
    global soccer
    cont = 1
    conta = 0
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    fut_matches = []
    for i in soccer:
        if soccer.index(i) % 2 == 0:
            ind1 = soccer.index(i)
            ind2 = int(soccer.index(i))+1

            fut_matches.append(partido_fut(soccer[ind1], soccer[ind2])[0])
            #finalizar_ciclo_fut(partidos_jugados)

    for i in fut_matches:
        if cont % 2 == 0:
            Label(window, text=f"{i['team1']}", font=("Courier", 10)).place(x=280, y=100+conta)
            Label(window, text=f"{i['team2']}", font=("Courier", 10)).place(x=280, y=135+conta)
            Label(window, text="VS", font=("Courier", 10)).place(x=300, y=117+conta)
            Button(window, text="Bet in this match").place(x=350, y=110+conta)
            cont += 1
            conta += 100
        else:
            Label(window, text=f"{i['team1']}", font=("Courier", 10)).place(x=0, y=100+conta)
            Label(window, text=f"{i['team2']}", font=("Courier", 10)).place(x=0, y=135+conta)
            Label(window, text="VS", font=("Courier", 10)).place(x=20, y=117+conta)
            Button(window, text="Bet in this match").place(x=130, y=110+conta)
            cont += 1

def verif_code():
    """Checks the code sent via email to verify an account"""
    global code, verif
    if code == verif.get():
        mainpage()
    else:
        Label(window, text="Incorrect code, terminating session").place(x=100, y=100)
        sleep(2)
        window.destroy()

def gui_email_verif():
    global code, email, username, verif
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    dumpling = login_info["logins"]
    verif = StringVar()
    try:
        for i in range(6):
            piece_of_code = str(random.randint(0,10))
            code = code + piece_of_code
        message = f"""Subject: Verification code

            Hey {username.get()}!\nWelcome to FRIO MX, to start using our betting service you must verify your email.
            Enter this code in the application to verify yourself:\n{code}
            """
        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(ec.email, ec.password)
        server.sendmail(ec.email, email.get(), message)
        server.quit()
    except:
        Label(window, text="There was an error when sending the verification email, check your details and try again").place(x=0, y=0)
        sleep(4)
        dumpling.pop()
        window.destroy()
    else:
        Label(window, text="We sent you a verification email,", font=("Courier", 16)).place(x=0, y=0)
        Label(window, text="type in the code to verify your account:", font=("Courier", 16)).place(x=0, y=35)
        Entry(window, width=30, textvariable=verif).place(x=175, y=100)
        Button(window, text="Submit",command=verif_code, font="Courier").place(x=220, y=200)

def next_img():
    """Iterate through the mainpage images"""
    global mainpage, soccer, basket, games_playes, games_played2
    if mainpage == True:
        panel = Label(window,width= 540, height= 500)
        panel.place(x=0, y= 130)
        try:
            img = next(images)
        except StopIteration:
            pass
        else:
            img = Image.open(path + r"\media\\" + img)
            img = ImageTk.PhotoImage(img)
            panel.img = img
            panel['image'] = img
            window.update()
            Label(window, text="Select the sport you want to bet in", font=("Courier", 18)).place(x=0, y=390, height=50, width=540)
            Button(window, text="Football (Soccer)", command=fut_page).place(x=0, y=440, height=60, width=270)
            Button(window, text="Basketball").place(x=0, y=500, height=60, width=270)
            Button(window, text="Tennis (Coming soon)").place(x=0, y=560, height=60, width=270)
            Canvas(window).place(x=270, y=440, height=180, width=270)
            dumpling = games_played[0]
            Label(window, text=f"{dumpling['score1']} - {dumpling['score2']}", font=("Courier", 16)).place(x=340, y=455)
            Label(window, text=f"{dumpling['team1']}", font=("Courier", 10)).place(x=280, y=438)
            Label(window, text=f"{dumpling['team2']}", font=("Courier", 10)).place(x=400, y=477)
            dumpling = games_played2[0]
            Label(window, text=f"{dumpling['score1']} - {dumpling['score2']}", font=("Courier", 16)).place(x=340, y=515)
            Label(window, text=f"{dumpling['team1']}", font=("Courier", 10)).place(x=280, y=498)
            Label(window, text=f"{dumpling['team2']}", font=("Courier", 10)).place(x=400, y=537)
            Button(window, text="About FRIO MX", command=about_page).place(x=445, y=360)
    else:
        panel = Label(window,width= 540, height= 500)
        panel.place(x=0, y= 130)
        try:
            img = next(images)
        except StopIteration:
            pass
        else:
            img = Image.open(path + r"\media\\" + img)
            img = ImageTk.PhotoImage(img)
            panel.img = img
            panel['image'] = img
            Button(window, text="About FRIO MX", command=about_page).place(x=445, y=590)
            window.update()

def mainpage():
    """Mainpage of FRIO MX"""
    global money, username, mainpage, soccer, basket, games_played, games_played2
    mainpage = True
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    window.geometry("540x620")
    window.title("FRIO MX")
    window.resizable(0, 0)
    Label(window, text="Welcome", font=("Courier", 20)).place(x=30, y=0)
    Label(window, text=f"{username.get()}", font=("Courier", 20)).place(x=160, y=0)
    Label(window, text="to", font=("Courier", 20)).place(x=50, y=75)
    Label(window, text="FRIO MX", font=("Courier", 60)).place(x=110, y=35)
    Label(window, text=f"Your balance is ${money}", font=("Courier", 8)).place(x=365, y=0)
    Button(text='>', command=next_img).place(x=505, y=90)
    next_img()
    Label(window, text="Select the sport you want to bet in", font=("Courier", 18)).place(x=0, y=390, height=50, width=540)
    Button(window, text="Football (Soccer)", command=fut_page).place(x=0, y=440, height=60, width=270)
    Button(window, text="Basketball").place(x=0, y=500, height=60, width=270)
    Button(window, text="Tennis (Coming soon)").place(x=0, y=560, height=60, width=270)
    Canvas(window).place(x=270, y=440, height=180, width=270)
    dumpling = games_played[0]
    Label(window, text=f"{dumpling['score1']} - {dumpling['score2']}", font=("Courier", 16)).place(x=340, y=455)
    Label(window, text=f"{dumpling['team1']}", font=("Courier", 10)).place(x=280, y=438)
    Label(window, text=f"{dumpling['team2']}", font=("Courier", 10)).place(x=400, y=477)
    dumpling = games_played2[0]
    Label(window, text=f"{dumpling['score1']} - {dumpling['score2']}", font=("Courier", 16)).place(x=340, y=515)
    Label(window, text=f"{dumpling['team1']}", font=("Courier", 10)).place(x=280, y=498)
    Label(window, text=f"{dumpling['team2']}", font=("Courier", 10)).place(x=400, y=537)
    Button(window, text="About FRIO MX", command=about_page).place(x=445, y=360)

def check_create_acc():
    """Double check if all the user details are valid and doesn't overlap other users information"""
    global username, password, email, sec_password
    dumpling = login_info["logins"]
    flag1, flag2, flag3 = False, False, False
    for i in dumpling:
        if username.get() == i["user"]:
            label = Label(window, text="Username already in use")
            label.place(x=190, y=220)
            window.update()
            sleep(2)
            label.config(text="")
            flag1 = False
        else:
            flag1 = True
        if password.get() != sec_password.get():
            label = Label(window, text="Passwords aren't matching")
            label.place(x=190, y=220)
            window.update()
            sleep(2)
            label.config(text="")
            flag2 = False
        else:
            flag2 = True
        if email.get() == i["correo"] or email.get() == "":
            label = Label(window, text="Email already in use")
            label.place(x=190, y=220)
            window.update()
            sleep(2)
            label.config(text="")
            flag3 = False
        else:
            flag3 = True
    if flag1 and flag2 and flag3:
        dumpling.append({"user": username.get(), "password": password.get(), "perms": 0, "money": 0, "correo": email.get()})
        gui_email_verif()

def check_login():
    """Checks if login credentials are valid -not working"""
    global money, user, log, username, password
    user = username.get()
    passw = password.get()
    dumpling = login_info["logins"]
    for i in dumpling:
            if i["user"] == user and i["password"] == passw:
                user = i["user"]
                money = i["money"]
                log = dumpling.index(i)
                mainpage()
    return False

def reload_gui():
    """Reloads the mainpage"""
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    window.geometry("540x620")
    window.title("FRIO MX")
    window.resizable(0, 0)
    Button(window, text="Login", bg="#4ea9bf", width=13, command=gui_login).place(x=342, y=0)
    Button(window, text="Create an account", bg="#50a82a", command=gui_create_acc).place(x=433, y=0)
    Label(window, text="Welcome to FRIO MX", font=("Courier", 32)).place(x=35, y=40)
    Button(text='>', command=next_img).place(x=515, y=50)
    next_img()

def gui_create_acc():
    """Create a new account with GUI"""
    global email, username, password, sec_password
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    window.geometry("540x310")
    window.title("Create a new account")
    email = StringVar()
    username = StringVar()
    password = StringVar()
    sec_password = StringVar()
    Entry(window, textvariable=email, width= 30).place(x=40, y=100)
    Entry(window, textvariable=username, width= 30).place(x=40, y=200)
    Entry(window, textvariable=password, width= 30).place(x=300, y=100)
    Entry(window, textvariable=sec_password, width= 30).place(x=300, y=200)
    Label(window, text="Create a new FRIO MX account!", font=("Courier", 22)).place(x=21,y=0)
    Label(window, text="Email:", font=("Courier", 18)).place(x=40, y=60)
    Label(window, text="New username:", font=("Courier",18)).place(x=40, y=160)
    Label(window, text="Password:", font=("Courier", 18)).place(x=300, y=60)
    Label(window, text="Repeat password:", font=("Courier", 18)).place(x=300, y=160)
    Button(window, text="Create account", font=("Courier", 8), command=check_create_acc).place(x=208, y=250)
    Button(window, text="Back", font=("Courier", 8), command=reload_gui).place(x=10, y=280)

def gui_login():
    """Login into your account with GUI"""
    global username, password
    Canvas(window, width= 1000, height= 1000).place(x=0, y=0)
    window.geometry("540x310")
    window.title("Log in")
    username = StringVar()
    password = StringVar()
    Entry(window, textvariable=username, width= 30).place(x=170, y=100)
    Entry(window, textvariable=password, width= 30).place(x=170, y=180)
    Label(window, text="Log into your FRIO MX account", font=("Courier", 20)).place(x=38, y=0)
    Label(window, text="Username:", font=("Courier", 18)).place(x=170, y=60)
    Label(window, text="Password:", font=("Courier", 18)).place(x=170, y=140)
    Button(window, text="Log in", font=("Courier", 10), command=check_login).place(x=235, y=230)
    Button(window, text="Back", font=("Courier", 8), command=reload_gui).place(x=10, y=280)

def gui():
    """Principal graphic interface configuration"""
    global window
    window = Tk()
    window.geometry("540x620")
    window.title("FRIO MX")
    window.resizable(0, 0)
    Button(window, text="Login", bg="#4ea9bf", width=13, command=gui_login).place(x=342, y=0)
    Button(window, text="Create an account", bg="#50a82a", command=gui_create_acc).place(x=433, y=0)
    Label(window, text="Welcome to FRIO MX", font=("Courier", 32)).place(x=35, y=40)
    Button(text='>', command=next_img).place(x=515, y=50)
    next_img()
    window.mainloop()

if debug:
    main()
else:
    gui()


with open(path + r"\src\fut.json","w") as file:
    json.dump(statsfut, file)
with open(path + r"\src\basq.json", "w") as archivo:
    json.dump(statsbasq, archivo)
with open(path + r"\src\logins.json","w") as login_data:
    json.dump(login_info, login_data)
