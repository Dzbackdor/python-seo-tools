import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import os
import logging
import sys
from colorama import Fore, init
import atexit

# Initialize Colorama
init(autoreset=True)

# Colors for terminal text
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW

def clear_terminal():
    """
    Membersihkan terminal untuk semua OS (Windows, Linux, macOS)
    """
    try:
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Linux/macOS
        else:
            os.system('clear')
    except Exception as e:
        print(f"{R}Gagal membersihkan terminal: {e}{W}")

banner = f"""

{R}╔═════════════════════════════════╗
{R}║{Y}   _           _   _ _     _     {R}║    
{R}║{Y}  | |_ ___ ___| |_| |_|___| |_   {R}║    
{R}║{Y}  | . | .'|  _| '_| | |   | '_|  {R}║ 
{R}║{Y}  |___|__,|___|_,_|_|_|_|_|_,_|  {R}║ 
{R}║     🐍 {W}PYTHON SEO TOOLS 🐍      {R}║                 
{R}╚═════════════════════════════════╝
"""

def pastikan_browser_tetap_aktif(driver):
    """
    Fungsi untuk memastikan browser tetap aktif meskipun tidak di foreground
    """
    try:
        anti_throttle_script = """
        // Simpan referensi ke fungsi requestAnimationFrame asli
        const originalRAF = window.requestAnimationFrame;
        
        // Buat fungsi untuk memastikan browser tetap aktif
        function keepBrowserActive() {
            // Panggil requestAnimationFrame untuk menjaga aktivitas browser
            originalRAF(keepBrowserActive);
            
            // Tambahkan sedikit aktivitas DOM untuk mencegah throttling
            if (!window._lastActiveTime || Date.now() - window._lastActiveTime > 500) {
                window._lastActiveTime = Date.now();
                
                // Buat elemen dummy dan hapus untuk memaksa aktivitas DOM
                const dummy = document.createElement('div');
                document.body.appendChild(dummy);
                document.body.removeChild(dummy);
                
                // Log aktivitas (opsional, untuk debugging)
                console.log('Menjaga browser tetap aktif: ' + new Date().toISOString());
            }
        }
        
        // Mulai loop untuk menjaga aktivitas
        keepBrowserActive();
        
        // Tambahkan listener untuk Page Visibility API
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                console.log('Halaman tidak terlihat, memastikan tetap aktif');
                // Tingkatkan frekuensi aktivitas saat halaman tidak terlihat
                window._lastActiveTime = 0;
            }
        });
        
        return "Script anti-throttling berhasil diterapkan";
        """
        
        result = driver.execute_script(anti_throttle_script)
        print(f"{G}Browser akan tetap aktif meskipun tidak di foreground{W}")
        return True
    except Exception as e:
        print(f"{R}Gagal menerapkan script anti-throttling: {e}{W}")
        return False

def jaga_fokus_browser(driver):
    """
    Fungsi untuk menjaga fokus browser secara periodik
    """
    try:
        driver.execute_script("""
        // Fokuskan window
        window.focus();
        
        // Klik pada body untuk memastikan fokus
        if (document.body) {
            document.body.click();
        }
        
        // Scroll sedikit untuk memicu aktivitas
        window.scrollBy(0, 1);
        window.scrollBy(0, -1);
        
        return "Browser difokuskan";
        """)
        
        return True
    except Exception as e:
        print(f"{R}Gagal menjaga fokus browser: {e}{W}")
        return False

def inisialisasi_driver():
    """
    Inisialisasi Chrome driver dengan konfigurasi optimal
    """
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Tambahkan flag untuk mencegah throttling
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    
    # Flag lain yang sudah ada
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--lang=en-US')
    
    try:
        print(f"{Y}Menginisialisasi Chrome driver...{W}")
        driver = uc.Chrome(options=options)
        
        # Dapatkan resolusi layar
        screen_width = driver.execute_script("return window.screen.width")
        screen_height = driver.execute_script("return window.screen.height")
        
        # Atur ukuran jendela browser
        window_width = int(screen_width * 0.8)
        window_height = screen_height
        
        # Atur posisi jendela
        position_x = 0
        position_y = 0
        
        # Atur ukuran dan posisi jendela
        driver.set_window_size(window_width, window_height)
        driver.set_window_position(position_x, position_y)
        
        print(f"{G}Chrome driver berhasil diinisialisasi.{W}")
        return driver
        
    except Exception as e:
        print(f"{R}Error inisialisasi Chrome driver: {e}{W}")
        print(f"{Y}Mencoba lagi dengan konfigurasi berbeda...{W}")
        
        # Coba dengan konfigurasi minimal
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            driver = uc.Chrome(options=options)
            print(f"{G}Chrome driver berhasil diinisialisasi dengan konfigurasi minimal.{W}")
            return driver
        except Exception as e2:
            print(f"{R}Gagal menginisialisasi Chrome driver: {e2}{W}")
            return None

def baca_url_dari_file(nama_file="list.txt"):
    """
    Membaca URL dari file list.txt
    """
    try:
        if not os.path.exists(nama_file):
            print(f"{R}File {nama_file} tidak ditemukan.{W}")
            print(f"{Y}Membuat file {nama_file} kosong...{W}")
            with open(nama_file, 'w') as file:
                file.write("")
            return []
            
        with open(nama_file, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except Exception as e:
        print(f"{R}Terjadi kesalahan saat membaca file: {e}{W}")
        return []

def tampilkan_loading_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Menampilkan loading bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{R}{bar}{W}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def tutup_popup_saat_scroll(driver):
    """
    Fungsi untuk menutup popup yang muncul saat scrolling
    """
    try:
        # Cari popup spesifik yang Anda sebutkan
        popup_selectors = [
            'button#close.ng-scope',
            'button[id="close"][class="ng-scope"]',
            'button#close[aria-label="Close"]',
            '#close.ng-scope'
        ]
        
        popup_ditutup = False
        
        for selector in popup_selectors:
            try:
                popup_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for popup in popup_elements:
                    if popup.is_displayed():
                        print(f"{Y}🚨 Popup ditemukan saat scroll: {selector}{W}")
                        
                        # Method 1: Klik langsung
                        try:
                            popup.click()
                            print(f"{G}✓ Popup ditutup dengan klik normal{W}")
                            popup_ditutup = True
                            time.sleep(0.5)
                            return True
                        except:
                            pass
                        
                        # Method 2: JavaScript click
                        try:
                            driver.execute_script("arguments[0].click();", popup)
                            print(f"{G}✓ Popup ditutup dengan JavaScript{W}")
                            popup_ditutup = True
                            time.sleep(0.5)
                            return True
                        except:
                            pass
                        
                        # Method 3: Sembunyikan
                        try:
                            driver.execute_script("""
                                var element = arguments[0];
                                element.style.display = 'none';
                                element.style.visibility = 'hidden';
                                element.style.opacity = '0';
                                
                                // Sembunyikan parent juga
                                var parent = element.parentNode;
                                if (parent) {
                                    parent.style.display = 'none';
                                }
                            """, popup)
                            print(f"{G}✓ Popup disembunyikan dengan force hide{W}")
                            popup_ditutup = True
                            time.sleep(0.5)
                            return True
                        except:
                            pass
            
            except:
                continue
        
        # Jika tidak ada popup spesifik, coba Escape
        if not popup_ditutup:
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.ESCAPE)
                actions.perform()
                time.sleep(0.2)
            except:
                pass
        
        return popup_ditutup
        
    except Exception as e:
        print(f"{R}Error saat tutup popup: {e}{W}")
        return False

