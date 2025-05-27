from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import random
import string
from colorama import Fore, init
from bs4 import BeautifulSoup

# Initialize Colorama
init(autoreset=True)

# Colors for terminal text
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW

def pastikan_browser_tetap_aktif(driver):
    """
    Fungsi untuk memastikan browser tetap aktif meskipun tidak di foreground
    """
    try:
        # print(f"{Y}Memastikan browser tetap aktif di daftar.py...{W}")
        
        # Tambahkan script untuk mencegah throttling saat tab tidak aktif
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
        print(f"{G}Browser akan tetap aktif meskipun tidak di foreground: {result}{W}")
        return True
    except Exception as e:
        print(f"{R}Gagal menerapkan script anti-throttling: {W}{e}")
        return False

def jaga_fokus_browser(driver):
    """
    Fungsi untuk menjaga fokus browser secara periodik
    """
    try:
        # Gunakan JavaScript untuk memfokuskan window
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
        print(f"{R}Gagal menjaga fokus browser: {W}{e}")
        return False

def baca_akun_google():
    """
    Membaca email dan password dari file akun.txt
    """
    try:
        if not os.path.exists('akun.txt'):
            print(f"{R}File akun.txt tidak ditemukan{W}")
            return None, None
            
        with open('akun.txt', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            
        if len(lines) >= 2:
            email = lines[0]
            password = lines[1]
            return email, password
        else:
            print(f"{R}Format file akun.txt tidak valid. Harus ada email di baris 1 dan password di baris 2")
            return None, None
            
    except Exception as e:
        print(f"{R}Error membaca file akun.txt: {W}{e}")
        return None, None

def pindahkan_akun_ke_limit(email, password):
    """
    Memindahkan akun yang terkena limit ke file akunlimit.txt dan menghapus dari akun.txt
    """
    try:
        # Simpan ke akunlimit.txt
        with open('akunlimit.txt', 'a', encoding='utf-8') as file:
            file.write(f"{email}\n{password}\n")
        print(f"{Y}Akun {email} dipindahkan ke akunlimit.txt{W}")
        
        # Baca semua akun dari akun.txt
        if os.path.exists('akun.txt'):
            with open('akun.txt', 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
            
            # Hapus akun yang terkena limit (2 baris pertama)
            if len(lines) >= 2:
                lines_baru = lines[2:]  # Ambil dari baris ke-3 dst
                
                # Tulis ulang file akun.txt tanpa akun yang terkena limit
                with open('akun.txt', 'w', encoding='utf-8') as file:
                    for line in lines_baru:
                        file.write(line + '\n')
                
                print(f"{G}Akun {email} berhasil dihapus dari akun.txt")
                return True
            else:
                print(f"{Y}Tidak ada akun lain di akun.txt")
                return False
        
        return False
        
    except Exception as e:
        print(f"{R}Error saat memindahkan akun ke limit: {W}{e}")
        return False

def cek_akun_terkena_limit(driver):
    """
    Mengecek apakah ada class="gPpQmL" yang menandakan akun terkena limit
    """
    try:
        # Ambil HTML halaman
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Cari elemen dengan class="gPpQmL"
        elemen_limit = soup.find(class_="gPpQmL")
        
        if elemen_limit:
            print(f"{R}Terdeteksi class='gPpQmL' - Akun terkena limit!")
            return True
        else:
            print(f"{G}Tidak ada class='gPpQmL' - Akun normal")
            return False
            
    except Exception as e:
        print(f"{R}Error saat mengecek limit akun: {W}{e}")
        return False

def lanjutkan_proses(driver, url):
    """
    Fungsi untuk melanjutkan proses pendaftaran setelah klik elemen signup.
    DIMODIFIKASI: Sekarang menggunakan akun dari file akun.txt
    """
    try:
        print(f"{Y}=== {G}Melanjutkan proses pendaftaran di {W}{url} {Y}===")
        
        # Cek koneksi sebelum melanjutkan
        if not cek_koneksi_browser(driver):
            print(f"{R}Koneksi ke browser terputus sebelum memulai proses pendaftaran")
            simpan_url_gagal(url, "Koneksi browser terputus sebelum pendaftaran")
            # Coba reconnect
            new_driver = coba_reconnect_browser(driver, url)
            if new_driver:
                driver = new_driver
            else:
                print(f"{R}Tidak dapat melanjutkan proses karena koneksi terputus")
                return
        
        # Terapkan anti-throttling dengan penanganan error
        try:
            pastikan_browser_tetap_aktif(driver)
        except Exception as e:
            print(f"{Y}Peringatan: Gagal menerapkan anti-throttling: {W}{e}")
            # Cek apakah koneksi terputus
            if not cek_koneksi_browser(driver):
                simpan_url_gagal(url, f"Anti-throttling gagal: {e}")
                new_driver = coba_reconnect_browser(driver, url)
                if new_driver:
                    driver = new_driver
                    # Coba lagi dengan driver baru
                    return lanjutkan_proses(driver, url)
        
        # Jaga fokus browser
        jaga_fokus_browser(driver)
        
        # **BACA AKUN DARI FILE akun.txt**
        email, password = baca_akun_google()
        
        if not email or not password:
            print(f"{R}Tidak dapat membaca akun dari file akun.txt")
            simpan_url_gagal(url, "Gagal membaca akun dari akun.txt")
            return
        
        print(f"{G}Menggunakan akun: {W}{email}")
        
        # Menggunakan BeautifulSoup untuk mencari elemen dengan ID yang mengandung "googleSM_ROOT"
        html_saat_ini = driver.page_source
        soup = BeautifulSoup(html_saat_ini, 'html.parser')
        
        # Cari elemen dengan ID yang mengandung "googleSM_ROOT"
        elemen_bs4 = soup.find(lambda tag: tag.has_attr('id') and 'googleSM_ROOT' in tag['id'])
        
        if elemen_bs4:
            # Jika elemen ditemukan dengan BeautifulSoup, dapatkan ID lengkapnya
            elemen_id = elemen_bs4['id']
            print(f"{G}Elemen dengan ID yang mengandung 'googleSM_ROOT' ditemukan: {elemen_id}{W}")
            
            # Gunakan Selenium untuk menemukan elemen dengan ID yang sama dan klik
            try:
                elemen_selenium = driver.find_element(By.ID, elemen_id)
                
                # Scroll ke elemen tersebut
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemen_selenium)
                time.sleep(1)
                
                # Klik elemen
                elemen_selenium.click()
                print(f"{G}Elemen dengan ID '{elemen_id}' berhasil diklik!")
                
                # Tunggu sebentar setelah klik
                time.sleep(2)
                
                # Proses login Google pada popup dengan akun dari file
                handle_google_login(driver, email, password, url)
                
            except Exception as e:
                print(f"{R}Gagal mengklik elemen dengan ID '{elemen_id}': {W}{e}")
                simpan_url_gagal(url, f"Gagal klik elemen Google: {e}")
                
                # Coba alternatif dengan JavaScript click
                try:
                    print(f"{Y}Mencoba klik dengan JavaScript...{W}")
                    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, elemen_id))
                    print(f"{G}Elemen dengan ID '{elemen_id}' berhasil diklik dengan JavaScript!")
                    time.sleep(2)
                    
                    # Proses login Google pada popup dengan akun dari file
                    handle_google_login(driver, email, password, url)
                    
                except Exception as e2:
                    print(f"{R}Gagal mengklik elemen dengan JavaScript: {e2}{W}")
                    simpan_url_gagal(url, f"Gagal klik elemen Google dengan JavaScript: {e2}")
        else:
            print(f"{R}Elemen dengan ID yang mengandung 'googleSM_ROOT' tidak ditemukan.")
            simpan_url_gagal(url, "Elemen googleSM_ROOT tidak ditemukan")
            
    except Exception as e:
        print(f"{R}Error dalam lanjutkan_proses: {W}{e}")
        simpan_url_gagal(url, f"Error lanjutkan_proses: {e}")

