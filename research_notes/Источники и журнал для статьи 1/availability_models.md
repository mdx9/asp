# Модели готовности восстанавливаемых систем с учётом обнаружения отказа, покрытия и ложных срабатываний (NFV, SDN, облако, контейнеры)

**Итог:** основной список — 18 новых позиций (А1–А18), из них 10 с годом выпуска тома 2021–2026 (А9–А18). Оговорка: у А9 (Sebastio et al.) журнальный том датирован 2021 г., но ранний доступ был в 2017–2018 г. Без неё за 2021–2026 гг. остаётся 9 из 18, то есть ровно половина. Ещё 15 проверенных позиций вынесены в резерв (Р1–Р15). Ни одна позиция не совпадает с [1]–[65] из `09-references.md` и с работами, упомянутыми в его служебных разделах: Aguilera/Le Lann/Toueg DISC 2002, Fischer/Lynch/Paterson, Hsu/Lee/Ke MATCOM, Leners et al. EuroSys 2015, ETSI NFV-REL 007. С `failure_detectors.md` пересечений нет.

**Метод проверки.** Выходные данные (авторы, название, издание, год, том, выпуск, страницы, DOI) по каждой позиции получены из CrossRef REST API (`api.crossref.org/works?query.bibliographic=…`), аннотации — из OpenAlex (`api.openalex.org/works/https://doi.org/<DOI>`). Ссылка на запись CrossRef для каждой работы имеет вид `https://api.crossref.org/works/<DOI>`. Полные тексты **не читались**: содержание сверено только по аннотациям. Где аннотация не получена, это указано явно.

**Главный отрицательный результат.** Не найдено ни одной рецензируемой работы, где ложные объявления отказа входили бы в модель готовности как интенсивность, зависящая от времени обнаружения, и порождали бы внутренний оптимум T_o. Ближайшие работы таковы: А4 (типы детекторов, задержки обнаружения и несовершенное покрытие в модели готовности, без ложных срабатываний), А8 (компромисс «время обнаружения — частота ложных тревог», но для детектора аномалий, а не в модели готовности) и А14 (отказы самого средства обнаружения, но без ложных срабатываний). Это подкрепляет формулировку новизны статьи.

---

## Вопрос 1. Марковские, полумарковские модели, SRN, SAN и SPN готовности NFV, SDN, облака, Kubernetes и контейнеров

### Takeaway
Направление хорошо развито: SAN-модели NFV и NFV-MANO (группа NTNU), SRN-модели контейнеров и контейнеризированного IMS, полумарковские модели цепочек сервисных функций, модель кластера Kubernetes на SysML. Время обнаружения в этих работах — **заданный входной параметр или предмет анализа чувствительности**. Ложные объявления отказа ни в одной из них не моделируются (по аннотациям).

### Cited Findings

**А6.** Sakic E., Kellerer W. Response Time and Availability Study of RAFT Consensus in Distributed SDN Control Plane // IEEE Transactions on Network and Service Management. — 2018. — Vol. 15, № 1. — P. 304–318. — DOI: 10.1109/TNSM.2017.2775061.
*Проверено: CrossRef (https://api.crossref.org/works/10.1109/tnsm.2017.2775061); аннотация — OpenAlex.* Модели на стохастических сетях активностей (SAN) для кластера SDN-контроллеров ONOS и OpenDaylight с RAFT: выборы лидера после отказа контроллера, восстановление состояния, время отклика и готовность. Интенсивности восстановления кластера измерены в реальных экспериментах. Показано, что быстрое омоложение ПО снижает время отклика и повышает долговременную готовность. Задержка обнаружения отказа лидера (тайм-аут выборов RAFT) — естественный аналог T_o. Входит ли она в модель как отдельный параметр и учитываются ли ложные перевыборы, по аннотации **не установлено**: проверить по полному тексту — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tnsm.2017.2775061).

**А7.** Tola B., Nencioni G., Helvik B. E. Network-Aware Availability Modeling of an End-to-End NFV-Enabled Service // IEEE Transactions on Network and Service Management. — 2019. — Vol. 16, № 4. — P. 1389–1403. — DOI: 10.1109/TNSM.2019.2948725.
*Проверено: CrossRef; аннотация — OpenAlex.* Двухуровневая модель: нижний уровень — минимальные сечения топологии, верхний — SAN для динамики отказов VNF, MANO, узлов сети и SDN-контроллеров. Численный результат: менее надёжные узлы сети снижают готовность NFV-службы **более чем на порядок** даже при резервировании VNF и MANO. Интеграция с SDN ухудшает готовность, если контроллеры не защищены — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tnsm.2019.2948725).

