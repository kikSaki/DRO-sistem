# DRO-sistem
Projekt pri predmetu Vhodno-Izhodne naprave na Fakulteti za Računalništvo in Informatiko


# Uvod
Merilne letve so ključen instrument za natančno merjenje razdalj, višin in drugih dimenzij v različnih industrijskih in aplikativnih kontekstih. Prav tako so v merilnih sistemih pomembni kazalniki pozicij (DRO – Digital Read Out), ki numerično prikazujejo same meritve letve. Ker imam doma eno merilno letev za katero potrebujemo kazalnik pozicij, sem se odločil, da za projekt naredim prav to s pomočjo Arduino mikrokontrolerja.

# Merilne letve
Merilne letve so ključno orodje v različnih industrijah, ki omogočajo natančna merjenja dolžin, višin, širin in drugih dimenzij. Njihova uporabnost sega od gradbeništva do znanstvenih raziskav, kjer so nepogrešljive pri zagotavljanju natančnosti in zanesljivosti meritev.
Njihova zasnova omogoča enostavno uporabo in natančno merjenje, kar je ključno pri številnih aplikacijah, kjer je potrebna natančna dimenzijska analiza.
Glavna tehnologija merjenja je fotoelktrično skeniranje, pri katerem skeniranje zazna izjemno fine črte široke le nekaj mikrometrov. Samo merjenje pa lahko poteka na dva načina. Absolutno, kjer je vrednost položaja na voljo takoj ob vklopu kodirnika in inkrementalno, ki uporablja izhodiščne referenčne točke.
 
Slika 3: Fotoelektrično skeniranje


# Digitalni kazalniki (DRO)
Digitalni kazalniki za merilne letve omogočajo enostavno branje meritev v numerični obliki, kar povečuje uporabnost in natančnost. Merilna letev se z DRO sistemom poveže z RS2332 DB9 ali pa z 12 oz. 7-pinskim konektorjem. Povezovanje z merilno letvijo je običajno enostavno in intuitivno, saj večina proizvajalcev ponuja jasna navodila in uporabniško prijazne aplikacije za upravljanje naprave.
 
DRO sistemi omogočajo več funckij, na tem projektu se bom osredotočil le na nekaj pomembnejših.
 
# Projekt
## Sestavni deli
•	Arduino Mega (po želji tudi drug Arduino) <br />
•	Merilna letev Iskra TELA TGM111 <br />
•	Raspberry Pi 2B ** <br /> 
•	7-palčni Raspberry Pi zaslon ** <br />
**Po želji, saj za delovanje samega DRO sistema ta komponenta ni potrebna
## Povezava Arduino mikrokontrolerja z merilno letvijo
Moja merilna letev za povezavo uporablja 12-pinski konektor. Kljub večjemu številu pinov so za povezavo potrebni le štiri pini. Ostali služijo različnim namenom kot je varnost same naprave.
 
Slika 7: Označeni pini na 12-pinskem konektorju, ki so potrebni za povezavo
Pin B se na Arduino poveže na 5 V, pin K se poveže na GND, pina G in H pa na digitalne pine, v mojem primeru sem jih dal na pin 2 in pin 4.
 
Slika 8: Povezava med merilno letvijo in Arduino mikrokontrolerjem
## Arduino program
Program, ki je potreben za branje podatkov je izjemno preprost.

### Definicija pinov:
#define encoder0PinA  2 
#define encoder0PinB  4

### Inicializacija spremenljivk:
volatile int encoder0Pos = 0; //Pozicija merilne letve
boolean newdata = false; //Ali se je kodirnik premaknil

String input; //Za branje serijske povezave

### Setup:
Funkcijo attachInterrupt uporabimo, da se ob vsaki zaznani spremembi izvede funkcija doEncoder, normalno pa se lahko izvajajo pa še ostali deli kode. 
Zanimivo je tudi, da v sami dokumentaciji funkcije attachInterrupt piše, da se velikokrat ta funkcija uporablja pri rotacijskih kodirnikih. V mojem primeru je ta kodirnik linearen.

void setup() {
  Serial.begin (115200);
  pinMode(encoder0PinA, INPUT); //Pin 2 = Input
  digitalWrite(encoder0PinA, HIGH);       // turn on pull-up resistor
  pinMode(encoder0PinB, INPUT); //Pin 4 = Input
  digitalWrite(encoder0PinB, HIGH);       // turn on pull-up resistor
 
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoder, CHANGE);  // encoder pin on interrupt 0 - pin 2
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoder, CHANGE);
}