def handle_google_login(driver, email, password, url):
    """
    Fungsi untuk menangani login Google pada popup dengan penanganan koneksi terputus.
    DIPERBAIKI: Tambah pembersihan browser setelah deteksi limit
    """
    try:
        print(f"{Y}Menunggu popup login Google muncul...")
        
        # Tunggu dan beralih ke window popup
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        window_handles = driver.window_handles
        
        print(f"{G}Popup terdeteksi, beralih ke window popup...")
        driver.switch_to.window(window_handles[1])
        # Tambahan untuk atur posisi & ukuran popup
        driver.set_window_size(500, 600)
        driver.set_window_position(0, 0)
        
        # Cek koneksi sebelum melanjutkan
        if not cek_koneksi_browser(driver):
            print(f"{R}Koneksi ke browser terputus setelah beralih ke popup")
            simpan_url_gagal(url, "Koneksi terputus setelah beralih ke popup")
            # Coba reconnect
            new_driver = coba_reconnect_browser(driver, driver.current_url)
            if new_driver:
                driver = new_driver
                # Mulai ulang proses login
                return handle_google_login(driver, email, password, url)
            else:
                raise Exception("Tidak dapat menghubungkan kembali browser")
        
        # Terapkan anti-throttling pada popup
        try:
            pastikan_browser_tetap_aktif(driver)
        except Exception as e:
            print(f"{Y}Peringatan: Gagal menerapkan anti-throttling: {W}{e}")
        
        # Jaga fokus browser pada popup
        try:
            jaga_fokus_browser(driver)
        except Exception as e:
            print(f"{Y}Peringatan: Gagal menjaga fokus browser: {W}{e}")
        
        # Cek koneksi sebelum mencari elemen
        if not cek_koneksi_browser(driver):
            print(f"{R}Koneksi ke browser terputus sebelum mencari form email")
            simpan_url_gagal(url, "Koneksi terputus sebelum mencari form email")
            # Coba reconnect
            new_driver = coba_reconnect_browser(driver, driver.current_url)
            if new_driver:
                driver = new_driver
                # Mulai ulang proses login
                return handle_google_login(driver, email, password, url)
            else:
                raise Exception("Tidak dapat menghubungkan kembali browser")
        
        # Proses login email
        email_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']"))
        )
        
        print(f"{G}Form email ditemukan, mengisi email...")
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(1)
        
        print(f"{Y}Mengklik tombol Next setelah mengisi email...")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "identifierNext"))
        )
        next_button.click()
        
        # Tunggu password field muncul
        time.sleep(3)
        
        # Proses login password
        try:
            password_input = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Enter your password"]'))
            )
        except:
            password_input = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
            )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_input)
        time.sleep(1)
        
        print(f"{G}Form password ditemukan, mengisi password...")
        
        try:
            password_input.clear()
            password_input.send_keys(password)
        except Exception as e1:
            print(f"{Y}Metode 1 gagal: {e1}, mencoba metode 2...")
            try:
                driver.execute_script("arguments[0].value = arguments[1];", password_input, password)
            except Exception as e2:
                print(f"{Y}Metode 2 gagal: {e2}, mencoba metode 3...")
                try:
                    password_input.click()
                    time.sleep(1)
                    password_input.send_keys(password)
                except Exception as e3:
                    print(f"{R}Semua metode gagal mengisi password: {e3}{W}")
                    simpan_url_gagal(url, f"Gagal mengisi password: {e3}")
                    raise
        
        time.sleep(1)
        
        print(f"{Y}Mengklik tombol Next setelah mengisi password...")
        try:
            password_next = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "passwordNext"))
            )
            password_next.click()
        except Exception as e:
            print(f"{Y}Klik normal gagal: {e}, mencoba dengan JavaScript...")
            driver.execute_script("document.getElementById('passwordNext').click();")
        
        # Tunggu proses login selesai
        print(f"{Y}Menunggu proses login selesai...")
        time.sleep(5)
        
        # Kembali ke window utama
        print(f"{Y}Kembali ke window utama...")
        driver.switch_to.window(window_handles[0])
        
        # **CEK APAKAH AKUN TERKENA LIMIT**
        print(f"{Y}Mengecek apakah akun terkena limit...")
        time.sleep(7)  # Tunggu halaman dimuat
        
        if cek_akun_terkena_limit(driver):
            print(f"{R}Akun {email} terkena limit! Memindahkan ke akunlimit.txt...")
            
            # Pindahkan akun ke file limit
            if pindahkan_akun_ke_limit(email, password):
                print(f"{Y}Akun dipindahkan. Melakukan pembersihan browser sebelum akun berikutnya...")
                
                # **TAMBAHAN: PEMBERSIHAN BROWSER SETELAH LIMIT TERDETEKSI**
                try:
                    # Import fungsi logout dan pembersihan
                    import logout
                    
                    print(f"{G}{'='*50}")
                    print(f"{W}PEMBERSIHAN BROWSER SETELAH AKUN TERKENA LIMIT")
                    print(f"{G}{'='*50}{W}")
                    
                    # Lakukan logout dari Google terlebih dahulu
                    print(f"{Y}[{W}1/4{Y}] Logout dari Google...")
                    logout.logout_dari_google(driver)
                    
                    # Hapus semua cookies
                    print(f"{Y}[{W}2/4{Y}] Menghapus semua cookies...")
                    logout.hapus_cookies_menyeluruh(driver)
                    
                    # Hapus semua data browser
                    print(f"{Y}[{W}3/4{Y}] Menghapus semua data browser...")
                    logout.hapus_semua_data_browser(driver)
                    
                    # Reset browser state
                    print(f"{Y}[{W}4/4{Y}] Reset browser state...")
                    logout.reset_browser_state(driver)
                    
                    print(f"{G}✓ Pembersihan browser lengkap selesai")
                    
                except ImportError:
                    print(f"{Y}Modul logout tidak tersedia, melakukan pembersihan sederhana...")
                    
                    print(f"{B}{'='*50}")
                    print(f"{B}PEMBERSIHAN BROWSER SEDERHANA SETELAH AKUN TERKENA LIMIT")
                    print(f"{B}{'='*50}{W}")
                    
                    # Logout dari Google sederhana
                    print(f"{Y}[1/2] Logout dari Google...")
                    logout_dari_google_sederhana(driver)
                    
                    # Pembersihan browser sederhana
                    print(f"{Y}[2/2] Pembersihan browser...")
                    pembersihan_browser_sederhana(driver)
                    
                    print(f"{G}✓ Pembersihan sederhana selesai")
                
                except Exception as clean_error:
                    print(f"{Y}Peringatan saat pembersihan lengkap: {W}{clean_error}")
                    print(f"{Y}Mencoba pembersihan sederhana...")
                    
                    # Fallback ke pembersihan sederhana
                    try:
                        logout_dari_google_sederhana(driver)
                        pembersihan_browser_sederhana(driver)
                        print(f"{G}✓ Pembersihan fallback selesai")
                    except Exception as fallback_error:
                        print(f"{Y}Peringatan pembersihan fallback: {W}{fallback_error}")
                        # Pembersihan minimal terakhir
                        try:
                            driver.delete_all_cookies()
                            driver.execute_script("window.localStorage.clear();")
                            driver.execute_script("window.sessionStorage.clear();")
                            print(f"{G}✓ Pembersihan minimal selesai")
                        except:
                            print(f"{Y}Pembersihan minimal juga gagal, melanjutkan tanpa pembersihan")
                
                # **PERBAIKAN: BUKA URL KEMBALI SETELAH PEMBERSIHAN**
                print(f"{G}{'='*50}")
                print(f"{Y}Membuka kembali URL setelah pembersihan: {W}{url}")
                print(f"{G}{'='*50}")
                try:
                    driver.get(url)
                    print(f"{G}✓ URL berhasil dibuka kembali")
                    time.sleep(5)  # Tunggu halaman dimuat sepenuhnya
                    
                    # Pastikan browser tetap aktif setelah membuka URL
                    pastikan_browser_tetap_aktif(driver)
                    
                except Exception as url_error:
                    print(f"{R}Gagal membuka URL kembali: {url_error}{W}")
                    simpan_url_gagal(url, f"Gagal membuka URL setelah pembersihan: {url_error}")
                    return
                
                # Baca akun berikutnya
                email_baru, password_baru = baca_akun_google()
                
                if email_baru and password_baru:
                    print(f"{G}Menggunakan akun berikutnya: {W}{email_baru}")
                    
                    # **MULAI DARI AWAL DENGAN BROWSER YANG BERSIH DAN URL YANG SUDAH DIBUKA**
                    return lanjutkan_proses_dengan_akun_baru(driver, url)
                else:
                    print(f"{R}Tidak ada akun lain yang tersedia di akun.txt{W}")
                    simpan_url_gagal(url, "Semua akun habis atau terkena limit")
                    return
            else:
                print(f"{R}Gagal memindahkan akun ke limit{W}")
                simpan_url_gagal(url, "Gagal memindahkan akun ke limit")
                return
        else:
            print(f"{G}Login Google berhasil dengan akun: {W}{email}!")
            
            # Lanjutkan dengan modul komentar.py
            try:
                print(f"\n{W}Melanjutkan proses ke modul komentar.py...{W}")
                import komentar
                komentar.lanjutkan_komentar(driver, driver.current_url)
            except ImportError:
                print(f"{R}Modul komentar.py tidak ditemukan. Pastikan file komentar.py ada di direktori yang sama.{W}")
                simpan_url_gagal(url, "Modul komentar.py tidak ditemukan")
            except Exception as e:
                print(f"{R}Terjadi kesalahan saat menjalankan modul komentar.py: {W}{e}")
                simpan_url_gagal(url, f"Error komentar.py: {e}")
        
    except TimeoutException as e:
        print(f"{R}Timeout saat menunggu elemen pada popup login Google: {W}{e}")
        simpan_url_gagal(url, f"Timeout login Google: {e}")
        
        # Coba kembali ke window utama
        try:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        
        # Cek apakah login berhasil dengan mencari elemen user-auth-logout
        print(f"{Y}Memeriksa apakah login berhasil dengan mencari elemen user-auth-logout...{W}")
        time.sleep(5)
        
        html_saat_ini = driver.page_source
        soup = BeautifulSoup(html_saat_ini, 'html.parser')
        elemen_logout = soup.find(attrs={"data-hook": "user-auth-logout"})
        
        if elemen_logout:
            print(f"{G}Elemen user-auth-logout ditemukan! Login berhasil meskipun popup tidak terdeteksi.{W}")
            
            # Cek limit setelah login berhasil
            if cek_akun_terkena_limit(driver):
                print(f"{R}Akun {email} terkena limit setelah login berhasil!{W}")
                if pindahkan_akun_ke_limit(email, password):
                    # **PEMBERSIHAN BROWSER SETELAH TIMEOUT TAPI LOGIN BERHASIL**
                    print(f"{Y}Melakukan pembersihan browser setelah timeout...{W}")
                    try:
                        import logout
                        logout.reset_browser_untuk_url_baru(driver)
                    except:
                        driver.delete_all_cookies()
                        driver.execute_script("window.localStorage.clear();")
                        driver.execute_script("window.sessionStorage.clear();")
                    
                    driver.refresh()
                    time.sleep(5)
                    email_baru, password_baru = baca_akun_google()
                    if email_baru and password_baru:
                        return lanjutkan_proses_dengan_akun_baru(driver, url)
                    else:
                        simpan_url_gagal(url, "Semua akun habis setelah timeout")
                        return
            else:
                print(f"{G}Login Google berhasil!{W}")
                try:
                    print(f"\n{W}Melanjutkan proses ke modul komentar.py...{W}")
                    import komentar
                    komentar.lanjutkan_komentar(driver, driver.current_url)
                except ImportError:
                    print(f"{R}Modul komentar.py tidak ditemukan.{W}")
                    simpan_url_gagal(url, "Modul komentar.py tidak ditemukan setelah timeout")
                except Exception as e:
                    print(f"{R}Terjadi kesalahan saat menjalankan modul komentar.py: {W}{e}")
                    simpan_url_gagal(url, f"Error komentar.py setelah timeout: {e}")
        else:
            print(f"{R}Elemen user-auth-logout tidak ditemukan. Login mungkin gagal.{W}")
            simpan_url_gagal(url, "Login gagal - elemen logout tidak ditemukan setelah timeout")
            
    except Exception as e:
        print(f"{R}Terjadi kesalahan saat proses login Google: {W}{e}")
        simpan_url_gagal(url, f"Error login Google: {e}")
        
        # Coba reconnect jika error disebabkan oleh koneksi terputus
        if "Connection" in str(e) or "HTTPConnectionPool" in str(e):
            print(f"{Y}Error koneksi terdeteksi, mencoba menghubungkan kembali...{W}")
            new_driver = coba_reconnect_browser(driver, driver.current_url)
            if new_driver:
                driver = new_driver
                # Coba login lagi dengan driver baru
                return handle_google_login(driver, email, password, url)
        
        # Coba kembali ke window utama
        try:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        
        # Cek apakah login berhasil dengan mencari elemen user-auth-logout
        print(f"{Y}Memeriksa apakah login berhasil dengan mencari elemen user-auth-logout...{W}")
        time.sleep(5)
        
        html_saat_ini = driver.page_source
        soup = BeautifulSoup(html_saat_ini, 'html.parser')
        elemen_logout = soup.find(attrs={"data-hook": "user-auth-logout"})
        
        if elemen_logout:
            print(f"{G}Elemen user-auth-logout ditemukan! Login berhasil meskipun terjadi error.{W}")
            
            # Cek limit setelah login berhasil
            if cek_akun_terkena_limit(driver):
                print(f"{R}Akun {email} terkena limit setelah error!{W}")
                if pindahkan_akun_ke_limit(email, password):
                    # **PEMBERSIHAN BROWSER SETELAH ERROR TAPI LOGIN BERHASIL**
                    print(f"{Y}Melakukan pembersihan browser setelah error...{W}")
                    try:
                        import logout
                        logout.reset_browser_untuk_url_baru(driver)
                    except:
                        driver.delete_all_cookies()
                        driver.execute_script("window.localStorage.clear();")
                        driver.execute_script("window.sessionStorage.clear();")
                    
                    driver.refresh()
                    time.sleep(5)
                    email_baru, password_baru = baca_akun_google()
                    if email_baru and password_baru:
                        return lanjutkan_proses_dengan_akun_baru(driver, url)
                    else:
                        simpan_url_gagal(url, "Semua akun habis setelah error")
                        return
            else:
                print(f"{G}Login Google berhasil!")
                try:
                    print(f"\n{Y}Melanjutkan proses ke modul komentar.py...")
                    import komentar
                    komentar.lanjutkan_komentar(driver, driver.current_url)
                except ImportError:
                    print(f"{R}Modul komentar.py tidak ditemukan.")
                    simpan_url_gagal(url, "Modul komentar.py tidak ditemukan setelah error")
                except Exception as e:
                    print(f"{R}Terjadi kesalahan saat menjalankan modul komentar.py: {W}{e}")
                    simpan_url_gagal(url, f"Error komentar.py setelah error login: {e}")
        else:
            print(f"{R}Elemen user-auth-logout tidak ditemukan. Login mungkin gagal.")
            simpan_url_gagal(url, "Login gagal - elemen logout tidak ditemukan setelah error")

