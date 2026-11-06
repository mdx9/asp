# Пул источников для статьи 1 «Модель готовности телекоммуникационной службы с управляемым временем обнаружения отказа и учётом ложных срабатываний»

Составлен 06.11.2026 по `09-references.md` ([1]–[65]) и заметкам `research_notes/Источники и журнал для статьи 1/`. Сводный отчёт — `reports/Источники и журнал для статьи 1.md`.

**Правило отбора.** В пул входят только позиции с выходными данными, подтверждёнными по CrossRef, DBLP, rfc-editor.org, сайту издателя или официальному тексту документа. Поле, помеченное в заметках как «не подтверждено», в описание не вносится. Если без этого поля описание неполноценно (год тома, номер выпуска), позиция исключается. DOI, страницы и годы перенесены из заметок без изменений. Новых не добавлено. Оформление по ГОСТ Р 7.0.100-2018, на языке оригинала. При 1–3 авторах описание начинается с заголовка (первый автор). При четырёх авторах оно начинается с заглавия, а после косой черты перечислены все авторы. При пяти и более после косой черты указаны первые три с пометкой [et al.] или [и др.].

**Ключи.**
- D<N> — позиция [N] из `09-references.md`.
- A<id> — основной список `availability_models.md` (А1–А18); AR<id> — его резерв (Р1–Р15).
- F<id> — основной список `failure_detectors.md` (Н1–Н17); FR<id> — его резерв (Р1–Р6).
- R<id> — основной список `russian_literature.md` (Р1–Р18); RD<id> — его резерв (Д1–Д4); RX<id> — позиции того же файла без номера (RX1 — ГОСТ Р МЭК 61165-2019, RX2 — Гнеденко, Беляев, Соловьев, RX3 — Половко, Гуров).
- M<id> — дополнительные источники `parameter_measurements.md`, пронумерованные здесь:
  - M1 — Ford et al. «Availability in Globally Distributed Storage Systems» (OSDI 2010);
  - M2 — Vishwanath, Nagappan «Characterizing cloud computing hardware reliability» (SoCC 2010);
  - M3 — Gill, Jain, Nagappan «Understanding network failures in data centers: measurement, analysis, and implications» (SIGCOMM 2011);
  - M4 — Meza et al. «A Large Scale Study of Data Center Network Reliability» (IMC 2018);
  - M5 — Straesser et al. «An Empirical Study of Container Image Configurations and Their Impact on Start Times» (CCGrid 2023);
  - M6 — Schroeder, Gibson «A Large-Scale Study of Failures in High-Performance Computing Systems», журнальная версия (IEEE TDSC 2010);
  - M7 — Abdollahi Vayghan et al. «Deploying Microservice Based Applications with Kubernetes: Experiments and Lessons Learned» (IEEE CLOUD 2018);
  - M8 — «Microservice Based Architecture: Towards High-Availability for Stateful Applications with Kubernetes» (IEEE QRS 2019);
  - M9 — «A Kubernetes controller for managing the availability of elastic microservice based stateful applications» (Journal of Systems and Software, 2021);
  - M10 — Kubernetes Documentation (v1.37): kube-controller-manager; Node Status; Kubelet Configuration (v1beta1); kube-apiserver;
  - M11 — Kubernetes v1.32.0 Release Notes (CHANGELOG-1.32);
  - M12 — Sahoo et al. «Failure data analysis of a large-scale heterogeneous server environment» (DSN 2004);
  - M13 — Garraghan et al. «An empirical failure-analysis of a large-scale cloud computing environment» (HASE 2014).

## Пул (88 позиций)

### Модели готовности, покрытие, обнаружение в восстанавливаемых системах

