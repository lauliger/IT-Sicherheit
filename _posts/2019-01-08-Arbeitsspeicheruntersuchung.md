---
layout: post
title: "Arbeitsspeicheruntersuchung"
date: 2019-01-08
excerpt: "Erste Schritte zur Untersuchung von Arbeitsspeicherabbilder."
tags: [Rekall, Linux, Arbeitsspeicher, Dumb, Memory Dumb]
comments: false
---

<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>

## Was ist *Memory Forensik*?

*"Memory Forensik" (Arbeitsspeicheruntersuchung)* beschreibt die __Sicherung__ des Arbeitsspeichers in Form eines Abbildes 
und das __Untersuchen__ des Abbildes auf einen möglichen Sicherheitsvorfall.
Bei all den Vorteilen, die eine Arbeitsspeicheruntersuchung gegenüber der traditionellen Untersuchung von persistentem Speicher bietet, 
ist es keine Überraschung, dass es heutzutage zu den ersten Schritten bei einem Sicherheitsvorfall zählt.
Einige wichtige Punkte, die für die Arbeitsspeicheruntersuchung sprechen:

<summary>Kleiner Angriffsvektor</summary>
<p><i>Heutzutage bewegen sich selbst einfache Benutzer in Speichergrössen von über 1 Terabyte. Diese Speichermenge erhöht auch den Aufwand eines Forensikers, der persistente Speicher untersuchen muss. Beim Arbeitsspeicher hingegen, hält sich die zu untersuchende Menge stark in Grenzen.</i></p>

<summary>Laufende Aktivitäten</summary>
  <p><i>Zusätzlich beinhaltet der flüchtige Speicher Informationen über aktive Prozesse und Netzwerkverbindungen.</i></p>

<summary>Anti-Forensik umgehen</summary>
  <p><i>Weiter könnten Passwörter, die zur Entschlüsselung eines persistenten Speichers benötigt werden, aus dem Arbeitsspeicher extrahiert und so Zugang zu mehr Beweisen erlangt werden.</i></p>

<summary>Temporärer Code</summary>
  <p><i>Schadcode der nur im Arbeitsspeicher geschrieben wird, kann so entdeckt und untersucht werden.</i></p>
<p></p>

## Warnung

Beim Herunterladen so wie auch beim Untersuchen des infizierten Abbildes, könnte sich das eigene System infizieren.
Daher wird eine virtuelle Umgebung empfohlen und diese sollte nicht im Zusammenhang mit privaten Daten stehen.
Untersuche infizierte Abbilder nie in einer sensiblen Netzwerkumgebung, wie z.B bei der Arbeit oder in der Schule.
Solche Untersuchungen müssen genehmigt werden und sollten unter Einhaltung aller Sicherheitsmassnahmen durchgeführt werden.
Bitte __respektiere__ die __Privatsphäre__ sowie auch das __Sicherheitsbedürfnis__ von Anderen.

## Vorbereitungen


__Virtuelle Umgebung & Rekall installieren__
<ol>
  <li><summary><code>pacman -S python-virtualenv</code></summary>
</li>
<li><summary><code>virtualenv -p python2 /tmp/MyEnv</code></summary>
<p>Ausgabe bei Erfolg:</p>
<textarea style="resize:none" rows="4" cols="55" readonly>Running virtualenv with interpreter /usr/bin/python2
New python executable in /tmp/MyEnv/bin/python2
Also creating executable in /tmp/MyEnv/bin/python
    Installing setuptools, pip, wheel...done.</textarea></li>
    <li><code>source /tmp/MyEnv<b>/bin/activate</b></code></li>
    <li><summary><code>pip install rekall</code></summary>
        <p>Es könnten Probleme beim Version von Wheel, pip oder Setuptools vorkommen.</p>
        <p><code>pip install --upgrade pip wheel setuptools</code></p>
        <p>Sollte ein Fehler wegen der efilter Version aufkommen:</p>
        <textarea rows="2" cols="55" style="color: red; resize:none">rekall-efilter 1.6.0 has requirement future==0.16.0, but you'll have future 0.17.1 which is incompatible.</textarea>
        <p><code>pip install --upgrade rekall-efilter</code></p></li>
</ol>
<p></p>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">


<script>
function cpMdHash() {
  var copyText = document.getElementById('md5Txt').select();
  document.execCommand("copy");
}
</script>
<script>
function cpCmd(){
var cmdText = document.getElementById('cmdTxt').select();
document.execCommand('copy');
}
</script>


__Abbild mit Stuxnet__

<a href="http://www.jonrajewski.com/data/Malware/stuxnet.vmem.zip">   Abbild als Zip herunterladen</a>

Das Abbild stellt einen infizierten WindowsXP Rechner dar.
Bitte überprüfe, ob es sich beim heruntergeladenen File wirklich um das angegebene Abbild handelt!

MD5Hash:
<textarea id="md5Txt" readonly rows="2" cols="35">8f630be089e791cc23571ce51c73df0c</textarea>
<button class="btn" onclick="cpMdHash()"><i class="fa fa-clipboard"></i></button>

Befehl:
<textarea id="cmdTxt" readonly rows="2" cols="65">echo "8f630be089e791cc23571ce51c73df0c" stuxnet.vmem.zip | md5sum -c -</textarea>
<button class="btn" onclick="cpCmd()"><i class="fa fa-clipboard"></i></button>


