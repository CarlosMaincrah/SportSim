import json
import random
import time
import os
from smtplib import SMTP

path = os.path.dirname(os.path.abspath(__file__))

#"EQUIPO": [ATACK, DEFENSE, REPUTATION]
with open(path + r"\fut.txt","r") as file:
    statsfut = json.load(file)
with open(path + r"\basq.txt", "r") as archivo:
    statsbasq = json.load(archivo)
with open(path + "\logins.txt","r") as login_data:
    login_info = json.load(login_data)

jornada = []
user = ""
money = 0
cont = 0
log = 0
apuesta = []
code = ""

def correo_verif(correo):
    """Función para mandar un correo de verificación a la hora de crear una cuenta"""
    global code, user
    try:
        for i in range(6):
            pedazo = str(random.randint(0,10))
            code = code + pedazo
        username = 'kaveskydimitri@gmail.com'
        password = 'trojandick42'
        message = f"""Subject: Correo de verificacion
Hola {user}!\nBienvenido a FRIO MX, para comenzar a usar nuestro servicio de apuestas debes verificar tu correo electronico.
Ingresa este codigo en la aplicacion para verificarte:\n{code}
"""
        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(username, correo, message)
        server.quit()
    except:
        print("Hubo un error al enviar el correo para verificar tu correo electrónico, revisa tus datos y vuelve a intentarlo")

def deposito():
    """Función para ingresar más dinero a tu cuenta"""
    print(f"Actualmente tienes {money} de crédito, tienes opción de comprar 4 paquetes.\n1- 1000 créditos\n2- 5000 créditos\n3- 10000 créditos\n4- 50000 créditos")
    e = input("¿Qué paquete deseas comprar? ")
    while e != "q":
        dumpling = login_info["logins"]
        dumpling = dumpling[log]
        if e == "1":
            dumpling["money"] += 1000
            time.sleep(2)
            print("Transacción autorizada")
            return True
        elif e == "2":
            dumpling["money"] += 5000
            time.sleep(2)
            print("Transacción autorizada")
            return True
        elif e == "3":
            dumpling["money"] += 10000
            time.sleep(2)
            print("Transacción autorizada")
            return True
        elif e == "4":
            dumpling["money"] += 50000
            time.sleep(2)
            print("Transacción autorizada")
            return True

def results():
    """Función que da resultados de los partidos y paga las apuestas ganadas"""
    for i in jornada:
        print(f"Partido #{i['numpartido']}:\n{i['team1']} vs {i['team2']}: {i['score1']}-{i['score2']}")

    for i in apuesta:
        print(f"Has apostado {i['monto']} por {i['equipo']} en el partido #{i['partido']}")
        for r in jornada:
            if i["partido"] == r["numpartido"]:
                if i["equipo"] == r["team1"]:
                    if r["score1"] > r["score2"]:
                        dif = ((abs(r["stats1"][2] - 100) + 10 )/100) + 1
                        print(f"Has ganado tu apuesta, tu equipo ganó el partido #{r['numpartido']}")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]*dif
                        print(f"Hemos añadido {i['monto']*dif} a tu cuenta!\n")
                    elif r["team1"] < r["team2"]:
                        print(f"Has perdido tu apuesta, tu equipo perdió el partido #{r['numpartido']}\n")
                    elif r["team1"] == r["team2"]:
                        print("Tu equipo ha empatado en el partido, se te devolverá tu apuesta\n")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]
                elif i["equipo"] == r["team2"]:
                    if r["score2"] > r["score1"]:
                        dif = ((abs(r["stats2"][2] - 100) + 10 )/100) + 1
                        print(f"Has ganado tu apuesta, tu equipo ganó el partido #{r['numpartido']}")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]*dif
                        print(f"Hemos añadido {i['monto']*dif} a tu cuenta!\n")
                    elif r["score2"] < r["score1"]:
                        print(f"Has perdido tu apuesta, tu equipo perdió el partido #{r['numpartido']}\n")
                    elif r["team1"] == r["team2"]:
                        print("Tu equipo ha empatado en el partido, se te devolverá tu apuesta\n")
                        dumpling = login_info["logins"]
                        dumpling = dumpling[log]
                        dumpling["money"] += i["monto"]