- D19 | Ke, J.-C. On a repairable system with detection, imperfect coverage and reboot: Bayesian approach / J.-C. Ke, S.-L. Lee, Y.-L. Hsu // Simulation Modelling Practice and Theory. – 2008. – Vol. 16, No. 3. – P. 353–367. – DOI 10.1016/j.simpat.2007.12.001. | 2008 | модели готовности: восстанавливаемая система с этапом обнаружения и неполным охватом
- D20 | Ke, J.-C. Parametric Programming Approach for a Two-Unit Repairable System With Imperfect Coverage, Reboot and Fuzzy Parameters / J.-C. Ke, H.-I. Huang, C.-H. Lin // IEEE Transactions on Reliability. – 2008. – Vol. 57, No. 3. – P. 498–506. – DOI 10.1109/TR.2008.927703. | 2008 | модели готовности: неполный охват и перезапуск, то же семейство
- D33 | Kim, D. S. Availability Modeling and Analysis of a Virtualized System / D. S. Kim, F. Machida, K. S. Trivedi // Proceedings of the 15th IEEE Pacific Rim International Symposium on Dependable Computing (PRDC). – IEEE, 2009. – P. 365–371. – DOI 10.1109/PRDC.2009.64. | 2009 | модели готовности: время обнаружения как заданная величина (30 с)
- D34 | Nguyen, T. A. A Comprehensive Availability Modeling and Analysis of a Virtualized Servers System Using Stochastic Reward Nets / T. A. Nguyen, D. S. Kim, J. S. Park // The Scientific World Journal. – 2014. – Vol. 2014. – Article 165316. – 18 p. – DOI 10.1155/2014/165316. | 2014 | модели готовности: SRN виртуализированных серверов
- D35 | Reliability and Availability in Virtualized Networks: A Survey on Standards, Modeling Approaches, and Research Challenges / M. Di Mauro, W. Cerroni, F. Postiglione [et al.] // IEEE Communications Surveys & Tutorials. – 2026. – Vol. 28. – P. 5121–5158. – DOI 10.1109/COMST.2026.3670039. | 2026 | модели готовности: обзор по виртуализированным сетям
- D37 | Vaidyanathan, K. A Comprehensive Model for Software Rejuvenation / K. Vaidyanathan, K. S. Trivedi // IEEE Transactions on Dependable and Secure Computing. – 2005. – Vol. 2, No. 2. – P. 124–137. – DOI 10.1109/TDSC.2005.15. | 2005 | модели готовности: внутренний оптимум по временному параметру
- D57 | Trivedi, K. S. Probability and Statistics with Reliability, Queuing, and Computer Science Applications / K. S. Trivedi. – 2nd ed. – New York : John Wiley & Sons, 2001. – 848 p. – ISBN 978-0-471-33341-8. | 2001 | модели готовности: марковский и полумарковский аппарат, процессы восстановления
- D59 | Amdahl, G. M. Validity of the single processor approach to achieving large scale computing capabilities / G. M. Amdahl // Proceedings of the AFIPS Spring Joint Computer Conference. – Atlantic City, NJ, 1967. – Vol. 30. – P. 483–485. – DOI 10.1145/1465482.1465560. | 1967 | модели готовности: форма предельного выигрыша 1 + Tо⁰/Tр
- A1 | Arnold, T. F. The Concept of Coverage and Its Effect on the Reliability Model of a Repairable System / T. F. Arnold // IEEE Transactions on Computers. – 1973. – Vol. C-22, No. 3. – P. 251–254. – DOI 10.1109/T-C.1973.223703. | 1973 | модели готовности: первоисточник понятия охвата в восстанавливаемой системе
- A4 | Availability Modeling of SIP Protocol on IBM© WebSphere© / K. Trivedi, D. Wang, D. J. Hunt [et al.] // Proceedings of the 14th IEEE Pacific Rim International Symposium on Dependable Computing (PRDC 2008). – IEEE, 2008. – P. 323–330. – DOI 10.1109/PRDC.2008.50. | 2008 | модели готовности: задержки обнаружения и неполный охват у телеком-службы
- A8 | A Model-Based Approach to Anomaly Detection Trading Detection Time and False Alarm Rate / C. F. Goncalves, D. S. Menasche, A. Avritzer [et al.] // Proceedings of the 2020 Mediterranean Communication and Computer Networking Conference (MedComNet). – IEEE, 2020. – P. 1–8. – DOI 10.1109/MedComNet49392.2020.9191549. | 2020 | детекторы отказов: компромисс «время обнаружения — частота ложных тревог»
- A9 | Sebastio, S. An Availability Analysis Approach for Deployment Configurations of Containers / S. Sebastio, R. Ghosh, T. Mukherjee // IEEE Transactions on Services Computing. – 2021. – Vol. 14, No. 1. – P. 16–29. – DOI 10.1109/TSC.2017.2788442. | 2021 | модели готовности: деревья отказов и SRN контейнерных конфигураций
- A10 | Comparative Performability Assessment of SFCs: The Case of Containerized IP Multimedia Subsystem / M. Di Mauro, G. Galatro, M. Longo [et al.] // IEEE Transactions on Network and Service Management. – 2021. – Vol. 18, No. 1. – P. 258–272. – DOI 10.1109/TNSM.2020.3044232. | 2021 | модели готовности: SRN контейнеризированного IMS
- A11 | Tola, B. Model-Driven Availability Assessment of the NFV-MANO With Software Rejuvenation / B. Tola, Y. Jiang, B. E. Helvik // IEEE Transactions on Network and Service Management. – 2021. – Vol. 18, No. 3. – P. 2460–2477. – DOI 10.1109/TNSM.2021.3090208. | 2021 | модели готовности: SAN NFV-MANO, компромисс накладных расходов и готовности
- A12 | Performability of Network Service Chains: Stochastic Modeling and Assessment of Softwarized IP Multimedia Subsystem / M. Di Mauro, G. Galatro, F. Postiglione, M. Tambasco // IEEE Transactions on Dependable and Secure Computing. – 2022. – Vol. 19, No. 5. – P. 3071–3086. – DOI 10.1109/TDSC.2021.3082626. | 2022 | модели готовности: M/G/c + SRN программного IMS
- A13 | Kumar, A. Bayesian Modeling of Repairable Systems With Imperfect Coverage and Delayed Detection Dynamics / A. Kumar, C. Shekhar // Quality and Reliability Engineering International. – 2025. – Vol. 41, No. 4. – P. 1630–1641. – DOI 10.1002/qre.3742. | 2025 | модели готовности: фаза обнаружения как отдельная стадия восстановления
- A14 | Na, S. Repair policies of failure detection equipments and system availability / S. Na, S.-H. Bang // Communications for Statistical Applications and Methods. – 2022. – Vol. 29, No. 2. – P. 151–160. – DOI 10.29220/csam.2022.29.2.151. | 2022 | модели готовности: отказы самого средства обнаружения
- A15 | Impact of Service Function Aging on the Dependability for MEC Service Function Chain / J. Bai, X. Chang, F. Machida [et al.] // IEEE Transactions on Dependable and Secure Computing. – 2023. – Vol. 20, No. 4. – P. 2811–2824. – DOI 10.1109/TDSC.2022.3150782. | 2023 | модели готовности: полумарковская модель цепочки сервисных функций
- A16 | Model-Driven Dependability Assessment of Microservice Chains in MEC-Enabled IoT / J. Bai, X. Chang, F. Machida [et al.] // IEEE Transactions on Services Computing. – 2023. – Vol. 16, No. 4. – P. 2769–2785. – DOI 10.1109/TSC.2023.3241430. | 2023 | модели готовности: оптимизация интервалов омоложения по готовности
- A17 | Hecht, M. A Reliability and Availability Model of a Kubernetes Cluster Using SysML / M. Hecht, S. Agena // Proceedings of the 2024 Annual Reliability and Maintainability Symposium (RAMS). – IEEE, 2024. – P. 1–7. – DOI 10.1109/RAMS51492.2024.10457826. | 2024 | модели готовности: модель кластера платформы, параметры из хаос-тестов
- A18 | Mandal, P. Availability and Reliability of Core Networks (4G/5G) From a Deployment Standpoint / P. Mandal // IEEE Transactions on Services Computing. – 2025. – Vol. 18, No. 2. – P. 647–659. – DOI 10.1109/TSC.2025.3528332. | 2025 | модели готовности: ядро 4G/5G из VNF
- AR7 | Mukwevho, M. A. Toward a Smart Cloud: A Review of Fault-Tolerance Methods in Cloud Systems / M. A. Mukwevho, T. Celik // IEEE Transactions on Services Computing. – 2021. – Vol. 14, No. 2. – P. 589–605. – DOI 10.1109/TSC.2018.2816644. | 2021 | модели готовности: обзор методов отказоустойчивости облака
- AR14 | Hecht, M. Software Reliability and Availability Testing of a Kubernetes Cluster / M. Hecht // Proceedings of the 2026 Annual Reliability and Maintainability Symposium (RAMS). – IEEE, 2026. – P. 1–6. – DOI 10.1109/RAMS50514.2026.11424466. | 2026 | измерения: время и вероятность восстановления в кластере платформы как вход модели

