# Logboek practicum 3

---
Template;
**Datum:**
Omschrijving werk:
---
**Datum: 24-2-2025**
Omschrijving werk: Github repository aangemaakt. Logboek aangemaakt. 
Afmaken plan van aanpak; evaluatie en reflectie schrijven; 
planning afbeelding vervangen; inleiding, achtergrond informatie, 
project beschrijving, project fases en planning afgemaakt; spellingscontrole; 
toevoegen bronnenlijst; plan van aanpak ingeleverd en geüpload naar github
---
**Datum: 25-2-2025**
Omschrijving werk: Feedback plan van aanpak; reflectie geschreven; ticketing fase 2
opgezet en bijgewerkt; html & css bestanden in git; teksten uit PvA op juiste pagina's;
footer github link gemaakt; menu en andere links werkend gemaakt;
---
**Datum 26-2-2025**
Omschrijving werk: Inhoudelijke teksten verbeteren; styling consistent maken; css bestand
ordenen en opschonen; footer schoollink gemaakt; gekregen feedback op plan van aanpak verwerkt; menu verplaatst &
icoontjes werkend op juiste plek; alle documenten gevalideerd online;

#### Feedback plan van aanpak
- De gebruiker moet meerdere dingen in kunnen stellen. Bij deze tool is dit waarschrijnlijk slecht te configureren, 
waarschijnlijk wel wat bij de installatie van de tool, maar niet per run.
- Kijk of je de gebruiker de hoeveelheid plotjes kunt laten instellen (of evt icoontjes kun laten kiezen)
- kijken naar output van de tool (csv of alleen maar png) en of daar zelf een plot mee te maken is d.m.v. matplotlib, 
daar zijn dan ook weer configuratiemogelijkheden.

Het bestand limits.txt in de configuration map zou in principe aangepast kunnen voordat je fastqc runt. Dat zou betekenen dat je 
een python scriptje runt vooraf, die limits.txt aanpast naar de wensen van de gebruiker. Verder zijn hier ook de 
mogelijkheid tot het toevoegen van adapters en contaminants in respectievelijke bestanden in dezelfde map.

De resultaten zijn:
- html-bestand met interactieve resultaten, hetzelfde als in programma van de tool zelf.
- zip die bevat:
    - summery.txt -> lijst met per test pass, warn fail
    - hetzelfde html bestand nogmaals
    - data.txt -> tekstbestand met alle data (geen resultaten), hier zou je zelf de grafieken van kunnen maken.
    - .fo bestand → ???
    - map met icoontjes (png)
    - map met plaatjes (png & html duplicaten)

Verder is er een header-template.html waar je de look van de output kan veranderen. Als je je eigen plotjes maakt minder relevant.

----
**Datum: 27-2-2025**
Omschrijving werk: bestanden van meer comments voorzien; reflectie fase 2; fastqc_page gemaakt; 
start research html forms; begonnen met readme;

-----
**Datum:4-3-2025**
Omschrijving werk: br syntax; feedback verwerking; Flask demo's doorwerken; Flask tutorial;
app.py aangemaakt; base.html aangemaakt als basis template; alle html files op de base html aangepast;
css kloppend gemaakt met flask & jinja veranderingen;

-----
**Datum: 5-3-2025**
Omschrijving werk: resultaten pagina aangemaakt; html forms toegevoegd; forms via app.py aan resultaten
pagina gekoppeld; teksten en limits uitklapbaar gemaakt; ticketing opgeschoond en verbeterd;
 help fastqc html's aan forms gekoppeld en uitklapbaar gemaakt; styling fastqc pagina; repo ingeleverd

---
**Datum: 6-3-2025**
Omschrijving werk: feedback ontvangen en besproken; alle html en css gevalideerd; app.py bekommentariseerd
en van docstring voorzien; alle html bekommentariseerd; referentielink onder help pagina's gemaakt;
css voor referentielink; opnieuw repo ingeleverd

