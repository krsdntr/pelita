async function run() {
  try {
    const res = await fetch("https://www.imankatolik.or.id/kalender_share_kecil.php");
    const html = await res.text();
    console.log(html);
  } catch (err) {
    console.error(err);
  }
}
run();
