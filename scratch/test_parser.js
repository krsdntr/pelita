const bookMapping = {
  "kej": "kej", "kel": "kel", "im": "im", "bil": "bil", "ul": "ul", "yos": "yos",
  "hak": "hak", "rut": "rut", "1sam": "1sam", "2sam": "2sam", "1raj": "1raj",
  "2raj": "2raj", "1taw": "1taw", "2taw": "2taw", "ezr": "ezr", "neh": "neh",
  "est": "est", "ayb": "ayb", "mzm": "maz", "ams": "ams", "pkh": "pkh",
  "kid": "kid", "yes": "yes", "yer": "yer", "rat": "rat", "yeh": "yeh",
  "dan": "dan", "hos": "hos", "yoel": "yoel", "amos": "amos", "ob": "ob",
  "yun": "yun", "mik": "mik", "nah": "nah", "hab": "hab", "zef": "zef",
  "hag": "hag", "zak": "zak", "mal": "mal",
  "tob": "tob", "yud": "yud", "t-est": "t-est", "keb": "keb", "sir": "sir",
  "bar": "bar", "t-dan": "t-dan", "1mak": "1mak", "2mak": "2mak",
  "mat": "mat", "mrk": "mrk", "luk": "luk", "yoh": "yoh", "kis": "kis",
  "rm": "rm", "1kor": "1kor", "2kor": "2kor", "gal": "gal", "ef": "ef",
  "flp": "flp", "kol": "kol", "1tes": "1tes", "2tes": "2tes", "1tim": "1tim",
  "2tim": "2tim", "tit": "tit", "flm": "flm", "ibr": "ibr", "yak": "yak",
  "1ptr": "1ptr", "2ptr": "2ptr", "1yoh": "1yoh", "2yoh": "2yoh", "3yoh": "3yoh",
  "yudas": "yud-sb", "why": "why"
};

async function test() {
  const html = `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
html,body{margin:0;padding:0;height:100%;border:none}
body{background-color:#ffffff;font-family:Verdana, Arial, Helvetica, sans-serif;font-size:11px};
.t1,.t2{border-color:#000;border-style:solid;}
.t1{border-width: 0 0 1px 1px;border-spacing:0;border-collapse:collapse;width:100%}
.t2{margin:0;padding:1px;border-width:1px 1px 0 0;}
.c{text-align:center}
.s{font-size:9px}
</style></head>
<body>
<table class="t1" cellspacing="0" border="1" height="100%"><tr height="1%"><td class="t2 c">Kalender Liturgi hari ini<br />
<b><small><a href="http://www.imankatolik.or.id" target="_blank">imankatolik.or.id</a></small></b></td></tr><tr height="1%"><td class="t2 c"><a href="/kalender/29Mei.html" style="font-size:12px;text-decoration:none;color:#000000" target="_blank"><b>29 Mei 2026</b></a></td></tr>
<tr height="60%"><td class="t2"><table width="100%">
<tr><td class="c"><a href="/kalender/29Mei.html" style="text-decoration:none" target="_blank"><b>St. Paulus VI</b></a></td></tr><tr><td>
<div class="c"><small><a href="/alkitabq.php?q=1Ptr4:7-13;" target="_blank">1Ptr 4:7-13</a>; <a href="/alkitabq.php?q=Mzm96:10;Mzm96:11-12;Mzm96:13;" target="_blank">Mzm 96:10.11-12.13</a>; <a href="/alkitabq.php?q=Mrk11:11-26;" target="_blank">Mrk 11:11-26</a>. <br />
BcO <a href="/alkitabq.php?q=2Kor11:30-99;2Kor12:1-13;" target="_blank">2Kor 11:30-12:13</a></small></div></td></tr><tr><td>
<table style="width:100%"><tr><td class="c s">
<a href="/kalender_share_kecil.php?d=-1&i=" style="text-decoration:none">◄</a></td><td class="c s">Warna Liturgi Hijau</td><td class="c s"><a href="/kalender_share_kecil.php?d=1&i=" style="text-decoration:none">►</a></td></tr></table></td></tr></table></td></tr><tr height="1%"><td class="t2 c s"><a href="/kalender.php?b=5&t=2026" target="_blank">Kalender bulan Mei 2026</a></td></tr></table>
</body>
</html>`;

  const dateMatch = html.match(/font-size:12px;[^>]*><b>(.*?)<\/b>/i);
  const dateStr = dateMatch ? dateMatch[1].trim() : "Tanggal Tidak Diketahui";
  console.log("Date:", dateStr);

  const saintMatch = html.match(/href="\/kalender\/[^"]+" style="text-decoration:none"[^>]*><b>(.*?)<\/b>/i);
  const saintStr = saintMatch ? saintMatch[1].trim() : "Hari Biasa";
  console.log("Saint:", saintStr);

  const colorMatch = html.match(/Warna Liturgi\s+([A-Za-z]+)/i);
  const colorStr = colorMatch ? colorMatch[1].trim() : "Hijau";
  console.log("Color:", colorStr);

  const readings = [];
  const linkRegex = /<a href="\/alkitabq\.php\?q=([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
  let match;

  while ((match = linkRegex.exec(html)) !== null) {
    const rawQuery = match[1];
    const text = match[2].trim();

    const matchIndex = match.index;
    const precedingText = html.substring(Math.max(0, matchIndex - 15), matchIndex);
    const isBcO = /BcO/i.test(precedingText);

    const queryParse = rawQuery.match(/^([1-3]?[A-Za-z]+)\s*(\d+)/i);
    let internalLink = null;
    let bookId = null;
    let chapter = null;
    let startVerse = null;

    if (queryParse) {
      const rawBook = queryParse[1].toLowerCase();
      chapter = parseInt(queryParse[2]);
      bookId = bookMapping[rawBook] || null;

      const verseMatch = rawQuery.match(/:(\d+)/);
      if (verseMatch) {
        startVerse = parseInt(verseMatch[1]);
      }

      if (bookId && chapter) {
        internalLink = `/read/${bookId}/${chapter}${startVerse ? `?v=${startVerse}` : ''}`;
      }
    }

    readings.push({
      text,
      isBcO,
      rawQuery,
      internalLink,
      bookId,
      chapter,
      startVerse
    });
  }

  console.log("Readings:", JSON.stringify(readings, null, 2));
}

test();
