# Проверка опубликованных измерений для параметров модели готовности (λ / T_н, T_о, T_р, p) и дополнительные источники

Дата проверки: 6 ноября 2026 г. Все значения ниже выписаны из полных текстов (PDF извлечён `pdftotext`), если не оговорено иное. Выходные данные сверены по CrossRef (`api.crossref.org`); DBLP из текущей среды недоступен (защита Anubis), поэтому DBLP-ключи не перепроверялись.

Сводка статусов:

| № | Источник | Статус |
|---|---|---|
| 1 | Vayghan et al., arXiv:1901.04946 | **CONFIRMED** по числам; **DIFFERS** по трём интерпретациям (смысл 0,028 с; «carrier-grade» = OpenSAF в схеме *No-Redundancy* с резервным экземпляром; отказ узла имитирован командой `reboot`). Рецензируемой версии нет |
| 2 | Roberts, Archibald, Trinder, arXiv:2507.02158 | Числа **CONFIRMED**; **DIFFERS** по смыслу: измерен отказ *контейнера*, а не узла; 4 % — относительно SKI, а не «по сравнению с отсутствием отказа»; время округлено до 1 с. Рецензируемой версии не найдено |
| 3 | Schroeder, Gibson, DSN 2006 | 23 000 / 4750 / 9 лет — **CONFIRMED**; деление 0,54 отказа/узел·год — **методически некорректно** (большинство узлов работало 2–4 года, не 9) |
| 4 | Guo et al., Pingmesh, SIGCOMM 2015 | ≈10⁻⁵ — **CONFIRMED** (внутри модуля; общий диапазон 10⁻⁴–10⁻⁵); «≈10⁻³ для десятков мс» — **CONFIRMED как вывод** из P99.9, сами авторы так не формулируют |
| 5 | Ben Hassan, Mansour, Procedia CS 2024 | Выходные данные **CONFIRMED**; числа 50 мс / 1–1,57 с / 3,48–5 с — **NOT VERIFIED** (полный текст из среды недоступен, 403) |
| 6 | Таймеры Kubernetes | **DIFFERS**: `node-monitor-grace-period` = **50 с начиная с v1.32** (было 40 с); `--pod-eviction-timeout` **удалён в v1.27**; 300 с — `tolerationSeconds`; lease 10 с / 40 с — CONFIRMED |

---

## 1. Vayghan L. A. et al. «Kubernetes as an Availability Manager for Microservice Applications» (arXiv:1901.04946)

### Takeaway
Все числовые значения, приведённые в диссертации, совпадают с таблицами I–V полного текста. Но 0,028 с — это не время перенаправления трафика в смысле T_р (запрограммированные правила на узлах), а интервал от пометки узла NotReady до удаления IP экземпляра из объекта Endpoints по журналам; значение 3,346 с относится к OpenSAF в схеме, которую авторы называют *No-Redundancy* (активный + запасной экземпляр, создаваемый при отказе), и взято из более ранней работы авторов. Рецензируемой публикации именно этой статьи не найдено.