### Детекторы отказов

- D9 | Chen, W. On the Quality of Service of Failure Detectors / W. Chen, S. Toueg, M. K. Aguilera // IEEE Transactions on Computers. – 2002. – Vol. 51, No. 5. – P. 561–580. – DOI 10.1109/TC.2002.1004595. | 2002 | детекторы отказов: метрики качества T_D, T_MR, λ_M
- D10 | The φ Accrual Failure Detector / N. Hayashibara, X. Défago, R. Yared, T. Katayama // Proceedings of the 23rd IEEE International Symposium on Reliable Distributed Systems (SRDS). – IEEE, 2004. | 2004 | детекторы отказов: φ-accrual, эмпирический компромисс
- D18 | Chandra, T. D. Unreliable Failure Detectors for Reliable Distributed Systems / T. D. Chandra, S. Toueg // Journal of the ACM. – 1996. – Vol. 43, No. 2. – P. 225–267. – DOI 10.1145/226643.226647. | 1996 | детекторы отказов: неотличимость отказа от медленного процесса
- D21 | Ma, T. On the Quality of Service of Crash-Recovery Failure Detectors / T. Ma, J. Hillston, S. Anderson // IEEE Transactions on Dependable and Secure Computing. – 2010. – Vol. 7, No. 3. – P. 271–283. – DOI 10.1109/TDSC.2009.35. | 2010 | детекторы отказов: качество детектора для восстанавливаемых объектов
- D22 | Freiling, F. C. The Failure Detector Abstraction / F. C. Freiling, R. Guerraoui, P. Kuznetsov // ACM Computing Surveys. – 2011. – Vol. 43, No. 2. – Article 9. – 40 p. – DOI 10.1145/1883612.1883616. | 2011 | детекторы отказов: обзор, компромисс выбора предельного времени ожидания
- D23 | Detecting failures in distributed systems with the Falcon spy network / J. B. Leners, H. Wu, W.-L. Hung [et al.] // Proceedings of the 23rd ACM Symposium on Operating Systems Principles (SOSP). – ACM, 2011. – P. 279–294. – DOI 10.1145/2043556.2043583. | 2011 | детекторы отказов: достоверный детектор ценой принудительного прекращения
- F1 | Chaurasia, B. IHFD: an improved heartbeat-based failure detector of ◇P class for partially synchronous hierarchical distributed systems / B. Chaurasia, A. Verma, P. Verma // Complex & Intelligent Systems. – 2026. – Vol. 12, No. 12. – Article 312. – DOI 10.1007/s40747-026-02423-z. | 2026 | детекторы отказов: адаптивный тайм-аут, метрики Чена — Туэга на PlanetLab
- F2 | Stab-FD: A cooperative and adaptive failure detector for wide area networks / P. Sens, L. Arantes, A. G. de M. Rossetto, O. Marin // Journal of Parallel and Distributed Computing. – 2024. – Vol. 186. – Article 104803. – DOI 10.1016/j.jpdc.2023.104803. | 2024 | детекторы отказов: калибровка таймеров по стабильности канала
- F3 | Consistency Before Availability: Network Reference Point based Failure Detection for Controller Redundancy / B. Johansson, M. Rågberger, A. V. Papadopoulos, T. Nolte // Proceedings of the 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA). – IEEE, 2023. – P. 1–8. – DOI 10.1109/ETFA54631.2023.10275664. | 2023 | детекторы отказов: цена ложного объявления отказа в резервированной паре
- F10 | Das, A. SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol / A. Das, I. Gupta, A. Motivala // Proceedings of the International Conference on Dependable Systems and Networks (DSN 2002). – IEEE, 2002. – P. 303–312. – DOI 10.1109/DSN.2002.1028914. | 2002 | детекторы отказов: компромисс «скорость — ложные срабатывания — нагрузка»
- F11 | Dadgar, A. Lifeguard: Local Health Awareness for More Accurate Failure Detection / A. Dadgar, J. Phillips, J. Currey // Proceedings of the 48th Annual IEEE/IFIP International Conference on Dependable Systems and Networks Workshops (DSN-W). – IEEE, 2018. – P. 22–25. – DOI 10.1109/DSN-W.2018.00017. | 2018 | детекторы отказов: ложные срабатывания от медленной обработки у наблюдателя
- F6 | Wang, Y. An Approach for Fast Fault Detection in Virtual Network / Y. Wang, R. Fang // Tehnički vjesnik — Technical Gazette. – 2023. – Vol. 30, No. 4. – P. 1146–1151. – DOI 10.17559/TV-20230207000330. | 2023 | детекторы отказов: миллисекундное обнаружение в виртуальном сетевом элементе
- F7 | Ji, C. FASTR: Fast Resilience for Stateful Programmable Data Planes / C. Ji, F. Kuipers // Proceedings of the 21st International Conference on Network and Service Management (CNSM 2025). – IFIP/IEEE, 2025. – P. 1–7. – DOI 10.23919/CNSM67658.2025.11297557. | 2025 | детекторы отказов: сердцебиение в плоскости данных, приоритет против ложных тревог
- F9 | A Survey on Rerouting Techniques with P4 Programmable Data Plane Switches / A. Mazloum, E. Kfoury, J. Gomez, J. Crichigno // Computer Networks. – 2023. – Vol. 230. – Article 109795. – DOI 10.1016/j.comnet.2023.109795. | 2023 | детекторы отказов: обзор, BFD в плоскости данных и минимальный τ
- D1 | Kubernetes Documentation. Concepts: Cluster Architecture — Nodes; Controllers; Services, Load Balancing, and Networking — EndpointSlices / The Kubernetes Authors. – URL: https://kubernetes.io/docs/concepts/architecture/nodes/ ; https://kubernetes.io/docs/concepts/architecture/controller/ ; https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/ | б. г. (обр. 2026) | детекторы отказов: штатный контур обнаружения отказа узла платформы
- M10 | Kubernetes Documentation (v1.37): kube-controller-manager; Node Status; Kubelet Configuration (v1beta1); kube-apiserver / The Kubernetes Authors. – URL: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/ ; https://kubernetes.io/docs/reference/node/node-status/ ; https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/ ; https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/ (дата обращения: 06.11.2026) | б. г. (обр. 2026) | детекторы отказов: значения по умолчанию (50 с, Lease 10 с / 40 с, tolerationSeconds 300 с)
- M11 | Kubernetes v1.32.0 Release Notes (CHANGELOG-1.32) / The Kubernetes Authors. – URL: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.32.md (дата обращения: 06.11.2026) | б. г. (обр. 2026) | детекторы отказов: смена node-monitor-grace-period 40 → 50 с

