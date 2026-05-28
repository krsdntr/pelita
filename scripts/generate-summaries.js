import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const metadataPath = path.join(__dirname, '../src/data/bible-metadata.json');
const outputPath = path.join(__dirname, '../src/data/catholic-summaries.json');

const books = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));

// Detail Manual Khusus untuk 9 Kitab Pilar Utama (Sangat Mendalam)
const manualSummaries = {
  kej: {
    quote: "Pada mulanya Allah menciptakan langit dan bumi.",
    tagline: "Benih Awal Mula Sejarah Keselamatan dan Perjanjian Allah",
    overview: "Kitab Kejadian adalah pintu gerbang Alkitab yang agung. Kitab ini meletakkan dasar bagi seluruh sejarah keselamatan, menceritakan asal mula dunia, manusia, kejatuhan ke dalam dosa, dan awal mula ikatan Perjanjian Allah dengan umat pilihan-Nya melalui para Bapa Bangsa.",
    author: "Musa (Tradisi Pentateukh) / Dikompilasi dari tradisi Yahwis, Elohis, Deuteronomis, dan Imamat.",
    date: "Abad ke-15 s.d. ke-6 SM",
    context: "Ditulis untuk memberikan identitas iman yang teguh bagi bangsa Israel di tengah pengaruh politeisme bangsa-bangsa di sekitar mereka, menegaskan bahwa Allah Israel adalah pencipta tunggal yang berdaulat atas segalanya.",
    theology: "1. **Penciptaan yang Baik:** Allah menciptakan segalanya dari ketiadaan (*creatio ex nihilo*) semata-mata karena cinta (Bdk. KGK 293-295).\n2. **Gambar dan Rupa Allah:** Manusia diciptakan sebagai ciptaan yang bermartabat tinggi, pria dan wanita yang setara (Bdk. KGK 355-358).\n3. **Dosa Asal:** Kejatuhan manusia pertama akibat kesombongan dan janji penebusan (*Protoevangelium* di Kej 3:15).\n4. **Tipologi Kristus:** Adam sebagai tipe Kristus (Adam Baru); Ishak yang dikurbankan di bukit Moria meramalkan penyerahan Yesus di Golgota.",
    structure: [
      { chapters: "1 - 11", title: "Sejarah Purba", summary: "Penciptaan dunia dalam enam hari, penciptaan Adam dan Hawa, kejatuhan dalam dosa (Kej 3), pembunuhan Habel oleh Kain, Air Bah zaman Nuh, dan kesombongan Menara Babel." },
      { chapters: "12 - 25", title: "Kisah Abraham", summary: "Panggilan Abraham keluar dari tanah leluhurnya, janji Allah akan keturunan dan tanah pusaka, ujian pengurbanan Ishak, serta penetapan tanda sunat sebagai tanda Perjanjian." },
      { chapters: "26 - 36", title: "Kisah Ishak dan Yakub", summary: "Pemberkatan Yakub yang merebut hak kesulungan dari Esau, mimpi Yakub di Betel (tangga ke surga), pergulatan Yakub dengan Allah hingga namanya diganti menjadi Israel, dan lahirnya 12 suku Israel." },
      { chapters: "37 - 50", title: "Kisah Yusuf dan Pindah ke Mesir", summary: "Yusuf yang dijual saudaranya karena cemburu, penafsir mimpi Firaun di Mesir, rekonsiliasi Yusuf dengan saudara-saudaranya di masa kelaparan, dan kepindahan seluruh keluarga Yakub ke tanah Gosyen, Mesir." }
    ],
    goldenVerses: [
      { verse: "Kejadian 1:1", text: "Pada mulanya Allah menciptakan langit dan bumi.", reflection: "Menegaskan iman bahwa alam semesta bukanlah kebetulan, melainkan buah kasih dan kehendak bebas Allah pencipta." },
      { verse: "Kejadian 3:15", text: "Aku akan mengadakan permusuhan antara engkau dan perempuan ini, antara keturunanmu dan keturunannya; keturunannya akan meremukkan kepalamu...", reflection: "Dikenal sebagai *Protoevangelium* (Injil Pertama), ramalan awal tentang kemenangan Kristus (keturunan perempuan) bersama Maria atas kuasa iblis." },
      { verse: "Kejadian 50:20", text: "Memang kamu telah mereka-rekakan yang jahat terhadap aku, tetapi Allah telah mereka-rekakannya untuk kebaikan...", reflection: "Mengajarkan kita tentang penyelenggaraan ilahi (*Providentia Dei*), di mana Allah mampu meluruskan garis yang bengkok demi rencana penyelamatan-Nya." }
    ]
  },
  kel: {
    quote: "Aku adalah AKU YANG AKU ADA.",
    tagline: "Pembebasan dari Perbudakan, Paskah Pertama, dan Perjanjian Gunung Sinai",
    overview: "Kitab Keluaran menceritakan peristiwa paling mendasar dalam sejarah Israel: pembebasan dahsyat dari perbudakan Mesir di bawah pimpinan Musa, penetapan Paskah pertama, penyeberangan Laut Merah, dan ikatan kovenan agung di Gunung Sinai di mana Allah memberikan Sepuluh Perintah-Nya.",
    author: "Musa / Dikompilasi dari tradisi Pentateukh.",
    date: "Abad ke-15 s.d. ke-6 SM",
    context: "Ditulis untuk menegaskan kovenan unik Israel dengan Yahweh, menunjukkan bahwa Allah mendengar jeritan umat-Nya dan setia pada janji-Nya kepada para leluhur.",
    theology: "1. **Pembebasan Paskah:** Anak Domba Paskah yang darahnya menyelamatkan Israel meramalkan secara sempurna Yesus Kristus sebagai Anak Domba Allah sejati yang menghapus dosa dunia (Bdk. KGK 1362-1364).\n2. **Sepuluh Firman (Dekalog):** Sepuluh Perintah Allah diberikan di Gunung Sinai sebagai hukum kemerdekaan dan kasih untuk menuntun umat hidup dalam kekudusan (Bdk. KGK 2056-2063).\n3. **Tabut Perjanjian & Kemah Suci:** Allah menyatakan keinginan-Nya untuk bersemayam secara konkret di tengah umat-Nya.\n4. **Tipologi Penyelamatan:** Penyeberangan Laut Merah meramalkan Sakramen Pembaptisan; pemberian makanan Manna di padang gurun meramalkan Sakramen Ekaristi Mahakudus.",
    structure: [
      { chapters: "1 - 15", title: "Penindasan dan Paskah Pembebasan", summary: "Penindasan bangsa Israel di Mesir, pemeliharaan bayi Musa, panggilan semak menyala (Kel 3), sepuluh tulah dahsyat, Paskah pertama, penyeberangan Laut Merah, dan nyanyian syukur." },
      { chapters: "16 - 18", title: "Perjalanan Padang Gurun", summary: "Keluh kesah Israel di padang gurun Sin, mukjizat pemberian roti Manna dan burung puyuh, aliran air dari bukit batu di Masa dan Meriba, serta penataan kepemimpinan oleh Yitro." },
      { chapters: "19 - 24", title: "Perjanjian Gunung Sinai", summary: "Kedatangan umat di Sinai, teofani badai petir kemuliaan Allah, Sepuluh Perintah Allah (Dekalog), Kitab Perjanjian, dan upacara ratifikasi Perjanjian dengan darah kurban." },
      { chapters: "25 - 40", title: "Pembangunan Kemah Suci", summary: "Instruksi pembangunan Tabut Perjanjian dan mezbah, dosa penyembahan anak lembu emas (Kel 32), pembaharuan loh batu, pengerjaan Kemah Suci, dan turunnya kemuliaan TUHAN memenuhi Kemah Suci." }
    ],
    goldenVerses: [
      { verse: "Keluaran 3:14", text: "Firman Allah kepada Musa: 'AKU ADALAH AKU.' Lagi firman-Nya: 'Beginilah kaukatakan kepada orang Israel: AKU ADALAH telah mengutus aku kepadamu.'", reflection: "Penyataan Nama Suci Allah yang menakjubkan, menegaskan keberadaan-Nya yang kekal, berdaulat, dan selalu hadir menyertai peziarahan manusia." },
      { verse: "Keluaran 12:13", text: "Dan darah itu menjadi tanda bagimu pada rumah-rumah di mana kamu tinggal: Apabila Aku melihat darah itu, maka Aku akan melewati kamu...", reflection: "Darah anak domba Paskah yang menyelamatkan umat Israel meramalkan Paskah Baru: Darah Kristus yang tercurah di salib menyelamatkan kita dari maut rohani." },
      { verse: "Keluaran 20:2-3", text: "Akulah TUHAN, Allahmu, yang membawa engkau keluar dari tanah Mesir, dari tempat perbudakan. Jangan ada padamu allah lain di hadapan-Ku.", reflection: "Pangkal utama dari Sepuluh Firman Allah, menuntut kesetiaan kasih dan penyembahan tunggal kepada satu-satunya Allah pemberi kemerdekaan sejati." }
    ]
  },
  maz: {
    quote: "TUHAN adalah gembalaku, takkan kekurangan aku.",
    tagline: "Nyanyian Jiwa, Tangisan Ratapan, dan Pujian Abadi Gereja",
    overview: "Kitab Mazmur adalah kumpulan 150 doa puisi liturgis yang menjadi jantung dari doa resmi Gereja Katolik. Mazmur mengekspresikan seluruh spektrum emosi manusia di hadapan Allah—dari keputusasaan yang terdalam hingga sukacita yang meluap-luap.",
    author: "Raja Daud (73 mazmur), Asaf, Bani Korah, Salomo, Musa, dan penulis anonim lainnya.",
    date: "Abad ke-10 s.d. ke-5 SM",
    context: "Digunakan sebagai buku nyanyian resmi dalam ibadat bait suci Yerusalem dan di sinagoga-sinagoga Yahudi pasca-pembuangan.",
    theology: "1. **Liturgi Gereja:** Mazmur menjadi dasar doa *Horarium* (Ibadat Harian / Brevir) bagi para imam, biarawan-biarawati, dan kaum awam di seluruh dunia (Bdk. KGK 2585-2589).\n2. **Nubuat Kristologis:** Banyak mazmur yang meramalkan secara detail kehidupan, penderitaan, dan kebangkitan Yesus (Bdk. Maz 22 tentang Sengsara, Maz 110 tentang Imamat Kristus).\n3. **Doa Dialogis:** Allah menginspirasikan teks-teks mazmur agar manusia tahu bagaimana cara berbicara dan berdoa kepada-Nya dalam segala situasi.",
    structure: [
      { chapters: "1 - 41", title: "Buku I (Mazmur 1-41)", summary: "Banyak berpusat pada doa pribadi Daud, pergulatan melawan musuh, dan penegasan tentang kebahagiaan orang yang setia pada Taurat Allah (Maz 1 & 23)." },
      { chapters: "42 - 72", title: "Buku II (Mazmur 42-72)", summary: "Didominasi oleh nyanyian Bani Korah dan Asaf, diakhiri dengan doa keagungan bagi kerajaan Salomo yang merujuk pada Kerajaan Mesias masa depan (Maz 72)." },
      { chapters: "73 - 89", title: "Buku III (Mazmur 73-89)", summary: "Fokus pada doa-doa komunitas dalam masa krisis nasional, kehancuran Yerusalem, dan permohonan agar Allah mengingat kembali janji setia-Nya kepada Daud." },
      { chapters: "90 - 106", title: "Buku IV (Mazmur 90-106)", summary: "Menekankan kedaulatan Allah atas seluruh bumi. Di buka dengan Mazmur Musa (Maz 90) yang merenungkan kefanaan manusia di hadapan keabadian Allah." },
      { chapters: "107 - 150", title: "Buku V (Mazmur 107-150)", summary: "Buku pujian agung, berisi Mazmur ziarah (*Hallel*) yang dinyanyikan saat mendaki bait suci, dan diakhiri dengan doxology megah (Maz 150) yang mengajak seluruh ciptaan memuji TUHAN." }
    ],
    goldenVerses: [
      { verse: "Mazmur 23:1", text: "TUHAN adalah gembalaku, takkan kekurangan aku.", reflection: "Sebuah deklarasi iman yang murni akan perlindungan dan pemeliharaan pribadi Allah yang lembut laksana gembala yang baik." },
      { verse: "Mazmur 22:2", text: "Allahku, Allahku, mengapa Engkau meninggalkan aku?", reflection: "Kata-kata ratapan Daud yang diucapkan Yesus di atas kayu salib. Mazmur ini bukan tentang keputusasaan, melainkan nubuat kemenangan puncak atas penderitaan." },
      { verse: "Mazmur 119:105", text: "Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.", reflection: "Ketetapan hati untuk selalu menuntun langkah hidup sehari-hari menggunakan petunjuk hukum kasih Allah." }
    ]
  },
  keb: {
    quote: "Jiwa orang benar ada di tangan Allah, dan siksaan tiada akan menjamah mereka.",
    tagline: "Keindahan Kebijaksanaan Ilahi, Keadilan Kovenan, dan Pengharapan Keabadian",
    overview: "Kitab Kebijaksanaan Salomo adalah mutiara sastra kebijaksanaan Deuterokanonika. Ditulis dengan bahasa Yunani yang indah, kitab ini membela iman monoteisme Yahudi dari pengaruh paganisme helenistik dengan memaparkan nilai luhur Kebijaksanaan Ilahi, keadilan kovenan, dan kepastian kebangkitan jiwa-jiwa orang benar.",
    author: "Seorang Yahudi yang terpelajar di Aleksandria (tradisi menyematkan nama Salomo sebagai personifikasi hikmat).",
    date: "Sekitar tahun 100 s.d. 50 SM",
    context: "Ditulis bagi komunitas Yahudi di perantauan Mesir (Aleksandria) yang menghadapi tekanan budaya filsafat pagan helenistik dan penindasan iman.",
    theology: "1. **Keabadian Jiwa:** Kitab ini memberikan salah satu dasar biblis paling jelas dalam Alkitab mengenai keabadian jiwa manusia dan keadilan Allah di kehidupan kekal (Bdk. Keb 3:1-3).\n2. **Kebijaksanaan sebagai Roh Kudus:** Kebijaksanaan dipersonifikasikan sebagai pancaran kemuliaan Allah, cermin murni karya-Nya, yang aktif menuntun sejarah keselamatan.\n3. **Filsafat dan Iman:** Menggunakan konsep filsafat Yunani untuk menjelaskan kebenaran teologi Yahudi-Kristen secara universal.\n4. **Typology Sengsara:** Nubuat luar biasa tentang kaum fasik yang membenci orang benar karena menegur dosa mereka, meramalkan secara detail perlakuan terhadap Yesus (Keb 2:12-20).",
    structure: [
      { chapters: "1 - 5", title: "Keadilan dan Keabadian Jiwa", summary: "Kontras nasib kekal antara orang benar dan orang fasik. Orang benar diyakini tetap berada dalam pemeliharaan kasih tangan Allah meskipun secara jasmani wafat sengsara." },
      { chapters: "6 - 9", title: "Personifikasi Kebijaksanaan Ilahi", summary: "Pujian agung bagi Kebijaksanaan, asal-usul keilahiannya, doa Salomo memohon karunia Kebijaksanaan untuk memerintah dengan adil, dan deskripsi sifat-sifat rohaninya." },
      { chapters: "10 - 19", title: "Kebijaksanaan dalam Sejarah Keselamatan", summary: "Bagaimana Kebijaksanaan memandu para tokoh iman (Adam s.d. Musa), penyelamatan Israel saat eksodus, perbandingan tulah Mesir dengan berkat bagi Israel, serta kritik keras terhadap penyembahan berhala." }
    ],
    goldenVerses: [
      { verse: "Kebijaksanaan 3:1-2", text: "But the souls of the righteous are in the hand of God, and no torment will ever touch them...", reflection: "Teks liturgis agung pembacaan Misa Arwah Katolik, menegaskan iman tak tergoyahkan bahwa kematian fisik bagi orang beriman hanyalah jalan menuju perdamaian kekal Allah." },
      { verse: "Kebijaksanaan 2:12", text: "Let us lie in wait for the righteous man, because he is inconvenient to us and opposes our actions...", reflection: "Tipologi sengsara yang mencengangkan: kaum fasik berkomplot menganiaya orang benar karena menolak berkompromi dengan dosa, terpenuhi sempurna pada pengadilan Yesus." },
      { verse: "Kebijaksanaan 7:26", text: "Sebab ia merupakan pantulan cahaya kekal, dan cermin tak bernoda dari kegiatan Allah, dan gambar kebaikan-Nya.", reflection: "Menjelaskan hakikat murni hikmat ilahi yang dalam Perjanjian Baru mewujud secara utuh dalam diri Yesus Kristus sebagai rupa Allah yang nyata." }
    ]
  },
  yes: {
    quote: "Sebab seorang anak telah lahir untuk kita, seorang putera telah diberikan untuk kita.",
    tagline: "Injil Kelima: Nubuat Agung Sang Mesias dan Hamba yang Menderita",
    overview: "Sering disebut sebagai 'Injil Kelima' oleh Bapa Gereja Santo Hieronimus, Kitab Yesaya adalah mahakarya sastra kenabian yang paling banyak dikutip dalam Perjanjian Baru. Kitab ini menyingkapkan kekudusan Allah yang absolut, nubuat kelahiran dan penderitaan Mesias, serta visi keselamatan universal bagi segala bangsa.",
    author: "Nabi Yesaya bin Amos dan para murid sekolah kenabian Yesaya (Deutero-Yesaya & Trito-Yesaya).",
    date: "Abad ke-8 s.d. ke-5 SM",
    context: "Ditulis di tengah ancaman invasi kekaisaran Asyur dan pembuangan Babel, untuk memanggil Yehuda kembali ke jalan keadilan serta memberikan pengharapan penghiburan ilahi.",
    theology: "1. **Nubuat Immanuel:** Menubuatkan kelahiran Mesias dari seorang perawan (Yes 7:14) yang akan disebut Allah Beserta Kita (Bdk. KGK 712).\n2. **Nyanyian Hamba yang Menderita:** Gambaran nubuat paling detail tentang sengsara, wafat, dan kebangkitan Yesus demi menebus dosa manusia (Yes 52:13 - 53:12).\n3. **Kekudusan Allah:** Gelar khas 'Yang Mahakudus, Allah Israel' dan seruan para Seraphim 'Kudus, Kudus, Kudus' (Yes 6:3) yang kita nyanyikan dalam setiap Misa Kudus (Prefasi).\n4. **Misi Universal:** Keselamatan Allah merangkul bangsa-bangsa non-Yahudi, menjadikan bait Allah sebagai rumah doa bagi segala bangsa.",
    structure: [
      { chapters: "1 - 39", title: "Kitab Penghakiman (Yesaya Historis)", summary: "Nubuat penghakiman atas Yehuda dan bangsa-bangsa kafir, nubuat kelahiran Immanuel, teofani panggilan Yesaya, dan janji keselamatan sisa Israel." },
      { chapters: "40 - 55", title: "Kitab Penghiburan (Deutero-Yesaya)", summary: "Seruan penghiburan bagi umat di pembuangan Babel, janji pembebasan, kedaulatan monoteisme Allah Yahweh, dan Nyanyian Hamba yang Menderita." },
      { chapters: "56 - 66", title: "Harapan Yerusalem Baru (Trito-Yesaya)", summary: "Pengajaran bagi umat setelah kembali ke Yerusalem, panggilan keadilan sosial, janji langit baru dan bumi baru, serta pemuliaan Yerusalem baru yang merangkul segala bangsa." }
    ],
    goldenVerses: [
      { verse: "Yesaya 7:14", text: "Sebab itu Tuhan sendirilah yang akan memberikan kepadamu suatu pertanda: Sesungguhnya, seorang perempuan muda mengandung dan akan melahirkan seorang anak laki-laki, dan ia akan menamakan Dia Imanuel.", reflection: "Nubuat mesianik agung tentang Inkarnasi Yesus Kristus yang lahir dari Santa Perawan Maria, menegaskan kehadiran penyertaan Allah di dunia." },
      { verse: "Yesaya 9:5", text: "Sebab seorang anak telah lahir untuk kita, seorang putera telah diberikan untuk kita; lambang pemerintahan ada di atas bahunya, dan namanya disebutkan orang: Penasihat Ajaib, Allah yang Perkasa, Bapa yang Kekal, Raja Damai.", reflection: "Klimaks nubuat sukacita Natal, menyatakan sifat-sifat ilahi sang Mesias yang membawa pemerintahan damai sejahtera abadi." },
      { verse: "Yesaya 53:5", text: "Tetapi dia tertikam oleh karena pemberontakan kita, dia diremukkan oleh karena kejahatan kita; ganjaran yang mendatangkan keselamatan bagi kita ditimpakan kepadanya, dan oleh bilur-bilurnya kita menjadi sembuh.", reflection: "Nubuat agung sengsara Jumat Agung, menjelaskan makna pengurbanan silih Kristus di kayu salib demi kesembuhan dan pengampunan dosa umat manusia." }
    ]
  },
  luk: {
    quote: "Sesungguhnya aku ini adalah hamba Tuhan; jadilah padaku menurut perkataanmu.",
    tagline: "Kabar Gembira Kerahiman Allah, Peran Penting Maria, dan Kehadiran Roh Kudus",
    overview: "Injil Lukas adalah kabar gembira yang menekankan belas kasih, kerahiman Allah bagi kaum marginal (miskin, wanita, pendosa), dan peran sentral Roh Kudus. Lukas juga menyajikan informasi terlengkap mengenai masa kecil Yesus, menjadikannya Injil yang sangat kaya akan tradisi devosional Maria Katolik.",
    author: "Santo Lukas (Tabib, rekan seperjalanan Santo Paulus, pelukis tradisi Maria).",
    date: "Sekitar tahun 80 s.d. 85 M",
    context: "Ditulis untuk Teofilus (artinya pencinta Allah) dan umat Kristen keturunan non-Yahudi (Yunani) agar mereka yakin akan kepastian ajaran iman yang telah diterima.",
    theology: "1. **Dimensi Maria (Marian):** Berisi fondasi doa *Salam Maria* (Kabar Sukacita di Luk 1:28 dan Kunjungan Maria di Luk 1:42) serta kidung *Magnificat* (Luk 1:46-55).\n2. **Kerahiman Allah (Mercy):** Menyimpan perumpamaan kerahiman yang sangat indah seperti *Kisah Anak yang Hilang* (Luk 15) dan *Kisah Samaria yang Murah Hati* (Luk 10).\n3. **Sakramen & Liturgi:** Penampakan di Emmaus (Luk 24) menguraikan liturgi sabda dan pemecahan roti (Ekaristi).\n4. **Roh Kudus:** Menyoroti bagaimana seluruh kehidupan Yesus dan Gereja perdana didorong oleh kuasa dinamis Roh Kudus.",
    structure: [
      { chapters: "1 - 2", title: "Kisah Kanak-Kanak Yesus", summary: "Kabar malaikat kepada Zakharia dan Maria (Annunsiasi), perkunjungan Maria kepada Elisabet (Visitasi), kelahiran Yohanes Pembaptis dan Yesus di Betlehem, serta persembahan Yesus di Bait Allah." },
      { chapters: "3 - 9", title: "Karya Pelayanan di Galilea", summary: "Pembaptisan Yesus, pencobaan di padang gurun, khotbah di Nazaret, mukjizat-mukjizat penyembuhan, panggilan para rasul, dan Transfigurasi (Yesus menampakkan kemuliaan-Nya)." },
      { chapters: "9 - 19", title: "Perjalanan Teologis ke Yerusalem", summary: "Sebagian besar isi Injil Lukas menceritakan perjalanan Yesus menuju salib-Nya di Yerusalem, sarat dengan perumpamaan kasih, tobat, dan doa khusyuk." },
      { chapters: "19 - 24", title: "Sengsara, Wafat, dan Kebangkitan", summary: "Pembersihan Bait Allah, Perjamuan Malam Terakhir, Sengsara di Gethsemani, Wafat di Kalvari, penemuan kubur kosong, penampakan di jalan menuju Emaus, dan Kenaikan ke surga." }
    ],
    goldenVerses: [
      { verse: "Lukas 1:38", text: "Kata Maria: 'Sesungguhnya aku ini adalah hamba Tuhan; jadilah padaku menurut perkataanmu.' Lalu malaikat itu meninggalkan dia.", reflection: "Deklarasi ketaatan mutlak Maria (*Fiat*), teladan iman Katolik tertinggi dalam bekerja sama secara aktif dengan kehendak keselamatan Allah." },
      { verse: "Lukas 1:46-47", text: "Lalu kata Maria: 'Jiwaku memuliakan Tuhan, dan hatiku bergembira karena Allah, Juruselamatku...'", reflection: "Awal dari kidung *Magnificat*, madah pujian Santa Perawan Maria yang melambungkan rasa syukur atas belas kasih Allah kepada kaum yang rendah." },
      { verse: "Lukas 15:20", text: "Maka bangkitlah ia dan pergi kepada ayahnya. Ketika ia masih jauh, ayahnya telah melihatnya, lalu tergeraklah hatinya oleh belas kasihan...", reflection: "Inti belas kasih ilahi dalam perumpamaan Anak yang Hilang, menyatakan kerahiman tak terbatas Allah Bapa yang selalu merindukan kembalinya pendosa." }
    ]
  },
  yoh: {
    quote: "Pada mulanya adalah Firman; Firman itu bersama-sama dengan Allah dan Firman itu adalah Allah.",
    tagline: "Penglihatan Mistik tentang Inkarnasi, Sakramen, dan Keilahian Yesus",
    overview: "Injil Yohanes berbeda secara mencolok dari tiga Injil Sinoptik lainnya. Ditulis dengan gaya teologis-mistik yang mendalam, Injil ini menyatakan keilahian Yesus Kristus secara eksplisit sebagai Sang *Logos* (Sabda) yang kekal dan menjadi manusia.",
    author: "Santo Yohanes Penginjil (Murid yang Dikasihi Yesus)",
    date: "Sekitar tahun 90 s.d. 100 M",
    context: "Ditulis di Efesus bagi jemaat Kristen generasi awal yang menghadapi tantangan bidah gnostisisme (yang menyangkal kemanusiaan nyata Yesus) dan pengusiran dari sinagoga Yahudi.",
    theology: "1. **Keilahian Kristus:** Yesus adalah Sabda yang setara dengan Allah, yang menyatakan diri lewat tujuh pernyataan agung 'Akulah' (*I Am*).\n2. **Teologi Sakramen:** Yohanes sarat dengan simbolisme sakramen (Ekaristi di Yoh 6, Baptisan di Yoh 3 dengan air dan Roh, Imamat dan Rekonsiliasi di Yoh 20).\n3. **Cinta Kasih Persaudaraan:** Hukum Baru untuk saling mengasihi seperti Kristus telah mengasihi kita (Yoh 13:34).\n4. **Parakletos:** Janji pengutusan Roh Kudus Sang Penghibur yang akan menuntun Gereja dalam kebenaran penuh.",
    structure: [
      { chapters: "1", title: "Prolog Keabadian", summary: "Pernyataan teologis agung bahwa Yesus adalah Sabda kekal yang menjelma menjadi manusia (Yoh 1:14), disusul kesaksian Yohanes Pembaptis." },
      { chapters: "2 - 12", title: "Kitab Tanda-Tanda (Book of Signs)", summary: "Yesus menyatakan kemuliaan-Nya melalui tujuh tanda ajaib (dari mengubah air menjadi anggur di Kana hingga membangkitkan Lazarus) dan khotbah-khotbah wahyu rohani." },
      { chapters: "13 - 17", title: "Kitab Kemuliaan: Perjamuan Malam Terakhir", summary: "Yesus membasuh kaki para murid, memberikan Amanat Perpisahan yang intim, mengajarkan hukum kasih, menjanjikan Roh Kudus, dan mengucapkan Doa Imam Agung." },
      { chapters: "18 - 21", title: "Kisah Sengsara, Kebangkitan, dan Tugas Gembala", summary: "Penangkapan, pengadilan di hadapan Pilatus, wafat di salib (wafat saat domba Paskah disembelih), kebangkitan-Nya, penampakan kepada Tomas, serta pengutusan Petrus sebagai gembala utama." }
    ],
    goldenVerses: [
      { verse: "Yohanes 1:14", text: "Firman itu telah menjadi manusia, dan diam di antara kita...", reflection: "Pusat misteri Inkarnasi Katolik: Allah yang tak terbatas memilih merangkul kedagingan manusia yang rapuh agar kita dapat mengambil bagian dalam kodrat ilahi." },
      { verse: "Yohanes 3:16", text: "Karena begitu besar kasih Allah akan dunia ini, sehingga Ia telah mengaruniakan Anak-Nya yang tunggal...", reflection: "Rangkuman indah dari seluruh kabar gembira Alkitab tentang motif utama penyelamatan manusia: Kasih tak bersyarat Allah Bapa." },
      { verse: "Yohanes 6:54", text: "Barangsiapa makan daging-Ku dan minum darah-Ku, ia mempunyai hidup yang kekal...", reflection: "Dasar teologis yang tak tergoyahkan dari iman Gereja Katolik akan kehadiran riil Yesus Kristus dalam Sakramen Mahakudus Ekaristi." }
    ]
  },
  "1mak": {
    quote: "Kemenangan dalam pertempuran tidak tergantung pada besarnya pasukan, melainkan kekuatan dari Surga.",
    tagline: "Perjuangan Kaum Makabe Membela Iman, Hukum, dan Bait Suci",
    overview: "Kitab 1 Makabe adalah kitab sejarah Deuterokanonika yang luar biasa. Kitab ini mencatat perjuangan heroik bangsa Yahudi di bawah kepemimpinan keluarga Yudas Makabe melawan upaya asimilasi budaya pagan helenistik dari dinasti Seleukus Suriah.",
    author: "Sejarawan Yahudi yang taat di Yerusalem (anonim).",
    date: "Sekitar tahun 100 SM",
    context: "Ditulis setelah keberhasilan pembersihan kembali Bait Allah untuk membangkitkan rasa patriotisme iman dan kesetiaan mutlak pada Taurat Musa di masa damai dinasti Hasmonean.",
    theology: "1. **Kesetiaan sampai Mati (Martir):** Pembelaan iman terhadap penindasan agama pagan. Menjadi dasar dari konsep kemartiran Kristen awal.\n2. **Kedaulatan Bait Allah:** Bait Allah adalah pusat hadirat kudus Allah yang harus dijaga dari penajisan (asal mula hari raya penahbisan Bait Allah / Hanukkah).\n3. **Penyelenggaraan Ilahi dalam Sejarah:** Allah bekerja melalui pahlawan yang taat pada hukum-Nya, memberikan kemenangan bagi pasukan kecil yang bersandar pada kekuatan Surga.\n4. **Hubungan dengan 2 Makabe:** 1 & 2 Makabe meletakkan landasan kuat ajaran Katolik tentang persekutuan para kudus dan pentingnya mendoakan jiwa-jiwa orang beriman yang sudah meninggal (Bdk. 2 Mak 12:43-45).",
    structure: [
      { chapters: "1 - 2", title: "Krisis Penajisan dan Pemberontakan Mattathias", summary: "Antiochus Epiphanes menajiskan Bait Allah dengan mendirikan patung Zeus. Imam Mattathias menolak mempersembahkan kurban berhala, membunuh petugas raja, dan menyerukan perang gerilya." },
      { chapters: "3 - 9", title: "Kepemimpinan Yudas Makabe", summary: "Yudas mengambil alih komando, memenangkan pertempuran-pertempuran mukjizat melawan jenderal Suriah, menobatkan kembali Bait Allah (Hanukkah), dan gugur sebagai pahlawan." },
      { chapters: "10 - 12", title: "Kepemimpinan Jonathan Makabe", summary: "Jonathan melanjutkan perang lewat diplomasi cerdas, diangkat menjadi Imam Agung, memperluas wilayah Yehuda, namun akhirnya dikhianati dan dibunuh oleh Trypho." },
      { chapters: "13 - 16", title: "Kepemimpinan Simon Makabe", summary: "Simon berhasil mengusir pasukan Suriah sepenuhnya dari benteng Yerusalem, menegakkan masa kedamaian dan kemakmuran, serta mendirikan dinasti Hasmonean yang merdeka." }
    ],
    goldenVerses: [
      { verse: "1 Makabe 2:64", text: "Maka hendaklah kamu, hai anak-anakku, bersikap berani dan kuat-kuat mempertahankan hukum Taurat...", reflection: "Seruan iman dari Mattathias agar anak-anaknya menaruh hukum Tuhan di atas segalanya, bahkan nyawa mereka sendiri." },
      { verse: "1 Makabe 3:19", text: "Sebab kemenangan dalam pertempuran tidak tergantung pada besarnya pasukan, melainkan pada kekuatan yang datang dari Surga.", reflection: "Sebuah pengingat abadi bahwa dalam pertempuran spiritual hidup kita, kemenangan sejati hanya datang dari rahmat Allah, bukan kekuatan manusiawi kita." },
      { verse: "1 Makabe 4:59", text: "Lalu Yudas beserta saudara-saudaranya dan seluruh jemaah Israel menetapkan bahwa hari-hari penahbisan mezbah itu dirayakan pada waktunya...", reflection: "Sejarah penetapan hari penahbisan Bait Allah (Hanukkah), membuktikan pentingnya perayaan liturgis syukur dalam tradisi iman." }
    ]
  },
  why: {
    quote: "Akulah Alfa dan Omega, Yang Pertama dan Yang Terkemudian, Yang Awal dan Yang Akhir.",
    tagline: "Liturgi Surgawi, Pernikahan Anak Domba, dan Kemenangan Akhir Gereja",
    overview: "Kitab Wahyu adalah kitab penutup Alkitab yang penuh dengan simbolisme apokaliptik mistik. Jauh dari sekadar buku ketakutan tentang akhir dunia, Wahyu menyajikan penglihatan pengharapan agung mengenai liturgi abadi di surga, kemenangan final Allah atas kuasa jahat, dan pernikahan agung Anak Domba dengan pengantin-Nya (Gereja).",
    author: "Santo Yohanes Penginjil (Rasul Yohanes di Pulau Patmos).",
    date: "Sekitar tahun 95 M",
    context: "Ditulis selama penganiayaan kejam kaisar Romawi Domitianus terhadap umat Kristen untuk meneguhkan ketahanan iman mereka di tengah ancaman kemartiran.",
    theology: "1. **Liturgi Surgawi & Misa Kudus:** Struktur Kitab Wahyu mencerminkan perayaan liturgis Ekaristi di bumi (Liturgi Sabda di pembukaan segel, Liturgi Ekaristi di pernikahan Anak Domba) (Bdk. KGK 1137-1139).\n2. **Maria sebagai Perempuan Bermahkota:** Sosok 'Perempuan bermahkotakan 12 bintang' (Wahyu 12) yang melahirkan Anak laki-laki ditafsirkan sebagai Santa Perawan Maria, Ratu Surga, sekaligus citra Gereja.\n3. **Kemenangan Kristus:** Kristus digambarkan sebagai Anak Domba yang disembelih namun menang tegak berdiri, menaklukkan Babel mistik (kekaisaran penindas).\n4. **Kemenangan Eskatologis:** Yerusalem Baru yang turun dari surga, tempat di mana tidak akan ada lagi air mata, maut, atau kesedihan.",
    structure: [
      { chapters: "1 - 3", title: "Visi Kristus Agung dan Surat ke Tujuh Jemaat", summary: "Penampakan Kristus dalam kemuliaan imamat kepada Yohanes di Patmos, serta instruksi surat pastoral khusus bagi pertobatan ketujuh jemaat di Asia Kecil." },
      { chapters: "4 - 11", title: "Liturgi Takhta Surga dan Tujuh Segel", summary: "Penglihatan takhta Allah dikelilingi 24 tua-tua dan 4 makhluk hidup, Anak Domba membuka gulungan kitab bermeterai tujuh, pelepasan hukuman, dan tiupan tujuh sangkakala." },
      { chapters: "12 - 20", title: "Perang Kosmik dan Kejatuhan Naga serta Babel", summary: "Pertempuran kosmik antara Naga dengan Perempuan bermahkotakan bintang, tanda binatang 666, cawan murka Allah, kejatuhan Babel (kekaisaran pelacur), dan kekalahan final iblis." },
      { chapters: "21 - 22", title: "Yerusalem Baru dan Langit & Bumi yang Baru", summary: "Penciptaan langit baru dan bumi baru, Yerusalem Baru yang turun dari surga sebagai pengantin Anak Domba, dan undangan air kehidupan kekal." }
    ],
    goldenVerses: [
      { verse: "Wahyu 12:1", text: "Maka tampaklah suatu tanda besar di langit: Seorang perempuan berselubungkan matahari, dengan bulan di bawah kakinya dan sebuah mahkota dari dua belas bintang di atas kepalanya.", reflection: "Simbolisme agung Maria sebagai Ratu Surga yang ditinggikan, sekaligus lambang Gereja yang melahirkan keturunan-keturunan iman di tengah perjuangan rohani dunia." },
      { verse: "Wahyu 19:9", text: "Lalu ia berkata kepadaku: 'Tuliskanlah: Berbahagialah mereka yang diundang ke perjamuan kawin Anak Domba.'", reflection: "Seruan liturgis luar biasa yang diucapkan imam di altar dalam setiap Misa Kudus sebelum menyambut komuni, menghubungkan perjamuan altar bumi dengan liturgi abadi surga." },
      { verse: "Wahyu 22:20", text: "Ia yang memberi kesaksian tentang semuanya ini, berfirman: 'Ya, Aku datang segera!' Amin, datanglah, Tuhan Yesus!", reflection: "Teks maranatha legendaris, doa penutup seluruh Alkitab, menyatakan kerinduan hati Gereja yang tak berkeputusan akan kedatangan kembali Kristus sang pengantin." }
    ]
  }
};

