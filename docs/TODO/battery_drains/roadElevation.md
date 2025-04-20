\section{Nadmorska višina}

Električna vozila izkazujejo različne vzorce porabe energije, odvisno od terena, ki ga prevozijo. Nadmorska višina in naklon predstavljata kritična dejavnika, ki vplivata na porabo baterije, z vidnimi posledicami za načrtovanje poti in oceno doseganja. Ta raziskava preučuje fizikalne mehanizme, kvantifikativne vplive in praktične vidike, povezane z vplivom sprememb nadmorske višine na porabo energije pri električnih vozilih.

\subsection{Fizikalni principi porabe energije}

Osnovni odnos med nadmorsko višino in porabo energije pri električnih vozilih izhaja iz osnovnih fizikalnih načel. Kot je opisano v predhodnem delu, potencialno energijo, potrebno za premagovanje nadmorskega višinskega razlike, lahko izrazimo s pomočjo enačbe \( E = mgh \), kjer \( m \) predstavlja maso vozila, \( g \) pa težnostno pospešek, in \( h \) razliko v višini. Ta enačba, čeprav poenostavljena, zagotavlja teoretično osnovo za razumevanje, zakaj električna vozila porabijo več energije pri vzpenjanju.

Pri vzpenjanju mora pogonski sistem vozila ustvariti dovolj veliko silo, da premaga tako valjno kot težnostno silo, ki deluje proti smeri gibanja. Ta dodatno delo se neposredno prevede v povečano porabo energije iz baterije. Zahteva po moči se povečuje sorazmerno z naklonom in maso vozila. Težja električna vozila z večjimi baterijskimi paketi paradoksalno zahtevajo več energije za vzpenjanje, kar ustvarja izziv za ravnotežje med zmogljivostjo doseganja in energetsko učinkovitostjo na hribovitih poteh.

Fizika porabe energije glede na nadmorsko višino pri električnih vozilih tudi predstavlja zanimivo dualnost. Medtem ko vzpenjanje po hribih zahteva dodatno energijo, spuščanje omogoča vračanje energije preko regenerativnega zaviranja. Med spuščanjem se vozilova potencialna energija pretvori nazaj v električno energijo, namesto da bi se izgubila kot toplina preko klasičnih zaviralnih sistemov. Vendar pa je to vračanje nikoli popolno – fizikalne omejitve in sistemovske neefikasnosti pomenijo, da je energija, pridobljena med spuščanjem, vedno manjša od dodatne energije, porabljene med ustreznim vzpenjanjem.

\subsection{Kvantitativni vpliv}

Raziskave kažejo, da lahko spremembe nadmorske višine pomembno vplivajo na porabo energije pri električnih vozilih. Na primer, 100 metrov nadmorskega višinskega razlike lahko poveča porabo energije za 5–10\%. Vzpenjačni odseki lahko povečajo porabo energije za do 30\% v primerjavi z vožnjo po ravni površini pri podobnih hitrostih \cite{Zhang2018}. Razmerje med naklonom in porabo energije ni popolnoma linearno; zmerni nakloni med 2–5\% povzročajo sorazmerno večje izgube učinkovitosti, kot bi jih napovedal preprosti fizikalni model.

Študije, ki preučujejo vzorce vožnje v realnem svetu, kažejo, da lahko regenerativno zaviranje povrne približno 30–70\% dodatne energije, porabljene med vzpenjanjem, odvisno od dejavnikov, kot so specifični model vozila, profil spuščanja in vedenje voznika \cite{Montoya2017}. Učinkovitost regenerativnega zaviranja se zmanjša pri strmih spuščanjih, saj je maksimalna moč, ki jo lahko ujame regenerativni sistem, omejena.

Zhang et al. \cite{Zhang2018} so ugotovili, da lahko poraba energije pri električnih vozilih pomembno vpliva izbira poti v območjih z različnimi nadmorskimi profilom. Poti z enakimi razdaljami lahko kažejo razlike v porabi energije do 30\% samo zaradi kumulativnega nadmorskega višinskega razlike in njene porazdelitve po poti.

Montoya et al. \cite{Montoya2017} so razvili modele porabe energije, ki posebej obravnavajo nelinearne funkcije polnjenja in dejavnike nadmorske višine pri problemih potovanja električnih vozil. Njihova raziskava je potrdila, da lahko točno modeliranje nadmorske višine izboljša napovedi porabe energije za 8–15\% v primerjavi z modeli, ki zanemarjajo topografske informacije. Podobno so Froger et al. \cite{Froger2019} vključili nelinearne funkcije polnjenja v probleme potovanja električnih vozil, ki upoštevajo spremembe energije glede na nadmorsko višino.

\subsection{Uporaba v algoritmu}

Preko API-je lahko ocenim visinske razlike. Ko ta podatek pridobim lahko izracunam povprecen vzpon na kilometer in temu primerno ocenim porabo energije ter kolicino nazaj pridobljene.