### Cited Findings
- Стенд (разд. III): «This cluster is composed of three VMs running on OpenStack cloud. Ubuntu 16.04 … Kubernetes 1.8.2 runs on all VMs and the container engine is Docker 17.09»; NTP для синхронизации; приложение VLC. По рис. 5: Master + Node 1 + Node 2. — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- Повторности (разд. III): «Each scenario has been repeated 10 times and the average of the measurements are shown in Table I through Table V. All the measurements reported in this paper are in seconds.» — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- Определения (разд. III, рис. 4): Reaction — от внесения отказа до первой реакции Kubernetes; Repair — от первой реакции до восстановления отказавшего экземпляра; Recovery — от первой реакции до восстановления обслуживания; Outage = Reaction + Recovery. — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Способ внесения отказа узла (разд. IV.A):** «a node failure is simulated by the Linux's reboot command on a VM hosting the pod»; узел помечается not ready «after the fourth missed status update». — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Табл. I (No-Redundancy, default), Reaction / Repair / Recovery / Outage, с:** VLC Container 0.716 / 0.472 / 1.050 / 1.766; Pod Container 0.496 / 32.570 / 31.523 / 32.019; **Node Failure 38.187 / 262.542 / 262.665 / 300.852**. — CONFIRMED. [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Табл. II (N-Way Active, default):** Pod Container 0.696 / 30.986 / **0.034** / 0.730; **Node Failure 38.554 / 262.178 / 0.028 / 38.582** (строка VLC Container: outage 0.579). — CONFIRMED. [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Смысл Recovery при N-Way Active и отказе узла (разд. IV.B):** «The recovery time is when the IP of Pod1 is removed from the endpoints list»; реакция — «the time the master marks the node as not ready and schedules the pod for termination». То есть 0,028 с = интервал «узел NotReady → IP удалён из Endpoints», измеренный по меткам времени журналов Kubernetes/Docker/systemd (разд. V, Construct Validity), а не на стороне клиента и не до момента применения правил iptables на узлах. — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Табл. III (most responsive, отказ Pod Container):** No-Redundancy 0.708 / 3.039 / 3.337 / 4.045; N-Way Active 0.521 / 3.008 / 0.032 / 0.554. — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Табл. IV (most responsive, отказ узла):** No-Redundancy 0.976 / 2.791 / 2.998 / **3.974**; N-Way Active 0.849 / 2.173 / **0.022** / **0.872**. — CONFIRMED. [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- Настройка «most responsive» (разд. IV.C): kubelet «post the node's status every second», node controller «read the updated statuses every second and only allow one missed status update»; «configuration parameters related to handling node failure are set to the lowest value possible (one second)». Конкретные имена флагов в статье не названы. — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- Оговорка авторов (разд. IV.C): «We are aware of the network overhead and potential false node failure reports for the most responsive configuration». — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- **Табл. V (OpenSAF):** VLC Process 0.650 / – / 0.145 / 0.795; VM Failure 3.233 / – / 0.123 / 3.351; **Physical Host Failure 3.229 / – / 0.118 / 3.346**. Условия (разд. IV.D): «In the experiments with OpenSAF we used a No-redundancy redundancy model with two VLC applications, one active and the other one as a spare to be instantiated and take over in case of failure of the active»; результаты взяты из более ранней работы авторов («In [20] we conducted a set of experiments»). — [arXiv PDF](https://arxiv.org/pdf/1901.04946)
- arXiv: только v1 от 15.01.2019; поле Comments: «paper submitted to Journal of Network and Computer Applications»; Journal-ref отсутствует; DOI arXiv 10.48550/arXiv.1901.04946; класс cs.SE. — [arXiv abs](https://arxiv.org/abs/1901.04946)
- Поиск CrossRef по названию не находит журнальной версии; находятся родственные рецензируемые работы той же группы: (а) Abdollahi Vayghan L., Saied M. A., Toeroe M., Khendek F. Deploying Microservice Based Applications with Kubernetes: Experiments and Lessons Learned // 2018 IEEE 11th Int. Conf. on Cloud Computing (CLOUD). — 2018. — P. 970–973. — DOI 10.1109/CLOUD.2018.00148; (б) … Microservice Based Architecture: Towards High-Availability for Stateful Applications with Kubernetes // 2019 IEEE 19th Int. Conf. on Software Quality, Reliability and Security (QRS). — 2019. — P. 176–185. — DOI 10.1109/QRS.2019.00034; (в) … A Kubernetes controller for managing the availability of elastic microservice based stateful applications // Journal of Systems and Software. — 2021. — Vol. 175. — Art. 110924. — DOI 10.1016/j.jss.2021.110924. — [CrossRef API](https://api.crossref.org/works?query.bibliographic=Kubernetes+as+an+Availability+Manager+for+Microservice+Applications+Vayghan)

**Проверенная запись:** Abdollahi Vayghan L., Saied M. A., Toeroe M., Khendek F. Kubernetes as an Availability Manager for Microservice Applications [Электронный ресурс] : preprint. — 2019. — arXiv:1901.04946 [cs.SE]. — DOI: 10.48550/arXiv.1901.04946. — URL: https://arxiv.org/abs/1901.04946 (Фамилия первого автора в оригинале — «Abdollahi Vayghan», так её даёт и CrossRef для работ 2018–2021 гг.; форма «Vayghan L. A.» неточна.)

### Inferences
- Расхождение 0,028 с (источник) против T_р = 1,12 с (Э1) объяснимо по определению: в источнике интервал закрывается удалением адреса из объекта Endpoints на управляющем узле, а не применением правил kube-proxy на всех узлах и не восстановлением потока у клиента. Утверждение «столбец Recovery есть прямое измерение T_р» (09-references.md, [13]) следует смягчить: это измерение **управляющей части** T_р (от решения до обновления Endpoints), без распространения на узлы.
- Значение 3,346 с нельзя подавать как «carrier-grade менеджер при резервировании N-Way Active»: схема OpenSAF — активный + запасной, отказ «физического хоста», результаты из другой работы; повторности для табл. V в статье не указаны.
- Отказ узла через `reboot` — это корректное завершение ОС, а не снятие питания; при `reboot` kubelet может успеть часть действий. Для сопоставления с Э1 (снятие питания через BMC, ForceOff) это нужно оговорить.
- Для списка ВАК: самой статьи в рецензируемом виде нет; при необходимости рецензируемой опоры ссылаться на CLOUD 2018 (DOI 10.1109/CLOUD.2018.00148) — по аннотации arXiv это «preliminary work» с конфигурацией по умолчанию, но **полный текст CLOUD 2018 не сверялся** и номера измерений из него не брать.

### Gaps
- Полный текст CLOUD 2018 и [20] (источник табл. V) не получены — какое именно число повторностей и стенд у OpenSAF, неизвестно.
- Kubernetes 1.8.2 использовал обновления статуса узла (до появления Lease-механизма по умолчанию); перенос 38 с на текущие версии некорректен без оговорки.

---

## 2. Roberts J., Archibald B., Trinder P. «Signalling Health for Improved Kubernetes Microservice Availability» (arXiv:2507.02158)

### Takeaway
Числа 0,1 с, 86 %, 99 %, 8,7 с, 4 %, Kubernetes 1.27.8, один узел, 30 повторностей, SockShop — подтверждены. Но работа измеряет **обнаружение отказа контейнера (процесса) пробами kubelet**, а не отказа узла; это не источник для T_о обнаружения отказа узла. Рецензируемой версии не найдено (на 06.11.2026 только arXiv v1).

### Cited Findings
- Аннотация: SCM «detects container failure 86% faster than PCM … We find PCM can erroneously detect failures, and this reduces service availability by 4%». — [arXiv abs](https://arxiv.org/abs/2507.02158)
- Стенд (разд. VI.A): «Experiments are executed on a 1-node Kubernetes v1.27.8 cluster using CRI-O v1.27.1 hosted on an Ubuntu 20.04 virtual machine with 32GB RAM and 8 vCPUs»; нагрузка Locust, ограничена 100 запросами/с; сервис catalogue из SockShop. — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- Повторности (разд. VI.A): «Each test configuration is run thirty times. Times are measured to the nearest second because the shortest permitted probe interval is 1s». — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- Внесение отказа: «Container failure is induced by terminating the HTTP request-handling process, the catalogue program, 60s after Locust starts». — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- **Табл. IV (время до постановки перезапуска в очередь = время обнаружения отказа; затем время до запуска), среднее ± СКО, с:** Default Probes **8.7 ± 0.5** / 38.9 ± 0.3; Fast Probes **0.7 ± 0.5** / 2.9 ± 0.5; SKI **0.1 ± 0.3** / 2.2 ± 0.4. Текст разд. VI.D: «SKI detects failure in 0.1s, 0.6s (86%) faster than FP and 8.6s (99%) faster than DP». — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- Параметры проб (разд. IV.C, VI.A): у FP интервал 1 с, «marking the catalogue container Unhealthy after one failed liveness probe instead of the default three», grace period 2 с; модель для DP: «Tl,p ≈ (3−1/2)3s+0.2s ≈ 7.7s. This is 1s lower than the 8.7s measured in Table IV» — т. е. у DP период 3 с, порог 3. — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- Модель времени обнаружения при опросе: Tl,p ≈ (N − 1/2)·I + L — та же форма, что формула (3.16) диссертации T_о = (k − ½)τ. — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- **Табл. VI (накопленное число Ready-подов за 290 с):** No Failure 291 (0 %); Default Probes 80 (−211, 73 %); Fast Probes 274 (−17, 6 %); SKI 286 (−5, 2 %). Текст разд. VI.E: «Availability under FP is 274 Pods, 12 Pods (4%) lower than SKI, which we attribute to the additional container restarts»; при FP контейнер перезапускался «between 2 and 6 times with a mean of 3 ± 1 restarts»; причина — «failing liveness probes». — [arXiv PDF](https://arxiv.org/pdf/2507.02158)
- Версии arXiv: только v1 от 2 июля 2025; Comments «10 pages, 7 figures»; Journal-ref отсутствует; DOI arXiv 10.48550/arXiv.2507.02158; лицензия CC BY 4.0. — [arXiv abs](https://arxiv.org/abs/2507.02158)
- Поиск по названию в CrossRef (6.11.2026) записей с этим названием не вернул. — [CrossRef API](https://api.crossref.org/works?query.bibliographic=Signalling%20Health%20Improved%20Kubernetes%20Microservice%20Availability)

**Проверенная запись:** Roberts J., Archibald B., Trinder P. Signalling Health for Improved Kubernetes Microservice Availability [Электронный ресурс] : preprint. — 2025. — arXiv:2507.02158 [cs.DC]. — DOI: 10.48550/arXiv.2507.02158. — URL: https://arxiv.org/abs/2507.02158

### Inferences
- «Частый опрос снижает доступность на 4 %» корректно только как «на 4 % ниже, чем при сигнальном контроле (274 против 286)»; относительно работы без отказа снижение при FP — 6 %. Мера «доступности» здесь — накопленный счёт Ready-подов по выборкам, а не коэффициент готовности.
- 0,1 ± 0,3 с — среднее по величинам, округлённым до целой секунды; как параметр T_о оно годится только как порядок величины.
- В 09-references.md ([3]) текст «0,1 с против 0,7 с … и 8,7 с» корректен; но оговорка «отказ контейнера на одном узле, а не узла» обязательна. Ложные срабатывания здесь — от liveness-проб при медленном старте/нагрузке, т. е. качественное подтверждение члена ложных срабатываний модели, но не измерение p.

### Gaps
- Рецензируемая версия: не найдена (DBLP недоступен из среды; проверить по DBLP/IEEE Xplore вручную; возможна публикация на конференции 2025–2026 гг.).

---

## 3. Schroeder B., Gibson G. A. «A Large-Scale Study of Failures in High-Performance Computing Systems» (DSN 2006)

### Takeaway
23 000 отказов, 4750 узлов, 9 лет — подтверждено дословно. Но 23 000 / (4750 × 9) = 0,54 отказа/узел·год систематически занижает интенсивность: по табл. 1 подавляющее большинство узлов (системы типов E и F) введено в эксплуатацию в 2001–2003 гг. и наблюдалось 2–4 года, а не 9; кроме того, «узел» здесь — SMP/NUMA-машина от 2 до 256 процессоров с сильно различающейся частотой отказов.

### Cited Findings
- Аннотация: «The data has been collected over the past 9 years at Los Alamos National Laboratory and includes 23000 failures recorded on more than 20 different systems, mostly large clusters of SMP and NUMA nodes»; «average failure rates differ wildly across systems, ranging from 20–1000 failures per year, and that time between failures is modeled well by a Weibull distribution with decreasing hazard rate». — [Полный текст, сайт автора](https://www.cs.cmu.edu/~bianca/dsn06.pdf)
- Разд. 1: «covers 22 high-performance computing (HPC) systems, including a total of 4750 machines and 24101 processors». Разд. 2.1: «22 high-performance computing systems that have been in production use at LANL between 1996 and November 2005 … In total the systems include 4750 nodes and 24101 processors». Разд. 2.3: сбор ведётся с июня 1996 г.; запись — каждый отказ, «that required the attention of a system administrator». — [PDF](https://www.cs.cmu.edu/~bianca/dsn06.pdf)
- Табл. 1 (стр. 2): системы 5–12 (тип E, 4 проц./узел) и 13–18 (тип F, 2 проц./узел) — ввод в эксплуатацию с 09/01–12/01 (системы 5–6), 05/02–10/02 (7–8) и 09/03 (9–18); NUMA-системы 19–22 — 16–128 процессоров на узел, часть с 1996–1997 гг. — [PDF](https://www.cs.cmu.edu/~bianca/dsn06.pdf)
- Разд. 5.1: годовая частота по системам — «ranging from only 17 failures per year for system 2, to an average of 1159 failures per year for system 7» (расхождение с округлённым «20–1000» аннотации); нормированная на процессор частота различается между системами значительно меньше; распределение отказов по узлам не пуассоновское (рис. 3: узлы 21–23 системы 20 — 6 % узлов, 20 % отказов). — [PDF](https://www.cs.cmu.edu/~bianca/dsn06.pdf)
- Время восстановления (разд. 6): среднее по всем отказам «close to 6 hours». — [PDF](https://www.cs.cmu.edu/~bianca/dsn06.pdf)
- Выходные данные по CrossRef: DSN'06, P. 249–258, DOI 10.1109/DSN.2006.5. Журнальная версия: IEEE Transactions on Dependable and Secure Computing, 2010, Vol. 7, № 4, P. 337–350, DOI 10.1109/TDSC.2009.4. — [CrossRef API](https://api.crossref.org/works?query.bibliographic=Large-Scale+Study+of+Failures+in+High-Performance+Computing+Systems+Schroeder+Gibson)

**Проверенные записи:**
- Schroeder B., Gibson G. A. A large-scale study of failures in high-performance computing systems // Proc. Int. Conf. on Dependable Systems and Networks (DSN'06). — Philadelphia, PA : IEEE, 2006. — P. 249–258. — DOI: 10.1109/DSN.2006.5.
- Schroeder B., Gibson G. A. A Large-Scale Study of Failures in High-Performance Computing Systems // IEEE Transactions on Dependable and Secure Computing. — 2010. — Vol. 7, № 4. — P. 337–350. — DOI: 10.1109/TDSC.2009.4. (Журнальная версия — содержание не сверялось.)

### Inferences
- Арифметика 23 000/(4750·9) = 0,538 верна, но знаменатель (42 750 узло-лет) завышен в 2–4 раза для ~95 % узлов (системы 5–18, ≈4,5 тыс. узлов, наблюдались ≈2–4 года). Поэтому 0,54 — нижняя граница λ, а T_н ≈ 1,9 года — верхняя граница; в 09-references.md это названо («оценка верхняя»), но порядок завышения стоит указать. Точное значение по узло-годам требует исходных данных LANL (опубликованы авторами), в статье не приводится.
- В счёт входят отказы любой природы (аппаратные, программные, сеть, человеческий фактор), требовавшие вмешательства администратора — это ближе к «отказу узла» модели, чем аппаратные AFR (см. п. 7).

### Gaps
- Точная интенсивность «на узел-год» по каждой системе в тексте не приведена (только графики рис. 2а/2б).

---

## 4. Guo C. et al. «Pingmesh» (ACM SIGCOMM 2015)

### Takeaway
Доля потерь ≈10⁻⁵ подтверждается для потерь внутри модуля (pod); между модулями — до 7,63·10⁻⁵, общий нормальный диапазон авторы дают как 10⁻⁴–10⁻⁵. «Вероятность превышения задержкой десятков мс ≈10⁻³» — корректное прочтение P99.9 = 23,35 мс (DC1) и 11,07 мс (DC2), но само выражение «вероятность» в статье не используется. Значение 10⁻³ в статье есть также как **порог тревоги** по потерям — не путать.

### Cited Findings
- **Табл. 1 (стр. 144), доля потерь intra-pod / inter-pod:** DC1 (US West) 1.31×10⁻⁵ / 7.55×10⁻⁵; DC2 (US Central) 2.10×10⁻⁵ / 7.63×10⁻⁵; DC3 (US East) 9.58×10⁻⁶ / 4.00×10⁻⁵; DC4 (Europe) 1.52×10⁻⁵ / 5.32×10⁻⁵; DC5 (Asia) 9.82×10⁻⁶ / 1.54×10⁻⁵. — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- Разд. 4.2 (стр. 145): «the packet drop rates are in the range of 10−4 − 10−5 … we find the drop rate is in this range unless network incidents happen»; «the intra-pod drop rate is around 10−5, which is larger than we have expected». — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- Метод оценки потерь (разд. 4.2): «Pingmesh does not directly measure packet drop rate» — оценка по повторной передаче TCP SYN: (зонды с RTT ≈3 с + зонды с RTT ≈9 с) / число успешных зондов. — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- **Задержка (разд. 4.1, стр. 144):** «At P99.9, the inter-pod latencies are 23.35ms and 11.07ms for DC1 and DC2, respectively. At P99.99, the inter-pod latencies become 1397.63ms and 105.84ms»; P50/P99 intra-pod и inter-pod для DC1 — (216 us, 1.26 ms) и (268 us, 1.34 ms); измеряется RTT TCP SYN/SYN-ACK без полезной нагрузки; данные одного «normal working day». — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- Пример сервиса за неделю (разд. 4.3): потери «around 4 × 10−5», P99 «500-560us»; порог тревоги: «If the packet drop rate is greater than 10−3 or the 99th percentile latency is larger than 5ms, we will categorize this as a network problem». — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- Ограничение зондирования (разд. 3): «The minimum probe interval between any two servers is limited to 10 seconds». — [SIGCOMM PDF](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf)
- Выходные данные (CrossRef): Proc. 2015 ACM Conf. on Special Interest Group on Data Communication (SIGCOMM '15), P. 139–152, DOI 10.1145/2785956.2787496; дублирующая публикация: ACM SIGCOMM Computer Communication Review, 2015, Vol. 45, № 4, P. 139–152, DOI 10.1145/2829988.2787496. — [CrossRef API](https://api.crossref.org/works?query.bibliographic=Pingmesh+Large-Scale+System+Data+Center+Network+Latency+Measurement)

**Проверенная запись:** Guo C., Yuan L., Xiang D., Dang Y., Huang R., Maltz D., Liu Z., Wang V., Pang B., Chen H., Lin Z.-W., Kurien V. Pingmesh: A Large-Scale System for Data Center Network Latency Measurement and Analysis // Proc. ACM SIGCOMM 2015. — London : ACM, 2015. — P. 139–152. — DOI: 10.1145/2785956.2787496.

### Inferences
- Для p: P(RTT > 23,35 мс) ≈ 10⁻³ в DC1 и P(RTT > 11,07 мс) ≈ 10⁻³ в DC2 — вывод из определения процентиля, корректный; формулировать как «по данным [Pingmesh], 99,9-й процентиль RTT составил 11–23 мс, т. е. …». Зависимость сильно различается между ЦОД: P99.99 — 1,4 с в DC1, но 0,106 с в DC2; утверждение «10⁻⁴ при 1,4 с» верно только для DC1.
- RTT включает обработку SYN ядром удалённого сервера; для сообщений контроля работоспособности уровня приложения (kubelet → API) хвост будет хуже.

### Gaps
- Распределение задержки для меж-ЦОД каналов в статье не приводится.

---

## 5. Ben Hassan A., Mansour M. «Performance Evaluation of BFD over VRRP» (Procedia CS 2024)

### Takeaway
Выходные данные подтверждены по CrossRef (т. 251, с. 256–264, 2024, DOI 10.1016/j.procs.2024.11.108; открытый доступ, CC BY-NC-ND). Числа 50 мс, 1–1,57 с и 3,48–5 с **повторно проверить не удалось**: ScienceDirect возвращает 403 для автоматических запросов, API Elsevier полный текст не отдаёт. Аннотация подтверждает предмет: PNETLAB, сравнение времени сходимости, потерь, загрузки ЦП и полосы.

### Cited Findings
- CrossRef: «Performance Evaluation of Bidirectional Forwarding Detection (BFD) over the Virtual Router Redundancy Protocol (VRRP)», Procedia Computer Science, vol. 251, pp. 256–264, 2024; авторы в записи: given «A.Ben», family «Hassan»; «M.» «Mansour»; PII S1877050924033428. — [CrossRef](https://api.crossref.org/works/10.1016/j.procs.2024.11.108)
- OpenAlex: лицензия cc-by-nc-nd, publishedVersion; аффилиация обоих авторов — University of Tripoli; аннотация: «we implemented BFD with VRRP to reduce downtime … The comparison was made based on convergence time, packet loss, CPU usage, and bandwidth consumption. PNETLAB emulation used in this work». — [OpenAlex](https://api.openalex.org/works/doi:10.1016/j.procs.2024.11.108)
- Попытки чтения полного текста: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1877050924033428) — HTTP 403.

**Проверенная запись (по CrossRef):** Ben Hassan A., Mansour M. Performance Evaluation of Bidirectional Forwarding Detection (BFD) over the Virtual Router Redundancy Protocol (VRRP) // Procedia Computer Science. — 2024. — Vol. 251. — P. 256–264. — DOI: 10.1016/j.procs.2024.11.108.

### Inferences
- Форма фамилии неоднозначна: CrossRef кодирует «Hassan, A.Ben», OpenAlex связывает с профилем «Alzubair Hassan». Сверить по титулу статьи (вероятно, «Ben Hassan» — составная фамилия).
- Работа — эмуляция (PNETLAB), а не измерение на оборудовании; при ссылке так и указывать.

### Gaps
- Числа 50 мс / 1–1,57 с / 3,48–5 с, интервалы BFD и таймеры VRRP, название конференции — **сверить вручную в браузере** (статья в открытом доступе). В 09-references.md ([65]) утверждается, что содержание сверено по полному тексту; независимо это не подтверждено.

---

## 6. Значения по умолчанию таймеров отказа узла в Kubernetes

### Takeaway
**`node-monitor-grace-period` по умолчанию = 50 с начиная с Kubernetes v1.32** (ранее 40 с). Флаг `--pod-eviction-timeout` удалён в v1.27; вытеснение после 300 с определяется `tolerationSeconds` = 300 у допусков `not-ready`/`unreachable`, которые добавляет контроллер допуска DefaultTolerationSeconds. Пульс узла — обновление Lease каждые 10 с (длительность Lease 40 с); `.status` при неизменном состоянии передаётся раз в 5 мин. Итог «обнаружение + вытеснение» в текущих версиях ≈ 50 + 300 = 350 с (ранее 340 с).

### Cited Findings
- kube-controller-manager (документация v1.37, текущая): «--node-monitor-grace-period duration Default: 50s — Amount of time which we allow running Node to be unresponsive before marking it unhealthy. Must be N times more than kubelet's nodeStatusUpdateFrequency …»; «--node-monitor-period Default: 5s»; «--node-startup-grace-period Default: 1m0s». Флага `--pod-eviction-timeout` на странице нет. — [kubernetes.io kube-controller-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/); исходник: [GitHub kubernetes/website](https://github.com/kubernetes/website/blob/main/content/en/docs/reference/command-line-tools-reference/kube-controller-manager.md)
- CHANGELOG v1.32.0 (и v1.32.0-alpha.1): «The default value for node-monitor-grace-period has been increased to 50s (earlier 40s) (Ref - kubernetes/kubernetes#121793) (#126287)». — [CHANGELOG-1.32](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.32.md)
- CHANGELOG v1.26: «CLI flag `pod-eviction-timeout` is deprecated and will be removed together with `enable-taint-manager` in v1.27» (#113710); CHANGELOG v1.27: «Remove deprecated `--enable-taint-manager` and `--pod-eviction-timeout` CLI flags» (#115840). — [CHANGELOG-1.26](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.26.md); [CHANGELOG-1.27](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.27.md)
- kube-apiserver: «--default-not-ready-toleration-seconds int Default: 300»; «--default-unreachable-toleration-seconds int Default: 300 — Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration». — [kube-apiserver reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
- Node status (Conditions): «`Unknown` if the node controller has not heard from the node in the last `node-monitor-grace-period` (default is 50 seconds)»; «NodeMonitorGracePeriod, which defaults to 50 seconds. This will cause either an `node.kubernetes.io/unreachable` taint …». **Но в разделе Heartbeats той же страницы сохранилось: «… 5 minutes, which is much longer than the 40 second default timeout for unreachable nodes»** — внутреннее противоречие документации. — [Node Status](https://kubernetes.io/docs/reference/node/node-status/)
- Heartbeats: «The kubelet creates and then updates its Lease object every 10 seconds (the default update interval) … If the Lease update fails, the kubelet retries, using exponential backoff that starts at 200 milliseconds and capped at 7 seconds»; «The default interval for `.status` updates to Nodes is 5 minutes». — [Node Status](https://kubernetes.io/docs/reference/node/node-status/)
- KubeletConfiguration v1beta1: `nodeStatusUpdateFrequency` Default "10s" («frequency that kubelet computes node status and checks if an update to the API server is necessary»); `nodeStatusReportFrequency` Default "5m"; `nodeLeaseDurationSeconds` Default 40 («The lease is currently renewed every 10s, per KEP-0009»). — [Kubelet Configuration (v1beta1)](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/)
- Nodes: «By default, the node controller waits 5 minutes between marking the node as `Unknown` and submitting the first eviction request»; «By default, the node controller checks the state of each node every 5 seconds»; «--node-eviction-rate (default 0.1) per second, meaning it won't evict pods from more than 1 node per 10 seconds»; `--secondary-node-eviction-rate` 0.01. — [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)

**Запись для списка:** Kubernetes Documentation (v1.37): kube-controller-manager; Node Status; Kubelet Configuration (v1beta1); kube-apiserver. — The Kubernetes Authors. — URL: https://kubernetes.io/docs/ (дата обращения: 06.11.2026); Kubernetes v1.32.0 Release Notes (CHANGELOG-1.32). — URL: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.32.md

### Inferences
- В 09-references.md ([1]) и в главе 1 значение «признание узла недостижимым через 40 с» верно только для версий ≤ 1.31; для текущих — 50 с, и 340 с → 350 с. При τ = 10 с (Lease) это k = 5 пропусков, а не 4. В тексте обязательно указывать версию платформы.
- «Период передачи сведений о состоянии узла 10 с» в текущих версиях точнее формулировать как «период обновления Lease 10 с»; `.status` при неизменном состоянии передаётся раз в 5 мин.

### Gaps
- Версия Kubernetes стенда Э1 в проверке не участвовала — при ≥1.32 расчёты T_о по умолчанию пересчитать.

---

## 7. Дополнительные источники измерений (отсутствуют в 09-references.md)

### Takeaway
Найдено и сверено по полному тексту 4 источника по интенсивности отказов узлов/устройств (Google, Microsoft ×2, Facebook) и 1 по времени запуска контейнеров (по аннотации). Рецензируемых измерений времени перенаправления трафика kube-proxy/eBPF при отказе узла **не найдено** — только блоги и документация; это поддерживает тезис о новизне измерения T_р в Э1.

### Cited Findings
**7.1. Ford D. et al. (Google), OSDI 2010 — интенсивность недоступности узлов (λ с учётом программных отказов)**
- «Figure 1 plots the CDF of node unavailability duration, showing that less than 10% of events last longer than 15 minutes. This data is gathered from tens of Google storage cells, each with 1000 to 7000 nodes, over a one year period» (разд. 2). — [USENIX PDF](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Ford.pdf)
- **Табл. 2 «Component failures across several Google cells»: MTTF Disk 10–50 years; Node 4.3 months; Rack 10.2 years**; «The numbers we report for component failures are inclusive of software errors and hardware failures … most node failures are transitory» (разд. 3). Причины недоступности: перезапуски ПО хранилища, плановые и внеплановые перезагрузки; в анализе — события ≥ 15 мин. — [USENIX PDF](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Ford.pdf)
- Запись: Ford D., Labelle F., Popovici F. I., Stokely M., Truong V.-A., Barroso L., Grimes C., Quinlan S. Availability in Globally Distributed Storage Systems // Proc. 9th USENIX Symp. on Operating Systems Design and Implementation (OSDI '10). — Vancouver : USENIX Association, 2010. — URL: https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Ford.pdf (DOI нет; **страницы не сверены** — страница USENIX вернула 403).

**7.2. Vishwanath K. V., Nagappan N. (Microsoft), SoCC 2010 — аппаратные отказы серверов**
- «We have details on part replacement for over 100,000 servers (exact number withheld)»; период 14 месяцев; значения нормированы на 100 серверов: «9 machine failures in 14 months translates to an annual failure rate (AFR) of around 8%»; «92% of the machines do not see any repair event»; «70% of all server failures is due to hard disks, 6% due to RAID controller and 5% due to memory and the rest (18%) due to other factors» (разд. 3). — [PDF Microsoft Research](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/06/socc088-vishwanath.pdf)
- Запись (CrossRef): Vishwanath K. V., Nagappan N. Characterizing cloud computing hardware reliability // Proc. 1st ACM Symp. on Cloud Computing (SoCC '10). — Indianapolis : ACM, 2010. — P. 193–204. — DOI: 10.1145/1807128.1807161.

**7.3. Gill P., Jain N., Nagappan N. (Microsoft), SIGCOMM 2011 — отказы сетевых устройств ЦОД, включая балансировщики**
- Данные «from October 2009 to September 2010»; «Top of Rack switches (ToRs) and aggregation switches exhibit the highest reliability in the network with failure rates of about 5% and 10%, respectively»; «We observe 1 in 5 load balancers exhibit a failure»; «load balancers (LB-1, LB-2) are the least reliable with a 1 in 5 chance of experiencing failure» (разд. 4.3, рис. 4 — вероятность отказа за год); сетевая избыточность «only 40% effective in reducing the median impact of failure». — [SIGCOMM 2011 PDF](https://conferences.sigcomm.org/sigcomm/2011/papers/sigcomm/p350.pdf)
- Запись (CrossRef): Gill P., Jain N., Nagappan N. Understanding network failures in data centers: measurement, analysis, and implications // Proc. ACM SIGCOMM 2011 Conf. — Toronto : ACM, 2011. — P. 350–361. — DOI: 10.1145/2018436.2018477.

**7.4. Meza J., Xu T., Veeraraghavan K., Mutlu O. (Facebook), IMC 2018 — надёжность сети ЦОД**
- 7 лет инцидентов внутри ЦОД и 18 мес. заявок по магистрали (аннотация); «in 2017, MTBI varied by three orders of magnitude across switch types: from 39,495 device-hours for core devices to 9,958,828 device-hours for RSWs» (разд. 5.5); «Rack switch incidents … are currently around 28% of all network incidents»; магистральные узлы: «50% of edge nodes fail less than once every 1710 h, or 2.3 months. And 90% of edge nodes fail less than once every 3521 h, or 4.8 months»; «time to failure and time to repair closely follow exponential functions» (разд. 6). — [IMC 2018 PDF](https://conferences.sigcomm.org/imc/2018/papers/imc18-final179.pdf)
- Запись (CrossRef): Meza J., Xu T., Veeraraghavan K., Mutlu O. A Large Scale Study of Data Center Network Reliability // Proc. Internet Measurement Conference 2018 (IMC '18). — Boston : ACM, 2018. — P. 393–407. — DOI: 10.1145/3278532.3278566. (Город по программе IMC'18 не сверялся.)

**7.5. Straesser M. et al., CCGrid 2023 — время запуска контейнеров (для T_п / переразмещения)**
- По аннотации (IEEE Xplore / AMiner, полный текст не читался): время запуска контейнеров в одной среде различается «between hundreds of milliseconds and tens of seconds»; набор — около 200 000 образов Docker Hub (Zenodo: 200 986 действительных образов). — [IEEE Xplore 10171550](https://ieeexplore.ieee.org/document/10171550); [Zenodo 7602500](https://zenodo.org/records/7602500)
- Запись (CrossRef): Straesser M., Bauer A., Leppich R., Herbst N., Chard K., Foster I., Kounev S. An Empirical Study of Container Image Configurations and Their Impact on Start Times // 2023 IEEE/ACM 23rd Int. Symp. on Cluster, Cloud and Internet Computing (CCGrid). — IEEE, 2023. — P. 94–105. — DOI: 10.1109/CCGrid57682.2023.00019.

**7.6. Schroeder B., Gibson G. A. — журнальная версия (TDSC 2010)** — см. п. 3; предпочтительна для списка ВАК (содержание не сверялось).

**7.7. Кандидаты, не проверенные (названы в ссылках Roberts et al.):** Sahoo R., Squillante M., Sivasubramaniam A., Zhang Y. «Failure data analysis of a large-scale heterogeneous server environment», DSN 2004; Garraghan P., Townend P., Xu J. «An empirical failure-analysis of a large-scale cloud computing environment», HASE 2014. — [arXiv:2507.02158, список литературы](https://arxiv.org/pdf/2507.02158)

### Inferences
- Диапазон λ узла по опубликованным данным: ≈0,08 /год (только аппаратные замены, Microsoft) — ≥0,54 /год (все отказы, требовавшие администратора, LANL; нижняя граница) — ≈2,8 /год (любая недоступность ≥15 мин, включая плановые перезагрузки, Google: 12 / 4,3 мес.). Выбор T_н = 1 год в числовом примере лежит внутри диапазона; в тексте полезно показать диапазон и пояснить, что определение «отказа» различается.
- Для балансировщиков/устройств перенаправления (Gill 2011): отказ за год у 1 из 5 — довод в пользу того, что звено перенаправления само ненадёжно.
- Рецензируемого измерения задержки перенаправления kube-proxy (iptables/IPVS/nftables/eBPF) при отказе узла не найдено (поиск 06.11.2026 вернул блоги и документацию, например [Netdata](https://www.netdata.cloud/guides/kubernetes/kubernetes-ipvs-stale-rules/), [DEV Community](https://dev.to/le_beltagy/i-replaced-kube-proxy-with-ebpf-in-production-and-why-my-monitoring-went-blind-for-6-hours-1n18)) — не цитировать как измерения.

### Gaps
- Страницы OSDI'10 (Ford) не сверены — проверить на usenix.org в браузере или по DBLP.
- Числа Straesser et al. сверены только по аннотации; конкретные значения времени запуска брать после чтения полного текста.
- Измерений хвоста задержки для межплощадочных каналов (WAN), пригодных для p, в этой проверке не найдено; Meza et al. дают лишь MTBF/MTTR магистральных узлов.
