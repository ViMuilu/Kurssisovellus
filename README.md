# Kurssisovellus

[Heroku](https://protected-ridge-97744.herokuapp.com/)

[Tietokanta](https://github.com/ViMuilu/Kurssisovellus/blob/master/schema.sql)

## Käyttöohje

Sovelluksen etusivulla käyttäjä voi kirjautua sisään / luoda uuden tilin

Kun sovellukseen kirjautuu onnistuneesti avautuu valikko. Valikosta on kaksi veriota opiskelijan/opettajan pääero näillä on, että vain opettaja voi luoda kurssin klikkaamalla "Createa a new course" painiketta.

Valikossa opiskelija voi klikata kurssin nimeä Courses otsikon alta jolloin avautuu kurssi sivu. Kurssi sivulla opiskelija voi liittyä kurssille painamalla Join course painiketta. Jos opiskelija on liittynyt kurssille tämä pystyy tekemään kurssi tehtäviä klikkaamalla kurssi sivulla olevia tehtäviä. Ollessaan tehtävä sivulla opiskelija voi valita mielestään oikean vastauksen. Opiskelija pystyy lähtemään kurssilta painamalla "Leave course" painiketta.

Opettaja luotuaan kurssin pystyy lisäämään kurssille tehtäviä kurssisivulla olevan New Task painikkeen avulla. Tehtävien luonti sivulla hän voi asettaa tehtävälle nimen ja sivullaa olevein ohjeiden mukaan vastaukset ja oikean vastauksen. Opettaja voi myös muokat kurssiensa kuvausta(Edit course description) sekä poistaa kurssin(Delete course). Kurssinsa sivulla opettaja voi myös tarkastella opsikelijoiden tehtävien tuloksia painamalla course statistics painiketta.

Huom kun lisää tehtäviä / tekee tehtäviä / muutta kuvausta tulee käyttäjän painaa refresh page painikettä tämän jälkeen.

## Ominaisuudet

Käyttäjä voi luoda kursseja (Toteutettu)

Käyttäjä voi asettaa kursseille tehtäviä(Toteutettu)

Käyttäjä voi selata kurssi tarjontaa ja liittyä haluamalleen kursille. (Toteutettu)

Käyttäjä voi luoda tunnukset (perus(Toteutettu)/opettaja(Toteutettu)).

Käyttäjä voi suorittaa kurssi tehtäviä(Toteutettu).

Kursseilla on yhteenvetosivu joista opiskelija näkee omat suoritetut tehtävät ja opettaja voi seurata kurssin etenemistä(Toteutettu).



