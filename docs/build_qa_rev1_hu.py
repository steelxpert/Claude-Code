#!/usr/bin/env python3
"""Build FLINS-CFS-001-HU: Hungarian informative translation of the feasibility Q&A rev1 (.docx).
Usage: python3 docs/build_qa_rev1_hu.py --rev rev1 --out OUT.docx"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from hu_build import start

TITLE = "Hidegen alakított acél födémszerkezet csavarcölöpökön"
SUBTITLE = "Megvalósíthatósági kérdések és válaszok a termékfejlesztéshez"
N, A, F = start("FLINS-CFS-001", TITLE, SUBTITLE, "hidegen alakított acél, födémszerkezet, csavarcölöp, GMNIA, Eurocode", [
    ("Tárgy:", "A termék és a tervező-ajánlatkészítő program megvalósíthatósága: kérdések, előzetes válaszok, észrevételek és nyitott döntések"),
    ("Bemenő adatok:", "A FlexInSheet ötletgyűjtő feljegyzése (2026. október); a STEELXPERT „Hidegen hajlított acél padlórendszerek – tervezési "
                       "alapok” című áttekintése (2026. október); a rev0-ra adott észrevételek (2026.10.27.)"),
    ("Kapcsolódó feljegyzések:", "FLINS-CFS-002 vizsgálati program · CFS-003 MI-támogatás · CFS-004 tűzvédelem és akusztika · "
                                 "CFS-005 rezgési követelmények · CFS-006 főtartó-koncepció")])
H, P, B, T = N.H, N.P, N.B, N.table


def Q(n, q, owner=None):
    H(3, f"Q{n}. {q}")
    if owner:
        P(f"**Döntéshozó: {owner}.**")


def R(text):
    P(f"**Észrevétel (2026.10.27.):** {text}")


N.toc()

H(1, "Cél, bemenő adatok és a feljegyzés felépítése", new_page=True)
P("A FlexInSheet Kft. új terméket tervez: csavarcölöp-alapozású, hidegen alakított acél födémszerkezetet lakóházakhoz, és hozzá egy "
  "tervező-ajánlatkészítő programot az értékesítők számára. A 2026. októberi ötletgyűjtő feljegyzés három dolgot kért: az ötlet kérdés–válasz "
  "formájú áttekintését, a legjobb változatok kiválasztását és a program első, előzetes változatát. Ez a feljegyzés az első a három közül.")
P("Az 1. revízió tartalmazza a rev0-ra adott észrevételeket: minden kérdésnél szerepel az előzetes válasz, félkövérrel az észrevétel, és ahol "
  "az észrevétel további kidolgozást kért, hivatkozás az azt tartalmazó feljegyzésre. A döntéshozók: a FlexInSheet (termék), a geotechnikai "
  "partner (alapozás) és a STEELXPERT (tartószerkezeti tervezési alapelvek).")

H(1, "Termék és hatókör", new_page=True)
Q(1, "Milyen födémtípus a termék?")
P("Gerendás födémpanel: peremprofilhoz csatlakozó C-szelvényű gerendák OSB födémlappal, az észak-amerikai és a brit könnyűacélvázas gyakorlat "
  "szerint (hiv. AISI S240-15, B2 szakasz; SCI P402, 2.1 szakasz). Először csavarcölöpökön álló, egyszintes földszinti födém, később emeleti "
  "födémek ugyanabból a katalógusból. A cölöpfejeken futó főtartó az a részlet, amelyet a födémszerkezeti dokumentumok csak általánosan "
  "tárgyalnak.")
R("Elfogadva. Az ilyen rendszerek nem kezelik megfelelően a csavarcölöpök nagy koncentrált reakcióit; a megfordított erőjátékot szétosztó elem "
  "szükséges, hidegen alakított szelvényekből (dobozszelvény vagy hátával összefordított pár) vagy melegen hengerelt szelvényből (RHS, SHS, "
  "alacsony HEA/HEB). Az előzetes vizsgálat a FLINS-CFS-006-ban szerepel: a hajlítás sosem mértékadó, a cölöpfej feletti gerinclemez-beroppanás "
  "igen, és két koncepció kerül a T3 vizsgálatokba.")
Q(2, "Előregyártott födémpanel vagy helyszínen szerelt szerkezet?", "FlexInSheet")
P("Ez határozza meg a csomóponti katalógust, az emelési teheresetet, és azt, hogy a programnak panelekre kell-e bontania a födémet. Az "
  "előzetes program helyszíni szerelést feltételez.")
R("A FlexInSheet gyártási és helyszíni kapacitással is rendelkezik, és mindkét megoldásra nyitott; először a lineáris elemekből történő "
  "helyszíni szerelés várható. A vizsgálati program a panel emelési vizsgálatát lehetőségként megtartja (FLINS-CFS-002, 6. fejezet).")
Q(3, "Milyen tehertartományt kell a táblázatoknak lefedniük?")
P("Az MSZ EN 1991-1-1 a magyar nemzeti melléklettel: az A kategóriára q_[k] = 2,0 kN/m², válaszfalak 0,8–1,2 kN/m², burkolatok 0,5–1,5 kN/m², "
  "koncentrált teher 2,0 kN, valamint a felhasználó által megadott terhek. Táblázati teherosztályok 2,5, 3,5, 4,5 és 5,5 kN/m² teljes "
  "karakterisztikus teherrel.")
R("Elfogadva. A reális lakóépületi hasznos teher legfeljebb 2,0–3,0 kN/m², a válaszfalakból és teherhordó falakból származó vonalmenti "
  "terhekkel és koncentrált terhekkel (kályha, kémény) együtt. A falakból származó vonalmenti terhek külön esetként kerülnek a táblázatok "
  "tengelyei közé.")
Q(4, "Milyen használhatósági követelmények vonatkoznak a födémre?", "STEELXPERT")
P("Alapértelmezésként a brit követelményrendszer (hiv. SCI P402, 2.1.2 szakasz): teljes lehajlás L/350 és 15 mm, hasznos teherből L/450, "
  "1 kN koncentrált erőre vonatkozó határérték, 8 Hz és 5 mm az állandó teher és a hasznos teher 20 %-a alatt; a táblázatokban külön rezgési "
  "oszlop.")
R("Az értékek egyelőre elfogadva; a részletes kutatás alapján a nemzetközi gyakorlatra támaszkodunk. Ez a kutatás a FLINS-CFS-005, amely "
  "háromszintű követelményrendszert javasol (8 Hz előírt és 10 Hz célérték; 1 kN-os lehajlás az Onysko-féle és a svéd határérték szerint; "
  "SCI P354 válaszfaktor nagy fesztávokra), és kimutatja, hogy a fesztávok többségét a rezgés határozza meg, nem a teherbírás.")
Q(5, "Melyik szelvénycsalád?", "FlexInSheet")
P("Peremmerevített C-szelvény, 150–300 mm, 1,2–2,5 mm, S350GD+Z, 400 vagy 600 mm-es tengelytávolsággal, gépészeti áttörésekkel; a "
  "tényleges szelvénycsaládot a hengerlő határozza meg.")
R("Elfogadva; a főtartó szelvényeit lásd a Q1-nél.")

H(1, "Tartószerkezeti módszer", new_page=True)
Q(6, "Az AISI mint iránymutatás és az Eurocode mint igazolás: összeegyeztethetők?")
P("Igen: az AISI S240-15 adja a kialakítási szabályokat, a GMNIA az ellenállásokat, az EN 1993-1-3 és az EN 1993-1-14 γ_[M1] tényezővel "
  "igazolja azokat, a DSM (hiv. AISI S100-16, 1. függelék) pedig a független összehasonlítási alap.")
R("Elfogadva.")
Q(7, "Megvalósítható-e CalculiX-szel egy paraméteres, GMNIA-alapú teherbírásitáblázat-számítássorozat?")
P("Megvalósítható, és elemszinten bizonyított; kb. 340 gerendaeset, 60 támaszeset, 80 főtartó-eset; néhány CPU-nap. A költséget a "
  "validálás jelenti: tönkremeneteli módonként fizikai vizsgálatokkal kalibrált γ_[FE] modelltényező (hiv. EN 1993-1-14:2025, A melléklet).")
R("Jól hangzik. A FlexInSheet minden új terméket fizikailag is vizsgál, de nem laboratóriumban. A vizsgálati program (FLINS-CFS-002) a "
  "FlexInSheet üzemére készült; akkreditált szervezet jelenléte csak a tanúsítási vizsgálatnál szükséges.")
Q(8, "Mely tönkremeneteli módokat kell a táblázatoknak kezelniük?")
P("A támaszköz közepén lokális és torzulásos horpadás szabad alsó övvel, valamint a rezgés; a támaszoknál a gerinclemez beroppanása "
  "teherátadó merevítővel és anélkül (hiv. EN 1993-1-3:2006, 6.1.7; AISI S100-16, G5); a főtartó hajlítása, beroppanása és lehorgonyzása a "
  "cölöpfejnél.")
R("Elfogadva.")
Q(9, "A csomópontok is paraméteresek legyenek?")
P("A csavarozott kapcsolatoknál kísérleti alapú ellenállások (hiv. EN 1993-1-3:2006, 8. szakasz és A melléklet), végeselemes számítás csak "
  "a cölöpfej-részletnél.")
R("Elfogadva, azzal a kéréssel, hogy készüljön előzetes vizsgálati program AISI- és EN-hivatkozásokkal, ábrákkal, a Q7 beépítésével. "
  "Elkészült FLINS-CFS-002 néven: T0–T6 sorozat, hat vizsgálati elrendezés ábrája, vizsgálati mátrix és értékelés.")
Q(10, "Mi szükséges a geotechnikai oldalról?", "geotechnikai partner")
P("Cölöptípusonként és -hosszonként a nyomási, vízszintes és kihúzási ellenállás tervezési értéke, a minimális cölöptávolság és a "
  "fagyhatárra vonatkozó szabály, mindez katalógusfájlban. A program talajmechanikai számítást soha nem végez.")
R("Tudomásul véve.")

H(1, "A tervező-ajánlatkészítő program", new_page=True)
Q(11, "Ki használja, és mit kell előállítania?")
P("Az értékesítők; ajánlatcsomag kiosztással, anyagkimutatással, árral és aláírt tervezési alapelvekkel; determinisztikus és "
  "visszakövethető statikai rész.")
R("Jól hangzik.")
Q(12, "Reális-e az engedélyezési tervekből való adatbevitel?")
P("Részben: DXF-import, vektoros PDF-import jóváhagyással, és biztonsági megoldásként kézi kontúrrajzolás a PDF fölött.")
R("Elfogadva. Arra a kérdésre, hogy használható-e itt MI – a PrePoMax-keretrendszerhez hasonlóan, valós alaprajzokon, egymást követő "
  "munkamenetekben felépített keretrendszerként –, a FLINS-CFS-003 válaszol: igen, A funkcióként, valós projektekből épülő "
  "keretrendszer-ciklussal és pontozott tesztkészlettel.")
Q(13, "Ügyfélgép, saját szerver és böngésző: ellentmondás?")
P("Nem: a böngészős felületű Python-háttérrendszer laptopon, a FlexInSheet szerverén vagy hosztolt környezetben is fut; a katalógusok "
  "központi URL-ről, helyi gyorsítótárral töltődnek.")
R("Rendben. A tulajdonos a STEELXPERT (tartalom, táblázatok, tervezési alapelvek, keretrendszer), a rendszergazda a fejlesztő; az "
  "értékesítők felhasználók (FLINS-CFS-003, 4. fejezet).")
Q(14, "Legyen-e MI-támogatás?")
P("Igen, a statikai számításon kívül: tervértelmezés, ajánlatszöveg, kérdések megválaszolása, valamint a fejlesztői oldalon a végeselemes "
  "számítássorozat vezérlése.")
R("Részletesebb kifejtést kértek, tartószerkezeti háttérrel rendelkező, de nem fejlesztő olvasók számára. Elkészült FLINS-CFS-003 néven "
  "(5 oldal).")
Q(15, "FreeCAD legyen a felhasználói felület?")
P("Az értékesítési programhoz nem; webes felület 2D-s rajzfelülettel. A FreeCAD később exportálóként jöhet szóba.")
R("Elfogadva; IFC-exportra igény van.")

H(1, "Kockázatok és értékelés", new_page=True)
N.N(["A csavarcölöpök hazai elfogadtatása. Nincs hazai szabály; a DIBt-út német. **Észrevétel:** a FlexInSheet a csavarcölöpös gyakorlat "
     "minden területén jelentős tapasztalattal rendelkezik; az elfogadtatás útját velük együtt kell dokumentálni.",
     "γ_[FE] modelltényező. Fizikai vizsgálatok nélkül a táblázatok nem felelnek meg az Eurocode-nak (hiv. EN 1993-1-14:2025, A melléklet). "
     "**Észrevétel:** a vizsgálati programok után derül ki; ez most a FLINS-CFS-002.",
     "Rezgési követelmények. A magyar nemzeti melléklet nem határozza meg őket. **Észrevétel:** a kutatás alapján a nemzetközi gyakorlat kerül "
     "átvételre; ez most a FLINS-CFS-005.",
     "A tervimport minősége. A kézi kontúrrajzolás lehetősége csökkenti a kockázatot. **Észrevétel:** elfogadva.",
     "Tűzvédelmi és akusztikai teljesítmény. Vizsgálaton alapul, nem számítható. **Észrevétel:** nagy problémának tekintendő; bármilyen "
     "számítási munka előtt alapos kutatás szükséges, a FlexInSheet tűzvédelmi szakértőt bíz meg, hivatkozásként pedig a Lindab "
     "szelemen-tűzállósági tanulmánya szolgál. A kutatás FLINS-CFS-004 néven elkészült; a Lindab-tanulmány az interneten nem volt fellelhető, "
     "egy példányát kérjük."])
P("Az értékelés változatlan: a termék és a program megvalósítható. A kritikus utat a fizikai vizsgálatsorozat, a tűzvédelmi koncepció és a "
  "geotechnikai elfogadtatás útja jelenti, nem a szoftver.")
T("Nyitott döntések és felelőseik az észrevételek után", ["Tétel", "Felelős", "Szükséges ehhez"],
  [["Előregyártott panel vagy helyszínen szerelt szerkezet (Q2): helyszíni szerelés várható, megerősítendő", "FlexInSheet",
    "Csomóponti katalógus, emelési teheresetek"],
   ["A hengerlő szelvénycsaládja (Q5)", "FlexInSheet", "Számítássorozat, katalógusfájl"],
   ["Főtartó-koncepció: merevített, hidegen alakított dobozszelvény vagy melegen hengerelt szelvény (Q1)", "STEELXPERT a FlexInSheet-tel, "
    "a T3 után", "Cölöpsor-részlet, táblázatok"],
   ["Rezgési követelményrendszer (Q4): ideiglenes rendszer a CFS-005-ben", "STEELXPERT", "Tervezési alapelvek, fesztávtáblázatok"],
   ["A cölöpök tervezési értékei, cölöptávolság, fagyhatárra vonatkozó szabály (Q10)", "Geotechnikai partner", "Cölöpkatalógus-fájl"],
   ["Tűzvédelmi koncepció és szakértő; Lindab-tanulmány", "FlexInSheet (szakértő), Bán Csaba (tanulmány)", "Rétegrendkatalógus, tanúsítás"],
   ["A csavarcölöpök hazai elfogadtatásának útja", "FlexInSheet a geotechnikai partnerrel", "Termékengedélyezés"]], [7.0, 4.0, 5.5])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
