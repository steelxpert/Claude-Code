#!/usr/bin/env python3
"""Build FLINS-CFS-003-HU: Hungarian informative translation of the AI-assistance plan (.docx).
Usage: python3 docs/build_ai_plan_hu.py --figs FIGDIR_HU --out OUT.docx"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hu_build import start

TITLE = "A mesterséges intelligencia szerepe a programban"
SUBTITLE = "Rövid terv a fejlesztőcsapatnak: mit végez az MI, mit nem végezhet, és hogyan tanul a valós projektekből"
N, A, F = start("FLINS-CFS-003", TITLE, SUBTITLE, "mesterséges intelligencia, keretrendszer, tervértelmezés, ajánlatkészítő program, visszakövethetőség", [
    ("Olvasók:", "Tartószerkezeti háttérrel rendelkező fejlesztőcsapat: STEELXPERT, a geotechnikai partner, FlexInSheet. "
                 "Programozási ismeret nem szükséges."),
    ("Tárgy:", "Válasz a megvalósíthatósági feljegyzés Q12, Q13 és Q14 kérdéséhez fűzött észrevételekre")],
    [("Kapcsolódó:", "STEELXPERT 2026.032a — FLINS-CFS-001 rev0 (megvalósíthatósági kérdések és válaszok); "
                     "FLINS-CFS-002 rev0 (vizsgálati program)")])
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure

# ---------------------------------------------------------------- 1
H(1, "Az alapszabály", new_page=True)
P("A program kétféle részből áll. A statikai számítómag hagyományos, determinisztikus kód: beolvassa a tervező által aláírt "
  "fesztávtáblázatokat, a csomópont- és cölöpkatalógust és a kialakítási szabályokat, és a jóváhagyott födémkontúrból minden alkalommal "
  "ugyanazt a kiosztást, anyagkimutatást és árat állítja elő. A mesterséges intelligencia (MI) e számítómag mellett működik: előkészíti a "
  "felhasználó által jóváhagyandó bemenő adatokat, és magyarázza az eredményeket; szelvényt nem választ, cölöpszámot nem határoz meg, "
  "táblázatot nem módosít. Az elrendezést az 1. ábra mutatja.")
P("A szabálynak a biztonságon túl gyakorlati oka is van. A cég nevében kiadott ajánlatnak reprodukálhatónak kell lennie: azonos tervből két "
  "értékesítő ugyanarra az eredményre jut, és a tervező minden számot vissza tud vezetni egy táblázatra és egy szabályra. Az MI válasza ebben "
  "az értelemben nem reprodukálható, ezért ott kap szerepet, ahol egy téves válasz következménye egy javítás, nem pedig egy szerkezet.")
FIG(F / "F1_ai_touchpoints.png", "Az MI-funkciók (A–D) a determinisztikus statikai számítás mellett")

# ---------------------------------------------------------------- 2
H(1, "Az MI feladatai: négy kapcsolódási pont", new_page=True)
H(2, "A. Az engedélyezési terv értelmezése")
P("A felhasználó feltölti az engedélyezési tervet (PDF vagy DXF). Az MI javaslatot tesz a födémkontúrra, megjelöli a teherhordónak tekintett "
  "falakat, és felsorolja a felismert koncentrált terheket (kályha, kémény, kád). A javaslat a terv fölött jelenik meg a képernyőn. A "
  "felhasználó javítja és jóváhagyja, és a számítómagba csak a jóváhagyott geometria kerül. Tiszta DXF-fájlnál az MI többnyire helyes "
  "eredményt ad; szkennelt PDF-nél inkább a kézi kontúrrajzolás kiindulópontja. Mindkettő hasznos.")
H(2, "B. Az eredmény magyarázata és az ajánlat megfogalmazása")
P("A számítómag kiosztást és számértékeket ad vissza. Az MI ezekből elkészíti az ajánlat szövegét a megrendelő nyelvén, közérthetően "
  "elmagyarázza, miért ott vannak a cölöpök, és felsorolja a tervező által aláírandó feltevéseket. Kizárólag a számítómag eredményéből és a "
  "tervezési alapelvekből dolgozik; olyan számot, amely ezekben nem szerepel, nem adhat meg.")
H(2, "C. Kérdések megválaszolása")
P("Az értékesítők kérdeznek: „lehet-e itt 4 m a cölöptávolság”, „mi a teendő, ha az ügyfél csempeburkolatot szeretne”. Az MI a tervezési "
  "alapelvek és a táblázatok alapján válaszol, vagy a módosított bemenettel újra lefuttatja a számítómagot, és megmutatja az eltérést. Ha a "
  "kérdés a tervező döntését igényli, ezt jelzi, és megfogalmazza a kérdést a tervező számára.")
H(2, "D. A fejlesztői oldal")
P("Ugyanez az MI fejlesztői formájában (Claude Code) írja és teszteli a szoftvert, a PrePoMax- és CalculiX-kapcsolaton keresztül vezérli a "
  "végeselemes számítássorozatot, és elkészíti a jelentéseket. A projektben az MI-munka nagy része itt történik, és ez az értékesítő "
  "felhasználó számára nem látható. Az MI közreműködésével készülő, validált táblázatokat a tervező ellenőrzi és aláírja, mielőtt azok a "
  "programba kerülnek.")
T("Mit végezhet és mit nem végezhet az MI", ["Megengedett", "Nem megengedett"],
  [["Javaslat a födémkontúrra és a terhekre, jóváhagyásra", "A jóváhagyott kontúr önálló módosítása"],
   ["Eredmény magyarázata; ajánlatszöveg a számítómag eredményéből", "Ellenállás, fesztáv, cölöpszám vagy ár kitalálása"],
   ["A számítómag újrafuttatása módosított bemenettel, összehasonlítás", "A fesztávtáblázatok vagy a katalógusok szerkesztése"],
   ["Kérdés megfogalmazása a tervező számára", "Tervezési alapelvek jóváhagyása"],
   ["Kódírás és tesztelés; a végeselemes számítássorozat vezérlése (fejlesztői oldal)", "Táblázat közzététele a tervező ellenőrzése nélkül"]],
  [8.2, 8.3])

# ---------------------------------------------------------------- 3
H(1, "Hogyan tanul: a keretrendszer", new_page=True)
P("A Q12-höz fűzött kérdés az volt, hogy betanítható-e az MI valós projekteken, ahogyan a PrePoMax-keretrendszer is felvett oktatóanyagokból "
  "épül. Igen, és a módszer egyszerűbb, mint amilyennek hangzik. Maga az MI-modell változatlan marad, azt senki nem tanítja be és nem "
  "módosítja. Ami készül, az egy keretrendszer (angolul harness): írott utasítások, kidolgozott példák, ellenőrzőlisták és automatikus "
  "ellenőrzések gyűjteménye, amelyet az MI minden munkamenet elején beolvas, és amely közönséges fájlokként a projekt tulajdonában marad. A "
  "PrePoMax-keretrendszer pontosan ilyen: az oktatóanyagok tartalmából épül.")
P("A födémprogram keretrendszere valós projektekből, egyenként épül fel (2. ábra). Minden projekt egy munkamenet: az MI értelmezi a tervet, a "
  "mérnök kijavítja a hibákat, a javítás pedig bekerül az utasítások közé, vagy kidolgozott példaként rögzül. Ugyanez a projekt a tervvel és "
  "a jóváhagyott helyes eredménnyel ezután tesztesetként tárolódik. A keretrendszer minden későbbi módosítását az összes tárolt teszteseten "
  "ellenőrzik, így a program a már látott terveken csak javulhat, az új terveken elért eredmény pedig mérhető és kimutatható. Húsz-harminc "
  "valós terv után a keretrendszer lefedi a szokásos hazai tervábrázolási konvenciókat; száz terv után minden gyakorlati értelemben betanított "
  "segéd, és mégsincs benne semmi, ami fekete doboz volna.")
FIG(F / "F2_harness_loop.png", "A keretrendszer ciklusa: minden valós projektből szabály, példa és teszteset lesz")
P("A gyakorlatban három feltétel szükséges. A javításokat olyan szakembernek kell végeznie, aki tudja, mi a teherhordó fal, ezért az első "
  "projektek a tervező közreműködésével készülnek. A tesztkészletet meg kell őrizni: ez a tervek és a jóváhagyott eredmények mappáját jelenti, "
  "a felhasználásukra vonatkozó engedéllyel együtt. Végül az eredményt figyelemmel kell kísérni: a nem mért keretrendszer minősége "
  "észrevétlenül romlik.")

# ---------------------------------------------------------------- 4
H(1, "Szerepek, adatok és költségek", new_page=True)
H(2, "Szerepek")
P("A Q13-hoz fűzött kérdésre a válasz igen. A program és tartalmának tulajdonosa a STEELXPERT (az aláírt táblázatok, a tervezési alapelvek, a "
  "keretrendszer). A telepítést, a frissítést és a mentést a fejlesztő végzi rendszergazdaként. Az értékesítők felhasználók. A "
  "cölöpkatalógust a geotechnikai partner állítja össze és ellenőrzi. A termék tartalmáról (szelvények, részletek, árak) a FlexInSheet dönt.")
H(2, "Az adatok helye")
P("A megrendelői tervek személyes és üzleti adatok. A program a FlexInSheet saját szerverén vagy az értékesítő laptopján fut; a tervek ott "
  "maradnak. Az MI-szolgáltatáshoz csak az adott lépéshez szükséges adatrész kerül, olyan üzleti szerződés keretében, amely kizárja az adatok "
  "felhasználását a szolgáltató modelljeinek tanítására. A statikai számítómag adatai a szervert soha nem hagyják el. A FlexInSheet kérésére "
  "az A–C funkció kikapcsolható; a program kézi kontúrrajzolással ekkor is működik.")
H(2, "Költségek")
B("Üzleti MI-előfizetés az értékesítő felhasználóknak és a fejlesztőnek; induláskor havonta néhány száz euró nagyságrendben.")
B("A keretrendszer fejlesztői munkaigénye: az első tíz projekt tart a legtovább, utána projektenként kb. egy óra a javítások beépítése.")
B("Tervezői munkaidő: az első húsz tervértelmezés ellenőrzése, valamint az aláírt tervezési alapelvek, amelyekre az MI válaszai épülnek.")
B("Valós engedélyezési tervek mappája, tesztesetként való felhasználásuk engedélyével.")
H(2, "Az első három hónap")
N.N(["A program jelenlegi első változata: kontúr begépelve vagy DXF-ből, számítómag, kiosztás, anyagkimutatás (elkészült).",
     "Az A funkció DXF-re és tiszta PDF-re, az első tesztkészlet tíz valós tervvel.",
     "A B funkció: a FlexInSheet által jóváhagyott ajánlatszöveg-sablon, amelyet a számítómag eredménye tölt ki.",
     "A keretrendszer és a tesztkészlet működik, az eredményről havi kimutatás készül; a C funkció a tervezési alapelvek aláírása után "
     "kerül be."])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