### Двусторонний контроль пересылки (BFD) и RFC

- D2 | Katz, D. Bidirectional Forwarding Detection (BFD) : RFC 5880 / D. Katz, D. Ward. – IETF, 2010. – Standards Track. – URL: https://www.rfc-editor.org/rfc/rfc5880.txt | 2010 | BFD-RFC: правило Detect Mult × интервал
- F12 | Katz, D. Bidirectional Forwarding Detection (BFD) for IPv4 and IPv6 (Single Hop) : RFC 5881 / D. Katz, D. Ward. – IETF, 2010. – Proposed Standard. – DOI 10.17487/RFC5881. – URL: https://www.rfc-editor.org/rfc/rfc5881.txt | 2010 | BFD-RFC: однопролётный профиль
- F13 | Katz, D. Bidirectional Forwarding Detection (BFD) for Multihop Paths : RFC 5883 / D. Katz, D. Ward. – IETF, 2010. – Proposed Standard. – DOI 10.17487/RFC5883. – URL: https://www.rfc-editor.org/rfc/rfc5883.txt | 2010 | BFD-RFC: многопролётный тракт (межплощадочный канал)
- D63 | Akiya, N. Common Interval Support in Bidirectional Forwarding Detection : RFC 7419 / N. Akiya, M. Binderberger, G. Mirsky. – IETF, 2014. – Informational. – URL: https://www.rfc-editor.org/rfc/rfc7419.html | 2014 | BFD-RFC: набор общеупотребительных периодов, τ_min
- FR4 | YANG Data Model for Bidirectional Forwarding Detection (BFD) : RFC 9127 / R. Rahman, L. Zheng, M. Jethanandani [et al.]. – IETF, 2021. – DOI 10.17487/RFC9127. | 2021 | BFD-RFC: модель конфигурации параметров сессии
- F4 | Unaffiliated Bidirectional Forwarding Detection (BFD) Echo : RFC 9747 / W. Cheng, R. Wang, X. Min [et al.]. – IETF, 2025. – Proposed Standard. – DOI 10.17487/RFC9747. – URL: https://www.rfc-editor.org/rfc/rfc9747.txt | 2025 | BFD-RFC: правило Detect Mult пропусков в режиме эхо
- F5 | Haas, J. Bidirectional Forwarding Detection (BFD) Encapsulated in Large Packets : RFC 9764 / J. Haas, A. Fu. – IETF, 2025. – Proposed Standard. – DOI 10.17487/RFC9764. – URL: https://www.rfc-editor.org/rfc/rfc9764.txt | 2025 | BFD-RFC: длина контрольного сообщения как параметр
- D65 | Ben Hassan, A. Performance Evaluation of Bidirectional Forwarding Detection (BFD) over the Virtual Router Redundancy Protocol (VRRP) / A. Ben Hassan, M. Mansour // Procedia Computer Science. – 2024. – Vol. 251. – P. 256–264. – DOI 10.1016/j.procs.2024.11.108. | 2024 | BFD-RFC: раздельные составляющие обнаружения и переключения (эмуляция)
- FR1 | Fault tolerance in SDN data plane considering network and application based metrics / B. Yamansavascilar, A. C. Baktir, A. Ozgovde, C. Ersoy // Journal of Network and Computer Applications. – 2020. – Vol. 170. – Article 102780. – DOI 10.1016/j.jnca.2020.102780. | 2020 | BFD-RFC: запись T_d = (M + 1)·T_i, расхождение формул

