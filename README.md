# Hen Coop für Home Assistant

Die Integration verbindet Home Assistant mit dem [Pi-Dienst henCoop](https://github.com/NilsKrueger/henCoop). Der Pi steuert Motor und Endschalter eigenständig.

1. Pi-Dienst gemäß dessen README installieren und einen eigenen `HEN_API_TOKEN` setzen. HTTP nur im geschützten Netz verwenden.
2. Dieses Repository in HACS als benutzerdefiniertes Repository (Typ **Integration**) hinzufügen, Hen Coop herunterladen und Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** „HACS Hen Coop Controller“ auswählen. Vollständige API-URL (z. B. `http://raspberrypi.local:8000`) und Token eintragen.

Das Cover unterstützt Öffnen, Schließen und Stoppen. Vor einem Richtungswechsel zuerst stoppen. Die beiden Binärsensoren zeigen die tatsächlichen Endkontakte. Ohne eindeutige Endlage meldet die stehende Tür keine gesicherte Position.

Für eine Alarmierung kann eine Automation das Cover-Attribut `last_stop_reason` auswerten: `timeout` bedeutet Zeitlimit ohne erreichten Zielkontakt, `error` einen Steuerungsfehler. Der Wert beschreibt die letzte beendete Fahrt und bleibt bis zur nächsten beendeten Fahrt erhalten. Nach Dienststart und bei älterer Pi-API ist er zunächst unbekannt. Der Status wird alle zehn Sekunden abgefragt; er ist kein Ereignisprotokoll.