def tangani_popup(driver, max_attempts=3):
    """
    Menangani pop-up awal
    """
    print(f"{Y}Menangani pop-up awal...{W}")
    
    # Pastikan browser tetap aktif
    pastikan_browser_tetap_aktif(driver)
    
    # Daftar selector umum untuk tombol tutup pop-up
    popup_selectors = [
        "button.close", ".close", "[class*='close']", 
        ".dismiss", "[class*='dismiss']",
        ".fa-times", ".icon-close", "[aria-label='Close']", "[title='Close']",
        "[id*='close']", "[id*='dismiss']",
        ".modal-backdrop", ".overlay", ".popup-overlay"
    ]
    
    attempts = 0
    popup_yang_sudah_ditutup = set()  # Track popup yang sudah pernah ditutup
    
    while attempts < max_attempts:
        jaga_fokus_browser(driver)
        
        # Update loading bar
        tampilkan_loading_bar(attempts, max_attempts, prefix=f'{Y}Memeriksa pop-up:{W}', suffix='Selesai', length=30)
        
        current_popup_found = False
        popup_baru_ditemukan = False
        
        # Coba setiap selector
        for selector in popup_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        try:
                            # Buat identifier unik untuk popup ini
                            popup_id = f"{selector}_{element.location}_{element.size}"
                            
                            # Cek apakah popup ini sudah pernah ditutup
                            if popup_id not in popup_yang_sudah_ditutup:
                                jaga_fokus_browser(driver)
                                element.click()
                                popup_yang_sudah_ditutup.add(popup_id)
                                current_popup_found = True
                                popup_baru_ditemukan = True
                                print(f"{G}Popup baru ditutup: {selector}{W}")
                                time.sleep(0.5)
                            else:
                                # Popup yang sama muncul lagi, abaikan
                                print(f"{Y}Popup berulang diabaikan: {selector}{W}")
                        except:
                            pass
            except:
                continue
        
        # Jika tidak ada popup baru, coba tekan Escape sekali saja
        if not popup_baru_ditemukan and attempts == 0:
            try:
                jaga_fokus_browser(driver)
                actions = ActionChains(driver)
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
                print(f"{Y}Escape key ditekan untuk menutup popup{W}")
            except:
                pass
        
        # Jika tidak ada popup baru yang ditemukan, increment attempts
        if not popup_baru_ditemukan:
            attempts += 1
        else:
            # Reset attempts jika masih ada popup baru yang berhasil ditutup
            # Tapi batasi maksimal 2 kali reset untuk menghindari loop tak terbatas
            if attempts < 2:
                attempts = 0
            else:
                attempts += 1
    
    # Tampilkan loading bar 100%
    tampilkan_loading_bar(max_attempts, max_attempts, prefix=f'{Y}Memeriksa pop-up:{W}', suffix='Selesai', length=30)
    
    if popup_yang_sudah_ditutup:
        print(f"\n{G}Pop-up telah ditangani ({len(popup_yang_sudah_ditutup)} popup ditutup){W}")
    else:
        print(f"\n{Y}Tidak ada pop-up yang ditemukan atau perlu ditutup{W}")
    
    # Tunggu sebentar untuk memastikan popup tidak muncul lagi
    time.sleep(1)
    
    # Cek sekali lagi apakah masih ada popup yang muncul
    popup_masih_ada = False
    for selector in popup_selectors[:3]:  # Cek hanya beberapa selector utama
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    popup_masih_ada = True
                    break
            if popup_masih_ada:
                break
        except:
            continue
    
    if popup_masih_ada:
        print(f"{Y}Masih ada popup yang muncul, tapi akan diabaikan untuk melanjutkan proses{W}")
    
    print(f"{G}Proses penanganan popup selesai, melanjutkan ke tahap berikutnya{W}")

def klik_elemen_dengan_id(driver, elemen_id):
    """
    Klik elemen dengan ID tertentu
    """
    try:
        jaga_fokus_browser(driver)
        elemen = driver.find_element(By.ID, elemen_id)
        elemen.click()
        print(f"{G}Elemen {elemen_id} berhasil diklik.{W}")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"{R}Gagal mengklik elemen {elemen_id}: {e}{W}")
        try:
            jaga_fokus_browser(driver)
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, elemen_id))
            print(f"{G}Elemen {elemen_id} berhasil diklik dengan JavaScript.{W}")
            time.sleep(2)
            return True
        except Exception as e2:
            print(f"{R}Gagal mengklik elemen {elemen_id} dengan JavaScript: {e2}{W}")
            return False

def klik_elemen_login(driver):
    """
    Klik elemen login
    """
    try:
        jaga_fokus_browser(driver)
        
        elemen_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="login-as-member-text-button"]'))
        )
        
        jaga_fokus_browser(driver)
        
        try:
            elemen_login.click()
            print(f"{G}Elemen login berhasil diklik.{W}")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"{R}Gagal mengklik elemen login: {e}{W}")
            try:
                jaga_fokus_browser(driver)
                driver.execute_script("arguments[0].click();", elemen_login)
                print(f"{G}Elemen login berhasil diklik dengan JavaScript.{W}")
                time.sleep(2)
                return True
            except Exception as e2:
                print(f"{R}Gagal mengklik elemen login dengan JavaScript: {e2}{W}")
                return False
            
    except TimeoutException:
        print(f"{R}Elemen login tidak muncul dalam waktu yang ditentukan.{W}")
        return False
    except Exception as e:
        print(f"{R}Terjadi kesalahan saat mencari elemen login: {e}{W}")
        return False

