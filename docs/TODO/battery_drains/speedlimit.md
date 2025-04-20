\section{Hitrost vožnje}

Povezava med hitrostjo vožnje in porabo energije v električnih vozilih (EV) je močna in zelo nelinearna, predvsem zaradi vpliva sil zračnega upora. Z naraščanjem hitrosti se moč, potrebna za premagovanje zračnega upora, znatno poveča, kar zmanjšuje celotno energetsko učinkovitost.

Sila zračnega upora ($F_d$), ki deluje na premikajoče se vozilo, je podana z enačbo:

\[
F_d = \frac{1}{2} \rho v^2 C_d A
\]

kjer je $F_d$ sila zračnega upora, $\rho$ gostota zraka, $v$ hitrost, $C_d$ koeficient zračnega upora in $A$ čelna površina vozila.

Ta povezava pomeni, da majhna povečanja hitrosti vodijo do nesorazmerno višje porabe energije. Na primer, podvojitev hitrosti s 50 km/h na 100 km/h poveča porabo energije na enoto razdalje za faktor štiri pod idealiziranimi pogoji, kjer prevladuje zračni upor.

Ta trend podpira raziskava o učinkovitosti EV. Pri avtocestnih hitrostih lahko zračni upor predstavlja do 50\% celotne porabe energije EV. Za razliko od vozil z notranjim zgorevanjem (ICEV), ki so običajno učinkovitejša na avtocestah kot v mestni vožnji, EV pogosto dosegajo boljšo učinkovitost v mestnih pogojih z ustavljanjem in speljevanjem zaradi regenerativnega zaviranja.

Višje hitrosti, zlasti na avtocestah, znatno povečajo porabo energije. \cite{Kancharla2018} so ugotovili, da lahko 10\% povečanje hitrosti poveča porabo energije do 20\%, odvisno od zasnove vozila in voznih pogojev. Podobno je \cite{Fiori2016} pokazal, da so EV najbolj učinkoviti pri zmernih hitrostih (40-70 km/h), pri čemer se učinkovitost nad tem razponom močno zmanjša. Na primer, povečanje hitrosti s 100 km/h na 120 km/h lahko zmanjša doseg vozila za 20-25\%. Tako so lahko srednje hitre arterijske ceste pogosto optimalne za učinkovitost EV.

Običajni algoritmi za usmerjanje, ki dajejo prednost času potovanja pred porabo energije, lahko izberejo hitre poti, ki so za EV suboptimalne. Sodobni modeli usmerjanja bi morali vključevati profile hitrosti, ki upoštevajo spremembe na poti, in tako pomagati voznikom izbrati poti, ki ohranjajo učinkovite hitrosti ter zmanjšujejo prekomerna nihanja hitrosti.

\subsection{Spreminjanje hitrosti in vzorci pospeševanja}

Matematični modeli porabe energije EV med pospeševanjem kažejo, da je poraba energije na kilometer odvisna od hitrosti in pospeševanja. Ko so parametri vozila in cestni pogoji konstantni, je poraba odvisna od profilov hitrosti in pospeševanja. Študije kažejo, da lahko uporaba več skrbno upravljanih krivulj pospeševanja za dosego ciljne hitrosti iz mirovanja zmanjša porabo energije na kilometer v primerjavi z enojnim, konstantnim pospeševanjem.

Ta vpogled vpliva na strategije ekološke vožnje in sisteme prilagodljivega tempomata, kar nakazuje, da lahko gladke, postopne krivulje pospeševanja izboljšajo učinkovitost, tudi pri višjih potovalnih hitrostih. Raziskovalci so opredelili optimalne strategije pospeševanja za specifične pogoje glede na ciljne hitrosti: sosedski (0-40 km/h), mestni (0-80 km/h) in avtocestni (0-120 km/h), pri čemer vsaka zmanjšuje porabo energije.

\subsection{Uporaba v algoritmu}

Ceste imajo omejitve katere lahko upostevam v izracun uporabe.
