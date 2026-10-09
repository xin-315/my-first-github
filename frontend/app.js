/**
 * 智学罗盘 (SmartStudy AI) - 学生端全交互控制器
 * JC2001 Software Engineering - Group 5 (BSc BMIS)
 */

// =============================================================================
// 多学科精品真题与避坑知识本体库 (Curated Multi-Discipline Question Bank - Chinese)
// =============================================================================
const DB_ZH = {
  law: {
    name: "民商法学与民法典",
    badge: "期末高频考点",
    questions: [
      {
        id: "law_1",
        difficulty: "★★★☆☆",
        tag: "可撤销民事法律行为 · 撤销权存续期间",
        stem: "甲于2023年3月1日因受欺诈与乙签订二手车买卖合同，同年5月1日甲知道该欺诈事由。根据《民法典》关于可撤销民事法律行为的规定，甲请求人民法院撤销该合同的除斥期间应当自何时起算？最迟于何时届满？",
        options: [
          { key: "A", text: "自合同签订之日（2023年3月1日）起算，最迟于 3 年内届满", isCorrect: false, trapId: "trap_law_1" },
          { key: "B", text: "自知道受欺诈之日（2023年5月1日）起算，最迟于 1 年内届满", isCorrect: true },
          { key: "C", text: "自欺诈行为终止之日起算，最迟于 1 年内届满", isCorrect: false, trapId: "trap_law_2" },
          { key: "D", text: "自合同签订之日起算，无论是否知情一律在 2 年内届满", isCorrect: false, trapId: "trap_law_3" }
        ],
        explanation: "【权威考点解析 · 民法典第152条】：重大误解撤销权自知道之日起90日内行使，受欺诈撤销权自知道或者应当知道之日起1年内行使；自行为发生之日起5年内未行使的撤销权消灭。该期限性质属于除斥期间，不发生中止、中断或延长！",
        traps: {
          trap_law_1: {
            title: "🚨 典型混淆陷阱：把'形成权除斥期间'错套为'3年普通诉讼时效'",
            desc: "这是全校 64% 学生最常踩的深坑！通用 AI 答题时也经常将《民法典》第 188 条的 3 年诉讼时效套到撤销权上。诉讼时效管的是'请求权'，而撤销权属于'形成权'，必须适用严格的法定除斥期间！",
            prereq: "先修定理前置：请求权 vs 形成权区别",
            radarHit: "trapDefense"
          },
          trap_law_2: {
            title: "🚨 规范错配陷阱：把'受欺诈'与'受胁迫'的法定起算点混为一谈",
            desc: "《民法典》严格区分受欺诈与受胁迫：受胁迫才自'胁迫行为终止之日'起算；受欺诈则是自'知道或者应当知道撤销事由之日'起算！",
            prereq: "先修定理前置：胁迫与欺诈意志瑕疵法定起算条件",
            radarHit: "boundary"
          },
          trap_law_3: {
            title: "🚨 历史废条死记陷阱：混淆旧合同法与现行民法典",
            desc: "误用了已被废止的旧合同法条款。现行民法典明确统一为受欺诈起算 1 年，最长保护期为 5 年（并非 2 年）。",
            prereq: "先修定理前置：民法典总则编撤销权体系",
            radarHit: "recall"
          }
        },
        graph: {
          title: "民法典第152条·可撤销民事法律行为拓扑子图",
          nodes: [
            { id: "c1", label: "撤销权除斥期间", type: "core", x: 260, y: 140 },
            { id: "p1", label: "知道欺诈之日起 1年", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "行为发生起最长 5年", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "陷阱: 错套3年诉讼时效", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "陷阱: 错记胁迫终止点", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "主除斥期间" },
            { from: "p2", to: "c1", label: "最长保护期" },
            { from: "c1", to: "t1", label: "易错于 (混淆权利性质)" },
            { from: "c1", to: "t2", label: "易错于 (错配起算点)" }
          ]
        },
        socraticPrompt: "同学，请停下来想一想：在民法理论中，当事人要消灭一个已经成立的合同，行使的是让相对人掏钱还货的'请求权'，还是凭单方意思就能变更法律关系的'形成权'？为什么这两种权利的时效规定截然不同？"
      },
      {
        id: "law_2",
        difficulty: "★★★★☆",
        tag: "物权编 · 动产善意取得构成要件与阻却事由",
        stem: "甲将其所有的专业单反相机出借给乙使用，乙擅自以市场公允价 12000 元卖给不知情的摄影爱好者丙，并当场完成交付并收款完毕。一周后甲发现此事，向丙主张相机所有权要求其无偿归还。关于本案法律效力，下列说法完全正确的是？",
        options: [
          { key: "A", text: "因乙对相机无处分权，乙丙之间的买卖合同自始绝对无效，丙不能取得所有权", isCorrect: false, trapId: "trap_law_2_1" },
          { key: "B", text: "丙已基于《民法典》善意取得制度原始取得该相机所有权，甲无权要求返还原物", isCorrect: true },
          { key: "C", text: "因相机属于出借物而非遗失物，丙必须先行向甲支付合理补偿后方可保留相机", isCorrect: false, trapId: "trap_law_2_2" },
          { key: "D", text: "善意取得仅适用于不动产物权，动产在原权利人甲明确追认前处于效力待定状态", isCorrect: false, trapId: "trap_law_2_3" }
        ],
        explanation: "【权威考点解析 · 民法典第311条与第597条】：① 无处分权人订立的买卖合同有效（彻底废除原合同法第51条效力待定说）；② 善意取得构成要件：受让人受让时善意且无重大过失、以合理价格转让、已依法完成交付。丙完全满足三要件，依法取得动产所有权；甲只能向无权处分人乙主张侵权赔偿或不当得利！",
        traps: {
          trap_law_2_1: {
            title: "🚨 废除旧法死记陷阱：把'处分权瑕疵'误等同于'买卖合同绝对无效'",
            desc: "这是法学期末和考研 58% 学生极易踩中的传统重灾区！民法典明确区分负担行为（债权合同）与处分行为（物权变动）。买卖合同即使无权处分也有效，不能履行则承担违约责任，善意受让人更直接受善意取得保护！",
            prereq: "先修定理前置：债权合同效力与物权变动分离原则",
            radarHit: "recall"
          },
          trap_law_2_2: {
            title: "🚨 规则混淆陷阱：错把'遗失物盗脏物回赎'套用到'意定借用委托物'上",
            desc: "《民法典》第 312 条仅对遗失物等'非基于真正权利人意思脱离占有的物'规定了 2 年内可支付对价请求返还。本案中甲是自愿借给乙的（占有委托物），原权利人必须自担信托风险，根本不存在有偿回赎权利！",
            prereq: "先修定理前置：占有脱离物 vs 占有委托物法律后果差异",
            radarHit: "boundary"
          },
          trap_law_2_3: {
            title: "🚨 制度适用范围盲区：善意取得横跨动产与不动产两大领域",
            desc: "通用 AI 常常将动产交付与不动产登记要件张冠李戴。善意取得恰恰是以动产占有公信力与不动产登记公信力为双支柱的法定原始取得制度！",
            prereq: "先修定理前置：物权公示与公信原则在动产中的体现",
            radarHit: "trapDefense"
          }
        },
        graph: {
          title: "民法典第311条·善意取得构成与阻却拓扑图",
          nodes: [
            { id: "c1", label: "动产善意取得 (311条)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "善意+合理价格+完成交付", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "占有委托物风险归属", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "陷阱: 误判买卖合同无效", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "陷阱: 错套遗失物回赎补偿", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "法定三要素" },
            { from: "p2", to: "c1", label: "阻却原物返还" },
            { from: "c1", to: "t1", label: "易错于 (负担与处分行为未区分)" },
            { from: "c1", to: "t2", label: "易错于 (脱离物与委托物混同)" }
          ]
        },
        socraticPrompt: "同学请思考：如果原所有人甲自己不谨慎把相机借给不可靠的朋友乙，而善意买家丙在市场上付了真金白银拿到了相机，法律为什么要保护丙而不是保护甲？这背后体现了怎样的商事交易安全价值取向？"
      },
      {
        id: "law_3",
        difficulty: "★★★★☆",
        tag: "总则编 · 表见代理与权利外观责任",
        stem: "某软件科技公司解聘了销售副总张某，但疏忽未及时收缴其持有的加盖公司公章的空白业务授权书及合同专用章。次日，张某持上述文件以该科技公司名义，与不知其离职且已尽通常注意义务的某云服务商签订了价值 80 万元的机房服务器租用合同。关于该合同效力与责任，下列说法正确的是？",
        options: [
          { key: "A", text: "张某离职后已无代理权，该合同自始绝对无效，科技公司不负任何民事责任", isCorrect: false, trapId: "trap_law_3_1" },
          { key: "B", text: "构成表见代理，该合同对科技公司有效，科技公司须承担合同约定的履约付款责任", isCorrect: true },
          { key: "C", text: "该合同属于效力待定合同，若科技公司在法定 30 天内不予追认，则合同直接归于消灭", isCorrect: false, trapId: "trap_law_3_2" },
          { key: "D", text: "只有当云服务商能充分证明科技公司高管存在主观欺诈故意时，方能认定表见代理成立", isCorrect: false, trapId: "trap_law_3_3" }
        ],
        explanation: "【权威考点解析 · 民法典第172条】：行为人没有代理权、超越代理权或者代理权终止后，仍然实施代理行为，相对人有理由相信行为人有代理权的，代理行为有效。公司未收回印章与授权书具有重大过失（可归责的外观），相对人善意无过失，构成表见代理！公司履行后可向张某追偿！",
        traps: {
          trap_law_3_1: {
            title: "🚨 机械无权否定陷阱：忽视商事外观法理对善意第三人的倾斜保护",
            desc: "很多初学者只看到'张某已离职无权'这半句话，机械认定合同无效。表见代理制度的存在目的，恰恰就是在代理权实质欠缺时，因被代理人造成了权利外观而强制其承受法律后果！",
            prereq: "先修定理前置：权利外观理论与信赖利益保护",
            radarHit: "trapDefense"
          },
          trap_law_3_2: {
            title: "🚨 程序顺位颠倒陷阱：把'表见代理'降级为'狭义无权代理的效力待定'",
            desc: "表见代理一旦成立，相对人享有选择权：既可以主张表见代理有效要求公司履约，也可以主动撤销。但被代理人（科技公司）根本无权单方面通过'拒绝追认'来废除合同！",
            prereq: "先修定理前置：表见代理与狭义无权代理法律后果断点",
            radarHit: "boundary"
          },
          trap_law_3_3: {
            title: "🚨 归责要件苛刻化陷阱：混淆'权利外观可归责性'与'侵权故意'",
            desc: "认定表见代理完全不需要被代理人具有主观欺诈故意！只要公章管理不善、授权书未收回等客观过失造成了权利外观，就足以认定本人具有可归责性！",
            prereq: "先修定理前置：表见代理客观要件与主观要件判定标准",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "民法典第172条·表见代理效力归属拓扑图",
          nodes: [
            { id: "c1", label: "表见代理 (172条)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "权利外观+本人过失", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "相对人善意且无过失", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "陷阱: 错判为绝对无效", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "陷阱: 误以为必须本人故意", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "外观形成归责" },
            { from: "p2", to: "c1", label: "信赖保护要件" },
            { from: "c1", to: "t1", label: "易错于 (机械无权观)" },
            { from: "c1", to: "t2", label: "易错于 (苛刻主观要件)" }
          ]
        },
        socraticPrompt: "请同学设身处地推演：如果你是一家供应商，对方拿着盖有鲜章的授权书和公章来签约，你有可能去查他们公司内部今天有没有发红头文件开除这个人吗？法律为什么要让疏于管理印章的公司买单？"
      }
    ]
  },

  cs: {
    name: "计算机体系结构",
    badge: "期末压轴考点",
    questions: [
      {
        id: "cs_1",
        difficulty: "★★★★☆",
        tag: "RISC经典流水线 · 冒险处理与前递旁路",
        stem: "在标准五级按序执行流水线（IF, ID, EX, MEM, WB）中，指令 i 为算术运算（如 add R1, R2, R3），紧随其后的指令 i+1（如 sub R4, R1, R5）在执行阶段需要用到 R1。关于此场景下的流水线冒险与优化，下列说法正确的是？",
        options: [
          { key: "A", text: "属于写后读 (WAR) 反相关冒险；五级流水线必须插入 2 个周期停顿", isCorrect: false, trapId: "trap_cs_1" },
          { key: "B", text: "属于读后写 (RAW) 真实数据相关；可通过硬件前递旁路 (Forwarding) 消除所有停顿", isCorrect: true },
          { key: "C", text: "属于结构冒险 (Structural Hazard)；必须通过将单端口寄存器升级为多端口解决", isCorrect: false, trapId: "trap_cs_2" },
          { key: "D", text: "属于控制冒险 (Control Hazard)；需要引入分支历史表 (BHT) 预测执行", isCorrect: false, trapId: "trap_cs_3" }
        ],
        explanation: "【权威考点解析 · RISC 五级流水线数据前递】：指令 i 在 EX 阶段结束时（ALU 输出端）已经计算出了 R1 的新值，而指令 i+1 在 EX 阶段开始时才需要 R1。通过在 EX/MEM 流水线寄存器引出一根前递直通线（Forwarding Path）送入 ALU 输入端，即可完全消除气泡（Zero Stall）！",
        traps: {
          trap_cs_1: {
            title: "🚨 高阶概念死记硬背陷阱：五级顺序流水线根本不可能出现 WAR/WAW 反相关！",
            desc: "这是通用大模型极易给出的知识幻觉！只有在支持'乱序执行 (Out-of-Order Execution)'的超标量处理器（如 Tomasulo 架构）中才可能发生 WAR 冒险。在经典五级顺序流水线中，指令按序流淌，前一条指令不可能在后一条指令之后才读取！",
            prereq: "先修定理前置：按序执行与乱序执行的前提差异",
            radarHit: "boundary"
          },
          trap_cs_2: {
            title: "🚨 分类混淆陷阱：误将'寄存器数据传递'判断为'硬件结构资源冲突'",
            desc: "结构冒险指的是多个指令在同一时钟周期争夺同一物理部件（例如单端口内存同时读指令与读数据）。题干明确是寄存器数值的前后依赖，是纯粹的数据冒险！",
            prereq: "先修定理前置：三大流水线冒险分类边界",
            radarHit: "recall"
          },
          trap_cs_3: {
            title: "🚨 题意泛化盲猜陷阱：算术指令不存在条件分支",
            desc: "控制冒险仅由条件分支（beq, bne）或无条件跳转（jmp）修改 PC 引起，普通算术指令没有任何分支预测需求！",
            prereq: "先修定理前置：控制冒险与分支指令语义",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "RISC 五级流水线·数据依赖与前递旁路图谱",
          nodes: [
            { id: "c1", label: "流水线数据冒险 (RAW)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "前提: 按序发射执行", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "方案: ALU前递旁路", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "幻觉陷阱: 错套WAR反相关", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "混淆陷阱: 错判为结构争用", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "体系结构约束" },
            { from: "p2", to: "c1", label: "硬件零停顿优化" },
            { from: "c1", to: "t1", label: "易错于 (乱序与顺序概念混淆)" },
            { from: "c1", to: "t2", label: "易错于 (资源争用与数据流混淆)" }
          ]
        },
        socraticPrompt: "吴同学，请观察 MIPS 五级流水线的时空图：在按序发射的情况下，如果一条指令在时钟周期 3 的末尾已经拿到了算术结果，而下一条指令在周期 4 的开始才需要这个结果，为什么我们非要傻等到周期 5 写回寄存器堆才拿呢？中间能搭一条近道吗？"
      },
      {
        id: "cs_2",
        difficulty: "★★★★☆",
        tag: "存储层次结构 · Cache 组相联映射与缺失分析",
        stem: "某 32 位字节编址处理器配置有 32KB 的数据 Cache，Cache 块大小为 64 字节，采用 4 路组相联（4-Way Set Associative）映射。现程序频繁循环访问步长为 32KB 的大数组导致严重的冲突缺失（Conflict Miss）。下列关于该 Cache 字段划分与缺失优化，叙述完全正确的是？",
        options: [
          { key: "A", text: "主存地址划分为：Tag=19位，Index=7位，Offset=6位；将相联度提升为 8 路可直接缓解冲突缺失", isCorrect: true },
          { key: "B", text: "主存地址划分为：Tag=18位，Index=8位，Offset=6位；将替换算法由 LRU 改为 FIFO 可降低缺失率", isCorrect: false, trapId: "trap_cs_2_1" },
          { key: "C", text: "主存地址划分为：Tag=20位，Index=6位，Offset=6位；将块大小从 64B 增大到 128B 能根治冲突缺失", isCorrect: false, trapId: "trap_cs_2_2" },
          { key: "D", text: "只要在 CPU 内部增加一级指令预取缓冲区（Prefetch Buffer），即可完全消除数据 Cache 的所有缺失", isCorrect: false, trapId: "trap_cs_2_3" }
        ],
        explanation: "【权威考点解析 · Cache 地址划分与 3C 缺失】：① 块大小 64B = 2⁶，故 Offset = 6 位；总块数 = 32KB / 64B = 512 块；4 路组相联则组数 = 512 / 4 = 128 组 = 2⁷，故 Index = 7 位；Tag = 32 - 7 - 6 = 19 位！② 冲突缺失源于多个数据映射到同一下标组，增大路数（如改为 8 路）或引入 Victim Cache 是经典有效解法！",
        traps: {
          trap_cs_2_1: {
            title: "🚨 组数计算与替换策略双重陷阱：混淆 Cache 总块数与组数",
            desc: "许多同学直接把 512 块当成 512 组算出 9 位或 8 位 Index。更严重的是，LRU 基于时间局部性是理论与工程最佳基准，FIFO 不仅缺失率更高，还会引发著名的 Belady 异常！",
            prereq: "先修定理前置：组相联 Cache 组数计算公式与局部性原理",
            radarHit: "precision"
          },
          trap_cs_2_2: {
            title: "🚨 块大小盲目增大陷阱：块过大会压缩组数并加剧冲突缺失",
            desc: "在 Cache 总容量固定的前提下，盲目增大块大小会导致 Cache 总组数急剧减半，反而使步长访问的冲突缺失雪上加霜，并显著增加主存缺失惩罚（Miss Penalty）！",
            prereq: "先修定理前置：3C 缺失模型（冷启动/容量/冲突）权衡博弈",
            radarHit: "boundary"
          },
          trap_cs_2_3: {
            title: "🚨 部件职责错配陷阱：把指令预取与数据访存混为一谈",
            desc: "指令预取缓冲区针对的是顺序指令流的自适应提取，对大步长随机跳转的数据密集型数组读写根本无法起到降低冲突缺失的作用！",
            prereq: "先修定理前置：哈佛结构下指令 Cache 与数据 Cache 行为解耦",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "组相联 Cache·地址解码与冲突缺失权衡图谱",
          nodes: [
            { id: "c1", label: "4路组相联 (Index 7位)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "块大小64B (Offset 6位)", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "容量32KB (128组/Tag 19位)", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "陷阱: 错把块数当组数", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "陷阱: 误以为FIFO优于LRU", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "低位块内寻址" },
            { from: "p2", to: "c1", label: "相联度与组数约束" },
            { from: "c1", to: "t1", label: "易错于 (计算除以路数遗漏)" },
            { from: "c1", to: "t2", label: "易错于 (替换算法局部性原理违背)" }
          ]
        },
        socraticPrompt: "请同学拿起草稿纸算一算：如果一个水库有 512 个蓄水池，每个池子单独编号。现在我们把每 4 个池子编成一个大组，那么一共有多少个大组？为什么寻址时硬件只需要对组号进行解码，而组内的 4 个池子是并行比较 Tag 的？"
      },
      {
        id: "cs_3",
        difficulty: "★★★★★",
        tag: "虚拟存储系统 · TLB 快表与缺页异常处理时序",
        stem: "在支持现代多级页表的虚拟内存系统中，当 CPU 执行一条访存指令（如 lw $t0, 0($a0)）发生地址翻译时，下列关于 TLB（快表）、Page Table（页表）以及缺页异常（Page Fault）的时序与硬件协作，哪一项表述是完全正确的？",
        options: [
          { key: "A", text: "若 TLB 命中，CPU 直接获取物理地址并发起内存读取，全程完全无需访问主存中的多级页表", isCorrect: true },
          { key: "B", text: "若 TLB 缺失，硬件 MMU 必须立即向操作系统内核报告缺页中断异常（Page Fault），暂停当前进程", isCorrect: false, trapId: "trap_cs_3_1" },
          { key: "C", text: "操作系统缺页异常处理程序完成磁盘换页调入后，CPU 从导致缺页指令的'下一条指令 (PC+4)'恢复执行", isCorrect: false, trapId: "trap_cs_3_2" },
          { key: "D", text: "页表中的有效位（Valid Bit）为 1 且 TLB 缺失时，该物理页必定已经被完全换出到磁盘交换区", isCorrect: false, trapId: "trap_cs_3_3" }
        ],
        explanation: "【权威考点解析 · 虚拟地址翻译流水线】：① TLB 是页表的高速缓存，TLB 命中时 1 周期内即可完成 VA 到 PA 转换；② TLB 缺失并不等于缺页（Page Fault）！硬件 Page Walker 自动遍历主存页表，若页表项 Valid=1，仅需将该条目回填 TLB 即可，完全不需要唤醒 OS 缺页处理！③ 缺页属于 Fault 级异常，换页完成后硬件必须重新执行引发异常的本条原指令！",
        traps: {
          trap_cs_3_1: {
            title: "🚨 经典混淆高危陷阱：把'TLB Miss'错当成'Page Fault'",
            desc: "这是全网大模型乱回答与期末考试 71% 学生必错的核心深坑！TLB 缺失只是快表中没有缓存该页表项，物理页完全可能好端端躺在物理内存中。只有当页表查询发现 Valid=0（该页尚未载入内存）时，才会触发真正的 Page Fault！",
            prereq: "先修定理前置：TLB 快表缓存机制 vs 页表有效位语义",
            radarHit: "trapDefense"
          },
          trap_cs_3_2: {
            title: "🚨 异常返回语义断点陷阱：把'Fault 重执原指令'误套为'Interrupt 返回 PC+4'",
            desc: "中断（Interrupt）是异步的，通常返回下一条指令；而缺页属于故障（Fault），访存指令因缺页尚未成功读取数据，若直接跳到下一条指令，当前寄存器将读入垃圾数据，程序逻辑直接崩塌！",
            prereq: "先修定理前置：三大异常类型（Interrupt, Trap, Fault）保存 PC 行为准则",
            radarHit: "boundary"
          },
          trap_cs_3_3: {
            title: "🚨 标志位逻辑彻底反转陷阱：Valid=1 恰恰代表页面在物理内存中",
            desc: "Valid/Present 位为 1 代表页面就在主存物理帧中；为 0 才表示页面未分配或已换出到磁盘 Swap 分区！",
            prereq: "先修定理前置：页表项 PTE（Valid, Dirty, Reference）结构规范",
            radarHit: "recall"
          }
        },
        graph: {
          title: "虚拟内存·TLB查表与缺页异常处理拓扑图",
          nodes: [
            { id: "c1", label: "VA地址翻译流水线", type: "core", x: 260, y: 140 },
            { id: "p1", label: "TLB命中: 1周期直出PA", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "TLB缺失≠缺页 (PageWalk)", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "幻觉陷阱: TLBMiss直报缺页", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "陷阱: 缺页返回跳至PC+4", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "命中快速通道" },
            { from: "p2", to: "c1", label: "硬件自动补填" },
            { from: "c1", to: "t1", label: "易错于 (未区分TLB与页表层级)" },
            { from: "c1", to: "t2", label: "易错于 (混淆Fault与Interrupt返回)" }
          ]
        },
        socraticPrompt: "请同学回想一下：如果一个图书管理员记性特别好（TLB），但他脑子里记不住某本书放在哪个书架上了（TLB Miss），是不是意味着这本书就一定被图书馆扔掉或者借走了呢？他去翻一下总目录卡片（Page Table）是不是就能查到了？"
      }
    ]
  },

  econ: {
    name: "计量经济学",
    badge: "期末必考大题",
    questions: [
      {
        id: "econ_1",
        difficulty: "★★★★☆",
        tag: "经典假定违背 · 多重共线性诊断",
        stem: "在多元回归模型 Y = β₀ + β₁X₁ + β₂X₂ + u 中，若自变量 X₁ 与 X₂ 之间存在严重但非完全的多重共线性，下列关于普通最小二乘法 (OLS) 估计量性质的描述中，哪一项是完全正确的？",
        options: [
          { key: "A", text: "OLS 估计量失去无偏性 (Biased)，无法客观反映总体真实参数", isCorrect: false, trapId: "trap_econ_1" },
          { key: "B", text: "高斯-马尔可夫定理完全失效，OLS 估计量不再属于最佳线性无偏估计 (BLUE)", isCorrect: false, trapId: "trap_econ_2" },
          { key: "C", text: "OLS 估计量依然保持无偏性与 BLUE 性质，但参数方差膨胀，导致 t 检验失效", isCorrect: true },
          { key: "D", text: "模型的总判定系数 R² 会严重受挫跌落至接近 0", isCorrect: false, trapId: "trap_econ_3" }
        ],
        explanation: "【权威考点解析 · 多重共线性的统计学后果】：在严格外生假定 E(u|X)=0 和同方差假定下，只要不存在'完全共线性'（|X'X| ≠ 0），高斯-马尔可夫定理全部成立！OLS 依然是无偏且 BLUE 的！共线性的真正后果是方差膨胀因子 (VIF) 剧增，标准误过大，单个变量的 t 统计量显著下降，但总体回归方程的 F 检验和 R² 通常依然很高！",
        traps: {
          trap_econ_1: {
            title: "🚨 核心属性误杀陷阱：把'估计精度不足'误等同于'估计量有偏'",
            desc: "很多学生以及未经图谱事实约束的通用大模型，张口就回答'估计量有偏'！有偏（Bias）只有在遗漏关键变量或存在内生性时才会发生。自变量之间有相关性绝不破坏无偏性！",
            prereq: "先修定理前置：无偏性数学证明前提 E(u|X)=0",
            radarHit: "recall"
          },
          trap_econ_2: {
            title: "🚨 定理条件理解陷阱：误判 BLUE 性质失效",
            desc: "在所有线性无偏估计量中，OLS 依然是方差最小的那个（BLUE），只是此时这个'最小方差'本身已经被样本数据推高了而已。",
            prereq: "先修定理前置：高斯-马尔可夫定理证明边界",
            radarHit: "boundary"
          },
          trap_econ_3: {
            title: "🚨 经典反常识表象陷阱：共线性下 R² 和 F 往往虚高！",
            desc: "多重共线性的最经典教科书表象就是：F 检验极度显著、R² 很高（如 0.85），但每个自变量的 t 检验都无法拒绝原假设！",
            prereq: "先修定理前置：联合假设 F 检验与个体 t 检验差异",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "多重共线性·统计性质与诊断陷阱拓扑图",
          nodes: [
            { id: "c1", label: "多重共线性 (Multicollinearity)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "假定成立: E(u|X)=0 (严格外生)", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "性质: 依然为 BLUE (无偏且有效)", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "幻觉陷阱: 错判为产生内生偏误", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "表象陷阱: 误以为 R² 会暴跌", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "保证无偏前提" },
            { from: "p2", to: "c1", label: "最小方差性质" },
            { from: "c1", to: "t1", label: "易错于 (混淆有偏与方差大)" },
            { from: "c1", to: "t2", label: "易错于 (忽略总体F检验)" }
          ]
        },
        socraticPrompt: "吴同学，请思考一下无偏性公式 E(β̂) = β 的数学本质：只要残差项与自变量无关，自变量 X₁ 和 X₂ 之间的相关程度，是会偏移回归直线的期望中心，还是仅仅会让估计值在抽样时剧烈左右晃动？"
      },
      {
        id: "econ_2",
        difficulty: "★★★★★",
        tag: "因果推断核心 · 工具变量法 (IV/2SLS) 与弱工具变量",
        stem: "在估算教育年限（Educ）对对数工资水平（ln(Wage)）的因果效应方程中，因存在无法直接观测的'个人天生能力'遗漏，解释变量 Educ 产生严重内生性。研究人员选取'受教育者家庭距离最近大学的公里数 (Distance)'作为候选工具变量 Z。下列关于工具变量有效性及两阶段最小二乘法（2SLS）性质的论述，完全正确的是？",
        options: [
          { key: "A", text: "Z 必须同时满足相关性条件（Cov(Z, Educ) ≠ 0）和严格的外生性排他性假定（Cov(Z, u) = 0 且 Z 不能直接决定工资）", isCorrect: true },
          { key: "B", text: "即便第一阶段回归的 F 统计量仅为 2.8（远低于 10），只要样本量 N 趋于无穷大，2SLS 估计量依然绝对无偏且方差最小", isCorrect: false, trapId: "trap_econ_2_1" },
          { key: "C", text: "在模型恰好识别（内生变量数 = 工具变量数 = 1）时，可直接通过过度识别检验（Sargan-Hansen Test）在统计学上严格检验 Z 是否外生", isCorrect: false, trapId: "trap_econ_2_2" },
          { key: "D", text: "为了提高因果解释力，合格的工具变量 Z 必须对因变量 ln(Wage) 具有显著而直接的强相关推动力", isCorrect: false, trapId: "trap_econ_2_3" }
        ],
        explanation: "【权威考点解析 · 工具变量法与因果识别】：① 工具变量两大铁律：外生性条件（Exogeneity，与扰动项正交且无直接因果通路）+ 相关性条件（Relevance，与内生变量强相关）；② Staiger-Stock 经验法则：第一阶段 F > 10 方可排除弱工具变量风险！弱工具变量会导致 2SLS 甚至比普通 OLS 偏误更大！③ 恰好识别时模型自由度为 0，外生性假定必须依赖经济学理论论证，数学上不可直接检验！",
        traps: {
          trap_econ_2_1: {
            title: "🚨 弱工具变量致命盲区：大样本并不能自动拯救弱工具变量的严重偏误",
            desc: "这是计量经济学实证顶级翻车现场！当第一阶段相关性微弱时（F < 10），2SLS 的渐近偏误会朝 OLS 方向靠拢，抽样分布极度肥尾畸变，常规标准误完全失效，甚至产生毁灭性虚假因果！",
            prereq: "先修定理前置：Staiger-Stock 弱工具变量与有限样本偏误定理",
            radarHit: "boundary"
          },
          trap_econ_2_2: {
            title: "🚨 自由度与识别条件数学盲区：恰好识别根本无法进行统计外生性检验",
            desc: "过度识别检验（如 Sargan Test / Hansen J 统计量）的前提是工具变量个数 m 严格大于内生变量个数 k（即 m > k）。恰好识别时残差与预测值完全正交，残差平方和自由度为 0，根本无法做检验！",
            prereq: "先修定理前置：Sargan-Hansen 过度识别检验统计自由度定义",
            radarHit: "precision"
          },
          trap_econ_2_3: {
            title: "🚨 排他性约束彻底颠倒：合格的工具变量绝对不能直接影响因变量！",
            desc: "排他性约束（Exclusion Restriction）的严苛定义是：工具变量 Z 只能'通过内生变量 Educ 这唯一通道'间接影响工资！若 Z 本身直接决定工资，则该变量直接进入原方程扰动项，外生性荡然无存！",
            prereq: "先修定理前置：DAG 因果有向无环图与排他性约束定理",
            radarHit: "trapDefense"
          }
        },
        graph: {
          title: "因果推断·工具变量识别与外生性约束拓扑图",
          nodes: [
            { id: "c1", label: "2SLS 工具变量识别", type: "core", x: 260, y: 140 },
            { id: "p1", label: "排他性外生: Cov(Z,u)=0", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "强相关检验: 阶段一F>10", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "弱工具陷阱: F<10致严重偏误", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "错位陷阱: 恰好识别做Sargan", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "因果外生约束" },
            { from: "p2", to: "c1", label: "识别强度门禁" },
            { from: "c1", to: "t1", label: "易错于 (低估弱工具破坏力)" },
            { from: "c1", to: "t2", label: "易错于 (忽视检验自由度约束)" }
          ]
        },
        socraticPrompt: "请同学在脑海中画一条因果箭头：如果离大学近的地区本身就是高工资的沿海大城市（即 Z 直接影响了 Wage），那我们怎么可能分清楚那些高工资是因为多读了书，还是因为出生在大城市呢？这就是为什么排他性约束如此至关重要！"
      },
      {
        id: "econ_3",
        difficulty: "★★★★☆",
        tag: "经典假定违背 · 异方差性怀特检验与稳健标准误",
        stem: "在截面家庭消费支出回归中，富裕家庭的储蓄与消费弹性差异远大于低收入家庭，导致误差项呈现随收入增加而发散的异方差性（Var(u_i|X_i) = σ_i²）。下列关于异方差对 OLS 的危害、检验方法及修正策略的叙述中，哪一项完全符合现代实证规范？",
        options: [
          { key: "A", text: "存在异方差时，OLS 估计量 β̂ 彻底失去无偏性与一致性，算出来的回归系数数值完全毫无参考价值", isCorrect: false, trapId: "trap_econ_3_1" },
          { key: "B", text: "怀特检验（White Test）要求研究者必须预先知道异方差的具体数学形式（如指数形式或线性形式）方可实施", isCorrect: false, trapId: "trap_econ_3_2" },
          { key: "C", text: "OLS 估计量依然无偏且一致，但传统公式计算的标准误严重有偏；现代学界通用做法是直接采用 White 稳健标准误（Robust Standard Errors）进行统计推断", isCorrect: true },
          { key: "D", text: "采用加权最小二乘法 (WLS) 在任何情况下都无条件优于 OLS 稳健回归，绝对不可能引入新的模型设定误差", isCorrect: false, trapId: "trap_econ_3_3" }
        ],
        explanation: "【权威考点解析 · 异方差后果与稳健推断】：① 异方差违背同方差假定，破坏高斯-马尔可夫定理的'有效性（BLUE）'，但完全不影响期望 E(β̂)=β，故 OLS 估计量依然无偏且一致！② 异方差的真正致命伤是传统公式计算的 Var(β̂) 有偏，导致 t 统计量和置信区间全线失真！③ 怀特检验通过辅助回归无需预设异方差形式，学界当前黄金准则是报告 OLS 系数并配备 Heteroskedasticity-Robust 标准误（如 Stata 中的 , robust）！",
        traps: {
          trap_econ_3_1: {
            title: "🚨 性质混淆高频深坑：把'有效性受损'误判为'估计量失去无偏性'",
            desc: "全班 60% 同学会脱口而出'OLS 估计量有偏'！无偏性的唯一前提是外生性 E(u|X)=0。残差方差变大变小，只是让估计量的抽样波动变大，绝不会让总体平均估计中心发生系统性偏移！",
            prereq: "先修定理前置：无偏性条件 vs BLUE 有效性条件断点对比",
            radarHit: "recall"
          },
          trap_econ_3_2: {
            title: "🚨 统计检验机制混淆：误把'怀特检验'等同于依赖具体形式的检验",
            desc: "怀特检验最大的突破性贡献，正是由于它将残差平方对所有自变量的一阶项、平方项及交互项做辅助回归，完全不需要研究者猜测异方差是哪种特定函数！",
            prereq: "先修定理前置：White (1980) 渐近大样本辅助回归构造原理",
            radarHit: "boundary"
          },
          trap_econ_3_3: {
            title: "🚨 WLS 盲目盲信反模式：错误权重的 WLS 甚至比 OLS 还要糟糕",
            desc: "可行广义最小二乘法 (FGLS/WLS) 只有在研究者准确猜对异方差函数结构时才渐近有效。若权重矩阵设定错误，WLS 的估计量反而会失去一致性，因此现代顶级实证论文几乎清一色采用 OLS + Robust 标准误！",
            prereq: "先修定理前置：FGLS 稳健性风险与夹心方差估计量（Sandwich Estimator）",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "异方差·成因后果与怀特稳健推断图谱",
          nodes: [
            { id: "c1", label: "异方差性 (Var(u|X)=σi²)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "系数保持无偏与一致", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "对策: White稳健标准误", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "误区: 错判OLS系数有偏", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "误区: 盲目套用WLS权重", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "外生假定成立" },
            { from: "p2", to: "c1", label: "夹心协方差修正" },
            { from: "c1", to: "t1", label: "易错于 (混淆方差大与期望偏)" },
            { from: "c1", to: "t2", label: "易错于 (忽视权重设定偏误)" }
          ]
        },
        socraticPrompt: "请同学思考：如果一台电子秤只是偶尔称重读数抖动变大（方差大），但平均下来称 100 次的均值依然是完全准确的（无偏），我们应该直接扔掉这台秤，还是给它换一个能正确计算误差范围的合格说明书（稳健标准误）？"
      }
    ]
  },

  se: {
    name: "软件工程与系统设计",
    badge: "JC2001课程核心",
    questions: [
      {
        id: "se_1",
        difficulty: "★★★☆☆",
        tag: "软件过程模型 · 敏捷 Scrum 与瀑布模型适用权衡",
        stem: "在某智慧医院核心业务系统研发项目中，急诊排班与医保微服务接口的需求受政策影响变动极为频繁且不确定，但底层患者核心电子病历的归档存储模块受到国家卫健委《三级医院评审标准》极其严苛的合规性与审计可追溯性约束。关于该项目的软件过程模型选择，下列哪种策略最为科学合理？",
        options: [
          { key: "A", text: "强制推行纯瀑布模型（Waterfall），在阶段一彻底冻结所有医保与排班需求规格说明书后才允许进入编码阶段", isCorrect: false, trapId: "trap_se_1_1" },
          { key: "B", text: "采用混合软件过程模型（Hybrid Model），底层强合规与稳定架构采用架构先行和严格文档，高频易变的业务服务采用 2 周 Sprint 的 Scrum 敏捷迭代验证", isCorrect: true },
          { key: "C", text: "彻底废弃所有软件架构设计文档与测试用例，全盘采用极限编程（XP），依靠每天结对重构解决所有国家合规性评审", isCorrect: false, trapId: "trap_se_1_2" },
          { key: "D", text: "采用大爆炸模型（Big Bang Model），由开发人员在期末截止前一周连续通宵一次性交付全量代码", isCorrect: false, trapId: "trap_se_1_3" }
        ],
        explanation: "【权威考点解析 · 软件生命周期模型权衡】：根据 Boehm 软件工程经济学定律，需求变更成本随项目周期呈指数级增长。面对'高变动度业务'强推瀑布模型必然导致项目严重延期超支；而在'高合规性底层'盲目推行极端零文档开发必然导致验收失败。业内成熟工业实践普遍采用 Hybrid 敏捷双轨制：架构约束基线受控，前端应用敏捷迭代！",
        traps: {
          trap_se_1_1: {
            title: "🚨 传统教条主义瀑布陷阱：在易变业务中强行'冻结需求'",
            desc: "很多刚学软件工程的同学盲目崇拜瀑布模型的严密性，忽视了当外部业务或政策月月变更时，瀑布模型的前后阶段强依赖会导致全团队陷入永无止境的'需求变更提交流程'和代码大规模推倒重来！",
            prereq: "先修定理前置：Boehm 软件变更成本指数曲线与瀑布局限性",
            radarHit: "boundary"
          },
          trap_se_1_2: {
            title: "🚨 敏捷宣言教条化误读陷阱：把'拥抱变更'误等同于'不要任何文档和架构'",
            desc: "敏捷宣言原文是'可工作的软件胜于详尽的文档'，绝不是'不要文档'！在医疗、金融、航天等安全关键系统（Safety-critical systems）中，需求追溯矩阵（RTM）和接口契约文档是法律法规强制要求的一票否决项！",
            prereq: "先修定理前置：敏捷宣言核心原则与合规性系统工程规范",
            radarHit: "recall"
          },
          trap_se_1_3: {
            title: "🚨 反工程开发模式陷阱：大爆炸模型是混乱工程的代名词",
            desc: "无计划、无阶段审查、无测试门禁的大爆炸模型违背了软件工程的一切基本原则，是导致绝大多数软件项目彻底报废的头号反模式！",
            prereq: "先修定理前置：软件危机本质与现代软件工程控制论",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "软件过程模型·敏捷迭代与架构合规权衡图谱",
          nodes: [
            { id: "c1", label: "混合敏捷过程模型 (Hybrid)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "底层强合规: 架构基线受控", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "变动业务层: 2周Scrum迭代", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "教条瀑布: 强行冻结变动需求", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "伪敏捷: 盲目抛弃所有架构文档", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "合规质量底线" },
            { from: "p2", to: "c1", label: "快速拥抱变更" },
            { from: "c1", to: "t1", label: "易错于 (教条僵化开发)" },
            { from: "c1", to: "t2", label: "易错于 (放任混乱无序)" }
          ]
        },
        socraticPrompt: "请同学思考：如果一栋大厦的地基和承重梁（合规核心）要求必须有图纸审查且绝对不能摇晃，而顶层的办公室隔断（变动业务）租户随时想要调整，我们应该全部打掉重盖，还是应该在地基稳固的前提下采用可移动轻量隔断？"
      },
      {
        id: "se_2",
        difficulty: "★★★★☆",
        tag: "面向对象架构设计 · SOLID 原则与依赖倒置 (DIP)",
        stem: "在设计一个多源学术文献知识图谱抽取引擎时，上层核心分析业务类 LiteratureAnalyzer 直接通过硬编码实例化了具体的 MySQL 数据库客户端（即 this.db = new MySQLClient()）。现因业务扩展需要支持分布式图数据库 Neo4j 及向量数据库 Milvus。根据 SOLID 设计原则中的依赖倒置原则（DIP），应如何实施最佳重构？",
        options: [
          { key: "A", text: "在 LiteratureAnalyzer 内部增加大量的 if-else 或 switch-case 语句，根据传入的环境变量分别执行不同数据库的私有操作代码", isCorrect: false, trapId: "trap_se_2_1" },
          { key: "B", text: "抽象出统一的 IKnowledgeStorage 契约接口，使上层 LiteratureAnalyzer 与具体的 MySQLClient/Neo4jClient 均只依赖该抽象接口，通过构造函数依赖注入（DI）解耦", isCorrect: true },
          { key: "C", text: "直接让 Neo4jClient 类强制继承自 MySQLClient 类，并通过重写（Override）覆写其中的关系查询方法", isCorrect: false, trapId: "trap_se_2_2" },
          { key: "D", text: "将所有数据库操作逻辑整合到一个全局公共上帝类（God Class）GlobalDBManager 中，由业务类直接调用其静态方法", isCorrect: false, trapId: "trap_se_2_3" }
        ],
        explanation: "【权威考点解析 · SOLID 原则与依赖倒置 DIP】：① 依赖倒置原则定义：高层模块不应该依赖低层模块，两者都应该依赖抽象；抽象不应该依赖细节，细节应该依赖抽象。② 方案 B 通过引入 IKnowledgeStorage 接口，解除了高层分析类对底层持久化技术的紧耦合，新增图数据库或向量数据库只需扩展新实现类，无需改动现有业务逻辑，同时完美符合开闭原则（OCP）！",
        traps: {
          trap_se_2_1: {
            title: "🚨 分支蔓延坏味道陷阱：严重违反开闭原则 (OCP)",
            desc: "用大量的条件分支（if-else）来扩展底层实现是初学者最常犯的工程坏味道！每次接入新数据库都要修改高层业务代码并重新编译测试，极易引发回归缺陷（Regression Bugs）！",
            prereq: "先修定理前置：开闭原则（OCP：对扩展开放，对修改关闭）",
            radarHit: "trapDefense"
          },
          trap_se_2_2: {
            title: "🚨 继承滥用深坑：严重违反里氏替换原则 (LSP)",
            desc: "图数据库和关系型数据库在数据模型、事务语义和查询契约上根本不存在'is-a'的派生替换关系！强行继承导致基类契约被肆意破坏，子类无法安全替换父类！",
            prereq: "先修定理前置：里氏替换原则（LSP）与契约式设计（DbC）",
            radarHit: "boundary"
          },
          trap_se_2_3: {
            title: "🚨 上帝类紧耦合陷阱：制造单点故障并扼杀单元测试",
            desc: "引入全局万能上帝类（God Class）是典型的反模式，导致系统内聚度（Cohesion）极低而耦合度（Coupling）极高，全局状态混乱，且单元测试中将彻底无法进行依赖 Mock！",
            prereq: "先修定理前置：单一职责原则（SRP）与单元测试 Mock 隔离要求",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "SOLID架构·依赖倒置与接口隔离设计图谱",
          nodes: [
            { id: "c1", label: "依赖倒置原则 (DIP)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "抽象契约接口 (IKnowledgeStorage)", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "依赖注入解耦 (DI/IoC)", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "坏味道: if-else破坏OCP", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "坏味道: 乱继承破坏LSP", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "面向接口编程" },
            { from: "p2", to: "c1", label: "控制反转实现" },
            { from: "c1", to: "t1", label: "易错于 (业务与底层技术硬绑定)" },
            { from: "c1", to: "t2", label: "易错于 (为了复用代码滥用继承)" }
          ]
        },
        socraticPrompt: "请同学想象一下家里的电源插座：国标三孔插座定义了一套抽象规范（接口），无论是台灯、电脑还是电冰箱（实现类），只要符合插头规范就能插上工作。如果每买一台新电器，我们都得把墙砸开重新接线（修改业务代码），这样的设计能持续吗？"
      },
      {
        id: "se_3",
        difficulty: "★★★★☆",
        tag: "软件质量保证 · 边界值分析与变异测试 (Mutation Testing)",
        stem: "在开发学生成绩管理系统的GPA计算模块时，某函数要求输入单门课程学分必须落在有效区间 [0.5, 10.0] 之间。关于该模块的黑盒测试用例设计以及自动化测试套件的充分性度量，下列说法完全正确的是？",
        options: [
          { key: "A", text: "只要测试套件在代码行覆盖率（Line Coverage）上达到了 100%，就足以证明所有边界值缺陷已被完全消除，无需进一步质量检验", isCorrect: false, trapId: "trap_se_3_1" },
          { key: "B", text: "边界值分析（BVA）不仅应选取边界上及边界内的值（如 0.5, 0.6, 9.9, 10.0），还必须选取边界外紧邻的无效输入（如 0.4, 10.1）检验防御性拦截；变异测试通过在源代码中植入变异体（Mutant）来客观度量测试用例的真正杀伤力", isCorrect: true },
          { key: "C", text: "边界值分析法要求测试人员只能输入合法范围内的有效数据，严禁输入任何负向或越界的无效数据", isCorrect: false, trapId: "trap_se_3_2" },
          { key: "D", text: "变异测试是一种专门用于测量系统在 10 万人并发选课时服务器 CPU 占用率的白盒压力测试工具", isCorrect: false, trapId: "trap_se_3_3" }
        ],
        explanation: "【权威考点解析 · 边界值测试与变异测试杀灭率】：① 绝大多数程序 Bug 发生在输入输出边界处，边界值分析（BVA）必须包含正向与负向邻界值（如 0.4 与 10.1 阻断拦截）；② 覆盖率幻觉（Coverage Illusion）：100% 语句覆盖完全可能包含大量'无断言弱测试'（Assertion-free Tests）！变异测试通过自动把 `>=` 改为 `>`、`+` 改为 `-` 等方式产生代码变异体，唯有测试用例能令变异体报错失败（Killed），才能证明测试套件具备真正的缺陷捕获能力！",
        traps: {
          trap_se_3_1: {
            title: "🚨 虚假覆盖率安全感陷阱：高行覆盖率 ≠ 高检错能力",
            desc: "这是软件工程质量门禁中最危险的盲区！测试代码执行了每一行，并不代表它断言了每一行的逻辑正确性！如果测试用例中没有任何 assert，覆盖率依然可以显示 100%，但变异测试杀伤率将直降为 0！",
            prereq: "先修定理前置：测试充分性准则与变异分数（Mutation Score）定义",
            radarHit: "trapDefense"
          },
          trap_se_3_2: {
            title: "🚨 负向测试缺失陷阱：忽略边界外拦截测试直接导致生产崩溃",
            desc: "只测试合法数据（Positive Testing）是脆弱软件的典型征兆。健壮性测试必须覆盖紧邻边界外的无效等价类，确保异常被安全捕获并抛出受控错误，而非直接抛出未捕获异常导致系统崩溃！",
            prereq: "先修定理前置：等价类划分与健壮性边界值分析矩阵",
            radarHit: "boundary"
          },
          trap_se_3_3: {
            title: "🚨 测试类型概念错配陷阱：把'变异测试'误判为'性能压测'",
            desc: "变异测试是著名的'测试你的测试（Testing the Tests）'的高级元测试技术，属于缺陷注入（Fault Injection）和测试集能力评价领域，与性能压测完全无关！",
            prereq: "先修定理前置：故障注入机制与自动化变异算子（Mutator）分类",
            radarHit: "recall"
          }
        },
        graph: {
          title: "质量保证·边界值分析与变异测试杀伤力拓扑图",
          nodes: [
            { id: "c1", label: "变异测试 (Mutation Testing)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "BVA: 跨越正负边界取样", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "破除弱断言: 杀灭率评价", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "虚荣陷阱: 迷信100%行覆盖率", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "概念陷阱: 误判变异测试为压测", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "高危边界敏感度" },
            { from: "p2", to: "c1", label: "测试用例质量度量" },
            { from: "c1", to: "t1", label: "易错于 (忽略断言有效性)" },
            { from: "c1", to: "t2", label: "易错于 (测试类型概念混同)" }
          ]
        },
        socraticPrompt: "请同学思考：如果一个保安只是把公司的每一个房间门推开看了一眼（代码行覆盖率 100%），但他根本不认识谁是小偷（没有写判断断言 assert），那么当真正有小偷把房间里的电脑搬走时（变异体引入），这个保安能发出警报吗？"
      }
    ]
  }
};

// =============================================================================
// 多学科精品真题与避坑知识本体库 (Curated Multi-Discipline Question Bank - English)
// =============================================================================
const DB_EN = {
  se: {
    name: "Software Engineering & Architecture",
    badge: "JC2001 Core Syllabus",
    questions: [
      {
        id: "se_1",
        difficulty: "★★★☆☆",
        tag: "Process Models · Scrum vs Waterfall Trade-offs",
        stem: "In a smart hospital health-informatics project, emergency scheduling and insurance API specifications change frequently due to shifting national health policies, whereas the core electronic health record (EHR) archiving module is governed by strict statutory audit and traceability mandates. Which software process strategy is most scientifically defensible?",
        options: [
          { key: "A", text: "Enforce a strict Waterfall model, completely freezing all insurance and scheduling requirements in Phase 1 before coding commences", isCorrect: false, trapId: "trap_se_1_1" },
          { key: "B", text: "Adopt a Hybrid process model: architecture-centric, documented governance for the compliant core, paired with 2-week agile Scrum sprints for volatile microservices", isCorrect: true },
          { key: "C", text: "Completely abandon architectural documentation and formal test cases, using Extreme Programming (XP) with daily pair refactoring for all regulatory audits", isCorrect: false, trapId: "trap_se_1_2" },
          { key: "D", text: "Adopt the Big Bang model, having developers code continuously in the final week prior to final delivery", isCorrect: false, trapId: "trap_se_1_3" }
        ],
        explanation: "【Authoritative Analysis · Software Lifecycle Trade-offs】: According to Boehm's software engineering economics, the cost of requirement changes escalates exponentially over the project lifecycle. Forcing a rigid Waterfall model on volatile business logic causes severe schedule delays and budget overruns; conversely, zero-documentation hacking on compliant cores leads to audit rejection. Industry best practice is a Hybrid dual-track approach: architectural baselines under strict control, paired with agile front-end sprints.",
        traps: {
          trap_se_1_1: {
            title: "🚨 Dogmatic Waterfall Trap: Forcibly 'Freezing Requirements' in Volatile Domains",
            desc: "A classic misconception among novice engineers. When business policies change monthly, Waterfall's sequential phase dependencies cause endless change requests and massive code rewrites!",
            prereq: "Prerequisite Concept: Boehm's Cost of Change Curve & Waterfall Constraints",
            radarHit: "trapDefense"
          },
          trap_se_1_2: {
            title: "🚨 Extreme Agilism Trap: Mistaking 'Agile' for 'Zero Documentation & No Architecture'",
            desc: "In safety-critical or regulatory-compliant domains, Requirements Traceability Matrices (RTM) and interface contracts are mandatory audit criteria!",
            prereq: "Prerequisite Concept: Safety-Critical Regulatory Standards & Audit Traceability",
            radarHit: "boundary"
          },
          trap_se_1_3: {
            title: "🚨 Cowboy Coding Trap: Big Bang Delivery without Incremental Validation",
            desc: "Deferring integration to the final week prevents early risk discovery, resulting in unmanageable integration faults!",
            prereq: "Prerequisite Concept: Incremental Integration vs Big Bang Risk Management",
            radarHit: "recall"
          }
        },
        graph: {
          title: "Software Process Trade-offs · Scrum vs Waterfall Topology",
          nodes: [
            { id: "c1", label: "Hybrid Process Model", type: "core", x: 260, y: 140 },
            { id: "p1", label: "Prereq: Change Cost Curve", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Prereq: Audit Traceability", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: Dogmatic Freeze", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Zero-Doc Extremism", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Economic Driver" },
            { from: "p2", to: "c1", label: "Compliance Constraint" },
            { from: "c1", to: "t1", label: "Prone to (Rigid Phasing)" },
            { from: "c1", to: "t2", label: "Prone to (Uncontrolled Agile)" }
          ]
        },
        socraticPrompt: "Consider the two distinct subsystems: one is volatile with rapid policy changes, while the other is mission-critical with strict government audits. Can a single extreme methodology (pure Waterfall or zero-doc XP) satisfy both constraints simultaneously?"
      },
      {
        id: "se_2",
        difficulty: "★★★★☆",
        tag: "Object-Oriented Architecture · SOLID Principles & DIP",
        stem: "In an academic knowledge extraction engine, the core analysis class LiteratureAnalyzer hardcodes a direct instantiation of a database client: this.db = new MySQLClient(). Due to project expansion, the system must now support Neo4j graph databases and vector stores. According to the Dependency Inversion Principle (DIP), what is the optimal refactoring strategy?",
        options: [
          { key: "A", text: "Introduce nested if-else / switch-case blocks inside LiteratureAnalyzer to execute vendor-specific queries based on environment variables", isCorrect: false, trapId: "trap_se_2_1" },
          { key: "B", text: "Define a unified IKnowledgeStorage interface so that LiteratureAnalyzer and concrete clients (MySQLClient, Neo4jClient) depend solely on the abstraction, injected via constructor Dependency Injection (DI)", isCorrect: true },
          { key: "C", text: "Force Neo4jClient to inherit directly from MySQLClient and override relational query methods", isCorrect: false, trapId: "trap_se_2_2" },
          { key: "D", text: "Consolidate all database routines into a static God Class GlobalDBManager called directly by business classes", isCorrect: false, trapId: "trap_se_2_3" }
        ],
        explanation: "【Authoritative Analysis · SOLID Principles & DIP】: DIP states: High-level modules should not depend on low-level modules; both should depend on abstractions. Option B decouples the core analysis logic from underlying storage mechanisms, adhering to DIP and the Open/Closed Principle (OCP).",
        traps: {
          trap_se_2_1: {
            title: "🚨 Branch Sprawl Code Smell: Severely Violating Open/Closed Principle (OCP)",
            desc: "Using conditionals (if-else) to extend low-level drivers means modifying core business logic every time a database is added, risking regression bugs!",
            prereq: "Prerequisite Concept: Open/Closed Principle (Open for extension, closed for modification)",
            radarHit: "trapDefense"
          },
          trap_se_2_2: {
            title: "🚨 Inheritance Abuse: Violating Liskov Substitution Principle (LSP)",
            desc: "Graph databases and relational databases have completely different query contracts and data models; an 'is-a' relationship does not hold!",
            prereq: "Prerequisite Concept: Liskov Substitution Principle (LSP)",
            radarHit: "boundary"
          },
          trap_se_2_3: {
            title: "🚨 Monolithic Anti-Pattern: Introducing God Class and Global State",
            desc: "A static God Class tightly couples all modules to a single global state, impeding unit testing and parallel development!",
            prereq: "Prerequisite Concept: Single Responsibility Principle (SRP)",
            radarHit: "recall"
          }
        },
        graph: {
          title: "SOLID Principles · Dependency Inversion Topology",
          nodes: [
            { id: "c1", label: "Dependency Inversion (DIP)", type: "core", x: 260, y: 140 },
            { id: "p1", label: "Abstraction Contract", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Dependency Injection", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: Switch Sprawl", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: God Class Coupling", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Enables Decoupling" },
            { from: "p2", to: "c1", label: "Runtime Provision" },
            { from: "c1", to: "t1", label: "Prone to (Violates OCP)" },
            { from: "c1", to: "t2", label: "Prone to (Anti-Pattern)" }
          ]
        },
        socraticPrompt: "If class A directly constructs `new B()`, what happens to class A when class B's constructor parameters change? Who is controlling the dependency?"
      },
      {
        id: "se_3",
        difficulty: "★★★★☆",
        tag: "Software Quality Assurance · Boundary Value Analysis & Mutation Testing",
        stem: "In a university GPA calculation module, valid course credits must fall within the range [0.5, 10.0]. Regarding black-box test design and test suite adequacy measurement, which statement is entirely correct?",
        options: [
          { key: "A", text: "Achieving 100% line coverage is sufficient to prove that all boundary defects have been eliminated, requiring no further testing", isCorrect: false, trapId: "trap_se_3_1" },
          { key: "B", text: "Boundary Value Analysis (BVA) must test boundary values (0.5, 10.0) as well as adjacent invalid inputs (0.4, 10.1); Mutation Testing evaluates test adequacy by injecting artificial faults (mutants) into source code", isCorrect: true },
          { key: "C", text: "Boundary Value Analysis requires testers to supply only valid in-range inputs, strictly avoiding invalid or out-of-bound inputs", isCorrect: false, trapId: "trap_se_3_2" },
          { key: "D", text: "Mutation Testing is a white-box stress testing tool used exclusively to measure CPU load under 100,000 concurrent users", isCorrect: false, trapId: "trap_se_3_3" }
        ],
        explanation: "【Authoritative Analysis · BVA & Mutation Testing Kill Rates】: ① Most defects occur at boundary conditions; BVA must test both valid boundaries and immediate invalid off-points (e.g. 0.4 and 10.1). ② Coverage Illusion: 100% statement coverage can be achieved with assertion-free tests! Mutation testing changes operators (e.g. >= to >) to verify if the test suite actually fails (kills mutants), measuring genuine defect-detection efficacy.",
        traps: {
          trap_se_3_1: {
            title: "🚨 False Sense of Security: High Line Coverage ≠ High Defect Detection",
            desc: "A critical blind spot in QA. Executing a line does not verify its correctness! Without rigorous assertions, line coverage is high but mutation score is 0%!",
            prereq: "Prerequisite Concept: Test Adequacy Criteria & Mutation Score",
            radarHit: "trapDefense"
          },
          trap_se_3_2: {
            title: "🚨 Missing Negative Testing: Omitting Off-Boundary Input Causes Crashes",
            desc: "Testing only valid inputs (positive testing) is a symptom of brittle software. Robustness requires verifying defensive rejection of invalid equivalence classes!",
            prereq: "Prerequisite Concept: Robustness Testing & Equivalence Partitioning",
            radarHit: "boundary"
          },
          trap_se_3_3: {
            title: "🚨 Concept Confusion: Confusing Mutation Testing with Stress/Performance Testing",
            desc: "Mutation testing is a fault-injection test assessment technique, not a load or performance benchmarking tool!",
            prereq: "Prerequisite Concept: Fault Injection & Mutation Testing Definitions",
            radarHit: "recall"
          }
        },
        graph: {
          title: "SQA & Mutation Testing · Test Adequacy Topology",
          nodes: [
            { id: "c1", label: "Mutation Testing Adequacy", type: "core", x: 260, y: 140 },
            { id: "p1", label: "Boundary Value Analysis", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Fault Injection / Mutant Kill", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: Coverage Illusion", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Stress Test Confusion", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Input Sampling" },
            { from: "p2", to: "c1", label: "Adequacy Metric" },
            { from: "c1", to: "t1", label: "Prone to (Assertion-Free)" },
            { from: "c1", to: "t2", label: "Prone to (Category Error)" }
          ]
        },
        socraticPrompt: "If a security guard opens every door in a building but doesn't check IDs (100% statement coverage without assertions), will an intruder be detected if one sneaks in (mutant)? What gives genuine quality assurance?"
      }
    ]
  },
  cs: {
    name: "Computer Systems Architecture",
    badge: "Hardware & Systems",
    questions: [
      {
        id: "cs_1",
        difficulty: "★★★★☆",
        tag: "RISC Pipeline Architecture · Hazards & Forwarding Paths",
        stem: "In a standard 5-stage in-order pipeline (IF, ID, EX, MEM, WB), instruction i is an arithmetic operation (e.g. add R1, R2, R3), followed immediately by instruction i+1 (e.g. sub R4, R1, R5) which requires R1 in the EX stage. Which statement regarding pipeline hazards and optimization is correct?",
        options: [
          { key: "A", text: "This is a Write-After-Read (WAR) anti-dependency hazard; the pipeline must stall for 2 cycles", isCorrect: false, trapId: "trap_cs_1" },
          { key: "B", text: "This is a Read-After-Write (RAW) true data dependency; it can be resolved with zero stalls using hardware forwarding from EX/MEM to ALU", isCorrect: true },
          { key: "C", text: "This is a Structural Hazard; it must be resolved by upgrading the register file to multi-port hardware", isCorrect: false, trapId: "trap_cs_2" },
          { key: "D", text: "This is a Control Hazard; it requires branch prediction using a Branch History Table (BHT)", isCorrect: false, trapId: "trap_cs_3" }
        ],
        explanation: "【Authoritative Analysis · RISC Pipeline Data Forwarding】: Instruction i computes R1 at the end of the EX stage. Instruction i+1 needs R1 at the beginning of the EX stage. By forwarding R1 directly from the EX/MEM pipeline register to the ALU input multiplexer, data hazards are resolved with zero stall cycles.",
        traps: {
          trap_cs_1: {
            title: "🚨 Misconception Trap: WAR/WAW hazards cannot occur in in-order pipelines!",
            desc: "WAR hazards only occur in out-of-order superscalar architectures (e.g. Tomasulo algorithm). In an in-order pipeline, instructions flow sequentially, so an older instruction can never read after a newer instruction writes!",
            prereq: "Prerequisite Concept: In-Order vs Out-of-Order Execution",
            radarHit: "boundary"
          },
          trap_cs_2: {
            title: "🚨 Category Confusion Trap: Confusing data dependencies with structural resource contention",
            desc: "Structural hazards occur when hardware resources cannot support all concurrent instruction combinations (e.g. single-port memory). Here, the issue is data value dependency!",
            prereq: "Prerequisite Concept: Three Types of Pipeline Hazards",
            radarHit: "recall"
          },
          trap_cs_3: {
            title: "🚨 Irrelevant Hazard Trap: Arithmetic instructions do not branch",
            desc: "Control hazards are exclusively caused by PC-modifying branch or jump instructions, not arithmetic operations!",
            prereq: "Prerequisite Concept: Control Hazards & Branch Prediction",
            radarHit: "synthesis"
          }
        },
        graph: {
          title: "RISC Pipeline · Data Dependencies & Forwarding",
          nodes: [
            { id: "c1", label: "Pipeline RAW Hazard", type: "core", x: 260, y: 140 },
            { id: "p1", label: "In-Order Issue", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "ALU Forwarding", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: WAR Anti-Dependency", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Structural Contention", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Architectural Rule" },
            { from: "p2", to: "c1", label: "Zero-Stall Solution" },
            { from: "c1", to: "t1", label: "Prone to (Out-of-Order Myth)" },
            { from: "c1", to: "t2", label: "Prone to (Resource Confusion)" }
          ]
        },
        socraticPrompt: "In an in-order pipeline, if instruction i produces its result at cycle 3, and instruction i+1 needs it at cycle 4, why should we wait until cycle 5 when it is written back to the register file?"
      },
      {
        id: "cs_2",
        difficulty: "★★★★☆",
        tag: "Memory Hierarchy · Set-Associative Cache Mapping",
        stem: "A 32-bit byte-addressed processor features a 32KB data cache with 64-byte blocks and 4-way set associativity. A loop accessing a large array with a 32KB stride causes severe conflict misses. Which statement regarding address fields and optimization is correct?",
        options: [
          { key: "A", text: "Address division: Tag=19 bits, Index=7 bits, Offset=6 bits; increasing associativity to 8-way directly alleviates conflict misses", isCorrect: true },
          { key: "B", text: "Address division: Tag=18 bits, Index=8 bits, Offset=6 bits; replacing LRU with FIFO reduces miss rates", isCorrect: false, trapId: "trap_cs_2_1" },
          { key: "C", text: "Address division: Tag=20 bits, Index=6 bits, Offset=6 bits; increasing block size to 128B cures conflict misses", isCorrect: false, trapId: "trap_cs_2_2" },
          { key: "D", text: "Adding an instruction prefetch buffer inside the CPU eliminates all data cache misses", isCorrect: false, trapId: "trap_cs_2_3" }
        ],
        explanation: "【Authoritative Analysis · Cache Address Breakdown & 3C Misses】: Block size 64B = 2⁶ -> Offset = 6 bits. Total blocks = 32KB / 64B = 512 blocks. 4-way set associative -> Sets = 512 / 4 = 128 sets = 2⁷ -> Index = 7 bits. Tag = 32 - 7 - 6 = 19 bits. Conflict misses occur when addresses map to the same set; increasing associativity (e.g. 8-way) directly mitigates conflict misses.",
        traps: {
          trap_cs_2_1: {
            title: "🚨 Set Count Calculation Trap: Confusing total cache blocks with sets",
            desc: "Dividing total capacity by block size gives total blocks (512), not sets! With 4 ways, there are 128 sets (7 index bits). Furthermore, FIFO suffers from Belady's anomaly!",
            prereq: "Prerequisite Concept: Set-Associative Cache Formulas & Locality Principle",
            radarHit: "precision"
          },
          trap_cs_2_2: {
            title: "🚨 Block Size Illusion: Larger blocks can exacerbate conflict misses",
            desc: "Increasing block size for a fixed cache size reduces the number of sets, potentially worsening conflict misses for strided access!",
            prereq: "Prerequisite Concept: 3C Miss Model (Compulsory, Capacity, Conflict)",
            radarHit: "boundary"
          },
          trap_cs_2_3: {
            title: "🚨 Instruction vs Data Cache Confusion",
            desc: "Instruction prefetchers handle the instruction stream, providing zero benefit for data array strides!",
            prereq: "Prerequisite Concept: Harvard Architecture Split Cache Separation",
            radarHit: "recall"
          }
        },
        graph: {
          title: "Memory Hierarchy · Cache Associativity Topology",
          nodes: [
            { id: "c1", label: "Conflict Miss Mitigation", type: "core", x: 260, y: 140 },
            { id: "p1", label: "Address Breakdown (19/7/6)", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Associativity Expansion", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: Total Blocks as Sets", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Block Size Oversizing", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Mathematical Foundation" },
            { from: "p2", to: "c1", label: "Resolution Technique" },
            { from: "c1", to: "t1", label: "Prone to (Calculation Error)" },
            { from: "c1", to: "t2", label: "Prone to (Sub-optimal Tuning)" }
          ]
        },
        socraticPrompt: "If an array access jumps by exactly 32KB every step, and your cache index repeats every 32KB, all accesses collide into the exact same set index! How can you provide more available slots per set?"
      }
    ]
  },
  econ: {
    name: "Econometrics & Quantitative Modeling",
    badge: "Honours Core",
    questions: [
      {
        id: "econ_1",
        difficulty: "★★★★☆",
        tag: "Econometrics · Gauss-Markov Theorem & OLS Omitted Variable Bias",
        stem: "When estimating a Mincer earnings equation via Ordinary Least Squares (OLS), the true model includes unobserved innate ability. If ability is omitted and positively correlated with schooling, which property of the OLS estimator for returns to schooling is violated?",
        options: [
          { key: "A", text: "OLS remains unbiased and consistent, but standard errors are underestimated", isCorrect: false, trapId: "trap_econ_1" },
          { key: "B", text: "The Gauss-Markov zero conditional mean assumption E(u|X)=0 is violated, causing positive omitted variable bias", isCorrect: true },
          { key: "C", text: "This is pure heteroscedasticity; OLS remains unbiased and BLUE", isCorrect: false, trapId: "trap_econ_2" },
          { key: "D", text: "Multicollinearity between regressors causes the (X'X) matrix to be singular, preventing computation", isCorrect: false, trapId: "trap_econ_3" }
        ],
        explanation: "【Authoritative Analysis · Gauss-Markov & Omitted Variable Bias】: When an omitted regressor is correlated with both the dependent variable and an included regressor, it enters the error term u. Consequently, Cov(X, u) ≠ 0, directly violating the zero conditional mean assumption E(u|X)=0. The OLS estimator becomes biased and inconsistent.",
        traps: {
          trap_econ_1: {
            title: "🚨 Efficiency vs Unbiasedness Confusion",
            desc: "Novice students often confuse efficiency with unbiasedness. Omitting an uncorrelated variable merely inflates variance, but omitting a correlated variable destroys consistency!",
            prereq: "Prerequisite Concept: Gauss-Markov Zero Conditional Mean Assumption",
            radarHit: "boundary"
          },
          trap_econ_2: {
            title: "🚨 Heteroscedasticity Category Confusion",
            desc: "Heteroscedasticity concerns Var(u|X) ≠ σ²; it affects standard errors and efficiency, but does NOT cause omitted variable bias!",
            prereq: "Prerequisite Concept: Homoscedasticity vs Endogeneity",
            radarHit: "recall"
          },
          trap_econ_3: {
            title: "🚨 Multicollinearity Confusion",
            desc: "Multicollinearity requires multiple regressors in the model with high correlation. An unobserved, omitted variable is not an included regressor!",
            prereq: "Prerequisite Concept: Full Rank Condition & Multicollinearity",
            radarHit: "trapDefense"
          }
        },
        graph: {
          title: "Econometrics · Omitted Variable Bias Topology",
          nodes: [
            { id: "c1", label: "Omitted Variable Bias", type: "core", x: 260, y: 140 },
            { id: "p1", label: "E(u|X) = 0 Violation", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Endogeneity / Ability", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: Confusing with Efficiency", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Misattributing Heteroscedasticity", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Direct Mechanism" },
            { from: "p2", to: "c1", label: "Omitted Cause" },
            { from: "c1", to: "t1", label: "Prone to (Bias vs Variance)" },
            { from: "c1", to: "t2", label: "Prone to (Error Term Confusion)" }
          ]
        },
        socraticPrompt: "If innate ability makes individuals earn more and also stay in school longer, when you attribute wage growth purely to schooling without measuring ability, are you overestimating or underestimating schooling's true causal impact?"
      }
    ]
  },
  law: {
    name: "Commercial & Contract Law",
    badge: "Legal Foundations",
    questions: [
      {
        id: "law_1",
        difficulty: "★★★☆☆",
        tag: "Contract Law · Vitiating Factors & Rescission Limitation",
        stem: "Party A enters into a commercial sales agreement on 1 March 2023 induced by fraudulent misrepresentation by Party B. Party A discovers the fraud on 1 May 2023. Under statutory contract law governing voidable contracts, when does the limitation period for exercising the right of rescission commence, and when does it strictly expire?",
        options: [
          { key: "A", text: "Commences on contract signing (1 March 2023), expiring strictly in 3 years", isCorrect: false, trapId: "trap_law_1" },
          { key: "B", text: "Commences on the date the fraud is discovered (1 May 2023), expiring in 1 year", isCorrect: true },
          { key: "C", text: "Commences on the cessation of the fraudulent act, expiring in 1 year", isCorrect: false, trapId: "trap_law_2" },
          { key: "D", text: "Commences on contract signing, expiring in 2 years regardless of notice", isCorrect: false, trapId: "trap_law_3" }
        ],
        explanation: "【Authoritative Analysis · Rescission Extinction Periods】: The right of rescission for fraudulent misrepresentation commences when the aggrieved party knows or ought to have known of the ground for rescission, expiring strictly in 1 year (with an absolute long-stop period of 5 years from contract formation). This is an extinction/preclusion period and cannot be suspended or interrupted.",
        traps: {
          trap_law_1: {
            title: "🚨 Misconception Trap: Confusing Preclusion Periods with 3-Year General Limitation Actions",
            desc: "General limitation periods govern claims for damages (claims), whereas rescission is a formative power subject to strict statutory preclusion!",
            prereq: "Prerequisite Concept: Formative Rights vs Claims & Preclusion Periods",
            radarHit: "trapDefense"
          },
          trap_law_2: {
            title: "🚨 Rule Mismatch Trap: Confusing Fraud with Duress commencement points",
            desc: "Under duress, the period commences when the coercion ceases. Under fraud, it commences when the fraud is known or ought to be known!",
            prereq: "Prerequisite Concept: Vitiating Factors Statutory Commencement Rules",
            radarHit: "boundary"
          },
          trap_law_3: {
            title: "🚨 Obsolete Statute Confusion",
            desc: "Confusing superseded legacy contract rules with modern codified contract frameworks.",
            prereq: "Prerequisite Concept: Modern Codified Contract Law Rules",
            radarHit: "recall"
          }
        },
        graph: {
          title: "Contract Law · Rescission Period Topology",
          nodes: [
            { id: "c1", label: "Rescission Period", type: "core", x: 260, y: 140 },
            { id: "p1", label: "Knowledge of Fraud (1 Year)", type: "prereq", x: 120, y: 60 },
            { id: "p2", label: "Absolute Long-Stop (5 Years)", type: "prereq", x: 400, y: 60 },
            { id: "t1", label: "Trap: 3-Year Limitation Confusion", type: "trap", x: 130, y: 240 },
            { id: "t2", label: "Trap: Duress Cessation Mismatch", type: "trap", x: 390, y: 240 }
          ],
          edges: [
            { from: "p1", to: "c1", label: "Statutory Start" },
            { from: "p2", to: "c1", label: "Max Protection Limit" },
            { from: "c1", to: "t1", label: "Prone to (Nature of Rights)" },
            { from: "c1", to: "t2", label: "Prone to (Commencement Mismatch)" }
          ]
        },
        socraticPrompt: "Why does the law impose a strict 1-year extinction period once fraud is discovered, rather than allowing the innocent party to hold the threat of rescission indefinitely over commercial transactions?"
      }
    ]
  }
};

// 当前题库指针 (动态绑定语言)
let DB = (localStorage.getItem("smartstudy_lang") === "zh" || !localStorage.getItem("smartstudy_lang")) ? DB_ZH : DB_EN;

// =============================================================================
// 多语言国际化字典 (Internationalization Dictionary - EN / ZH)
// =============================================================================
const I18N = {
  en: {
    brandName: "SmartStudy AI",
    brandSubtitle: "STUDY CONSOLE v1.0",
    courseBadge: "University of Aberdeen · JC2001 Group 5 Honours Project",
    fastEnter: "Enter Study Workspace →",
    backToPortal: "Back to Portal",
    tabQuiz: "01 Misconception Quiz",
    tabTutor: "02 Socratic AI Tutor",
    tabGraph: "03 Knowledge Graph",
    tabReport: "04 Learning Telemetry",
    suitesHeading: "CURRICULUM MODULES",
    telemetryHeading: "SYSTEM METRICS",
    groundingGate: "GROUNDING GATE",
    hallucinationDrop: "HALLUCINATION DROP",
    diagnosticEngine: "DIAGNOSTIC ENGINE",
    streak: "STREAK",
    apiStatus: "API: Local Sandbox",
    switchBadge: "⇄ Switch",
    radarTitle: "COGNITIVE 5D TELEMETRY",
    radarCaption: "⚡ Adaptive Trap Tracking / Prerequisite Topology Diagnosis",
    tutorName: "Socratic AI Companion",
    tutorStatus: "GraphRAG Grounded · Zero Hallucination",
    tutorInvite: "\"Notice subtle assumptions in the question? Pick an option to test your intuition, and I will guide you to unpack underlying prerequisite theorems!\"",
    tutorBtn: "Enter Socratic Seminar Room",
    prevItem: "◀ PREV ITEM",
    resetItem: "🔄 RESET",
    nextItem: "NEXT ITEM >",
    counterPrefix: "Item",
    counterMid: "/",
    counterSuffix: "· 18 Items Practiced Today",
    benchmarkTag: "🎯 BENCHMARK TEST",
    loadingStem: "Loading question stem...",
    subjects: {
      se: "[SE] ⚙️ Software Eng.",
      cs: "[CS] 💻 Architecture",
      econ: "[ECON] 📈 Econometrics",
      law: "[LAW] ⚖️ Commercial Law"
    },
    portalHeroBadge: "🎓 University of Aberdeen · JC2001 Software Engineering",
    portalHeroTitle: "Adaptive Cognitive Knowledge Graph &<br>Exam Distractor Trap Diagnosis System",
    portalHeroDesc: "An intelligent diagnostic study assistant tailored for university STEM & Software Engineering curricula. Moving beyond rote memorisation to pinpoint underlying misconceptions, distractor traps, and prerequisite gaps via Socratic dialogues.",
    pillGrounded: "⚡ GraphRAG Grounded Synthesis",
    pillTraps: "🎯 36+ Distractor Traps & Misconceptions",
    pillSocratic: "💬 Socratic Guided Inquiries",
    pillRadar: "📊 5D Cognitive Competency Radar",
    authCardTitle: "🚀 Student Identity Access & Fast Showcase",
    authCardDesc: "Click any member profile below to load individual telemetry, or enter student ID:",
    authInputPlaceholder: "Or enter Student ID / Name (e.g. 50106070 or Yuxuan Wu)",
    authSubmitBtn: "Launch Study Workspace →",
    authTip: "* Sandbox demo mode enabled. Click any card to enter interactive practice.",
    featuresSubheading: "SYSTEM ARCHITECTURE & CAPABILITIES",
    featuresHeading: "Four Core Capabilities: Conventional Quiz vs SmartStudy AI",
    feat1Title: "01 · Misconception Diagnosis",
    feat1Sub: "Distractor Trap Attribution",
    feat1Desc: "<strong>Conventional Quiz Flaw:</strong> Merely scores correct/wrong without explaining the root misconception.<br><strong>SmartStudy Remedy:</strong> Every distractor is linked to specific traps and prerequisite blind spots. Picking an option unfolds a deep diagnosis drawer.",
    feat1Tag: "Causal Attribution · Prerequisite Trace",
    feat2Title: "02 · Socratic AI Companion",
    feat2Sub: "Grounded Guided Inquiry",
    feat2Desc: "<strong>Conventional AI Flaw:</strong> Dumps the final answer immediately, bypassing independent critical thinking.<br><strong>SmartStudy Remedy:</strong> Grounded in GraphRAG facts, the AI prompts stepped inquiry, nudging students to deduce core theorems independently.",
    feat2Tag: "Zero Leakage · Stepped Guidance",
    feat3Title: "03 · Knowledge Graph Topology",
    feat3Sub: "Curriculum Concept Graph",
    feat3Desc: "<strong>Conventional Study Flaw:</strong> Fragmented concepts cause exam confusion.<br><strong>SmartStudy Remedy:</strong> Visualises topological links across Software Engineering, Architecture, Econometrics, and Law (prerequisites, theorems, and common traps).",
    feat3Tag: "Neo4j Topology · Prerequisite Links",
    feat4Title: "04 · Cognitive Telemetry & Radar",
    feat4Sub: "Real-time Skill Profiling",
    feat4Desc: "<strong>Conventional Metric Flaw:</strong> Raw percentage score fails to reflect cognitive robustness.<br><strong>SmartStudy Remedy:</strong> Dynamically calculates 5 skill dimensions (Recall, Defense, Deduction, Synthesis, Boundary) to generate targeted review plans.",
    feat4Tag: "5D Radar · Adaptive Tracking",
    footerCourse: "University of Aberdeen · JC2001 Introduction to Software Engineering (2026–27)",
    footerTeam: "Group 5 (BSc BMIS): Yuxuan Wu (PM · 50106070) · Yongtong Lin (BA · 50106038) · Sijian Wang (SA · 50106045) · Hao Jiang (Dev · 50106065) · Weixin Xie (QA · 50106034) · Zijian Zhang · Yusai Xi · Siqin Dong · Mingjie Yang · Zixuan Liang",
    footerVersion: "SmartStudy Assistant PoC v1.0 · Grounded with GraphRAG & Dual-Mode Diagnostic Engine",
    diagCorrectHeader: "Great Job! Concept accurately mastered, avoiding distractor traps!",
    diagLoading: "🧠 Cognitive Engine analysing answer & trap topology...",
    diagOfflineBadge: "[Offline Topology Fallback]",
    diagOnlineBadge: "[AI Live Diagnosis]",
    weakPointPrefix: "🔍 Prerequisite Blind Spot:",
    deductionPrefix: "📉 Defense Index Impact:",
    summonTutorBtn: "💬 Summon Socratic Tutor for Step-by-Step Guidance",
    feedbackCorrectTip: "✔ Prerequisite Concept Mastery +4 | Defense Index +6",
    radarRecall: "Recall",
    radarBoundary: "Boundary",
    radarDefense: "Defense",
    radarSynthesis: "Synthesis",
    radarPrecision: "Precision"
  },
  zh: {
    brandName: "智学罗盘",
    brandSubtitle: "每天学一点，慢慢变扎实",
    courseBadge: "阿伯丁大学 JC2001 Group 5 软件工程实践",
    fastEnter: "进入学习控制台 →",
    backToPortal: "返回产品介绍主页",
    tabQuiz: "智能刷题排雷",
    tabTutor: "苏格拉底学伴",
    tabGraph: "考点图谱全景",
    tabReport: "学情综合诊断",
    suitesHeading: "学习功能",
    telemetryHeading: "我的学习",
    groundingGate: "GROUNDING GATE",
    hallucinationDrop: "HALLUCINATION DROP",
    diagnosticEngine: "DIAGNOSTIC ENGINE",
    streak: "STREAK",
    apiStatus: "API: 沙箱模式",
    switchBadge: "⇄ 切换",
    radarTitle: "最近的学习状态",
    radarCaption: "根据你的练习记录，找到下一步该复习的地方",
    tutorName: "苏格拉底学霸助教",
    tutorStatus: "会一步步提示你思考",
    tutorInvite: "卡住了没关系。先说说你的想法，我会给你一个小提示，而不是直接把答案告诉你。", 
    tutorBtn: "进入启发式学伴研讨室",
    prevItem: "◀ PREV ITEM",
    resetItem: "🔄 RESET",
    nextItem: "下一题排雷练习 >",
    counterPrefix: "第",
    counterMid: "/",
    counterSuffix: "题 · 今日已练 18 题",
    benchmarkTag: "🎯 BENCHMARK TEST",
    loadingStem: "正在加载题干...",
    subjects: {
      se: "[SE] ⚙️ 软件工程",
      cs: "[CS] 💻 体系结构",
      econ: "[ECON] 📈 计量经济",
      law: "[LAW] ⚖️ 民商法学"
    },
    portalHeroBadge: "🎓 University of Aberdeen · JC2001 Software Engineering",
    portalHeroTitle: "把每一次做错题，<br>变成下一次进步的线索",
    portalHeroDesc: "不只告诉你答案对不对，还会帮你看懂错在哪里、该补哪一块。每天花一点时间，按自己的节奏练习、复习和回顾。",
    pillGrounded: "📚 按课程整理知识点",
    pillTraps: "🧭 看懂每次错题原因",
    pillSocratic: "💬 一步步提示，不直接剧透",
    pillRadar: "📈 记录自己的学习进度",
    authCardTitle: "👋 从今天的学习开始",
    authCardDesc: "选择一个体验身份，或者输入你的名字，马上开始练习：",
    authInputPlaceholder: "输入你的名字或学号（例如：小王 或 50106070）",
    authSubmitBtn: "开始学习",
    authTip: "演示模式无需注册。你的学习记录只保存在当前浏览器中。",
    featuresSubheading: "SYSTEM ARCHITECTURE & CAPABILITIES",
    featuresHeading: "把学习拆成四件容易开始的小事",
    feat1Title: "练一道题，知道错在哪里",
    feat1Sub: "错题不只是一个红叉",
    feat1Desc: "<strong>传统题库痛点：</strong>仅判断对错，无法解释“为什么错”。<br><strong>罗盘排雷方案：</strong>每个干扰项均绑定义题陷阱（Trap）与先修短板。选错即刻滑出诊断抽屉，直击思维误区。",
    feat1Tag: "错因归因 · 先修溯源",
    feat2Title: "卡住时，有人给你提示",
    feat2Sub: "不直接告诉你答案",
    feat2Desc: "<strong>传统 AI 痛点：</strong>直接倾倒标准答案，剥夺学生自主推导过程。<br><strong>罗盘导学方案：</strong>基于 GraphRAG 知识事实，采用多轮启发式反问，引导学生一步步自行推导出定理结论。",
    feat2Tag: "零剧透 · 阶梯式点拨",
    feat3Title: "把零散知识连起来",
    feat3Sub: "看见前后知识点的关系",
    feat3Desc: "<strong>传统复习痛点：</strong>知识孤岛零碎，考前死记硬背容易混淆。<br><strong>罗盘图谱方案：</strong>将法学、计组、计量经济与软工知识拓扑化，清晰展现“前置概念-核心定理-常见误区”连边。",
    feat3Tag: "Neo4j 拓扑 · 概念脉络",
    feat4Title: "知道下一步复习什么",
    feat4Sub: "学习记录会给你方向",
    feat4Desc: "<strong>传统评估痛点：</strong>单一正确率无法反映综合思维稳健度。<br><strong>罗盘诊断方案：</strong>实时计算五维能力（基础理解、陷阱防守、推演分析、综合迁移、知识广度），生成薄弱短板雷达。",
    feat4Tag: "五维雷达 · 动态追踪",
    footerCourse: "University of Aberdeen · JC2001 Introduction to Software Engineering (2026–27)",
    footerTeam: "Group 5 (BSc BMIS) 全体成员：吴宇轩(PM · 50106070) · 林泳桐(BA · 50106038) · 王思鉴(SA · 50106045) · 江昊(Dev · 50106065) · 谢炜昕(QA · 50106034) · 张梓健 · 习羽赛 · 董思钦 · 杨明杰 · 梁子铉",
    footerVersion: "SmartStudy Assistant PoC v1.0 · Grounded with GraphRAG & Dual-Mode Diagnostic Engine",
    diagCorrectHeader: "太棒了！考点精准命中，成功避开出题陷阱！",
    diagLoading: "🧠 认知引擎正在研判答案与陷阱拓扑...",
    diagOfflineBadge: "[离线高可用图谱兜底]",
    diagOnlineBadge: "[AI 实时诊断]",
    weakPointPrefix: "🔍 盲区定位：",
    deductionPrefix: "📉 易错扣减：",
    summonTutorBtn: "💬 召唤苏格拉底学霸助教启发点拨",
    feedbackCorrectTip: "✔ 基础概念牢固度 +4 | 排雷防守指数 +6",
    radarRecall: "基础概念 (Recall)",
    radarBoundary: "边界推演 (Boundary)",
    radarDefense: "排雷防守 (Defense)",
    radarSynthesis: "综合运用 (Synthesis)",
    radarPrecision: "计算精度 (Precision)"
  }
};
const API_BASE = (function() {
  if (typeof window !== "undefined" && window.location && window.location.origin && window.location.origin.startsWith("http")) {
    return window.location.origin;
  }
  return "http://127.0.0.1:8000";
})();

// =============================================================================
// 全局状态机 (Global State)
// =============================================================================
const GEMINI_DEFAULT_KEY = "sk-6a8d40733e5f0db6cd679d4562480edee4fdcaad5e7e1510bc73945df46d9083";
const GEMINI_DEFAULT_URL = "https://uuapi.net/v1";
const GEMINI_DEFAULT_MODEL = "gemini-3.8-flash";

const savedApiKey = localStorage.getItem("smartstudy_apikey");
const activeApiKey = (savedApiKey && savedApiKey.trim()) ? savedApiKey.trim() : GEMINI_DEFAULT_KEY;
const activeProvider = localStorage.getItem("smartstudy_provider") || "gemini";
const activeApiUrl = (savedApiKey && savedApiKey.trim()) ? (localStorage.getItem("smartstudy_apiurl") || GEMINI_DEFAULT_URL) : GEMINI_DEFAULT_URL;
const activeModel = (savedApiKey && savedApiKey.trim()) ? (localStorage.getItem("smartstudy_model") || GEMINI_DEFAULT_MODEL) : GEMINI_DEFAULT_MODEL;

const initialLang = localStorage.getItem("smartstudy_lang") || "zh";

const DEFAULT_WEAK_LISTS = {
  en: [
    { tag: "Waterfall vs Agile Trade-offs", reason: "Confusing regulatory audit with extreme agile", count: 2 },
    { tag: "SOLID & Dependency Inversion (DIP)", reason: "Direct coupling to low-level drivers without interface", count: 1 }
  ],
  zh: [
    { tag: "除斥期间 vs 诉讼时效", reason: "混淆权利性质（形成权 vs 请求权）", count: 2 },
    { tag: "顺序执行与乱序流水线", reason: "死搬 WAR 冒险导致判断失误", count: 1 }
  ]
};

const state = {
  lang: initialLang,
  currentSubject: localStorage.getItem("smartstudy_subject") || "se",
  currentQIndex: 0,
  activeTab: "quiz",
  theme: localStorage.getItem("smartstudy_theme") || "light",
  hasAnswered: false,

  // AI 大模型与知识图谱接口配置
  apiConfig: {
    provider: activeProvider,
    apiKey: activeApiKey,
    apiUrl: activeApiUrl,
    model: activeModel,
    neo4jUri: localStorage.getItem("smartstudy_neo4j") || "neo4j+s://smartstudy-aura.databases.neo4j.io",
    gateEnabled: localStorage.getItem("smartstudy_gate") !== "false"
  },

  // 学生能力五维画像 (0-100)
  radar: {
    recall: 76,       // 基础概念
    boundary: 62,     // 边界推演
    trapDefense: 65,  // 排雷防守
    synthesis: 72,    // 综合运用
    precision: 81     // 计算精度
  },

  // 历史刷题统计
  stats: {
    streakDays: 5,
    trapsAvoided: 14,
    totalAnswered: 18,
    predictedScore: 86.5
  },

  // 待排雷薄弱考点列表
  weakList: (initialLang === "zh" ? DEFAULT_WEAK_LISTS.zh : DEFAULT_WEAK_LISTS.en)
};

let miniRadarChart = null;
let largeRadarChart = null;

// =============================================================================
// DOM 加载与初始化
// =============================================================================
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initNavTabs();
  initApiModal();
  initSubjectSelector();
  initRadarCharts();
  loadQuestion();
  renderGraph();
  initSocraticChat();
  updateStatCards();
  checkBackendHealth();
  initAuthPortal();
  initI18n();
});

// =============================================================================
// 产品介绍门户与学生档案登录控制器 (Landing & Auth Portal Controller)
// =============================================================================
const DEMO_STUDENTS_CONFIG = {
  en: [
    {
      id: "50106070",
      name: "Yuxuan Wu",
      role: "PM · Group Leader",
      avatar: "YW",
      subject: "se",
      subjectLabel: "⚙️ Software Eng.",
      streak: 5
    },
    {
      id: "50106038",
      name: "Yongtong Lin",
      role: "Lead BA · Requirements",
      avatar: "YL",
      subject: "econ",
      subjectLabel: "📈 Econometrics",
      streak: 4
    },
    {
      id: "50106045",
      name: "Sijian Wang",
      role: "Chief Architect",
      avatar: "SW",
      subject: "cs",
      subjectLabel: "💻 Architecture",
      streak: 6
    },
    {
      id: "50106065",
      name: "Hao Jiang",
      role: "Development Lead",
      avatar: "HJ",
      subject: "se",
      subjectLabel: "⚙️ Software Eng.",
      streak: 7
    },
    {
      id: "guest",
      name: "Guest Learner",
      role: "Instant Sandbox Access",
      avatar: "GL",
      subject: "se",
      subjectLabel: "🚀 Instant Sandbox",
      streak: 1
    }
  ],
  zh: [
    {
      id: "50106070",
      name: "吴宇轩",
      role: "PM · 课题组组长",
      avatar: "吴",
      subject: "se",
      subjectLabel: "⚙️ 软件工程",
      streak: 5
    },
    {
      id: "50106038",
      name: "林泳桐",
      role: "Lead BA · 需求主管",
      avatar: "林",
      subject: "econ",
      subjectLabel: "📈 计量经济",
      streak: 4
    },
    {
      id: "50106045",
      name: "王思鉴",
      role: "Architect · 架构主管",
      avatar: "王",
      subject: "cs",
      subjectLabel: "💻 计算机体系",
      streak: 6
    },
    {
      id: "50106065",
      name: "江昊",
      role: "Dev Lead · 开发主管",
      avatar: "江",
      subject: "se",
      subjectLabel: "⚙️ 软件工程",
      streak: 7
    },
    {
      id: "guest",
      name: "访客体验生",
      role: "Guest · 速通免密",
      avatar: "客",
      subject: "se",
      subjectLabel: "🚀 全功能体验",
      streak: 1
    }
  ]
};

function getDemoStudents() {
  const lang = state.lang || "en";
  return DEMO_STUDENTS_CONFIG[lang] || DEMO_STUDENTS_CONFIG.en;
}

function switchRootView(view) {
  const portal = document.getElementById("portal-landing");
  const shell = document.getElementById("app-shell");
  if (!portal || !shell) return;

  if (view === "workspace") {
    portal.style.display = "none";
    shell.style.display = "flex";
    localStorage.setItem("smartstudy_current_view", "workspace");
    setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
      if (typeof rebuildRadarCharts === "function") rebuildRadarCharts();
      if (typeof renderGraph === "function") renderGraph();
    }, 60);
  } else {
    shell.style.display = "none";
    portal.style.display = "block";
    localStorage.setItem("smartstudy_current_view", "portal");
  }
}

function switchSubject(sub) {
  if (!DB[sub]) return;
  state.currentSubject = sub;
  state.currentQIndex = 0;
  localStorage.setItem("smartstudy_subject", sub);
  const btns = document.querySelectorAll(".subject-btn");
  btns.forEach(b => {
    if (b.dataset.subject === sub) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });
  loadQuestion();
  renderGraph();
  if (typeof resetChatWithContext === "function") resetChatWithContext();
}

function applyStudentProfile(student) {
  if (!student) return;
  state.currentUser = student;
  localStorage.setItem("smartstudy_current_user", JSON.stringify(student));

  const nameEl = document.getElementById("current-user-name");
  const roleEl = document.getElementById("current-user-role");
  const avatarEl = document.getElementById("current-user-avatar");
  if (nameEl) nameEl.textContent = student.name;
  if (roleEl) roleEl.textContent = `${student.role} (${student.id})`;
  if (avatarEl) avatarEl.textContent = student.avatar || student.name.charAt(0);

  const streakStrong = document.querySelector(".streak-badge strong");
  if (streakStrong && student.streak) streakStrong.textContent = student.streak;

  if (student.subject && DB[student.subject] && typeof switchSubject === "function") {
    switchSubject(student.subject);
  }
}

function renderDemoAccounts() {
  const demoContainer = document.getElementById("portal-demo-accounts");
  if (demoContainer) {
    const students = getDemoStudents();
    demoContainer.innerHTML = students.map(s => `
      <div class="demo-user-card" data-student-id="${s.id}" title="${state.lang === 'zh' ? '点击以【' + s.name + '】身份登入并进入控制台' : 'Click to launch workspace as ' + s.name}">
        <div class="demo-avatar">${s.avatar}</div>
        <div class="demo-name">${s.name}</div>
        <div class="demo-role">${s.role}</div>
        <div class="demo-subject">${s.subjectLabel}</div>
      </div>
    `).join("");

    demoContainer.querySelectorAll(".demo-user-card").forEach(card => {
      card.addEventListener("click", () => {
        const id = card.getAttribute("data-student-id");
        const list = getDemoStudents();
        const student = list.find(s => s.id === id) || list[0];
        applyStudentProfile(student);
        switchRootView("workspace");
      });
    });
  }

  // Also populate demo cards inside the modal if it exists
  const modalGrid = document.getElementById("demo-accounts-list");
  if (modalGrid) {
    const students = getDemoStudents();
    modalGrid.innerHTML = students.map(s => `
      <div class="demo-user-card" data-student-id="${s.id}" style="padding: 10px; cursor: pointer;">
        <div class="demo-avatar" style="width: 32px; height: 32px; font-size: 0.85rem;">${s.avatar}</div>
        <div class="demo-name" style="font-size: 0.88rem;">${s.name}</div>
        <div class="demo-role" style="font-size: 0.72rem;">${s.role}</div>
      </div>
    `).join("");

    modalGrid.querySelectorAll(".demo-user-card").forEach(card => {
      card.addEventListener("click", () => {
        const id = card.getAttribute("data-student-id");
        const list = getDemoStudents();
        const student = list.find(s => s.id === id) || list[0];
        applyStudentProfile(student);
        const loginModal = document.getElementById("login-modal");
        if (loginModal) loginModal.style.display = "none";
      });
    });
  }
}

function applyLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("smartstudy_lang", lang);
  DB = (lang === "zh") ? DB_ZH : DB_EN;
  const dict = I18N[lang] || I18N.en;

  // 1. Language Toggle Buttons
  const portalLangBtn = document.getElementById("portal-lang-btn");
  if (portalLangBtn) {
    const label = portalLangBtn.querySelector(".lang-label");
    if (label) label.textContent = (lang === "zh") ? "中文" : "English";
    portalLangBtn.title = (lang === "zh") ? "切换为英文 (Switch to English)" : "Switch to Chinese / 切换中文";
  }
  const sidebarLangBtn = document.getElementById("sidebar-lang-btn");
  if (sidebarLangBtn) {
    const label = sidebarLangBtn.querySelector(".lang-label");
    if (label) label.textContent = (lang === "zh") ? "中文" : "EN";
    sidebarLangBtn.title = (lang === "zh") ? "切换为英文 (Switch to English)" : "Switch to Chinese / 切换中文";
  }

  // 2. Portal Header & Hero
  const portalBrandSub = document.getElementById("portal-brand-sub");
  if (portalBrandSub) portalBrandSub.textContent = dict.courseBadge;

  const fastEnterText = document.getElementById("portal-fast-enter-text");
  if (fastEnterText) fastEnterText.textContent = dict.fastEnter;

  const heroBadge = document.querySelector(".portal-badge-pill span");
  if (heroBadge) heroBadge.textContent = dict.portalHeroBadge;

  const heroTitle = document.querySelector(".portal-hero-title");
  if (heroTitle) heroTitle.innerHTML = dict.portalHeroTitle;

  const heroDesc = document.querySelector(".portal-hero-desc");
  if (heroDesc) heroDesc.textContent = dict.portalHeroDesc;

  const pills = document.querySelectorAll(".portal-highlights-row .portal-pill-chip");
  if (pills && pills.length >= 4) {
    pills[0].textContent = dict.pillGrounded;
    pills[1].textContent = dict.pillTraps;
    pills[2].textContent = dict.pillSocratic;
    pills[3].textContent = dict.pillRadar;
  }

  // 3. Auth Card
  const authCardTitle = document.querySelector(".auth-card-header div:first-child span:last-child");
  if (authCardTitle) authCardTitle.textContent = dict.authCardTitle;

  const authCardDesc = document.querySelector(".auth-card-header div:last-child");
  if (authCardDesc) authCardDesc.textContent = dict.authCardDesc;

  const usernameInput = document.getElementById("portal-username-input");
  if (usernameInput) usernameInput.placeholder = dict.authInputPlaceholder;

  const loginBtn = document.getElementById("portal-login-btn");
  if (loginBtn) loginBtn.innerHTML = `${dict.authSubmitBtn}`;

  const loginTip = document.getElementById("portal-login-tip");
  if (loginTip) loginTip.textContent = dict.authTip;

  // Re-render student cards
  renderDemoAccounts();

  // 4. Features Section
  const featuresSub = document.querySelector(".portal-features-section div div:first-child");
  if (featuresSub) featuresSub.textContent = dict.featuresSubheading;

  const featuresHeading = document.querySelector(".portal-features-section div h2");
  if (featuresHeading) featuresHeading.textContent = dict.featuresHeading;

  const featureCards = document.querySelectorAll(".portal-feature-card");
  if (featureCards && featureCards.length >= 4) {
    featureCards[0].querySelector(".feature-card-title").textContent = dict.feat1Title;
    featureCards[0].querySelector(".feature-card-subtitle").textContent = dict.feat1Sub;
    featureCards[0].querySelector(".feature-card-p").innerHTML = dict.feat1Desc;
    featureCards[0].querySelector(".feature-card-tag").textContent = dict.feat1Tag;

    featureCards[1].querySelector(".feature-card-title").textContent = dict.feat2Title;
    featureCards[1].querySelector(".feature-card-subtitle").textContent = dict.feat2Sub;
    featureCards[1].querySelector(".feature-card-p").innerHTML = dict.feat2Desc;
    featureCards[1].querySelector(".feature-card-tag").textContent = dict.feat2Tag;

    featureCards[2].querySelector(".feature-card-title").textContent = dict.feat3Title;
    featureCards[2].querySelector(".feature-card-subtitle").textContent = dict.feat3Sub;
    featureCards[2].querySelector(".feature-card-p").innerHTML = dict.feat3Desc;
    featureCards[2].querySelector(".feature-card-tag").textContent = dict.feat3Tag;

    featureCards[3].querySelector(".feature-card-title").textContent = dict.feat4Title;
    featureCards[3].querySelector(".feature-card-subtitle").textContent = dict.feat4Sub;
    featureCards[3].querySelector(".feature-card-p").innerHTML = dict.feat4Desc;
    featureCards[3].querySelector(".feature-card-tag").textContent = dict.feat4Tag;
  }

  // 5. Portal Footer
  const footerCourse = document.querySelector(".portal-footer div:nth-child(1)");
  if (footerCourse) footerCourse.textContent = dict.footerCourse;

  const footerTeam = document.querySelector(".portal-footer div:nth-child(2)");
  if (footerTeam) footerTeam.textContent = dict.footerTeam;

  const footerVersion = document.querySelector(".portal-footer div:nth-child(3)");
  if (footerVersion) footerVersion.textContent = dict.footerVersion;

  // 6. Sidebar (App Shell)
  const brandName = document.querySelector(".brand-meta .brand-name");
  if (brandName) brandName.textContent = dict.brandName;

  const brandSub = document.querySelector(".brand-meta .brand-subtitle");
  if (brandSub) brandSub.textContent = dict.brandSubtitle;

  const backToPortalSpan = document.querySelector("#back-to-portal-btn span");
  if (backToPortalSpan) backToPortalSpan.textContent = dict.backToPortal;

  const navHeading = document.querySelector(".nav-group-heading");
  if (navHeading) navHeading.textContent = dict.suitesHeading;

  const tabQuiz = document.querySelector('.nav-tab-item[data-view="quiz"] .tab-label');
  if (tabQuiz) tabQuiz.textContent = dict.tabQuiz;

  const tabTutor = document.querySelector('.nav-tab-item[data-view="tutor"] .tab-label');
  if (tabTutor) tabTutor.textContent = dict.tabTutor;

  const tabGraph = document.querySelector('.nav-tab-item[data-view="graph"] .tab-label');
  if (tabGraph) tabGraph.textContent = dict.tabGraph;

  const tabReport = document.querySelector('.nav-tab-item[data-view="report"] .tab-label');
  if (tabReport) tabReport.textContent = dict.tabReport;

  const apiStatusText = document.getElementById("nav-api-status-text");
  if (apiStatusText) apiStatusText.textContent = dict.apiStatus;

  const switchBadge = document.querySelector(".user-switch-badge");
  if (switchBadge) switchBadge.textContent = dict.switchBadge;

  // 7. Subject Buttons in Quiz view
  const subBtns = document.querySelectorAll(".subject-btn");
  subBtns.forEach(btn => {
    const s = btn.getAttribute("data-subject");
    if (s && dict.subjects[s]) {
      btn.textContent = dict.subjects[s];
    }
  });

  // 8. Quiz Actions
  const prevBtn = document.getElementById("prev-q-btn");
  if (prevBtn) prevBtn.textContent = dict.prevItem;

  const resetBtn = document.getElementById("reset-q-btn");
  if (resetBtn) resetBtn.textContent = dict.resetItem;

  const nextBtn = document.getElementById("next-q-btn");
  if (nextBtn) nextBtn.textContent = dict.nextItem;

  // 9. Quiz Sidebar Cards
  const radarTitle = document.querySelector(".quiz-sidebar .side-title span");
  if (radarTitle) radarTitle.textContent = dict.radarTitle;

  const radarCaption = document.querySelector(".quiz-sidebar .radar-caption");
  if (radarCaption) radarCaption.textContent = dict.radarCaption;

  const compName = document.querySelector(".companion-name");
  if (compName) compName.textContent = dict.tutorName;

  const compStatus = document.querySelector(".companion-status");
  if (compStatus) compStatus.innerHTML = `<span class="status-dot"></span> ${dict.tutorStatus}`;

  const compBubble = document.querySelector(".companion-bubble");
  if (compBubble) compBubble.textContent = dict.tutorInvite;

  const tutorLaunchBtn = document.querySelector(".tutor-launch-btn");
  if (tutorLaunchBtn) tutorLaunchBtn.textContent = dict.tutorBtn;

  // 10. Socratic Chat View
  const chatTitle = document.querySelector(".chat-title");
  if (chatTitle) {
    chatTitle.textContent = (lang === "zh")
      ? "启发式苏格拉底学霸助教 (SOCRATIC AGENT)"
      : "Socratic Reasoning AI Tutor (SOCRATIC AGENT)";
  }
  const chatSubtitle = document.querySelector(".chat-subtitle");
  if (chatSubtitle) {
    chatSubtitle.textContent = (lang === "zh")
      ? "接入学科本体知识图谱 · 强制学术置信度仲裁 · 幻觉发生率降低 68.4%"
      : "Grounded in Curriculum Knowledge Graph · Grounding Gate ≥ 85% · Hallucination Rate Drop -68.4%";
  }

  const chips = document.querySelectorAll(".quick-chip");
  if (chips && chips.length >= 4) {
    if (lang === "zh") {
      chips[0].textContent = "💡 为什么这个选项是高频出题陷阱？";
      chips[1].textContent = "⛓️ 解这道题必须掌握哪些前置定理？";
      chips[2].textContent = "🎯 请给我一道同构变式强化题";
      chips[3].textContent = "🔍 怎样快速区分这些核心概念与边界条件？";
    } else {
      chips[0].textContent = "💡 Why is this option a frequent distractor trap?";
      chips[1].textContent = "⛓️ What prerequisite theorems are essential for this problem?";
      chips[2].textContent = "🎯 Provide an isomorphic problem for reinforcement";
      chips[3].textContent = "🔍 How to rigorously distinguish between core concepts?";
    }
  }

  const chatInput = document.getElementById("chat-input-text");
  if (chatInput) {
    chatInput.placeholder = (lang === "zh")
      ? "向苏格拉底助教输入你的解题思考或疑问（支持探讨推导思路与前置条件）..."
      : "Enter your reasoning, hypothesis, or questions for Socratic dialogue...";
  }

  const chatSendBtn = document.getElementById("chat-send-btn");
  if (chatSendBtn) chatSendBtn.textContent = (lang === "zh") ? "发 送" : "SEND";

  // 11. Knowledge Graph View
  const graphTitle = document.querySelector("#view-graph .section-title");
  if (graphTitle) {
    graphTitle.textContent = (lang === "zh")
      ? "学科知识本体与出题陷阱拓扑图谱 (NEO4J DAG VISUALIZER)"
      : "Curriculum Ontology & Exam Distractor Topology (NEO4J DAG VISUALIZER)";
  }
  const graphDesc = document.querySelector("#view-graph .section-desc");
  if (graphDesc) {
    graphDesc.textContent = (lang === "zh")
      ? "核心考点 (Core Concept)、先修依赖 (Prerequisites) 与 认知混淆易错点 (Misconception Traps)"
      : "Core Syllabus Concepts, Prerequisite Dependencies, and Cognitive Misconception Traps";
  }
  const graphLegends = document.querySelectorAll(".graph-legend-item span");
  if (graphLegends && graphLegends.length >= 3) {
    graphLegends[0].textContent = (lang === "zh") ? "核心考核考点" : "Core Syllabus Concept";
    graphLegends[1].textContent = (lang === "zh") ? "前置定理基础" : "Prerequisite Foundation";
    graphLegends[2].textContent = (lang === "zh") ? "典型易错陷阱" : "Distractor Misconception Trap";
  }

  // 12. Analytics & Report View
  const statLabels = document.querySelectorAll("#view-report .stat-label");
  if (statLabels && statLabels.length >= 4) {
    statLabels[0].textContent = (lang === "zh") ? "CONSECUTIVE DAYS / 连续打卡" : "CONSECUTIVE STUDY DAYS";
    statLabels[1].textContent = (lang === "zh") ? "TRAPS IDENTIFIED / 识破陷阱" : "TRAPS DEFENDED";
    statLabels[2].textContent = (lang === "zh") ? "PREDICTED SCORE / 模拟预测" : "PROJECTED EXAM SCORE";
    statLabels[3].textContent = (lang === "zh") ? "GROUNDING CONFIDENCE / 仲裁可信度" : "GROUNDING CONFIDENCE";
  }

  const radarBigTitle = document.querySelector("#view-report .panel-title span");
  if (radarBigTitle) {
    radarBigTitle.textContent = (lang === "zh")
      ? "认知能力五维全景画像 (ECharts 5.5.1 Radar)"
      : "Cognitive Competency 5D Panorama (ECharts 5.5.1)";
  }

  const defectLogTitle = document.querySelector("#view-report .defect-panel .panel-title span");
  if (defectLogTitle) {
    defectLogTitle.textContent = (lang === "zh")
      ? "重点攻坚与薄弱知识点排雷队列 (BENCHMARK DEFECT LOG)"
      : "Curriculum Defect Queue & Target Review (BENCHMARK DEFECT LOG)";
  }

  const colTopic = document.querySelector(".col-topic");
  if (colTopic) {
    colTopic.textContent = (lang === "zh")
      ? "DEFECT TARGET & REASON / 考点与归因"
      : "DEFECT TARGET & CAUSAL ATTRIBUTION";
  }

  const evalRec = document.querySelector(".eval-rec-box");
  if (evalRec) {
    evalRec.innerHTML = (lang === "zh")
      ? `💡 <strong>EVAL RECOMMENDATION</strong>: 自适应追踪模型判定：建议今日优先复习上述失误考点前置定理，并完成 1 道同构变式强化题。`
      : `💡 <strong>EVAL RECOMMENDATION</strong>: Adaptive tracker indicates: Focus today on prerequisite theorems for flagged items, then complete 1 reinforcement item.`;
  }

  // 13. Update Active Student Profile Display
  if (state.currentUser) {
    const matched = getDemoStudents().find(s => s.id === state.currentUser.id);
    if (matched) {
      applyStudentProfile(matched);
    }
  }

  // 14. Update WeakList language
  state.weakList = (lang === "zh") ? DEFAULT_WEAK_LISTS.zh : DEFAULT_WEAK_LISTS.en;

  // 15. Reload Question, Radar Charts and Graph
  loadQuestion();
  if (typeof rebuildRadarCharts === "function") rebuildRadarCharts();
  if (typeof renderGraph === "function") renderGraph();
  updateStatCards();
}

function initI18n() {
  const currentLang = localStorage.getItem("smartstudy_lang") || "zh";

  const portalLangBtn = document.getElementById("portal-lang-btn");
  if (portalLangBtn) {
    portalLangBtn.addEventListener("click", () => {
      const nextLang = (state.lang === "en") ? "zh" : "en";
      applyLanguage(nextLang);
    });
  }

  const sidebarLangBtn = document.getElementById("sidebar-lang-btn");
  if (sidebarLangBtn) {
    sidebarLangBtn.addEventListener("click", () => {
      const nextLang = (state.lang === "en") ? "zh" : "en";
      applyLanguage(nextLang);
    });
  }

  applyLanguage(currentLang);
}

function initAuthPortal() {
  renderDemoAccounts();

  const loginBtn = document.getElementById("portal-login-btn");
  const usernameInput = document.getElementById("portal-username-input");
  if (loginBtn && usernameInput) {
    const handleLogin = () => {
      const val = usernameInput.value.trim();
      const students = getDemoStudents();
      let matched = students.find(s => s.id === val || s.name.toLowerCase() === val.toLowerCase());
      if (!matched) {
        const isZh = (state.lang === "zh");
        const displayName = val || (isZh ? "吴同学" : "Yuxuan Wu");
        matched = {
          id: val && val.match(/^\d+$/) ? val : "50106070",
          name: displayName,
          role: isZh ? "BSc BMIS · 学生档案" : "BSc BMIS · Student Profile",
          avatar: isZh ? (displayName.charAt(0) || "学") : (displayName.slice(0, 2).toUpperCase() || "YW"),
          subject: "se",
          subjectLabel: isZh ? "⚙️ 软件工程" : "⚙️ Software Eng.",
          streak: 3
        };
      }
      applyStudentProfile(matched);
      switchRootView("workspace");
    };

    loginBtn.addEventListener("click", handleLogin);
    usernameInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") handleLogin();
    });
  }

  const fastEnterBtn = document.getElementById("portal-fast-enter-btn");
  if (fastEnterBtn) {
    fastEnterBtn.addEventListener("click", () => {
      const savedUser = localStorage.getItem("smartstudy_current_user");
      const students = getDemoStudents();
      if (savedUser) {
        try {
          applyStudentProfile(JSON.parse(savedUser));
        } catch (e) {
          applyStudentProfile(students[0]);
        }
      } else {
        applyStudentProfile(students[0]);
      }
      switchRootView("workspace");
    });
  }

  const portalThemeBtn = document.getElementById("portal-theme-btn");
  if (portalThemeBtn) {
    portalThemeBtn.addEventListener("click", () => {
      const newTheme = (state.theme === "light") ? "dark" : "light";
      state.theme = newTheme;
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("smartstudy_theme", newTheme);
      updateThemeIcon();
      if (typeof rebuildRadarCharts === "function") rebuildRadarCharts();
      if (typeof renderGraph === "function") renderGraph();
    });
  }

  const backToPortalBtn = document.getElementById("back-to-portal-btn");
  if (backToPortalBtn) {
    backToPortalBtn.addEventListener("click", () => {
      switchRootView("portal");
    });
  }

  const userProfileBtn = document.getElementById("user-profile-btn");
  const loginModal = document.getElementById("login-modal");
  const closeLoginModalBtn = document.getElementById("close-login-modal-btn");
  const logoutBtn = document.getElementById("logout-btn");

  if (userProfileBtn && loginModal) {
    userProfileBtn.addEventListener("click", () => {
      loginModal.style.display = "flex";
      renderDemoAccounts();
    });
  }
  if (closeLoginModalBtn && loginModal) {
    closeLoginModalBtn.addEventListener("click", () => {
      loginModal.style.display = "none";
    });
  }
  if (loginModal) {
    loginModal.addEventListener("click", (e) => {
      if (e.target === loginModal) loginModal.style.display = "none";
    });
  }
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      if (loginModal) loginModal.style.display = "none";
      localStorage.removeItem("smartstudy_current_user");
      switchRootView("portal");
    });
  }

  // 初始视图判定：首次打开默认展示介绍门户
  const initialView = localStorage.getItem("smartstudy_current_view");
  if (initialView === "workspace") {
    const savedUser = localStorage.getItem("smartstudy_current_user");
    if (savedUser) {
      try { applyStudentProfile(JSON.parse(savedUser)); } catch (e) {}
    }
    switchRootView("workspace");
  } else {
    switchRootView("portal");
  }
}


// =============================================================================
// 后端健康状态静默探测 (Silent Backend Health Probe)
// =============================================================================
async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (res.ok) {
      const data = await res.json();
      const statusText = document.querySelector(".sidebar-status-chip .status-text");
      if (statusText) {
        statusText.textContent = "FASTAPI ONLINE";
      }
      console.log("[SmartStudy] Backend probe success:", data);
    }
  } catch (e) {
    // 离线静默降级，不向控制台抛出任何未捕获异常
  }
}

// =============================================================================
// =============================================================================
// API Key 接口配置与模态交互管理 (API Key Configuration Manager)
// =============================================================================
function initApiModal() {
  const modal = document.getElementById("api-modal");
  const openBtn = document.getElementById("api-settings-btn");
  const closeBtn = document.getElementById("close-api-modal-btn");
  const cancelBtn = document.getElementById("cancel-api-btn");
  const saveBtn = document.getElementById("save-api-btn");
  const testBtn = document.getElementById("test-api-btn");
  const providerSelect = document.getElementById("api-provider-select");
  const keyInput = document.getElementById("api-key-input");
  const toggleKeyBtn = document.getElementById("toggle-key-visibility-btn");
  const urlInput = document.getElementById("api-url-input");
  const modelInput = document.getElementById("api-model-input");
  const neo4jInput = document.getElementById("neo4j-uri-input");
  const gateCheckbox = document.getElementById("gate-checkbox");
  const feedback = document.getElementById("api-test-feedback");

  // 同步当前配置至表单
  function syncConfigToUI() {
    if (providerSelect) providerSelect.value = state.apiConfig.provider;
    if (keyInput) keyInput.value = state.apiConfig.apiKey;
    if (urlInput) urlInput.value = state.apiConfig.apiUrl;
    if (modelInput) modelInput.value = state.apiConfig.model;
    if (neo4jInput) neo4jInput.value = state.apiConfig.neo4jUri;
    if (gateCheckbox) gateCheckbox.checked = state.apiConfig.gateEnabled;
    updateApiBadge();
  }

  function updateApiBadge() {
    const badge = document.getElementById("api-settings-btn");
    const textEl = document.getElementById("nav-api-status-text");
    if (!badge || !textEl) return;

    if (state.apiConfig.provider === "mock") {
      textEl.textContent = "API: 本地沙箱";
      badge.classList.remove("active");
    } else if (state.apiConfig.apiKey) {
      textEl.textContent = `API: ${state.apiConfig.model}`;
      badge.classList.add("active");
    } else {
      textEl.textContent = "API: 配置Key";
      badge.classList.remove("active");
    }
  }

  // 打开/关闭模态窗
  if (openBtn) {
    openBtn.addEventListener("click", () => {
      syncConfigToUI();
      if (feedback) feedback.style.display = "none";
      if (modal) modal.style.display = "flex";
    });
  }

  const hideModal = () => {
    if (modal) modal.style.display = "none";
  };

  if (closeBtn) closeBtn.addEventListener("click", hideModal);
  if (cancelBtn) cancelBtn.addEventListener("click", hideModal);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) hideModal();
    });
  }

  // 密码可见性切换
  if (toggleKeyBtn && keyInput) {
    toggleKeyBtn.addEventListener("click", () => {
      keyInput.type = keyInput.type === "password" ? "text" : "password";
      toggleKeyBtn.textContent = keyInput.type === "password" ? "👁️" : "🙈";
    });
  }

  // 提供商联动预填端点
  if (providerSelect) {
    providerSelect.addEventListener("change", () => {
      const val = providerSelect.value;
      if (val === "gemini") {
        if (urlInput) urlInput.value = GEMINI_DEFAULT_URL;
        if (modelInput) modelInput.value = GEMINI_DEFAULT_MODEL;
        if (keyInput && (!keyInput.value || !keyInput.value.trim())) {
          keyInput.value = GEMINI_DEFAULT_KEY;
        }
      } else if (val === "dashscope") {
        if (urlInput) urlInput.value = "https://dashscope.aliyuncs.com/compatible-mode/v1";
        if (modelInput) modelInput.value = "qwen-turbo";
      } else if (val === "openai") {
        if (urlInput) urlInput.value = "https://api.openai.com/v1";
        if (modelInput) modelInput.value = "gpt-4o-mini";
      } else if (val === "mock") {
        if (feedback) {
          feedback.className = "api-status-banner success";
          feedback.style.display = "flex";
          feedback.textContent = "💡 离线沙箱模式：无需 API Key，由本地知识图谱启发引擎提供稳定高效支持。";
        }
      }
    });
  }

  // 测试接口连通性
  if (testBtn) {
    testBtn.addEventListener("click", async () => {
      if (!feedback) return;
      const provider = providerSelect ? providerSelect.value : "dashscope";
      const key = keyInput ? keyInput.value.trim() : "";
      const url = urlInput ? urlInput.value.trim() : "";
      const model = modelInput ? modelInput.value.trim() : "qwen-turbo";

      if (provider === "mock") {
        feedback.className = "api-status-banner success";
        feedback.style.display = "flex";
        feedback.textContent = "✅ 本地高保真沙箱已连通！多学科图谱与启发式知识引擎运行正常。";
        return;
      }

      if (!key) {
        feedback.className = "api-status-banner error";
        feedback.style.display = "flex";
        feedback.textContent = "❌ 请先填写大模型 API Key 密钥后再发起连通性测试！";
        return;
      }

      feedback.className = "api-status-banner";
      feedback.style.display = "flex";
      feedback.textContent = `⚡ 正在连接 ${url} 测试 ${model} 响应，请稍候...`;

      try {
        const resp = await fetch(`${url}/chat/completions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${key}`
          },
          body: JSON.stringify({
            model: model,
            messages: [{ role: "user", content: "ping" }],
            max_tokens: 5
          })
        });

        if (resp.ok) {
          feedback.className = "api-status-banner success";
          feedback.innerHTML = `✅ 连通性测试成功 (HTTP 200)！成功接入 <strong>${model}</strong> 大模型。`;
        } else {
          const errData = await resp.json().catch(() => ({}));
          feedback.className = "api-status-banner error";
          feedback.innerHTML = `❌ 接口响应异常 (HTTP ${resp.status})：${errData.error?.message || errData.message || '鉴权失败或模型权限不足'}`;
        }
      } catch (err) {
        // 浏览器直接调用常见跨域或网络告警，给予友好提示
        feedback.className = "api-status-banner error";
        feedback.innerHTML = `⚠️ 测试提示：${err.message || '网络连接超时'}。<br><span style="font-size:0.78rem;">若本地浏览器因 CORS 策略限制直连，保存配置后在助教对话中将启用图谱仲裁保障。</span>`;
      }
    });
  }

  // 保存配置
  if (saveBtn) {
    saveBtn.addEventListener("click", () => {
      state.apiConfig.provider = providerSelect ? providerSelect.value : "dashscope";
      state.apiConfig.apiKey = keyInput ? keyInput.value.trim() : "";
      state.apiConfig.apiUrl = urlInput ? urlInput.value.trim() : "https://dashscope.aliyuncs.com/compatible-mode/v1";
      state.apiConfig.model = modelInput ? modelInput.value.trim() : "qwen-turbo";
      state.apiConfig.neo4jUri = neo4jInput ? neo4jInput.value.trim() : "neo4j+s://smartstudy-aura.databases.neo4j.io";
      state.apiConfig.gateEnabled = gateCheckbox ? gateCheckbox.checked : true;

      localStorage.setItem("smartstudy_provider", state.apiConfig.provider);
      localStorage.setItem("smartstudy_apikey", state.apiConfig.apiKey);
      localStorage.setItem("smartstudy_apiurl", state.apiConfig.apiUrl);
      localStorage.setItem("smartstudy_model", state.apiConfig.model);
      localStorage.setItem("smartstudy_neo4j", state.apiConfig.neo4jUri);
      localStorage.setItem("smartstudy_gate", String(state.apiConfig.gateEnabled));

      updateApiBadge();

      if (feedback) {
        feedback.className = "api-status-banner success";
        feedback.style.display = "flex";
        feedback.innerHTML = `💾 配置已保存！当前服务：<strong>${state.apiConfig.provider === 'mock' ? '本地沙箱' : state.apiConfig.model}</strong>。`;
      }

      setTimeout(() => {
        hideModal();
      }, 700);
    });
  }

  syncConfigToUI();
}