def klik_elemen_signup(driver):
    """
    Klik elemen signup
    """
    try:
        jaga_fokus_browser(driver)
        
        elemen_signup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="switchToSignUp"]'))
        )
        
        jaga_fokus_browser(driver)
        
        try:
            elemen_signup.click()
            print(f"{G}Elemen signup berhasil diklik.{W}")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"{R}Gagal mengklik elemen signup: {e}{W}")
            try:
                jaga_fokus_browser(driver)
                driver.execute_script("arguments[0].click();", elemen_signup)
                print(f"{G}Elemen signup berhasil diklik dengan JavaScript.{W}")
                time.sleep(2)
                return True
            except Exception as e2:
                print(f"{R}Gagal mengklik elemen signup dengan JavaScript: {e2}{W}")
                return False
            
    except TimeoutException:
        print(f"{R}Elemen signup tidak muncul dalam waktu yang ditentukan.{W}")
        return False
    except Exception as e:
        print(f"{R}Terjadi kesalahan saat mencari elemen signup: {e}{W}")
        return False

# def cari_elemen_dengan_bs4_dan_scroll(driver, timeout=60, wait_time=0.5):
#     """
#     Fungsi untuk mencari elemen dengan ID yang mengandung 'root-comment-box-start' sambil scroll
#     dan menangani popup yang muncul saat scrolling.
#     """
#     print(f"{Y}Mencari elemen root-comment-box-start sambil scroll dan tangani popup...{W}")
    
#     # Pastikan browser tetap aktif
#     pastikan_browser_tetap_aktif(driver)
    
#     # Waktu mulai
#     start_time = time.time()
    
#     # Waktu terakhir menjaga fokus
#     last_focus_time = time.time()
    
#     # Jumlah percobaan scroll
#     scroll_attempts = 0
#     max_scroll_attempts = 2
    
#     while scroll_attempts < max_scroll_attempts:
#         # Reset posisi scroll
#         driver.execute_script("window.scrollTo(0, 0);")
#         time.sleep(1)
        
#         print(f"{Y}Percobaan scroll ke-{scroll_attempts + 1}...{W}")
        
#         # Posisi scroll awal
#         posisi_scroll = 0
#         langkah_scroll = 600
#         posisi_scroll_terakhir = -1
        
#         # Scroll sampai tidak bisa scroll lagi
#         while True:
#             # Periksa timeout
#             if time.time() - start_time > timeout:
#                 print(f"{R}Timeout tercapai ({timeout} detik).{W}")
#                 return None
            
#             # Jaga fokus setiap 5 detik
#             current_time = time.time()
#             if current_time - last_focus_time > 5:
#                 jaga_fokus_browser(driver)
#                 last_focus_time = current_time
            
#             # Dapatkan tinggi halaman
#             tinggi_halaman = driver.execute_script("return document.body.scrollHeight")
#             total_langkah = (tinggi_halaman // langkah_scroll) + 1
            
#             # Update loading bar
#             tampilkan_loading_bar(min(posisi_scroll // langkah_scroll, total_langkah), total_langkah, 
#                                  prefix=f'{Y}Mencari elemen:{W}', suffix=f'Scrolling ({scroll_attempts + 1})', length=30)
            
#             # Scroll ke posisi baru
#             driver.execute_script(f"window.scrollTo(0, {posisi_scroll});")
#             time.sleep(wait_time)
            
#             # 🚨 PENTING: Cek dan tutup popup setelah setiap scroll
#             tutup_popup_saat_scroll(driver)
            
#             # Dapatkan posisi scroll aktual
#             posisi_scroll_aktual = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            
#             # Ambil HTML dan parse dengan BeautifulSoup
#             html_saat_ini = driver.page_source
#             soup = BeautifulSoup(html_saat_ini, 'html.parser')
            
#             # Cari elemen yang mengandung "root-comment-box-start" dalam ID
#             elemen_bs4 = soup.find(lambda tag: tag.has_attr('id') and 'root-comment-box-start' in tag['id'])
            
#             if elemen_bs4:
#                 elemen_id = elemen_bs4['id']
                
#                 # Tampilkan loading bar 100%
#                 tampilkan_loading_bar(total_langkah, total_langkah, 
#                                      prefix=f'{Y}Mencari elemen:{W}', suffix=f'{G}Ditemukan!{W}', length=30)
                
#                 print(f"\n{G}🎯 Elemen root-comment-box-start ditemukan: {elemen_id}{W}")
                
#                 # 🚨 PENTING: Tutup popup lagi setelah elemen ditemukan
#                 print(f"{Y}Memeriksa popup setelah elemen ditemukan...{W}")
#                 for i in range(3):  # Coba 3 kali
#                     if tutup_popup_saat_scroll(driver):
#                         print(f"{G}✓ Popup berhasil ditutup setelah elemen ditemukan{W}")
#                     time.sleep(0.5)
                
#                 jaga_fokus_browser(driver)
                
#                 try:
#                     elemen_selenium = driver.find_element(By.ID, elemen_id)
#                     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemen_selenium)
#                     time.sleep(1)
                    
#                     # 🚨 PENTING: Tutup popup sekali lagi setelah scroll ke elemen
#                     print(f"{Y}Memeriksa popup setelah scroll ke elemen...{W}")
#                     tutup_popup_saat_scroll(driver)
                    
#                     return elemen_id
#                 except Exception as e:
#                     print(f"{R}Elemen ditemukan dengan BeautifulSoup tetapi tidak dengan Selenium: {e}{W}")
            
#             # Cek apakah sudah tidak bisa scroll lagi
#             if posisi_scroll_aktual == posisi_scroll_terakhir:
#                 print(f"\n{Y}Tidak bisa scroll lagi. Sudah mencapai batas bawah halaman.{W}")
#                 break
            
#             posisi_scroll_terakhir = posisi_scroll_aktual
#             posisi_scroll += langkah_scroll
        
#         # Tunggu sebentar sebelum percobaan berikutnya
#         if scroll_attempts < max_scroll_attempts - 1:
#             print(f"{Y}Menunggu 10 detik sebelum percobaan berikutnya...{W}")
#             time.sleep(10)
            
