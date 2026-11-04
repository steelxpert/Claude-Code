#!/usr/bin/env python3
"""Build FLINS-CFS-004-HU: Hungarian informative translation of the fire and acoustic research note (.docx).
Usage: python3 docs/build_fire_acoustic_hu.py --figs FIGDIR_HU --out OUT.docx"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hu_build import start

TITLE = "A födémrendszer tűzvédelmi és akusztikai teljesítménye"
SUBTITLE = ("Kutatási feljegyzés: hazai követelmények, a hidegen alakított acélgerendás födém viselkedését meghatározó tényezők, "
            "a megfelelőség útjai és az ellenőrizendő tételek")
N, A, F = start("FLINS-CFS-004", TITLE, SUBTITLE, "tűzállóság, OTSZ, EN 13501-2, EN 1365-2, akusztika, MSZ 15601-1, könnyűacélváz", [
    ("Tárgy:", "Válasz a megvalósíthatósági feljegyzés 5. kockázati tételére: a tűzvédelmi és akusztikai teljesítmény vizsgálaton alapul, "
               "és a számítási munka előtt tisztázandó"),
    ("Állapot:", "Irodai kutatás publikált összefoglalók és szakmai ismeretek alapján. A forrásdokumentumok a fejlesztői környezetből nem "
                 "voltak letölthetők; minden érték ellenőrzési jelölést kap (7. fejezet).")],
    [("Kapcsolódó:", "STEELXPERT 2026.032a — FLINS-CFS-001 rev0 (kérdések és válaszok); FLINS-CFS-002 rev0 (vizsgálati program)")])
H, P, B, T = N.H, N.P, N.B, N.table
N.toc()

H(1, "Cél és összefoglaló következtetés", new_page=True)
P("Egy könnyűacélvázas födém tűzállósága és hangszigetelése számítással nem állítható elő: mindkettő egy bevizsgált rétegrend "
  "tulajdonsága. A feljegyzés összegyűjti, mit írnak elő a hazai szabályok, mi határozza meg a kutatások szerint a viselkedést, mely utak "
  "vezetnek megfelelő termékhez, és mi ellenőrizendő még a forrásdokumentumokban. A megvalósíthatósági feljegyzés 5. kockázati tételéhez "
  "fűzött észrevételre válaszol.")
P("Következtetés. Családi háznál a födémmel szemben támasztott tűzvédelmi követelmény alacsony, és szabványos gipszkarton álmennyezettel "
  "teljesíthető; többlakásos épületnél a lakáselválasztó födémhez bevizsgált, 60 perces rétegrend és az MSZ 15601-1 szerinti akusztikai "
  "rétegrend szükséges, a két követelményt pedig ugyanazok az elemek teljesítik: két réteg lemez rugalmas sínen, ásványgyapot az üregben, "
  "tömeg a födémlapon. A terméknek ezért két rétegrendre van szüksége, nem egy egész rétegrendcsaládra. A javasolt út: a 30 perces esetre egy "
  "gipszkartongyártó osztályba sorolt könnyűacélvázas födémrendszerének átvétele, a 60 perces lakáselválasztó födémre pedig egy EN 1365-2 "
  "szerinti vizsgálat megrendelése az ÉMI-nél, a FlexInSheet által már a kezdetektől bevont tűzvédelmi szakértővel, ahogyan az észrevétel "
  "javasolja. Az észrevételben említett Lindab-szelementanulmány az interneten nem volt fellelhető; egy példányát kérjük (4.3. szakasz).")

H(1, "Hazai tűzvédelmi követelmények", new_page=True)
P("A tűzvédelmi előírásokat az Országos Tűzvédelmi Szabályzat, az 54/2014. (XII. 5.) BM rendelet tartalmazza, legutóbb a 8/2022. (IV. 14.) "
  "BM rendelettel módosított formában. A teherhordó szerkezetektől megkövetelt tűzállóságot az épület kockázati osztálya (NAK, AK, KK, MK) "
  "és szintszáma határozza meg a 2. melléklet 1. táblázatában (hiv. OTSZ 2. melléklet, 1. táblázat); a tetőfödémekre külön táblázat "
  "vonatkozik. A tűzállósági osztályba sorolás az MSZ EN 13501-2 szerint, az MSZ EN 1363-1, födémeknél az MSZ EN 1365-2 szerinti "
  "vizsgálatok alapján történik; az R, E és I kritérium, valamint a percértékek (15, 30, 45, 60, 90) a megszokott európai értékek. "
  "Szomszédos vagy egymásra épülő szerkezetek tűzállósága nem adható össze.")
P("A lakóépületi födémre vonatkozó pontos táblázati értékek a keresési eredményekből nem voltak kinyerhetők, ezeket az egységes szerkezetű "
  "szövegből (njt.hu vagy Jogtár) kell kiolvasni. A táblázat szakmai ismerete alapján, megerősítendő: az egy- vagy kétszintes családi ház "
  "NAK osztályú, födémei az R 15 – REI 30 tartományba esnek; a több, egymás fölötti lakást tartalmazó épület AK vagy KK osztályú, "
  "lakáselválasztó födémei a REI 30 – REI 60 tartományba esnek. A 16. § (3) bekezdés pinceszinti könnyítése lakóépületekre nem vonatkozik.")
P("Két szempont kifejezetten erre a termékre jellemző. Először: a csavarcölöpökön álló földszinti födém nyitott vagy lábazattal körülzárt "
  "kúszótér feletti födém, nem pince feletti; az előírás erre külön esetet nem tartalmaz, ezért az épület legalsó födémjeként kezelendő, "
  "amelynek alsó oldala ki van téve a kúszótérben lévő anyagoknak. A tárolt anyag nélküli, átszellőztetett kúszótér kis tűzterhet jelent, a "
  "gépészettel és hőszigeteléssel körülzárt lábazat azonban üreg, és üregként kell kialakítani (éghető burkolat nélkül, a kerület mentén "
  "üregzárakkal). Másodszor: az acél főtartó és a cölöpfej a teherviselő szerkezet része, ezért a födémmel azonos tűzállóságot kell "
  "biztosítaniuk; a nyitott kúszótérben lévő csupasz acél főtartó védelem nélküli acélszerkezet.")

H(1, "Mi határozza meg a hidegen alakított acélgerendás födém tűzállóságát", new_page=True)
P("A vékony, hidegen alakított szelvények gyorsan felmelegszenek, és korán veszítenek szilárdságukból. Az EN 1993-1-2 a 4. keresztmetszeti "
  "osztályú szelvények kritikus hőmérsékletét 350 °C-ban korlátozza; a kutatások ezt a határt egybehangzóan a biztonság javára tévedőnek "
  "találják: a Cseh Műszaki Egyetemen Z-szelemeneken végzett tűzvizsgálatok és héjmodellek (Schwarz, Slatinka, Jandera, ASFE 2015), a "
  "coimbrai szigma szelvényű gerendák és oszlopok, valamint egy lengyel kétmezős szelemenvizsgálat a kritikus hőmérsékletet 400–450 °C-ra "
  "teszik, és a lokális horpadás után a kötélhatás további tartalékot ad (Aalto, Lu és Mäkeläinen). Ennek ellenére a védelem nélküli gerenda "
  "szabványos tűzben néhány perc alatt eléri a 350 °C-ot, ezért a védelem nélküli, hidegen alakított födém R 15 minősítésre sem vehető "
  "figyelembe, és minden minősítés az álmennyezeti burkolatból származik.")
P("A burkolat és rögzítése a meghatározó. A gipszkarton késlelteti a hőmérséklet emelkedését az üregben; a tűzállóság akkor ér véget, amikor "
  "a lemez megreped és leesik, ez pedig a lemez típusától, a rétegek számától, a csavarkiosztástól és az illesztések eltolásától függ. A "
  "brit útmutató ökölszabályai (hiv. SCI P402, 2.2.2 szakasz): 30 perc 18 mm-es nútféderes födémlappal és alul egy réteg 12,5 mm-es "
  "tűzgátló lemezzel; 60 perc egy második, eltolt illesztésű lemezréteggel. Gyártói források ezt három vastagabb lemezzel 120 percig "
  "terjesztik ki. Ezek előtervezési iránymutatások, nem osztályba sorolások.")
P("A queenslandi (Mahendran, Kesawan) teljes léptékű födémvizsgálatok két eredménye megváltoztatja a részletképzést. A forró övre "
  "fektetett üregkitöltő hőszigetelés nem segít, sőt csökkentheti a tűzállóságot, mert a hőt a gerendában tartja; a burkolaton kívül "
  "elhelyezett hőszigetelés, illetve a lemezből és hőszigetelésből álló kompozit panelek jobban teljesítenek. Továbbá a gerincáttörések "
  "és a gerendamagasság kevésbé számítanak, mint a burkolat: a zárt övű gerendákkal végzett négy vizsgálatban a gerendák kihajlással "
  "mentek tönkre, de csak a burkolat tönkremenetele után. Acéllemezzel kasírozott gipszkarton rendszerek újabb vizsgálatokban 120–140 "
  "percet értek el. A termékre vonatkozó tanulság: a költséget a lemezbe és a rögzítésébe kell fektetni, nem az acélba.")
P("Emeleti födémnél a másik eset a felülről érő tűz: a födémlap (OSB, forgácslap) éghető, az E és I kritériumot a födémlap és – ahol "
  "előírás – egy nem éghető réteg (gipszrost lemez vagy száraz esztrich) együtt teljesíti. A kúszótér feletti földszinti födémnél ez az "
  "eset nem fordul elő.")

H(1, "A tűzállósági megfelelőség útjai", new_page=True)
H(2, "Osztályba sorolt rendszer átvétele")
P("A gipszkartongyártók rendelkeznek osztályba sorolási jelentésekkel könnyűacélvázas födém- és álmennyezeti rendszerekre: Európában a "
  "Knauf, a Rigips (Saint-Gobain) és a Siniat, acélgerendás galériafödémekre a Promat. A közzétett jelentések többsége fagerendás "
  "födémekre vagy födém alatti függesztett álmennyezetekre vonatkozik; a teherhordó, hidegen alakított acélgerendákra szólók kevesebben "
  "vannak, és egy gerendamagasság-tartományhoz és rögzítési kiosztáshoz kötöttek. Az első feladat a hazai leányvállalatok érvényes "
  "osztályba sorolási jelentéseinek összegyűjtése a 150 mm-es és magasabb C-gerendás födémekre, és annak ellenőrzése, hogy az alkalmazási "
  "terület (EN 15725 szerinti kiterjesztett alkalmazás) lefedi-e a FlexInSheet szelvényét, tengelytávolságát és födémlapját. Ha igen, a "
  "30 perces, esetleg a 60 perces födém sem igényel új vizsgálatot.")
H(2, "A lakáselválasztó födém vizsgálata")
P("Ha egyik jelentés sem fedi le a rétegrendet, egy terhelt födém-próbatest MSZ EN 1365-2 szerinti kemencevizsgálata az ÉMI-nél adja meg "
  "az osztályba sorolást. Egy vizsgálat egy rétegrendet, és a közvetlen alkalmazási terület szerint a gerendamagasságok és támaszközök "
  "meghatározott tartományát fedi le; a próbatest kb. 4 × 3 m-es teljes födém tervezési teherrel. A költség egy személyautó árának "
  "nagyságrendjébe esik, az átfutási idő hónapokban mérhető; korán kell tervezni, és egyszer, a végleges rétegrenden kell elvégezni.")
H(2, "A Lindab-tanulmány és a tűzvédelmi szakértő")
P("Az észrevételben említett, a hidegen alakított szelemenek tűzállóságáról szóló Lindab-tanulmány az interneten nem volt fellelhető. A "
  "keresés a BME 2011-es tűzállósági jelentését adta a Lindab Coverline magas trapézlemezről, valamint az ÉMI A-313-2006 számú "
  "tanúsítványát a Lindab Construline Z és C szelvényekre; egyik sem a keresett szelementanulmány. Egy példányát kérjük; ha az védelem "
  "nélküli szelemenek 350 °C-os határhoz viszonyított vizsgálatait tartalmazza, alátámasztja a nyitott kúszótérben lévő főtartó tervezését. "
  "Tűzvédelmi szakértő bevonása – ahogyan az észrevétel javasolja – elfogadott: a szakértő elkészíti a termék tűzvédelmi koncepcióját (a "
  "lefedett kockázati osztályok, a szükséges tűzállóságok, a rétegrendek, az üregekre vonatkozó szabályok, a cölöpfej védelme), és "
  "képviseli azt az ÉMI előtt.")

H(1, "Akusztika", new_page=True)
P("Az épületen belüli hangszigetelés hazai követelményeit az MSZ 15601-1 (2007-es kiadás) tartalmazza. Két lakás közötti födémre a gyártói "
  "műszaki adatlapok egybehangzóan R'_[w] + C ≥ 51 dB léghanggátlást és L'_[n,w] ≤ 55 dB lépéshangszintet adnak meg; ezek a szabványból "
  "megerősítendők, beleértve azt is, hogy a C vagy a C_[tr] tag alkalmazandó. Egy lakáson belül és családi háznál nincs kötelező érték; a "
  "födém itt komfortkérdés. A kúszótér feletti földszinti födémre semmilyen akusztikai követelmény nem vonatkozik.")
P("A könnyűacélvázas födémekre vonatkozó brit adatok megmutatják, milyennek kell lennie a rétegrendnek. Az SCI akusztikai útmutatója "
  "rugalmas sínre szerelt álmennyezetű C-gerendás födémre (két réteg 15 mm-es hanggátló gipszkarton vagy két réteg 10 mm-es gipszrost "
  "lemez, 100 mm ásványgyapot az üregben, felül úsztatott rétegű födémlap) várható értékként 47–58 dB D_[nT,w] + C_[tr] léghanggátlást és "
  "39–60 dB L'_[nT,w] lépéshangszintet ad meg; a szórás az úsztatott rétegtől és a tömegtől függ. Az Egyesült Királyságban az új "
  "épületekre vonatkozó követelmény 45 dB, illetve 62 dB. Ezek az SCI műszaki adatlapjainak (P320–P322) várható értékei, nem "
  "FlexInSheet-födémen mért adatok. A teljes szerkezeti vastagság 250–380 mm.")
P("Az akusztikai tanulság ugyanaz, mint a tűzvédelmi: tömeg és lecsatolás. A könnyűacélvázas födém a lakáselválasztó födémre vonatkozó "
  "értékeket csak nehéz felső réteggel (gipszrost lemez, száraz esztrich vagy rugalmas rétegen vékony nedves esztrich) és lecsatolt "
  "álmennyezettel teljesíti. Mindkettő ugyanaz az elem, amely a 60 perces tűzállóságot adja, így a lakáselválasztó födém rétegrendje "
  "egyetlen termék. A helyszíni mérések leggyakrabban a könnyűacélvázas falakon át történő kerülőutas hangterjedés miatt maradnak el a "
  "laboratóriumi értékektől; a falcsatlakozást a födémmel együtt kell megtervezni.")

H(1, "A cölöpökön álló földszinti födém egyéb épületfizikai kérdései", new_page=True)
B("**Hőtechnika.** A szabad levegő feletti födém a 7/2006. (V. 24.) TNM rendelet szerint „alsó zárófödém árkád felett”, U ≤ 0,17 W/m²K "
  "követelménnyel; zárt, fűtetlen kúszótér felett a fűtetlen pincére vonatkozó U ≤ 0,26 W/m²K érték alkalmazandó. A hatályos szövegben "
  "megerősítendő. A főtartó és a cölöpfej a hőszigetelési síkot átszelő hőhíd, a fejlemeznél hőhídmegszakítás szükséges.")
B("**Nedvesség.** A nyitott, átszellőztetett kúszótér kiszárítja az üreget, de hideg levegőt juttat a hőszigetelt födém alá: a hideg oldali "
  "acélnak a páratömör rétegen kívül kell maradnia, a zárt lábazat kockázata pedig a nyári páralecsapódás a hideg acélon. A cölöpalapozású "
  "épületek amerikai gyakorlata a nem szellőztetett, hőszigetelt lábazatot és a talajon elhelyezett párazáró réteget részesíti előnyben; a "
  "hazai éghajlatra az épületfizikai tervezőnek külön értékelést kell készítenie.")
B("**Tartósság.** Az EN 1993-1-3 B melléklete a bevonatot a környezeti hatáshoz köti: száraz belső térben a Z275 a szokásos; az "
  "átszellőztetett kúszótér felé nyitott alsó oldalú födémpanel nedves, fűtetlen környezetben van, és Z350 vagy kiegészítő szerves bevonat "
  "szükséges lehet; a nyitott kúszótérben lévő főtartó és cölöpfej külső környezetben van, és az EN ISO 1461 szerint tűzihorganyozandó. A "
  "cölöpszár a geotechnikai partner hatáskörébe tartozik.")

H(1, "Ellenőrzési lista és források", new_page=True)
T("A tervezési alapelvek kiadása előtt a forrásdokumentumokkal ellenőrizendő értékek", ["Tétel", "Forrás", "Állapot"],
  [["A födém tűzállósága kockázati osztály és szintszám szerint", "OTSZ 2. melléklet, 1. táblázat (egységes szerkezetű szöveg)", "nem sikerült kinyerni"],
   ["A lakáselválasztó födém akusztikai értékei: 51 dB / 55 dB", "MSZ 15601-1:2007", "gyártói adatlapokból idézve"],
   ["30 és 60 perces ökölszabály", "SCI P402, 2.2.2", "a STEELXPERT áttekintéséből"],
   ["Könnyűacélvázas födémek akusztikai tartományai", "SCI P320, P321, P322", "keresési összefoglaló"],
   ["A 4. keresztmetszeti osztály kritikus hőmérsékletére vonatkozó kutatások", "ASFE 2015 (CTU), coimbrai disszertációk, Aalto-tanulmányok", "keresési összefoglalók"],
   ["Queenslandi könnyűacélvázas födém-tűzvizsgálatok", "Kesawan és Mahendran, ASCE JSE 2015; SSRC 2014", "keresési összefoglaló"],
   ["U-értékek levegő feletti és kúszótér feletti födémre", "7/2006. (V. 24.) TNM, hatályos melléklet", "szakmai ismeret"],
   ["A környezeti hatásnak megfelelő bevonati osztály", "EN 1993-1-3:2006, B melléklet", "szakmai ismeret"],
   ["Lindab szelemen-tűzállósági tanulmány", "példány Bán Csabától", "az interneten nem található"]], [6.0, 7.0, 3.5])
T("Felhasznált források", ["Forrás", "Tartalom"],
  [["54/2014. (XII. 5.) BM, 8/2022. (IV. 14.) BM", "OTSZ: kockázati osztályok, a 2. melléklet tűzállósági táblázatai"],
   ["MSZ EN 13501-2; MSZ EN 1363-1; MSZ EN 1365-2", "Födémek osztályba sorolási és vizsgálati szabványai"],
   ["EN 1993-1-2:2005", "A 4. keresztmetszeti osztály kritikus hőmérséklete: 350 °C"],
   ["Schwarz, Slatinka, Jandera, ASFE 2015", "Z-szelemenek viselkedése tűzben; a 350 °C-os határ a biztonság javára téved"],
   ["Kesawan, Mahendran, ASCE J. Struct. Eng. 2015; SSRC 2014", "Teljes léptékű könnyűacélvázas födém-tűzvizsgálatok, a burkolat és a hőszigetelés hatása"],
   ["SCI P402 (2015); SCI P320–P322", "Tűzvédelmi ökölszabályok; könnyűacélvázas födémek várható akusztikai értékei"],
   ["MSZ 15601-1:2007", "Épületen belüli hangszigetelési követelmények"],
   ["Efectis-jelentés a Knauf részére (2010); Promat PXS-REI60; Siniat födémadatok", "Osztályba sorolt álmennyezet- és födémrendszerek példái"],
   ["ÉMI-kiadványok (Geier, Parlagi Gáspárné)", "Fa- és könnyűvázas szerkezetek tűzvédelmének hazai gyakorlata"]], [6.5, 10.0])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
