#!/usr/bin/env python3
"""Build FLINS-CFS-005-HU: Hungarian informative translation of the floor vibration criteria note (.docx).
Usage: python3 docs/build_vibration_hu.py --figs FIGDIR_HU --out OUT.docx"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import vib_calc as v
from floorframe import catalog
from hu_build import start


def hu(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")


TITLE = "Födémrezgési követelmények a tervezési alapelvekhez"
SUBTITLE = "Könnyű lakóépületi födémek nemzetközi gyakorlata és ideiglenes követelményrendszer a fesztávtáblázatokhoz"
N, A, F = start("FLINS-CFS-005", TITLE, SUBTITLE,
    "födémrezgés, EN 1995-1-1 7.3.3, SCI P354, CFSEI J200-26, ATC DG1, Onysko, könnyű födém", [
    ("Tárgy:", "Válasz a megvalósíthatósági feljegyzés Q4 kérdésére és 3. kockázati tételére: a magyar nemzeti melléklet könnyű födémekre "
               "nem ad rezgési követelményt, ezért a nemzetközi gyakorlat kerül átvételre"),
    ("Állapot:", "Irodai kutatás publikált összefoglalók és szakmai ismeretek alapján, a fejlesztői katalógusra végzett előzetes "
                 "számításokkal. A 6. fejezetben jelölt értékek a forrásdokumentumokkal ellenőrizendők.")],
    [("Kapcsolódó:", "STEELXPERT 2026.032a — FLINS-CFS-001 rev0 (kérdések és válaszok); FLINS-CFS-002 rev0 (vizsgálati program, T6)")])
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure
N.toc()

H(1, "Miért a rezgés határozza meg a födém fesztávját", new_page=True)
P("A fa alapú födémlappal készülő, hidegen alakított acélgerendás födém tömege 50–120 kg/m². Fesztávját ritkán a teherbírás korlátozza, "
  "sokkal inkább a járó emberre adott válasza. A kis tömeg miatt egy lépés nagyobb gyorsulást kelt, mint egy azonos merevségű betonfödémen, "
  "a sajátfrekvencia pedig abba a tartományba esik, ahol vagy a járás felharmonikusaival kialakuló rezonancia (kb. 8–10 Hz alatt), vagy az "
  "egyes sarokleütésekre adott tranziens válasz (e fölött) érzékelhető. Az Eurocode 0 (hiv. EN 1990:2002, A1.4.4) előírja az ellenőrzést, "
  "és az anyagspecifikus részekre utal; az EN 1993 ilyen födémekre nem ad követelményt, és a magyar nemzeti mellékletek sem tartalmaznak "
  "erre vonatkozó előírást. A követelményt ezért a nemzetközi gyakorlatból kell átvenni, és a tervezési alapelvekben rögzíteni, ahogyan a "
  "Q4-hez fűzött észrevétel is megállapította.")
P("Az 1. ábra előzetes számítása mutatja a katalógusra gyakorolt hatást. Száraz rétegrendnél a 200 mm magas gerenda 600 mm-es "
  "tengelytávolsággal kb. 4,8 m fesztávnál 8 Hz alá kerül, jóval a teherbírásból adódó fesztáv alatt; a lakáselválasztó födém akusztikai "
  "és tűzvédelmi követelményei miatt amúgy is szükséges nehezebb rétegrendnél a frekvencia tovább csökken, mert a többlettömeghez nem "
  "társul többletmerevség. A fesztávtáblázatok rezgési oszlopa ezért a gyakorlati fesztávok többségénél mértékadó, és az itt választott "
  "követelmény határozza meg a termék gazdaságosságát.")
FIG(F / "F1_frequency_vs_span.png", "A kéttámaszú katalógusgerendák alapfrekvenciája a fesztáv függvényében, 600 mm tengelytávolsággal, két "
    "födémtömegre (ideiglenes keresztmetszeti merevség: 0,85 I_[gross])")

H(1, "Az alkalmazott követelmények", new_page=True)
P("Könnyű födémekre négy követelménycsalád terjedt el; a legtöbb nemzeti gyakorlat ezek közül kettőt kombinál.")
H(2, "Alsó frekvenciahatár")
P("Az EN 1995-1-1:2004, 7.3.3 lakóépületi fafödémekre f_[1] = 8 Hz alatt külön vizsgálatot ír elő, és a legtöbb nemzeti melléklet "
  "megtartja a 8 Hz-es értéket; egy európai összehasonlítás szerint a határérték országonként 7 és 10,5 Hz között van. Hidegen alakított "
  "acélgerendás födémekre a trapézlemezes, gipszalapú kiegyenlítő réteggel készülő födémeken végzett kutatás legalább 10 Hz-et javasolt, "
  "mert a kis tömeg miatt a járás második és harmadik felharmonikusa 8 Hz fölött is érzékelhető. Az SCI gyakorlata szerint a "
  "könnyűacélvázas födémnek 8 Hz fölötti, nagyfrekvenciás födémnek kell lennie.")
H(2, "Merevség 1 kN koncentrált erő alatt")
P("Könnyű gerendás födémekre ez a legelterjedtebb követelmény, mert ez korrelál a legjobban a szubjektív megítéléssel: az 1 kN "
  "koncentrált erőből számított lehajlás, a szomszédos gerendákra jutó teherelosztás figyelembevételével. Alkalmazott határértékek: Onysko "
  "(Kanada; az NBC 9. részének rezgési követelményében és az ATC Design Guide 1-ben): 3 m fesztáv alatt 2,0 mm, fölötte 8 / L^[1,3] mm; az "
  "EN 1995-1-1 brit nemzeti melléklete: 4 m fesztáv alatt 1,8 mm, fölötte a fesztávval csökkenő érték; Svédország 1,5 mm; Ausztrália "
  "2,0 mm. Az EN 1995-1-1, 7.3.3 ugyanezt az ellenőrzést w / F ≤ a alakban fogalmazza meg, nemzetileg meghatározott a értékkel; a magyar "
  "nemzeti melléklet szerinti a értéket ki kell olvasni (6. fejezet).")
H(2, "Egységimpulzusra adott sebességválasz")
P("Az EN 1995-1-1 második ellenőrzése, v ≤ b^[(f1 ζ − 1)], a nagyfrekvenciás födémek egységimpulzusra adott sebességválaszát korlátozza, "
  "nemzetileg meghatározott b paraméterrel és ζ csillapítással. Merev födémlapú acélgerendáknál ritkán mértékadó, de az Eurocode-út része, "
  "ezért ellenőrzésként megmarad.")
H(2, "Válaszfaktor vagy gyorsulás")
P("Az acélipari módszer (hiv. SCI P354, 2009-es átdolgozott kiadás) a járásra adott gyorsulásválaszt számítja, az emberi érzékelés szerint "
  "súlyozza, és egy R válaszfaktoron keresztül az ISO 10137 és a BS 6472 alapgörbéivel veti össze; a P354 külön szakaszt tartalmaz a "
  "könnyűacélvázas födémekre, valamint egyszerűsített módszert a nagyfrekvenciás födémekre. A lakóépületi szorzótényezők a táblázat "
  "legkisebb értékei (nappal 2–4, éjjel 1,4 nagyságrendűek, a P354 5.3 táblázatában megerősítendők), amelyeket a könnyű födémek csak "
  "tömeggel és csillapítással teljesítenek. Az észak-amerikai út (hiv. AISC Design Guide 11, 2. kiadás, 2016; ATC Design Guide 1, 1999) a "
  "csúcsgyorsulást korlátozza, a DG11 szerint irodákban és lakásokban 0,5 % g értékre; a CFSEI J200-26 műszaki tájékoztató (2026. január) "
  "ezeket hidegen alakított acélgerendás födémekre alkalmazza, és elkülöníti a kis- és nagyfrekvenciás rendszereket. A University of "
  "Waterloo kutatása (Parnell) szerint a hidegen alakított acélfödémekre az ATC-módszer adja a legjobb előrejelzést: a vizsgált födémeknél "
  "a járásból eredő gyorsulás az ISO lakóépületi határértékén, az 1 kN-os lehajlás az Onysko-féle határértéken belül maradt; a kutatás "
  "tervezési csillapítási értékeket is javasolt, amelyek a disszertációból veendők át.")

H(1, "Ideiglenes követelményrendszer a fesztávtáblázatokhoz", new_page=True)
P("Három szint, mindhárom teljesítendő; az első kettőt a fesztávtáblázat minden cellájára számítjuk, a harmadikat csak ott, ahol mértékadó "
  "lehet.")
T("Ideiglenes rezgési követelmények", ["Szint", "Követelmény", "Érték", "Forrás"],
  [["1", "Alapfrekvencia f_[1] (kéttámaszú, állandó tömeg és a hasznos teher 10 %-a)", "≥ 8 Hz előírt; száraz rétegrendnél ≥ 10 Hz célérték",
    "EN 1995-1-1 7.3.3; hidegen alakított födémekre vonatkozó kutatás"],
   ["2", "Lehajlás 1 kN erőből a fesztáv közepén, k_[dist] teherelosztással", "≤ min(1,5 mm; 8 / L^[1,3] mm)", "Onysko / NBC; brit NM; Svédország"],
   ["3", "R válaszfaktor az SCI P354 nagyfrekvenciás módszerével, 4,5 m-nél nagyobb fesztáv vagy 20 m²-nél nagyobb mező esetén",
    "R ≤ 8 előírt; célérték a P354 lakóépületi nappali értéke", "SCI P354; ISO 10137"],
   ["–", "Egységimpulzusra adott sebesség v", "EN 1995-1-1 (7.4), b a magyar NM szerint, ellenőrzésként", "EN 1995-1-1 7.3.3"]],
  [1.0, 6.5, 5.0, 4.0])
P("Az értékek ideiglenesek. Az 1. szint 8 Hz-es értéke az európai minimum; a 10 Hz-es célérték a legkisebb tömegű és csillapítású száraz "
  "rétegrendet védi. A 2. szint a svéd állandó és az Onysko-féle, fesztávtól függő határérték közül a szigorúbbat veszi, a kettő kb. "
  "3,6 m-nél egyezik meg. A 3. szint az egyetlen, amely a tömeget és a csillapítást kifejezetten figyelembe veszi, és ezt kalibrálja a "
  "födémprototípus vizsgálata (hiv. FLINS-CFS-002, T6): a mért frekvenciát, csillapítást és 1 kN-os lehajlást a számított értékekkel "
  "vetjük össze, és a követelményrendszert a táblázatok véglegesítése előtt egyszer korrigáljuk.")
P("Csillapítás. A T6 mérés eredményéig a tervezési értékek: födémlappal ellátott, burkolat nélküli gerendás födémre 3 %, gipszkarton "
  "álmennyezettel és válaszfalakkal 4,5 %, összhangban a P354 4.1 táblázatának berendezett acélfödémekre vonatkozó értékével és a waterlooi "
  "ajánlások alsó határával.")

H(1, "A rezgési szintek számítása a programban", new_page=True)
P("Az 1. szint az EN 1995-1-1 (7.5) összefüggését használja: f_[1] = (π / 2L²) · √((EI)_[l] / m), ahol (EI)_[l] a gerendák egységnyi "
  "szélességre jutó hajlítómerevsége (E I_[eff] / s), m pedig a födém tömege kg/m²-ben. A födémlap saját merevségét a frekvenciánál "
  "elhanyagoljuk, ami csavarozott födémlapnál a biztonság javára tévedő közelítés.")
P("A 2. szint a w = F L³ / (48 E I_[eff]) · k_[dist] lehajlást számítja, ahol k_[dist] az 1 kN-os erőnek a terhelt gerendára jutó része. A "
  "brit nemzeti melléklet összefüggése, k_[dist] = max(0,38 − 0,08 ln(14 (EI)_[b] / s⁴), 0,30), ahol (EI)_[b] a födémlap gerendákra "
  "merőleges merevsége kNm²/m-ben, s pedig a tengelytávolság m-ben, 22 mm-es OSB födémlapra 400 és 600 mm-es tengelytávolságnál a 0,30-as "
  "alsó határértéket adja; merevebb födémlap ezen tovább nem javít. A csavarozott födémlap–gerenda kapcsolat, annak elcsúszása, valamint a "
  "bemetszett vagy kapcsolószögacélos gerendavégek a valós merevséget a kéttámaszú ideális érték alá csökkentik; a T6 vizsgálat ezt az "
  "eltérést méri, és merevségi tényezőt állapít meg a táblázatok számára.")
rows = []
for name in ("C200-1.5", "C250-2.0", "C300-2.5"):
    sec = catalog.section(name)
    for L in (3.0, 3.6, 4.2, 4.8, 5.4):
        f60, f110 = v.f1_hz(sec, L, 600, 60), v.f1_hz(sec, L, 600, 110)
        w = v.w_1kN_mm(sec, L, v.k_dist_ukna(sec, 600)); lim = min(1.5, v.onysko_limit_mm(L))
        ok = "igen" if (f60 >= 8 and w <= lim) else "nem"
        rows.append([name.replace(".", ","), hu(L, 1), hu(f60, 1), hu(f110, 1), hu(w, 2), hu(lim, 2), ok])
T("A katalógusgerendák előzetes vizsgálata 600 mm tengelytávolsággal (ideiglenes merevség: 0,85 I_[gross], k_[dist] = 0,30)",
  ["Szelvény", "L [m]", "f1, 60 kg/m² [Hz]", "f1, 110 kg/m² [Hz]", "w(1 kN) [mm]", "határérték [mm]", "1. és 2. szint, száraz"],
  rows, [2.2, 1.4, 2.8, 2.8, 2.4, 2.0, 2.9])
P("Az előzetes vizsgálat a táblázatok várható jellegét mutatja: az 1 kN-os lehajlási feltételt mindhárom szelvény minden fesztávnál "
  "bőven teljesíti, a frekvencia a döntő. A nehezebb, lakáselválasztó rétegrendnél a 8 Hz-es szint a 200 mm-es gerendát kb. 4,0 m-re, a "
  "250 mm-es gerendát kb. 5,2 m-re korlátozza, még a válaszfaktoros ellenőrzés előtt. A beavatkozási lehetőségek: magasabb gerenda, "
  "sűrűbb kiosztás vagy merevebb, együttdolgozó födémlap; a tömeg növelése önmagában ront a helyzeten.")

H(1, "A vizsgálati program hozzájárulása", new_page=True)
P("A vizsgálati program T6 födémprototípusán sarokejtéses és járásból eredő gerjesztéssel mérjük a sajátfrekvenciát és a csillapítást, "
  "valamint az 1 kN-os lehajlást (hiv. ISO 18324:2016 a módszerre; SCI P354 függelék a járásvizsgálatra). A mért értékek kalibrálják az e "
  "fejezetben szereplő merevségi tényezőt és csillapítást, és mellettük rögzítjük a jelenlévők szubjektív megítélését is; a fenti "
  "követelmények többsége eredetileg így született. Az első megépült házon végzett második mérés zárja a kört.")

H(1, "Ellenőrzési lista és források", new_page=True)
T("A forrásdokumentumokkal ellenőrizendő értékek", ["Tétel", "Forrás", "Állapot"],
  [["A 7.3.3 szerinti a, b és ζ magyar nemzeti melléklet szerinti értéke", "MSZ EN 1995-1-1 NM (MSZT)", "nem sikerült kinyerni"],
   ["Lakóépületi szorzótényezők és a könnyűacélvázas födémekre vonatkozó módszer", "SCI P354, 5.3 táblázat és a könnyűacélvázas födémekről "
    "szóló szakasz", "keresési összefoglaló; szakmai ismeret"],
   ["A k_dist összefüggés és az 1,8 mm-es határérték", "A BS EN 1995-1-1 brit nemzeti melléklete, NA.2.6", "szakmai ismeret"],
   ["Az Onysko-féle 2,0 mm és 8/L^1,3 határérték", "ATC DG1; NBC 2010 9. rész", "keresési összefoglaló"],
   ["0,5 % g gyorsulási határérték", "AISC DG11, 2. kiadás, 4-1 táblázat", "szakmai ismeret"],
   ["Hidegen alakított födémekre vonatkozó követelmények és csillapítási értékek", "CFSEI J200-26 (2026); Parnell, University of "
    "Waterloo, disszertáció", "keresési összefoglalók"],
   ["10 Hz-es javaslat hidegen alakított födémekre", "ICCFSS 2018/2019 cikkek (Missouri S&T tudásbázis)", "keresési összefoglaló"]],
  [6.0, 7.0, 3.5])
T("Felhasznált források", ["Forrás", "Tartalom"],
  [["EN 1990:2002, A1.4.4", "A rezgési használhatóság alapelve"],
   ["EN 1995-1-1:2004, 7.3.3 és (7.5)", "8 Hz, koncentrált erős és impulzussebesség-ellenőrzés, frekvenciaképlet"],
   ["SCI P354 (2009)", "Válaszfaktoros módszer, könnyűacélvázas födémek, csillapítási táblázat"],
   ["SCI P402 (2015)", "A STEELXPERT áttekintésében idézett 8 Hz-es és 5 mm-es követelmény"],
   ["CFSEI J200-26 műszaki tájékoztató (2026)", "Hidegen alakított acélgerendás födémek rezgése"],
   ["AISC Design Guide 11 (2016); ATC Design Guide 1 (1999)", "Gyorsulási követelmények; könnyű lakóépületi födémek"],
   ["Parnell, University of Waterloo", "Hidegen alakított acélfödémek rezgési használhatósága; ATC-módszer; csillapítás"],
   ["Onysko és mtsai; NBC 9. rész", "1 kN-os lehajlási követelmény"],
   ["Aalborgi Egyetem összehasonlító tanulmánya; SBUF 09038 (Svédország)", "Könnyű födémek nemzeti követelményei; könnyűacélvázas "
    "födémek rezgése"],
   ["ISO 10137:2007; ISO 18324:2016", "Alapgörbék; födémrezgés vizsgálati módszere"]], [6.5, 10.0])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