#             # Refresh halaman
#             print(f"{Y}Me-refresh halaman...{W}")
#             driver.refresh()
#             time.sleep(5)
#             pastikan_browser_tetap_aktif(driver)
        
#         scroll_attempts += 1
    
#     # Tampilkan loading bar 100%
#     tampilkan_loading_bar(100, 100, 
#                          prefix=f'{Y}Mencari elemen:{W}', suffix=f'{R}Tidak ditemukan{W}', length=30)
    
#     print(f"\n{R}Elemen root-comment-box-start tidak ditemukan setelah {max_scroll_attempts} percobaan{W}")
#     return None

def cari_elemen_dengan_bs4_dan_scroll(driver, timeout=60, wait_time=0.5):
    """
    Fungsi untuk mencari elemen dengan ID yang mengandung 'root-comment-box-start' sambil scroll
    dan menangani popup yang muncul saat scrolling.
    """
    print(f"{Y}Mencari elemen root-comment-box-start sambil scroll dan tangani popup...{W}")
    
    # Pastikan browser tetap aktif
    pastikan_browser_tetap_aktif(driver)
    
    # Waktu mulai
    start_time = time.time()
    
    # Waktu terakhir menjaga fokus
    last_focus_time = time.time()
    
    # Jumlah percobaan scroll
    scroll_attempts = 0
    max_scroll_attempts = 2
    
    while scroll_attempts < max_scroll_attempts:
        # Reset posisi scroll
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        print(f"{Y}Percobaan scroll ke-{scroll_attempts + 1}...{W}")
        
        # Posisi scroll awal
        posisi_scroll = 0
        langkah_scroll = 600
        posisi_scroll_terakhir = -1
        
        # Scroll sampai tidak bisa scroll lagi
        while True:
            # Periksa timeout
            if time.time() - start_time > timeout:
                print(f"{R}Timeout tercapai ({timeout} detik).{W}")
                return None
            
            # Jaga fokus setiap 5 detik
            current_time = time.time()
            if current_time - last_focus_time > 5:
                jaga_fokus_browser(driver)
                last_focus_time = current_time
            
            # Dapatkan tinggi halaman
            tinggi_halaman = driver.execute_script("return document.body.scrollHeight")
            total_langkah = (tinggi_halaman // langkah_scroll) + 1
            
            # Update loading bar
            tampilkan_loading_bar(min(posisi_scroll // langkah_scroll, total_langkah), total_langkah, 
                                 prefix=f'{Y}Mencari elemen:{W}', suffix=f'Scrolling ({scroll_attempts + 1})', length=30)
            
            # Scroll ke posisi baru
            driver.execute_script(f"window.scrollTo(0, {posisi_scroll});")
            time.sleep(wait_time)
            
            # 🚨 PENTING: Cek dan tutup popup setelah setiap scroll
            tutup_popup_saat_scroll(driver)
            
            # Dapatkan posisi scroll aktual
            posisi_scroll_aktual = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            
            # Ambil HTML dan parse dengan BeautifulSoup
            html_saat_ini = driver.page_source
            soup = BeautifulSoup(html_saat_ini, 'html.parser')
            
            # Cari elemen yang mengandung "root-comment-box-start" dalam ID
            elemen_bs4 = soup.find(lambda tag: tag.has_attr('id') and 'root-comment-box-start' in tag['id'])
            
            if elemen_bs4:
                elemen_id = elemen_bs4['id']
                
                # Tampilkan loading bar 100%
                tampilkan_loading_bar(total_langkah, total_langkah, 
                                     prefix=f'{Y}Mencari elemen:{W}', suffix=f'{G}Ditemukan!{W}', length=30)
                
                print(f"\n{G}🎯 Elemen root-comment-box-start ditemukan: {elemen_id}{W}")
                
                # 🚨 BARU: Klik body untuk menghilangkan popup setelah elemen ditemukan
                print(f"{Y}🖱️  Mengklik body untuk menghilangkan popup...{W}")
                try:
                    # Method 1: Klik pada body dengan JavaScript
                    driver.execute_script("""
                        // Klik pada body untuk menghilangkan popup
                        if (document.body) {
                            document.body.click();
                        }
                        
                        // Klik pada area kosong di tengah layar
                        var centerX = window.innerWidth / 2;
                        var centerY = window.innerHeight / 2;
                        
                        var event = new MouseEvent('click', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: centerX,
                            clientY: centerY
                        });
                        
                        document.elementFromPoint(centerX, centerY)?.click();
                        
                        console.log('Body diklik untuk menghilangkan popup');
                    """)
                    print(f"{G}✓ Body berhasil diklik dengan JavaScript{W}")
                    time.sleep(1)
                    
                    # Method 2: Klik dengan ActionChains sebagai backup
                    try:
                        actions = ActionChains(driver)
                        # Klik di tengah layar
                        actions.move_by_offset(0, 0)  # Reset ke tengah
                        actions.click()
                        actions.perform()
                        print(f"{G}✓ Klik tengah layar berhasil dengan ActionChains{W}")
                        time.sleep(0.5)
                    except Exception as action_error:
                        print(f"{Y}⚠️  ActionChains click gagal: {action_error}{W}")
                    
                    # Method 3: Klik pada elemen body secara langsung
                    try:
                        body_element = driver.find_element(By.TAG_NAME, "body")
                        body_element.click()
                        print(f"{G}✓ Body element berhasil diklik langsung{W}")
                        time.sleep(0.5)
                    except Exception as body_error:
                        print(f"{Y}⚠️  Body element click gagal: {body_error}{W}")
                        
                except Exception as click_error:
                    print(f"{R}❌ Gagal mengklik body: {click_error}{W}")
                
                # 🚨 PENTING: Tutup popup lagi setelah klik body
                print(f"{Y}Memeriksa popup setelah klik body...{W}")
                for i in range(3):  # Coba 3 kali
                    if tutup_popup_saat_scroll(driver):
                        print(f"{G}✓ Popup berhasil ditutup setelah klik body (percobaan {i+1}){W}")
                    time.sleep(0.5)
                
                # Tekan Escape sebagai langkah tambahan
                try:
                    print(f"{Y}🔑 Menekan Escape key untuk memastikan popup hilang...{W}")
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ESCAPE)
                    actions.perform()
                    print(f"{G}✓ Escape key berhasil ditekan{W}")
                    time.sleep(1)
                except Exception as escape_error:
                    print(f"{Y}⚠️  Escape key gagal: {escape_error}{W}")
                
                jaga_fokus_browser(driver)
                
                try:
                    elemen_selenium = driver.find_element(By.ID, elemen_id)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemen_selenium)
                    time.sleep(1)
                    
                    # 🚨 PENTING: Tutup popup sekali lagi setelah scroll ke elemen
                    print(f"{Y}Memeriksa popup setelah scroll ke elemen...{W}")
                    tutup_popup_saat_scroll(driver)
                    
                    # Klik body sekali lagi setelah scroll ke elemen
                    print(f"{Y}🖱️  Klik body sekali lagi setelah scroll ke elemen...{W}")
                    try:
                        driver.execute_script("""
                            // Klik body lagi setelah scroll
                            if (document.body) {
                                document.body.click();
                            }
                            
                            // Klik area di sekitar elemen yang ditemukan
                            var element = document.getElementById(arguments[0]);
                            if (element) {
                                var rect = element.getBoundingClientRect();
                                var clickX = rect.left + (rect.width / 2);
                                var clickY = rect.top - 50; // Klik sedikit di atas elemen
                                
                                var clickEvent = new MouseEvent('click', {
                                    view: window,
                                    bubbles: true,
                                    cancelable: true,
                                    clientX: clickX,
                                    clientY: clickY
                                });
                                
                                document.elementFromPoint(clickX, clickY)?.click();
                            }
                        """, elemen_id)
                        print(f"{G}✓ Area sekitar elemen berhasil diklik{W}")
                        time.sleep(1)
                    except Exception as final_click_error:
                        print(f"{Y}⚠️  Klik final gagal: {final_click_error}{W}")
                    
                    return elemen_id
                except Exception as e:
                    print(f"{R}Elemen ditemukan dengan BeautifulSoup tetapi tidak dengan Selenium: {e}{W}")
            
            # Cek apakah sudah tidak bisa scroll lagi
            if posisi_scroll_aktual == posisi_scroll_terakhir:
                print(f"\n{Y}Tidak bisa scroll lagi. Sudah mencapai batas bawah halaman.{W}")
                break
            
            posisi_scroll_terakhir = posisi_scroll_aktual
            posisi_scroll += langkah_scroll
        
        # Tunggu sebentar sebelum percobaan berikutnya
        if scroll_attempts < max_scroll_attempts - 1:
            print(f"{Y}Menunggu 10 detik sebelum percobaan berikutnya...{W}")
            time.sleep(10)
            
            # Refresh halaman
            print(f"{Y}Me-refresh halaman...{W}")
            driver.refresh()
            time.sleep(5)
            pastikan_browser_tetap_aktif(driver)
        
        scroll_attempts += 1
    
    # Tampilkan loading bar 100%
    tampilkan_loading_bar(100, 100, 
                         prefix=f'{Y}Mencari elemen:{W}', suffix=f'{R}Tidak ditemukan{W}', length=30)
    
    print(f"\n{R}Elemen root-comment-box-start tidak ditemukan setelah {max_scroll_attempts} percobaan{W}")
    return None