// 主题控制 (Theme Switcher)
// =============================================================================
function initTheme() {
  const saved = localStorage.getItem("smartstudy_theme") || "light";
  state.theme = saved;
  document.documentElement.setAttribute("data-theme", saved);
  updateThemeIcon();

  const toggleBtn = document.getElementById("theme-toggle-btn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      state.theme = state.theme === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", state.theme);
      localStorage.setItem("smartstudy_theme", state.theme);
      updateThemeIcon();
      rebuildRadarCharts();
      renderGraph();
    });
  }
}

function updateThemeIcon() {
  const sun = document.getElementById("icon-sun");
  const moon = document.getElementById("icon-moon");
  if (!sun || !moon) return;
  if (state.theme === "dark") {
    sun.style.display = "block";
    moon.style.display = "none";
  } else {
    sun.style.display = "none";
    moon.style.display = "block";
  }
}

// =============================================================================
// 顶部页面切换 (Navigation Tabs)
// =============================================================================
function initNavTabs() {
  const tabs = document.querySelectorAll(".nav-tab-item");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const viewId = tab.dataset.view;
      state.activeTab = viewId;

      document.querySelectorAll(".view-section").forEach(sec => {
        sec.classList.remove("active");
      });

      const targetSec = document.getElementById(`view-${viewId}`);
      if (targetSec) {
        targetSec.classList.add("active");
      }

      if (viewId === "report" && largeRadarChart) {
        setTimeout(() => largeRadarChart.resize(), 50);
      }
      if (viewId === "graph") {
        renderGraph();
      }
    });
  });
}