def apostar(usuario):
    """Función para ingresar apuestas a ciertos equipos"""
    global money
    print(f"\n\nBienvenido {usuario}")
    e = input("¿Deseas apostar en algún partido de la jornada? ")
    while e not in "si no":
        print("Error, respuesta inválida")
        e = input("¿Deseas apostar en algún partido de la jornada? ")
    if e == "si" or e == "s":
        print(f"Tienes {money} de crédito para apostar")
        f = str(input(f"¿En qué partido(s) deseas apostar?(Separar con ',' y sin espacios) "))
        f = f.split(",")
        for i in f:
            dumpling = jornada[int(i)-1]
            print(f"Partido #{i}:\n{dumpling['team1']} vs {dumpling['team2']}")
            print("(LOCAL vs VISITANTE)")
            r = input("¿A cuál equipo vas a apostar? ")
            if r == "VISITANTE" or r == "visitante" or r == "v":
                g = int(input(f"¿Cuánto apostarás por {dumpling['team2']}? "))
                while g > money:
                    print("No puedes apostar más dinero del que actualmente posees, intente de nuevo.")
                    e = input("¿Deseas depositar más crédito a tu cuenta? ")
                    while e not in "si no":
                        print("Error, respuesta inválida")
                        e = input("¿Deseas depositar más crédito a tu cuenta? ")
                    
                    if e == "si" or e == "s":
                        deposito()
                        break
                    elif e == "no" or e == "n":
                        print("Es imposible completar la apuesta\n")
                    g = int(input(f"¿Cuánto apostarás por {dumpling['team2']}? "))
                r = input(f"¿Estás seguro que deseas apostar {g} por {dumpling['team2']} en el partido #{i}? ")
                if r == "si" or r == "s":
                    print("Apuesta completada")
                    apuesta.append({"equipo": dumpling['team2'], "monto": g, "partido": i})
                    dumpling = login_info["logins"]
                    dumpling = dumpling[log]
                    dumpling["money"] -= g
                else:
                    pass
            elif r == "LOCAL" or r == "local" or r == "l":
                g = int(input(f"¿Cuánto apostarás por {dumpling['team1']}? "))
                while g > money:
                    print("No puedes apostar más dinero del que actualmente posees, intente de nuevo.")
                    e = input("¿Deseas depositar más crédito a tu cuenta? ")
                    if e == "si" or e == "s":
                        deposito()
                        break
                    else:
                        break
                    g = int(input(f"¿Cuánto apostarás por {dumpling['team1']}? "))
                r = input(f"¿Estás seguro que deseas apostar {g} por {dumpling['team1']} en el partido #{i}? ")
                if r == "si" or r == "s":
                    print("Apuesta completada")
                    apuesta.append({"equipo": dumpling['team1'], "monto": g, "partido": i})
                    dumpling = login_info["logins"]
                    dumpling = dumpling[log]
                    dumpling["money"] -= g
                else:
                    pass
    elif e == "no" or e == "n":
        f = input("¿Deseas ver los resultados de la jornada? ")
        while f not in "si no":
            print("Error, respuesta inválida")
            f = input("¿Deseas ver los resultados de la jornada? ")
        if f == "si" or f == "s":
            return True
        elif f == "no" or f == "n":
            exit()


def login():
    """Función para ingresar usuario y contraseña para entrar al programa en modo usuario o superusuario"""
    global user, money, log
    dumpling = login_info["logins"]
    e = input("¿Ya tienes una cuenta de FRIO MX? ")
    while e not in "si no":
        print("Error, respuesta no válida")
        e = input("¿Ya tienes una cuenta de FRIO MX? ")

    if e == "si" or e == "s":
        e = input("Ingresa tu usuario: ")
        f = input("Ingresa tu contraseña: ")
        for i in dumpling:
            if i["user"] == e and i["password"] == f:
                user = i["user"]
                money = i["money"]
                log = dumpling.index(i)
                return True
    elif e == "no" or e == "n":
        e = input("¿Deseas crear una nueva cuenta? ")
        while e not in "si no":
            print("Error, respuesta no válida")
            e = input("¿Deseas crear una nueva cuenta? ")
        if e == "si" or e == "s":
            f = ""
            g = " "
            r = ""
            while f != g:
                for i in dumpling:
                    if i["user"] == e:
                        print("Error, nombre de usuario en uso")
                r = input("Ingresa tu correo electrónico: ")
                if i["correo"] == r:
                        print("Error, correo electrónico en uso")
                e = input("Ingresa tu nuevo usuario: ")
                f = input("Ingresa tu nueva contraseña: ")
                g = input("Reingresa tu contraseña: ")
                if f != g:
                    print("Error, las contraseñas no coinciden")
            dumpling.append({"user": e, "password": f, "perms": 0, "money": 0, "correo": r})
            correo_verif(dumpling[-1]["correo"])
            print("Se te envió un correo para verificar tu cuenta")
            le = input("Ingresa el código enviado: ")
            conta = 0
            if le == code:
                login()
            else:
                print("Error, el código de verificación no coincide")
                dumpling.pop()
        elif e == "no" or e == "n":
            return False
    with open(path + "\logins.txt","w") as login_data:
                json.dump(login_info, login_data)
    