### Измерения: интенсивность отказов, задержка, перерыв обслуживания

- D3 | Roberts, J. Signalling Health for Improved Kubernetes Microservice Availability : preprint / J. Roberts, B. Archibald, P. Trinder. – 2025. – arXiv:2507.02158 [cs.DC]. – DOI 10.48550/arXiv.2507.02158. | 2025 | измерения: обнаружение отказа контейнера, ложные обнаружения при частом опросе
- D4 | Transparent Fault Tolerance for Stateful Applications in Kubernetes with Checkpoint/Restore / H. Schmidt, Z. Rejiba, R. Eidenbenz, K.-T. Förster // Proceedings of the 42nd International Symposium on Reliable Distributed Systems (SRDS). – IEEE, 2023. – P. 129–139. – DOI 10.1109/SRDS60354.2023.00022. | 2023 | измерения: время восстановления и составляющая обнаружения (~3 с)
- D5 | Chen, Z. Resilience Evaluation of Kubernetes in Cloud–Edge Environments : preprint / Z. Chen, M. Goudarzi, A. Nadjaran Toosi. – 2025. – arXiv:2507.16109. | 2025 | измерения: внесение неисправностей в кластеры платформы
- D13 | Kubernetes as an Availability Manager for Microservice Applications : preprint / L. Abdollahi Vayghan, M. A. Saied, M. Toeroe, F. Khendek. – 2019. – arXiv:1901.04946 [cs.SE]. – DOI 10.48550/arXiv.1901.04946. | 2019 | измерения: перерыв обслуживания при отказе узла, по умолчанию и в наиболее отзывчивой настройке
- D55 | Kubernetes Scalability and Performance SLIs/SLOs / Kubernetes Community, SIG Scalability. – URL: https://github.com/kubernetes/community/tree/master/sig-scalability/slos | б. г. (обр. 2026) | измерения: показатель задержки программирования распределения нагрузки (≈ Tр)
- D56 | Schroeder, B. A Large-Scale Study of Failures in High-Performance Computing Systems / B. Schroeder, G. A. Gibson // Proceedings of the International Conference on Dependable Systems and Networks (DSN'06). – Philadelphia, PA : IEEE, 2006. – P. 249–258. – DOI 10.1109/DSN.2006.5. | 2006 | измерения: интенсивность отказов узлов (LANL, 9 лет)
- D62 | Pingmesh: A Large-Scale System for Data Center Network Latency Measurement and Analysis / C. Guo, L. Yuan, D. Xiang [et al.] // Proceedings of the ACM SIGCOMM 2015. – London : ACM, 2015. – P. 139–152. – DOI 10.1145/2785956.2787496. | 2015 | измерения: потери и хвост задержки в ЦОД — содержание p
- M1 | Availability in Globally Distributed Storage Systems / D. Ford, F. Labelle, F. I. Popovici [et al.] // Proceedings of the 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI '10). – Vancouver : USENIX Association, 2010. – URL: https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Ford.pdf | 2010 | измерения: MTTF узла 4,3 мес. с учётом программных отказов
- M2 | Vishwanath, K. V. Characterizing cloud computing hardware reliability / K. V. Vishwanath, N. Nagappan // Proceedings of the 1st ACM Symposium on Cloud Computing (SoCC '10). – Indianapolis : ACM, 2010. – P. 193–204. – DOI 10.1145/1807128.1807161. | 2010 | измерения: годовая доля аппаратных отказов серверов ≈ 8 %
- M4 | A Large Scale Study of Data Center Network Reliability / J. Meza, T. Xu, K. Veeraraghavan, O. Mutlu // Proceedings of the Internet Measurement Conference 2018 (IMC '18). – ACM, 2018. – P. 393–407. – DOI 10.1145/3278532.3278566. | 2018 | измерения: MTBI сетевых устройств, экспоненциальность наработки и восстановления
- M5 | An Empirical Study of Container Image Configurations and Their Impact on Start Times / M. Straesser, A. Bauer, R. Leppich [et al.] // 2023 IEEE/ACM 23rd International Symposium on Cluster, Cloud and Internet Computing (CCGrid). – IEEE, 2023. – P. 94–105. – DOI 10.1109/CCGrid57682.2023.00019. | 2023 | измерения: время запуска контейнеров (Tп)

### Нормативные документы

