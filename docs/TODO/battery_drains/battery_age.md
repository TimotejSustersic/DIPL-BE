\section{Starost in zdravje baterije}

Degradacija baterij v električnih vozilih (EV) predstavlja kritični vidik, ki neposredno vpliva na zmogljivost vozila, napovedovanje dosega in na koncu uporabnost vozila skozi celoten njegov življenjski ciklus. Ta poglavje preiskuje kompleksne mehanizme staranja baterij, dejavnike, ki pospešujejo degradacijo, in njihove posledice za sistem za usmerjanje v vozilih z električnim pogonom.

\subsection{Mehanizmi degradacije baterij}

Degradacija baterij se dogaja naravno s časom, predvsem zaradi ciklov polnjenja in praznjenja ter kalendarskega staranja. Povprečno izgubijo baterije vozil z električnim pogonom okoli 2–3\% kapacitete na leto po začetnem obdobju. Do osmega leta lahko nekatere baterije izgubijo celo 20\% uporabne kapacitete \cite{Hiermann2016}.

\subsection{Kalendarsko staranje}

Kalendarsko staranje predstavlja izgubo kapacitete, ki se pojavi s časom, tudi kadar baterija ni aktivno ciklirana. V nasprotju s tradicionalnimi mehanskimi sistemi, kjer se staranje dogaja med delovanjem, se litij-ionske baterije degradirajo tudi kadar so neaktivne. Ta pojav je zelo pomemben za električna vozila, ki preživijo velik del svojega življenjskega cikla parkirana.

Stopnja kalendarskega staranja je močno odvisna od dveh ključnih dejavnikov: temperature in stanja polnjenosti (SoC). Baterije, shranjene pri povišanih temperaturah nad 35°C in pri visokih stanjih polnjenosti nad 70\%, doživljajo znatno pospešeno degradacijo. Optimalni shranjevalni pogoji, pri katerih se baterije hranijo pri temperaturah med 10–15°C in pri stanju polnjenosti pod 50\%, lahko zmanjšajo to staranje. Vendar so takšni pogoji redko dosegljivi v praksi.

Študije so pokazale, da zmanjšanje časa, preživetega pri visokih stanjih polnjenosti, lahko zelo zmanjša kalendarsko staranje. Na primer, Lunz et al. so pokazali, da znižanje ciljnih vrednosti stanja polnjenosti in zmanjšanje časov mirovanja pri visokih stanjih polnjenosti lahko bistveno podaljša življenjsko dobo baterij \cite{Lunz2011}.

\subsection{Ciklično staranje}

Ciklično staranje nastane zaradi ponavljajočih se ciklov polnjenja in praznjenja. Na molekularni ravni se degradacija pojavlja zaradi kemijskih reakcij in fizikalnih sprememb v materialih anode in katode. Med ciklom se litijevi ioni gibljejo med anodo in katodo, kar proizvaja energijo za delovanje vozila. V tem procesu pride do izgube litijevih ionov in sprememb v notranji kemijski strukturi baterije.

Na strani anode so glavni mehanizmi degradacije tvorba trdne elektrolitske meje (SEI), elektropliranje kovinskega litija in izguba aktivnega materiala. Ko baterija preide skozi začetne cikle, litijevi ioni iz katode in organske spojine iz topila elektrolita reagirajo z grafitno anodo in tvorijo tanko plast, znano kot SEI. Ta proces nepovratno porabi litij, zmanjša dostopno količino litija za nadaljnje cikliranje in zmanjša kapaciteto baterije.

\subsection{Vpliv temperature}

Temperatura je eden od najpomembnejših dejavnikov, ki vpliva na degradacijo litij-ionskih baterij, tako med shranjevanjem kot med aktivnim uporabo. Raziskave so pokazale, da baterije, ki delujejo pri povišanih temperaturah, doživljajo znatno pospešeno staranje. Na primer, Dubarry et al. so pokazali, da je baterija, preizkušena pri 60°C, razvila petkrat več notranjega upora v primerjavi z identično baterijo, ki je delovala pri 25°C \cite{Dubarry2012}.

Za optimalno delovanje in trajnost bi baterije morale biti polnjene v temperaturnem območju med 15–50°C. Pesaran et al. so določili območje med 15–35°C kot idealno za vozila z hibridnim električnim pogonom (PHEV), saj je pokazalo, da je zmanjšanje stopnje degradacije povezano z manjšimi in bolj ekonomičnimi baterijskimi sistemi \cite{Pesaran2009}.

\subsection{Stanje polnjenosti in globina praznjenja}

Stanje polnjenosti (SoC) in globina praznjenja (DoD) imata pomembno vlogo pri določanju življenjske dobe baterije, tako med shranjevanjem kot med delovanjem. Raziskave kažejo, da je izogibanje globokim ciklom praznjenja nad 60\% DoD ključno za ohranjanje maksimalne življenjske dobe baterije.

Staranje baterij med shranjevanjem je predvsem odvisno od temperature in stanja polnjenosti, pri čemer visoka stanja polnjenosti pospešujejo izgubo kapacitete. Za vozila z hibridnim električnim pogonom so Smith et al. predlagali strategije za zmanjšanje kalendarskega staranja pri visokih stanjih polnjenosti, kot so polnjenje ob pravem času in namerno delno praznjenje za baterije v vozilih, parkiranih v vročem okolju \cite{Smith2018}.

\subsection{Uporaba v algoritmu}

glede na starost vozila in povprecno degradacijo lahko ocenim dejansko kapaciteto baterije ter jo upostevam pri izračunu.