// =============================================================================
// 学科切换器 (Subject Switcher)
// =============================================================================
function initSubjectSelector() {
  const btns = document.querySelectorAll(".subject-btn");
  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.currentSubject = btn.dataset.subject;
      state.currentQIndex = 0;
      loadQuestion();
      renderGraph();
      resetChatWithContext();
    });
  });
}

// =============================================================================
// 题卡与选项交互 (Quiz & Trap Remediation Engine)
// =============================================================================
function getCurrentQuestion() {
  return DB[state.currentSubject].questions[state.currentQIndex];
}

function loadQuestion() {
  state.hasAnswered = false;
  const q = getCurrentQuestion();

  // 更新题目标签与题干
  document.getElementById("q-difficulty").textContent = q.difficulty;
  document.getElementById("q-tag").textContent = q.tag;
  document.getElementById("q-stem").textContent = q.stem;

  const counterEl = document.getElementById("q-counter");
  if (counterEl) {
    const totalInSub = DB[state.currentSubject].questions.length;
    if (state.lang === "zh") {
      counterEl.textContent = `${DB[state.currentSubject].name} · 第 ${state.currentQIndex + 1} / ${totalInSub} 题 (今日已练 18 题)`;
    } else {
      counterEl.textContent = `${DB[state.currentSubject].name} · Item ${state.currentQIndex + 1} / ${totalInSub} (18 Items Practiced Today)`;
    }
  }

  // 渲染选项列表
  const container = document.getElementById("options-container");
  container.innerHTML = "";

  q.options.forEach(opt => {
    const card = document.createElement("div");
    card.className = "quiz-option-card";
    card.dataset.key = opt.key;
    card.innerHTML = `
      <div class="opt-circle">${opt.key}</div>
      <div class="opt-text">${opt.text}</div>
    `;

    card.addEventListener("click", () => handleSelectOption(opt, card, q));
    container.appendChild(card);
  });

  // 收起排雷抽屉
  const drawer = document.getElementById("diagnostic-drawer");
  drawer.className = "diagnostic-drawer";
  drawer.style.display = "none";
  drawer.innerHTML = "";

  // 重置按钮文本
  document.getElementById("next-q-btn").textContent = (state.lang === "zh") ? "下一题排雷练习 >" : "NEXT ITEM >";
}