- D6 | Network Functions Virtualisation (NFV); Resiliency Requirements : ETSI GS NFV-REL 001 V1.1.1 (2015-01). – ETSI, 2015. – URL: https://www.etsi.org/deliver/etsi_gs/NFV-REL/001_099/001/01.01.01_60/gs_NFV-REL001v010101p.pdf | 2015 | нормативные: уровни доступности и схемы резервирования NFV
- D15 | Network Functions Virtualisation (NFV); Architectural Framework : ETSI GS NFV 002 V1.2.1 (2014-12). – ETSI, 2014. – URL: https://www.etsi.org/deliver/etsi_gs/NFV/001_099/002/01.02.01_60/gs_NFV002v010201p.pdf | 2014 | нормативные: эталонная архитектура NFV
- D16 | Network Functions Virtualisation (NFV) Release 3; Architecture; Report on the Enhancements of the NFV architecture towards «Cloud-native» and «PaaS» : ETSI GR NFV-IFA 029 V3.3.1 (2019-11). – ETSI, 2019. – URL: https://www.etsi.org/deliver/etsi_gr/NFV-IFA/001_099/029/03.03.01_60/gr_NFV-IFA029v030301p.pdf | 2019 | нормативные: контейнерная инфраструктура NFV, «пять девяток»
- D26 | Network Functions Virtualisation (NFV); Assurance; Report on Active Monitoring and Failure Detection : ETSI GS NFV-REL 004 V1.1.1 (2016-04). – ETSI, 2016. – URL: https://www.etsi.org/deliver/etsi_gs/nfv-rel/001_099/004/01.01.01_60/gs_nfv-rel004v010101p.pdf | 2016 | нормативные: активный контроль и обнаружение отказов в NFV
- D31 | 5G; Service requirements for the 5G system : 3GPP TS 22.261 version 19.12.0 Release 19 (ETSI TS 122 261 V19.12.0, 2025-10). – ETSI / 3GPP, 2025. – URL: https://www.etsi.org/deliver/etsi_ts/122200_122299/122261/ | 2025 | нормативные: требования доступности службы связи 5G
- D30 | VNF and CNF Placement in 5G: Recent Advances and Future Trends / W. Attaoui, E. Sabir, H. Elbiaze, M. Guizani // IEEE Transactions on Network and Service Management. – 2023. – Vol. 20, No. 4. – P. 4698–4733. – DOI 10.1109/TNSM.2023.3264005. | 2023 | нормативные: контекст — контейнерные сетевые функции в 5G (обзор)
- D60 | Types and characteristics of SDH network protection architectures : ITU-T Recommendation G.841 (10/98). – ITU-T, 1998. – URL: https://www.itu.int/rec/T-REC-G.841-199810-I/en | 1998 | нормативные: выдержка и время завершения переключения
- D61 | Ethernet ring protection switching : ITU-T Recommendation G.8032/Y.1344 (03/2020). – ITU-T, 2020. – URL: https://www.itu.int/rec/T-REC-G.8032/en | 2020 | нормативные: ориентир 50 мс для времени переключения
- D8 | ГОСТ Р 27.102-2021. Надежность в технике. Надежность объекта. Термины и определения : национальный стандарт Российской Федерации : дата введения 2022-01-01. – Москва : Стандартинформ. | 2021 | нормативные: определение коэффициента готовности (п. 106)
- D17 | ГОСТ Р 53111-2008. Устойчивость функционирования сети связи общего пользования. Требования и методы проверки : национальный стандарт Российской Федерации : введен в действие приказом Ростехрегулирования от 18.12.2008 № 529-ст : дата введения 2009-10-01. | 2008 | нормативные: Kг = Tо/(Tо + Tв), нормы Kг сетей связи
- R18 | ГОСТ Р 27.010-2019 (МЭК 61703:2016). Надежность в технике. Математические выражения для показателей безотказности, готовности, ремонтопригодности : национальный стандарт Российской Федерации : утвержден приказом Росстандарта от 12.09.2019 № 673-ст : дата введения 2019-12-01. | 2019 | нормативные: расчётные выражения коэффициента готовности
- RX1 | ГОСТ Р МЭК 61165-2019. Надежность в технике. Применение марковских методов : национальный стандарт Российской Федерации : утвержден приказом Росстандарта от 05.09.2019 № 635-ст : дата введения 2019-12-01. | 2019 | нормативные: марковские методы, допущение постоянных интенсивностей

### Отечественные работы

- R1 | Богатырев, В. А. Оценка надежности восстанавливаемого кластера контейнерной виртуализацией / В. А. Богатырев, Фунг Ван Кю // Научно-технический вестник информационных технологий, механики и оптики. – 2025. – Т. 25, № 5. – С. 988–995. – DOI 10.17586/2226-1494-2025-25-5-988-995. | 2025 | отечественные: готовность восстанавливаемого контейнерного кластера
- R2 | До Мань Кием. Полумарковская модель надежности компьютерной системы с контейнерной виртуализацией / До Мань Кием, В. А. Богатырев // Информатика и автоматизация. – 2026. – Т. 25, № 5. – С. 1604–1639. – DOI 10.15622/ia.25.5.10. | 2026 | отечественные: полумарковская модель контейнерной системы
- R7 | Богатырев, В. А. Оценка готовности компьютерной системы к своевременному обслуживанию запросов при его совмещении с информационным восстановлением памяти после отказов / В. А. Богатырев, С. В. Богатырев, А. В. Богатырев // Научно-технический вестник информационных технологий, механики и оптики. – 2023. – Т. 23, № 3. – С. 608–617. – DOI 10.17586/2226-1494-2023-23-3-608-617. | 2023 | отечественные: двухэтапное восстановление в модели готовности
- R11 | Богатырев, В. А. Оптимизация периодичности инициализации контроля на основе дублированных вычислений / В. А. Богатырев, Д. Э. Лисичкин // Программные продукты и системы. – 2019. – Т. 32, № 2. – С. 214–220. – DOI 10.15827/0236-235X.126.214-220. | 2019 | отечественные: оптимум периодичности контроля по готовности
- R12 | Тахаутдинова, К. И. Оптимизация периодичности тестирования памяти вычислительных систем / К. И. Тахаутдинова, В. А. Богатырев // International Journal of Open Information Technologies. – 2026. – Т. 14, № 3. – С. 14–18. | 2026 | отечественные: противоречие «частота тестирования — простой»
- R13 | Зеленцов, Б. П. Модель надежности объекта при недостоверном контроле / Б. П. Зеленцов // Надежность и качество сложных систем. – 2020. – № 3 (31). – С. 46–54. – DOI 10.21685/2307-4205-2020-3-6. | 2020 | отечественные: недостоверный контроль (ошибки первого и второго рода)
- R14 | Зеленцов, Б. П. Модель надежности объекта с учетом мониторинга технического состояния / Б. П. Зеленцов // Вестник СибГУТИ. – 2020. – № 4 (52). – С. 14–27. | 2020 | отечественные: периодический мониторинг, скрытые отказы
- R15 | Зеленцов, Б. П. Метод расчета для коэффициента готовности пассивной оптической сети доступа в условиях недостоверного контроля / Б. П. Зеленцов, Е. П. Ионикова, В. П. Шувалов // T-Comm: Телекоммуникации и транспорт. – 2019. – Т. 13, № 7. – С. 10–15. – DOI 10.24411/2072-8735-2018-10285. | 2019 | отечественные: коэффициент готовности сети связи при недостоверном контроле
- RD2 | Зеленцов, Б. П. Модели элементов оптической сети доступа в условиях резервирования и учета недостоверного контроля их технического состояния / Б. П. Зеленцов, Е. П. Ионикова, В. П. Шувалов // Вестник СибГУТИ. – 2019. – № 1. – С. 3–15. | 2019 | отечественные: резервирование 1:1 и 1+1 при недостоверном контроле
- R17 | Шувалов, В. П. Методика оценки коэффициента готовности системы с резервированием. Пассивный режим / В. П. Шувалов, Б. П. Зеленцов, И. Г. Квиткова // T-Comm: Телекоммуникации и транспорт. – 2020. – Т. 14, № 8. – С. 21–25. – DOI 10.36724/2072-8735-2020-14-8-21-25. | 2020 | отечественные: коэффициент готовности при резервировании замещением
- R16 | Нетес, В. А. Отказы по общей причине и их влияние на устойчивость сетей и систем связи / В. А. Нетес // T-Comm: Телекоммуникации и транспорт. – 2024. – Т. 18, № 2. – С. 4–9. – DOI 10.36724/2072-8735-2024-18-2-4-9. | 2024 | отечественные: отказы по общей причине в сетях связи
- RD3 | Оценка показателей надежности шлюза по умолчанию в корпоративных сетях / А. Н. Земцов, М. А. Кузнецов, Д. А. Редняков, М. С. Аль-Мерри Гайс // Экономика и качество систем связи. – 2026. – № 1 (39). – С. 77–86. | 2026 | отечественные: надёжность резервирования шлюза (статья журнала-кандидата)