def validasi_file_diperlukan():
    """
    Validasi apakah file-file yang diperlukan ada
    """
    files_required = {
        'list.txt': 'File berisi daftar URL yang akan diproses',
        'komen.txt': 'File berisi template komentar',
        'akun.txt': 'File berisi akun Google (email dan password)'
    }
    
    missing_files = []
    
    for file_name, description in files_required.items():
        if not os.path.exists(file_name):
            missing_files.append((file_name, description))
    
    if missing_files:
        print(f"{R}{'='*60}")
        print(f"{R}FILE YANG DIPERLUKAN TIDAK DITEMUKAN!")
        print(f"{R}{'='*60}{W}")
        
        for file_name, description in missing_files:
            print(f"{R}✗ {file_name}{W} - {description}")
        
        print(f"\n{Y}Membuat file yang diperlukan...{W}")
        
        # Buat file yang hilang
        for file_name, description in missing_files:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    if file_name == 'list.txt':
                        file.write("# Masukkan URL di sini, satu URL per baris\n")
                        file.write("# Contoh:\n")
                        file.write("# https://example.com/page1\n")
                        file.write("# https://example.com/page2\n")
                    elif file_name == 'komen.txt':
                        file.write("# Masukkan template komentar di sini\n")
                        file.write("# Format untuk link: [url]teks yang akan diberi link[link:https://website.com]\n")
                        file.write("# Contoh:\n")
                        file.write("# Terima kasih atas informasinya! [url]Kunjungi website kami[link:https://mywebsite.com] untuk info lebih lanjut.\n")
                    elif file_name == 'akun.txt':
                        file.write("# Masukkan akun Google di sini\n")
                        file.write("# Format: email di baris pertama, password di baris kedua\n")
                        file.write("# Contoh:\n")
                        file.write("# email1@gmail.com\n")
                        file.write("# password1\n")
                        file.write("# email2@gmail.com\n")
                        file.write("# password2\n")
                        file.write("# dst...\n")
                
                print(f"{G}✓ {file_name} berhasil dibuat{W}")
            except Exception as e:
                print(f"{R}✗ Gagal membuat {file_name}: {e}{W}")
        
        print(f"\n{Y}Silakan isi file-file tersebut sebelum menjalankan program lagi.{W}")
        print(f"\n{B}Format file akun.txt:{W}")
        print(f"{G}email1@gmail.com{W}")
        print(f"{G}password1{W}")
        print(f"{G}email2@gmail.com{W}")
        print(f"{G}password2{W}")
        print(f"{Y}(dan seterusnya untuk akun tambahan){W}")
        return False
    
    # Validasi khusus untuk file akun.txt
    if os.path.exists('akun.txt'):
        try:
            with open('akun.txt', 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            
            if len(lines) < 2:
                print(f"{R}{'='*60}")
                print(f"{R}FILE akun.txt TIDAK VALID!")
                print(f"{R}{'='*60}{W}")
                print(f"{R}File akun.txt harus berisi minimal 2 baris (email dan password){W}")
                print(f"\n{B}Format yang benar:{W}")
                print(f"{G}email1@gmail.com{W}")
                print(f"{G}password1{W}")
                print(f"{G}email2@gmail.com{W}")
                print(f"{G}password2{W}")
                return False
            
            if len(lines) % 2 != 0:
                print(f"{Y}{'='*60}")
                print(f"{Y}PERINGATAN: FILE akun.txt")
                print(f"{Y}{'='*60}{W}")
                print(f"{Y}Jumlah baris tidak genap. Pastikan setiap email memiliki password.{W}")
                print(f"{Y}Baris terakhir mungkin tidak akan digunakan.{W}")
                print(f"\n{B}Format yang benar:{W}")
                print(f"{G}email1@gmail.com{W}")
                print(f"{G}password1{W}")
                print(f"{G}email2@gmail.com{W}")
                print(f"{G}password2{W}")
                
                response = input(f"\n{Y}Lanjutkan? (y/n): {W}").strip().lower()
                if response != 'y':
                    return False
            
            print(f"{G}✓ File akun.txt valid dengan {len(lines)//2} akun{W}")
            
        except Exception as e:
            print(f"{R}Error saat validasi akun.txt: {e}{W}")
            return False
    
    print(f"{G}✓ Semua file yang diperlukan ditemukan dan valid{W}")
    return True

def baca_url_yang_sudah_selesai():
    """
    Membaca URL yang sudah selesai diproses dari komen-done.txt
    """
    try:
        with open('komen-done.txt', 'r', encoding='utf-8') as file:
            urls_selesai = set(line.strip() for line in file if line.strip())
        return urls_selesai
    except FileNotFoundError:
        return set()
    except Exception as e:
        print(f"{Y}Peringatan: Gagal membaca komen-done.txt: {e}{W}")
        return set()

def filter_url_belum_selesai(urls):
    """
    Filter URL yang belum selesai diproses
    """
    urls_selesai = baca_url_yang_sudah_selesai()
    urls_belum_selesai = [url for url in urls if url not in urls_selesai]
    
    if urls_selesai:
        print(f"{G}Ditemukan {len(urls_selesai)} URL yang sudah selesai diproses{W}")
        print(f"{Y}Akan memproses {len(urls_belum_selesai)} URL yang belum selesai{W}")
    else:
        print(f"{Y}Tidak ada URL yang sudah selesai, akan memproses semua URL{W}")
    
    return urls_belum_selesai

def tampilkan_statistik_url(urls_total, urls_selesai, urls_belum_selesai):
    """
    Menampilkan statistik URL
    """
    print(f"\n{B}{'='*50}")
    print(f"{B}STATISTIK URL")
    print(f"{B}{'='*50}{W}")
    print(f"{W}Total URL di list.txt: {G}{len(urls_total)}{W}")
    print(f"{W}URL sudah selesai: {G}{len(urls_selesai)}{W}")
    print(f"{W}URL belum selesai: {Y}{len(urls_belum_selesai)}{W}")
    
    if len(urls_selesai) > 0:
        persentase = (len(urls_selesai) / len(urls_total)) * 100
        print(f"{W}Progress: {G}{persentase:.1f}%{W}")
    
    print(f"{B}{'='*50}{W}")

def proses_satu_url(driver, url, index, total):
    """
    Memproses satu URL dengan pembersihan browser
    """
    try:
        print(f"\n{R}{'='*50}")
        print(f"{Y}[{W}{index}/{total}{Y}] Memproses URL: {W}{url}")
        print(f"{R}{'='*50}{W}")
        
        driver.get(url)
        time.sleep(3)
        
        # Pastikan browser tetap aktif
        pastikan_browser_tetap_aktif(driver)
        
        # Tangani popup
        tangani_popup(driver)
        
        # Cari elemen root-comment-box-start
        elemen_id = cari_elemen_dengan_bs4_dan_scroll(driver)
        
        if elemen_id:
            print(f"{G}Elemen root-comment-box-start ditemukan: {elemen_id}{W}")
            
            # Langkah 1: Klik elemen root-comment-box-start
            if klik_elemen_dengan_id(driver, elemen_id):
                print(f"{G}Berhasil mengklik elemen root-comment-box-start{W}")
                
                # Langkah 2: Klik elemen login
                if klik_elemen_login(driver):
                    print(f"{G}Berhasil mengklik elemen login{W}")
                    
                    # Langkah 3: Klik elemen signup
                    if klik_elemen_signup(driver):
                        print(f"{G}Berhasil mengklik elemen signup{W}")
                        
                        # Panggil modul daftar.py
                        try:
                            print(f"\n{W}Melanjutkan proses ke modul daftar.py...{W}")
                            import daftar
                            daftar.lanjutkan_proses(driver, url)
                            
                            # TAMBAHAN: Panggil logout dan pembersihan setelah proses selesai
                            print(f"\n{Y}Memulai proses logout dan pembersihan browser...")
                            try:
                                import logout
                                driver = logout.lakukan_logout_dan_bersihkan(driver, url)
                                
                                if driver is None:
                                    print(f"{R}Pembersihan browser gagal, driver menjadi None")
                                    return False
                                else:
                                    print(f"{G}✓ Browser berhasil dibersihkan untuk URL ke-{W}{index}")
                                    
                            except ImportError:
                                print(f"{R}Modul logout.py tidak ditemukan.{W}")
                            except Exception as logout_error:
                                print(f"{R}Error saat logout dan pembersihan: {logout_error}{W}")
                            
                            print(f"{G}✓ URL ke-{index} berhasil diproses dan dibersihkan{W}")
                            return True
                            
                        except ImportError:
                            print(f"{R}Modul daftar.py tidak ditemukan.{W}")
                            return False
                        except Exception as e:
                            print(f"{R}Terjadi kesalahan saat menjalankan daftar.py: {e}{W}")
                            return False
                    else:
                        print(f"{R}Gagal mengklik elemen signup{W}")
                        return False
                else:
                    print(f"{R}Gagal mengklik elemen login{W}")
                    return False
            else:
                print(f"{R}Gagal mengklik elemen root-comment-box-start{W}")
                return False
        else:
            print(f"{R}Elemen root-comment-box-start tidak ditemukan{W}")
            return False
            
    except Exception as e:
        print(f"{R}Gagal memproses URL {url}: {e}{W}")
        
        # Coba lakukan pembersihan meskipun ada error
        try:
            print(f"{Y}Mencoba pembersihan browser meskipun ada error...{W}")
            import logout
            driver = logout.lakukan_logout_dan_bersihkan(driver, url)
            
            if driver is None:
                print(f"{R}Pembersihan gagal setelah error{W}")
                return False
            else:
                print(f"{G}Pembersihan berhasil meskipun ada error{W}")
                
        except Exception as cleanup_error:
            print(f"{R}Gagal melakukan pembersihan setelah error: {cleanup_error}{W}")
        
        return False

def menu_utama():
    """
    Menu utama program
    """
    clear_terminal()
    print(banner)
    
    print(f"{R}{'='*50}")
    print(f"{W}🐍MODE OPERASI")
    print(f"{R}{'='*50}{W}")
    
    print(f"{W}1. {G}Mode Otomatis - Proses semua URL secara otomatis")
    print(f"{W}2. {G}Mode Test - Test dengan satu URL (Dev)")
    print(f"{W}3. {G}Keluar")
    
    while True:
        try:
            pilihan = input(f"\n{Y}📝 Masukkan pilihan : {W}").strip()
            
            if pilihan == '1':
                print(f"{G}✅ Memulai mode otomatis...")
                mode_otomatis()
                break
            elif pilihan == '2':
                print(f"{G}✅ Memulai mode test...")
                mode_test()
                break
            elif pilihan == '3':
                print(f"{R}⚠️ Keluar dari program...")
                sys.exit(0)
            else:
                print(f"{R}Pilihan tidak valid. Masukkan 1, 2, atau 3.")
                
        except KeyboardInterrupt:
            print(f"\n{W}Program dibatalkan oleh user")
            sys.exit(0)

def mode_otomatis():
    """
    Mode otomatis untuk memproses semua URL
    """
    # Inisialisasi driver
    driver = inisialisasi_driver()
    if not driver:
        print(f"{R}Gagal menginisialisasi browser{W}")
        return
    
    # Daftarkan fungsi untuk menutup driver
    def close_driver():
        try:
            driver.quit()
        except:
            pass
    
    atexit.register(close_driver)
    
    # Baca URL dari file
    urls = baca_url_dari_file("list.txt")
    
    if not urls:
        print(f"{R}Tidak ada URL yang ditemukan di file list.txt{W}")
        driver.quit()
        return
    
    # Filter URL yang belum selesai
    urls_belum_selesai = filter_url_belum_selesai(urls)
    
    if not urls_belum_selesai:
        print(f"{G}Semua URL sudah selesai diproses!{W}")
        driver.quit()
        return
    
    print(f"\n{G}Memulai pemrosesan {len(urls_belum_selesai)} URL...{W}")
    
    # Proses setiap URL
    berhasil = 0
    gagal = 0
    
    for i, url in enumerate(urls_belum_selesai, 1):
        try:
            if proses_satu_url(driver, url, i, len(urls_belum_selesai)):
                berhasil += 1
            else:
                gagal += 1
                
            # Tunggu sebentar sebelum URL berikutnya
            if i < len(urls_belum_selesai):
                print(f"{Y}Menunggu 5 detik sebelum URL berikutnya...{W}")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print(f"\n{Y}Proses dibatalkan oleh user{W}")
            break
        except Exception as e:
            print(f"{R}Error pada URL {url}: {e}{W}")
            gagal += 1
    
    # Tampilkan hasil akhir
    print(f"\n{Y}{'='*50}")
    print(f"{G}HASIL PEMROSESAN")
    print(f"{Y}{'='*50}{W}")
    print(f"{G}Berhasil: {W}{berhasil}")
    print(f"{R}Gagal: {W}{gagal}")
    print(f"{W}Total: {W}{berhasil + gagal}")
    
    # Tutup browser
    try:
        driver.quit()
        print(f"{G}Browser berhasil ditutup.")
    except:
        pass

def mode_test():
    """
    Mode test untuk satu URL
    """
    # Baca URL dari file
    urls = baca_url_dari_file("list.txt")
    
    if not urls:
        print(f"{R}Tidak ada URL yang ditemukan di file list.txt")
        return
    
    # Tampilkan daftar URL
    print(f"\n{Y}DAFTAR URL YANG TERSEDIA:{W}")
    for i, url in enumerate(urls, 1):
        print(f"{G}{i}. {W}{url}")
    
    while True:
        try:
            pilihan = input(f"\n{Y}Pilih nomor URL untuk test (1-{len(urls)}): {W}").strip()
            
            try:
                index = int(pilihan) - 1
                if 0 <= index < len(urls):
                    url_terpilih = urls[index]
                    break
                else:
                    print(f"{R}Nomor tidak valid. Pilih antara 1-{len(urls)}.{W}")
            except ValueError:
                print(f"{R}Masukkan nomor yang valid.")
                
        except KeyboardInterrupt:
            print(f"\n{Y}Test dibatalkan")
            return
    
    print(f"\n{G}URL terpilih: {W}{url_terpilih}")
    
    # Inisialisasi driver
    driver = inisialisasi_driver()
    if not driver:
        print(f"{R}Gagal menginisialisasi browser")
        return
    
    # Daftarkan fungsi untuk menutup driver
    def close_driver():
        try:
            driver.quit()
        except:
            pass
    
    atexit.register(close_driver)
    
    # Proses URL terpilih
    try:
        if proses_satu_url(driver, url_terpilih, 1, 1):
            print(f"\n{G}✓ Test berhasil untuk URL: {W}{url_terpilih}")
        else:
            print(f"\n{R}✗ Test gagal untuk URL: {W}{url_terpilih}")
    except KeyboardInterrupt:
        print(f"\n{Y}Test dibatalkan oleh user")
    except Exception as e:
        print(f"\n{R}Error saat test: {e}{W}")
    
    # Tutup browser
    try:
        driver.quit()
        print(f"{G}Browser berhasil ditutup.{W}")
    except:
        pass

def tampilkan_info_sistem():
    """
    Menampilkan informasi sistem dan versi
    """
    import platform
    
    print(f"{B}{'='*50}")
    print(f"{B}INFORMASI SISTEM")
    print(f"{B}{'='*50}{W}")
    print(f"{W}OS: {G}{platform.system()} {platform.release()}{W}")
    print(f"{W}Python: {G}{platform.python_version()}{W}")
    
    try:
        import selenium
        print(f"{W}Selenium: {G}{selenium.__version__}{W}")
    except ImportError:
        print(f"{W}Selenium: {R}Tidak tersedia{W}")
    
    try:
        import undetected_chromedriver as uc
        print(f"{W}Undetected ChromeDriver: {G}Tersedia{W}")
    except ImportError:
        print(f"{W}Undetected ChromeDriver: {R}Tidak tersedia{W}")
    
    try:
        from bs4 import BeautifulSoup
        print(f"{W}BeautifulSoup: {G}Tersedia{W}")
    except ImportError:
        print(f"{W}BeautifulSoup: {R}Tidak tersedia{W}")
    
    try:
        from colorama import Fore
        print(f"{W}Colorama: {G}Tersedia{W}")
    except ImportError:
        print(f"{W}Colorama: {R}Tidak tersedia{W}")
    
    print(f"{B}{'='*50}{W}")

def backup_file_penting():
    """
    Backup file dinonaktifkan
    """
    pass

def cek_koneksi_browser(driver, timeout=5):
    """
    Memeriksa apakah koneksi ke browser masih aktif
    """
    try:
        driver.execute_script("return navigator.userAgent;")
        return True
    except Exception as e:
        if "Connection" in str(e) or "HTTPConnectionPool" in str(e):
            return False
        return True

def coba_reconnect_browser(driver, url, max_attempts=3):
    """
    Fungsi untuk mencoba menghubungkan kembali browser jika koneksi terputus
    """
    print(f"{Y}Koneksi ke browser terputus. Mencoba menghubungkan kembali...{W}")
    
    for attempt in range(max_attempts):
        try:
            print(f"{Y}Percobaan reconnect ke-{attempt+1}/{max_attempts}...{W}")
            
            # Tutup driver yang ada
            try:
                driver.quit()
            except:
                pass
            
            # Inisialisasi driver baru
            new_driver = inisialisasi_driver()
            if not new_driver:
                continue
            
            # Buka URL terakhir
            new_driver.get(url)
            print(f"{G}Berhasil menghubungkan kembali: {url}{W}")
            
            # Pastikan browser tetap aktif
            pastikan_browser_tetap_aktif(new_driver)
            
            return new_driver
            
        except Exception as e:
            print(f"{R}Gagal reconnect percobaan ke-{attempt+1}: {e}{W}")
            time.sleep(3)
    
    print(f"{R}Gagal reconnect setelah {max_attempts} percobaan{W}")
    return None

def tampilkan_statistik_akun():
    """
    Menampilkan statistik akun yang tersedia
    """
    try:
        print(f"\n{B}{'='*50}")
        print(f"{B}STATISTIK AKUN GOOGLE")
        print(f"{B}{'='*50}{W}")
        
        # Hitung akun aktif
        akun_aktif = 0
        if os.path.exists('akun.txt'):
            with open('akun.txt', 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            akun_aktif = len(lines) // 2
        
        # Hitung akun limit
        akun_limit = 0
        if os.path.exists('akunlimit.txt'):
            with open('akunlimit.txt', 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
            akun_limit = len(lines) // 2
        
        print(f"{W}Akun aktif tersedia: {G}{akun_aktif}{W}")
        print(f"{W}Akun terkena limit: {R}{akun_limit}{W}")
        print(f"{W}Total akun: {Y}{akun_aktif + akun_limit}{W}")
        
        if akun_aktif == 0:
            print(f"\n{R}⚠️  PERINGATAN: Tidak ada akun aktif tersedia!{W}")
            print(f"{Y}Silakan tambahkan akun ke file akun.txt{W}")
            return False
        elif akun_aktif == 1:
            print(f"\n{Y}⚠️  PERINGATAN: Hanya tersisa 1 akun aktif!{W}")
            print(f"{Y}Disarankan menambah akun cadangan ke file akun.txt{W}")
        
        print(f"{B}{'='*50}{W}")
        return True
        
    except Exception as e:
        print(f"{R}Error saat menampilkan statistik akun: {e}{W}")
        return True  # Tetap lanjutkan meskipun error statistik

def main():
    """
    Fungsi utama program
    """
    try:
        # Bersihkan terminal dan tampilkan banner
        clear_terminal()
        print(banner)
        
        # Tampilkan informasi sistem
        tampilkan_info_sistem()
        
        # Validasi file yang diperlukan
        if not validasi_file_diperlukan():
            input(f"\n{Y}Tekan Enter untuk keluar...{W}")
            sys.exit(1)
        
        # Tampilkan statistik akun
        if not tampilkan_statistik_akun():
            input(f"\n{Y}Tekan Enter untuk keluar...{W}")
            sys.exit(1)
        
        # Buat backup file penting
        print(f"\n{Y}Membuat backup file penting...{W}")
        backup_file_penting()
        
        # Baca dan tampilkan statistik URL
        urls_total = baca_url_dari_file("list.txt")
        if not urls_total:
            print(f"{R}File list.txt kosong atau tidak berisi URL yang valid{W}")
            print(f"{Y}Silakan isi file list.txt dengan URL yang akan diproses{W}")
            input(f"\n{Y}Tekan Enter untuk keluar...{W}")
            sys.exit(1)
        
        # Langsung gunakan filter_url_belum_selesai untuk mendapatkan statistik
        urls_belum_selesai = filter_url_belum_selesai(urls_total)
        
        # Hitung URL yang sudah selesai
        urls_selesai_count = len(urls_total) - len(urls_belum_selesai)
        
        # Tampilkan statistik sederhana
        print(f"\n{B}{'='*50}")
        print(f"{B}STATISTIK URL")
        print(f"{B}{'='*50}{W}")
        print(f"{W}Total URL di list.txt: {G}{len(urls_total)}{W}")
        print(f"{W}URL sudah selesai: {G}{urls_selesai_count}{W}")
        print(f"{W}URL belum selesai: {Y}{len(urls_belum_selesai)}{W}")
        
        if urls_selesai_count > 0:
            persentase = (urls_selesai_count / len(urls_total)) * 100
            print(f"{W}Progress: {G}{persentase:.1f}%{W}")
        
        print(f"{B}{'='*50}{W}")
        
        if not urls_belum_selesai:
            print(f"\n{G}{'='*60}")
            print(f"{G}SEMUA URL SUDAH SELESAI DIPROSES!")
            print(f"{G}{'='*60}{W}")
            input(f"\n{Y}Tekan Enter untuk keluar...{W}")
            sys.exit(0)
        
        # Tampilkan menu utama
        menu_utama()
        
    except KeyboardInterrupt:
        print(f"\n{Y}Program dibatalkan oleh user{W}")
        sys.exit(0)
    except Exception as e:
        print(f"{R}Terjadi kesalahan fatal: {e}{W}")
        input(f"\n{Y}Tekan Enter untuk keluar...{W}")
        sys.exit(1)

# Jalankan fungsi jika file ini dijalankan langsung
if __name__ == "__main__":
    main()
