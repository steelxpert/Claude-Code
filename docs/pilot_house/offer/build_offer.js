// STEELXPERT 2026.032a - FLINS mintaház: ajánlatlevél + kísérő e-mail (.docx), docx-js.
// Run: node build_offer.js   (writes the two .docx files; language hu-HU throughout)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, PageBreak,
} = require("docx");

const LANG = { value: "hu-HU", eastAsia: "hu-HU", bidirectional: "hu-HU" };
const FONT = "Arial", GRAY = "666666", DARK = "1A1A1A", ACCENT = "2E5C8A";
const CREATOR = "Bán Csaba (STEELXPERT Kft.)";

const C = {
  date: "Budapest, 2026. november 13.",
  addressee: ["Szabó András ügyvezető", "FlexInSheet Kft.", "2400 Dunaújváros, Előd utca 4.", "Másolat: Kalászi Balázs"],
  subject: "Ajánlat – FLINS mintaház (pilot ház) tartószerkezeti tervezése, STEELXPERT 2026.032a",
  salutation: "Szia András!",
  opening:
    "Ahogy a keddi megbeszélésen felvetettem: megtervezek egy komplett kis mintaházat – barn-house stílusú " +
    "hétvégi ház, kb. 12,5 × 5,2 m, galériával és tetőablakkal – kizárólag a FLINS által ma gyártott " +
    "hidegen alakított C / U szelvényekből, csavarcölöp-alapozáson. A cél egy kézzelfogható, Eurocode " +
    "szerint igazolt példa arra, hogy a portfóliótokból egy egész ház felépíthető; ez adja az alapot a " +
    "házon belüli döntésetekhez. A csatolt 3D vázmodell mutatja, hol tartunk: minden szerkezeti elem a " +
    "helyén van, a méretek még előzetesek.",
  h1: "Amit kaptok",
  deliverables: [
    "Tervezési alapok: magyarországi hó- és szélteher-burkoló (kb. 400 m tengerszint feletti magasságig), anyagok, szelvénykészlet, feltételezések.",
    "3D vázmodell minden elemmel valós méretben és helyen, STEP formátumban, általános elrendezési PDF nézetekkel; kapcsolattípusonként egy kidolgozott részlet.",
    "Hatások (MSZ EN 1990 / 1991 + nemzeti melléklet), globális 3D rúdmodell, szelvényellenőrzések MSZ EN 1993-1-3 szerint: tető, hosszfalak, oromfalak, galéria, padlóváz, főkeretek, merevítés és állékonyság, használhatóság.",
    "Kapcsolati ellenőrzések (MSZ EN 1993-1-8 / 1993-1-3), típusonként egy: keretcsomópontok, oszloptalp, vonórúdvégek, lehorgonyzások, panel–gerenda kapcsolat.",
    "Talajcsavar-reakciótábla a geotechnikus (Szecsey Márton) részére.",
    "Magyar nyelvű statikai dokumentáció számítási melléklettel és tervezői nyilatkozattal.",
    "Két egyeztetés veletek és egy revíziós kör.",
  ],
  h2: "Feltételek",
  conditions: [
    "Szelvények: C / U150 × 1,5; a főkeretekhez C200 × 2,0, a padló keresztgerendáihoz C200 × 2,5 (egyeztetett kivételek). Az ellenállásokat számítással (EN 1993-1-3) igazolom, nem vizsgálattal: amíg nincs FLINS típusvizsgálat, minden érték ELŐZETES.",
    "A tárgy a ház csupasz acélváza. Burkolat, padlólemez, héjalás, nyílászárók másoktól; teherhordásban nem számolok velük.",
    "Nem tartalmazza: építészet, épületfizika, tűz- és akusztikai tervezés, a csavarcölöpök geotechnikai tervezése és próbaterhelése, vizsgálatok, gyártmánytervek és szabáslisták, engedélyezési dokumentáció.",
  ],
  h3: "Ár és határidő",
  price: [
    "Átalányár: 2 445 000 Ft + ÁFA (163 mérnökóra × 15 000 Ft/óra).",
    "Határidő: a megrendeléstől számított 4 hét.",
    "Az ajánlat 30 napig érvényes.",
  ],
  attachment:
    "Melléklet: FLINS_mintahaz_3D_vazmodell.html – a ház 3D vázmodellje egyetlen fájlban. Bármely böngészőben " +
    "megnyílik, telepítés és internet nélkül; egérrel forgatható, görgővel nagyítható, a részletek a bal " +
    "oldali listából külön is megnézhetők. Koncepció, nem ellenőrzött méretek.",
  closing: "Ha kérdés van, hívj – szívesen átbeszéljük.",
  sender: ["Bán Csaba", "okl. építőmérnök, tartószerkezeti vezető tervező (T-T/01-18387)", "STEELXPERT Kft.", "info@steelxpert.com"],
  tagline: "Acélszerkezetek – statikai tervezés és ellenőrzés",
  letterheadPlaceholder: "[cím / telefonszám – kérlek egészítsd ki]",
};

