# 🐍 Python SEO Tools - Automated Comment Bot
Automated comment bot untuk website menggunakan Python, Selenium, dan undetected ChromeDriver. Tools ini dirancang untuk melakukan komentar otomatis dengan akun Google pada website tertentu untuk keperluan SEO dan digital marketing.

<img src="/python-seo-tools.png" width="600" alt="SeO Backlink Komentar">

Rekomendasi menggunakan tools ini dengan tools pelengkapnya
- [URL-Cleaner-Comparator](https://github.com/Dzbackdor/URL-Cleaner-Comparator)
- [moz-pro-without-api-key](https://github.com/Dzbackdor/moz-pro-without-api-key)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-green.svg)](https://selenium-python.readthedocs.io/)


## 🎯 Kegunaan Tools

### 🔗 SEO & Link Building
- **Backlink Generation** - Membuat backlink berkualitas melalui komentar dengan link
- **Domain Authority Boost** - Meningkatkan otoritas domain melalui link dari website lain
- **Anchor Text Optimization** - Mengoptimalkan anchor text untuk keyword tertentu
- **Link Diversity** - Menciptakan variasi sumber backlink yang natural

### 📈 Digital Marketing
- **Brand Awareness** - Meningkatkan awareness brand melalui komentar yang relevan
- **Traffic Generation** - Mengarahkan traffic ke website melalui link dalam komentar
- **Lead Generation** - Menghasilkan potential leads dari audience website target
- **Content Promotion** - Mempromosikan konten blog/artikel terbaru

### 💼 Business Development
- **Market Research** - Menganalisis kompetitor dan target audience
- **Community Engagement** - Berpartisipasi dalam komunitas online yang relevan
- **Relationship Building** - Membangun hubungan dengan website owner dan audience
- **Brand Positioning** - Memposisikan brand sebagai expert di bidang tertentu

### 🎨 Content Marketing
- **Content Distribution** - Mendistribusikan konten ke berbagai platform
- **Engagement Boost** - Meningkatkan engagement pada konten yang dipublikasikan
- **Social Proof** - Menciptakan social proof melalui komentar positif
- **User Generated Content** - Mendorong terciptanya diskusi dan UGC

### 🏢 Agency & Freelancer
- **Client Services** - Menyediakan layanan SEO dan digital marketing untuk klien
- **Scalable Operations** - Mengotomatisasi proses yang repetitif dan time-consuming
- **ROI Improvement** - Meningkatkan ROI campaign dengan automasi
- **Competitive Advantage** - Memberikan keunggulan kompetitif dalam layanan

### 📊 Research & Analytics
- **Competitor Analysis** - Menganalisis strategi komentar kompetitor
- **Market Intelligence** - Mengumpulkan data tentang tren dan preferensi audience
- **A/B Testing** - Testing berbagai template komentar untuk optimasi
- **Performance Tracking** - Melacak performa campaign melalui analytics

## 📋 Fitur

- ✅ **Mode Otomatis** - Proses semua URL secara otomatis
- ✅ **Mode Test** - Test dengan satu URL untuk development
- ✅ **Multi-Account Support** - Mendukung multiple akun Google
- ✅ **Account Limit Detection** - Deteksi otomatis akun yang terkena limit
- ✅ **Browser Anti-Throttling** - Menjaga browser tetap aktif
- ✅ **Auto Reconnect** - Reconnect otomatis jika koneksi terputus
- ✅ **Progress Tracking** - Melacak URL yang sudah selesai diproses
- ✅ **Custom Link Comments** - Komentar dengan link khusus
- ✅ **Browser Cleanup** - Pembersihan browser otomatis

## 🛠️ Requirements

### System Requirements
- Python 3.7+
- Google Chrome Browser
- Windows/Linux/macOS

### Python Dependencies
```
undetected-chromedriver>=3.5.0
selenium>=4.15.0
beautifulsoup4>=4.12.0
colorama>=0.4.6
```

## 📦 Installation

1. **Clone repository:**
```bash
git clone https://github.com/Dzbackdor/python-seo-tools.git
cd python-seo-tools
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Dalam beberapa kasus jika terjadi error saat menjalankan tools ini, pastikan anda telah menginstal requirements.txt yang dibutuhkan. Setelah itu coba jalankan perintah berikut:**
```bash
pip install distutils-pytest
```
```bash
pip install setuptools
```

3. **Setup files:**
Program akan otomatis membuat file yang diperlukan saat pertama kali dijalankan.

## ⚙️ Configuration

### 1. Setup URL Target (`list.txt`)
```
https://example.com/page1
https://example.com/page2
https://example.com/page3
```

### 2. Setup Akun Google (`akun.txt`)
```
email1@gmail.com
password1
email2@gmail.com
password2
```

### 3. Setup Template Komentar (`komen.txt`)
```
# Format biasa
Terima kasih atas informasinya yang sangat bermanfaat!

# Format dengan link khusus
Artikel yang bagus! [url]Kunjungi website kami[link:https://mywebsite.com] untuk info lebih lanjut.
```

### 4. Setup Popup (`daftar.py`)
```
# cari di def handle_google_login(driver, email, password, url):
line 304 dan 305
driver.set_window_size(500, 600)
driver.set_window_position(0, 0)
```

## 🚀 Usage

### Mode Otomatis
```bash
python main.py
# Pilih: 1. Mode Otomatis
```

### Mode Test
```bash
python main.py
# Pilih: 2. Mode Test
```

### Import sebagai Module
```python
from main import inisialisasi_driver, proses_satu_url
from daftar import lanjutkan_proses
from komentar import lanjutkan_komentar

# Inisialisasi driver
driver = inisialisasi_driver()

# Proses satu URL
success = proses_satu_url(driver, "https://example.com", 1, 1)
```

## 📝 Comment Format

### Format Link Khusus
```
[url]teks yang akan diberi link[link:https://website.com]
```

**Contoh:**
```
Terima kasih! [url]Kunjungi blog kami[link:https://myblog.com] untuk artikel menarik lainnya.
```

**Hasil:** Teks "Kunjungi blog kami" akan menjadi link ke https://myblog.com

## 📊 Features Detail

### 🔄 Auto Account Management
- Deteksi otomatis akun yang terkena limit
- Pemindahan akun limit ke `akunlimit.txt`
- Penggunaan akun berikutnya secara otomatis

### 🧹 Browser Cleanup
- Logout otomatis dari Google
- Pembersihan cookies dan storage
- Reset browser state untuk akun berikutnya

### 📈 Progress Tracking
- URL yang sudah selesai disimpan di `komen-done.txt`
- Resume otomatis dari URL yang belum selesai
- Statistik progress real-time

### 🔧 Error Handling
- Auto reconnect jika browser crash
- Fallback methods untuk setiap operasi
- Logging error ke `gagal-koment.txt`

## 🎯 Workflow

1. **Initialization** - Setup browser dan validasi file
2. **URL Processing** - Baca URL dari `list.txt`
3. **Account Login** - Login dengan akun dari `akun.txt`
4. **Comment Process** - Posting komentar sesuai template
5. **Cleanup** - Logout dan pembersihan browser
6. **Next URL** - Lanjut ke URL berikutnya

## 📋 Menu Options

```
🐍MODE OPERASI
1. Mode Otomatis - Proses semua URL secara otomatis
2. Mode Test - Test dengan satu URL (Dev)
3. Keluar
```

## 🔍 Monitoring

### Real-time Progress
- Loading bar untuk setiap operasi
- Status update untuk setiap langkah
- Statistik akun dan URL

### Log Files
- `komen-done.txt` - URL berhasil
- `gagal-koment.txt` - URL gagal dengan error message
- `akunlimit.txt` - Akun yang terkena limit

## ⚠️ Important Notes

### Browser Requirements
- Tools ini menggunakan undetected ChromeDriver
- Chrome browser harus terinstall
- Tidak perlu download ChromeDriver manual

### Account Safety
- Gunakan akun Google khusus untuk bot
- Jangan gunakan akun personal utama
- Monitor limit rate untuk menghindari suspend

### Rate Limiting
- Tools sudah include delay antar operasi
- Akun yang terkena limit otomatis dipindahkan
- Gunakan multiple akun untuk efisiensi

## 🐛 Troubleshooting

### Chrome Driver Issues
```bash
# Update Chrome browser ke versi terbaru
# Restart program jika ada error driver
```

### Connection Issues
```bash
# Tools include auto-reconnect
# Periksa koneksi internet
# Restart program jika masalah persisten
```

### Account Limit
```bash
# Akun otomatis dipindah ke akunlimit.txt
# Tambah akun baru ke akun.txt
# Monitor penggunaan akun
```

## 📈 Performance Tips

1. **Multiple Accounts** - Siapkan 5-10 akun Google
2. **Stable Internet** - Gunakan koneksi internet stabil
3. **Monitor Resources** - Tutup aplikasi lain saat running
4. **Regular Cleanup** - Hapus file log lama secara berkala

## ⚡ Changelog

### v1.1.1
- Initial release
- Basic comment automation
- Multi-account support
- Browser cleanup system

## 📞 Support

- Create an issue for bug reports
- Star ⭐ this repo if it helps you
- Follow for updates

## ⚠️ Disclaimer

Tools ini dibuat untuk tujuan edukasi dan automasi legitimate. Pengguna bertanggung jawab penuh atas penggunaan tools ini. Pastikan mematuhi Terms of Service website target dan tidak melakukan spam. Gunakan dengan bijak untuk keperluan SEO dan digital marketing yang etis.

---

**Made with ❤️ by Dzone**