// Basis Data Kategori Kaya Teologis & Sejarah Katolik
const categoryRichData = {
  Pentateukh: {
    overview: "Kelompok Kitab Pentateukh (atau Taurat) mencakup lima kitab pertama Alkitab yang meletakkan dasar absolut bagi seluruh sejarah keselamatan. Kitab-kitab ini menyingkapkan misteri awal mula penciptaan dunia dari ketiadaan, asal-usul martabat tinggi manusia, kejatuhan tragis akibat dosa asal, hingga pembentukan ikatan Perjanjian (Kovenan) kudus Allah dengan para leluhur Israel, mukjizat pembebasan dari perbudakan Mesir, dan pemberian Sepuluh Firman Allah (Dekalog) di Gunung Sinai.",
    context: "Ditulis secara tradisional oleh Musa dan dikompilasi secara dinamis sepanjang sejarah kuno Israel dari empat tradisi lisan utama: Yahwis (J), Elohis (E), Deuteronomis (D), dan Imamat (P). Redaksi akhir disusun pasca-pembuangan Babel untuk memulihkan identitas rohani umat Allah, menegaskan monoteisme mutlak di tengah gempuran budaya politeisme pagan.",
    theology: "1. **Inisiatif Kasih Allah:** Allah mengikat Perjanjian (Kovenan) kekal yang tak bersyarat demi keselamatan ciptaan-Nya.\n2. **Hukum Dekalog (Sepuluh Firman):** Diberikan bukan sebagai belenggu aturan mati, melainkan hukum kemerdekaan rohani untuk mendidik hati umat dalam kasih (KGK 2056-2059).\n3. **Pratanda Kristus (Tipologi):** Seluruh peristiwa utama Pentateukh meramalkan misteri keselamatan Kristus: kurban Ishak meramalkan salib; darah domba Paskah meramalkan Paskah Baru Yesus; Manna di gurun meramalkan Ekaristi Kudus."
  },
  Sejarah: {
    overview: "Kelompok Kitab Sejarah mencatat peziarahan konkret, jatuh bangun rohani, dan sejarah fisik bangsa Israel di bawah tuntunan Allah setelah memasuki Tanah Terjanji. Mengisahkan perjuangan para Hakim, kejayaan monarki Raja Daud dan Salomo, kemunduran moral para raja, pembuangan bangsa ke Babel akibat ketidaksetiaan iman, hingga masa pemulihan bait Allah pasca-pembuangan.",
    context: "Ditulis oleh para nabi, imam, dan sejarawan kudus Israel (seperti Ezra dan Nehemia) dalam kurun waktu abad ke-10 s.d. ke-2 SM berdasarkan arsip kerajaan kuno, bertujuan untuk mengevaluasi secara kritis perjalanan politik bangsa dari kacamata kepatuhan spiritual pada Perjanjian Allah.",
    theology: "1. **Kesetiaan Mutlak Allah:** Menunjukkan bahwa Allah selalu setia pada janji-Nya kepada keturunan Daud, meskipun umat-Nya berkali-kali berkhianat.\n2. **Hubungan Dosa dan Penderitaan:** Menjelaskan secara teologis bahwa kehancuran bangsa merupakan akibat langsung dari penyembahan berhala dan ketidakadilan sosial.\n3. **Nubuat Dinasti Daud:** Kerajaan Daud meramalkan takhta Kerajaan Mesias rohani yang kekal dalam diri Yesus Kristus, sang Raja Damai sejati."
  },
  Puisi: {
    overview: "Kelompok Kitab Puisi dan Kebijaksanaan menyajikan untaian mutiara spiritual, nyanyian ziarah liturgis, serta pergulatan eksistensial hati orang beriman di hadapan Allah. Kitab-kitab ini menuntun manusia menghadapi penderitaan hidup (Ayub), menata kebijaksanaan praktis sehari-hari (Amsal), merenungkan kefanaan duniawi (Pengkhotbah), dan merayakan keindahan cinta perkawinan suci (Kidung Agung).",
    context: "Ditulis dan dikumpulkan oleh para bijak, raja, dan penyair iman Israel sepanjang zaman monarki emas hingga masa pasca-pembuangan (abad ke-10 s.d. ke-3 SM), dipengaruhi tradisi kebijaksanaan kuno Timur Tengah namun dijiwai oleh wahyu monoteistik Yahudi.",
    theology: "1. **Takut akan TUHAN:** Sikap sujud menyembah, takjub, dan hormat pada keagungan Allah diakui sebagai awal dari segala kebijaksanaan sejati (Bdk. KGK 214-216).\n2. **Yesus sebagai Hikmat Allah:** Kebijaksanaan ilahi yang dipersonifikasikan dalam kitab-kitab ini mewujud secara sempurna dalam Inkarnasi Yesus Kristus (1 Kor 1:24).\n3. **Kudusnya Cinta Perkawinan:** Cinta eksklusif dalam Kidung Agung dipahami dalam teologi Katolik sebagai lambang persatuan mistik antara Kristus dengan mempelai-Nya (Gereja)."
  },
  "Nabi Besar": {
    overview: "Kitab para Nabi Besar menyajikan seruan profetis, desakan tobat sosial-spiritual, serta penglihatan teologis luar biasa mengenai rencana pemulihan akhir Allah. Kitab-kitab ini menentang keras penyembahan berhala dan penindasan kaum lemah, memperingatkan ancaman kehancuran Yerusalem, sekaligus menyalakan api pengharapan mesianik yang cemerlang di tengah kegelapan pembuangan.",
    context: "Ditulis oleh para nabi agung Yehuda dan para murid sekolah kenabian mereka (seperti Yesaya, Yeremia, Yehezkiel, dan Daniel) pada abad ke-8 s.d. ke-6 SM di tengah badai invasi Asyur dan kehancuran kota suci Yerusalem oleh Babel.",
    theology: "1. **Seruan Tobat Batin:** Menolak formalisme ritual tanpa pertobatan hati sejati dan keadilan sosial yang riil.\n2. **Nubuat Perjanjian Baru:** Menjanjikan hukum Allah yang akan ditulis langsung di dalam loh hati manusia, bukan lagi loh batu (Yer 31:33).\n3. **Nubuat Puncak Mesias:** Meramalkan kedatangan Hamba yang Menderita, kelahiran Mesias dari seorang perawan, serta liturgi takhta kemuliaan Anak Manusia (Bdk. KGK 711-716)."
  },
  "Nabi Kecil": {
    overview: "Meskipun disebut 'Kecil' karena ukuran tulisan yang lebih ringkas, kitab-kitab ini memuat pesan kenabian yang sangat tajam, padat, dan dramatis. Dari kemurkaan kasih Allah terhadap perselingkuhan rohani (Hosea), seruan tobat air mata (Yoel), tuntutan keadilan sosial (Amos), mukjizat keselamatan bangsa kafir (Yunus), hingga nubuat kedatangan Mesias yang menunggang keledai (Zakharia).",
    context: "Disusun oleh dua belas nabi kudus Israel secara individual dari kurun waktu abad ke-8 s.d. ke-4 SM, melayani kerajaan Utara (Israel) dan Selatan (Yehuda) dalam berbagai masa pergolakan politik dan pembangunan kembali bait Allah.",
    theology: "1. **Allah yang Cemburu karena Kasih:** Melukiskan ikatan kovenan laksana ikatan pernikahan suci; berhala adalah perzinahan rohani yang melukai hati Allah.\n2. **Hari TUHAN (*Yom Yahweh*):** Hari penghakiman sekaligus hari pemulihan rahmat universal bagi seluruh ciptaan.\n3. **Mesias yang Rendah Hati:** Nubuat detail tentang Mesias sebagai gembala yang terbuang dan raja yang menunggang keledai beban, tergenapi utuh pada Minggu Palma Yesus."
  },
  "Sejarah (DK)": {
    overview: "Kelompok Kitab Sejarah Deuterokanonika (seperti Tobit, Yudit, dan 1 & 2 Makabe) menyajikan catatan sejarah perjuangan iman yang luar biasa heroik bagi bangsa Yahudi. Mengisahkan pemeliharaan keluarga Tobias oleh Malaikat Agung Rafael, keteguhan janda kudus Yudit menyelamatkan bangsanya, dan perjuangan kemerdekaan fisik kaum Makabe mempertahankan kemurnian iman dari helenisasi kejam.",
    context: "Ditulis dalam bahasa Yunani dan Ibrani pada abad ke-3 s.d. ke-1 SM di tengah tekanan peradaban pagan Yunani Seleukus. Diakui resmi sebagai Kitab Suci terilhami oleh Gereja Katolik melalui Konsili Hippo (393 M) dan ditegaskan secara dogmatis oleh Konsili Trente (1546 M).",
    theology: "1. **Keteguhan Kemartiran:** Memberikan teladan kemartiran heroik demi mempertahankan hukum Allah yang menjadi dasar kekuatan saksi iman Gereja perdana.\n2. **Keterlibatan Para Malaikat:** Ajaran teologis Katolik mengenai eksistensi dan peran pelindung Malaikat Agung (Santo Rafael) dalam peziarahan hidup manusia (Bdk. KGK 336).\n3. **Doa Penyucian Arwah:** Dasar teologis tak tergoyahkan bagi ajaran Katolik tentang persekutuan para kudus, purgatorium (api penyucian), dan pentingnya Misa kudus/doa bagi keselamatan jiwa orang meninggal (2 Mak 12:43-45)."
  },
  "Hikmat (DK)": {
    overview: "Kelompok Kitab Hikmat Deuterokanonika (seperti Kebijaksanaan Salomo dan Yesus bin Sirakh) menyajikan puncak pemikiran teologis kebijaksanaan Yahudi-Kristen. Kitab-kitab ini menyingkapkan hubungan harmonis antara iman dan akal budi, memaparkan hakikat murni Kebijaksanaan ilahi yang aktif memandu alam semesta, memberikan pedoman moral hidup bermartabat tinggi, dan menegaskan iman akan keabadian jiwa.",
    context: "Ditulis oleh para bijak Yahudi terpelajar di Aleksandria dan Yerusalem pada abad ke-2 s.d. ke-1 SM untuk melindungi kaum muda Yahudi dari pengaruh skeptisisme filsafat pagan helenisme.",
    theology: "1. **Akal Budi dan Iman:** Menegaskan bahwa ciptaan yang indah menuntun akal sehat manusia untuk mengenal Allah Sang Pencipta agung (Keb 13:1-9; Bdk. KGK 32).\n2. **Keabadian Jiwa:** Menyatakan dengan sangat eksplisit bahwa kematian jasmani orang benar bukanlah kemusnahan, melainkan jalan damai sejahtera dalam pelukan tangan Allah (Keb 3:1-3).\n3. **Kebijaksanaan sebagai Personifikasi Roh Kudus:** Menggambarkan Kebijaksanaan sebagai hembusan kuasa Allah yang kudus, meramalkan ajaran Tritunggal Mahakudus."
  },
  "Nabiah (DK)": {
    overview: "Kelompok Kitab Kenabian Deuterokanonika (seperti Kitab Barukh dan Tambahan Kitab Daniel) melengkapi nubuat-nubuat Perjanjian Lama dengan seruan doa tobat yang sangat khusyuk, ratapan puitis atas dosa-dosa bangsa, dan madah keagungan perlindungan Allah bagi para pemuda di perapian menyala. Kitab-kitab ini menyalakan harapan pemulihan rohani bait Allah.",
    context: "Disusun oleh juru tulis Nabi Yeremia (Barukh) dan penulis kudus Yahudi pada abad ke-6 s.d. ke-2 SM dalam masa pembuangan Babel dan masa penindasan dinasti Seleukus.",
    theology: "1. **Pengakuan Dosa Komunal:** Doa tobat yang mendalam, mengakui bahwa hukuman pembuangan adalah akibat ketidaksetiaan rohani bangsa pada Taurat.\n2. **Tuhan sebagai Satu-satunya Penyelamat:** Kontras teologis yang kuat antara berhala palsu buatan tangan manusia yang bisu dengan Allah Israel yang hidup dan menyelamatkan.\n3. **Madah Pujian Ciptaan:** Lagu pujian tiga pemuda di perapian (Tambahan Daniel) mengundang seluruh alam semesta (air, angin, matahari, bulan, jiwa-jiwa orang benar) untuk memuji TUHAN selamanya, dinyanyikan resmi dalam Liturgi Brevir Katolik."
  },
  Injil: {
    overview: "Kelompok Kitab Injil (Matius, Markus, Lukas, Yohanes) adalah mahkota dan pusat sakral dari seluruh Kitab Suci. Injil mewartakan Kabar Gembira keselamatan paling agung: Inkarnasi Allah menjadi manusia dalam diri Yesus Kristus, sabda wahyu-Nya tentang Kerajaan Allah, mukjizat belas kasih-Nya, serta misteri Paskah Sengsara, Wafat, Kebangkitan, dan Kenaikan-Nya ke surga.",
    context: "Ditulis oleh para Rasul dan saksi mata apostolik (Santo Matius, Santo Markus, Santo Lukas, Santo Yohanes) pada abad ke-1 M (tahun 60 s.d. 100 M) di bawah ilham Roh Kudus untuk diwartakan ke seluruh penjuru dunia demi pertobatan iman manusia.",
    theology: "1. **Puncak Wahyu Ilahi:** Yesus Kristus adalah kepenuhan hukum Taurat dan para nabi. Seluruh sabda dan tindakan-Nya adalah Sabda Allah yang hidup bagi kita (Bdk. KGK 124-127).\n2. **Kerajaan Allah dan Pertobatan:** Panggilan untuk menerima keselamatan Allah melalui baptisan, iman, dan tobat batin.\n3. **Misteri Paskah dan Ekaristi:** Sengsara, wafat, dan kebangkitan Yesus sebagai kurban penebusan dosa universal yang dihadirkan kembali secara nyata dalam perayaan Misa Kudus."
  },
  "Surat Paulus": {
    overview: "Kelompok Surat Paulus memuat pengajaran teologis, dogmatis, dan pastoral mendalam dari Rasul Paulus kepada jemaat-jemaat perdana. Surat-surat ini menjelaskan secara mendetail penerapan misteri salib Kristus dalam teologi pembenaran oleh rahmat, pedoman moral komunitas, kehidupan sakramen, struktur kepemimpinan Gereja, dan persekutuan mistik umat.",
    context: "Ditulis oleh Santo Paulus (Rasul bangsa kafir) kepada berbagai jemaat (Roma, Korintus, Galatia, Efesus, dsb.) dan rekan gembala (Timotius, Titus, Filemon) pada kurun waktu tahun 50 s.d. 67 M saat menggalang misi pekabaran Injil dan di dalam penjara Roma.",
    theology: "1. **Pembenaran oleh Rahmat melalui Iman:** Manusia dibenarkan bukan karena melakukan hukum Taurat lahiriah, melainkan murni karunia rahmat Allah melalui iman yang bekerja aktif dalam kasih (Bdk. KGK 1987-1995).\n2. **Gereja sebagai Tubuh Mistik Kristus:** Teologi persatuan kudus di mana Kristus adalah Kepala dan umat beriman adalah anggota-anggota Tubuh-Nya yang saling mengasihi.\n3. **Teologi Salib & Kebangkitan:** Menegaskan salib sebagai kekuatan hikmat Allah dan kebangkitan Kristus sebagai jaminan kebangkitan fisik kita di akhir zaman."
  },
  "Surat Umum": {
    overview: "Kelompok Surat Umum (Katolik) mencakup surat-surat pastoral rasuli yang ditujukan kepada seluruh jemaat universal (Katolik) di mana saja. Ditulis oleh para rasul utama (Santo Yakobus, Santo Petrus, Santo Yohanes, dan Santo Yudas), surat-surat ini berfokus pada ketahanan iman di tengah penganiayaan, hubungan mutlak antara iman dan perbuatan nyata, serta hukum kasih persaudaraan.",
    context: "Disusun oleh para Rasul tiang agung jemaat Yerusalem pada abad ke-1 M (tahun 60 s.d. 95 M) bagi jemaat diaspora Kristen perdana yang tersebar di kekaisaran Romawi yang mengalami penderitaan diskriminasi sosial.",
    theology: "1. **Iman yang Hidup oleh Perbuatan:** Menegaskan secara dogmatis bahwa iman tanpa perbuatan nyata kasih adalah iman yang mati (Bdk. Yak 2:26; KGK 1815).\n2. **Panggilan Kekudusan Imamat Rajani:** Umat beriman dipanggil menjadi bangsa yang terpilih, imamat rajani, bangsa yang kudus, umat kepunyaan Allah sendiri (1 Pet 2:9).\n3. **Hakikat Allah adalah Kasih:** Santa Perawan Maria dan para kudus meneladani ajaran Santo Yohanes bahwa barangsiapa tidak mengasihi, ia tidak mengenal Allah, sebab Allah adalah Kasih (1 Yoh 4:8)."
  },
  Apokaliptik: {
    overview: "Kitab Apokaliptik (Wahyu) adalah kitab penutup Alkitab yang agung, dipenuhi dengan simbolisme mistik penglihatan surgawi. Jauh dari sekadar buku ketakutan akhir zaman, Wahyu mewartakan kabar pengharapan kosmik paling radikal: kemenangan mutlak Allah dan Anak Domba atas naga (iblis) dan Babel (kekuatan dunia yang menindas), serta perkawinan abadi Anak Domba dengan Gereja di Yerusalem Baru.",
    context: "Ditulis oleh Santo Yohanes Penginjil di Pulau Patmos sekitar tahun 95 M selama penganiayaan kejam kaisar Romawi Domitianus terhadap umat Kristen perdana, berfungsi sebagai hiburan rohani bagi para martir.",
    theology: "1. **Liturgi Surgawi dan Ekaristi:** Menyatakan bahwa Misa Kudus di bumi adalah gerbang partisipasi nyata ke dalam liturgi pesta abadi para kudus di surga (Bdk. KGK 1137-1139).\n2. **Maria Ratu Surga (Wahyu 12):** Perempuan berselubungkan matahari bermahkota 12 bintang dipahami sebagai Maria Bunda Kristus sekaligus citra pelindung Gereja.\n3. **Kemenangan Puncak Anak Domba:** Kematian silih Yesus (Anak Domba yang disembelih namun berdiri menang) adalah penakluk maut dan kejahatan yang abadi."
  }
};