### Статистика и метрология

- D50 | Gilbert, E. N. Capacity of a Burst-Noise Channel / E. N. Gilbert // Bell System Technical Journal. – 1960. – Vol. 39, No. 5. – P. 1253–1265. – DOI 10.1002/j.1538-7305.1960.tb03959.x. | 1960 | статистика-метрология: модель пачечных потерь
- D51 | Elliott, E. O. Estimates of Error Rates for Codes on Burst-Noise Channels / E. O. Elliott // Bell System Technical Journal. – 1963. – Vol. 42, No. 5. – P. 1977–1997. – DOI 10.1002/j.1538-7305.1963.tb00955.x. | 1963 | статистика-метрология: модель пачечных потерь
- D52 | ГОСТ Р 8.736-2011. Государственная система обеспечения единства измерений. Измерения прямые многократные. Методы обработки результатов измерений. Основные положения : национальный стандарт Российской Федерации : дата введения 2013-01-01. – Москва : Стандартинформ. | 2011 | статистика-метрология: обработка многократных измерений, доверительные интервалы
- D53 | Evaluation of measurement data — Guide to the expression of uncertainty in measurement : JCGM 100:2008. – Joint Committee for Guides in Metrology, 2008. – URL: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf | 2008 | статистика-метрология: неопределённость измерений

## Итоги

**Всего:** 88 позиций.

**Распределение по ключам:** D — 39; A и AR — 15; F и FR — 14; R, RD и RX — 14; M — 6.

**Распределение по тематике:**

| Тематика | Позиций |
|---|---|
| Модели готовности | 21 |
| Детекторы отказов (с A8 и документацией платформы D1, M10, M11) | 18 |
| BFD и RFC | 9 |
| Измерения (с AR14) | 12 |
| Нормативные (с D30) | 12 |
| Отечественные | 12 |
| Статистика и метрология | 4 |

**Доля 2021–2026:** 36 из 88, то есть 40,9 %. Счёт ведётся по году тома или выпуска, как его требует ГОСТ Р 7.0.100-2018. В счёт входят:
- D3, D4, D5, D8, D30, D31, D35, D65;
- A9–A18, AR7, AR14;
- F1–F7 без F8, F9, FR4;
- R1, R2, R7, R12, R16, RD3;
- M5.

Оговорка: у A9 и AR7 том датирован 2021 г., но ранний доступ открыт в 2017–2018 гг. Если считать по ранней дате, получается 34 из 88, то есть 38,6 %. Электронная документация D1, D55, M10, M11 без даты в счёт не входит.

**На русском языке:** 17 позиций — D8, D17, D52, R1, R2, R7, R11, R12, R13, R14, R15, R16, R17, R18, RD2, RD3, RX1.

**Школа Богатырева:** 5 работ — R1, R2, R7, R11, R12.

**Зеленцов и Шувалов, недостоверный контроль:** 5 работ — R13, R14, R15, RD2, R17.

**Препринты без рецензируемой версии:** D3, D5, D13. Включены, потому что они составляют единственную экспериментальную опору по платформе. Для журнала ВАК их число стоит держать минимальным.

**Сверить до подачи статьи, на выходные данные пула не влияет:**
- R17 — инициалы второго автора. CyberLeninka указывает «Вячеслав Петрович», вероятно ошибочно.
- RD3 — формат выпуска «№ 1 (39)». Он согласуется с нумерацией архива журнала (№ 1 (31) 2024 … № 3 (41) 2026), но по PDF не сверен.
- D65 — числа 50 мс, 1–1,57 с и 3,48–5 с независимо не перепроверены (ScienceDirect вернул 403).
- F10 — год 2002 следует из названия конференции DSN 2002 и из DOI. CrossRef даты не возвращает, OpenAlex указывает 2003.
- M1 — страницы не сверены, поэтому описание дано без них.
- D10 — DOI и страницы в заметках не подтверждены, поэтому описание дано без них.
- RX1 — каталоги расходятся в статусе стандарта («взамен» или «действующий»). Проверить на fgis.gost.ru.

