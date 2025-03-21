# QliRpa - QR-Code-basierte Musikspeicherung

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

## Über QliRpa

QliRpa (ein Kofferwort aus "QR" und "april" rückwärts) ist eine Open-Source-Implementierung, die von dem Artikel "MusiqR" in der c't 2025, Heft 7, Seite 32 (von Hartmut Gieselmann) inspiriert wurde. Das Projekt ermöglicht es, Musikdateien (MP3) in QR-Codes zu kodieren und sie aus diesen wiederherzustellen. Es dient als Machbarkeitsstudie und erforscht die Grenzen und Möglichkeiten der Speicherung von Audiodaten in Bildformaten.

**Kernidee:** Eine MP3-Datei wird in ein komprimiertes Zwischenformat (TSAC) umgewandelt, Base64-kodiert und dann als QR-Code dargestellt. Der umgekehrte Prozess extrahiert die Base64-Daten aus dem QR-Code, dekodiert sie und wandelt sie zurück in eine WAV-Datei (und optional in eine MP3-Datei).

## Credits

*   **Hartmut Gieselmann:** Für die ursprüngliche Idee und den Artikel "MusiqR" in der c't.
*   **Fabrice Bellard:** Für die Entwicklung des TSAC-Audio-Codecs ([https://bellard.org/tsac/](https://bellard.org/tsac/)), der die Grundlage für die effiziente Audiokompression bildet.
*   **Google Gemini:** Für die Unterstützung bei der Erstellung der Python-Skripte für die Kodierung und Dekodierung.
*   **Entwickler der verwendeten Bibliotheken:** `qrcode`, `pyzbar`, `Pillow`, `base64`, und `subprocess`.

## Funktionsweise

Das Projekt besteht aus zwei Haupt-Python-Skripten:

1.  **`qr-gen.py`:**
    *   Konvertiert eine MP3-Datei in eine TSAC-Datei mithilfe des `tsac`-Programms (von Fabrice Bellard).
    *   Kodiert die Binärdaten der TSAC-Datei mit Base64, um sie QR-Code-kompatibel zu machen.
    *   Erzeugt einen QR-Code aus den Base64-kodierten Daten und speichert ihn als PNG-Bild.

2.  **`qr-dec.py`:**
    *   Liest einen QR-Code aus einer PNG-Datei.
    *   Dekodiert die Base64-kodierten Daten.
    *   Speichert die dekodierten Binärdaten als TSAC-Datei.
    *   Konvertiert die TSAC-Datei mithilfe des `tsac`-Programms in eine WAV-Datei.

## Installation und Verwendung

### Voraussetzungen

*   **Python 3.7+:** Stelle sicher, dass Python 3.7 oder höher installiert ist.
*   **`tsac`:** Lade das `tsac`-Programm von [https://bellard.org/tsac/](https://bellard.org/tsac/) herunter und lege es entweder in dasselbe Verzeichnis wie die Python-Skripte oder in ein Verzeichnis, das in deiner `PATH`-Umgebungsvariablen enthalten ist. Stelle sicher, dass es ausführbar ist (`chmod +x tsac` unter Linux/macOS).
*   **Python-Bibliotheken:** Installiere die benötigten Bibliotheken mit:
    ```bash
    pip install qrcode pyzbar Pillow
    ```

### Benutzung

1.  **MP3 in QR-Code umwandeln:**

    ```bash
    python qr-gen.py <mp3_datei> <qr_code_datei.png>
    ```
    Beispiel:
    ```bash
    python qr-gen.py meine_musik.mp3 mein_qr_code.png
    ```

2.  **QR-Code in WAV-Datei umwandeln:**

    ```bash
    python qr-dec.py <qr_code_datei.png> -o <ausgabe_datei.wav>
    ```
    Beispiel:
    ```bash
    python qr-dec.py mein_qr_code.png -o meine_musik.wav
    ```

    **Optional:** Du kannst die erzeugte WAV-Datei mit `ffmpeg` wieder zurück in eine MP3-Datei verwandeln.

## Limitierungen und wichtige Hinweise

*   **Datenmenge:** QR-Codes haben eine begrenzte Kapazität. Die tatsächliche Größe der speicherbaren Musik hängt von der Version des QR-Codes, dem Fehlerkorrekturlevel und der Effizienz der TSAC-Kompression ab. Längere Musikstücke oder höhere Audioqualitäten benötigen möglicherweise mehrere QR-Codes (dies ist in der aktuellen Version *nicht* implementiert).

*   **Binärdaten in QR-Codes:** Das direkte Speichern von Binärdaten in QR-Codes ist problematisch, da QR-Code-Reader oft versuchen, die Daten als Text in einem unbekannten Zeichensatz zu interpretieren. Dies führt zu Datenverfälschungen. QliRpa verwendet *Base64-Kodierung*, um dieses Problem zu umgehen. Base64 wandelt Binärdaten in eine reine Textdarstellung um, die von QR-Code-Readern problemlos verarbeitet werden kann. Der Nachteil ist ein erhöhter Platzbedarf (ca. 33%).

*   **Fehlerkorrektur:** QR-Codes verfügen über eine integrierte Fehlerkorrektur. Es wird empfohlen, mindestens den Fehlerkorrekturlevel "L" (Low) zu verwenden. Höhere Fehlerkorrekturlevel (M, Q, H) erhöhen die Robustheit gegenüber Beschädigungen des QR-Codes, reduzieren aber die verfügbare Datenkapazität.

*   **`tsac`:** Dieses Projekt verwendet den TSAC-Audiocodec von Fabrice Bellard. Es ist wichtig, die Lizenzbedingungen von TSAC zu beachten.

*   **Keine perfekte Rekonstruktion:** Die Kompressionsverfahren (sowohl MP3 als auch TSAC) sind verlustbehaftet. Die aus dem QR-Code zurückgewonnene WAV-Datei ist *nicht* bit-identisch zur originalen MP3-Datei.

## Lizenz

Der Python-Code in diesem Projekt ist unter der CC0 1.0 Universal (CC0 1.0) Public Domain Dedication lizenziert.  Du kannst den Code kopieren, modifizieren, verteilen und verwenden, auch für kommerzielle Zwecke, ohne um Erlaubnis zu fragen. Siehe die Datei [LICENSE](LICENSE) für Details. Beachte jedoch, dass `tsac` seine eigenen Lizenzbedingungen hat.
