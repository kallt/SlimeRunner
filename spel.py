import pgzrun                               #Importerar pygame-zero library för att skapa och köra spelet
import random                               #Importerar random-library som jag använder senare för att slumpmässa fiendens position.

WIDTH = 640                                 #Spelfönstrets bredd och höjd
HEIGHT = 480

ground = HEIGHT - 100                       #Position för marken i spelet (platformens position)

#Här skapar jag bakgrunds och platformsbilder och centrerar de i mitten av spelskärmen
background1 = Actor("background1", (WIDTH/2, HEIGHT/2))                 
background2 = Actor("background2", (WIDTH/2, HEIGHT/2))
platform = Actor("platform", (WIDTH/2, ground + 50))

#Koden skapar spelare och fiende och anger deras startposition
player = Actor("player", (100, ground))
enemy = Actor("enemy", (WIDTH, ground))

#Här initialiserar jag spelets fysik och statusvariabler
gravity = 0.8           #här sätter jag ''gravitationen'' som kommer påverka spelaren
speed = 0               #Speed kommer styra spelarens vertikala hastighet
difficulty = 8          #Difficulty styr fiendens hstighet
points = 0              #Poängräknare
game_over = False       #Indikerar om spelet är över
player_ducks = False    #indikerar om spelaren duckar

#Funktionen draw ska rita alla spelobjekt på skärmen, inuti så har jag metoder som används senare av objekten
def draw():
    background1.draw()                  #Ska rita bakgrund 1 och 2
    background2.draw()          
    platform.draw()                     #Här ritar man ut ''marken'' som gör spelet lite ''snyggare'' för användaren
    player.draw()                       #Ritar spel karaktären 
    enemy.draw()                        #Ritar fienden
    screen.draw.text(str(int(points)), center=(WIDTH/2, 100), fontsize = 40, color = (0,0,0))       #Visar poängen i mitten av skärmen, jag har justerade text storleken och färgen

#Funktion som uppdaterar spelets logik vid varje bildruta
def update():
    global game_over                    #Här användar jag global för att referera till game_over variabeln som är definerad utanför funktionen
    if not game_over:                   #If statement som ska updatera spelarens och fiendes rörelser, samt svårighetsgraden (difficulty) medans spelet inte är över
        update_player()
        update_enemy()
        update_difficulty()
    else:                               #Else statment som ska ändra spelarens bild till en ''död'' bild ifall spelet är över
        player.image = "player_dead"

    if player.colliderect(enemy):       #if statment som använder en inbyggd funktion (colliderect) i pygame som märker om spelare och fiende krokar
        game_over = True                #Om förgående konditionen uppfylls så avslutas spelet

#Funktion som uppdaterar spelets svårighetsgrad baserat på poängen
def update_difficulty():
    global difficulty
    if points < 100:
        difficulty = 8
    elif points < 200:
        difficulty = 12
    elif points < 300:
        difficulty = 14
    else:
        difficulty = 16

#Funktion som uppdaterar fiendens position och hanterar poängräkning
def update_enemy():
    global points
    enemy.x -= difficulty               #Justerar hur hastigheten, hur snabbt fienden rör sig beroende på svårighetsgraden
    enemy.angle += 1                    #Roterar fienden som skapar lite mer ''animation'' än en statisk fiende
    if enemy.x  < 0:                    #if statment som kollar om fienden rör sig utanför skärmen
        enemy.x = WIDTH                 #Om konditionen över uppfylls så ''spawnar'' fienden igen från högerkanten
        points += 10                    #Spelarens poäng ökar också med 10
        enemy.y = random.choice([ground, ground -40])           #Här användar jag random för att slumpmässigt välja fiendens startposition 

#Funktion som uppdaterar spelarens position och hanterar spelarens bild beroende på dess rörelse
def update_player():
    global speed
    if speed > 0:                       #Om spelarens faller så ändras bilden
        player.image = "player_falls"           
    elif speed < 0:                     #Om spelaren hoppas så ändras bilden 
        player.image = "player_jumps"
    elif player_ducks:                  #Om spelaren duckar så ändras bilden
        player.image = "player_ducks" 
    else:                               #Om spelaren är stationär och inte gör något så används en standard bild
        player.image = "player" 

    player.y += speed                   #Kod som ska ''animera'' ett hopp, spelarens vertikala postion ändras baserat på hastighet 
    speed += gravity                    #lägger till gravitation till hastigheten så att spelaren kan falla

    if player.y > ground:               #if statment som kollar om spelarens position är vid ground 
        speed = 0                       #Nollställer hastigheten så att spelaren inte faller igenom spelskärmen

#Funktion som hanterar tangettryckningar så att spelaren kan kontrollera jump och duck
def on_key_down(key):
    global speed, player_ducks
    if key == keys.SPACE and speed == 0 and not player_ducks:               #If statment som kollar om 'space' knappen är nertryckt, hastigheten är noll och om spelaren inte duckar 
        speed = -12                                                         #Spelaren får då "negativ" hastighet vilket representerar ett hopp i spelet
    if key == keys.DOWN and speed == 0:                                     #If som kollar om 'neråt' knappen är nertryck och hastigheten är noll
        player_ducks = True                                                 #Bilden och positionen för spelaren ändras
        player.y += 20

#Funktion som ska hanterar tangetknappens uppsläpp
def on_key_up(key):
    global player_ducks
    if key == keys.DOWN and player_ducks: 
        player_ducks = False                                                #Slutar ducka när nedåt pilen släpps
        player.y -= 20                                                      #Flyttar tillbaka spelare till standard positionen

pgzrun.go()     #startar spelet