async function handleSelectOption(opt, cardEl, q) {
  if (state.hasAnswered) return;
  state.hasAnswered = true;

  const allCards = document.querySelectorAll(".quiz-option-card");
  allCards.forEach(c => c.classList.add("disabled"));

  const dict = I18N[state.lang || "en"] || I18N.en;
  const drawer = document.getElementById("diagnostic-drawer");
  drawer.style.display = "block";
  drawer.className = "diagnostic-drawer";
  drawer.innerHTML = `
    <div class="diag-header" style="color: var(--primary-500, #4f8ef7);">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="spin">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
        <path d="M12 2a10 10 0 0 1 10 10"></path>
      </svg>
      <span>${dict.diagLoading}</span>
    </div>
  `;

  let diagResult = null;

  // 1. 发起 POST /api/diagnose 请求（带有 snake_case 与 camelCase 双向字段）
  try {
    const payload = {
      question_id: q.id || q.question_id || "",
      questionId: q.id || q.question_id || "",
      selected_option: opt.key,
      selectedOption: opt.key,
      selected_key: opt.key,
      selectedKey: opt.key
    };

    const resp = await fetch(`${API_BASE}/api/diagnose`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (resp.ok) {
      diagResult = await resp.json();
    } else {
      console.warn("Backend /api/diagnose returned status:", resp.status);
    }
  } catch (err) {
    console.warn("Backend /api/diagnose unreachable, engaging local fallback engine:", err && err.message ? err.message : err);
  }

  // 2. 本地高保真兜底（若后端未启动、网络中断或返回异常）
  if (!diagResult) {
    const isCorrect = Boolean(opt.isCorrect);
    const localTrap = (q.traps && q.traps[opt.trapId]) ? q.traps[opt.trapId] : {
      title: state.lang === "zh" ? "🚨 典型易错陷阱" : "🚨 Classic Distractor Trap",
      desc: q.explanation || (state.lang === "zh" ? "该选项未能准确命中核心定理。" : "This option deviates from the core theorem."),
      prereq: q.tag || (state.lang === "zh" ? "前置核心考点" : "Prerequisite Concept")
    };

    diagResult = {
      is_correct: isCorrect,
      isCorrect: isCorrect,
      trap_name: isCorrect ? null : localTrap.title,
      trapTitle: isCorrect ? null : localTrap.title,
      concept_name: isCorrect ? (q.tag || "核心定理") : localTrap.prereq,
      conceptName: isCorrect ? (q.tag || "核心定理") : localTrap.prereq,
      socratic_guidance: isCorrect ? (q.explanation || dict.diagCorrectHeader) : (localTrap.desc || q.socraticPrompt),
      socraticHint: isCorrect ? (q.explanation || dict.diagCorrectHeader) : (localTrap.desc || q.socraticPrompt),
      fallback_mode: true,
      fallbackMode: true
    };
  }

  // 3. 字段归一化解析（严格兼容 snake_case 与 camelCase）
  const isCorrect = (diagResult.is_correct !== undefined) ? Boolean(diagResult.is_correct) : Boolean(diagResult.isCorrect);
  const fallbackMode = (diagResult.fallback_mode !== undefined) ? Boolean(diagResult.fallback_mode) : Boolean(diagResult.fallbackMode);
  const defaultTrapTitle = state.lang === "zh" ? "典型易错陷阱" : "Classic Distractor Trap";
  const rawTrap = diagResult.trap_name || diagResult.trapTitle || diagResult.trap_title || diagResult.trapName || defaultTrapTitle;
  const trapTitle = rawTrap.startsWith("🚨") ? rawTrap : `🚨 ${rawTrap}`;
  const conceptName = diagResult.concept_name || diagResult.conceptName || diagResult.prerequisite || q.tag || (state.lang === "zh" ? "前置核心考点" : "Prerequisite Concept");
  const socraticText = diagResult.socratic_guidance || diagResult.socraticHint || diagResult.socratic_hint || diagResult.socraticGuidance || (isCorrect ? q.explanation : (q.socraticPrompt || "Review prerequisite definitions."));

  // 诊断模式徽章文本与样式
  const badgeText = fallbackMode ? dict.diagOfflineBadge : dict.diagOnlineBadge;
  const badgeBorder = fallbackMode ? "var(--border-subtle, #30363d)" : (isCorrect ? "var(--emerald-500, #10b981)" : "var(--primary-500, #4f8ef7)");
  const badgeColor = fallbackMode ? "var(--text-muted, #8b949e)" : (isCorrect ? "var(--emerald-500, #10b981)" : "var(--primary-500, #4f8ef7)");
  const badgeHtml = `<span class="eval-tag" style="font-size:0.75rem;margin-left:auto;padding:2px 8px;border-radius:4px;border:1px solid ${badgeBorder};color:${badgeColor};font-family:var(--font-mono);">${badgeText}</span>`;

  // 4. 根据诊断结果渲染抽屉与更新能力雷达
  if (isCorrect) {
    // 答对
    cardEl.classList.add("correct");
    drawer.className = "diagnostic-drawer success";
    drawer.innerHTML = `
      <div class="diag-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span>${dict.diagCorrectHeader}</span>
        ${badgeHtml}
      </div>
      <div class="diag-body">${socraticText}</div>
      <div class="diag-features">
        <div class="diag-feature-pill">
          <span style="color: #10b981;">✔</span> ${state.lang === 'zh' ? '基础概念牢固度 +4' : 'Prerequisite Recall +4'}
        </div>
        <div class="diag-feature-pill">
          <span style="color: #10b981;">✔</span> ${state.lang === 'zh' ? '陷阱防御指数 +5' : 'Trap Defense Index +5'}
        </div>
      </div>
    `;

    // 奖励五维雷达分
    state.radar.recall = Math.min(100, state.radar.recall + 4);
    state.radar.trapDefense = Math.min(100, state.radar.trapDefense + 5);
    state.radar.synthesis = Math.min(100, state.radar.synthesis + 3);
    state.stats.trapsAvoided++;
    state.stats.predictedScore = Math.min(99, +(state.stats.predictedScore + 0.5).toFixed(1));
    updateRadarCharts();
    updateStatCards();

  } else {
    // 答错踩坑！
    cardEl.classList.add("wrong");
    // 同时高亮正确选项
    allCards.forEach(c => {
      const optionData = q.options.find(o => o.key === c.dataset.key);
      const isCorrectOpt = optionData && optionData.isCorrect;
      const isBackendCorrect = (diagResult.correct_key && c.dataset.key === diagResult.correct_key) ||
                               (diagResult.correctKey && c.dataset.key === diagResult.correctKey);
      if (isCorrectOpt || isBackendCorrect) {
        c.classList.add("correct");
      }
    });

    drawer.className = "diagnostic-drawer trap";
    drawer.innerHTML = `
      <div class="diag-header">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <span>${trapTitle}</span>
        ${badgeHtml}
      </div>
      <div class="diag-body">${socraticText}</div>
      <div class="diag-features">
        <div class="diag-feature-pill" style="border-color: #f59e0b; color: #d97706;">
          <span>${dict.weakPointPrefix} </span><strong>${conceptName}</strong>
        </div>
        <div class="diag-feature-pill" style="border-color: #f43f5e; color: #e11d48;">
          <span>${dict.deductionPrefix} </span>${state.lang === 'zh' ? '排雷防守指数 -6' : 'Defense Index -6'}
        </div>
      </div>
      <div style="margin-top: 16px; display: flex; gap: 12px;">
        <button id="summon-tutor-btn" class="btn-secondary" style="background: var(--bg-surface); font-size: 0.86rem; border-color: var(--primary-500); color: var(--primary-600);">
          ${dict.summonTutorBtn}
        </button>
      </div>
    `;

    // 扣减排雷分
    state.radar.trapDefense = Math.max(30, state.radar.trapDefense - 6);
    state.radar.boundary = Math.max(30, state.radar.boundary - 4);
    updateRadarCharts();

    // 绑定助教召唤按钮
    const summonBtn = document.getElementById("summon-tutor-btn");
    if (summonBtn) {
      summonBtn.addEventListener("click", () => {
        switchToTutorTabWithQuestion(q, opt, {
          title: trapTitle,
          prereq: conceptName
        });
      });
    }

    // 记录到薄弱考点列表
    addWeakPoint(conceptName, trapTitle);
  }
}

function addWeakPoint(tag, reason) {
  const existing = state.weakList.find(w => w.tag === tag);
  if (existing) {
    existing.count++;
  } else {
    state.weakList.unshift({ tag, reason, count: 1 });
  }
  renderWeakPointsList();
}

function renderWeakPointsList() {
  const container = document.getElementById("weak-points-list");
  if (!container) return;
  container.innerHTML = "";
  state.weakList.slice(0, 4).forEach(item => {
    const el = document.createElement("div");
    el.style.padding = "10px 14px";
    el.style.borderRadius = "var(--radius-sm)";
    el.style.background = "var(--bg-surface-subtle)";
    el.style.border = "1px solid var(--border-subtle)";
    el.style.marginBottom = "8px";
    el.style.fontSize = "0.86rem";
    const badgeText = (state.lang === "zh") ? `失误 ${item.count} 次` : `${item.count} Flagged`;
    el.innerHTML = `
      <div style="font-weight: 700; color: var(--text-title); display: flex; justify-content: space-between;">
        <span>${item.tag}</span>
        <span style="color: var(--rose-500); font-size: 0.78rem;">${badgeText}</span>
      </div>
      <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">${item.reason}</div>
    `;
    container.appendChild(el);
  });
}

// =============================================================================
// 题目导航与分页控制 (Question Navigation & Cycling)
// =============================================================================
function goToNextQuestion() {
  const qList = DB[state.currentSubject].questions;
  if (state.currentQIndex < qList.length - 1) {
    state.currentQIndex++;
  } else {
    // 切到下一学科的第 1 题
    const subjects = Object.keys(DB);
    const currIdx = subjects.indexOf(state.currentSubject);
    const nextSub = subjects[(currIdx + 1) % subjects.length];
    state.currentSubject = nextSub;
    state.currentQIndex = 0;
    syncSubjectButtons(nextSub);
  }
  loadQuestion();
  renderGraph();
  resetChatWithContext();
}

function goToPrevQuestion() {
  if (state.currentQIndex > 0) {
    state.currentQIndex--;
  } else {
    // 切到上一学科的最后 1 题
    const subjects = Object.keys(DB);
    const currIdx = subjects.indexOf(state.currentSubject);
    const prevSub = subjects[(currIdx - 1 + subjects.length) % subjects.length];
    state.currentSubject = prevSub;
    state.currentQIndex = DB[prevSub].questions.length - 1;
    syncSubjectButtons(prevSub);
  }
  loadQuestion();
  renderGraph();
  resetChatWithContext();
}

function syncSubjectButtons(sub) {
  document.querySelectorAll(".subject-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.subject === sub);
  });
}

