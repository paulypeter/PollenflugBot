# PollenflugBot

[Zum Bot](https://t.me/pollenflug_bot)

## Was macht der Bot?

Der Bot sendet jeden Tag um 7:00 ME(S)Z die DWD-Vorhersage zum Pollenflug.

### Befehle

| Befehl | Wirkung |
|---|---|
| /hilfe | Einen Link zu dieser Seite erhalten |
| /abonnieren | Abonniert den Bot |
| /abo_abbestellen | Beendet das Abonnement |
| /heute | Sendet die heutige Vorhersage |
| /morgen | Sendet die morgige Vorhersage |
| /pollenart_wechseln | Eine neue Pollenart für die Vorhersagen auswählen |
| /feedback_senden | Eine Nachricht an den Admin senden |
| /abbrechen | Die aktuelle Aktion abbrechen |

## Welche Daten werden gespeichert?

__Zusätzlich zu den durch Telegram gespeicherten Daten gilt Folgendes:__

Für länger als 24 h werden gespeichert:

- die Telegram-User-ID
- die gewählte Pollenart

Bis zum nächsten Morgen wird gespeichert, ob an die gespeicherte Telegram-ID die heutige und/oder morgige Vorhersage bereits versendet wurde.

Die Daten werden nicht an Dritte weitergegeben.

### Löschen der Daten

Jeden Morgen werden die Daten von Nicht-Abonnenten gelöscht.