**А9.** Sebastio S., Ghosh R., Mukherjee T. An Availability Analysis Approach for Deployment Configurations of Containers // IEEE Transactions on Services Computing. — 2021. — Vol. 14, № 1. — P. 16–29. — DOI: 10.1109/TSC.2017.2788442.
*Проверено: CrossRef (том 14, № 1, 2021); OpenAlex датирует работу 2018 г. по раннему доступу, при цитировании указывать 2021.* Деревья отказов и стохастические сети вознаграждений (SRN) для конфигураций развёртывания контейнеров по мотивам Kubernetes: служба реагирования на отказ и миграция, готовность k из N, чувствительность к ключевым параметрам, открытый программный инструмент для анализа «что если». Одна из первых аналитических моделей готовности контейнерной платформы — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tsc.2017.2788442).

**А10.** Di Mauro M., Galatro G., Longo M., Postiglione F., Tambasco M. Comparative Performability Assessment of SFCs: The Case of Containerized IP Multimedia Subsystem // IEEE Transactions on Network and Service Management. — 2021. — Vol. 18, № 1. — P. 258–272. — DOI: 10.1109/TNSM.2020.3044232.
*Проверено: CrossRef; аннотация — OpenAlex.* SRN и структурные схемы надёжности (RBD) для контейнеризированного IMS как цепочки сервисных функций. Совместный анализ готовности и производительности (performability) с алгоритмом OptChains+, который ищет конфигурации минимальной стоимости при заданной производительности. Есть анализ чувствительности. Телекоммуникационная служба на контейнерах — прямая предметная параллель статьи — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tnsm.2020.3044232).

**А11.** Tola B., Jiang Y., Helvik B. E. Model-Driven Availability Assessment of the NFV-MANO With Software Rejuvenation // IEEE Transactions on Network and Service Management. — 2021. — Vol. 18, № 3. — P. 2460–2477. — DOI: 10.1109/TNSM.2021.3090208.
*Проверено: CrossRef; аннотация — OpenAlex.* SAN-модели конфигураций развёртывания NFV-MANO по образцу контейнеризированных открытых реализаций. Учтено омоложение ПО и исследован **компромисс между его накладными расходами и приростом готовности** — структурный аналог компромисса «ускорение обнаружения — ложные срабатывания». Параметры восстановления получены инъекцией отказов на реальной реализации MANO — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tnsm.2021.3090208).

**А12.** Di Mauro M., Galatro G., Postiglione F., Tambasco M. Performability of Network Service Chains: Stochastic Modeling and Assessment of Softwarized IP Multimedia Subsystem // IEEE Transactions on Dependable and Secure Computing. — 2022. — Vol. 19, № 5. — P. 3071–3086. — DOI: 10.1109/TDSC.2021.3082626.
*Проверено: CrossRef (в CrossRef фамилия первого автора записана как «Mauro Mario Di»); аннотация — OpenAlex; препринт arXiv:2105.09004.* Стенд на платформе Clearwater. Производительность — сеть массового обслуживания с узлами M/G/c; готовность — SRN-модель отказов и восстановлений softIMS. Ищутся оптимальные конфигурации, обеспечивающие заданную готовность (например, «пять девяток») при минимальной стоимости — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tdsc.2021.3082626).