def lanjutkan_proses_dengan_akun_baru(driver, url):
    """
    Fungsi untuk melanjutkan proses dengan akun baru setelah akun sebelumnya terkena limit
    DIPERBAIKI: URL sudah dibuka sebelumnya, tidak perlu refresh lagi
    """
    try:
        print(f"{Y}=== Memulai ulang proses dengan akun baru ==={W}")
        print(f"{Y}URL saat ini: {W}{driver.current_url}")
        
        # Pastikan browser tetap aktif
        pastikan_browser_tetap_aktif(driver)
        jaga_fokus_browser(driver)
        
        # **TIDAK PERLU REFRESH KARENA URL SUDAH DIBUKA SEBELUMNYA**
        # Tunggu sebentar untuk memastikan halaman dimuat sepenuhnya
        print(f"{Y}Menunggu halaman dimuat sepenuhnya...")
        time.sleep(3)
        
        # Tangani popup terlebih dahulu
        print(f"{Y}Menangani popup sebelum mencari elemen...")
        try:
            import importlib
            main_module = importlib.import_module('main')
            main_module.tangani_popup(driver)
        except:
            print(f"{Y}Menggunakan fungsi popup manual...")
            tangani_popup_manual(driver)
        
        # MULAI DARI AWAL: Cari elemen root-comment-box-start dengan scroll
        print(f"{Y}Mencari elemen root-comment-box-start dengan scroll...")
        
        elemen_id = None
        
        # Coba import fungsi dari main.py
        try:
            import importlib
            main_module = importlib.import_module('main')
            
            # Gunakan fungsi pencarian dengan scroll dari main.py
            elemen_id = main_module.cari_elemen_dengan_bs4_dan_scroll(driver, timeout=60, wait_time=0.5)
            
        except ImportError as ie:
            print(f"{Y}Gagal mengimpor main module: {ie}. Menggunakan metode manual...")
            # Gunakan fungsi manual sebagai fallback
            elemen_id = cari_elemen_root_comment_manual(driver, timeout=60, wait_time=0.5)
            
        except Exception as e:
            print(f"{Y}Error saat menggunakan fungsi main: {e}. Menggunakan metode manual...")
            # Gunakan fungsi manual sebagai fallback
            elemen_id = cari_elemen_root_comment_manual(driver, timeout=60, wait_time=0.5)
        
        if elemen_id:
            print(f"{G}Elemen root-comment-box-start ditemukan: {elemen_id}{W}")
            
            # Tentukan fungsi yang akan digunakan (main atau manual)
            try:
                import importlib
                main_module = importlib.import_module('main')
                use_main_functions = True
            except:
                use_main_functions = False
                print(f"{Y}Menggunakan fungsi manual karena main module tidak tersedia")
            
            # Langkah 1: Klik elemen root-comment-box-start
            klik_berhasil = False
            if use_main_functions:
                try:
                    klik_berhasil = main_module.klik_elemen_dengan_id(driver, elemen_id)
                except:
                    print(f"{Y}Fungsi main gagal, menggunakan manual...")
                    klik_berhasil = klik_elemen_dengan_id_manual(driver, elemen_id)
            else:
                klik_berhasil = klik_elemen_dengan_id_manual(driver, elemen_id)
            
            if klik_berhasil:
                print(f"{G}Berhasil mengklik elemen root-comment-box-start")
                
                # Langkah 2: Klik elemen login
                login_berhasil = False
                if use_main_functions:
                    try:
                        login_berhasil = main_module.klik_elemen_login(driver)
                    except:
                        print(f"{Y}Fungsi login main gagal, menggunakan manual...")
                        login_berhasil = klik_elemen_login_manual(driver)
                else:
                    login_berhasil = klik_elemen_login_manual(driver)
                
                if login_berhasil:
                    print(f"{G}Berhasil mengklik elemen login")
                    
                    # Langkah 3: Klik elemen signup
                    signup_berhasil = False
                    if use_main_functions:
                        try:
                            signup_berhasil = main_module.klik_elemen_signup(driver)
                        except:
                            print(f"{Y}Fungsi signup main gagal, menggunakan manual...")
                            signup_berhasil = klik_elemen_signup_manual(driver)
                    else:
                        signup_berhasil = klik_elemen_signup_manual(driver)
                    
                    if signup_berhasil:
                        print(f"{G}Berhasil mengklik elemen signup")
                        
                        # Langkah 4: Lanjutkan dengan proses login Google menggunakan akun baru
                        return lanjutkan_proses(driver, url)
                    else:
                        print(f"{R}Gagal mengklik elemen signup dengan akun baru")
                        simpan_url_gagal(url, "Gagal mengklik elemen signup dengan akun baru")
                else:
                    print(f"{R}Gagal mengklik elemen login dengan akun baru")
                    simpan_url_gagal(url, "Gagal mengklik elemen login dengan akun baru")
            else:
                print(f"{R}Gagal mengklik elemen root-comment-box-start dengan akun baru")
                simpan_url_gagal(url, "Gagal mengklik elemen root-comment-box-start dengan akun baru")
        else:
            print(f"{R}Elemen root-comment-box-start tidak ditemukan setelah scroll")
            simpan_url_gagal(url, "Elemen root-comment-box-start tidak ditemukan dengan akun baru setelah scroll")
            
    except Exception as e:
        print(f"{R}Error dalam lanjutkan_proses_dengan_akun_baru: {W}{e}")
        simpan_url_gagal(url, f"Error proses akun baru: {e}")

