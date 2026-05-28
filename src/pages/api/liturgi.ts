export const prerender = false;

// Standard Catholic/Indonesian Bible book abbreviations mapped to internal Pelita IDs
const bookMapping: Record<string, string> = {
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

export async function GET({ url }) {
  const d = url.searchParams.get("d") || "0";
  const targetUrl = `https://www.imankatolik.or.id/kalender_share_kecil.php?d=${encodeURIComponent(d)}`;

  try {
    const res = await fetch(targetUrl);
    if (!res.ok) {
      throw new Error(`Failed to fetch from imankatolik.or.id: ${res.statusText}`);
    }

    const html = await res.text();

    // 1. Parse Date
    // Format in HTML: <a href="/kalender/...html" style="font-size:12px;text-decoration:none;color:#000000" target="_blank"><b>29 Mei 2026</b></a>
    const dateMatch = html.match(/font-size:12px;[^>]*><b>(.*?)<\/b>/i);
    const dateStr = dateMatch ? dateMatch[1].trim() : "Tanggal Tidak Diketahui";

    // 2. Parse Saint/Feast Day name
    // Format in HTML: <a href="/kalender/29Mei.html" style="text-decoration:none" target="_blank"><b>St. Paulus VI</b></a>
    const saintMatch = html.match(/href="\/kalender\/[^"]+" style="text-decoration:none"[^>]*><b>(.*?)<\/b>/i);
    const saintStr = saintMatch ? saintMatch[1].trim() : "Hari Biasa";

    // 3. Parse Liturgical Color
    // Format in HTML: <td class="c s">Warna Liturgi Hijau</td>
    const colorMatch = html.match(/Warna Liturgi\s+([A-Za-z]+)/i);
    const colorStr = colorMatch ? colorMatch[1].trim() : "Hijau";

    // 4. Parse Readings
    // Format in HTML: <a href="/alkitabq.php?q=..." ...>...</a>
    // We want to extract each anchor link under the readings container
    const readings: any[] = [];
    const linkRegex = /<a href="\/alkitabq\.php\?q=([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
    let match;

    while ((match = linkRegex.exec(html)) !== null) {
      const rawQuery = match[1]; // e.g. "1Ptr4:7-13;" or "Mzm96:10;Mzm96:11-12;"
      const text = match[2].trim(); // e.g. "1Ptr 4:7-13" or "Mzm 96:10.11-12.13"

      // Determine if this is Office of Readings (Bacaan Offisi / BcO)
      // Check if "BcO" is within 15 characters before the link in the HTML
      const matchIndex = match.index;
      const precedingText = html.substring(Math.max(0, matchIndex - 15), matchIndex);
      const isBcO = /BcO/i.test(precedingText);

      // Parse the first book & chapter from the query to build internal link
      // Query pattern: book abbreviation followed by chapter, e.g. "1Ptr4" or "Mzm96"
      const queryParse = rawQuery.match(/^([1-3]?[A-Za-z]+)\s*(\d+)/i);
      let internalLink = null;
      let bookId = null;
      let chapter = null;
      let startVerse = null;

      if (queryParse) {
        const rawBook = queryParse[1].toLowerCase();
        chapter = parseInt(queryParse[2]);
        bookId = bookMapping[rawBook] || null;

        // Extract starting verse if present (e.g., from :7-13)
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

    return new Response(
      JSON.stringify({
        date: dateStr,
        celebration: saintStr,
        liturgicalColor: colorStr,
        readings
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "public, max-age=3600" // Cache for 1 hour
        }
      }
    );
  } catch (error: any) {
    console.error("[Liturgi Proxy Error]:", error);
    return new Response(
      JSON.stringify({ error: "Internal Server Error", details: error.message }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" }
      }
    );
  }
}
