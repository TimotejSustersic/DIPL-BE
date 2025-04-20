\section{Temperatura okolice}

Zmogljivost baterij električnih vozil (EV) je zelo občutljiva na temperaturo okolice, kar vpliva tako na operativno učinkovitost kot na dolgoročno zdravje baterije. Litij-ionske baterije, ki so prevladujoča tehnologija v EV, kažejo izrazite elektrokemijske odzive na temperaturne spremembe.

\subsection{Optimalni temperaturni razponi delovanja}

Baterije EV najbolje delujejo v zmernem temperaturnem razponu, običajno med 15–25°C. Izven tega okvira so zmogljivost in življenjska doba baterije prizadeti. Nizke temperature povečajo notranjo upornost, kar upočasni mobilnost ionov, medtem ko visoke temperature pospešijo kemično degradacijo in zmanjšajo kapaciteto.

Študija iz leta 2024 o električnih dvokolesnikih \cite{Xu2024} je ta razpon natančneje opredelila na 20–30°C za optimalno energetsko učinkovitost in doseg vožnje, pri čemer je uporabila podatke iz realnih pogojev. Prav tako je ugotovila, da se temperatura celic baterij pogosto poveča za ~2.2°C nad temperaturo okolice. Čeprav lahko EV varno delujejo med -20°C in 60°C, ostaja vrhunska učinkovitost omejena na ožji temperaturni razpon.

\subsection{Pogoji pri nizkih temperaturah}

Hladno vreme predstavlja izzive za zmogljivost EV zaradi povečane notranje upornosti in zmanjšane mobilnosti ionov. Pri -10°C se lahko doseg vozila zmanjša za 15–20\%, kot so pokazali Basso et al. (2019) \cite{Basso2019}. Xu et al. (2024) so kvantificirali povečanje porabe energije za 35.4\% pri -15°C v primerjavi z 24°C. Podobno so Liu et al. \cite{Liu2022} poročali o zmanjšanju dosega vožnje do 30\% v hladnih pogojih.

Nizke temperature prav tako vplivajo na učinkovitost regenerativnega zaviranja. Yazan et al. so ugotovili, da delovanje pri temperaturah med 0–15°C zmanjša doseg vožnje za ~28\% v primerjavi z zmernimi temperaturami (15–25°C).

\subsection{Pogoji pri visokih temperaturah}

Visoke temperature predstavljajo tveganja za pospešeno degradacijo baterije in povečano porabo energije. Lindgren et al. \cite{Lindgren2022} so poudarili dolgoročna tveganja poslabšanja pod ekstremno vročino, medtem ko so Kulkarni et al. \cite{Kulkarni2021} pokazali, da podvojitev temperature okolice od 25°C poveča porabo energije za ~35\% na kilometer.

Ti izsledki poudarjajo dvojni izziv takojšnjih vplivov na zmogljivost in dolgoročne poškodbe v vročih pogojih.

\subsection{Tehnološke rešitve in strategije blaženja posledic}

Za obvladovanje učinkov temperature so proizvajalci razvili napredne sisteme za termično upravljanje baterij (BTMS). Ti sistemi uporabljajo metode hlajenja, kot so zračno hlajenje, tekoče hlajenje, materiali s faznim prehodom ali hibridni pristopi, da ohranijo optimalne temperature baterij.

\subsection{Uporaba v algoritmu}

preko API-jev lahko izracunam povprecno temperaturo na sto kilometrov in primerno omejim domet
