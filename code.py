# Arin Tri Rahmadani/06/14119/X TJKT 1

import datetime
import os
import platform
import re
import subprocess
import time

# --- Definisi Kode Warna ANSI ---
HIJAU = "\033[92m"
MERAH = "\033[91m"
KUNING = "\033[93m"
BIRU = "\033[94m"
TEBAL = "\033[1m"
RESET = "\033[0m"


def cek_ping_lengkap(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    try:
        # Menjalankan ping dan mengambil output
        output = subprocess.check_output(
            f"ping {param} 1 {host}", shell=True, text=True, stderr=subprocess.STDOUT
        )

        # Logika mencari angka latency (ms)
        match = re.search(r"(?:time|waktu)[=<](\d+)\s*ms", output, re.IGNORECASE)

        if match:
            latency = int(match.group(1))
            return "Aktif", latency
        return "Aktif", 0  # Aktif tapi latency tidak terbaca

    except subprocess.CalledProcessError:
        return "Tidak Aktif / Timeout", None


hosts = ["8.8.8.8", "google.com", "192.168.1.113"]
log = []
kumpulan_latency = []

print(f"{TEBAL}{BIRU}=== Sistem Monitoring & Statistik Jaringan Sederhana ==={RESET}\n")

for host in hosts:
    status, latency = cek_ping_lengkap(host)
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if status == "Aktif" and latency is not None:
        kumpulan_latency.append(latency)
        str_latency = f"{latency} ms"
        # Memberi warna hijau jika aktif
        warna_status = f"{HIJAU}{status}{RESET}"
    else:
        str_latency = "N/A"
        # Memberi warna merah jika mati
        warna_status = f"{MERAH}{status}{RESET}"

    log_entry = f"{waktu_sekarang} - {host}: {status} ({str_latency})"
    log.append(log_entry)

    print(
        f"[{waktu_sekarang}] {host} -> {warna_status} | Latency: {KUNING}{str_latency}{RESET}"
    )
    time.sleep(1)

# --- Logika Rata-rata, Max, dan Min ---
print(f"\n{TEBAL}{BIRU}=== Statistik Latency Jaringan ==={RESET}")
if kumpulan_latency:
    l_min = min(kumpulan_latency)
    l_max = max(kumpulan_latency)
    l_avg = sum(kumpulan_latency) / len(kumpulan_latency)

    info_statistik = (
        f"Minimum Latency : {KUNING}{l_min} ms{RESET}\n"
        f"Maksimum Latency: {KUNING}{l_max} ms{RESET}\n"
        f"Rata-rata (Avg) : {KUNING}{round(l_avg, 2)} ms{RESET}"
    )
    # Teks murni tanpa kode warna khusus untuk disimpan di file txt agar tidak merusak format teks log
    info_statistik_file = (
        f"Minimum Latency : {l_min} ms\n"
        f"Maksimum Latency: {l_max} ms\n"
        f"Rata-rata (Avg) : {round(l_avg, 2)} ms"
    )
else:
    info_statistik = f"{MERAH}Statistik tidak tersedia (Semua jaringan down).{RESET}"
    info_statistik_file = "Statistik tidak tersedia (Semua jaringan down)."

print(info_statistik)


# AI rule-based
def klasifikasi_jaringan_ai(status_log, latency_list):
    # Cek jika ada yang mati
    for entry in status_log:
        if "Tidak Aktif" in entry:
            return f"{TEBAL}{MERAH}⚠️ Jaringan Tidak Normal!{RESET}", "⚠️ Jaringan Tidak Normal!"

    if latency_list and (sum(latency_list) / len(latency_list)) > 100:
        return (
            f"{TEBAL}{KUNING}⚠️ Jaringan Normal dan Kurang Stabil!{RESET}",
            "⚠️ Jaringan Normal dan Kurang Stabil!",
        )

    return (
        f"{TEBAL}{HIJAU}✅ Jaringan Normal dan Stabil :]{RESET}",
        "✅ Jaringan Normal dan Stabil :]",
    )


kesimpulan_warna, kesimpulan_file = klasifikasi_jaringan_ai(log, kumpulan_latency)
print(f"\nKesimpulan AI: {kesimpulan_warna}")

# Simpan ke file arin.log_jaringan.txt
with open("arin.log_jaringan.txt", "a", encoding="utf-8") as f:
    f.write("\n" + "=" * 45 + "\n")
    f.write(
        f"Waktu Cek: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    f.write("\n".join(log) + "\n\n")
    f.write(info_statistik_file + "\n")
    f.write(f"Kesimpulan AI: {kesimpulan_file}\n")