### Zanka:
void loop()
{
  //Če je bil kodirnik premaknjen
  if(newdata == true) 
  {
    printej(encoder0Pos); //Piši na serijski port
  }

  //Če dobimo podatke od uporabnika preko serijske povezave
  if(Serial.available()){
      input = Serial.readStringUntil('\n');
      encoder0Pos = input.toInt();
      printej(encoder0Pos);
    }

  newdata = false; //Spremeni na False dokler ne pridejo novi podatki
}


### Branje kodirnika:
V mojem primeru je obseg podatkov od približno 0 – 32000 oz. do -32000 (minus) odvisno od smeri premikanja. 
void doEncoder() //Če se zgodi prekinitev, se izvede ta funkcija
{
  //Če arduino zazna vzpon kvadratnega signala 
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB))
  {
    encoder0Pos++; //Povečaj pozicijo
  } else {
    encoder0Pos--; //Drugače zmanjšaj pozicijo
  }
  newdata = true; //Spremenimo na True, saj imamo nove podatke 
}

### Pisanje na serijski port:
Podatke pišemo na serijski port, saj jih kasneje obdelamo v drugem programu. Prav tako pa lahko delovanje testiramo v Arduino IDE, tako da odpremo serijski monitor in spremljamo izpis.
void printej(int encoder0Pos){
     Serial.println(encoder0Pos);
}

 
Slika 9: Prikaz serijskega monitorja in podatkov merilne letve
 
## Python program
V python-u sem naredil grafični vmesnik za sistem DRO, ki se preko serijskega port-a poveže na Arduino za branje podatkov. Program omogoča branje in prikaz podatkov iz mikrokontrolerja, ponastavitev mikrokontrolerja na branje iz ničle in pa nastavitev vrednosti od katere naprej bo mikrokontroler meril naprej oz. nazaj. Sam program je trenutno dopolnjen za eno merilno letev, v tem primeru za X os.

 
Slika 10: Grafični vmesnik za DRO sistem
### Knjižnice:
Za grafični vmesnik se lahko uporabi mnogo različnih knjižnic (sam sem uporabil PyQt5), zato ne bom veliko razlagal kako je narejen sam izgled vmesnika, ampak bolj o funkcionalnostih.
import sys
import serial //Za serijsko povezavo
from time import sleep

### Serijska povezava:
Za serijsko povezavo sem ustvaril svoj razred, ki bere in piše iz ali na serijski port.
class UpdateX(QObject):
    progress = pyqtSignal(str)
    // Poveži preko serijskega porta
    arduinoX = serial.Serial(port='COM3', baudrate=115200)

    def setX_os(self):
	  //Preberi vrednost iz mikrokontrolerja in zapiši na vmesnik
        while(True):    
            poz = self.arduinoX.readline().decode('UTF-8').rstrip()
            self.progress.emit(poz.zfill(6))
    
    //Piši vrednost, ki jo določi uporabnik, na mikrokontroler
    def setX(self, value):
        self.arduinoX.write(value.encode())
### Nitenje:
V primeru, da imamo več merilnih letev, vsako za svojo os, lahko uporabimo niti za vzporedno delovanje. To naredimo v inicializaciji razreda za grafični vmesnik.
self.updateX = UpdateX()
self.xThread = QThread()

//Serijsko povezavo vežemo na funkcijo setX, ki na vmesnik zapiše vrednost
self.updateX.progress.connect(self.setX)

//Razred updateX premaknemo v novo nit in vežemo s funkcijo, ki bere iz serijskega porta
self.updateX.moveToThread(self.xThread)
self.xThread.started.connect(self.updateX.setX_os)
self.xThread.start()

### Reset – ponastavitev:
Ena glavnih funkcij DRO sistema je ponastavitev vrednosti v prejšno oz. začetno stanje. Na tem projektu, je ponastavitev vrednosti vedno v začetno stanje, kar je enako 0.
def resetButton(self, b):
//Z nastavitvijo setDTR na False in True, lahko ponastavimo Arduino na začetno stanje
        if b.objectName() == "resX":
            self.xOs.setText("000000")
            UpdateX.arduinoX.setDTR(False)
            sleep(0.22)
            UpdateX.arduinoX.setDTR(True)

### Uporabnikov vnos:
Uporabnik ima možnost vpisa svoje začetne vrednosti, od katere se bo naprej merilo. To lahko stori s pritiskom na gumb ob osi, ki jo želi nastaviti (npr. gumb X). 
Trenutna meritev se izbriše, uporabnik pa lahko sedaj vpiše vrednost. Če se zmoti pritisne na gumb Clear, da se napačne vrednost zbriše. Ko vpiše željeno vrednost pritisne na gumb Enter, ki pokliče funkcijo, razreda UpdateX, setX, ki vrednost napiše na serijski port in jo prebere Arduino. Gumbi za nastavitev vrednosti se prav tako onemogočijo in se omogočijo šele ko uporabnik ponovno klikne na gumb X.

