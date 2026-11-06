# Детекторы отказов и обнаружение по сердцебиению/тайм-ауту: новые источники для статьи 1 (2.2.15)

Дата поиска: 6 ноября 2026 г. Проверено против `/home/user/asp/09-references.md` (65 позиций + раздел кандидатов). Исключены как уже имеющиеся: Chandra–Toueg [18], Chen–Toueg–Aguilera [9], Hayashibara φ-accrual [10], Ma–Hillston–Anderson [21], Freiling–Guerraoui–Kuznetsov [22], Falcon/Leners [23] и его продолжение EuroSys 2015 (упомянуто в разделе 1.5), Phan-Ba [14], Pingmesh [62], RFC 5880 [2], RFC 7419 [63], Ben Hassan–Mansour BFD/VRRP [65], Vayghan [13], Roberts [3], Chen–Goudarzi [5], Aguilera–Le Lann–Toueg (кандидат), документация Kubernetes «Nodes» [1], MetalLB [25]. Bertier в списке отдельной позицией не обнаружен, но в поиске новых работ не требовался.

**Итог:** основной список — 17 новых позиций (Н1–Н17), из них 9 за 2021–2026 гг. (Н1–Н9) и 8 более ранних (Н10–Н17); плюс 6 резервных (Р1–Р6). Способ проверки: CrossRef REST API по DOI (`https://api.crossref.org/works/<DOI>`), OpenAlex по DOI (`https://api.openalex.org/works/doi:<DOI>`, для аннотаций), JSON-метаданные и текст RFC с rfc-editor.org (`https://www.rfc-editor.org/rfc/rfcNNNN.json`, `.txt`), страница журнала (hrcak.srce.hr). DBLP недоступен из среды (антибот-заглушка), IEEE/ScienceDirect/Springer/USENIX вернули 403 — поэтому содержание большинства статей сверено **только по аннотации**, не по полному тексту.

## Вопрос 1. φ-accrual, SWIM/Lifeguard, госсип и адаптивные/обучаемые тайм-ауты (особенно 2019–2026)

### Takeaway
Свежая (2023–2026) рецензируемая линия адаптивных детекторов существует и оценивается теми же метриками качества обслуживания Чена–Туэга (частота ошибок, вероятность правильного ответа, время обнаружения) на трассах PlanetLab — это даёт статье прямую опору для «частоты ложных объявлений» как измеряемой величины. Lifeguard даёт важный практический аргумент: ложные срабатывания порождаются не только потерей сообщений в сети, но и медленной обработкой на стороне наблюдателя, то есть p в модели надо трактовать как «потеряно или опоздало» по любой причине.

### Cited Findings