def simpan_url_gagal(url, error_message):
    """
    Menyimpan URL yang gagal ke file gagal-koment.txt
    """
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('gagal-koment.txt', 'a', encoding='utf-8') as file:
            file.write(f"[{timestamp}] {url} - Error: {error_message}\n")
            
        print(f"{R}URL gagal disimpan ke gagal-koment.txt: {W}{url}")
        
    except Exception as e:
        print(f"{R}Gagal menyimpan URL gagal: {W}{e}")

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
    print(f"{Y}Koneksi ke browser terputus. Mencoba menghubungkan kembali...")
    
    for attempt in range(max_attempts):
        try:
            print(f"{Y}Percobaan reconnect ke-{W}{attempt+1}/{max_attempts}...")
            
            # Coba tutup driver yang ada
            try:
                driver.quit()
            except:
                pass
            
            # Inisialisasi driver baru
            from main import inisialisasi_driver
            new_driver = inisialisasi_driver()
            
            if not new_driver:
                continue
            
            # Buka URL terakhir
            new_driver.get(url)
            print(f"{G}Berhasil menghubungkan kembali: {W}{url}")
            
            # Pastikan browser tetap aktif
            pastikan_browser_tetap_aktif(new_driver)
            
            return new_driver
            
        except Exception as e:
            print(f"{R}Gagal reconnect percobaan ke-{attempt+1}: {W}{e}")
            time.sleep(3)
    
    print(f"{R}Gagal reconnect setelah {W}{max_attempts} {R}percobaan")
    return None

