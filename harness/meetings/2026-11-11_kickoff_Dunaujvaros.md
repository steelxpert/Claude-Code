# FlexInSheet CFS födémrendszer — belső indító megbeszélés (kick-off), 2026-11-11 kedd

**Helyszín:** FLINS telephely, 2400 Dunaújváros, Előd utca 4. · **Levezető:** Csaba (STEELXPERT)
**Résztvevők:** Ajkay Tibor (cégcsoport-tulajdonos), építészeti tervezés, acél alkatrészgyártás, értékesítés
**Jelleg:** belső levezetői jegyzet (chair notes). Nem kiadott anyag. Ajkay Tibor a teljes HU anyagot megkapta (FLINS-CFS-001-HU rev1 … 006, bemutató 17 dia); új ügyfélanyag keddre nem készül.
**Időkeret:** 90 perc. 1. rész döntések (45), 2. rész munkaáramok (45).

## Cél

1. A hat megrendelői döntés lezárása (bemutató 17. dia).
2. Csoportonként egy munkaáram, egy első feladat (2 hét), egy kapcsolattartó.

## Napirend

| idő | pont | tartalom | eszköz |
|---|---|---|---|
| 0:00–0:05 | Nyitás | cél, időkeret, mi NEM téma ma (lásd lent) | — |
| 0:05–0:15 | Hol állunk | FLINS-CFS-001 rev1: a termék és a program megvalósítható; az ütemet a kísérletek, a tűzvédelmi koncepció és a csavarcölöpök hazai elfogadtatása határozza meg, nem a szoftver. A program első változata fut; a fesztávtáblázatok IDEIGLENESEK (GMNIA + T-sorozat előtt nincs kiadható szám). | 3., 15., 16. dia |
| 0:15–0:55 | Döntések | D1–D6 alább, egyenként: javaslat → kérdés → döntés vagy felelős + határidő | 17. dia |
| 0:55–1:25 | Munkaáramok | táblázat alább, csoportonként kitöltve | — |
| 1:25–1:30 | Zárás | döntésnapló felolvasása, következő időpont, ki mit kap tőlünk | — |

## 1. rész — döntések (D1–D6)

| # | kérdés | miért most | javasolt irány | döntés / felelős / határidő |
|---|---|---|---|---|
| D1 | A hengerlő profilkészlete (Q5): mely hidegen alakított C-szelvények (magasság, lemezvastagság) és készül-e dobozszelvény (back-to-back C) a főtartóhoz | a katalógus, a GMNIA-számítássorozat és a próbatestek száma ettől függ (kb. 95 próbatest, 7 szelvény × 2 tengelytávolság a feltételezés) | gyártás adja a tényleges készletet; STEELXPERT rögzíti a katalógust | |
| D2 | Geotechnikai partner és csavarcölöp-katalógus | a cölöpfej-részlet (D03), a cölöpkiosztás és az engedélyezés (MSZ EN 1997-1) ezen áll | geotechnika felelőse: Szecsey Márton; partner és katalógus megnevezése | |
| D3 | Észrevételek a CFS-001…006 feljegyzésekhez | a rev1 lezárása, a HU szöveg véglegesítése | észrevételek írásban 1 héten belül; nincs észrevétel = elfogadott | |
| D4 | Célpiac: csak családi ház, vagy többlakásos is | a 60 perces tűzvédelmi és az akusztikai rétegrend (D07, D09, CFS-004) csak többlakásosnál kell | első kiadás: családi ház; többlakásos külön ütemben | |
| D5 | A program helye: FLINS saját szerver vagy az értékesítők laptopja | telepítés, adatvédelem (alaprajzok helyben maradnak), katalógusfrissítés | Docker-kép + indító; központi katalógus URL-ről, helyi tárral; döntés a futtatás helyéről | |
| D6 | Kérnek-e MI-támogatást (alaprajz-felismerés, ajánlatszöveg) | fejlesztési kör és költség | igen, de az MI a teherviselő számításon KÍVÜL marad (CFS-003); a fesztáv mindig a táblázatból jön | |

## 2. rész — munkaáramok

