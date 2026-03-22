# Hetzner Cloud & Storage Integration für Home Assistant

Diese inoffizielle Custom Component für Home Assistant ermöglicht es dir, deine Hetzner Cloud Server und Storage Boxen direkt in deinem Smart Home Dashboard zu überwachen. 

Die Integration nutzt die offizielle Hetzner REST-API und wird vollständig über die Home Assistant Benutzeroberfläche (Config Flow) eingerichtet.

## Funktionen

Die Integration ruft die Daten lokal ab und erstellt folgende Sensoren für deine Infrastruktur:

**Für jeden Cloud Server:**
* Status (running, off, etc.)
* CPU Kerne
* CPU Auslastung (%)
* Traffic Eingehend & Ausgehend (in GiB)
* Disk IOPS (Read + Write)
* Disk Durchsatz (B/s)
* Netzwerk PPS (Pakete pro Sekunde)
* Netzwerk Bandbreite (B/s)

**Für jede Storage Box:**
* Speicherkapazität (Quota in GiB)
* Belegter Speicherplatz (Usage in GiB)

## Voraussetzungen

Du benötigst einen API-Token aus der Hetzner Cloud Console. Da Hetzner mittlerweile auch die Storage Boxen über diese moderne API anbietet, reicht ein einziger Token für beide Dienste.

1. Logge dich in die [Hetzner Cloud Console](https://console.hetzner.cloud/) ein.
2. Wähle dein Projekt aus.
3. Gehe im linken Menü auf **Security** (Sicherheit) und dann auf **API Tokens**.
4. Klicke auf **Generate API Token**.
5. Gib dem Token einen Namen (z.B. "Home Assistant") und wähle als Berechtigung zwingend **Read** (Lesen) aus.
6. Kopiere den 64-stelligen Token. Er wird nur dieses eine Mal angezeigt!

## Installation über HACS (Empfohlen)

Da diese Integration aktuell noch nicht im Standard-HACS-Store gelistet ist, kannst du sie in wenigen Sekunden als benutzerdefiniertes Repository hinzufügen:

1. Öffne **HACS** in deinem Home Assistant.
2. Klicke oben rechts auf das Drei-Punkte-Menü und wähle **Benutzerdefinierte Repositories**.
3. Füge die URL dieses Repositories ein: `https://github.com/DEIN_GITHUB_NAME/hetzner-homeassistant`
4. Wähle als Kategorie **Integration** und klicke auf Hinzufügen.
5. Suche in HACS nach "Hetzner Cloud & Storage" und klicke auf Herunterladen.
6. Starte Home Assistant neu.

## Manuelle Installation

1. Lade dir das neueste Release aus diesem Repository herunter.
2. Kopiere den gesamten Ordner `hetzner_custom` in das Verzeichnis `/config/custom_components/` deiner Home Assistant Installation.
3. Starte Home Assistant neu.

## Konfiguration

Nach dem Neustart kannst du die Integration ganz normal über die Benutzeroberfläche hinzufügen:

1. Gehe in Home Assistant zu **Einstellungen** -> **Geräte & Dienste**.
2. Klicke unten rechts auf **Integration hinzufügen**.
3. Suche nach **Hetzner** und wähle die Integration aus.
4. Füge deinen zuvor generierten Hetzner API-Token in das Feld ein und klicke auf Senden.

Die Server und Storage Boxen werden nun automatisch als Geräte erkannt und die Sensoren mit Live-Daten gefüllt. Die Daten werden standardmäßig alle 60 Sekunden aktualisiert.

## Fehlerbehebung

Sollten die Sensoren nicht aktualisiert werden oder Fehler im Log auftauchen:
* Prüfe, ob der API-Token versehentlich mit Leerzeichen am Anfang oder Ende kopiert wurde.
* Stelle sicher, dass der Token noch gültig ist und nicht in der Hetzner Console gelöscht wurde.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Es steht in keiner offiziellen Verbindung zur Hetzner Online GmbH.