## Mit der Untersuchung beginnen

Ab diesem Punkt können wir mit der eigentlichen Arbeit beginnen.
Die Arbeit mit rekall (oder Volatility) beim Untersuchen von Arbeitsspeicherabbildern, erinnert schon fast an eine Detektivarbeit.
So gesehen, haben wir einen Tatort *(das Abbild)*, unsere Werkzeuge *(rekall)* und brauchen jetzt Verdächtige.
Fangen wir mit der Arbeit an, indem wir rekall im interaktiven Modus starten und dazu das Abbild laden.

{% highlight bash %}
rekall --filename /home/user/Downloads/stuxnet.vmem
{% endhighlight %}

### Prozessliste einsehen

Um überhaupt eine Vorstellung der Lage zu bekommen, beginnen wir mit der Einsicht in die Prozessliste.
Mit dem Befehl __pstree__ können alle Prozesse angezeigt werden, die zur Laufzeit, als das Abbild erstellt wurde, aktiv waren.

{% highlight bash %}
stuxnet.vmem 22:30:00> pstree
{% endhighlight %}

| _EPROCESS | ppid | thd_count | hnd_count | create_time |
|-------|--------|---------|---------|---------|
|0x823c8830 System (4)|0|59|403|-|
|. 0x820df020 smss.exe (376)|4|3|19|2010-10-29 17:08:53Z|
|.. 0x821a2da0 csrss.exe (600)|376|11|395|2010-10-29 17:08:54Z|
|.. 0x81da5650 winlogon.exe (624)|376|19|570|2010-10-29 17:08:54Z|
|... 0x82073020 services.exe (668)|624|21|431|2010-10-29 17:08:54Z|
|.... 0x8205ada0 alg.exe (188)|668|6|107|2010-10-29 17:09:09Z|
|.... 0x82279998 imapi.exe (756)|668|4|116|2010-10-29 17:11:54Z|
|.... 0x823315d8 vmacthlp.exe (844)|668|1|25|2010-10-29 17:08:55Z|
|.... 0x81db8da0 svchost.exe (856)|668|17|193|2010-10-29 17:08:55Z|
|..... 0x81fa5390 wmiprvse.exe (1872)|856|5|134|2011-06-03 04:25:58Z|
|.... 0x81c498c8 lsass.exe (868)|668|2|23|2011-06-03 04:26:55Z|
|.... 0x81e61da0 svchost.exe (940)|668|13|312|2010-10-29 17:08:55Z|
|.... 0x822843e8 svchost.exe (1032)|668|61|1169|2010-10-29 17:08:55Z|
|..... 0x822b9a10 wuauclt.exe (976)|1032|3|133|2010-10-29 17:12:03Z|
|..... 0x820ecc10 wscntfy.exe (2040)|1032|1|28|2010-10-29 17:11:49Z|
|.... 0x81e18b28 svchost.exe (1080)|668|5|80|2010-10-29 17:08:55Z|
|.... 0x81ff7020 svchost.exe (1200)|668|14|197|2010-10-29 17:08:55Z|
|.... 0x81fee8b0 spoolsv.exe (1412)|668|10|118|2010-10-29 17:08:56Z|
|.... 0x81e0eda0 jqs.exe (1580)|668|5|148|2010-10-29 17:09:05Z|
|.... 0x81fe52d0 vmtoolsd.exe (1664)|668|5|284|2010-10-29 17:09:05Z|
|..... 0x81c0cda0 cmd.exe (968)|1664|0|-|2011-06-03 04:31:35Z|
|...... 0x81f14938 ipconfig.exe (304)|968|0|-|2011-06-03 04:31:35Z|
|.... 0x821a0568 VMUpgradeHelper (1816)|668|3|96|2010-10-29 17:09:08Z|
|.... 0x81c47c00 lsass.exe (1928)|668|4|65|2011-06-03 04:26:55Z|
|... 0x81e70020 lsass.exe (680)|624|19|342|2010-10-29 17:08:54Z|
|  0x820ec7e8 explorer.exe (1196)|1728|16|582|2010-10-29 17:11:49Z|
|. 0x81e86978 TSVNCache.exe (324)|1196|7|54|2010-10-29 17:11:49Z|
|. 0x81c543a0 Procmon.exe (660)|1196|13|189|2011-06-03 04:25:56Z|
|. 0x81e6b660 VMwareUser.exe (1356)|1196|9|251|2010-10-29 17:11:50Z|
|. 0x8210d478 jusched.exe (1712)|1196|1|26|2010-10-29 17:11:50Z|
|. 0x81fc5da0 VMwareTray.exe (1912)|1196|1|50|2010-10-29 17:11:50Z|

### Verdächtige Prozesse

Um aus der pstree-Ausgabe vernünftig Indizien zu sammeln, benötigt man Erfahrung und Wissen über die Betriebssysteme die man untersucht.
Was hier schon für viele erfahrene XP-Nutzer ins Auge sticht: "lsass.exe" kommt 3x vor, obwohl dieser Prozess eigentlich nur einmal vorkommen sollte.
Dieser Beobachtung zu Grunde liegend, nehmen wir die Prozesse 680, 868 und 1928 genauer unter die Lupe.
Zurzeit sind alle 3 Prozesse gleichermassen verdächtigt.
Wobei bei Prozess 680 das Erstelldatum für dessen Validität spricht, da das Datum den, der anderen SYSTEM-Prozessen gleicht.

