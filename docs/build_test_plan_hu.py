#!/usr/bin/env python3
"""Build FLINS-CFS-002-HU: Hungarian informative translation of the test plan for members and joints (.docx).
Usage: python3 docs/build_test_plan_hu.py --figs FIGDIR_HU --out OUT.docx"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hu_build import start

TITLE = "Elem- és csomópontvizsgálati program"
SUBTITLE = "Fizikai vizsgálatok a GMNIA-alapú fesztávtáblázatok validálásához és a kísérleti alapú csomóponti ellenállások meghatározásához"
N, A, F = start("FLINS-CFS-002", TITLE, SUBTITLE,
    "hidegen alakított acél, vizsgálati program, GMNIA-validálás, EN 1993-1-14, AISI S100 K2, gerinclemez beroppanása, gerendabekötés", [
    ("Tárgy:", "Előzetes vizsgálati program a megvalósíthatósági feljegyzés Q7 és Q9 kérdésére: milyen próbatestek, milyen "
               "vizsgálati elrendezések, hány darab, és hogyan történik az eredmények értékelése az EN 1993-1-3 A melléklete, az "
               "EN 1990 D melléklete, az EN 1993-1-14 és az AISI S100-16 K fejezete szerint")],
    [("Kapcsolódó:", "STEELXPERT 2026.032a — FLINS-CFS-001 rev0 (megvalósíthatósági kérdések és válaszok); fejlesztői tároló, "
                     "„floorframe” csomag, fea/campaign.py modul")])
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure
N.toc()

# ------------------------------------------------------------------ 1
H(1, "Cél és hatókör", new_page=True)
P("Ez a feljegyzés azokat a fizikai vizsgálatokat foglalja össze, amelyekkel a FlexInSheet födémrendszere Eurocode-alapra helyezhető. A "
  "megvalósíthatósági feljegyzés két kérdésére válaszol (hiv. FLINS-CFS-001, Q7 és Q9): milyen vizsgálatok szükségesek ahhoz, hogy a "
  "GMNIA-számítássorozattal előállított fesztávtáblázatok tervezési ellenállásként használhatók legyenek, és milyen vizsgálatok adják annak a "
  "három csomópontnak az ellenállását, amelyet a végeselemes számítás gazdaságosan nem fed le.")
P("A program első, egyeztetésre szánt változat a FlexInSheet és a geotechnikai partner számára. A próbatestek száma, a támaszközök és a "
  "szelvénycsalád a fejlesztői tároló katalógusához kötött ideiglenes értékek, amelyek a hengerlő profilkészletének ismeretében "
  "véglegesíthetők (hiv. FLINS-CFS-001, Q5). A tűzvédelmi és akusztikai vizsgálat nem része a programnak; ezekkel külön kutatási feljegyzés "
  "foglalkozik.")
P("A szabványhivatkozások kiadást és szakaszt adnak meg (hiv. …). A szakaszszámok a 9. fejezetben felsorolt kiadásokból származnak; a program "
  "vizsgáló szervezetnek történő kiadása előtt a STEELXPERT indexelt szabványtárával ellenőrizendők.")

# ------------------------------------------------------------------ 2
H(1, "A vizsgálatok szerepe", new_page=True)
P("A vizsgálatoknak három különböző feladata van, és az értékelés mindháromnál eltér. Az 1. ábra mutatja, hogyan épülnek egymásra a "
  "sorozatok.")
B("**A végeselemes modell validálása.** Az elemvizsgálatok (T1, T2) eredményét olyan GMNIA-futtatásokkal vetjük össze, amelyek az egyes "
  "próbatestek mért anyagjellemzőit, vastagságát és kezdeti geometriai imperfekcióját használják. Az összevetés rögzíti a γ_[FE] "
  "modelltényezőt, amely a GMNIA-csúcsértéket tervezési ellenállássá alakítja (hiv. EN 1993-1-14:2025, 7. szakasz és A melléklet). A "
  "validált modell ezután további vizsgálat nélkül előállítja a teljes fesztávtáblázat-mátrixot minden szelvényre, tengelytávolságra és "
  "teherosztályra. Ez a GMNIA-út gazdasági indoka: kevés a vizsgálat, sok a táblázat.")
B("**Kísérleti alapú ellenállások.** A csomóponti és főtartó-vizsgálatok (T3, T4, T5) a karakterisztikus és a tervezési ellenállást közvetlenül "
  "a vizsgálati eredményekből adják (hiv. EN 1993-1-3:2006, 9. szakasz és A.6 melléklet; EN 1990:2002, D melléklet; AISI S100-16, K2.1). A "
  "végeselemes modell csak a cölöpfej-csomópontnál kap szerepet, ahol az erőjáték nem szokványos.")
B("**A rendszer megerősítése.** Egy vagy két födémprototípus (T6) igazolja, hogy az elemek együtt a feltételezett módon viselkednek: "
  "támaszmerevség, teherelosztás, rezgés és a szerkezet tönkremeneteli viselkedése (hiv. EN 1993-1-3:2006, A.4.2 és A.4.3 melléklet; "
  "AISI S100-16, K2.2).")
FIG(F / "F1_programme.png", "A vizsgálati program: mit ad az egyes sorozat, és hol kerül felhasználásra")
P("A STEELXPERT által már alkalmazott módszerből két elv következik. Először: a tönkremeneteli mód fontosabb az amplitúdónál. Minden "
  "próbatest kezdeti geometriai imperfekcióját a vizsgálat előtt felmérjük, a megfigyelt tönkremeneteli módot rögzítjük, és összevetjük a "
  "véges sávos jelleggörbéből az 1. fázisban adódó előrejelzéssel. Az a vizsgálat, amelynek tönkremeneteli módja eltér az előrejelzéstől, "
  "megállapítás, nem pedig adatpont. Másodszor: az AISI közvetlen szilárdsági módszere (DSM) a független összehasonlítási alap (hiv. AISI "
  "S100-16, 1. függelék). Minden elemvizsgálati eredményt a GMNIA mellett a DSM-mel is összevetünk, ami a vizsgálatot és a modellt is "
  "másodszor ellenőrzi.")
P("A FlexInSheet a saját üzemében végzi a vizsgálatokat, nem akkreditált laboratóriumban (hiv. FLINS-CFS-001, Q7 válasz). Ez a programban "
  "szereplő validálási és fejlesztési vizsgálatokhoz megfelelő, feltéve, hogy az erő- és elmozdulásmérés kalibrált és dokumentált "
  "(7. fejezet). Ahol egy eredménynek független tanúsítást kell alátámasztania, ott az adott sorozatot akkreditált szervezetnél "
  "megismételjük, vagy tanúk jelenlétében végezzük; ezeket az eseteket a vizsgálati mátrix jelöli.")

# ------------------------------------------------------------------ 3
H(1, "Valamennyi sorozatra érvényes próbatest-, anyag- és mérési előírások", new_page=True)
H(2, "T0: anyag és geometria")
P("A programban felhasznált minden tekercs és vastagság sík részéből húzó-próbatestek készülnek, tekercsenként három darab, az EN ISO "
  "6892-1:2019 szerinti vizsgálatra. A vizsgálat előtt a bevonatot eltávolítjuk, és megmérjük a magvastagságot. A mért f_[y,obs] "
  "folyáshatár és t_[obs] magvastagság (a) a validáló GMNIA-futtatások bemenő adata, és (b) a vizsgálati eredmények névleges értékekre "
  "történő átszámításának alapja (hiv. EN 1993-1-3:2006, A.6.2; AISI S100-16, K2.1.1). Az acél S350GD+Z az EN 10346:2015 szerint; a gyártói "
  "műbizonylatot a vizsgálati jegyzőkönyvvel együtt kell megőrizni.")
P("Minden elem-próbatestet a vizsgálat előtt felmérünk: a gerinc és az övek síktól való eltérését a hossz mentén öt keresztmetszetben "
  "vonalzóval és hézagmérővel vagy lézervonallal, az övek és a peremmerevítők szögét, valamint a teljes elem görbültségét és csavarodását. "
  "A mért imperfekciómezőt a validáló modellbe visszük át; ahol a mérés durva, a Schafer–Peköz-féle eloszlások adják a korlátot (a "
  "lokális imperfekció mediánja 0,34t, a torzulásosé 0,94t; 95 %-os szinten 1,35t, illetve 3,44t).")
H(2, "Műszerezés")
B("Erő: hidraulikus sajtó kalibrált erőmérő cellával, vagy ±2 % pontossággal lemért holtteher (homokzsák, víztartály). Holtteher a "
  "födémprototípusnál és a nagy támaszközű hajlítóvizsgálatoknál megfelelő; a beroppanási és csomóponti vizsgálatoknál a sajtó az előnyös, "
  "mert a csúcsérték után is elmozdulás-vezérlést tesz lehetővé.")
B("Elmozdulás: mérőórák vagy induktív elmozdulásmérők (LVDT) az ábrákon jelölt pontokban, minden terhelési lépcsőben leolvasva; az "
  "elcsúszás mérésénél 0,01 mm, a lehajlásoknál 0,1 mm felbontással. A támaszsüllyedést mérni és levonni kell.")
B("A szabad alsó öv oldalirányú elmozdulása a támaszköz közepén (két mérő) a hajlítóvizsgálatokban, mert ez jelzi a torzulásos horpadást, "
  "amelyet a GMNIA-modellnek vissza kell adnia.")
B("Fényképek minden próbatestről a vizsgálat előtt, a csúcsterhelésnél és a tönkremenetel után, léptékkel; ahol lehetséges, rövid "
  "videó a tönkremenetelről.")
B("Választható és olcsó: rögzített kamera és pettyezett minta a gerincen, a lokális horpadási alak digitális képkorrelációs méréséhez.")
H(2, "Terhelési protokoll")
P("A terhet legalább tíz lépcsőben kell a várható karakterisztikus ellenállásig felvinni, minden lépcsőben egy percig tartva a "
  "leolvasásokhoz, majd kisebb lépcsőkben a csúcsértékig és azon túl, amíg a teher legalább 20 %-kal le nem csökken, vagy az alakváltozás "
  "a vizsgálatot veszélyessé nem teszi. A várható csúcsérték 5 %-ának megfelelő előterhelés kiküszöböli a felfekvési hézagokat. A "
  "használhatósági leolvasásokhoz a próbatestet egyszer tehermentesíteni és újraterhelni kell (hiv. EN 1993-1-3:2006, A.3.1 és A.4.2).")

# ------------------------------------------------------------------ 4 member tests
H(1, "Elemvizsgálatok a GMNIA validálásához (Q7)", new_page=True)
H(2, "T1: gerendahajlítás")
P("Két, 600 mm tengelytávolságú gerendát a 300 mm-enként csavarozott OSB födémlappal együtt négypontos hajlítóvizsgálatnak vetünk alá "
  "(2. ábra). A födémlappal összekapcsolt gerendapár a födém valós megtámasztási állapota: a felső övet a födémlap megtámasztja, az alsó öv "
  "szabad, az oldalirányú megtámasztó erőt a födémlap kötőelemei viszik át. Laboratóriumi alternatíva az egyedi gerenda megtámasztó "
  "keretben (hiv. AISI S911-17 kalap szelvényű tartókra, a legközelebbi szabványos eljárás; EN 1993-1-3:2006, A.3.4), ez azonban "
  "idealizálja a megtámasztást, és a validáláshoz nem szükséges.")
P("A támaszközöket minden szelvénynél az 1. fázis jelleggörbéje alapján választjuk úgy, hogy a család minden mértékadó tönkremeneteli "
  "módja legalább egyszer vizsgálatra kerüljön: egy támaszköz, ahol a nyomott öv és a peremmerevítő torzulásos horpadása a mértékadó, egy, "
  "ahol a gerinc lokális horpadása, és a leghosszabb katalógusbeli támaszköz, ahol a lehajlási és rezgési követelmény a mértékadó, és a "
  "teherbírási tartalék a legnagyobb. Az ideiglenes szelvénycsaládnál ez a 200 és 250 mm-es szelvényekre kb. 3,0, 4,2 és 5,4 m.")
P("A támaszoknál teherátadó merevítő és 100 mm-es felfekvési hossz készül, hogy a próbatest hajlításra és ne a gerinclemez beroppanása "
  "miatt menjen tönkre; a beroppanásnak külön sorozata van. Egy konfigurációt a szokásos gépészeti gerincáttörésekkel is megismétlünk, mert "
  "az áttörések csökkentik a nyírási és beroppanási ellenállást, és a számítássorozat is tartalmazza őket (hiv. AISI S100-16, G6; AISI "
  "S240-15, B2.2).")
FIG(F / "F2_joist_bending.png", "T1 gerendahajlítás: födémlappal összekapcsolt gerendapár négypontos hajlítása, a támaszoknál teherátadó merevítővel")
P("Minden vizsgálat megadja a csúcsnyomatékot, a nyomaték–lehajlás görbét a csúcs utáni szakasszal együtt, az alsó öv oldalirányú "
  "elmozdulását és a tönkremeneteli módot. Ugyanannak a próbatestnek a validáló GMNIA-futtatása a mért f_[y,obs], t_[obs] értékekkel és "
  "imperfekciómezővel készül, a födémlap megtámasztását a csavarok helyén diszkrét rugók modellezik. Elfogadási feltétel: a csúcsérték "
  "±10 %-on belül, és azonos tönkremeneteli mód; ellenkező esetben a modellt a számítássorozat futtatása előtt javítani kell.")
H(2, "T2: a gerinclemez beroppanása a támaszoknál")
P("A gerinclemez beroppanása a támaszoknál a legtöbb födémgerenda mértékadó ellenőrzése (hiv. FLINS-CFS-001, Q8), és itt térnek el "
  "leginkább az Eurocode és az AISI képletei (hiv. EN 1993-1-3:2006, 6.1.7; AISI S100-16, G5). A födémben két terhelési eset fordul elő "
  "(3. ábra): a főtartóra felfekvő gerendavég, amely végtámaszon egyoldali teher (EOF), és a cölöpfejre felfekvő főtartó felülről érkező "
  "gerendaterhekkel, amely belső cölöpnél belső támaszon egyoldali teher (IOF), szélső cölöpnél EOF. A vizsgálati eljárás az AISI "
  "S909-17 és az EN 1993-1-3:2006, A.5.2 (belső támasz vizsgálata) szerinti, a valós részlet felfekvési hosszával.")
P("Minden gerendaesetet az AISI S240-15 által előírt teherátadó merevítővel és anélkül is vizsgálunk (hiv. B2.5), mert a merevítő "
  "költséggel jár, és a táblázatoknak meg kell mondaniuk, mikor szükséges. A főtartós esetet a T3 sorozat főtartó-változatain vizsgáljuk, "
  "így a T2(b) és a T3 próbatestei közösek.")
FIG(F / "F3_web_crippling.png", "T2 gerinclemez-beroppanás: (a) gerendavég a főtartón, EOF, merevítő nélkül és merevítővel; (b) főtartó a cölöpfej felett, IOF")
P("A beroppanási vizsgálat validáló modellje rövid, héjelemes modell a mért imperfekcióval. Ennek a tönkremeneteli módnak a "
  "modelltényezőjét a hajlítási módtól külön kell meghatározni, mert az EN 1993-1-14 tönkremeneteli módonként kéri a tényezőt, és az "
  "AISI beroppanási képlete maga is tapasztalati.")

# ------------------------------------------------------------------ 5 joints and bearers
H(1, "Főtartó- és csomópontvizsgálatok (Q9)", new_page=True)
H(2, "T3: főtartók cölöpreakciók hatására")
P("A főtartó a megfordított erőjátékot viseli: felülről megoszló gerendaterheket, alulról koncentrált cölöpreakciókat (hiv. FLINS-CFS-001, "
  "Q1 válasz). Három változatcsaládot vizsgálunk a 3(b) ábra szerinti IOF-elrendezésben: a legnagyobb magasságú C-szelvényből "
  "hátával összefordított szelvénypárt, dobozszelvényt, valamint melegen hengerelt változatot (RHS vagy alacsony HEA). A főtartó hossza "
  "három cölöpköz; a szélső támaszok a szomszédos cölöpöket helyettesítő lágy rugókon állnak, így a nyomaték és a középső cölöp koncentrált "
  "reakciója a födémhez hasonlóan együtt lép fel. Eredmények: a nyomaték és a beroppanás interakciója a cölöpnél, a szükséges "
  "fejlemezméret, valamint az, hogy kell-e gerincmerevítő vagy melegen hengerelt betét. A melegen hengerelt változatot számítással, az EN "
  "1993-1-1 szerint igazoljuk, és csak a részlet miatt vizsgáljuk egyszer.")
H(2, "T4: gerenda–peremprofil és gerenda–főtartó kapcsolatok")
P("A gerendavég kapcsolatát függőleges nyírásra vizsgáljuk: a peremprofil merev kerethez rögzített, a gerendacsonkot a kapcsolat közelében "
  "terheljük (4. ábra). Az eljárás az AISI S914-15 (hidegen alakított acélvázhoz kapcsolt gerendabekötő elemek) szerinti, az értékelés az "
  "EN 1993-1-3:2006, A.6 szerint történik. Három kialakítást vizsgálunk: kapcsolószögacél, kihajtott fül és bemetszett (kivágott) vég, "
  "mindegyiket a gyártásra javasolt csavarkiosztással. Az üzemi teherhez tartozó elcsúszást rögzítjük, mert befolyásolja a födém "
  "merevségét és rezgését.")
P("Az átlapolt csavarkötések nyíróvizsgálata a szelvénycsalád vastagságkombinációira csavaronként megadja a palástnyomási és billenési "
  "ellenállást (hiv. AISI S905-17; EN 1993-1-3:2006, 8.3 és A.6). Ha a csavar szállítója rendelkezik európai műszaki értékeléssel (ETA) "
  "ezekre a vastagságokra (hiv. EAD 330046-01-0602), a sorozat kombinációnként öt megerősítő vizsgálatra csökken.")
FIG(F / "F4_joist_rim_joint.png", "T4 gerenda–peremprofil kapcsolat nyíróvizsgálata és átlapolt csavarkötés nyíróvizsgálata")
H(2, "T5: főtartó–cölöpfej csomópont")
P("A cölöpfej-csomópont a rendszer egyetlen nem szabványos csomópontja, és a források ehhez adják a legkevesebb támpontot. A vizsgálat a "
  "kerethez rögzített cölöpszár-csonkon négyféle terheléssel történik (5. ábra): nyomás a fejlemezen át, kiemelés a csavarokon át, "
  "vízszintes nyírás, valamint nyomás a beépítési tűréssel külpontosan elhelyezett főtartóval. Maga a tűrés is vizsgálati paraméter: a "
  "geotechnikai partner megadja a cölöpök elérhető helyzeti és szintbeli tűrését, és a csomópontot ezzel a külpontossággal vizsgáljuk "
  "(hiv. a STEELXPERT áttekintésében idézett gyártói útmutató ±1°-os beállítási pontossága, helyzeti tűrés megadása nélkül).")
P("A vizsgálati eredmények a részlet végeselemes modelljét kalibrálják, amellyel ezután a fejlemezt, a hosszlyukakat és a merevítőt a "
  "főtartók és cölöptípusok teljes katalógusára méretezzük, ahelyett hogy minden kombinációt megvizsgálnánk.")
FIG(F / "F5_pile_head_joint.png", "T5 cölöpfej-csomópont: nyomás, kiemelés, vízszintes nyírás és külpontos nyomás")

# ------------------------------------------------------------------ 6 system
H(1, "Födémprototípus (T6)", new_page=True)
P("Legalább négy gerendaköz szélességű, kétmezős födém készül peremprofillal, cölöpcsonkokon vagy merev oszlopokon álló főtartókkal és OSB "
  "födémlappal, a helyszíni kivitelezésnek megfelelően (6. ábra). A vizsgálat ugyanazon a próbatesten három fázisban zajlik. 1. fázis, "
  "használhatóság: lehajlás 1 kN koncentrált erőből, sarokejtéses és járásból eredő gerjesztés a sajátfrekvencia és a csillapítás "
  "meghatározására, gyorsulásmérőkkel a mezők közepén (hiv. SCI P354; ISO 18324:2016 a födémrezgés vizsgálati módszerére; EN 1993-1-3:2006, "
  "A.6.5). 2. fázis, teherbírás: egyenletesen megoszló teher homokzsákkal vagy víztartállyal, lépcsőkben a (g + q) 1,0-, 1,35- és "
  "1,5-szereséig, tartással, a lehajlások és támaszsüllyedések rögzítésével (hiv. EN 1993-1-3:2006, A.4.2 elfogadási és szilárdsági "
  "vizsgálat; AISI S100-16, K2.2). 3. fázis, a prototípus tönkremenetele: a teher növelése a tönkremenetelig, amely megmutatja, hogy a "
  "rendszer a T1 és T2 alapján előre jelzett elemtönkremeneteli módban vagy egy kapcsolatnál megy-e tönkre (hiv. EN 1993-1-3:2006, A.4.3).")
P("Ha a termék előregyártott födémpanellé fejlődik (hiv. FLINS-CFS-001, Q2), az 1. fázis kiegészül a panel kijelölt emelési pontokon "
  "végzett emelési vizsgálatával, mert a szállítás és az emelés igénybevétele gyakran meghaladja az üzemi igénybevételt (hiv. SCI P402, "
  "3.3.3 szakasz).")
FIG(F / "F6_floor_system.png", "T6 födémprototípus: használhatósági, teherbírási és tönkremeneteli fázis egyetlen próbatesten")
P("A födémlap tárcsaként működő (síkbeli nyírási) teherbírása, amely a ház vízszintes merevítéséhez szükséges, nem része ennek a "
  "programnak. Ez szabványos konzolos tárcsavizsgálat (hiv. AISI S907-17; ASTM E455), és a falrendszer meghatározása után kerül a "
  "programba.")

# ------------------------------------------------------------------ 7 matrix
H(1, "Vizsgálati mátrix és ütemezés", new_page=True)
P("Az 1. táblázat a sorozatokat a fejlesztői tároló katalógusára (hét C-szelvény, két tengelytávolság) vonatkozó ideiglenes darabszámokkal "
  "sorolja fel. A konfigurációnkénti legalább három ismétlés az AISI S100-16, K2.1.1 szerinti; az EN 1993-1-3:2006, A.6.3.3 kevesebb "
  "vizsgálatból is megenged karakterisztikus értéket nagyobb csökkentéssel, ezt csak a melegen hengerelt főtartónál alkalmazzuk. Ha az "
  "ismétlések szórása a középérték 15 %-át meghaladja, további három próbatest készül (hiv. AISI S100-16, K2.1.1).")
rows = [["T0", "Húzó-próbatestek", "tekercsenként és vastagságonként 3", "15", "1", "üzem"],
        ["T0", "Imperfekciófelmérés", "minden elem-próbatest", "mind", "1", "üzem"],
        ["T1", "Gerendahajlítás, gerendapár födémlappal", "2 szelvény × 3 támaszköz × 3", "18", "1", "üzem"],
        ["T1h", "Gerendahajlítás gerincáttörésekkel", "1 szelvény × 1 támaszköz × 3", "3", "1", "üzem"],
        ["T2a", "Gerinclemez-beroppanás, gerenda a főtartón (EOF)", "2 szelvény × 2 (merevítővel / anélkül) × 3", "12", "1", "üzem"],
        ["T2b/T3", "Főtartó a cölöpfej felett (IOF), főtartó-változatok", "3 főtartótípus × 3", "9", "2", "üzem"],
        ["T4", "Gerenda–peremprofil kapcsolat nyírása", "3 kialakítás × 3", "9", "2", "üzem"],
        ["T4s", "Átlapolt csavarkötések nyíróvizsgálata", "3 vastagságpár × 5", "15", "2", "üzem, vagy a szállító ETA-ja"],
        ["T5", "Cölöpfej-csomópont", "4 terhelési eset × 3", "12", "2", "üzem a geotechnikai partnerrel"],
        ["T6", "Födémprototípus, három fázis", "1 vagy 2 próbatest", "1–2", "3", "üzem; tanúsításhoz tanúk jelenlétében"],
        ["T7", "Födémlap tárcsavizsgálata (később)", "AISI S907 / ASTM E455 szerint", "–", "később", "akkreditált laboratórium"]]
T("Vizsgálati mátrix (ideiglenes darabszámok a fejlesztői katalógusra)", ["Sorozat", "Tárgy", "Konfigurációk × ismétlések", "Db", "Ütem", "Helyszín"],
  rows, [1.3, 4.6, 4.6, 1.0, 1.1, 3.9])
P("Az 1. ütem (T0, T1, T2a) a számítássorozat validálása, és ez az első, mert enélkül a fesztávtáblázatok nem adhatók ki. A 2. ütem (T3, "
  "T4, T5) a számítássorozattal párhuzamosan fut, amint a főtartó- és csomóponti részletek megrajzolásra kerültek. A 3. ütem (T6) zárja a "
  "fejlesztést, és ez az a vizsgálat, amelyet független tanúsításhoz tanúk jelenlétében kell elvégezni. Összesen mintegy 95 próbatest "
  "készül, ebből kb. 60 kisméretű anyagminta és csomóponti csonk, amelyek darabonként egy óránál rövidebb vizsgálatot igényelnek; az "
  "ütemezést a hajlító- és a prototípus-vizsgálatok határozzák meg.")

# ------------------------------------------------------------------ 8 evaluation
H(1, "Az eredmények értékelése", new_page=True)
H(2, "Elemvizsgálatokból a modelltényezőig")
P("Minden T1 és T2 próbatestre lefut a validáló GMNIA-számítás a mért jellemzőkkel. Az R_[test] / R_[GMNIA] hányados a sorozatra megadja a "
  "modell középértékét és relatív szórását; ezekből a γ_[FE] modelltényező az EN 1993-1-14:2025, A melléklete szerint, az EN 1990:2002, "
  "D.8 statisztikai eljárásával (ismert relatív szórású ellenállási modell) határozható meg. A várható tartományba eső eredmény γ_[FE] = "
  "1,0 és 1,15 között van. A fesztávtáblázatokban a tervezési ellenállás ezután "
  "R_[d] = R_[GMNIA,nominal] / (γ_[FE] · γ_[M1]), ahol a névleges GMNIA-számítás névleges f_[y]-nal, névleges t-vel és az Eurocode szerinti "
  "egyenértékű imperfekciókkal fut, ahogyan ez a tároló számítássorozat-moduljában már megvalósult.")
P("Ugyanezeket a vizsgálati eredményeket a DSM-mel (hiv. AISI S100-16, 1. függelék) és az EN 1993-1-3:2006 6.1.4 és 6.1.7 szakasza "
  "szerinti kézi számítással is összevetjük. A háromirányú összehasonlítás (vizsgálat, GMNIA, szabvány) próbatestenként a futtatási "
  "naplóban szerepel.")
H(2, "Csomóponti és főtartó-vizsgálatokból a tervezési ellenállásig")
P("A vizsgálati eredményeket először a névleges anyagjellemzőre és vastagságra számítjuk át (hiv. EN 1993-1-3:2006, A.6.2). Egy "
  "konfiguráció karakterisztikus értéke a középérték mínusz k-szoros szórás, ahol k a vizsgálatok számától függően az A.6.3 szerinti, a "
  "tervezési érték pedig az A.6.4 szerinti γ_[M] tényezővel adódik. Egy tartományt lefedő vizsgálatcsaládnál (például a több vastagságra "
  "kiterjedő csavarkötés-vizsgálatoknál) az A.6.3.2 szerinti családi eljárást alkalmazzuk, hogy egyetlen ellenállási összefüggés lefedje a "
  "tartományt. Az AISI szerinti eljárás (hiv. S100-16, K2.1.1, ellenállási tényező a vizsgálati statisztikából) ugyanazokon az adatokon "
  "párhuzamosan fut, mivel a megrendelő mindkét szabványt alkalmazni kívánja.")
H(2, "Használhatósági adatok")
P("Az üzemi teherhez tartozó csomóponti elcsúszás, a főtartó- és támaszmerevség, valamint a mért födémfrekvencia és csillapítás a "
  "kiosztóprogram merevségi paramétereibe kerül: a fesztávtáblázatok rezgési oszlopot is tartalmaznak, és a T6 eredménye megerősíti vagy "
  "módosítja a tervezési alapelvekben felvett 8 Hz-es követelményt (hiv. FLINS-CFS-001, Q4).")
H(2, "Dokumentálás")
P("Minden próbatestről egyoldalas jegyzőkönyv készül: azonosítás, mért jellemzők és imperfekciók, a vizsgálati elrendezés fényképe, "
  "erő–elmozdulás görbe, csúcsérték, tönkremeneteli mód és az előrejelzéssel való összevetés. A jegyzőkönyveket és a validáló modellek "
  "futtatási naplóit a számítássorozat eredményeivel együtt a projektmappában őrizzük, így a táblázatok visszavezethetők az őket "
  "alátámasztó vizsgálatokra.")

# ------------------------------------------------------------------ 9 references
H(1, "Szabványok és hivatkozások", new_page=True)
refs = [["EN 1990:2002", "D melléklet: kísérlettel segített tervezés (D.4 tervezés, D.7 egyedi jellemző, D.8 ellenállási modellek)"],
        ["EN 1993-1-3:2006", "6.1.4 hajlítás, 6.1.7 helyi keresztirányú erők, 8.3 önmetsző csavarok, 9. szakasz kísérlettel segített tervezés, "
                             "A melléklet vizsgálati eljárások (A.3, A.4, A.5, A.6)"],
        ["EN 1993-1-14:2025", "Végeselemes analízissel segített tervezés: 7. szakasz validálás és verifikálás, A melléklet modelltényező"],
        ["EN 1993-1-1:2005", "Melegen hengerelt főtartó-változat"],
        ["EN ISO 6892-1:2019", "Fémes anyagok húzóvizsgálata"],
        ["EN 10346:2015", "Folyamatos tűzi bevonatolású acél; S350GD+Z"],
        ["EAD 330046-01-0602", "Rögzítőcsavarok fémszerkezeti elemekhez és lemezekhez (a csavar-ETA-k alapja)"],
        ["AISI S100-16", "G fejezet (G5 gerinclemez beroppanása, G6 áttörésekkel), K fejezet (K2.1 vizsgálatok a szerkezeti teljesítmény "
                         "meghatározására, K2.2 megerősítő vizsgálatok), 1. függelék (DSM)"],
        ["AISI S240-15", "B2 födémszerkezet, B2.5 teherátadó merevítők, B1.5 kapcsolatok"],
        ["AISI S905-17", "Mechanikus kötőelemes hidegen alakított acélkapcsolatok vizsgálati módszerei"],
        ["AISI S907-17 / ASTM E455", "Tárcsák konzolos vizsgálati módszere (későbbi ütem)"],
        ["AISI S909-17", "A gerinclemez beroppanásának vizsgálati módszere"],
        ["AISI S911-17", "Hidegen alakított kalap szelvényű tartók hajlítóvizsgálata (a gerendahajlítási vizsgálathoz legközelebbi eljárás)"],
        ["AISI S914-15", "Hidegen alakított acélvázhoz kapcsolt gerendabekötő elemek vizsgálati szabványa"],
        ["SCI P354; ISO 18324:2016", "Födémrezgés méretezése és vizsgálati módszere"],
        ["SCI P402 (2015)", "Könnyűacélvázas lakóépületek; 3.3.3 emelés és szállítás"],
        ["Schafer és Peköz (1998)", "Hidegen alakított acélelemek imperfekció-eloszlásai"]]
T("Hivatkozott szabványok és források", ["Hivatkozás", "Felhasználás"], refs, [4.0, 12.5])
P("A szakaszszámokat kiadás előtt az indexelt szabványtárban őrzött kiadásokkal kell egyeztetni; az EN 1993-1-3 2024-es, második generációs "
  "kiadása a fenti szakaszokat átszámozza, és a hozzá tartozó magyar nemzeti melléklet megjelenése után alkalmazandó.")
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