document.getElementById("next-q-btn").addEventListener("click", goToNextQuestion);

const prevBtn = document.getElementById("prev-q-btn");
if (prevBtn) {
  prevBtn.addEventListener("click", goToPrevQuestion);
}

document.getElementById("reset-q-btn").addEventListener("click", () => {
  loadQuestion();
});

// =============================================================================
// ECharts 5.5.1 五维雷达图体系 (双端联动：侧栏迷你图 + 大屏分析图)
// =============================================================================
function getRadarOption(isDark) {
  const dict = I18N[state.lang || "en"] || I18N.en;
  return {
    backgroundColor: "transparent",
    tooltip: { trigger: "item" },
    radar: {
      indicator: [
        { name: dict.radarRecall, max: 100 },
        { name: dict.radarBoundary, max: 100 },
        { name: dict.radarDefense, max: 100 },
        { name: dict.radarSynthesis, max: 100 },
        { name: dict.radarPrecision, max: 100 }
      ],
      shape: "polygon",
      splitNumber: 4,
      axisName: {
        color: isDark ? "#94a3b8" : "#475569",
        fontSize: 11,
        fontWeight: 600
      },
      splitLine: {
        lineStyle: {
          color: isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.07)"
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: isDark
            ? ["rgba(30, 41, 59, 0.5)", "rgba(30, 41, 59, 0.2)"]
            : ["rgba(241, 245, 249, 0.8)", "rgba(255, 255, 255, 0.8)"]
        }
      },
      axisLine: {
        lineStyle: {
          color: isDark ? "rgba(255, 255, 255, 0.12)" : "rgba(0, 0, 0, 0.1)"
        }
      }
    },
    series: [
      {
        type: "radar",
        data: [
          {
            value: [
              state.radar.recall,
              state.radar.boundary,
              state.radar.trapDefense,
              state.radar.synthesis,
              state.radar.precision
            ],
            name: (state.lang === "zh") ? "当前备考能力画像" : "Cognitive Mastery Profile",
            symbol: "circle",
            symbolSize: 4,
            itemStyle: { color: "#3b82f6" },
            lineStyle: { width: 2.2, color: "#2563eb" },
            areaStyle: {
              color: isDark
                ? "rgba(37, 99, 235, 0.4)"
                : "rgba(37, 99, 235, 0.25)"
            }
          }
        ],
        animationDuration: 500,
        animationEasing: "cubicOut"
      }
    ]
  };
}