#### WindowsXP Standardprozesse

Hier könnte es hilfreich sein das Gedächtnis aufzufrischen, oder für welche, die nie grossartig an einem XP Rechner gesessen haben, sich eine Liste von den Standardprozessen zur Seite zu legen.
Von der Uni-Regensburg, ist online eine dokumentierte Liste über die Standardprozesse von WinXP zu finden.
{% include winxplist.html %}

### Optionen evaluieren

Unter diesen 3 "lsass.exe" Prozessen, müsste einer valid und somit sauber sein, während 2 womöglich Schadcode beinhalten.
Doch wie wollen wir das nun herausfinden? Um den 2 gefälschten Prozessen auf die Spur zu kommen, haben wir ein breites Spektrum an Ansätzen und Möglichkeiten.
Auch hier, um einen Anhaltspunkt für das weitere Vorgehen zu finden, brauchen wir mehr Informationen.
Eine einfache __Google-Suche__ mit den Worten "lsass.exe windows xp" könnte uns interessante Informationen aufzeigen.
{% include prozessinformationen.html %}

Daraus können wir folgende Fakten ziehen:
* lsass.exe liegt im Ordner "C:\Windows\System32"
* lsass.exe steht auf SYSTEM Level und hat somit sehr hohe Rechte/Priorität
* lsass.exe ist ein lokaler Sicherheit-Authentifizierungsserver.
  Funktionen, die bei einem Trojaner typisch sind (Kontrolle von Fenstern oder das Bewegen der Maus oder Tastaturschläge) gehören nicht zu seiner Funktionsliste

### Rechtestufen

Da der valide Prozess "lsass.exe" SYSTEM-Rechte besitzt, müsste der valide Prozess grösser-gleich __(>=)__ Rechte zu den 2 Prozessen haben, die nicht zu den Standardprozessen von WindowsXP gehören.
Wenn wir Glück haben, sollte bei dieser Untersuchung ein Prozess höhere Rechte haben als die beiden anderen.
So wissen wir welcher der valide Prozess ist.
Mittels Rekall lassen sich die Rechte der einzelnen Prozesse aufzeigen:

{% highlight bash %}
stuxnet.vmem 22:42:00> tokens proc_regex=('lsass.exe')
{% endhighlight %}

|Process|Sid|Comment|
|-------|---|-------|
|0x81e70020 lsass.exe|680 S-1-5-18|Local System|
|0x81e70020 lsass.exe|680 S-1-5-32-544|Administrators|
|0x81e70020 lsass.exe|680 S-1-1-0|Everyone|
|0x81e70020 lsass.exe|680 S-1-5-11|Authenticated Users|
|0x81c498c8 lsass.exe|868 S-1-5-18|Local System|
|0x81c498c8 lsass.exe|868 S-1-5-32-544|Administrators|
|0x81c498c8 lsass.exe|868 S-1-1-0|Everyone|
|0x81c498c8 lsass.exe|868 S-1-5-11|Authenticated Users|
|0x81c47c00 lsass.exe|1928 S-1-5-18|Local System|
|0x81c47c00 lsass.exe|1928 S-1-5-32-544|Administrators|
|0x81c47c00 lsass.exe|1928 S-1-1-0|Everyone|
|0x81c47c00 lsass.exe|1928 S-1-5-11|Authenticated Users|

An dieser Ausgabe ist zu erkennen, dass alle 3 Verdächtigen die gleiche Berechtigung besitzen.
Somit konnte kein valider Prozess herauskristallisiert werden.
Es gibt noch die Möglichkeit, die Priorität zu überprüfen.
Denn der legitime Prozess sollte dank seinem SYSTEM-Level auch entsprechend höhere Priorität besitzen.
Tatsächlich besitzen bei Windows "normale" Anwendungen max. ein Prioritätlevel von 8, 
wohingegen SYSTEM-Anwendungen ein Level von 9 besitzen.

{% highlight bash %}
stuxnet.vmem 22:48:00> SELECT _EPROCESS.name, _EPROCESS.pid, _EPROCESS.Pcb.BasePriority FROM pslist() WHERE regex_proc("lsass.exe", _EPROCESS.name)
{% endhighlight %}

Wie bei einer SQL Abfrage wird mit __SELECT__ bestimmt, welche Spalten angefragt werden. In unserem Fall __name__, __die ID__ und das __Prioritätlevel__. Mit __FROM__ wird die Informationsquelle bestimmt, in diesem Fall die Werte von pslist().
pslist() ist ähnlich dem pstree().
Weiter wird die Ausgabe von pslist() durch __WHERE__ gefiltert, nur Daten die als name "lsass.exe" tragen werden berücksichtigt.

|pid|name|BasePriority|
|---|----|------------|
|680|lsass.exe|9|
|868|lsass.exe|8|
|1928|lsass.exe|8|

Durch diese Ausgabe sehen wir, dass die Priorität von Prozess 680 höher liegt, als die der anderen beiden Prozesse.
Wir können bereits jetzt davon ausgehen, dass es sich beim Prozess 680 um das valide lsass.exe handelt.
Dafür sprechen 2 Punkte:
* Das Erstelldatum, das ein Jahr vor den anderen 2 Prozessen liegt und mit anderen legitimen SYSTEM-Prozessen gleich liegt.
* Die höhere Priorität, die durch das SYSTEM-Level begründet wird.