def finalizar_ciclo_fut(partidos_jugados):
    """Esta función hace tweaks a los valores de ataque y defensa de los equipos dependiendo de su rendimiento en los partidos pasados SOLO PARA FUT"""
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
    
    with open(path + r"\fut.txt","w") as file:
        json.dump(statsfut, file)

def finalizar_ciclo_basq(partidos_jugados):
    """Esta función hace tweaks a los valores de ataque y defensa de los equipos dependiendo de su rendimiento en los partidos pasados SOLO PARA BASQ"""
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
    
    with open(path + r"\basq.txt","w") as file:
        json.dump(statsbasq, file)

def canasta(team1, team2):
    """Función para definir que equipo mete canasta o no"""
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

def gol(team1, team2):
    """Función para definir que equipo mete gol o no"""
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
    """Se le pasa una lista con un diccionario con todos los equipos"""
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
    """Genera un score entre dos equipos dependiendo de los traits de cada uno SOLO PARA BASQ"""
    global cont
    dumpling = statsbasq["equipos"]
    dumpling = dumpling[0]
    team1 = dumpling[equipo1]
    team2 = dumpling[equipo2]
    scoretotal1 = 0
    scoretotal2 = 0
    scores = []
    for i in range(random.randint(80, 91)):
        score1, score2 = canasta(team1, team2)
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
    print(f"Partido #{cont}:\n{equipo1}: {team1[2]} vs {equipo2}: {team2[2]}")
    jornada.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2, "numpartido": str(cont)})
    return scores

def partido_fut(equipo1, equipo2):
    """Genera un score entre dos equipos dependiendo de los traits de cada uno SOLO PARA FUT"""
    global cont
    dumpling = statsfut["equipos"]
    dumpling = dumpling[0]
    team1 = dumpling[equipo1]
    team2 = dumpling[equipo2]
    scoretotal1 = 0
    scoretotal2 = 0
    scores = []
    for i in range(random.randint(10,21)):
        score1, score2 = gol(team1, team2)
        scoretotal1 += score1
        scoretotal2 += score2
    cont += 1
    scores.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2})
    print(f"Partido #{cont}:\n{equipo1}: {team1[2]} vs {equipo2}: {team2[2]}")
    jornada.append({"team1": equipo1, "team2": equipo2, "score1": scoretotal1, "score2": scoretotal2, "stats1": team1, "stats2": team2, "numpartido": str(cont)})
    return scores

def main():
    with open(path + r"\fut.txt","r") as file:
        statsfut = json.load(file)
    with open(path + r"\basq.txt", "r") as archivo:
        statsbasq = json.load(archivo)
    with open(path + "\logins.txt","r") as login_data:
        login_info = json.load(login_data)
    if login():
        e = input("¿Qué deporte deseas visualizar? ")
        while e not in "futbol basquetbol":
            print("Error, respuesta no válida")
            e = input("¿Qué deporte deseas visualizar? ")
        if e in "futbol":
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
        elif e in "basquetbol":
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
        print("Acceso denegado")


main()
with open(path + r"\fut.txt","w") as file:
    json.dump(statsfut, file)
with open(path + r"\basq.txt", "w") as archivo:
    json.dump(statsbasq, archivo)
with open(path + "\logins.txt","w") as login_data:
    json.dump(login_info, login_data)