def cari_elemen_root_comment_manual(driver, timeout=60, wait_time=0.5):
    """
    Fungsi alternatif untuk mencari elemen root-comment-box-start jika import main gagal
    """
    try:
        print(f"{Y}Mencari elemen root-comment-box-start secara manual...")
        
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
            
            print(f"{Y}Percobaan scroll ke-{W}{scroll_attempts + 1}...")
            
            # Posisi scroll awal
            posisi_scroll = 0
            langkah_scroll = 600
            posisi_scroll_terakhir = -1
            
            # Scroll sampai tidak bisa scroll lagi
            while True:
                # Periksa timeout
                if time.time() - start_time > timeout:
                    print(f"{R}Timeout tercapai ({W}{timeout} {R}detik).")
                    return None
                
                # Jaga fokus setiap 5 detik
                current_time = time.time()
                if current_time - last_focus_time > 5:
                    jaga_fokus_browser(driver)
                    last_focus_time = current_time
                
                # Scroll ke posisi baru
                driver.execute_script(f"window.scrollTo(0, {posisi_scroll});")
                time.sleep(wait_time)
                
                # Dapatkan posisi scroll aktual
                posisi_scroll_aktual = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
                
                # Ambil HTML dan parse dengan BeautifulSoup
                html_saat_ini = driver.page_source
                soup = BeautifulSoup(html_saat_ini, 'html.parser')
                
                # Cari elemen yang mengandung "root-comment-box-start" dalam ID
                elemen_bs4 = soup.find(lambda tag: tag.has_attr('id') and 'root-comment-box-start' in tag['id'])
                
                if elemen_bs4:
                    elemen_id = elemen_bs4['id']
                    print(f"{G}Elemen root-comment-box-start ditemukan: {W}{elemen_id}")
                    
                    jaga_fokus_browser(driver)
                    
                    try:
                        elemen_selenium = driver.find_element(By.ID, elemen_id)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemen_selenium)
                        time.sleep(1)
                        return elemen_id
                    except Exception as e:
                        print(f"{R}Elemen ditemukan dengan BeautifulSoup tetapi tidak dengan Selenium: {W}{e}")
                
                # Cek apakah sudah tidak bisa scroll lagi
                if posisi_scroll_aktual == posisi_scroll_terakhir:
                    print(f"\n{Y}Tidak bisa scroll lagi. Sudah mencapai batas bawah halaman.")
                    break
                
                posisi_scroll_terakhir = posisi_scroll_aktual
                posisi_scroll += langkah_scroll
            
            # Tunggu sebentar sebelum percobaan berikutnya
            if scroll_attempts < max_scroll_attempts - 1:
                print(f"{Y}Menunggu 10 detik sebelum percobaan berikutnya...")
                time.sleep(10)
                
                # Refresh halaman
                print(f"{Y}Me-refresh halaman...")
                driver.refresh()
                time.sleep(5)
                pastikan_browser_tetap_aktif(driver)
            
            scroll_attempts += 1
        
        print(f"\n{R}Elemen root-comment-box-start tidak ditemukan setelah {W}{max_scroll_attempts} {R}percobaan")
        return None
        
    except Exception as e:
        print(f"{R}Error dalam pencarian manual: {W}{e}")
        return None