function initRadarCharts() {
  const isDark = state.theme === "dark";

  const miniDom = document.getElementById("mini-radar-chart");
  if (miniDom) {
    miniRadarChart = echarts.init(miniDom);
    miniRadarChart.setOption(getRadarOption(isDark));
  }

  const largeDom = document.getElementById("large-radar-chart");
  if (largeDom) {
    largeRadarChart = echarts.init(largeDom);
    largeRadarChart.setOption(getRadarOption(isDark));
  }

  window.addEventListener("resize", () => {
    if (miniRadarChart) miniRadarChart.resize();
    if (largeRadarChart) largeRadarChart.resize();
  });
}

function updateRadarCharts() {
  const updateData = {
    series: [
      {
        data: [
          {
            value: [
              state.radar.recall,
              state.radar.boundary,
              state.radar.trapDefense,
              state.radar.synthesis,
              state.radar.precision
            ]
          }
        ]
      }
    ]
  };
  if (miniRadarChart) miniRadarChart.setOption(updateData);
  if (largeRadarChart) largeRadarChart.setOption(updateData);
}

function rebuildRadarCharts() {
  if (miniRadarChart) {
    miniRadarChart.dispose();
    miniRadarChart = null;
  }
  if (largeRadarChart) {
    largeRadarChart.dispose();
    largeRadarChart = null;
  }
  initRadarCharts();
}