**Н1.** Chaurasia B., Verma A., Verma P. IHFD: an improved heartbeat-based failure detector of ◇P class for partially synchronous hierarchical distributed systems // Complex & Intelligent Systems. — 2026. — Vol. 12, № 12. — Article 312. — DOI: 10.1007/s40747-026-02423-z.
*Проверено:* CrossRef (https://api.crossref.org/works/10.1007/s40747-026-02423-z) — авторы, журнал, том 12, выпуск 12, номер статьи 312, дата публикации 9 авг. 2026; аннотация — OpenAlex. Страниц нет (статья с номером).
*Релевантность:* детектор сочетает адаптивную оценку тайм-аута со «статистической обработкой отклонений»; на трассах PlanetLab сравнивается с Chen, Bertier, PHI и др.; в корне иерархии частота ошибок (Mistake Rate) 6,6·10⁻⁵ и вероятность правильного ответа (Query Accuracy Probability) 0,9999, тогда как у Bertier и PHI частота ошибок 34,4–53,1·10⁻³ и 40,2–58,3·10⁻³ соответственно — пример того, что метрики Чена–Туэга остаются стандартом оценки в 2026 г. — [OpenAlex](https://api.openalex.org/works/doi:10.1007/s40747-026-02423-z); [CrossRef](https://api.crossref.org/works/10.1007/s40747-026-02423-z)

**Н2.** Sens P., Arantes L., Rossetto A. G. de M., Marin O. Stab-FD: A cooperative and adaptive failure detector for wide area networks // Journal of Parallel and Distributed Computing. — 2024. — Vol. 186. — Article 104803. — DOI: 10.1016/j.jpdc.2023.104803.
*Проверено:* CrossRef (том 186, апрель 2024, номер статьи 104803; OpenAlex указывает 2023 — это дата онлайн-публикации; в ГОСТ-описании брать год тома 2024). Аннотация в CrossRef/OpenAlex отсутствует; содержание — по фрагменту страницы ScienceDirect в поисковой выдаче (сама страница отдала 403).
*Релевантность:* детектор наблюдает стабильность дальних каналов и адаптивно калибрует таймеры по локальному и удалённому виду канала для повышения качества обслуживания; сравнивается с детекторами Chen и Bertier на трассах PlanetLab — работа о подстройке тайм-аута под наблюдаемую вероятность опоздания, т. е. о выборе τ·k в зависимости от p. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0743731523001739); [CrossRef](https://api.crossref.org/works/10.1016/j.jpdc.2023.104803)

**Н3.** Johansson B., Rågberger M., Papadopoulos A. V., Nolte T. Consistency Before Availability: Network Reference Point based Failure Detection for Controller Redundancy // Proc. 2023 IEEE 28th Int. Conf. on Emerging Technologies and Factory Automation (ETFA). — IEEE, 2023. — P. 1–8. — DOI: 10.1109/ETFA54631.2023.10275664.
*Проверено:* CrossRef + OpenAlex (аннотация).
*Релевантность:* в схеме горячего резерва контроллера обнаружение по сердцебиению с известным периодом трактует отсутствие сообщений как отказ, поэтому разделение сети неотличимо от отказа узла и даёт два активных первичных контроллера; авторы предлагают «опорные точки сети», жертвуя готовностью ради согласованности. Прямая иллюстрация цены ложного объявления отказа (член ущерба от ускорения обнаружения) в системе с резервированием. — [OpenAlex](https://api.openalex.org/works/doi:10.1109/etfa54631.2023.10275664)

**Н10.** Das A., Gupta I., Motivala A. SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol // Proc. Int. Conf. on Dependable Systems and Networks (DSN 2002). — IEEE, 2002. — P. 303–312. — DOI: 10.1109/DSN.2002.1028914.
*Проверено:* CrossRef (страницы 303–312, авторы; дата в CrossRef не указана); OpenAlex указывает 2003 — расхождение; год 2002 следует из идентификатора DOI (DSN.2002) и названия конференции. Аннотация — OpenAlex.
*Релевантность:* мотивирован тем, что классические протоколы сердцебиения либо дают квадратичную по размеру группы нагрузку, либо ухудшают время реакции или частоту ложных срабатываний; SWIM разделяет обнаружение и распространение, а ожидаемое время до первого обнаружения и нагрузка на участника не зависят от размера группы. Классическая формулировка того же компромисса «скорость — ложные срабатывания — служебная нагрузка», что и в модели с τ и k. — [OpenAlex](https://api.openalex.org/works/doi:10.1109/dsn.2002.1028914); [PDF](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf)

**Н11.** Dadgar A., Phillips J., Currey J. Lifeguard: Local Health Awareness for More Accurate Failure Detection // Proc. 48th Annual IEEE/IFIP Int. Conf. on Dependable Systems and Networks Workshops (DSN-W). — IEEE, 2018. — P. 22–25. — DOI: 10.1109/DSN-W.2018.00017. (Препринт: arXiv:1707.00788.)
*Проверено:* CrossRef (страницы 22–25, июнь 2018) + OpenAlex (аннотация).
*Релевантность:* в эксплуатации SWIM наблюдалась высокая частота ложных срабатываний из-за чувствительности к медленной обработке сообщений; расширения Lifeguard, учитывающие «локальное здоровье» детектора, снижают частоту ложных срабатываний более чем в 50 раз; авторы делают вывод, что модель fail-stop слишком упрощена для крупных ЦОД (кратковременное голодание ЦП, сбои ввода-вывода, случайная потеря пакетов). Основание для трактовки p как вероятности «потеряно ИЛИ опоздало», включая задержку обработки на приёмнике. — [OpenAlex](https://api.openalex.org/works/doi:10.1109/dsn-w.2018.00017); [arXiv](https://arxiv.org/pdf/1707.00788)

### Inferences
- Н1 и Н2 показывают, что в 2023–2026 гг. сравнение детекторов по-прежнему ведётся по метрикам Чена–Туэга [9] на трассах PlanetLab; ни одна из найденных работ (по аннотациям) не выводит системный коэффициент готовности как функцию параметров детектора — это согласуется с заявленным в 09-references разрывом, но полные тексты не прочитаны.
- Н3 даёт инженерный, а не вероятностный аргумент за «член ущерба» от ложного обнаружения: в резервированной паре ложное объявление отказа порождает раздвоение ведущего, а не просто лишнее переключение.
- Lifeguard (Н11) прямо поддерживает допущение статьи, что ложное объявление вызывается «потерей или опозданием» контрольного сообщения, но ставит под сомнение независимость событий: перегрузка наблюдателя коррелирует потери, что уводит от p^k к пакетной модели (Гилберт–Эллиотт уже есть в списке как [50], [51]).

### Gaps
- Не найдено рецензируемых работ 2021–2026 гг. именно о φ-accrual с машинным обучением/прогнозом межприходных интервалов: поиск дал только реализации и учебные материалы. Упоминаемый в выдаче «детектор на распределении Вейбулла для облаков» (PLOS ONE) не проверен — выходные данные не найдены.
- Полные тексты Н1, Н2, Н3 не получены (Springer/Elsevier/IEEE — 403); численные результаты Н2 и Н3 не сверены.
- Rapid (Suresh et al.) — см. резерв Р3: место публикации (USENIX ATC 2018) из среды подтвердить не удалось.

## Вопрос 2. Анализ BFD: время обнаружения, ложные срабатывания, настройка интервала и кратности; RFC помимо 5880 и 7419

### Takeaway
Номера и названия RFC подтверждены по rfc-editor.org: 5881, 5883, 7880, 9747 (март 2025) и 9764 (апрель 2025) — все Proposed Standard; RFC 9747 прямо воспроизводит правило «Detect Mult пропущенных пакетов → Down», т. е. ту же модель k·τ для режима эхо без управляющей сессии. Рецензируемых аналитических работ по BFD с моделью ложных срабатываний как функции (τ, k, p) найти не удалось; в литературе встречаются разные формулы времени обнаружения, что стоит оговорить в статье.

### Cited Findings

**Н4.** Cheng W., Wang R., Min X. (Ed.), Rahman R., Boddireddy R. Unaffiliated Bidirectional Forwarding Detection (BFD) Echo: RFC 9747. — IETF, March 2025. — Proposed Standard. — DOI: 10.17487/RFC9747. — URL: https://www.rfc-editor.org/rfc/rfc9747.txt
*Проверено:* https://www.rfc-editor.org/rfc/rfc9747.json + текст RFC.
*Релевантность:* режим эхо без связанной управляющей сессии; дословно: «When the bfd.SessionState is Up and a "Detect Mult" number of Unaffiliated BFD Echo packets have not arrived at device A as they should, the device A "MUST set bfd.SessionState to Down"»; интервал передачи задаётся на стороне A, поля интервалов в пакете «MUST NOT be used in the calculation of the Detection Time». Подтверждает, что пороговое правило k последовательных пропусков сохраняется в новейшем расширении BFD (2025) и применимо к узлам-хостам, не поддерживающим BFD. — [RFC 9747](https://www.rfc-editor.org/rfc/rfc9747.txt)

**Н5.** Haas J., Fu A. Bidirectional Forwarding Detection (BFD) Encapsulated in Large Packets: RFC 9764. — IETF, April 2025. — Proposed Standard. — DOI: 10.17487/RFC9764. — URL: https://www.rfc-editor.org/rfc/rfc9764.txt
*Проверено:* rfc-editor.org JSON + текст.
*Релевантность:* пакеты BFD обычно очень малы; RFC задаёт проверку способности тракта переносить полезную нагрузку заданного размера в асинхронном режиме (контроль Path MTU). Для статьи — обоснование того, что длина контрольного сообщения влияет на p и служебную нагрузку, а значит, является параметром настройки наряду с τ и k (раздел 3.4 диссертации выводит длину сообщения из формата [2]). — [RFC 9764](https://www.rfc-editor.org/rfc/rfc9764.txt)

**Н12.** Katz D., Ward D. Bidirectional Forwarding Detection (BFD) for IPv4 and IPv6 (Single Hop): RFC 5881. — IETF, June 2010. — Proposed Standard. — DOI: 10.17487/RFC5881. — URL: https://www.rfc-editor.org/rfc/rfc5881.txt
*Проверено:* rfc-editor.org JSON + текст (UDP-порт назначения 3784; TTL/Hop Limit 255 при передаче и проверка 255 при приёме).
*Релевантность:* профиль BFD для однопролётного IP — именно тот, который используется между соседними узлами в ЦОД/кластере (в т. ч. в MetalLB [25]); ссылка нужна, чтобы привязать модель к конкретной инкапсуляции контрольного сообщения. — [RFC 5881](https://www.rfc-editor.org/rfc/rfc5881.txt)

**Н13.** Katz D., Ward D. Bidirectional Forwarding Detection (BFD) for Multihop Paths: RFC 5883. — IETF, June 2010. — Proposed Standard. — DOI: 10.17487/RFC5883. — URL: https://www.rfc-editor.org/rfc/rfc5883.txt
*Проверено:* rfc-editor.org JSON + текст (порт 4784; защита TTL=255 «obviously does not work across multiple hops», нужна аутентификация).
*Релевантность:* многопролётный BFD (например, между узлами оверлейной сети контейнеров): вероятность p потери/опоздания на многопролётном тракте выше и зависит от числа переходов — обоснование, почему τ и k нельзя переносить с однопролётного случая без пересчёта. — [RFC 5883](https://www.rfc-editor.org/rfc/rfc5883.txt)

**Н14.** Pignataro C., Ward D., Akiya N., Bhatia M., Pallagatti S. Seamless Bidirectional Forwarding Detection (S-BFD): RFC 7880. — IETF, July 2016. — Proposed Standard. — DOI: 10.17487/RFC7880. — URL: https://www.rfc-editor.org/rfc/rfc7880.txt
*Проверено:* rfc-editor.org JSON + аннотация в тексте («simplified mechanism for using BFD with a large proportion of negotiation aspects eliminated»; обновляет RFC 5880; роли SBFDInitiator/SBFDReflector).
*Релевантность:* устраняет согласование параметров сессии — актуально для динамически создаваемых контейнерных функций, где время установления сессии само входит во время до начала контроля. — [RFC 7880](https://www.rfc-editor.org/rfc/rfc7880.txt)

**Н6.** Wang Y., Fang R. An Approach for Fast Fault Detection in Virtual Network // Tehnički vjesnik — Technical Gazette. — 2023. — Vol. 30, № 4. — P. 1146–1151. — DOI: 10.17559/TV-20230207000330.
*Проверено:* страница журнала на портале Hrčak (https://hrcak.srce.hr/305459: том 30, № 4, с. 1146–1151, дата выпуска 28.06.2023) + CrossRef.
*Релевантность:* для ВМ, контейнеров и распределённого ПО обнаружение протокольными методами на плоскости управления занимает секунды, через пользовательский интерфейс — сотни миллисекунд, причём основное время от отказа до восстановления уходит на обнаружение; предложено обнаружение по невыбранным сообщениям в очереди VIRTIO виртуального сетевого элемента с порогом по времени, что переводит обнаружение «с секундного на миллисекундный уровень». Утверждение о превосходстве над BFD и ping — по фрагменту выдачи, количественно не сверено. — [Hrčak](https://hrcak.srce.hr/305459)

### Inferences
- Для «частоты ложных объявлений ∝ (1−p)p^k/τ» рецензируемого первоисточника с выводом той же формулы найти не удалось; формула выводится авторской работой из правил RFC 5880 [2]. Это стоит прямо оговорить в статье.
- В литературе формула времени обнаружения BFD записывается по-разному: Yamansavascilar et al. (резерв Р1, по arXiv-версии) — T_d = (M+1)·T_i; вендорская документация — T_i × M; RFC 5880 — Detect Mult × согласованный интервал как тайм-аут; среднее (k−½)τ — это усреднение по фазе отказа внутри периода. Расхождение полезно упомянуть одной фразой, чтобы рецензент не принял (k−½)τ за ошибку.
- RFC 9747 (2025) и RFC 9764 (2025) позволяют показать, что BFD — развивающийся стандарт, и закрыть требование по доле источников 2021–2026 нормативными документами.

### Gaps
- Не найдено рецензируемых аналитических/экспериментальных работ, где частота ложных срабатываний BFD измерялась бы как функция интервала и кратности при заданной потере пакетов. Поиск дал документацию вендоров (Cisco, Juniper, Arista, Oracle) и патенты; найденная статья в Libyan Journal of Informatics о FHRP+BFD (ResearchGate 393513502) не проверена — год и выходные данные не установлены, не включена.
- Работы по BFD для VNF/облаков в рецензируемых журналах 2021–2026 гг. — кроме Н6 — не найдены; патенты (BFD offload в vNIC, S-BFD для ВМ/контейнеров) не включены как непрофильные для ВАК.
- RFC 5882 (Generic Application of BFD, июнь 2010, DOI 10.17487/RFC5882) подтверждён по метаданным, но его содержание (вопросы подавления дребезга сессии) в этой сессии не сверено — в резерв не вносился.

## Вопрос 3. Обнаружение отказа узла в Kubernetes: node-monitor-grace-period, сердцебиение через Lease, измерения задержки

### Takeaway
Рецензируемых работ 2021–2026 гг. с измерением времени обнаружения отказа узла Kubernetes в зависимости от node-monitor-grace-period найти не удалось — выдача состоит из блогов и документации. Первичным (нерецензируемым) источником служат официальная справка kube-controller-manager и KEP-589; важная находка — справка дословно формулирует ту же структуру «тайм-аут = N × период обновления», что и BFD k·τ.

### Cited Findings
- Справка kube-controller-manager (текущая версия документации): `--node-monitor-grace-period` по умолчанию **50s**, описание: «Amount of time which we allow running Node to be unresponsive before marking it unhealthy. Must be N times more than kubelet's nodeStatusUpdateFrequency, where N means number of retries allowed for kubelet to post node status»; `--node-monitor-period` по умолчанию 5s. — [kubernetes.io](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) (см. резерв Р6 — дополнение к [1]).
- KEP-589 «Efficient Node Heartbeat» (SIG Node, статус Implemented): kubelet обновляет объект Lease «every 10s by default»; «Lack of NodeStatus update for <node-monitor-grace-period> (default: 40s) results in NodeController marking node as NotReady»; NodeStatus обновляется раз в 5 мин. — [KEP-589](https://www.kubernetes.dev/resources/keps/589/) (резерв Р5).
- Расхождение: в KEP-589 значение по умолчанию 40 с, в текущей справке — 50 с. Блоги относят изменение к v1.31 или v1.32 и противоречат друг другу — [DEV](https://dev.to/naresh_007/the-six-minutes-that-decide-a-kubernetes-node-failure-47hd); версию изменения по первичному источнику (release notes) не подтвердил.

### Inferences
- Lease 10 с и grace period 40/50 с соответствуют k = 4–5 при τ = 10 с в терминах модели статьи; это прямое отображение (τ, k) на параметры Kubernetes, которое можно привести, сославшись на [1]/Р6, без рецензируемого источника.
- Дефицит рецензируемых измерений сам по себе подтверждает актуальность темы; уже имеющиеся [3], [5], [13] остаются основными экспериментальными опорами.

### Gaps
- Нет рецензируемых работ 2021–2026 гг. с измерением времени обнаружения отказа узла Kubernetes и ложных NotReady как функции grace period. Работа KAR (arXiv:2111.11562, «Reliable Actors with Retry Orchestration») измеряет время простоя собственной платформы (около 22 с на k3d), а не штатного Kubernetes — не включена; рецензируемая версия не проверена.
- Версия Kubernetes, в которой значение по умолчанию сменилось с 40 на 50 с, не подтверждена.

## Вопрос 4. Быстрое обнаружение отказов в SDN и программируемой плоскости данных (fast failover, OpenFlow + BFD, P4)

### Takeaway
В SDN устойчиво установлено, что при защите (fast failover с заранее рассчитанными путями) время восстановления определяется временем обнаружения, а не переключением; BFD в коммутаторе — стандартный способ уложиться в 50 мс. Новые работы 2023–2025 гг. переносят сердцебиение в программируемую плоскость данных P4 и доходят до единиц микросекунд при интервале 4 мкс, вводя приоритизацию очередей против ложных тревог — та же ось «τ ↓ ⇒ ложные срабатывания ↑», решаемая уменьшением p.

### Cited Findings

**Н7.** Ji C., Kuipers F. FASTR: Fast Resilience for Stateful Programmable Data Planes // Proc. 21st Int. Conf. on Network and Service Management (CNSM 2025). — IFIP/IEEE, 2025. — P. 1–7. — DOI: 10.23919/CNSM67658.2025.11297557.
*Проверено:* CrossRef + OpenAlex (аннотация); PDF на dl.ifip.org — 403.
*Релевантность:* сердцебиение реализовано целиком в плоскости данных; обнаружение отказа между соседними коммутаторами стабильно в пределах 10 мкс при интервале 4 мкс; учёт трафика снижает служебную нагрузку, а приоритетная очередь для контрольных сообщений служит для «avoid false alarms» при перегрузке. Прямой пример снижения p (вероятности опоздания контрольного сообщения) как способа допустить малые τ без роста ложных срабатываний. — [OpenAlex](https://api.openalex.org/works/doi:10.23919/cnsm67658.2025.11297557)

**Н8.** Franco D., Higuero M., Zaballa E. O., Unzilla J., Jacob E. Quantitative measurement of link failure reaction time for devices with P4-programmable data planes // Telecommunication Systems. — 2023 (онлайн 19.12.2023; год тома не подтверждён). — Vol. 85, № 2. — P. 277–288. — DOI: 10.1007/s11235-023-01084-4.
*Проверено:* CrossRef (том 85, № 2, с. 277–288; онлайн 19.12.2023). CrossRef даёт только дату онлайн-публикации 19.12.2023; год выпуска тома 85 явно не выведен — **не подтверждён**, при оформлении сверить на сайте Springer.
*Релевантность:* обзор процедур обнаружения, реакции и восстановления при отказе канала и количественное измерение времени реакции устройств с программируемой плоскостью данных относительно требования < 50 мс для сетей операторского класса; разделение «обнаружение / реакция / восстановление» совпадает со структурой составляющих времени простоя в модели. — [CrossRef](https://api.crossref.org/works/10.1007/s11235-023-01084-4)

**Н9.** Mazloum A., Kfoury E., Gomez J., Crichigno J. A Survey on Rerouting Techniques with P4 Programmable Data Plane Switches // Computer Networks. — 2023. — Vol. 230. — Article 109795. — DOI: 10.1016/j.comnet.2023.109795.
*Проверено:* CrossRef (июль 2023, том 230, № статьи 109795).
*Релевантность:* обзор перемаршрутизации в P4; по фрагменту текста — использование встроенных генераторов пакетов для BFD позволяет вынести обнаружение отказа канала в плоскость данных и снизить зависимость от плоскости управления. Обзорная опора для утверждения, что минимально достижимый τ определяется тем, где исполняется детектор. — [PDF](https://research.cec.sc.edu/files/cyberinfra/files/a_survey_on_rerouting_techniques_1.pdf); [CrossRef](https://api.crossref.org/works/10.1016/j.comnet.2023.109795)

**Н15.** van Adrichem N. L. M., van Asten B. J., Kuipers F. A. Fast Recovery in Software-Defined Networks // Proc. 2014 Third European Workshop on Software Defined Networks (EWSDN). — IEEE, 2014. — P. 61–66. — DOI: 10.1109/EWSDN.2014.13.
*Проверено:* CrossRef + OpenAlex (аннотация).
*Релевантность:* восстановление складывается из (a) обнаружения, (b) уведомления контроллера, (c) пересчёта путей; схема с BFD-сессией на каждом канале и заранее вычисленными основным и резервным путями сокращает время восстановления на порядок, причём оно постоянно и не зависит от длины пути и размера сети. Подтверждает декомпозицию времени простоя, где обнаружение — доминирующая управляемая составляющая. — [OpenAlex](https://api.openalex.org/works/doi:10.1109/ewsdn.2014.13)

**Н16.** Sharma S., Staessens D., Colle D., Pickavet M., Demeester P. OpenFlow: Meeting carrier-grade recovery requirements // Computer Communications. — 2013. — Vol. 36, № 6. — P. 656–665. — DOI: 10.1016/j.comcom.2012.09.011.
*Проверено:* CrossRef (март 2013, том 36, № 6, с. 656–665). Аннотация в OpenAlex отсутствует.
*Релевантность:* по вторичному пересказу (документ репозитория TU Delft в выдаче): восстановление по инициативе контроллера может превышать 100 мс, тогда как защита с BFD и fast failover укладывается в 50 мс, причём бо́льшая часть времени (около 40–44 мс) приходится на обнаружение BFD. **Числа не сверены по первоисточнику** — проверить перед цитированием. — [TU Delft repository](https://repository.tudelft.nl/file/File_4db1d88a-4652-4e38-bfc9-67572ac4db47); [CrossRef](https://api.crossref.org/works/10.1016/j.comcom.2012.09.011)

**Н17.** Cascone C., Sanvito D., Pollini L., Capone A., Sansò B. Fast failure detection and recovery in SDN with stateful data plane // International Journal of Network Management. — 2017. — Vol. 27, № 2. — Article e1957. — DOI: 10.1002/nem.1957.
*Проверено:* CrossRef (том 27, № 2, № статьи e1957; онлайн 22.11.2016) + аннотация CrossRef. Год тома 2017 — **не подтверждён явно** (CrossRef даёт дату онлайн-публикации 2016).
*Релевантность:* SPIDER — конвейер с периодическим зондированием каналов в коммутаторе (аналог BFD Hello) и быстрым перенаправлением без участия контроллера; указывает, что штатный OpenFlow fast failover не позволяет настраивать механизм обнаружения, а с зондированием в плоскости данных задержки обнаружения и восстановления гарантируются; по arXiv-версии (1511.05490) число потерянных пакетов снижается при уменьшении интервала сердцебиения и тайм-аута. — [CrossRef](https://api.crossref.org/works/10.1002/nem.1957); [arXiv](https://arxiv.org/pdf/1511.05490)

### Inferences
- Н7 (2025) и Н15/Н16 (2013–2014) вместе дают диапазон достижимого τ_min от микросекунд (плоскость данных P4) до десятков миллисекунд (BFD в коммутаторе/ОС) — это контекст для τ_min из раздела 3.3 и ориентира 50 мс [61].
- Ни одна из работ SDN-направления (по аннотациям) не ставит задачу оптимального выбора (τ, k) по критерию готовности; они минимизируют время восстановления при фиксированном или «достаточно малом» интервале — пространство для новизны статьи.

### Gaps
- Цифры «19,63–1564,33 мс» среднего времени автоматического переключения коммутаторов OpenFlow в зависимости от модели и типа канала встретились в выдаче без однозначной атрибуции к первоисточнику — не включены.
- Рецензируемые работы о BFD в контроллерах SDN (ONOS/OpenDaylight) с измерением ложных срабатываний 2021–2026 не найдены; ближайшее — Sakic, Kellerer (IEEE TNSM 2018, DOI 10.1109/TNSM.2017.2775061) о Raft в распределённой плоскости управления SDN, где ложные срабатывания детектора отказа лидера ведут к повторным выборам; содержание по первоисточнику не сверено, в список не вносилось.

---

**Резерв (проверены выходные данные; включать при нехватке или по необходимости):**

- **Р1.** Yamansavascilar B., Baktir A. C., Ozgovde A., Ersoy C. Fault tolerance in SDN data plane considering network and application based metrics // Journal of Network and Computer Applications. — 2020. — Vol. 170. — Article 102780. — DOI: 10.1016/j.jnca.2020.102780. *Проверено:* CrossRef; arXiv:1912.11849 (аннотация). Основная тема — защита с учётом качества альтернативных путей и QoE DASH; по arXiv-версии приводит формулу T_d = (M+1)·T_i и трактует кратность как защиту от ложных срабатываний при потере пакетов — полезно лишь как пример расхождения формул.
- **Р2.** Huang P., Guo C., Zhou L., Lorch J. R., Dang Y., Chintalapati M., Yao R. Gray Failure: The Achilles' Heel of Cloud-Scale Systems // Proc. 16th Workshop on Hot Topics in Operating Systems (HotOS XVI). — ACM, 2017. — P. 150–155. — DOI: 10.1145/3102980.3103005. *Проверено:* CrossRef (в CrossRef название — «Gray Failure»; полный подзаголовок по памяти, сверить). Содержание в этой сессии не сверено.
- **Р3.** Suresh L., Malkhi D., Gopalan P., Porto Carreiro I., Lokhandwala Z. Stable and Consistent Membership at Scale with Rapid. — arXiv:1803.03620, 2018. *Проверено:* arxiv.org/abs/1803.03620 (подозрение только по сигналам от нескольких источников; устойчивость при односторонней недостижимости и высокой потере пакетов). Публикация в USENIX ATC 2018 и страницы — **не подтверждено** (usenix.org — 403).
- **Р4.** Rahman R. (Ed.), Zheng L. (Ed.), Jethanandani M. (Ed.), Pallagatti S., Mirsky G. YANG Data Model for Bidirectional Forwarding Detection (BFD): RFC 9127. — IETF, October 2021. — DOI: 10.17487/RFC9127. *Проверено:* rfc-editor.org JSON; содержание не сверено. Примечание: RFC 9764 ссылается на модули BFD YANG из RFC 9314 — соотношение 9127/9314 не проверено.
- **Р5.** KEP-589: Efficient Node Heartbeat / W. Tyczynski (wojtek-t) et al. — Kubernetes Enhancement Proposal, SIG Node. — URL: https://www.kubernetes.dev/resources/keps/589/ *Проверено:* страница KEP (статус Implemented; Lease каждые 10 с; grace period 40 с в тексте KEP). Полное имя автора по GitHub-нику — не подтверждено.
- **Р6.** kube-controller-manager: Command line tools reference // Kubernetes Documentation. — URL: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/ *Проверено:* страница (node-monitor-grace-period = 50s, формулировка «N times more than kubelet's nodeStatusUpdateFrequency»). Логично оформить как дополнительный URL к имеющейся позиции [1], а не как новую позицию.