def klik_elemen_dengan_id_manual(driver, elemen_id):
    """
    Fungsi alternatif untuk klik elemen jika import main gagal
    """
    try:
        jaga_fokus_browser(driver)
        elemen = driver.find_element(By.ID, elemen_id)
        elemen.click()
        print(f"{G}Elemen {W}{elemen_id} {G}berhasil diklik.")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"{R}Gagal mengklik elemen {elemen_id}: {W}{e}")
        try:
            jaga_fokus_browser(driver)
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, elemen_id))
            print(f"{G}Elemen {W}{elemen_id} {G}berhasil diklik dengan JavaScript.")
            time.sleep(2)
            return True
        except Exception as e2:
            print(f"{R}Gagal mengklik elemen {W}{elemen_id} dengan JavaScript: {R}{e2}")
            return False

def klik_elemen_login_manual(driver):
    """
    Fungsi alternatif untuk klik login jika import main gagal
    """
    try:
        jaga_fokus_browser(driver)
        
        elemen_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="login-as-member-text-button"]'))
        )
        
        jaga_fokus_browser(driver)
        
        try:
            elemen_login.click()
            print(f"{G}Elemen login berhasil diklik.")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"{R}Gagal mengklik elemen login: {W}{e}")
            try:
                jaga_fokus_browser(driver)
                driver.execute_script("arguments[0].click();", elemen_login)
                print(f"{G}Elemen login berhasil diklik dengan JavaScript.")
                time.sleep(2)
                return True
            except Exception as e2:
                print(f"{R}Gagal mengklik elemen login dengan JavaScript: {W}{e2}")
                return False
            
    except TimeoutException:
        print(f"{R}Elemen login tidak muncul dalam waktu yang ditentukan.")
        return False
    except Exception as e:
        print(f"{R}Terjadi kesalahan saat mencari elemen login: {W}{e}")
        return False