**А15.** Bai J., Chang X., Machida F., Jiang L., Han Z., Trivedi K. S. Impact of Service Function Aging on the Dependability for MEC Service Function Chain // IEEE Transactions on Dependable and Secure Computing. — 2023. — Vol. 20, № 4. — P. 2811–2824. — DOI: 10.1109/TDSC.2022.3150782.
*Проверено: CrossRef; аннотация — OpenAlex.* Полумарковская модель переходной и стационарной готовности и надёжности цепочки сервисных функций MEC/NFV с произвольным числом функций; учтены старение, отказ и восстановление. Точность проверена имитационным моделированием, исследованы узкие места через анализ чувствительности и влияние неэкспоненциальных распределений интервалов — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tdsc.2022.3150782).

**А16.** Bai J., Chang X., Machida F., Trivedi K. S., Li Y. Model-Driven Dependability Assessment of Microservice Chains in MEC-Enabled IoT // IEEE Transactions on Services Computing. — 2023. — Vol. 16, № 4. — P. 2769–2785. — DOI: 10.1109/TSC.2023.3241430.
*Проверено: CrossRef; аннотация — OpenAlex.* Многомерная полумарковская модель цепочки микросервисов. **Совместно оптимизируются интервалы срабатывания омоложения** ОС узла и микросервисов, то есть управляемый временной параметр с внутренним оптимумом по готовности. Приведены диапазоны значений параметров, гарантирующие «пять девяток». Показано превосходство над CTMC-моделью. Методическая параллель к оптимизации T_o — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tsc.2023.3241430).

**А17.** Hecht M., Agena S. A Reliability and Availability Model of a Kubernetes Cluster Using SysML // Proc. 2024 Annual Reliability and Maintainability Symposium (RAMS). — IEEE, 2024. — P. 1–7. — DOI: 10.1109/RAMS51492.2024.10457826.
*Проверено: CrossRef; аннотация — OpenAlex.* Модель надёжности и готовности кластера Kubernetes в SysML (MBSE). Параметры модели измеряются средствами хаос-тестирования LitmusChaos. Численные результаты сверены с независимой моделью и совпали до 9-й значащей цифры. Продолжение: Hecht M. Software Reliability and Availability Testing of a Kubernetes Cluster // RAMS 2026, DOI 10.1109/RAMS50514.2026.11424466 — измеренные время и вероятность восстановления служат входом модели (см. Р14) — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/rams51492.2024.10457826).

**А18.** Mandal P. Availability and Reliability of Core Networks (4G/5G) From a Deployment Standpoint // IEEE Transactions on Services Computing. — 2025. — Vol. 18, № 2. — P. 647–659. — DOI: 10.1109/TSC.2025.3528332.
*Проверено: CrossRef; аннотация — OpenAlex.* Аналитическая модель готовности и надёжности сетевой службы ядра 4G/5G из VNF с учётом отказов узла, ВМ и узлов ядра. Сравниваются размещение в одной ВМ и в нескольких. Численный результат: размещение в одной ВМ даёт **более 14 % выигрыша по готовности и более 100 % по надёжности** — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tsc.2025.3528332).

### Inferences
- Время обнаружения отказа в моделях NFV, SDN и контейнеров — заданная величина или объект анализа чувствительности. Члена, который наказывал бы за ускорение обнаружения, нет; по аннотациям ни одна работа не содержит ложных объявлений отказа. Поэтому оптимум T_o в них возникнуть не может. Это согласуется с логикой раздела 1.4 диссертации о противодействующем члене.
- Ближайший методический аналог внутреннего оптимума по временному параметру — оптимизация интервала омоложения (А11, А16). Его можно цитировать как образец постановки «управляемый временной параметр ↔ накладные расходы ↔ готовность».

