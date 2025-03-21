import qrcode
import argparse
import subprocess
import os
import sys
import base64
import io

def create_qr_code(tsac_file_path, qr_code_image_path):
    """Erstellt einen QR-Code aus einer TSAC-Datei (Base64-kodiert)."""
    try:
        with open(tsac_file_path, 'rb') as f:
            binary_data = f.read()

        # Base64-Kodierung
        encoded_data = base64.b64encode(binary_data)
        encoded_text = encoded_data.decode('ascii')  # In ASCII-String umwandeln

        qr = qrcode.QRCode(
            version=None,  # Automatische Versionswahl
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Fehlerkorrektur L
            box_size=10,
            border=4,
        )
        qr.add_data(encoded_text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_image_path)
        print(f"QR-Code (Base64-kodiert) erstellt: {qr_code_image_path}")
        return True

    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {tsac_file_path}")
        return False
    except Exception as e:
        print(f"Fehler beim Erstellen des QR-Codes: {type(e).__name__}: {e}")
        return False

def convert_mp3_to_tsac(mp3_file_path, tsac_file_path):
    """Konvertiert MP3 zu TSAC (Qualität 1)."""
    try:
        # WICHTIG: Stelle sicher, dass tsac korrekt installiert und im Pfad ist!
        command = [
            "./tsac",  # Verwende eine Liste für subprocess.run
            "--cuda",
            "c",
            mp3_file_path,
            tsac_file_path,
            "-v",
            "-q", "4"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True) # check=True für Fehler
        print(f"TSAC erstellt: {tsac_file_path}")
        print(f"TSAC-Ausgabe:\n{result.stdout}")  # Gib die Ausgabe von tsac aus
        return True

    except FileNotFoundError:
        print("Fehler: 'tsac' wurde nicht gefunden. Stelle sicher, dass es im selben Verzeichnis wie das Skript liegt oder im PATH ist.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der TSAC-Konvertierung (Returncode {e.returncode}):")
        print(f"  Befehl: {e.cmd}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler bei der TSAC-Konvertierung: {type(e).__name__}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Erstellt einen Base64-kodierten QR-Code aus einer MP3-Datei, "
                    "unter Verwendung von tsac für die MP3->TSAC-Konvertierung."
    )
    parser.add_argument("mp3_file", help="Pfad zur MP3-Eingabedatei.")
    parser.add_argument("png_file", help="Pfad zur PNG-Ausgabedatei (QR-Code).")
    args = parser.parse_args()

    tsac_file_path = os.path.splitext(args.mp3_file)[0] + ".tsac"

    # 1. MP3 -> TSAC
    if not convert_mp3_to_tsac(args.mp3_file, tsac_file_path):
        sys.exit(1)

    # 2. TSAC -> QR-Code (Base64-kodiert)
    if not create_qr_code(tsac_file_path, args.png_file):
        sys.exit(1)

if __name__ == "__main__":
    main()