----
**Datum: 8-3-2025**
Omschrijving werk: reflectie fase 3 geschreven; ticketing fase 4; readme;

----
**Datum: 13-3-2025**
Omschrijving werk: plotting boxplot; plotting table; 
----
**Datum: 14-3-2025**
Omschrijving werk: start plotting heatmap; research in per tile quality module;
----
**Datum: 15-3-2025**
Omschrijving werk: plotting heatmap werkend gemaakt; plot per sequence quality scores; plot
per base sequence content; plot per sequence GC content; plot per base N content;
----
**Datum: 17-3-2025**
Omschrijving werk: plot sequence length distribution; plot sequence duplication levels;
----
**Datum: 19-3-2025**
Omschrijving werk: Duplication plot gefixt; overrepresented plot gemaakt; adapter plot gemaakt;
kmer table gemaakt, plot is niet mogelijk;

-----
**Datum: 20-3-2025**
Omschrijving werk: Opschoning ticketing & planning; 

----
**Datum: 21-3-2025**
Omschrijving werk: Betere oplossing voor de tables gemaakt; OOP refresher;

----
**Datum: 24-3-2025**
Omschrijving werk: limits.py limits class; hoofdfunctie gemaakt; prep functie gemaakt; output 
functie gemaakt; limits.py testing; main.py aangemaakt; FastQC class voor uitvoeren tool via de 
terminal; FastQC class testing; start plotting class in Plotting_v2.py 

----
**Datum: 25-3-2025**
Omschrijving werk: main.py hoofdfunctie naar ReadingDataTextFile class omgezet; onderlinge 
koppeling zodat de limits class; fastqc class; readingdatatextfile class & maketables class 
vanuit app.py uitgevoerd kunnen; koppeling in html en css;

----
**Datum: 26-3-2025**
Omschrijving werk: Verder in plotting class met boxplot; onderlinge koppeling; styling boxplot; 
start heatplot;

----
**Datum: 27-3-2025**
Omschrijving werk: Verder met heatplot; styling heatplot; start 1e lineplot;

----
**Datum: 28-3-2025**
Omschrijving werk: Verder met lineplotten; styling verschillende lineplotten; data prep 
verschillende lineplotten gekoppeld; 

----
**Datum: 29-3-2025**
Omschrijving werk: Herverdeling Plotting class tot MakePlots & PrepPlotData gebruikmakend van 
inheritance;
----
**Datum: 31-3-2025**
Omschrijving werk: Afronding plotting classes; achtergrond styling plotten; theoretische 
normaalverdeling plot niet werkend gekregen en in overleg met docent geschrapt; 

----
**Datum: 1-4-2025**
Omschrijving werk: Onderlinge koppeling van alle python scrips; koppeling app.py & resultaten 
html; verbetering limits.py; verbetering fastqc class;

----
**Datum: 2-4-2025**
Omschrijving werk: Als alle methodes aangevinkt zijn alles werkend en kloppend; gestart met 
becommentariëren main.py & plotting.py; feedback moment; fastqc tool toegevoegd aan project & 
onderlinge koppeling relatief gemaakt;

----
**Datum: 3-4-2025**
Omschrijving werk: limits class werkend met relatief pad; write output functie verbeterd; 
limits.py becommentarieerd;

----
**Datum: 7-4-2025**
Omschrijving werk: git branches merge; limits.py pylint, docstrings & comments; app.py pylint,
docstrings & comments; main.py pylint, docstrings & comments; start plotting.py pylint, 
docstrings & comments;

----
**Datum: 8-4-2025**
Omschrijving werk: pylint & comments plotting.py afgerond; file knopje gefikst;
streaming ipv saving plotten; deelse weergave van uitgevoerde methods gemaakt; logboek & reflectie
opgeschoond & gecommit

----
**Datum: 9-4-2025**
Omschrijving werk: readme verbeterd, grove versie; overzicht laatste taken; vertalen tool pagina;
valideren html; limits whitespacing


