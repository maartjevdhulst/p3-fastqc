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