Es liegt nun auf der Hand, welcher der 3 Prozesse valid ist und welche 2 verdächtigt werden, Schadcode zu beinhalten.
Wir untersuchen dennoch weiter die Prozesse. Evtl. können wir so den Handlungsradius bestimmen.
Wichtig für die Handlungsmöglichkeiten eines Prozesses, sind die Funktionen, die er verwendet/besitzt.
Viele Funktionen finden sich in DLL-Dateien. Das sind ganze Bibliotheken von Funktionen.
Auch die Framework-Funktionen, die windowseigene Algorithmen beinhalten, stellen diese über DLLs bereit.
Daher ist es für einen Forensiker interessant zu wissen, auf welche DLLs ein Prozess zugreift, dadurch lässt sich der Handlungsspielraum eingrenzen.

### Dll Anbindung

{% highlight bash %}
stuxnet.vmem 23:55:00> dlllist[680,868,1928]
{% endhighlight %}


lsass.exe pid: 680
Command line : C:\WINDOWS\system32\lsass.exe
Service Pack 3

|base|size|reason|dll_path|
|----|----|------|--------|
|0x1000000|0x6000|65535|C:\WINDOWS\system32\lsass.exe|
|0x7c900000|0xaf000|65535|C:\WINDOWS\system32\ntdll.dll|
|0x7c800000|0xf6000|65535|C:\WINDOWS\system32\kernel32.dll|

+54 weitere...


lsass.exe pid: 868
Command line : "C:\WINDOWS\\system32\\lsass.exe"
Service Pack 3

|base|size|reason|dll_path|
|----|----|------|--------|
|0x1000000|0x6000|65535|C:\WINDOWS\system32\lsass.exe|
|0x7c900000|0xaf000|65535|C:\WINDOWS\system32\ntdll.dll|
|0x7c800000|0xf6000|65535|C:\WINDOWS\system32\kernel32.dll|
|0x77dd0000|0x9b000|65535|C:\WINDOWS\system32\ADVAPI32.dll|
|0x77e70000|0x92000|65535|C:\WINDOWS\system32\RPCRT4.dll|
|0x77fe0000|0x11000|65535|C:\WINDOWS\system32\Secur32.dll|
|0x7e410000|0x91000|65535|C:\WINDOWS\system32\USER32.dll|
|0x77f10000|0x49000|65535|C:\WINDOWS\system32\GDI32.dll|


lsass.exe pid: 1928
Command line : "C:\WINDOWS\\system32\\lsass.exe"
Service Pack 3

|base|size|reason|dll_path|
|----|----|------|--------|
|0x1000000|0x6000|65535|C:\WINDOWS\system32\lsass.exe|
|0x7c900000|0xaf000|65535|C:\WINDOWS\system32\ntdll.dll|
|0x7c800000|0xf6000|65535|C:\WINDOWS\system32\kernel32.dll|
|0x77dd0000|0x9b000|65535|C:\WINDOWS\system32\ADVAPI32.dll|
|0x77e70000|0x92000|65535|C:\WINDOWS\system32\RPCRT4.dll|
|0x77fe0000|0x11000|65535|C:\WINDOWS\system32\Secur32.dll|
|0x7e410000|0x91000|65535|C:\WINDOWS\system32\USER32.dll|

+21 weitere...

Der legitime Prozess hat viel mehr DLLs eingebunden als die 2 illegitimen Prozesse.
Das überrascht nicht, da ein Programmierer von Schadcode, zwar evtl. Funktionen von der Framework benötigt, aber nicht alle.
Wozu den Schadcode unnötig aufblähen?
Natürlich ist das nur eine Interpretation und kann höchstens als Indiz und nicht als Beweis gewertet werden.
Was wir wissen müssen, DLL-Anbindungen können absichtlich verschleiert werden.
Ein Weg dies zu tun, ist das unlinken von DLLs aus der PEB. {% include PEB.html %}

Mit "ldrmodules" untersuchen wir die ldr Einträge. Dabei handelt es sich um einen Zeiger, der auf eine <a href="https://docs.microsoft.com/en-us/windows/desktop/api/winternl/ns-winternl-_peb_ldr_data">Struktur</a> zeigt, in dem Informationen über geladene DLLs zu finden sind.
Dort wird in der Antiforensik angesetzt, um DLLs vor einer Untersuchung zu verstecken.

{% highlight bash %}
stuxnet.vmem 22:59:00> ldrmodules[680,868,1928]
{% endhighlight %}


__0x81e70020 lsass.exe   680__