### Gaps
- Не найдено рецензируемой SPN- или SRN-модели готовности **Kubernetes** с явным параметром node-monitor-grace-period или тайм-аута обнаружения. Найдены только SBRC-доклады на португальском (Chaos-K8s, K8s-DT; https://sol.sbc.org.br/index.php/sbrc/article/view/42303, https://sol.sbc.org.br/index.php/sbrc/article/view/42336), их выходные данные не проверялись. Ещё найден SysML-подход А17.
- Как задержка обнаружения входит в А6 и А7 (отдельная экспоненциальная фаза или часть восстановления), по аннотациям установить нельзя. Нужен полный текст.

---

## Вопрос 2. Несовершенное покрытие, обнаружение и восстановление, ложные срабатывания, оптимизация параметров обнаружения

### Takeaway
Покрытие и задержка обнаружения давно входят в модели готовности (А1, А2, А4, А5), в том числе для ряда «восстанавливаемая система с этапом обнаружения» (А13, А14). Модель, где детектор **ложно объявляет отказ** и это добавляет простой, нашлась только вне моделей готовности — в детекторах аномалий (А8).

### Cited Findings

**А4.** Trivedi K., Wang D., Hunt D. J., Rindos A., Smith W. E., Vashaw B. Availability Modeling of SIP Protocol on IBM© WebSphere© // Proc. 14th IEEE Pacific Rim Int. Symp. on Dependable Computing (PRDC 2008). — IEEE, 2008. — P. 323–330. — DOI: 10.1109/PRDC.2008.50.
*Проверено: CrossRef; аннотация — OpenAlex.* Иерархическая модель готовности высокодоступного SIP-сервера приложений (телекоммуникационная служба!). По аннотации учтены **разные типы детекторов отказа, задержки обнаружения, задержки переключения**, перезапуски, перезагрузки, ремонт и **несовершенное покрытие обнаружения, переключения и восстановления**. Параметры взяты из эксплуатационных данных и HA-тестирования; для неопределённых параметров выполнен анализ чувствительности. Ближайший к статье классический образец «задержка обнаружения как параметр модели готовности телекоммуникационной службы»; ложных срабатываний в аннотации нет — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/prdc.2008.50).

**А5.** Matos R. D. S., Maciel P. R. M., Machida F., Kim D. S., Trivedi K. S. Sensitivity Analysis of Server Virtualized System Availability // IEEE Transactions on Reliability. — 2012. — Vol. 61, № 4. — P. 994–1006. — DOI: 10.1109/TR.2012.2220711.
*Проверено: CrossRef; аннотация — OpenAlex.* Марковские модели вознаграждения виртуализированной серверной системы (развитие [33]) и параметрический анализ чувствительности. Главный параметр для MTTF системы — интенсивность отказов узла, для готовности по производительности — интенсивность отказов приложений. Предложена стоимостная оптимизация — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tr.2012.2220711). Во фрагменте полного текста, выданном поиском, среднее время обнаружения отказа узла задано равным **30 с** («1/δh Mean time for host failure detection 30 sec»), то есть как константа — [ResearchGate](https://www.researchgate.net/publication/260632762_Sensitivity_Analysis_of_Server_Virtualized_System_Availability). Значение из фрагмента, по полному тексту не сверено.

**А8.** Goncalves C. F., Menasche D. S., Avritzer A., Antunes N., Vieira M. A Model-Based Approach to Anomaly Detection Trading Detection Time and False Alarm Rate // Proc. 2020 Mediterranean Communication and Computer Networking Conference (MedComNet). — IEEE, 2020. — P. 1–8. — DOI: 10.1109/MedComNet49392.2020.9191549.
*Проверено: CrossRef; аннотация — OpenAlex и arXiv:2006.08811 (https://arxiv.org/abs/2006.08811).* Аналитическая модель производительности и эксперименты используются для параметризации детектора аномалий по сигнатурам производительности в облачной (виртуализированной) среде. Метод позволяет **управлять долей ложных срабатываний**. Ключевая для статьи формулировка в названии: «компромисс между временем обнаружения и частотой ложных тревог». Проверка на нагрузке TPCx-V: точность (precision) 90–98 %. Готовность службы не моделируется — это опора для зависимости ν(T_o), а не для модели готовности.

**А13.** Kumar A., Shekhar C. Bayesian Modeling of Repairable Systems With Imperfect Coverage and Delayed Detection Dynamics // Quality and Reliability Engineering International. — 2025. — Vol. 41, № 4. — P. 1630–1641. — DOI: 10.1002/qre.3742.
*Проверено: CrossRef; аннотация — OpenAlex.* Двухблочная восстанавливаемая система с коэффициентом покрытия. Восстановление разбито на **две экспоненциальные фазы: обнаружение и локализация отказа, затем ремонт**; учтены перезагрузка и восстановление. Байесовская оценка: апостериорные распределения MTTF и стационарной готовности получены методом Монте-Карло. Новейшее продолжение линии [19]–[20]: задержка обнаружения — отдельная стадия с заданной интенсивностью, ложных срабатываний по аннотации нет — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1002/qre.3742).

**А14.** Na S., Bang S.-H. Repair policies of failure detection equipments and system availability // Communications for Statistical Applications and Methods. — 2022. — Vol. 29, № 2. — P. 151–160. — DOI: 10.29220/csam.2022.29.2.151.
*Проверено: CrossRef; аннотация — OpenAlex.* Система «основная система + средство обнаружения отказов». Средство обнаружения само может отказать, после чего отказ основной системы не обнаруживается. Для четырёх политик ремонта (последовательная, приоритетная, независимая, одновременная) построены марковские модели, стационарная готовность получена аналитически, приведён численный пример. Детектор вводится как самостоятельный отказывающий элемент модели готовности; ложные срабатывания не рассматриваются. Журнал корейский, индексируется в Scopus (по данным журнала, не проверено) — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.29220/csam.2022.29.2.151).