def klik_elemen_signup_manual(driver):
    """
    Fungsi alternatif untuk klik signup jika import main gagal
    """
    try:
        jaga_fokus_browser(driver)
        
        elemen_signup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="switchToSignUp"]'))
        )
        
        jaga_fokus_browser(driver)
        
        try:
            elemen_signup.click()
            print(f"{G}Elemen signup berhasil diklik.")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"{R}Gagal mengklik elemen signup: {W}{e}")
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
        print(f"{R}Terjadi kesalahan saat mencari elemen signup: {W}{e}")
        return False

def tangani_popup_manual(driver, max_attempts=3):
    """
    Fungsi alternatif untuk menangani popup jika import main gagal
    """
    try:
        print(f"{Y}Menangani pop-up awal...")
        
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
        
        while attempts < max_attempts:
            jaga_fokus_browser(driver)
            
            current_popup_found = False
            
            # Coba setiap selector
            for selector in popup_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            try:
                                jaga_fokus_browser(driver)
                                element.click()
                                current_popup_found = True
                                time.sleep(0.5)
                            except:
                                pass
                except:
                    continue
            
            # Jika tidak ada popup, coba tekan Escape
            if not current_popup_found:
                try:
                    jaga_fokus_browser(driver)
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.5)
                except:
                    pass
            
            if not current_popup_found:
                attempts += 1
            else:
                attempts = 0
        
        print(f"{G}Pop-up awal telah ditangani")
        return True
        
    except Exception as e:
        print(f"{Y}Peringatan saat menangani popup: {W}{e}")
        return True  # Tetap lanjutkan meskipun gagal menangani popup