|base|in_load|in_init|in_mem|mapped|
|----|-------|-------|------|------|
|0x1000000|*True*|__False__|*True*|\WINDOWS\system32\lsass.exe|
|0x7c900000|*True*|*True*|*True*|\WINDOWS\system32\ntdll.dll|
|0x77be0000|*True*|*True*|*True*|\WINDOWS\system32\msacm32.dll|
|0x76b40000|*True*|*True*|*True*|\WINDOWS\system32\winmm.dll|
|0x4d200000|*True*|*True*|*True*|\WINDOWS\system32\msprivs.dll|
|0x76f60000|*True*|*True*|*True*|\WINDOWS\system32\wldap32.dll|
|0x77c00000|*True*|*True*|*True*|\WINDOWS\system32\version.dll|
|0x5ad70000|*True*|*True*|*True*|\WINDOWS\system32\uxtheme.dll|
|0x74380000|*True*|*True*|*True*|\WINDOWS\system32\wdigest.dll|
|0x774e0000|*True*|*True*|*True*|\WINDOWS\system32\ole32.dll|
|0x75d90000|*True*|*True*|*True*|\WINDOWS\system32\oakley.dll|
|0x743a0000|*True*|*True*|*True*|\WINDOWS\system32\pstorsvc.dll|
|0x743c0000|*True*|*True*|*True*|\WINDOWS\system32\psbase.dll|
|0x77dd0000|*True*|*True*|*True*|\WINDOWS\system32\advapi32.dll|
|0x77a80000|*True*|*True*|*True*|\WINDOWS\system32\crypt32.dll|
|0x743e0000|*True*|*True*|*True*|\WINDOWS\system32\ipsecsvc.dll|
|0x68000000|*True*|*True*|*True*|\WINDOWS\system32\rsaenh.dll|
|0x74440000|*True*|*True*|*True*|\WINDOWS\system32\samsrv.dll|
|0x71a50000|*True*|*True*|*True*|\WINDOWS\system32\mswsock.dll|
|0x5b860000|*True*|*True*|*True*|\WINDOWS\system32\netapi32.dll|
|0x767f0000|*True*|*True*|*True*|\WINDOWS\system32\schannel.dll|
|0x6f880000|*True*|*True*|*True*|\WINDOWS\AppPatch\AcGenral.dll|
|0x71a90000|*True*|*True*|*True*|\WINDOWS\system32\wshtcpip.dll|
|0x71ab0000|*True*|*True*|*True*|\WINDOWS\system32\ws2_32.dll|
|0x74370000|*True*|*True*|*True*|\WINDOWS\system32\winipsec.dll|
|0x767a0000|*True*|*True*|*True*|\WINDOWS\system32\ntdsapi.dll|
|0x77920000|*True*|*True*|*True*|\WINDOWS\system32\setupapi.dll|
|0x7e410000|*True*|*True*|*True*|\WINDOWS\system32\user32.dll|
|0x68100000|*True*|*True*|*True*|\WINDOWS\system32\dssenh.dll|
|0x76080000|*True*|*True*|*True*|\WINDOWS\system32\msvcp60.dll|
|0x77f10000|*True*|*True*|*True*|\WINDOWS\system32\gdi32.dll|
|0x77120000|*True*|*True*|*True*|\WINDOWS\system32\oleaut32.dll|
|0x71b20000|*True*|*True*|*True*|\WINDOWS\system32\mpr.dll|
|0x76d60000|*True*|*True*|*True*|\WINDOWS\system32\iphlpapi.dll|
|0x5cb70000|*True*|*True*|*True*|\WINDOWS\system32\shimeng.dll|
|0x767c0000|*True*|*True*|*True*|\WINDOWS\system32\w32time.dll|
|0x76790000|*True*|*True*|*True*|\WINDOWS\system32\cryptdll.dll|
|0x77e70000|*True*|*True*|*True*|\WINDOWS\system32\rpcrt4.dll|
|0x77c10000|*True*|*True*|*True*|\WINDOWS\system32\msvcrt.dll|
|0x769c0000|*True*|*True*|*True*|\WINDOWS\system32\userenv.dll|
|0x7c800000|*True*|*True*|*True*|\WINDOWS\system32\kernel32.dll|
|0x773d0000|*True*|*True*|*True*|\WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll|
|0x71bf0000|*True*|*True*|*True*|\WINDOWS\system32\samlib.dll|
|0x662b0000|*True*|*True*|*True*|\WINDOWS\system32\hnetcfg.dll|
|0x74410000|*True*|*True*|*True*|\WINDOWS\system32\scecli.dll|
|0x75730000|*True*|*True*|*True*|\WINDOWS\system32\lsasrv.dll|
|0x7c9c0000|*True*|*True*|*True*|\WINDOWS\system32\shell32.dll|
|0x77c70000|*True*|*True*|*True*|\WINDOWS\system32\msv1_0.dll|
|0x76f20000|*True*|*True*|*True*|\WINDOWS\system32\dnsapi.dll|
|0x5d090000|*True*|*True*|*True*|\WINDOWS\system32\comctl32.dll|
|0x77f60000|*True*|*True*|*True*|\WINDOWS\system32\shlwapi.dll|
|0x71aa0000|*True*|*True*|*True*|\WINDOWS\system32\ws2help.dll|
|0x744b0000|*True*|*True*|*True*|\WINDOWS\system32\netlogon.dll|
|0x776c0000|*True*|*True*|*True*|\WINDOWS\system32\authz.dll|
|0x77fe0000|*True*|*True*|*True*|\WINDOWS\system32\secur32.dll|
|0x71cf0000|*True*|*True*|*True*|\WINDOWS\system32\kerberos.dll|
|0x77b20000|*True*|*True*|*True*|\WINDOWS\system32\msasn1.dll|


__0x81c498c8 lsass.exe   868__