## Исключённые кандидаты

| Ключ | Работа | Причина |
|---|---|---|
| A2 | Dugan, Trivedi, IEEE TC 1989 | Лимит объёма. Линию охвата представляют A1, D19, D20, A13 |
| A3 | Trivedi, Bobbio, CUP 2017 | Место издания и число страниц не подтверждены. Аппарат обеспечен D57 |
| A5 | Matos et al., IEEE TR 2012 | Лимит объёма. Значение 30 с взято из фрагмента и не сверено. Те же 30 с даёт D33 |
| A6 | Sakic, Kellerer, IEEE TNSM 2018 | Роль задержки обнаружения по аннотации не установлена |
| A7 | Tola, Nencioni, Helvik, IEEE TNSM 2019 | Лимит объёма. Линию NTNU представляет A11 |
| AR1–AR6, AR8–AR11, AR13 | Резерв `availability_models.md` | Лимит объёма. У AR3, AR9, AR13 содержание не сверено |
| AR12 | Xiong et al., IPDPS 2012 | Лимит объёма. Автонастройку детектора представляют F1 и F2 |
| AR15 | Bertier, Marin, Sens, DSN 2002 | CrossRef год не вернул. Работа нужна только как объект сравнения в F1 и F2 |
| F8 | Franco et al., Telecommunication Systems, т. 85, № 2 | Год тома не подтверждён (CrossRef даёт только онлайн-дату 19.12.2023) |
| F14 | RFC 7880 (S-BFD) | Лимит объёма |
| F15 | van Adrichem et al., EWSDN 2014 | Лимит объёма. Декомпозицию времени восстановления подтверждают D65 и F9 |
| F16 | Sharma et al., Computer Communications 2013 | Числа по первоисточнику не сверены (пересказ). Лимит объёма |
| F17 | Cascone et al., IJNM, т. 27, № 2 | Год тома 2017 явно не подтверждён (онлайн 2016) |
| FR2 | Huang et al. «Gray Failure», HotOS 2017 | Подзаголовок записан по памяти, содержание не сверено |
| FR3 | Suresh et al. «Rapid» | Публикация в USENIX ATC 2018 и страницы не подтверждены |
| FR5 | KEP-589 | Полное имя автора не подтверждено. Значения покрыты M10 и M11 |
| FR6 | Справка kube-controller-manager | Объединена с M10 (так рекомендует и заметка) |
| R3, R4, R5, R6, R8, RD1 | Работы школы Богатырева | Лимит «не более 5 работ школы» |
| R9 | Алексанков, Богатырев, Деркач, 2019 | Лимит школы. Кроме того, номер тома расходится: CrossRef даёт 24, CyberLeninka — 32 |
| R10 | Пашков, 2018 | Слабая связь с темой (размещение контроллеров SDN). Лимит объёма |
| RD4 | Ковальков, 2011 | Номер и страницы не извлечены |
| RX2 | Гнеденко, Беляев, Соловьев, 1965 | Число страниц не подтверждено. Лимит объёма. Можно вернуть без поля страниц |
| RX3 | Половко, Гуров «Основы теории надежности» | Год 2-го издания не подтверждён (2006 или 2008) |
| — | Черкесов «Надежность аппаратно-программных комплексов»; Ушаков (ред.) справочник 1985; учебник Шувалова и др. | Выходные данные не подтверждены или не проверялись |
| — | Хрусталев, Вестник НГУЭУ 2021 | Не рекомендован в заметке: журнал экономического вуза |
| M3 | Gill, Jain, Nagappan, SIGCOMM 2011 | Лимит объёма. Довод о ненадёжности звена перенаправления — вспомогательный |
| M6 | Schroeder, Gibson, IEEE TDSC 2010 | Дублирует D56. Содержание журнальной версии не сверено |
| M7 | Abdollahi Vayghan et al., IEEE CLOUD 2018 | Полный текст не сверен. Числа из него брать нельзя |
| M8, M9 | Работы той же группы, QRS 2019 и JSS 2021 | Состав авторов в заметках не приведён (стоит многоточие) |
| M12, M13 | Sahoo et al. DSN 2004; Garraghan et al. HASE 2014 | Не проверены. Названы только в списке литературы D3 |
| D7 | ITU-T E.800 | Редакция не установлена (1988, 1994 или 2008). Определения готовности вынесены в недоступный Supplement 6 |
| D14 | Phan-Ba, 2015 | Нерецензируемое эссе, содержание не сверено |
| D11, D12, D24, D25, D27, D28, D29, D32, D36, D38–D49, D54, D64 | Прочие позиции [1]–[65] | Относятся к главам 1, 2, 4, 5 диссертации или к стенду, а не к модели статьи. Лимит объёма |
| D58 | Wang, Zhang, Xu, DSN 2017 | Страницы и DOI не подтверждены. Лимит объёма |
| — | Aguilera, Le Lann, Toueg, DISC 2002 | Выходные данные подтверждены, но содержание не прочитано. Это кандидат на опровержение разрыва. До прочтения не цитировать |
| — | Hsu, Lee, Ke, MATCOM 2009; Ke, Liu, AMC 2014 | В списке без номера. Семейство представлено D19 и D20 |
| — | Tran, Vu, Kim, IEEE Access 2022 | В списке без номера, содержание не сверено. Кандидат для главы 4 |
| — | SBRC: Chaos-K8s, K8s-DT | Выходные данные не проверялись |