elif a.objectName() == "Enter":
            self.updateX.setX(text) //Funkcija za pisanje na serijski port

            self.ena.setEnabled(False)
            self.dva.setEnabled(False)
            self.tri.setEnabled(False)
            self.štiri.setEnabled(False)
            self.pet.setEnabled(False)
            self.šest.setEnabled(False)
            self.sedem.setEnabled(False)
            self.osem.setEnabled(False)
            self.devet.setEnabled(False)
            self.nič.setEnabled(False)
            self.clear.setEnabled(False)
            self.enter.setEnabled(False)
 
Slika 11: Prikaz uporabniškega vnosa

## Raspberry Pi in 7-palčni zaslon
DRO sistem je sicer že končan in ga lahko uporabljamo na željenih napravah (Windows, Linux), saj je vmesnik narejen v Python programskem jeziku. Ker pa imam na zalogi en Raspberry Pi 2B, ki mu ne dela HDMI port in 7-palčni zaslon na dotik iz drugega projekta sem se odločil, da DRO sistem in Raspberry Pi z zaslonom združim. 
7-palčni zaslon ima modul za povezavo z Raspberry Pi-jem in je povezava preprosta. Potrebuje le povezavo 5 V, GND in ploščati kabel za prenos podatkov.

 Za operacijski sistem sem se odločil za Raspbian, možna pa je uporaba skoraj katerega koli operacijskega sistema, ki lahko zažene program z grafičnim vmesnikom. Zaželjeno je tudi, da omogoča uporabo dotika na zaslonu, saj je uporaba narejenega DRO sistema prijazna tudi uporabi na dotik.
Grafični vmesnik na operacijskem sistemu Linux
Za razliko od Windows sistemov moramo na Linux-u v python skripti na začetku dodati vrstico #!/usr/bin/python3. Prav tako je potrebno spremeniti serijsko povezavo, saj ni več COM port. Povezavo lahko najdemo v datoteki /dev/ nekje pod imenom tty.  V mojem primeru je bilo ime ttyACM0. Torej v python skripti namesto COM3 napišemo /dev/ttyACM0.
arduinoX = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
Naredil sem tudi skripto, ki izvede ukaz python3 /home/maj/Desktop/gui.py v terminalu.
#!/bin/bash
python3 /home/maj/Desktop/gui.py

 
Slika 14: Prototip DRO sistema z merilno letvijo


## Namestitev v realno okolje
Izdelek je v okviru predmeta Vhodno-izhodne naprave le prototip končnega izdelka. Če bi hoteli, da se ta izdelek uporablja v realnem okolju, je potrebno zanj narediti še trpežno ohišje in ga namestiti k stroju, kjer se bo le-ta uporabljal.

## Ugotovitve
Osnoven sistem za prikaz meritev je zelo preprosto razviti. Komplikacije se začnejo pri naprednejših funkcijah, kjer ni potrebno le znanje programiranja in programske opreme ampak tudi strojne opreme, ki jo uporabljamo. 
Eden pogostih problemov je tudi zmogljivost mikrokontrolerja. Arduino, čeprav zmogljiv, ni primerljiv nekaterim drugim mikrokontrolerjem, ki so mnogo hitrejši in bi bili za zelo natančne in hitre meritve bolj primerni za ta projekt. Seveda se z močnejšimi komponentani potem veča tudi cena.
Še bolj kot pa procesna moč mikrokontrolerja, bi grafični vmesnik bilo bolje narediti s programskim jezikom, ki je hitrejši kot Python (npr. C ali podobno). Sploh pa pri takem projektu ne bi bil potreben grafični vmesnik, ampak bi lahko vse naredili s pomočjo mehaničnih komponent (gumbi, tipke) in 7 segmentnimi prikazovalniki. Tako bi lahko vso kodo imeli shranjeno na samem mikrokontrolerju in ne bi potrebovali dodatnih komponent.

## Zaključek
S projektom je vidno, da se velikokrat svet strojništva ali drugih strok poveže s svetom računalništva. Sistemi DRO so pomembni za človeku prijazen prikaz meritev, kar omogoča lažje in hitrejše delo. 
V mojem projektu tudi ni velike potrebe po izjemno hitrem sistemu, zato je delovanje mikrokontrolerja Arduino in programskega jezika Python še sprejemljivo. Kljub temu, pa se bom v prihodnosti odločil, da uporabljam več mehaničnih komponent, saj je pritisk na fizično tipalo popolnoma drugačno kot na zaslonu na dotik. Skoraj zagotovo bom ta projekt še nadgradil in obdelav, da bo bolj primeren realni uporabi.