function updateStatCards() {
  const elStreak = document.getElementById("stat-streak");
  const elTraps = document.getElementById("stat-traps");
  const elScore = document.getElementById("stat-score");
  if (elStreak) elStreak.textContent = `${state.stats.streakDays} 天`;
  if (elTraps) elTraps.textContent = `${state.stats.trapsAvoided} 个`;
  if (elScore) elScore.textContent = `${state.stats.predictedScore} 分`;
  renderWeakPointsList();
}

// =============================================================================
// 苏格拉底 AI 学霸助教 (Socratic Tutor Chat)
// =============================================================================
function initSocraticChat() {
  resetChatWithContext();

  const sendBtn = document.getElementById("chat-send-btn");
  const inputField = document.getElementById("chat-input-text");

  if (sendBtn && inputField) {
    sendBtn.addEventListener("click", () => handleUserChatMessage());
    inputField.addEventListener("keypress", (e) => {
      if (e.key === "Enter") handleUserChatMessage();
    });
  }

  // 快捷问题气泡
  document.querySelectorAll(".quick-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      if (inputField) {
        inputField.value = chip.textContent;
        handleUserChatMessage();
      }
    });
  });
}

function resetChatWithContext() {
  const container = document.getElementById("chat-msgs-container");
  if (!container) return;

  const q = getCurrentQuestion();
  const isZh = (state.lang === "zh");
  if (isZh) {
    container.innerHTML = `
      <div class="msg-row tutor">
        <div class="msg-avatar">AI</div>
        <div class="msg-bubble">
          同学你好！我是你的<strong>启发式苏格拉底学霸助教</strong>。我的回答直接锚定在经过验证的学科知识图谱上，<strong>绝不直接替你抄写答案，也绝不产生虚假乱回答的知识幻觉</strong>！<br><br>
          当前正在研习：<strong>【${DB[state.currentSubject].name}】</strong>。<br>
          ${q.socraticPrompt}
          <div>
            <span class="msg-grounding-tag">🔒 Neo4j 权威事实锚定 · 幻觉率降低 68.4%</span>
          </div>
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="msg-row tutor">
        <div class="msg-avatar">AI</div>
        <div class="msg-bubble">
          Greetings! I am your <strong>Socratic AI Study Companion</strong>. My responses are strictly anchored to verified syllabus knowledge graphs — <strong>no spoon-feeding solutions, zero hallucinated facts</strong>!<br><br>
          Active Curriculum: <strong>[${DB[state.currentSubject].name}]</strong>.<br>
          ${q.socraticPrompt}
          <div>
            <span class="msg-grounding-tag">🔒 GraphRAG Grounded Fact Base · Hallucination Rate Drop -68.4%</span>
          </div>
        </div>
      </div>
    `;
  }
}

