from pyzbar.pyzbar import decode
from PIL import Image
import argparse
import os
import sys
import base64
import subprocess

def decode_qr_to_tsac(qr_code_image_path, tsac_file_path):
    """
    Extrahiert Base64-kodierte Daten aus einem QR-Code, dekodiert sie und
    speichert das Ergebnis als TSAC-Datei.
    """
    try:
        image = Image.open(qr_code_image_path)
        codes = decode(image)

        if not codes:
            print("Kein QR-Code gefunden.")
            return False

        # Extrahiere die Base64-kodierten Daten aus dem QR-Code
        encoded_text = codes[0].data.decode('ascii')

        # Base64-Dekodierung
        binary_data = base64.b64decode(encoded_text)

        with open(tsac_file_path, 'wb') as f:
            f.write(binary_data)
        print(f"TSAC-Datei aus QR-Code (Base64-dekodiert) erstellt: {tsac_file_path}")
        return True

    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {qr_code_image_path}")
        return False
    except base64.binascii.Error:
        print("Fehler: Die Daten im QR-Code sind keine gültigen Base64-Daten.")
        return False
    except Exception as e:
        print(f"Fehler beim Dekodieren des QR-Codes: {type(e).__name__}: {e}")
        return False



def convert_tsac_to_wav(tsac_file_path, wav_file_path):
    """Konvertiert TSAC zu WAV (mit 'd' Parameter)."""
    try:
        command = [
            "./tsac",
            "--cuda",  # Behalte --cuda bei
            "d",      # WICHTIG: Füge den 'd' Parameter für die Dekodierung hinzu
            tsac_file_path,
            wav_file_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"WAV-Datei erstellt: {wav_file_path}")
        print(f"TSAC-Ausgabe (Dekodierung):\n{result.stdout}")
        return True

    except FileNotFoundError:
        print("Fehler: 'tsac' wurde nicht gefunden.  Stelle sicher, dass 'tsac' im selben Verzeichnis wie das Skript oder im PATH ist.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der TSAC->WAV-Konvertierung (Returncode {e.returncode}):")
        print(f"  Befehl: {e.cmd}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler bei der TSAC->WAV-Konvertierung: {type(e).__name__}: {e}")
        return False



def main():
    parser = argparse.ArgumentParser(
        description="Dekodiert einen Base64-kodierten QR-Code, der eine TSAC-Datei "
                    "enthält, und konvertiert diese in eine WAV-Datei."
    )
    parser.add_argument("png_file", help="Pfad zur PNG-Datei mit dem QR-Code.")
    parser.add_argument("-o", "--output", required=True, help="Pfad zur Ausgabe-WAV-Datei.")
    args = parser.parse_args()

    tsac_file_path = os.path.splitext(args.output)[0] + ".tsac"

    # 1. QR-Code (Base64) -> TSAC
    if not decode_qr_to_tsac(args.png_file, tsac_file_path):
        sys.exit(1)

    # 2. TSAC -> WAV
    if not convert_tsac_to_wav(tsac_file_path, args.output):
        sys.exit(1)


if __name__ == "__main__":
    main()