|base|in_load|in_init|in_mem|mapped|
|----|-------|-------|------|------|
|0x80000|__False__|__False__|__False__|
|0x7c900000|*True*|*True*|*True*|\WINDOWS\system32\ntdll.dll|
|0x77e70000|*True*|*True*|*True*|\WINDOWS\system32\rpcrt4.dll|
|0x7c800000|*True*|*True*|*True*|\WINDOWS\system32\kernel32.dll|
|0x77fe0000|*True*|*True*|*True*|\WINDOWS\system32\secur32.dll|
|0x7e410000|*True*|*True*|*True*|\WINDOWS\system32\user32.dll|
|0x1000000|*True*|__False__|*True*|__???__|
|0x77f10000|*True*|*True*|*True*|\WINDOWS\system32\gdi32.dll|
|0x77dd0000|*True*|*True*|*True*|\WINDOWS\system32\advapi32.dll|


__0x81c47c00 lsass.exe  1928__

|base|in_load|in_init|in_mem|mapped|
|----|-------|-------|------|------|                                   
|0x80000|__False__|__False__|__False__|__???__|
|0x76bf0000|*True*|*True*|*True*|\WINDOWS\system32\psapi.dll|
|0x7c900000|*True*|*True*|*True*|\WINDOWS\system32\ntdll.dll|
|0x77f60000|*True*|*True*|*True*|\WINDOWS\system32\shlwapi.dll|
|0x77c00000|*True*|*True*|*True*|\WINDOWS\system32\version.dll|
|0x771b0000|*True*|*True*|*True*|\WINDOWS\system32\wininet.dll|
|0x77dd0000|*True*|*True*|*True*|\WINDOWS\system32\advapi32.dll|
|0x77a80000|*True*|*True*|*True*|\WINDOWS\system32\crypt32.dll|
|0x77fe0000|*True*|*True*|*True*|\WINDOWS\system32\secur32.dll|
|0x7c800000|*True*|*True*|*True*|\WINDOWS\system32\kernel32.dll|
|0x1000000|*True*|__False__|*True*|__???__|
|0x5b860000|*True*|*True*|*True*|\WINDOWS\system32\netapi32.dll|
|0x680000|__False__|__False__|__False__|__???__|
|0x77e70000|*True*|*True*|*True*|\WINDOWS\system32\rpcrt4.dll|
|0x71ab0000|*True*|*True*|*True*|\WINDOWS\system32\ws2_32.dll|
|0x71ad0000|*True*|*True*|*True*|\WINDOWS\system32\wsock32.dll|
|0x774e0000|*True*|*True*|*True*|\WINDOWS\system32\ole32.dll|
|0x6f0000|__False__|__False__|__False__|__???__|
|0x7e410000|*True*|*True*|*True*|\WINDOWS\system32\user32.dll|
|0x77f10000|*True*|*True*|*True*|\WINDOWS\system32\gdi32.dll|
|0x77120000|*True*|*True*|*True*|\WINDOWS\system32\oleaut32.dll|
|0x76d60000|*True*|*True*|*True*|\WINDOWS\system32\iphlpapi.dll|
|0x769c0000|*True*|*True*|*True*|\WINDOWS\system32\userenv.dll|
|0x773d0000|*True*|*True*|*True*|\WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll|
|0x77c10000|*True*|*True*|*True*|\WINDOWS\system32\msvcrt.dll|
|0x870000|*True*|*True*|*True*|__???__|
|0x7c9c0000|*True*|*True*|*True*|\WINDOWS\system32\shell32.dll|
|0x76f20000|*True*|*True*|*True*|\WINDOWS\system32\dnsapi.dll|
|0x5d090000|*True*|*True*|*True*|\WINDOWS\system32\comctl32.dll|
|0x71aa0000|*True*|*True*|*True*|\WINDOWS\system32\ws2help.dll|
|0x77b20000|*True*|*True*|*True*|\WINDOWS\system32\msasn1.dll|


Durch diese Ausgaben erkennen wir, dass unsere 2 verdächtigen mehrere DLLs unverlinkt haben.
Hier noch ein Bild wie man sich die "unlinking DLLs" vorstellen kann:

<a href="../assets/img/hideDll.png" ><img width="300" height="214" src="../assets/img/hideDll.png"/></a>

### Scannen von Prozessen

Ein Scan mit der Funktion "malfind" könnte den Verdacht bestätigen. Denn malfind untersucht Prozesse auf eingeschleusten Code. 

{% highlight bash %}
stuxnet.vmem 23:14:00> malfind[680,868,1928]
{% endhighlight %}

Die Ausgabe ist extrem lange und ich bin zurzeit noch nicht in der Lage alles dazu zu erklären. Ein wichtiger Punkt ist die "MZ" Marke, da es sich dabei um ausführbaren Code handelt.

<a href="../assets/img/mz.png" ><img width="300" height="214" src="../assets/img/mz.png"/></a>

### Prozesse Extrahieren

Die Prozesse können zu weiteren Untersuchungen (Disassembly) aus dem Abbild extrahiert werden.
Dazu:

{% highlight bash %}
stuxnet.vmem 23:55:00> procdump[680,868,1928],dump_dir="./out"
{% endhighlight %}

### Funktionszugriffe einsehen