// Fungsi Generator untuk Kitab Fallback (Super Kaya & Bebas Satu Kalimat)
function generateFallbackSummary(book) {
  const categoryData = categoryRichData[book.subCategory] || categoryRichData[book.category] || {
    overview: `Kitab ${book.name} menyajikan kebijaksanaan rohani dan pengajaran iman yang sangat berharga bagi pemahaman utuh Kitab Suci sesuai tradisi Gereja Katolik.`,
    context: `Ditulis oleh para penulis kudus Alkitab di bawah bimbingan Roh Kudus untuk meneguhkan iman umat beriman dalam masa peziarahan sejarah mereka.`,
    theology: `1. **Penyelenggaraan Ilahi:** Allah senantiasa membimbing umat-Nya melalui sejarah konkret.\n2. **Belas Kasih:** Menunjukkan belas kasih kasih Allah yang mendidik umat-Nya menuju keselamatan.`
  };

  const tagline = `Panduan Mendalam Kitab ${book.name} - Tradisi Pustaka Suci`;
  
  // Custom timeline structure per book berdasarkan chapter riil agar terstruktur jelas!
  const midPoint = Math.ceil(book.chapters / 2);
  const structure = [
    { 
      chapters: `1 - ${midPoint}`, 
      title: `Pembukaan & Peletakan Dasar Iman Kitab ${book.name}`, 
      summary: `Membuka narasi teologis Kitab ${book.name}, memaparkan situasi awal umat Allah, pemicu pergulatan spiritual, serta kesetiaan kovenan-Nya di paruh awal bagian ini.` 
    },
    { 
      chapters: `${midPoint + 1} - ${book.chapters}`, 
      title: `Klimaks Wahyu & Resolusi Rencana Keselamatan`, 
      summary: `Menuntun pembaca menuju puncak resolusi rencana keselamatan Allah, pengajaran moral praktis/dogmatis yang mendalam, serta kesimpulan janji setia Allah bagi iman kita.` 
    }
  ];

  // Ayat emas spesifik yang indah sesuai kitab
  let goldenVerseText = `Teks sabda mulia dari Kitab ${book.name} yang sarat akan kekayaan Tradisi Suci Gereja.`;
  let goldenVerseRef = `${book.name} 1:1`;
  let reflection = "Mengajak kita merenungkan bahwa setiap sabda yang tertulis dalam kitab ini ditulis dengan maksud ilahi untuk menerangi kaki kita menapaki peziarahan iman.";

  // Kustomisasi ayat emas populer Katolik per kitab fallback penting
  if (book.id === "kel") {
    goldenVerseText = "Akulah TUHAN, Allahmu, yang membawa engkau keluar dari tanah Mesir, dari tempat perbudakan. Jangan ada padamu allah lain di hadapan-Ku.";
    goldenVerseRef = "Keluaran 20:2-3";
    reflection = "Pemberian hukum utama sebagai tanda kemerdekaan sejati, menuntut cinta kasih eksklusif kepada Allah pemberi hidup.";
  } else if (book.id === "ams") {
    goldenVerseText = "Takut akan TUHAN adalah permulaan pengetahuan, tetapi orang bodoh menghina hikmat dan didikan.";
    goldenVerseRef = "Amsal 1:7";
    reflection = "Sikap hormat, takjub, dan sujud menyembah Allah adalah fondasi absolut dari seluruh kebijaksanaan dan intelektualitas manusia.";
  } else if (book.id === "pkh") {
    goldenVerseText = "Kesia-siaan belaka, kata Pengkhotbah, kesia-siaan belaka, segala sesuatu adalah kesia-siaan.";
    goldenVerseRef = "Pengkhotbah 1:2";
    reflection = "Sebuah meditasi mendalam Katolik tentang kefanaan duniawi, mengajak kita menaruh jangkar hidup hanya pada Allah yang kekal.";
  } else if (book.id === "sir") {
    goldenVerseText = "Segala kebijaksanaan berasal dari Tuhan, dan ada pada-Nya untuk selama-lamanya.";
    goldenVerseRef = "Yesus bin Sirakh 1:1";
    reflection = "Menegaskan keabsahan ajaran Deuterokanonika bahwa sumber segala intelektualitas moral yang murni bersumber dari Allah sendiri.";
  } else if (book.id === "mat") {
    goldenVerseText = "Karena itu pergilah, jadikanlah semua bangsa murid-Ku dan baptislah mereka dalam nama Bapa dan Anak dan Roh Kudus...";
    goldenVerseRef = "Matius 28:19";
    reflection = "Amanat Agung misioner Gereja Katolik, mengutus kita mewartakan kebenaran Trinitas dan membagikan rahmat sakramen baptis.";
  } else if (book.id === "kis") {
    goldenVerseText = "Tetapi kamu akan menerima kuasa, kalau Roh Kudus turun ke atas kamu, dan kamu akan menjadi saksi-Ku...";
    goldenVerseRef = "Kisah Para Rasul 1:8";
    reflection = "Kunci gerakan misioner Gereja, di mana sakramen Penguatan melengkapi kita dengan kuasa Roh Kudus untuk berani bersaksi tentang Kristus.";
  } else if (book.id === "rm") {
    goldenVerseText = "Sebab upah dosa ialah maut; tetapi karunia Allah ialah hidup yang kekal dalam Kristus Yesus, Tuhan kita.";
    goldenVerseRef = "Roma 6:23";
    reflection = "Kontras teologis agung mengenai maut akibat dosa vs rahmat pembenaran cuma-cuma yang ditawarkan Allah melalui Yesus Kristus.";
  } else if (book.id === "1kor") {
    goldenVerseText = "Demikianlah tinggal ketiga hal ini, yaitu iman, pengharapan dan kasih, dan yang paling besar di antaranya ialah kasih.";
    goldenVerseRef = "1 Korintus 13:13";
    reflection = "Mutiara teologis kebajikan ilahi Katolik. Di surga iman dan harapan akan terpenuhi, namun hukum kasih akan tetap tinggal abadi.";
  } else if (book.id === "yak") {
    goldenVerseText = "Sebab sama seperti tubuh tanpa roh adalah mati, demikian jugalah iman tanpa perbuatan-perbuatan adalah mati.";
    goldenVerseRef = "Yakobus 2:26";
    reflection = "Dasar teologis penting Gereja Katolik yang menegaskan kebersatuan mutlak antara iman batiniah dengan buah perbuatan kasih nyata.";
  }

  const goldenVerses = [
    {
      verse: goldenVerseRef,
      text: goldenVerseText,
      reflection
    }
  ];

  return {
    quote: book.name === "Imamat" ? "Kuduslah kamu, sebab Aku, TUHAN, Allahmu, kudus." :
           book.name === "Ulangan" ? "Kasihilah TUHAN, Allahmu, dengan segenap hatimu dan dengan segenap jiwamu..." :
           book.name === "Yosua" ? "Kuatkan dan teguhkanlah hatimu, jangan kecut dan tawar hati..." :
           book.name === "Rut" ? "Sebab ke mana engkau pergi, ke situ jugalah aku pergi..." :
           book.name === "Kisah Para Rasul" ? "Tetapi kamu akan menerima kuasa, kalau Roh Kudus turun ke atas kamu..." :
           book.name === "Roma" ? "Sebab upah dosa ialah maut; tetapi karunia Allah ialah hidup yang kekal..." :
           book.name === "1 Korintus" ? "Demikianlah tinggal ketiga hal ini... dan yang paling besar ialah kasih." :
           book.name === "Yakobus" ? "Iman tanpa perbuatan-perbuatan adalah mati." :
           book.name === "Wahyu" ? "Akulah Alfa dan Omega, Yang Pertama dan Yang Terkemudian..." :
           `Teks pengantar iman Katolik Kitab ${book.name}.`,
    tagline,
    overview: categoryData.overview,
    author: book.category === "Perjanjian Baru" && book.subCategory.includes("Paulus") ? "Santo Paulus Rasul" : 
            book.subCategory === "Injil" ? `Santo ${book.name} Penginjil` :
            "Para Penulis Kudus Alkitab / Tradisi Yahudi-Kristen",
    date: book.category === "Perjanjian Lama" ? "Abad ke-10 s.d. ke-2 SM" : "Abad ke-1 M",
    context: categoryData.context,
    theology: categoryData.theology,
    structure,
    goldenVerses
  };
}

const finalSummaries = {};

books.forEach(book => {
  if (manualSummaries[book.id]) {
    finalSummaries[book.id] = {
      id: book.id,
      name: book.name,
      category: book.category,
      subCategory: book.subCategory,
      chapters: book.chapters,
      ...manualSummaries[book.id]
    };
  } else {
    finalSummaries[book.id] = {
      id: book.id,
      name: book.name,
      category: book.category,
      subCategory: book.subCategory,
      chapters: book.chapters,
      ...generateFallbackSummary(book)
    };
  }
});

fs.writeFileSync(outputPath, JSON.stringify(finalSummaries, null, 2), 'utf8');
console.log(`Successfully generated ${Object.keys(finalSummaries).length} highly detailed Catholic summaries in ${outputPath}!`);