def pembersihan_browser_sederhana(driver):
    """
    Fungsi pembersihan browser sederhana jika modul logout tidak tersedia
    """
    try:
        print(f"{Y}Melakukan pembersihan browser sederhana...")
        
        # 1. Hapus semua cookies
        try:
            driver.delete_all_cookies()
            print(f"{G}✓ Cookies dihapus")
        except Exception as e:
            print(f"{Y}Peringatan hapus cookies: {W}{e}")
        
        # 2. Clear localStorage dan sessionStorage
        try:
            driver.execute_script("""
            try {
                if (window.localStorage) window.localStorage.clear();
                if (window.sessionStorage) window.sessionStorage.clear();
                console.log('Storage cleared');
            } catch(e) {
                console.log('Storage clear error:', e);
            }
            """)
            print(f"{G}✓ Storage dibersihkan")
        except Exception as e:
            print(f"{Y}Peringatan clear storage: {W}{e}")
        
        # 3. Clear cache dan data lainnya
        try:
            driver.execute_script("""
            try {
                // Clear cache jika memungkinkan
                if ('caches' in window) {
                    caches.keys().then(names => {
                        names.forEach(name => {
                            caches.delete(name);
                        });
                    });
                }
                
                // Clear IndexedDB
                if (window.indexedDB) {
                    indexedDB.databases().then(databases => {
                        databases.forEach(db => {
                            indexedDB.deleteDatabase(db.name);
                        });
                    });
                }
                
                console.log('Advanced cleanup completed');
            } catch(e) {
                console.log('Advanced cleanup error:', e);
            }
            """)
            print(f"{G}✓ Cache dan IndexedDB dibersihkan")
        except Exception as e:
            print(f"{Y}Peringatan clear cache: {W}{e}")
        
        # 4. Tutup tab tambahan jika ada
        try:
            window_handles = driver.window_handles
            if len(window_handles) > 1:
                main_window = window_handles[0]
                for handle in window_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()
                driver.switch_to.window(main_window)
                print(f"{G}✓ Tab tambahan ditutup{W}")
        except Exception as e:
            print(f"{Y}Peringatan tutup tab: {W}{e}")
        
        # 5. Reset ke halaman kosong sebentar
        try:
            driver.get("about:blank")
            time.sleep(1)
            print(f"{G}✓ Browser direset ke halaman kosong")
        except Exception as e:
            print(f"{Y}Peringatan reset halaman: {W}{e}")
        
        print(f"{G}Pembersihan browser sederhana selesai")
        return True
        
    except Exception as e:
        print(f"{R}Error saat pembersihan sederhana: {W}{e}")
        return False

def logout_dari_google_sederhana(driver):
    """
    Logout dari Google sederhana jika modul logout tidak tersedia
    """
    try:
        print(f"{Y}Logout dari Google...")
        
        # Buka halaman logout Google
        driver.get("https://accounts.google.com/logout")
        time.sleep(3)
        
        print(f"{G}✓ Logout dari Google berhasil")
        
        # Buka halaman untuk menghapus semua akun yang tersimpan
        driver.get("https://accounts.google.com/signout")
        time.sleep(2)
        
        print(f"{G}✓ Signout dari semua akun Google")
        
        return True
        
    except Exception as e:
        print(f"{Y}Peringatan logout Google: {W}{e}")
        return False