Die nun Extrahierten .exe Dateien, können mit Tools wie __strings__ untersucht werden.
Wie bereits erwähnt, sollten die schädlichen 2 Prozesse, Funktionen aufrufen, die atypisch für Authentifizierungsserver sind, dafür aber Indizien aufgeben für einen Schädling. Besonders eine RAT *(Remote Access Tool)* wird zu vermuten sein,
da diese Art von Viren viel Kontrolle benötigen, darunter Kontrolle über Fenster, Tasteneingaben, Mausführung, Dokumente, Verzeichnisse etc.
Dazu müsste ein neuer Terminal geöffnet und folgender Befehl eingegeben werden:

{% highlight bash %}
strings --print-file-name --data --encoding=s executable.lsass.exe*  | grep --perl-regexp "ZwMapViewOfSection|ZwCreateSection|ZwOpenFile|ZwClose|ZwQueryAttributesFile|ZwQuerySection"
{% endhighlight %}

{% highlight bash %}
executable.lsass.exe_1928.exe: ZwMapViewOfSection
executable.lsass.exe_1928.exe: ZwCreateSection
executable.lsass.exe_1928.exe: ZwOpenFile
executable.lsass.exe_1928.exe: ZwClose
executable.lsass.exe_1928.exe: ZwQueryAttributesFile
executable.lsass.exe_1928.exe: ZwQuerySection
executable.lsass.exe_868.exe: ZwMapViewOfSection
executable.lsass.exe_868.exe: ZwCreateSection
executable.lsass.exe_868.exe: ZwOpenFile
executable.lsass.exe_868.exe: ZwClose
executable.lsass.exe_868.exe: ZwQueryAttributesFile
executable.lsass.exe_868.exe: ZwQuerySection
{% endhighlight %}

Prozess 680 fehlt in der Ausgabe. Ein Authentifizierungsserver würde diese Funktionen nicht benötigen.
Alle Untersuchungsschritte weisen unmissverständlich darauf hin, dass Prozess 680 der legitime originale "lsass.exe" ist.

### Assembly-Code analysieren

Ab hier bräuchte man erweitertes Assembly-Wissen, über das ich zurzeit nicht verfüge.
Daher endet dieser Blog fürs erste an diesem Punkt.


### Fazit

Dieses Projekt hat mir sehr viel Spass gemacht und ich habe die IT-Forensik kennengelernt.
Da die Begeisterung mich nicht loslässt, wird dieser Blog weiterhin ausgebaut.

### Scripte


__Stringsvergleich automatisieren__
<details><summary>[Ausklappen]</summary>
Hier noch ein kleines Script der die Ausgaben von Strings vergleicht.
(Es wird noch ein Script folgen für die Suche von verdächtigen Prozessen)

Funktionsweise:
Es handelt sich hier um ein Python-Script. Als Argumente werden 2 Dateien angegeben.
Die erste stellt das Original dar und die zweite wird mit der ersten verglichen.

{% highlight bash %}
python script.py executable.lsass.exe_680.exe executable.lsass.exe_868.exe
{% endhighlight %}
<p></p>
__Ausgabe:__

<a href="../assets/img/scriptausgabe.png" alt="Vergleichen mit dem Python-Skript"><img width="300" height="214" src="../assets/img/scriptausgabe.png"/></a>

Die Zeilen mit [+] bedeuten, dass diese Strings in beiden Dateien vorkommen. 
Die mit [!] hingegen, dass sie bei der ersten Datei nicht vorkommen.


<details><summary>Quellcode</summary>
    
    <pre style='color:#000020;background:#f6f8ff;'><span style='color:#200080; font-weight:bold; '>from</span> sys <span style='color:#200080; font-weight:bold; '>import</span> argv
<span style='color:#200080; font-weight:bold; '>import</span> os

