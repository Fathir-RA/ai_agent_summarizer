import sys
import os
import PyPDF2
import re
import textwrap
from pathlib import Path
from colorama import Fore, Style, init
from collections import Counter

init()

# ==========================================
# BAGIAN 1: CUSTOM TOOLS (FUNGSI UTAMA)
# ==========================================

def find_pdf_smart(filename):
    """Mencari file di script folder, downloads, documents, desktop."""
    filename = filename.replace('"', '').replace("'", "").strip()
    
    if os.path.exists(filename):
        return filename

    # Lokasi pencarian otomatis
    home = Path.home()
    search_locations = [
        home / "Downloads",
        home / "Documents",
        home / "Desktop",
        home / "OneDrive" / "Documents",
    ]
    
    print(Fore.YELLOW + f"🔍 [System Tool] Mencari '{filename}' di folder laptop..." + Style.RESET_ALL)
    
    for folder in search_locations:
        if folder.exists():
            candidate_path = folder / filename
            if candidate_path.exists():
                print(Fore.GREEN + f"✅ [System Tool] File ditemukan: {candidate_path}" + Style.RESET_ALL)
                return str(candidate_path)
    return None

def extract_text_from_pdf(pdf_path):
    try:
        real_path = find_pdf_smart(pdf_path)
        if not real_path:
            return None, f"File tidak ditemukan. Cek nama file di Downloads/Documents."

        text = ""
        with open(real_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # Baca maksimal 20 halaman agar cepat
            limit = min(len(reader.pages), 20)
            
            for i in range(limit):
                page = reader.pages[i]
                raw = page.extract_text()
                if raw:
                    # FIX 1: Hapus hyphenation (kata terpotong di ujung baris PDF)
                    # Contoh: "peru- bahan" menjadi "perubahan"
                    raw = raw.replace('-\n', '') 
                    text += raw + " "
        
        if not text.strip():
            return None, "PDF kosong atau berisi gambar scan."
        return text, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def simple_summarizer(text, num_sentences=3):
    # FIX 2: Advanced Cleaning
    # Ubah semua enter/tab menjadi spasi biasa
    text = re.sub(r'\s+', ' ', text).strip()
    
    # FIX 3: Split Kalimat yang Lebih Pintar
    # Memisahkan kalimat berdasarkan titik yang diikuti spasi dan huruf besar
    # Ini mencegah "Jokowi dkk." dianggap akhir kalimat.
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Hitung Frekuensi Kata
    words = re.findall(r'\w+', text.lower())
    stopwords = {'dan', 'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'adalah', 'untuk', 'dengan', 'pada', 'atau', 'saya', 'anda', 'tersebut', 'dalam', 'bisa', 'akan', 'juga', 'oleh', 'tidak', 'telah', 'sebagai', 'maka', 'namun', 'bab', 'halaman'}
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    word_freq = Counter(filtered_words)
    
    sentence_scores = {}
    for sent in sentences:
        # Abaikan kalimat yang terlalu pendek (< 20 huruf) atau terlalu panjang (> 500 huruf)
        if len(sent) < 20 or len(sent) > 500:
            continue
            
        for word in re.findall(r'\w+', sent.lower()):
            if word in word_freq:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_freq[word]
                else:
                    sentence_scores[sent] += word_freq[word]
    
    # Ambil kalimat terbaik
    import heapq
    top_sentences = heapq.nlargest(num_sentences * 2, sentence_scores, key=sentence_scores.get)
    
    # FIX 4: Deduplikasi (Cegah kalimat mirip muncul 2x)
    final_sentences = []
    seen_content = set()
    
    for sent in top_sentences:
        # Ambil 15 karakter pertama sebagai "sidik jari" kalimat
        signature = sent[:15].lower()
        if signature not in seen_content:
            final_sentences.append(sent)
            seen_content.add(signature)
        
        if len(final_sentences) >= num_sentences:
            break
            
    return final_sentences

# ==========================================
# BAGIAN 2: INTERFACE TERMINAL
# ==========================================

def main():
    print(Fore.CYAN + "==============================================")
    print(" 🤖 AI PDF SUMMARIZER ")
    print(" ----------------------------------------------")
    print(" Ketik 'keluar' untuk berhenti.")
    print(" Perintah: 'ringkas [nama_file.pdf]'" + Style.RESET_ALL)
    print(Fore.CYAN + "==============================================" + Style.RESET_ALL)

    while True:
        try:
            user_input = input(Fore.GREEN + "\nUser ➤ " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            break

        if user_input.lower() in ['keluar', 'exit', 'quit']:
            print(Fore.CYAN + "AI: Sampai jumpa! 👋" + Style.RESET_ALL)
            break
        
        if not user_input:
            continue

        if user_input.lower().startswith("ringkas"):
            raw_filename = user_input[7:].strip()
            
            if not raw_filename:
                print(Fore.WHITE + "AI: Tolong sebutkan nama filenya." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"⚙️  [AI Thinking] Mencari & Membaca file '{raw_filename}'..." + Style.RESET_ALL)
                
                full_text, error = extract_text_from_pdf(raw_filename)
                
                if error:
                    print(Fore.RED + f"❌ [System Error] {error}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + f"🧠 [AI Thinking] Menganalisis inti sari dokumen..." + Style.RESET_ALL)
                    summary_list = simple_summarizer(full_text, num_sentences=3)
                    
                    print(Fore.CYAN + f"\nAI: Berikut ringkasan poin penting dokumen tersebut:" + Style.RESET_ALL)
                    print("-" * 60)
                    
                    for i, sentence in enumerate(summary_list, 1):
                        # FIX 5: Text Wrapping yang lebih rapi (lebar 75 karakter)
                        wrapped = textwrap.fill(sentence, width=75)
                        indented = textwrap.indent(wrapped, '   ') # Tambah spasi di kiri
                        # Hapus spasi di awal baris pertama agar sejajar dengan angka
                        indented = indented.lstrip() 
                        
                        print(Fore.WHITE + f" {i}. {indented}" + Style.RESET_ALL)
                        print("") # Jarak antar poin
                    
                    print("-" * 60)     
        else:
            print(Fore.WHITE + "AI: Perintah tidak dikenali. Gunakan 'ringkas namafile.pdf'." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