| munkaáram | felelős csoport | első feladat (2 hét) | tőlünk kapják | tőlük kérjük | kapcsolattartó |
|---|---|---|---|---|---|
| W1 Szerkezeti koncepció és méretezés: katalógus, keretezési szabályok, GMNIA-számítássorozat (EN 1993-1-3, EN 1993-1-14), T0–T2a validálás | STEELXPERT | katalógus rögzítése D1 után; T0–T2a vizsgálati terv részletezése | katalógus v0, vizsgálati terv részletes változata | profilkészlet (D1), próbatestek gyártási vállalása | Csaba |
| W2 Gyártás: profilkészlet, dobozszelvény, csomóponti alkatrészek, próbatestek | acél alkatrészgyártás | profilkészlet és tűrések írásban; próbatest-gyártás ütemezése | szelvényrajzok (D02), csomóponti részletek (D03–D06) | gyártási korlátok, lemezvastagság-készlet, bevonat | |
| W3 Építészeti tervezés: alaprajzi típusok, rétegrendek, bemenő rajzok | építészeti tervezés | 3–5 jellemző alaprajz DXF-ben; rétegrend-igény (D07) | D01–D09 részletábrák, a program bemeneti követelményei (zárt poligon, réteg) | DXF-minták, tipikus fesztávok és terhek | |
| W4 Értékesítés: célpiac, ajánlati folyamat, a program használata | értékesítés | ajánlati folyamat lépései; mit kell a programnak kiadnia (PDF-ajánlat, anyagjegyzék, ár) | a program első változata (bemutató), 5 alaprajzi forma | árazási adatok, ügyféligények, hol fut a program (D5) | |
| W5 Geotechnika: csavarcölöp-katalógus, elfogadtatás, próbaterhelés | Szecsey Márton + FLINS | partner és katalógus (D2); a cölöpfej-részlet (D03) átnézése | támaszreakció-igény a programból (ideiglenes) | cölöp tervezési ellenállások, próbaterhelési eljárás | Szecsey Márton |
| W6 Vizsgálati program T0–T6 | STEELXPERT koordinál, labor partner (O-006) | labor megkeresése, T0 anyagvizsgálat és T1 gerendahajlítás előkészítése | FLINS-CFS-002 részletezve | labor és tanúsító szervezet kiválasztása (T6) | Csaba |
| W7 Program (app) első változata | STEELXPERT (Csaba; Máté szerepe később, O-002) | durva terv: hogyan nézzen ki, viselkedjen, működjön; adatszerződés a fesztávtáblázatokhoz (JSON) | — | D5 és D6 döntése | Csaba |
| W8 Engedélyezés: tervezési alapelvek, ÉMI/NMÉ, geotechnikai elfogadtatás | STEELXPERT + FLINS | az engedélyezési útvonal felvázolása; kapcsolat ÉMI-vel | tervezési alapelvek vázlata | FLINS döntés az NMÉ-ről | |

## Mi NEM téma kedden (ezt mondjuk ki a nyitásban)

- Fesztáv-számok: minden táblázat ideiglenes a GMNIA-számítássorozat és a T-sorozat előtt.
- Tűzvédelmi és akusztikai eredmény: csak az igény (D4) dől el, a megoldás a CFS-004 szerinti külön kutatási feljegyzés.
- Határidő a táblázatok első kiadására: a profilkészlet (D1) és a labor (W6) nélkül nem adható.
- Szoftver-részletek (nyelv, keretrendszer): a program első változata bemutatható, a fejlesztési szerepek később dőlnek el.

## Döntésnapló (a megbeszélésen töltjük)

| # | döntés | felelős | határidő | megjegyzés |
|---|---|---|---|---|
| D1 | | | | |
| D2 | | | | |
| D3 | | | | |
| D4 | | | | |
| D5 | | | | |
| D6 | | | | |

## Eredmény (rögzítve: FLIN-003, a levezető szóbeli összefoglalója alapján)

A megbeszélés napja: 2026-11-10, kedd (a fájlnév dátuma eltér, lásd STATE O-012).

- A termékötlet (csavarcölöpökre támaszkodó, hidegen alakított acél vázrendszer) jó — ebben egyetértés van.
- A fejlesztési programba (szerkezeti és szoftverfejlesztés) FLINS addig nem tesz jelentős időt és pénzt, amíg nem ismert: (a) milyen felépítmény kerül az alapkeretre, (b) mi a célpiac (lakó, kereskedelmi, védelmi).
- A D1–D6 pontok egyenként nem zárultak le [a levezető megerősítésére vár]; a döntésnapló ezért üres marad.
- A levezető javaslata: egy teljes, kis mintaház (modern pajtaház jellegű hétvégi ház) megtervezése csavarcölöpökön — födém (alapkeret), teherhordó külső és nem teherhordó belső falak, részleges közbenső födém, tető, falmerevítés, ablakkeretezés, tetőablak — 3D modell és Eurocode szerinti számítás formájában, rögzített áron és határidőre, a FLINS belső egyeztetéseinek alapjául. Állapot: javaslat, FLINS válaszára vár (STATE D-013, O-010).

Következő lépés a megbeszélés után: a döntésnapló a `harness/STATE_FLINS.md` §3/§4 részébe kerül (FLIN-003), az észrevételek a feljegyzésekbe.

## Szóhasználat (EN-HU szójegyzék, Zone A)

hidegen alakított (cold-formed) · dobozszelvény (box section, back-to-back C) · a gerinclemez beroppanása (web crippling) · határállapot (limit state) · torzulásos horpadás (distortional buckling) · kifordulás (lateral-torsional buckling) · fesztávtáblázat (span table) · főtartó (bearer) · gerenda (joist) · csavarcölöp (screw pile) · cölöpfej (pile head) · próbatest (test specimen) · modelltényező γ_FE (model factor).
