---
layout: post
title: "Arbeitsspeicheruntersuchung"
date: 2019-01-08
excerpt: "Erste Schritte zur Untersuchung von Arbeitsspeicherabbilder."
tags: [Rekall, Linux, Arbeitsspeicher, Dumb, Memory Dumb]
comments: false
---

## Was ist *Memory Forensik*?

*"Memory Forensik" (Arbeitsspeicheruntersuchung)* beschreibt die __Sicherung__ des Arbeitsspeichers in Form eines Abbildes und das __Untersuchen__ des Abbildes auf ein mögliches Sicherheitsvorfalls.
Bei all den Vorteilen die eine Arbeitsspeicheruntersuchung gegenüber der traditionellen Untersuchung von persistentem Speicher bietet, ist es keine Überraschung, dass es heutzutage zu den ersten Schritten bei einem Sicherheitsvorfall zählt.
Einige wichtige Punkte die für die Arbeitsspeicheruntersuchung sprechen:

{% include Vorteile.html %}

## Warnung

Beim herunterladen so wie auch beim untersuchen einer infizierten Dumb, könnten sie ihr eigenes System infizieren.
Daher wird eine virtuelle Umgebung empfohlen und diese sollte nicht im Zusammenhang mit privaten Daten stehen.
Untersuchen sie infizierte Dumbs nie in einer sensiblen Netzwerkumgebung, wie z.B bei der Arbeit oder in der Schule.
Solche Untersuchungen müssen genehmigt werden und sollten unter einhaltung aller Sicherheitsmassnahmen durchgeführt werden.
Bitte respektieren sie die Privatsphäre so wie auch das Sicherheitsbedürfnis von anderen.

## Vorbereitungen

{% include Vorbereitungen.html %}

{% include Abbild.html %}

## Mit der Untersuchung beginnen

Nun da alle Vorbereitungen abgeschlossen wurden und auch schon ein Abbild zur Untersuchung bereit steht, können wir mit dieser Anfangen.
Da wir die ganze Zeit über aus dem gleichen Abbild lesen, ist es bequemer Rekall gleich interaktiv mit geladenem Abbild zu starten:
{% include Rekall_Open.html %}

### Prozessliste einsehen

Um überhaupt eine Vorstellung der Lage zu bekommen, beginnen wir mit der Einsicht in die Prozessliste.
Mit dem Befehl __pstree__ können alle Prozesse angezeigt werden, die zur Laufzeit, als das Abbild erstellt wurde, aktiv waren.
{% include Rekall_Pstree.html %}

| Priority apples | Second priority | Third priority |
|-------|--------|---------|
| ambrosia | gala | red delicious |
| pink lady | jazz | macintosh |
| honeycrisp | granny smith | fuji |

### Verdächtige Prozesse

#### WindowsXP Standardprozesse

### Rechtestufen

### Dll Anbindung

### Scannen von Prozessen

### Prozesse Extrahieren

### Funktionszugriffe einsehen

### Assembly-Code analysieren

### Fazit

### Scripte