### Inferences
- Для статьи полезна связка: А4 (задержка обнаружения и покрытие в модели готовности телекоммуникационной службы) + А8 (компромисс «время обнаружения ↔ ложные тревоги» как известное явление) → отсутствие их объединения в модели готовности, где ν(T_o) добавляет простой. Это и есть вклад статьи.
- А13 и А14 показывают, что линия «repairable system with detection» активна в 2022–2025 гг. Ложные объявления отказа в ней по-прежнему не учитываются. Это дополнительное подтверждение разрыва к [19], [20].

### Gaps
- Целевой поиск по «false alarm» + «imperfect coverage» + «availability» в IEEE TR и RESS не дал работы, моделирующей ложные объявления отказа как источник простоя в марковской модели готовности (поисковые выдачи: https://dspace.bits-pilani.ac.in/items/0fe93004-d719-437c-a58d-a52c52281f2c ; https://www.emerald.com/insight/content/doi/10.1108/IJQRM-08-2021-0298/full/html). Это не доказательство отсутствия: в литературе по техническому обслуживанию (imperfect inspection, false positive) такие модели могут быть. Рекомендуемые запросы: «imperfect inspection false positive availability», «false alarm unnecessary failover availability».
- Работ, где тайм-аут или порог детектора оптимизируется **по критерию готовности**, а не по метрикам QoS детектора (T_D, λ_M), не найдено.

---

## Вопрос 3. Обзоры по моделированию надёжности и готовности виртуализированных сетей и облака

### Takeaway
Помимо уже имеющегося обзора [35] (Di Mauro et al., COMST 2026), есть проверенные обзоры по надёжности оркестратора NFV и по методам отказоустойчивости облака. В основной список они не вошли из-за лимита и вынесены в резерв (Р6, Р7).

### Cited Findings
- **Р6.** Gonzalez A. J., Nencioni G., Kamisinski A., Helvik B. E., Heegaard P. E. Dependability of the NFV Orchestrator: State of the Art and Research Challenges // IEEE Communications Surveys & Tutorials. — 2018. — Vol. 20, № 4. — P. 3307–3329. — DOI: 10.1109/COMST.2018.2830648. *Проверено: CrossRef. Аннотация не запрашивалась; содержание описано по названию.* Обзор надёжности оркестратора NFV — [CrossRef](https://api.crossref.org/works/10.1109/comst.2018.2830648).
- **Р7.** Mukwevho M. A., Celik T. Toward a Smart Cloud: A Review of Fault-Tolerance Methods in Cloud Systems // IEEE Transactions on Services Computing. — 2021. — Vol. 14, № 2. — P. 589–605. — DOI: 10.1109/TSC.2018.2816644. *Проверено: CrossRef (том 2021, ранний доступ 2018); аннотация — OpenAlex.* Классификация методов отказоустойчивости облака: реактивные, проактивные, «устойчивые» (resilient). Во втором классе время восстановления рассматривается как функция, подлежащая минимизации — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/tsc.2018.2816644).

### Inferences
- Для статьи (80–90 источников) достаточно одного обзора [35] и, при необходимости, Р6. Р7 ценен формулировкой «время восстановления как оптимизируемая функция».

### Gaps
- Свежего (2023–2026) обзора именно по моделированию готовности Kubernetes и контейнерных платформ не найдено.

---

## Вопрос 4. Классические основы (отсутствующие в 09-references.md)

### Takeaway
В списке уже есть учебник Trivedi 2001 [57] и Avizienis et al. [32], но нет первоисточников понятия «покрытие» и современной монографии Trivedi и Bobbio. Их стоит добавить.

### Cited Findings

**А1.** Arnold T. F. The Concept of Coverage and Its Effect on the Reliability Model of a Repairable System // IEEE Transactions on Computers. — 1973. — Vol. C-22, № 3. — P. 251–254. — DOI: 10.1109/T-C.1973.223703.
*Проверено: CrossRef; аннотация — OpenAlex.* Классическая работа о покрытии в **восстанавливаемой** дублированной системе. Показано, что даже малая доля «критических одиночных» (непокрытых) отказов резко снижает среднее время до отказа системы и увеличивает ожидаемый простой высоконадёжной системы. Прямой предшественник слагаемого «неидеальность обнаружения добавляет простой» в формуле статьи — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/t-c.1973.223703).