<span style='color:#200080; font-weight:bold; '>class</span> cl<span style='color:#308080; '>:</span>
    HEADER <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[95m'</span>
    OKBLUE <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[94m'</span>
    OKGREEN <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[92m'</span>
    <span style='color:#074726; '>WARNING</span> <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[93m'</span>
    FAIL <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[91m'</span>
    ENDC <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[0m'</span>
    BOLD <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[1m'</span>
    UNDERLINE <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\0</span><span style='color:#1060b6; '>33[4m'</span>


<span style='color:#200080; font-weight:bold; '>def</span> cmpStrings<span style='color:#308080; '>(</span><span style='color:#308080; '>)</span><span style='color:#308080; '>:</span>
    <span style='color:#595979; '>#Get List1</span>
    <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span><span style='color:#1060b6; '>"[ ] get strings of "</span><span style='color:#44aadd; '>+</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>1</span><span style='color:#308080; '>]</span><span style='color:#308080; '>)</span>
    cmdReturn <span style='color:#308080; '>=</span> os<span style='color:#308080; '>.</span>popen<span style='color:#308080; '>(</span><span style='color:#1060b6; '>"strings "</span><span style='color:#44aadd; '>+</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>1</span><span style='color:#308080; '>]</span><span style='color:#308080; '>)</span><span style='color:#308080; '>.</span>read<span style='color:#308080; '>(</span><span style='color:#308080; '>)</span>
    firstList <span style='color:#308080; '>=</span> buildList<span style='color:#308080; '>(</span>cmdReturn<span style='color:#308080; '>)</span>
    <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span>cl<span style='color:#308080; '>.</span>OKGREEN<span style='color:#44aadd; '>+</span><span style='color:#1060b6; '>"[+] "</span><span style='color:#44aadd; '>+</span><span style='color:#400000; '>str</span><span style='color:#308080; '>(</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>1</span><span style='color:#308080; '>]</span><span style='color:#308080; '>)</span><span style='color:#44aadd; '>+</span><span style='color:#1060b6; '>" converted to a list..."</span><span style='color:#44aadd; '>+</span>cl<span style='color:#308080; '>.</span>ENDC<span style='color:#308080; '>)</span>
    <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span><span style='color:#1060b6; '>"[ ] get strings of "</span><span style='color:#44aadd; '>+</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>2</span><span style='color:#308080; '>]</span><span style='color:#308080; '>)</span>
    cmdReturn <span style='color:#308080; '>=</span> os<span style='color:#308080; '>.</span>popen<span style='color:#308080; '>(</span><span style='color:#1060b6; '>"strings "</span><span style='color:#44aadd; '>+</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>2</span><span style='color:#308080; '>]</span><span style='color:#308080; '>)</span><span style='color:#308080; '>.</span>read<span style='color:#308080; '>(</span><span style='color:#308080; '>)</span>
    secondList <span style='color:#308080; '>=</span> buildList<span style='color:#308080; '>(</span>cmdReturn<span style='color:#308080; '>)</span>
    <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span>cl<span style='color:#308080; '>.</span>OKGREEN<span style='color:#44aadd; '>+</span>cl<span style='color:#308080; '>.</span>BOLD<span style='color:#44aadd; '>+</span><span style='color:#1060b6; '>"[+] "</span><span style='color:#44aadd; '>+</span>argv<span style='color:#308080; '>[</span><span style='color:#008c00; '>2</span><span style='color:#308080; '>]</span><span style='color:#44aadd; '>+</span><span style='color:#1060b6; '>" converted to a list..."</span><span style='color:#44aadd; '>+</span>cl<span style='color:#308080; '>.</span>ENDC<span style='color:#308080; '>)</span>
    <span style='color:#200080; font-weight:bold; '>for</span> c <span style='color:#200080; font-weight:bold; '>in</span> secondList<span style='color:#308080; '>:</span>
        <span style='color:#200080; font-weight:bold; '>if</span><span style='color:#308080; '>(</span>c <span style='color:#200080; font-weight:bold; '>in</span> firstList<span style='color:#308080; '>)</span><span style='color:#308080; '>:</span>
            <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span><span style='color:#1060b6; '>"[+] "</span><span style='color:#44aadd; '>+</span>c<span style='color:#308080; '>)</span>
        <span style='color:#200080; font-weight:bold; '>else</span><span style='color:#308080; '>:</span>
            <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span>cl<span style='color:#308080; '>.</span>FAIL<span style='color:#44aadd; '>+</span><span style='color:#1060b6; '>"[!] "</span><span style='color:#44aadd; '>+</span>c<span style='color:#44aadd; '>+</span>cl<span style='color:#308080; '>.</span>ENDC<span style='color:#308080; '>)</span>

<span style='color:#200080; font-weight:bold; '>def</span> buildList<span style='color:#308080; '>(</span>myString<span style='color:#308080; '>)</span><span style='color:#308080; '>:</span>
    out<span style='color:#308080; '>=</span><span style='color:#308080; '>[</span><span style='color:#308080; '>]</span>
    actualStr<span style='color:#308080; '>=</span><span style='color:#1060b6; '>''</span>
    <span style='color:#200080; font-weight:bold; '>for</span> c <span style='color:#200080; font-weight:bold; '>in</span> <span style='color:#400000; '>str</span><span style='color:#308080; '>(</span>myString<span style='color:#308080; '>)</span><span style='color:#308080; '>:</span>
        <span style='color:#200080; font-weight:bold; '>if</span> c <span style='color:#44aadd; '>!=</span> <span style='color:#1060b6; '>'</span><span style='color:#0f69ff; '>\n</span><span style='color:#1060b6; '>'</span><span style='color:#308080; '>:</span>
            actualStr <span style='color:#44aadd; '>+</span><span style='color:#308080; '>=</span> c
        <span style='color:#200080; font-weight:bold; '>else</span><span style='color:#308080; '>:</span>
            out<span style='color:#308080; '>.</span>append<span style='color:#308080; '>(</span>actualStr<span style='color:#308080; '>)</span>
            actualStr <span style='color:#308080; '>=</span> <span style='color:#1060b6; '>''</span>
    <span style='color:#200080; font-weight:bold; '>return</span> out

<span style='color:#200080; font-weight:bold; '>if</span> <span style='color:#074726; '>__name__</span><span style='color:#44aadd; '>==</span><span style='color:#1060b6; '>"__main__"</span><span style='color:#308080; '>:</span>
    <span style='color:#200080; font-weight:bold; '>print</span><span style='color:#308080; '>(</span><span style='color:#1060b6; '>"Start"</span><span style='color:#308080; '>)</span>
    cmpStrings<span style='color:#308080; '>(</span><span style='color:#308080; '>)</span>
</pre>
<!--Created using ToHtml.com on 2019-01-24 14:11:33 UTC -->
</details>
{% highlight bash %}
shasum:   e07034165a3030b2707e432149e3dc4a913c32f4
{% endhighlight %}
<a href="../scripte/compStrings.py" download>Als File herunterladen</a>
</details>