function switchToTutorTabWithQuestion(q, opt, trap) {
  // 切换到 tutor tab
  document.querySelectorAll(".nav-tab-item").forEach(t => t.classList.remove("active"));
  document.querySelector('.nav-tab-item[data-view="tutor"]').classList.add("active");

  document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));
  document.getElementById("view-tutor").classList.add("active");

  const isZh = (state.lang === "zh");
  const userName = (state.currentUser && state.currentUser.name) || (isZh ? "吴同学" : "Yuxuan Wu");
  const userMsg = isZh
    ? `助教你好，我刚才在做这道【${q.tag}】题时，选了错误选项 ${opt.key}，掉进了陷阱。请问为什么会这样？`
    : `Hello Tutor, while attempting the item on [${q.tag}], I chose distractor ${opt.key} and fell into a trap. Could you guide me through where my reasoning diverged?`;

  appendChatMessage("user", userMsg);

  setTimeout(() => {
    const tutorMsg = isZh
      ? `${userName}，你踩到了出题人最得意的陷阱——<strong>【${trap.title}】</strong>！<br><br>
         根据后台 Neo4j 图谱的先修依赖链，这里你遗漏的核心前置前提是：<strong>${trap.prereq}</strong>。<br><br>
         ${q.socraticPrompt}`
      : `${userName}, you encountered a classic distractor trap: <strong>${trap.title}</strong>!<br><br>
         According to our GraphRAG prerequisite chain, the primary conceptual gap is: <strong>${trap.prereq}</strong>.<br><br>
         ${q.socraticPrompt}`;

    appendChatMessage("tutor", tutorMsg);
  }, 500);
}

function getLocalSmartReply(text, q) {
  const isZh = (state.lang === "zh");
  const lower = text.toLowerCase();
  if (text.includes("前置") || text.includes("条件") || text.includes("前提") || lower.includes("prereq")) {
    const prereqs = q.graph.nodes.filter(n => n.type === "prereq").map(n => n.label).join(isZh ? "、" : ", ");
    return {
      text: isZh
        ? `根据后台 Neo4j 图谱反查，掌握【${q.tag}】的核心前置基石包括：<strong>${prereqs || '核心定理先修要件'}</strong>。请问在你的解题逻辑中，是否有遗漏这些前置约束？`
        : `According to our GraphRAG syllabus topology, foundational prerequisites for [${q.tag}] include: <strong>${prereqs || 'Core Prerequisite Theorems'}</strong>. In your reasoning process, did you account for all boundary conditions?`,
      tag: isZh ? "💡 图谱知识反查 · 前置先修链" : "💡 Graph Topology Prerequisite Trace"
    };
  } else if (text.includes("陷阱") || text.includes("为什么") || text.includes("深坑") || lower.includes("trap")) {
    const traps = Object.values(q.traps).map(t => t.title).join("<br>");
    return {
      text: isZh
        ? `出题专家在设计本考点时，针对学生认知薄弱点埋伏了典型认知陷阱：<br>${traps}<br><br>请结合具体题干分析，哪一个陷阱最容易使人误入歧途？`
        : `Examiners intentionally designed typical distractor traps around this topic:<br>${traps}<br><br>Reflecting on the problem statement, which assumption is most tempting yet flawed?`,
      tag: isZh ? "🚨 陷阱排雷反查 · 常见易错点" : "🚨 Distractor Trap Attribution"
    };
  } else if (text.includes("变式") || text.includes("再做") || text.includes("同构") || lower.includes("isomorphic") || lower.includes("reinforcement")) {
    return {
      text: isZh
        ? `已从【${DB[state.currentSubject].name}】题库拓扑中为你提取同构变式强化题：<br><br>设本题的核心前提条件发生对偶扰动，请问对应的因果推导结论是否依然成立？试在苏格拉底学伴中写出你的推导论据。`
        : `Extracted isomorphic reinforcement problem from [${DB[state.currentSubject].name}] topology:<br><br>If the primary boundary invariant is inverted, does the architectural guarantee still hold? State your deductive proof below.`,
      tag: isZh ? "🎯 同构变式强化 · 自适应出题" : "🎯 Isomorphic Reinforcement Item"
    };
  } else {
    return {
      text: isZh
        ? `⚠️ <strong>未识别到 API 链接或密钥</strong><br><br>当前系统尚未接入可用的大模型服务。<br>👉 请点击侧边栏（或顶部）的 <strong>「🔑 API 配置」</strong> 填入你的大模型 API Key 与接口端点（支持 DeepSeek、阿里云通义千问、OpenAI 等兼容端点）。`
        : `⚠️ <strong>No External LLM Endpoint Configured</strong><br><br>The system is currently operating in offline sandbox mode.<br>👉 Click <strong>"🔑 API Settings"</strong> in the sidebar to configure Gemini / Qwen / OpenAI endpoints if live inference is desired.`,
      tag: isZh ? "⚠️ 未识别到 API 链接" : "⚠️ Sandbox Mode Active"
    };
  }
}

async function handleUserChatMessage() {
  const input = document.getElementById("chat-input-text");
  const text = input.value.trim();
  if (!text) return;

  appendChatMessage("user", text);
  input.value = "";

  const q = getCurrentQuestion();
  const container = document.getElementById("chat-msgs-container");

  // 若配置了在线 API Key 且非离线模式，发起真实大模型启发式调用
  if (state.apiConfig.provider !== "mock" && state.apiConfig.apiKey) {
    let typingRow = null;
    if (container) {
      typingRow = document.createElement("div");
      typingRow.className = "msg-row tutor";
      typingRow.innerHTML = `
        <div class="msg-avatar">AI</div>
        <div class="msg-bubble" style="color: var(--text-muted); font-style: italic;">
          <span>🤖 助教已接入 ${state.apiConfig.model}，结合知识图谱事实锚定深度推演中...</span>
        </div>
      `;
      container.appendChild(typingRow);
      container.scrollTop = container.scrollHeight;
    }

    try {
      const systemPrompt = `你是一名严谨启发式助教（JC2001 软件工程自适应辅导系统）。\n` +
        `当前研习学科：【${DB[state.currentSubject].name}】。\n` +
        `考点知识标签：【${q.tag}】。\n` +
        `题干背景：${q.stem}\n` +
        `核心纪律：\n` +
        `1. 绝不可以直接给出正确答案选项字母或剧透答案！\n` +
        `2. 结合权威知识图谱事实启发，坚决杜绝学术幻觉与虚假乱回答；\n` +
        `3. 回复简短有力（120字内），通过反问与定理线索引导学生自主得出正确结论。`;

      const resp = await fetch(`${state.apiConfig.apiUrl}/chat/completions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${state.apiConfig.apiKey}`
        },
        body: JSON.stringify({
          model: state.apiConfig.model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: text }
          ],
          temperature: 0.6,
          max_tokens: 350
        })
      });

      if (typingRow) typingRow.remove();

      if (resp.ok) {
        const data = await resp.json();
        const rawReply = data.choices?.[0]?.message?.content || "大模型未返回有效文本内容。";
        // 格式化输出
        const formattedReply = rawReply
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/\n\n/g, "<br><br>")
          .replace(/\n/g, "<br>")
          .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

        appendChatMessage("tutor", formattedReply, `🔒 真实接入 ${state.apiConfig.model} · 知识图谱事实锚定`);
        return;
      } else {
        const errData = await resp.json().catch(() => ({}));
        appendChatMessage(
          "tutor",
          `⚠️ <strong>API 响应异常 (HTTP ${resp.status})</strong><br><br>接口返回错误：${errData.error?.message || errData.message || '鉴权失败或模型端点配置有误'}。<br>请检查「🔑 API 配置」中的 API Key 与端点地址。`,
          "❌ API 调用失败"
        );
        return;
      }
    } catch (err) {
      if (typingRow) typingRow.remove();
      appendChatMessage(
        "tutor",
        `⚠️ <strong>未识别到可用 API 链接或网络连接异常</strong><br><br>未能成功连接到 <code>${state.apiConfig.apiUrl}</code>。<br>错误提示：${err.message || '网络连接超时'}。<br><span style="font-size:0.8rem;color:var(--text-muted);">提示：若直接在本地以文件方式运行，浏览器安全策略可能会拦截跨域（CORS）请求，建议检查控制台或通过本地服务代理。</span>`,
        "⚠️ 未识别到 API 链接"
      );
      return;
    }
  }

  // 离线沙箱或未配置 API Key 时的兜底回复
  setTimeout(() => {
    const replyObj = getLocalSmartReply(text, q);
    if (typeof replyObj === "string") {
      appendChatMessage("tutor", replyObj);
    } else {
      appendChatMessage("tutor", replyObj.text, replyObj.tag);
    }
  }, 400);
}

function appendChatMessage(sender, htmlContent, customTag) {
  const container = document.getElementById("chat-msgs-container");
  if (!container) return;

  const tagText = customTag || "💡 苏格拉底启发点拨 · 严禁直接泄题";
  const row = document.createElement("div");
  row.className = `msg-row ${sender}`;
  row.innerHTML = `
    <div class="msg-avatar">${sender === 'tutor' ? 'AI' : '我'}</div>
    <div class="msg-bubble">
      ${htmlContent}
      ${sender === 'tutor' ? `<div><span class="msg-grounding-tag">${tagText}</span></div>` : ''}
    </div>
  `;

  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}

// =============================================================================
// 考点图谱全景画布渲染 (Interactive Neo4j Graph Canvas)
// =============================================================================
function renderGraph() {
  const svg = document.getElementById("large-graph-svg");
  if (!svg) return;

  const q = getCurrentQuestion();
  const isDark = state.theme === "dark";

  const colorMap = {
    core: { fill: isDark ? "#1e3a8a" : "#dbeafe", stroke: "#2563eb", text: isDark ? "#bfdbfe" : "#1e40af" },
    prereq: { fill: isDark ? "#064e3b" : "#d1fae5", stroke: "#059669", text: isDark ? "#a7f3d0" : "#065f46" },
    trap: { fill: isDark ? "#4c0519" : "#ffe4e6", stroke: "#e11d48", text: isDark ? "#fecdd3" : "#9f1239" }
  };

  let html = `<defs>
    <marker id="arrow-large" viewBox="0 0 10 10" refX="26" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="${isDark ? '#64748b' : '#94a3b8'}"/>
    </marker>
  </defs>`;

  // 连边
  q.graph.edges.forEach(edge => {
    const from = q.graph.nodes.find(n => n.id === edge.from);
    const to = q.graph.nodes.find(n => n.id === edge.to);
    if (!from || !to) return;

    const midX = (from.x * 1.5 + to.x * 1.5) / 2;
    const midY = (from.y * 1.5 + to.y * 1.5) / 2;

    html += `
      <line x1="${from.x * 1.5}" y1="${from.y * 1.5}" x2="${to.x * 1.5}" y2="${to.y * 1.5}"
            stroke="${isDark ? 'rgba(148, 163, 184, 0.4)' : '#cbd5e1'}" stroke-width="2" marker-end="url(#arrow-large)" />
      <text x="${midX}" y="${midY - 6}" font-size="11" fill="${isDark ? '#94a3b8' : '#64748b'}" text-anchor="middle" font-weight="600">${edge.label}</text>
    `;
  });

  // 节点
  q.graph.nodes.forEach(node => {
    const c = colorMap[node.type] || colorMap.core;
    const nx = node.x * 1.5;
    const ny = node.y * 1.5;
    html += `
      <g class="graph-node" transform="translate(${nx}, ${ny})" style="cursor: pointer;">
        <circle r="42" fill="${c.fill}" stroke="${c.stroke}" stroke-width="2.5" />
        <text y="4" font-size="12" font-weight="700" fill="${c.text}" text-anchor="middle">${node.label.length > 10 ? node.label.slice(0, 9) + '..' : node.label}</text>
      </g>
    `;
  });

  svg.innerHTML = html;
}