const run = (text, o = {}) => new TextRun({ text, font: FONT, size: 21, color: DARK, language: LANG, ...o });
const body = (text, o = {}) => new Paragraph({ spacing: { after: 90, ...(o.spacing || {}) }, children: [run(text, o.run || {})] });
const heading = (text) => new Paragraph({
  spacing: { before: 110, after: 50 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: ACCENT, space: 2 } },
  children: [run(text, { size: 22, bold: true, color: ACCENT })],
});
const bullet = (text) => new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 50 }, children: [run(text, { size: 20 })] });

const numbering = { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 420, hanging: 260 } } } }] }] };
const styles = { default: { document: { run: { font: FONT, size: 21, color: DARK, language: LANG } } } };

// ------------------------------------------------------------------ ajánlatlevél
const letter = [
  new Paragraph({ spacing: { after: 20 }, children: [run("STEELXPERT Kft.", { size: 30, bold: true, color: ACCENT })] }),
  new Paragraph({ spacing: { after: 20 }, children: [run(C.tagline, { size: 18, italics: true, color: GRAY })] }),
  new Paragraph({ spacing: { after: 20 }, children: [run(C.letterheadPlaceholder, { size: 17, italics: true, color: GRAY })] }),
  new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 4 } }, spacing: { after: 160 },
    children: [run("info@steelxpert.com", { size: 18, color: GRAY })] }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 160 }, children: [run(C.date, { size: 19, color: GRAY })] }),
  ...C.addressee.map((l, i) => body(l, { spacing: { after: i === C.addressee.length - 1 ? 140 : 20 }, run: i === 3 ? { color: GRAY, size: 19 } : {} })),
  new Paragraph({ spacing: { after: 120 }, children: [run(`Tárgy: ${C.subject}`, { bold: true })] }),
  body(C.salutation),
  body(C.opening),
  heading(C.h1), ...C.deliverables.map(bullet),
  heading(C.h2), ...C.conditions.map(bullet),
  heading(C.h3), ...C.price.map(bullet),
  new Paragraph({ spacing: { before: 100, after: 100 }, children: [run(C.attachment, { size: 19, italics: true, color: GRAY })] }),
  body(C.closing, { spacing: { after: 160 } }),
  body("Üdv,", { spacing: { after: 40 } }),
  ...C.sender.map((l, i) => body(l, { spacing: { after: 20 }, run: i === 0 ? { bold: true } : i === 3 ? { color: GRAY } : { size: 19 } })),
];

// ------------------------------------------------------------------ kísérő e-mail (törzs, Outlookba másolható)
const em = (text, o = {}) => new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, font: "Calibri", size: 21, language: LANG, ...o })] });
const email = [
  em("Tárgy: Ajánlat – FLINS mintaház tartószerkezeti tervezése (STEELXPERT 2026.032a)", { bold: true }),
  em("Címzett: Szabó András (szabo.andras@flins.hu); másolat: Kalászi Balázs", { color: GRAY, size: 19 }),
  em("Csatolmányok: 2026.032a_FLINS_mintahaz_ajanlat_rev0.pdf; FLINS_mintahaz_3D_vazmodell.html", { color: GRAY, size: 19 }),
  em("Szia András!"),
  em("Csatolom az ajánlatot a mintaház tartószerkezeti tervezésére, ahogy a keddi megbeszélésen szó volt róla " +
     "(2026.032a_FLINS_mintahaz_ajanlat_rev0.pdf), és mellé a ház 3D vázmodelljét (FLINS_mintahaz_3D_vazmodell.html)."),
  em("A HTML-t mentsd le, és dupla kattintással nyisd meg bármelyik böngészőben; nem kell hozzá telepítés, internet sem. " +
     "Egérrel forgatható, görgővel nagyítható, a bal oldali listából a részletek (eresz, gerinc, keretsarok, oromfal, " +
     "galéria, padlóváz) külön is megnézhetők. Minden méret még előzetes, a modell a koncepciót mutatja."),
  em("Röviden a lényeg, a részletek az ajánlatban: a csupasz acélváz teljes Eurocode szerinti tervezése STEP modellel és " +
     "magyar nyelvű statikai dokumentációval, 163 mérnökóra, 2 445 000 Ft + ÁFA átalányár, 4 hét a megrendeléstől."),
  em("Ha kérdés van, hívj."),
  em("Üdv,"),
  em("Csaba"),
  em("Bán Csaba | STEELXPERT Kft. | info@steelxpert.com", { color: GRAY, size: 19 }),
];

function build(children, file, title, page) {
  const doc = new Document({
    creator: CREATOR, lastModifiedBy: CREATOR, title, styles, numbering,
    sections: [{ properties: { page }, children }],
  });
  return Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(file, buf); console.log("written:", file); });
}
const A4 = (m) => ({ size: { width: 11906, height: 16838 }, margin: m });
build(letter, "2026.032a_FLINS_mintahaz_ajanlat_rev0.docx", "Ajánlat – FLINS mintaház tartószerkezeti tervezése",
  A4({ top: 560, right: 1000, bottom: 560, left: 1000 }))
  .then(() => build(email, "DRAFT/2026.032a_email_draft_rev0.docx", "Kísérő e-mail – FLINS mintaház ajánlat",
  A4({ top: 1134, right: 1134, bottom: 1134, left: 1134 })));