**А2.** Dugan J. B., Trivedi K. S. Coverage modeling for dependability analysis of fault-tolerant systems // IEEE Transactions on Computers. — 1989. — Vol. 38, № 6. — P. 775–787. — DOI: 10.1109/12.24286.
*Проверено: CrossRef; аннотация — OpenAlex.* Марковские, полумарковские, неоднородные марковские модели и расширенные стохастические сети Петри для вычисления коэффициента покрытия при постоянных, перемежающихся и переходных ошибках. Исследована чувствительность готовности к покрытию. Получен вывод: политика попытки переходного восстановления при обнаружении ошибки может **повышать** ненадёжность системы по сравнению с немедленной реконфигурацией — пример контринтуитивного влияния стратегии обработки обнаружения — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1109/12.24286).

**А3.** Trivedi K. S., Bobbio A. Reliability and Availability Engineering: Modeling, Analysis, and Applications. — Cambridge: Cambridge University Press, 2017. — DOI: 10.1017/9781316163047.
*Проверено: CrossRef (тип monograph, дата 3 августа 2017 г.); ISBN 9781107099500 — по рецензии в IJPE, DOI 10.23940/ijpe.19.04.p22.12631264. Число страниц и место издания по CrossRef **не подтверждены** (Cambridge — по издательству, проверить).* Современная монография: невосстанавливаемые и марковские модели, SPN/SRN, полумарковские процессы, PH-аппроксимация, иерархические модели. Стандартная ссылка на методологию марковских моделей готовности в дополнение к [57] — [OpenAlex](https://api.openalex.org/works/https://doi.org/10.1017/9781316163047).

### Inferences
- А1 + А2 + [19]/[20] + А13 образуют связную линию «покрытие и обнаружение в восстанавливаемых системах» с 1973 по 2025 г. Это удобно для обзорного абзаца статьи.

### Gaps
- Первоисточник понятия покрытия Bouricius et al. 1969 проверен (Р1), но в основной список не включён: для статьи достаточно А1.
- Классическую формулу готовности альтернирующего процесса восстановления (Kг = MTTF/(MTTF + MTTR)) обеспечивают [8], [17] и [57]; новый источник не нужен.

---

## Сводка основного списка (А1–А18)

| № | Работа | Год | Тип модели | T_o как параметр | Ложные срабатывания |
|---|---|---|---|---|---|
| А1 | Arnold, IEEE TC | 1973 | Марковская, покрытие | нет (покрытие) | нет |
| А2 | Dugan, Trivedi, IEEE TC | 1989 | Марковская, полумарковская, ESPN | обработка ошибки | нет |
| А3 | Trivedi, Bobbio, CUP | 2017 | монография | — | — |
| А4 | Trivedi et al., PRDC | 2008 | иерархическая, готовность SIP | **да (задержки обнаружения, анализ чувствительности)** | нет (по аннотации) |
| А5 | Matos et al., IEEE TR | 2012 | MRM, чувствительность | константа 30 с (фрагмент) | нет |
| А6 | Sakic, Kellerer, IEEE TNSM | 2018 | SAN → CTMC, RAFT SDN | не установлено | не установлено |
| А7 | Tola, Nencioni, Helvik, IEEE TNSM | 2019 | сечения + SAN, NFV | нет данных | нет |
| А8 | Goncalves et al., MedComNet | 2020 | модель детектора аномалий | **да (компромисс)** | **да** |
| А9 | Sebastio et al., IEEE TSC | 2021 (ранний доступ 2018) | FT + SRN, контейнеры | нет данных | нет |
| А10 | Di Mauro et al., IEEE TNSM | 2021 | SRN + RBD, cIMS | нет данных | нет |
| А11 | Tola, Jiang, Helvik, IEEE TNSM | 2021 | SAN, NFV-MANO + омоложение | компромисс по интервалу омоложения | нет |
| А12 | Di Mauro et al., IEEE TDSC | 2022 | M/G/c + SRN, softIMS | нет данных | нет |
| А13 | Kumar, Shekhar, QREI | 2025 | Марковская, байесовская, покрытие | фаза обнаружения (заданная) | нет |
| А14 | Na, Bang, CSAM | 2022 | Марковская, отказы детектора | нет | нет |
| А15 | Bai et al., IEEE TDSC | 2023 | полумарковская, SFC MEC | нет данных | нет |
| А16 | Bai et al., IEEE TSC | 2023 | полумарковская, оптимизация интервалов | оптимум интервала омоложения | нет |
| А17 | Hecht, Agena, RAMS | 2024 | SysML, Kubernetes | параметры из хаос-тестов | нет данных |
| А18 | Mandal, IEEE TSC | 2025 | аналитическая, 4G/5G VNF | нет | нет |

«Нет данных» означает, что аннотация вопрос не освещает. Для А6, А7, А9–А12, А15, А17 детальную роль задержки обнаружения нужно сверить по полному тексту.

## Резерв (выходные данные подтверждены по CrossRef; включать при нехватке)

- **Р1.** Bouricius W. G., Carter W. C., Schneider P. R. Reliability modeling techniques for self-repairing computer systems // Proc. 1969 24th National Conference (ACM '69). — ACM, 1969. — P. 295–309. — DOI: 10.1145/800195.805940. Первоисточник понятия покрытия.
- **Р2.** Amari S. V., Dugan J. B., Misra R. B. A separable method for incorporating imperfect fault-coverage into combinatorial models // IEEE Transactions on Reliability. — 1999. — Vol. 48, № 3. — P. 267–274. — DOI: 10.1109/24.799898.
- **Р3.** Longo F., Distefano S., Bruneo D., Scarpa M. Dependability modeling of Software Defined Networking // Computer Networks. — 2015. — Vol. 83. — P. 280–296. — DOI: 10.1016/j.comnet.2015.03.018. *Аннотация не получена (ScienceDirect вернул 403, в OpenAlex её нет); содержание не сверено.*
- **Р4.** Nencioni G., Helvik B. E., Heegaard P. E. Including Failure Correlation in Availability Modeling of a Software-Defined Backbone Network // IEEE Transactions on Network and Service Management. — 2017. — Vol. 14, № 4. — P. 1032–1045. — DOI: 10.1109/TNSM.2017.2755462. Двухуровневая модель (минимальные сечения + SAN) с корреляцией отказов, анализ чувствительности на национальной магистральной сети (аннотация — OpenAlex).
- **Р5.** Nencioni G., Helvik B. E., Gonzalez A. J., Heegaard P. E., Kamisinski A. Availability Modelling of Software-Defined Backbone Networks // Proc. 46th IEEE/IFIP DSN Workshops (DSN-W). — IEEE, 2016. — P. 105–112. — DOI: 10.1109/DSN-W.2016.28. По поисковой выдаче: высокая интенсивность отказов эксплуатации и обслуживания может снизить готовность SDN до порядка величины по сравнению с традиционной сетью (не сверено по тексту).
- **Р6, Р7** — см. вопрос 3.
- **Р8.** Ghosh R., Longo F., Frattini F., Russo S., Trivedi K. S. Scalable Analytics for IaaS Cloud Availability // IEEE Transactions on Cloud Computing. — 2014. — Vol. 2, № 1. — P. 57–70. — DOI: 10.1109/TCC.2014.2310737.
- **Р9.** Kulkarni S. G., Liu G., Ramakrishnan K. K., Arumaithurai M., Wood T., Fu X. REINFORCE: Achieving Efficient Failure Resiliency for Network Function Virtualization-Based Services // IEEE/ACM Transactions on Networking. — 2020. — Vol. 28, № 2. — P. 695–708. — DOI: 10.1109/TNET.2020.2969961. Механизм отказоустойчивости NFV, не модель готовности; содержание не сверено.
- **Р10.** Vizarreta P., Heegaard P., Helvik B., Kellerer W., Machuca C. M. Characterization of failure dynamics in SDN controllers // Proc. 9th Int. Workshop on Resilient Networks Design and Modeling (RNDM). — IEEE, 2017. — P. 1–7. — DOI: 10.1109/RNDM.2017.8093037.
- **Р11.** Tola B., Jiang Y., Helvik B. E. On the Resilience of the NFV-MANO: An Availability Model of a Cloud-native Architecture // Proc. 16th Int. Conf. on the Design of Reliable Communication Networks (DRCN 2020). — IEEE, 2020. — P. 1–7. — DOI: 10.1109/DRCN48652.2020.1570604378.
- **Р12.** Xiong N., Vasilakos A. V., Wu J., Yang Y. R., Rindos A., Zhou Y., Song W.-Z., Pan Y. A Self-tuning Failure Detection Scheme for Cloud Computing Service // Proc. IEEE 26th Int. Parallel and Distributed Processing Symp. (IPDPS). — IEEE, 2012. — P. 668–679. — DOI: 10.1109/IPDPS.2012.126. Автонастройка параметров детектора отказов облака под требования QoS (аннотация — OpenAlex). Может пересекаться с направлением `failure_detectors.md`.
- **Р13.** Turchetti R. C., Duarte E. P., Arantes L., Sens P. A QoS-configurable failure detection service for internet applications // Journal of Internet Services and Applications. — 2016. — Vol. 7, № 1. — Article 9. — DOI: 10.1186/s13174-016-0051-y. Содержание не сверено.
- **Р14.** Hecht M. Software Reliability and Availability Testing of a Kubernetes Cluster // Proc. 2026 Annual Reliability and Maintainability Symposium (RAMS). — IEEE, 2026. — P. 1–6. — DOI: 10.1109/RAMS50514.2026.11424466. Измерение времени и вероятности восстановления в Kubernetes средствами LitmusChaos как входа модели готовности (аннотация — OpenAlex).
- **Р15.** Bertier M., Marin O., Sens P. Implementation and performance evaluation of an adaptable failure detector // Proc. Int. Conf. on Dependable Systems and Networks (DSN 2002). — IEEE, 2002. — P. 354–363. — DOI: 10.1109/DSN.2002.1028920. *Год по CrossRef не возвращён, 2002 — по названию конференции (DSN 2002); в `failure_detectors.md` Bertier упоминается как объект сравнения, отдельной позицией не внесён.*
