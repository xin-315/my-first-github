"""
JC2001 Smart Study Assistant - Curated Multi-Discipline Seed Question Bank
Contains 12 curated questions across 4 subjects (law, cs, econ, se) with 36 fine-grained distractor traps.
"""

from typing import List, Dict
from backend.app.models.quiz import (
    QuizItem,
    OptionItem,
    TrapDetail,
    GraphNode,
    GraphEdge,
    GraphData
)

SEED_QUESTIONS: List[QuizItem] = [
    # =========================================================================
    # 1. LAW (民商法学与民法典)
    # =========================================================================
    QuizItem(
        id="law_1",
        subject="law",
        difficulty="★★★☆☆",
        tag="可撤销民事法律行为 · 撤销权存续期间",
        stem="甲于2023年3月1日因受欺诈与乙签订二手车买卖合同，同年5月1日甲知道该欺诈事由。根据《民法典》关于可撤销民事法律行为的规定，甲请求人民法院撤销该合同的除斥期间应当自何时起算？最迟于何时届满？",
        options=[
            OptionItem(key="A", text="自合同签订之日（2023年3月1日）起算，最迟于 3 年内届满", is_correct=False, trap_id="trap_law_1"),
            OptionItem(key="B", text="自知道受欺诈之日（2023年5月1日）起算，最迟于 1 年内届满", is_correct=True),
            OptionItem(key="C", text="自欺诈行为终止之日起算，最迟于 1 年内届满", is_correct=False, trap_id="trap_law_2"),
            OptionItem(key="D", text="自合同签订之日起算，无论是否知情一律在 2 年内届满", is_correct=False, trap_id="trap_law_3"),
        ],
        explanation="【权威考点解析 · 民法典第152条】：重大误解撤销权自知道之日起90日内行使，受欺诈撤销权自知道或者应当知道之日起1年内行使；自行为发生之日起5年内未行使的撤销权消灭。该期限性质属于除斥期间，不发生中止、中断或延长！",
        traps={
            "trap_law_1": TrapDetail(
                title="🚨 典型混淆陷阱：把'形成权除斥期间'错套为'3年普通诉讼时效'",
                desc="这是全校 64% 学生最常踩的深坑！通用 AI 答题时也经常将《民法典》第 188 条的 3 年诉讼时效套到撤销权上。诉讼时效管的是'请求权'，而撤销权属于'形成权'，必须适用严格的法定除斥期间！",
                prereq="先修定理前置：请求权 vs 形成权区别与法定除斥期间",
                radar_hit="trapDefense"
            ),
            "trap_law_2": TrapDetail(
                title="🚨 规范错配陷阱：把'受欺诈'与'受胁迫'的法定起算点混为一谈",
                desc="《民法典》严格区分受欺诈与受胁迫：受胁迫才自'胁迫行为终止之日'起算；受欺诈则是自'知道或者应当知道撤销事由之日'起算！",
                prereq="先修定理前置：胁迫与欺诈意志瑕疵法定起算条件",
                radar_hit="boundary"
            ),
            "trap_law_3": TrapDetail(
                title="🚨 历史废条死记陷阱：混淆旧合同法与现行民法典",
                desc="误用了已被废止的旧合同法条款。现行民法典明确统一为受欺诈起算 1 年，最长保护期为 5 年（并非 2 年）。",
                prereq="先修定理前置：民法典总则编撤销权体系",
                radar_hit="recall"
            )
        },
        graph=GraphData(
            title="民法典第152条·可撤销民事法律行为拓扑子图",
            nodes=[
                GraphNode(id="c1", label="撤销权除斥期间", type="core", x=260, y=140),
                GraphNode(id="p1", label="知道欺诈之日起 1年", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="行为发生起最长 5年", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="陷阱: 错套3年诉讼时效", type="trap", x=130, y=240),
                GraphNode(id="t2", label="陷阱: 错记胁迫终止点", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="主除斥期间"),
                GraphEdge(from_node="p2", to_node="c1", label="最长保护期"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (混淆权利性质)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (错配起算点)"),
            ]
        ),
        socratic_prompt="同学，请停下来想一想：在民法理论中，当事人要消灭一个已经成立的合同，行使的是让相对人掏钱还货的'请求权'，还是凭单方意思就能变更法律关系的'形成权'？为什么这两种权利的时效规定截然不同？"
    ),

    QuizItem(
        id="law_2",
        subject="law",
        difficulty="★★★★☆",
        tag="物权编 · 动产善意取得构成要件与阻却事由",
        stem="甲将其所有的专业单反相机出借给乙使用，乙擅自以市场公允价 12000 元卖给不知情的摄影爱好者丙，并当场完成交付并收款完毕。一周后甲发现此事，向丙主张相机所有权要求其无偿归还。关于本案法律效力，下列说法完全正确的是？",
        options=[
            OptionItem(key="A", text="因乙对相机无处分权，乙丙之间的买卖合同自始绝对无效，丙不能取得所有权", is_correct=False, trap_id="trap_law_2_1"),
            OptionItem(key="B", text="丙已基于《民法典》善意取得制度原始取得该相机所有权，甲无权要求返还原物", is_correct=True),
            OptionItem(key="C", text="因相机属于出借物而非遗失物，丙必须先行向甲支付合理补偿后方可保留相机", is_correct=False, trap_id="trap_law_2_2"),
            OptionItem(key="D", text="善意取得仅适用于不动产物权，动产在原权利人甲明确追认前处于效力待定状态", is_correct=False, trap_id="trap_law_2_3"),
        ],
        explanation="【权威考点解析 · 民法典第311条与第597条】：① 无处分权人订立的买卖合同有效（彻底废除原合同法第51条效力待定说）；② 善意取得构成要件：受让人受让时善意且无重大过失、以合理价格转让、已依法完成交付。丙完全满足三要件，依法取得动产所有权；甲只能向无权处分人乙主张侵权赔偿或不当得利！",
        traps={
            "trap_law_2_1": TrapDetail(
                title="🚨 废除旧法死记陷阱：把'处分权瑕疵'误等同于'买卖合同绝对无效'",
                desc="这是法学期末和考研 58% 学生极易踩中的传统重灾区！民法典明确区分负担行为（债权合同）与处分行为（物权变动）。买卖合同即使无权处分也有效，不能履行则承担违约责任，善意受让人更直接受善意取得保护！",
                prereq="先修定理前置：债权合同效力与物权变动分离原则",
                radar_hit="recall"
            ),
            "trap_law_2_2": TrapDetail(
                title="🚨 规则混淆陷阱：错把'遗失物盗脏物回赎'套用到'意定借用委托物'上",
                desc="《民法典》第 312 条仅对遗失物等'非基于真正权利人意思脱离占有的物'规定了 2 年内可支付对价请求返还。本案中甲是自愿借给乙的（占有委托物），原权利人必须自担信托风险，根本不存在有偿回赎权利！",
                prereq="先修定理前置：占有脱离物 vs 占有委托物法律后果差异",
                radar_hit="boundary"
            ),
            "trap_law_2_3": TrapDetail(
                title="🚨 制度适用范围盲区：善意取得横跨动产与不动产两大领域",
                desc="通用 AI 常常将动产交付与不动产登记要件张冠李戴。善意取得恰恰是以动产占有公信力与不动产登记公信力为双支柱的法定原始取得制度！",
                prereq="先修定理前置：物权公示与公信原则在动产中的体现",
                radar_hit="trapDefense"
            )
        },
        graph=GraphData(
            title="民法典第311条·善意取得构成与阻却拓扑图",
            nodes=[
                GraphNode(id="c1", label="动产善意取得 (311条)", type="core", x=260, y=140),
                GraphNode(id="p1", label="善意+合理价格+完成交付", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="占有委托物风险归属", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="陷阱: 误判买卖合同无效", type="trap", x=130, y=240),
                GraphNode(id="t2", label="陷阱: 错套遗失物回赎补偿", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="法定三要素"),
                GraphEdge(from_node="p2", to_node="c1", label="阻却原物返还"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (负担与处分行为未区分)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (脱离物与委托物混同)"),
            ]
        ),
        socratic_prompt="同学请思考：如果原所有人甲自己不谨慎把相机借给不可靠的朋友乙，而善意买家丙在市场上付了真金白银拿到了相机，法律为什么要保护丙而不是保护甲？这背后体现了怎样的商事交易安全价值取向？"
    ),

    QuizItem(
        id="law_3",
        subject="law",
        difficulty="★★★★☆",
        tag="总则编 · 表见代理与权利外观责任",
        stem="某软件科技公司解聘了销售副总张某，但疏忽未及时收缴其持有的加盖公司公章的空白业务授权书及合同专用章。次日，张某持上述文件以该科技公司名义，与不知其离职且已尽通常注意义务的某云服务商签订了价值 80 万元的机房服务器租用合同。关于该合同效力与责任，下列说法正确的是？",
        options=[
            OptionItem(key="A", text="张某离职后已无代理权，该合同自始绝对无效，科技公司不负任何民事责任", is_correct=False, trap_id="trap_law_3_1"),
            OptionItem(key="B", text="构成表见代理，该合同对科技公司有效，科技公司须承担合同约定的履约付款责任", is_correct=True),
            OptionItem(key="C", text="该合同属于效力待定合同，若科技公司在法定 30 天内不予追认，则合同直接归于消灭", is_correct=False, trap_id="trap_law_3_2"),
            OptionItem(key="D", text="只有当云服务商能充分证明科技公司高管存在主观欺诈故意时，方能认定表见代理成立", is_correct=False, trap_id="trap_law_3_3"),
        ],
        explanation="【权威考点解析 · 民法典第172条】：行为人没有代理权、超越代理权或者代理权终止后，仍然实施代理行为，相对人有理由相信行为人有代理权的，代理行为有效。公司未收回印章与授权书具有重大过失（可归责的外观），相对人善意无过失，构成表见代理！公司履行后可向张某追偿！",
        traps={
            "trap_law_3_1": TrapDetail(
                title="🚨 机械无权否定陷阱：忽视商事外观法理对善意第三人的倾斜保护",
                desc="很多初学者只看到'张某已离职无权'这半句话，机械认定合同无效。表见代理制度的存在目的，恰恰就是在代理权实质欠缺时，因被代理人造成了权利外观而强制其承受法律后果！",
                prereq="先修定理前置：权利外观理论与信赖利益保护",
                radar_hit="trapDefense"
            ),
            "trap_law_3_2": TrapDetail(
                title="🚨 程序顺位颠倒陷阱：把'表见代理'降级为'狭义无权代理的效力待定'",
                desc="表见代理一旦成立，相对人享有选择权：既可以主张表见代理有效要求公司履约，也可以主动撤销。但被代理人（科技公司）根本无权单方面通过'拒绝追认'来废除合同！",
                prereq="先修定理前置：表见代理与狭义无权代理法律后果断点",
                radar_hit="boundary"
            ),
            "trap_law_3_3": TrapDetail(
                title="🚨 归责要件苛刻化陷阱：混淆'权利外观可归责性'与'侵权故意'",
                desc="认定表见代理完全不需要被代理人具有主观欺诈故意！只要公章管理不善、授权书未收回等客观过失造成了权利外观，就足以认定本人具有可归责性！",
                prereq="先修定理前置：表见代理客观要件与主观要件判定标准",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="民法典第172条·表见代理效力归属拓扑图",
            nodes=[
                GraphNode(id="c1", label="表见代理 (172条)", type="core", x=260, y=140),
                GraphNode(id="p1", label="权利外观+本人过失", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="相对人善意且无过失", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="陷阱: 错判为绝对无效", type="trap", x=130, y=240),
                GraphNode(id="t2", label="陷阱: 误以为必须本人故意", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="外观形成归责"),
                GraphEdge(from_node="p2", to_node="c1", label="信赖保护要件"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (机械无权观)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (苛刻主观要件)"),
            ]
        ),
        socratic_prompt="请同学设身处地推演：如果你是一家供应商，对方拿着盖有鲜章的授权书和公章来签约，你有可能去查他们公司内部今天有没有发红头文件开除这个人吗？法律为什么要让疏于管理印章的公司买单？"
    ),

    # =========================================================================
    # 2. CS (计算机体系结构)
    # =========================================================================
    QuizItem(
        id="cs_1",
        subject="cs",
        difficulty="★★★★☆",
        tag="RISC经典流水线 · 冒险处理与前递旁路",
        stem="在标准五级按序执行流水线（IF, ID, EX, MEM, WB）中，指令 i 为算术运算（如 add R1, R2, R3），紧随其后的指令 i+1（如 sub R4, R1, R5）在执行阶段需要用到 R1。关于此场景下的流水线冒险与优化，下列说法正确的是？",
        options=[
            OptionItem(key="A", text="属于写后读 (WAR) 反相关冒险；五级流水线必须插入 2 个周期停顿", is_correct=False, trap_id="trap_cs_1"),
            OptionItem(key="B", text="属于读后写 (RAW) 真实数据相关；可通过硬件前递旁路 (Forwarding) 消除所有停顿", is_correct=True),
            OptionItem(key="C", text="属于结构冒险 (Structural Hazard)；必须通过将单端口寄存器升级为多端口解决", is_correct=False, trap_id="trap_cs_2"),
            OptionItem(key="D", text="属于控制冒险 (Control Hazard)；需要引入分支历史表 (BHT) 预测执行", is_correct=False, trap_id="trap_cs_3"),
        ],
        explanation="【权威考点解析 · RISC 五级流水线数据前递】：指令 i 在 EX 阶段结束时（ALU 输出端）已经计算出了 R1 的新值，而指令 i+1 在 EX 阶段开始时才需要 R1。通过在 EX/MEM 流水线寄存器引出一根前递直通线（Forwarding Path）送入 ALU 输入端，即可完全消除气泡（Zero Stall）！",
        traps={
            "trap_cs_1": TrapDetail(
                title="🚨 高阶概念死记硬背陷阱：五级顺序流水线根本不可能出现 WAR/WAW 反相关！",
                desc="这是通用大模型极易给出的知识幻觉！只有在支持'乱序执行 (Out-of-Order Execution)'的超标量处理器（如 Tomasulo 架构）中才可能发生 WAR 冒险。在经典五级顺序流水线中，指令按序流淌，前一条指令不可能在后一条指令之后才读取！",
                prereq="先修定理前置：按序执行与乱序执行的前提差异",
                radar_hit="boundary"
            ),
            "trap_cs_2": TrapDetail(
                title="🚨 分类混淆陷阱：误将'寄存器数据传递'判断为'硬件结构资源冲突'",
                desc="结构冒险指的是多个指令在同一时钟周期争夺同一物理部件（例如单端口内存同时读指令与读数据）。题干明确是寄存器数值的前后依赖，是纯粹的数据冒险！",
                prereq="先修定理前置：三大流水线冒险分类边界",
                radar_hit="recall"
            ),
            "trap_cs_3": TrapDetail(
                title="🚨 题意泛化盲猜陷阱：算术指令不存在条件分支",
                desc="控制冒险仅由条件分支（beq, bne）或无条件跳转（jmp）修改 PC 引起，普通算术指令没有任何分支预测需求！",
                prereq="先修定理前置：控制冒险与分支指令语义",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="RISC 五级流水线·数据依赖与前递旁路图谱",
            nodes=[
                GraphNode(id="c1", label="流水线数据冒险 (RAW)", type="core", x=260, y=140),
                GraphNode(id="p1", label="前提: 按序发射执行", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="方案: ALU前递旁路", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="幻觉陷阱: 错套WAR反相关", type="trap", x=130, y=240),
                GraphNode(id="t2", label="混淆陷阱: 错判为结构争用", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="体系结构约束"),
                GraphEdge(from_node="p2", to_node="c1", label="硬件零停顿优化"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (乱序与顺序概念混淆)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (资源争用与数据流混淆)"),
            ]
        ),
        socratic_prompt="吴同学，请观察 MIPS 五级流水线的时空图：在按序发射的情况下，如果一条指令在时钟周期 3 的末尾已经拿到了算术结果，而下一条指令在周期 4 的开始才需要这个结果，为什么我们非要傻等到周期 5 写回寄存器堆才拿呢？中间能搭一条近道吗？"
    ),

    QuizItem(
        id="cs_2",
        subject="cs",
        difficulty="★★★★☆",
        tag="存储层次结构 · Cache 组相联映射与缺失分析",
        stem="某 32 位字节编址处理器配置有 32KB 的数据 Cache，Cache 块大小为 64 字节，采用 4 路组相联（4-Way Set Associative）映射。现程序频繁循环访问步长为 32KB 的大数组导致严重的冲突缺失（Conflict Miss）。下列关于该 Cache 字段划分与缺失优化，叙述完全正确的是？",
        options=[
            OptionItem(key="A", text="主存地址划分为：Tag=19位，Index=7位，Offset=6位；将相联度提升为 8 路可直接缓解冲突缺失", is_correct=True),
            OptionItem(key="B", text="主存地址划分为：Tag=18位，Index=8位，Offset=6位；将替换算法由 LRU 改为 FIFO 可降低缺失率", is_correct=False, trap_id="trap_cs_2_1"),
            OptionItem(key="C", text="主存地址划分为：Tag=20位，Index=6位，Offset=6位；将块大小从 64B 增大到 128B 能根治冲突缺失", is_correct=False, trap_id="trap_cs_2_2"),
            OptionItem(key="D", text="只要在 CPU 内部增加一级指令预取缓冲区（Prefetch Buffer），即可完全消除数据 Cache 的所有缺失", is_correct=False, trap_id="trap_cs_2_3"),
        ],
        explanation="【权威考点解析 · Cache 地址划分与 3C 缺失】：① 块大小 64B = 2⁶，故 Offset = 6 位；总块数 = 32KB / 64B = 512 块；4 路组相联则组数 = 512 / 4 = 128 组 = 2⁷，故 Index = 7 位；Tag = 32 - 7 - 6 = 19 位！② 冲突缺失源于多个数据映射到同一下标组，增大路数（如改为 8 路）或引入 Victim Cache 是经典有效解法！",
        traps={
            "trap_cs_2_1": TrapDetail(
                title="🚨 组数计算与替换策略双重陷阱：混淆 Cache 总块数与组数",
                desc="许多同学直接把 512 块当成 512 组算出 9 位或 8 位 Index。更严重的是，LRU 基于时间局部性是理论与工程最佳基准，FIFO 不仅缺失率更高，还会引发著名的 Belady 异常！",
                prereq="先修定理前置：组相联 Cache 组数计算公式与局部性原理",
                radar_hit="precision"
            ),
            "trap_cs_2_2": TrapDetail(
                title="🚨 块大小盲目增大陷阱：块过大会压缩组数并加剧冲突缺失",
                desc="在 Cache 总容量固定的前提下，盲目增大块大小会导致 Cache 总组数急剧减半，反而使步长访问的冲突缺失雪上加霜，并显著增加主存缺失惩罚（Miss Penalty）！",
                prereq="先修定理前置：3C 缺失模型（冷启动/容量/冲突）权衡博弈",
                radar_hit="boundary"
            ),
            "trap_cs_2_3": TrapDetail(
                title="🚨 部件职责错配陷阱：把指令预取与数据访存混为一谈",
                desc="指令预取缓冲区针对的是顺序指令流的自适应提取，对大步长随机跳转的数据密集型数组读写根本无法起到降低冲突缺失的作用！",
                prereq="先修定理前置：哈佛结构下指令 Cache 与数据 Cache 行为解耦",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="组相联 Cache·地址解码与冲突缺失权衡图谱",
            nodes=[
                GraphNode(id="c1", label="4路组相联 (Index 7位)", type="core", x=260, y=140),
                GraphNode(id="p1", label="块大小64B (Offset 6位)", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="容量32KB (128组/Tag 19位)", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="陷阱: 错把块数当组数", type="trap", x=130, y=240),
                GraphNode(id="t2", label="陷阱: 误以为FIFO优于LRU", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="低位块内寻址"),
                GraphEdge(from_node="p2", to_node="c1", label="相联度与组数约束"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (计算除以路数遗漏)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (替换算法局部性原理违背)"),
            ]
        ),
        socratic_prompt="请同学拿起草稿纸算一算：如果一个水库有 512 个蓄水池，每个池子单独编号。现在我们把每 4 个池子编成一个大组，那么一共有多少个大组？为什么寻址时硬件只需要对组号进行解码，而组内的 4 个池子是并行比较 Tag 的？"
    ),

    QuizItem(
        id="cs_3",
        subject="cs",
        difficulty="★★★★★",
        tag="虚拟存储系统 · TLB 快表与缺页异常处理时序",
        stem="在支持现代多级页表的虚拟内存系统中，当 CPU 执行一条访存指令（如 lw $t0, 0($a0)）发生地址翻译时，下列关于 TLB（快表）、Page Table（页表）以及缺页异常（Page Fault）的时序与硬件协作，哪一项表述是完全正确的？",
        options=[
            OptionItem(key="A", text="若 TLB 命中，CPU 直接获取物理地址并发起内存读取，全程完全无需访问主存中的多级页表", is_correct=True),
            OptionItem(key="B", text="若 TLB 缺失，硬件 MMU 必须立即向操作系统内核报告缺页中断异常（Page Fault），暂停当前进程", is_correct=False, trap_id="trap_cs_3_1"),
            OptionItem(key="C", text="操作系统缺页异常处理程序完成磁盘换页调入后，CPU 从导致缺页指令的'下一条指令 (PC+4)'恢复执行", is_correct=False, trap_id="trap_cs_3_2"),
            OptionItem(key="D", text="页表中的有效位（Valid Bit）为 1 且 TLB 缺失时，该物理页必定已经被完全换出到磁盘交换区", is_correct=False, trap_id="trap_cs_3_3"),
        ],
        explanation="【权威考点解析 · 虚拟地址翻译流水线】：① TLB 是页表的高速缓存，TLB 命中时 1 周期内即可完成 VA 到 PA 转换；② TLB 缺失并不等于缺页（Page Fault）！硬件 Page Walker 自动遍历主存页表，若页表项 Valid=1，仅需将该条目回填 TLB 即可，完全不需要唤醒 OS 缺页处理！③ 缺页属于 Fault 级异常，换页完成后硬件必须重新执行引发异常的本条原指令！",
        traps={
            "trap_cs_3_1": TrapDetail(
                title="🚨 经典混淆高危陷阱：把'TLB Miss'错当成'Page Fault'",
                desc="这是全网大模型乱回答与期末考试 71% 学生必错的核心深坑！TLB 缺失只是快表中没有缓存该页表项，物理页完全可能好端端躺在物理内存中。只有当页表查询发现 Valid=0（该页尚未载入内存）时，才会触发真正的 Page Fault！",
                prereq="先修定理前置：TLB 快表缓存机制 vs 页表有效位语义",
                radar_hit="trapDefense"
            ),
            "trap_cs_3_2": TrapDetail(
                title="🚨 异常返回语义断点陷阱：把'Fault 重执原指令'误套为'Interrupt 返回 PC+4'",
                desc="中断（Interrupt）是异步的，通常返回下一条指令；而缺页属于故障（Fault），访存指令因缺页尚未成功读取数据，若直接跳到下一条指令，当前寄存器将读入垃圾数据，程序逻辑直接崩塌！",
                prereq="先修定理前置：三大异常类型（Interrupt, Trap, Fault）保存 PC 行为准则",
                radar_hit="boundary"
            ),
            "trap_cs_3_3": TrapDetail(
                title="🚨 标志位逻辑彻底反转陷阱：Valid=1 恰恰代表页面在物理内存中",
                desc="Valid/Present 位为 1 代表页面就在主存物理帧中；为 0 才表示页面未分配或已换出到磁盘 Swap 分区！",
                prereq="先修定理前置：页表项 PTE（Valid, Dirty, Reference）结构规范",
                radar_hit="recall"
            )
        },
        graph=GraphData(
            title="虚拟内存·TLB查表与缺页异常处理拓扑图",
            nodes=[
                GraphNode(id="c1", label="VA地址翻译流水线", type="core", x=260, y=140),
                GraphNode(id="p1", label="TLB命中: 1周期直出PA", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="TLB缺失≠缺页 (PageWalk)", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="幻觉陷阱: TLBMiss直报缺页", type="trap", x=130, y=240),
                GraphNode(id="t2", label="陷阱: 缺页返回跳至PC+4", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="命中快速通道"),
                GraphEdge(from_node="p2", to_node="c1", label="硬件自动补填"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (未区分TLB与页表层级)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (混淆Fault与Interrupt返回)"),
            ]
        ),
        socratic_prompt="请同学回想一下：如果一个图书管理员记性特别好（TLB），但他脑子里记不住某本书放在哪个书架上了（TLB Miss），是不是意味着这本书就一定被图书馆扔掉或者借走了呢？他去翻一下总目录卡片（Page Table）是不是就能查到了？"
    ),

    # =========================================================================
    # 3. ECON (计量经济学)
    # =========================================================================
    QuizItem(
        id="econ_1",
        subject="econ",
        difficulty="★★★★☆",
        tag="经典假定违背 · 多重共线性与遗漏变量偏差",
        stem="在多元回归模型 Y = β₀ + β₁X₁ + β₂X₂ + u 中，若自变量 X₁ 与 X₂ 之间存在严重但非完全的多重共线性，下列关于普通最小二乘法 (OLS) 估计量性质的描述中，哪一项是完全正确的？",
        options=[
            OptionItem(key="A", text="OLS 估计量失去无偏性 (Biased)，产生严重内生性偏差，无法客观反映总体真实参数", is_correct=False, trap_id="trap_econ_1"),
            OptionItem(key="B", text="高斯-马尔可夫定理完全失效，OLS 估计量不再属于最佳线性无偏估计 (BLUE)", is_correct=False, trap_id="trap_econ_2"),
            OptionItem(key="C", text="OLS 估计量依然保持无偏性与 BLUE 性质，但参数方差膨胀，导致 t 检验失效", is_correct=True),
            OptionItem(key="D", text="模型的总判定系数 R² 会严重受挫跌落至接近 0", is_correct=False, trap_id="trap_econ_3"),
        ],
        explanation="【权威考点解析 · 多重共线性的统计学后果】：在严格外生假定 E(u|X)=0 和同方差假定下，只要不存在'完全共线性'（|X'X| ≠ 0），高斯-马尔可夫定理全部成立！OLS 依然是无偏且 BLUE 的！共线性的真正后果是方差膨胀因子 (VIF) 剧增，标准误过大，单个变量的 t 统计量显著下降，但总体回归方程的 F 检验和 R² 通常依然很高！",
        traps={
            "trap_econ_1": TrapDetail(
                title="🚨 混淆无偏性与有效性边界：把'估计精度不足'误等同于'估计量有偏'",
                desc="很多学生以及未经图谱事实约束的通用大模型，张口就回答'估计量有偏'！有偏（Bias）只有在遗漏关键变量或存在内生性时才会发生。自变量之间有相关性绝不破坏无偏性！",
                prereq="遗漏变量偏差与高斯-马尔可夫定理：无偏性数学证明前提 E(u|X)=0",
                radar_hit="recall"
            ),
            "trap_econ_2": TrapDetail(
                title="🚨 定理条件理解陷阱：误判 BLUE 性质失效",
                desc="在所有线性无偏估计量中，OLS 依然是方差最小的那个（BLUE），只是此时这个'最小方差'本身已经被样本数据推高了而已。",
                prereq="先修定理前置：高斯-马尔可夫定理证明边界",
                radar_hit="boundary"
            ),
            "trap_econ_3": TrapDetail(
                title="🚨 经典反常识表象陷阱：共线性下 R² 和 F 往往虚高！",
                desc="多重共线性的最经典教科书表象就是：F 检验极度显著、R² 很高（如 0.85），但每个自变量的 t 检验都无法拒绝原假设！",
                prereq="先修定理前置：联合假设 F 检验与个体 t 检验差异",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="多重共线性·统计性质与诊断陷阱拓扑图",
            nodes=[
                GraphNode(id="c1", label="多重共线性 (Multicollinearity)", type="core", x=260, y=140),
                GraphNode(id="p1", label="假定成立: E(u|X)=0 (严格外生)", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="性质: 依然为 BLUE (无偏且有效)", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="幻觉陷阱: 错判为产生内生偏误", type="trap", x=130, y=240),
                GraphNode(id="t2", label="表象陷阱: 误以为 R² 会暴跌", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="保证无偏前提"),
                GraphEdge(from_node="p2", to_node="c1", label="最小方差性质"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (混淆有偏与方差大)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (忽略总体F检验)"),
            ]
        ),
        socratic_prompt="请思考：高斯-马尔可夫定理中保证OLS无偏性的关键假定是什么？遗漏的变量进入了误差项，此时自变量与误差项是否仍然正交？参数估计值的期望值是否等于真实总体参数？"
    ),

    QuizItem(
        id="econ_2",
        subject="econ",
        difficulty="★★★★★",
        tag="因果推断核心 · 工具变量法 (IV/2SLS) 与弱工具变量",
        stem="在估算教育年限（Educ）对对数工资水平（ln(Wage)）的因果效应方程中，因存在无法直接观测的'个人天生能力'遗漏，解释变量 Educ 产生严重内生性。研究人员选取'受教育者家庭距离最近大学的公里数 (Distance)'作为候选工具变量 Z。下列关于工具变量有效性及两阶段最小二乘法（2SLS）性质的论述，完全正确的是？",
        options=[
            OptionItem(key="A", text="Z 必须同时满足相关性条件（Cov(Z, Educ) ≠ 0）和严格的外生性排他性假定（Cov(Z, u) = 0 且 Z 不能直接决定工资）", is_correct=True),
            OptionItem(key="B", text="即便第一阶段回归的 F 统计量仅为 2.8（远低于 10），只要样本量 N 趋于无穷大，2SLS 估计量依然绝对无偏且方差最小", is_correct=False, trap_id="trap_econ_2_1"),
            OptionItem(key="C", text="在模型恰好识别（内生变量数 = 工具变量数 = 1）时，可直接通过过度识别检验（Sargan-Hansen Test）在统计学上严格检验 Z 是否外生", is_correct=False, trap_id="trap_econ_2_2"),
            OptionItem(key="D", text="为了提高因果解释力，合格的工具变量 Z 必须对因变量 ln(Wage) 具有显著而直接的强相关推动力", is_correct=False, trap_id="trap_econ_2_3"),
        ],
        explanation="【权威考点解析 · 工具变量法与因果识别】：① 工具变量两大铁律：外生性条件（Exogeneity，与扰动项正交且无直接因果通路）+ 相关性条件（Relevance，与内生变量强相关）；② Staiger-Stock 经验法则：第一阶段 F > 10 方可排除弱工具变量风险！弱工具变量会导致 2SLS 甚至比普通 OLS 偏误更大！③ 恰好识别时模型自由度为 0，外生性假定必须依赖经济学理论论证，数学上不可直接检验！",
        traps={
            "trap_econ_2_1": TrapDetail(
                title="🚨 弱工具变量致命盲区：大样本并不能自动拯救弱工具变量的严重偏误",
                desc="这是计量经济学实证顶级翻车现场！当第一阶段相关性微弱时（F < 10），2SLS 的渐近偏误会朝 OLS 方向靠拢，抽样分布极度肥尾畸变，常规标准误完全失效，甚至产生毁灭性虚假因果！",
                prereq="先修定理前置：Staiger-Stock 弱工具变量与有限样本偏误定理",
                radar_hit="boundary"
            ),
            "trap_econ_2_2": TrapDetail(
                title="🚨 自由度与识别条件数学盲区：恰好识别根本无法进行统计外生性检验",
                desc="过度识别检验（如 Sargan Test / Hansen J 统计量）的前提是工具变量个数 m 严格大于内生变量个数 k（即 m > k）。恰好识别时残差与预测值完全正交，残差平方和自由度为 0，根本无法做检验！",
                prereq="先修定理前置：Sargan-Hansen 过度识别检验统计自由度定义",
                radar_hit="precision"
            ),
            "trap_econ_2_3": TrapDetail(
                title="🚨 排他性约束彻底颠倒：合格的工具变量绝对不能直接影响因变量！",
                desc="排他性约束（Exclusion Restriction）的严苛定义是：工具变量 Z 只能'通过内生变量 Educ 这唯一通道'间接影响工资！若 Z 本身直接决定工资，则该变量直接进入原方程扰动项，外生性荡然无存！",
                prereq="先修定理前置：DAG 因果有向无环图与排他性约束定理",
                radar_hit="trapDefense"
            )
        },
        graph=GraphData(
            title="因果推断·工具变量识别与外生性约束拓扑图",
            nodes=[
                GraphNode(id="c1", label="2SLS 工具变量识别", type="core", x=260, y=140),
                GraphNode(id="p1", label="排他性外生: Cov(Z,u)=0", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="强相关检验: 阶段一F>10", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="弱工具陷阱: F<10致严重偏误", type="trap", x=130, y=240),
                GraphNode(id="t2", label="错位陷阱: 恰好识别做Sargan", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="因果外生约束"),
                GraphEdge(from_node="p2", to_node="c1", label="识别强度门禁"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (低估弱工具破坏力)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (忽视检验自由度约束)"),
            ]
        ),
        socratic_prompt="请同学在脑海中画一条因果箭头：如果离大学近的地区本身就是高工资的沿海大城市（即 Z 直接影响了 Wage），那我们怎么可能分清楚那些高工资是因为多读了书，还是因为出生在大城市呢？这就是为什么排他性约束如此至关重要！"
    ),

    QuizItem(
        id="econ_3",
        subject="econ",
        difficulty="★★★★☆",
        tag="经典假定违背 · 异方差性怀特检验与稳健标准误",
        stem="在截面家庭消费支出回归中，富裕家庭的储蓄与消费弹性差异远大于低收入家庭，导致误差项呈现随收入增加而发散的异方差性（Var(u_i|X_i) = σ_i²）。下列关于异方差对 OLS 的危害、检验方法及修正策略的叙述中，哪一项完全符合现代实证规范？",
        options=[
            OptionItem(key="A", text="存在异方差时，OLS 估计量 β̂ 彻底失去无偏性与一致性，算出来的回归系数数值完全毫无参考价值", is_correct=False, trap_id="trap_econ_3_1"),
            OptionItem(key="B", text="怀特检验（White Test）要求研究者必须预先知道异方差的具体数学形式（如指数形式或线性形式）方可实施", is_correct=False, trap_id="trap_econ_3_2"),
            OptionItem(key="C", text="OLS 估计量依然无偏且一致，但传统公式计算的标准误严重有偏；现代学界通用做法是直接采用 White 稳健标准误（Robust Standard Errors）进行统计推断", is_correct=True),
            OptionItem(key="D", text="采用加权最小二乘法 (WLS) 在任何情况下都无条件优于 OLS 稳健回归，绝对不可能引入新的模型设定误差", is_correct=False, trap_id="trap_econ_3_3"),
        ],
        explanation="【权威考点解析 · 异方差后果与稳健推断】：① 异方差违背同方差假定，破坏高斯-马尔可夫定理的'有效性（BLUE）'，但完全不影响期望 E(β̂)=β，故 OLS 估计量依然无偏且一致！② 异方差的真正致命伤是传统公式计算的 Var(β̂) 有偏，导致 t 统计量和置信区间全线失真！③ 怀特检验通过辅助回归无需预设异方差形式，学界当前黄金准则是报告 OLS 系数并配备 Heteroskedasticity-Robust 标准误（如 Stata 中的 , robust）！",
        traps={
            "trap_econ_3_1": TrapDetail(
                title="🚨 性质混淆高频深坑：把'有效性受损'误判为'估计量失去无偏性'",
                desc="全班 60% 同学会脱口而出'OLS 估计量有偏'！无偏性的唯一前提是外生性 E(u|X)=0。残差方差变大变小，只是让估计量的抽样波动变大，绝不会让总体平均估计中心发生系统性偏移！",
                prereq="先修定理前置：无偏性条件 vs BLUE 有效性条件断点对比",
                radar_hit="recall"
            ),
            "trap_econ_3_2": TrapDetail(
                title="🚨 统计检验机制混淆：误把'怀特检验'等同于依赖具体形式的检验",
                desc="怀特检验最大的突破性贡献，正是由于它将残差平方对所有自变量的一阶项、平方项及交互项做辅助回归，完全不需要研究者猜测异方差是哪种特定函数！",
                prereq="先修定理前置：White (1980) 渐近大样本辅助回归构造原理",
                radar_hit="boundary"
            ),
            "trap_econ_3_3": TrapDetail(
                title="🚨 WLS 盲目盲信反模式：错误权重的 WLS 甚至比 OLS 还要糟糕",
                desc="可行广义最小二乘法 (FGLS/WLS) 只有在研究者准确猜对异方差函数结构时才渐近有效。若权重矩阵设定错误，WLS 的估计量反而会失去一致性，因此现代顶级实证论文几乎清一色采用 OLS + Robust 标准误！",
                prereq="先修定理前置：FGLS 稳健性风险与夹心方差估计量（Sandwich Estimator）",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="异方差·成因后果与怀特稳健推断图谱",
            nodes=[
                GraphNode(id="c1", label="异方差性 (Var(u|X)=σi²)", type="core", x=260, y=140),
                GraphNode(id="p1", label="系数保持无偏与一致", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="对策: White稳健标准误", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="误区: 错判OLS系数有偏", type="trap", x=130, y=240),
                GraphNode(id="t2", label="误区: 盲目套用WLS权重", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="外生假定成立"),
                GraphEdge(from_node="p2", to_node="c1", label="夹心协方差修正"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (混淆方差大与期望偏)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (忽视权重设定偏误)"),
            ]
        ),
        socratic_prompt="请同学思考：如果一台电子秤只是偶尔称重读数抖动变大（方差大），但平均下来称 100 次的均值依然是完全准确的（无偏），我们应该直接扔掉这台秤，还是给它换一个能正确计算误差范围的合格说明书（稳健标准误）？"
    ),

    # =========================================================================
    # 4. SE (软件工程与系统设计)
    # =========================================================================
    QuizItem(
        id="se_1",
        subject="se",
        difficulty="★★★☆☆",
        tag="软件过程模型 · 敏捷 Scrum 与瀑布模型适用权衡",
        stem="在某智慧医院核心业务系统研发项目中，急诊排班与医保微服务接口的需求受政策影响变动极为频繁且不确定，但底层患者核心电子病历的归档存储模块受到国家卫健委《三级医院评审标准》极其严苛的合规性与审计可追溯性约束。关于该项目的软件过程模型选择，下列哪种策略最为科学合理？",
        options=[
            OptionItem(key="A", text="强制推行纯瀑布模型（Waterfall），在阶段一彻底冻结所有医保与排班需求规格说明书后才允许进入编码阶段", is_correct=False, trap_id="trap_se_1_1"),
            OptionItem(key="B", text="采用混合软件过程模型（Hybrid Model），底层强合规与稳定架构采用架构先行和严格文档，高频易变的业务服务采用 2 周 Sprint 的 Scrum 敏捷迭代验证", is_correct=True),
            OptionItem(key="C", text="彻底废弃所有软件架构设计文档与测试用例，全盘采用极限编程（XP），依靠每天结对重构解决所有国家合规性评审", is_correct=False, trap_id="trap_se_1_2"),
            OptionItem(key="D", text="采用大爆炸模型（Big Bang Model），由开发人员在期末截止前一周连续通宵一次性交付全量代码", is_correct=False, trap_id="trap_se_1_3"),
        ],
        explanation="【权威考点解析 · 软件生命周期模型权衡】：根据 Boehm 软件工程经济学定律，需求变更成本随项目周期呈指数级增长。面对'高变动度业务'强推瀑布模型必然导致项目严重延期超支；而在'高合规性底层'盲目推行极端零文档开发必然导致验收失败。业内成熟工业实践普遍采用 Hybrid 敏捷双轨制：架构约束基线受控，前端应用敏捷迭代！",
        traps={
            "trap_se_1_1": TrapDetail(
                title="🚨 传统教条主义瀑布陷阱：在易变业务中强行'冻结需求'",
                desc="很多刚学软件工程的同学盲目崇拜瀑布模型的严密性，忽视了当外部业务或政策月月变更时，瀑布模型的前后阶段强依赖会导致全团队陷入永无止境的'需求变更提交流程'和代码大规模推倒重来！",
                prereq="先修定理前置：Boehm 软件变更成本指数曲线与瀑布局限性",
                radar_hit="boundary"
            ),
            "trap_se_1_2": TrapDetail(
                title="🚨 敏捷宣言教条化误读陷阱：把'拥抱变更'误等同于'不要任何文档和架构'",
                desc="敏捷宣言原文是'可工作的软件胜于详尽的文档'，绝不是'不要文档'！在医疗、金融、航天等安全关键系统（Safety-critical systems）中，需求追溯矩阵（RTM）和接口契约文档是法律法规强制要求的一票否决项！",
                prereq="先修定理前置：敏捷宣言核心原则与合规性系统工程规范",
                radar_hit="recall"
            ),
            "trap_se_1_3": TrapDetail(
                title="🚨 反工程开发模式陷阱：大爆炸模型是混乱工程的代名词",
                desc="无计划、无阶段审查、无测试门禁的大爆炸模型违背了软件工程的一切基本原则，是导致绝大多数软件项目彻底报废的头号反模式！",
                prereq="先修定理前置：软件危机本质与现代软件工程控制论",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="软件过程模型·敏捷迭代与架构合规权衡图谱",
            nodes=[
                GraphNode(id="c1", label="混合敏捷过程模型 (Hybrid)", type="core", x=260, y=140),
                GraphNode(id="p1", label="底层强合规: 架构基线受控", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="变动业务层: 2周Scrum迭代", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="教条瀑布: 强行冻结变动需求", type="trap", x=130, y=240),
                GraphNode(id="t2", label="伪敏捷: 盲目抛弃所有架构文档", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="合规质量底线"),
                GraphEdge(from_node="p2", to_node="c1", label="快速拥抱变更"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (教条僵化开发)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (放任混乱无序)"),
            ]
        ),
        socratic_prompt="请同学思考：如果一栋大厦的地基和承重梁（合规核心）要求必须有图纸审查且绝对不能摇晃，而顶层的办公室隔断（变动业务）租户随时想要调整，我们应该全部打掉重盖，还是应该在地基稳固的前提下采用可移动轻量隔断？"
    ),

    QuizItem(
        id="se_2",
        subject="se",
        difficulty="★★★★☆",
        tag="面向对象架构设计 · SOLID 原则与依赖倒置 (DIP)",
        stem="在设计一个多源学术文献知识图谱抽取引擎时，上层核心分析业务类 LiteratureAnalyzer 直接通过硬编码实例化了具体的 MySQL 数据库客户端（即 this.db = new MySQLClient()）。现因业务扩展需要支持分布式图数据库 Neo4j 及向量数据库 Milvus。根据 SOLID 设计原则中的依赖倒置原则（DIP），应如何实施最佳重构？",
        options=[
            OptionItem(key="A", text="在 LiteratureAnalyzer 内部增加大量的 if-else 或 switch-case 语句，根据传入的环境变量分别执行不同数据库的私有操作代码", is_correct=False, trap_id="trap_se_2_1"),
            OptionItem(key="B", text="抽象出统一的 IKnowledgeStorage 契约接口，使上层 LiteratureAnalyzer 与具体的 MySQLClient/Neo4jClient 均只依赖该抽象接口，通过构造函数依赖注入（DI）解耦", is_correct=True),
            OptionItem(key="C", text="直接让 Neo4jClient 类强制继承自 MySQLClient 类，并通过重写（Override）覆写其中的关系查询方法", is_correct=False, trap_id="trap_se_2_2"),
            OptionItem(key="D", text="将所有数据库操作逻辑整合到一个全局公共上帝类（God Class）GlobalDBManager 中，由业务类直接调用其静态方法", is_correct=False, trap_id="trap_se_2_3"),
        ],
        explanation="【权威考点解析 · SOLID 原则与依赖倒置 DIP】：① 依赖倒置原则定义：高层模块不应该依赖低层模块，两者都应该依赖抽象；抽象不应该依赖细节，细节应该依赖抽象。② 方案 B 通过引入 IKnowledgeStorage 接口，解除了高层分析类对底层持久化技术的紧耦合，新增图数据库或向量数据库只需扩展新实现类，无需改动现有业务逻辑，同时完美符合开闭原则（OCP）！",
        traps={
            "trap_se_2_1": TrapDetail(
                title="🚨 分支蔓延坏味道陷阱：严重违反开闭原则 (OCP)",
                desc="用大量的条件分支（if-else）来扩展底层实现是初学者最常犯的工程坏味道！每次接入新数据库都要修改高层业务代码并重新编译测试，极易引发回归缺陷（Regression Bugs）！",
                prereq="先修定理前置：开闭原则（OCP：对扩展开放，对修改关闭）",
                radar_hit="trapDefense"
            ),
            "trap_se_2_2": TrapDetail(
                title="🚨 继承滥用深坑：严重违反里氏替换原则 (LSP)",
                desc="图数据库和关系型数据库在数据模型、事务语义和查询契约上根本不存在'is-a'的派生替换关系！强行继承导致基类契约被肆意破坏，子类无法安全替换父类！",
                prereq="先修定理前置：里氏替换原则（LSP）与契约式设计（DbC）",
                radar_hit="boundary"
            ),
            "trap_se_2_3": TrapDetail(
                title="🚨 上帝类紧耦合陷阱：制造单点故障并扼杀单元测试",
                desc="引入全局万能上帝类（God Class）是典型的反模式，导致系统内聚度（Cohesion）极低而耦合度（Coupling）极高，全局状态混乱，且单元测试中将彻底无法进行依赖 Mock！",
                prereq="先修定理前置：单一职责原则（SRP）与单元测试 Mock 隔离要求",
                radar_hit="synthesis"
            )
        },
        graph=GraphData(
            title="SOLID架构·依赖倒置与接口隔离设计图谱",
            nodes=[
                GraphNode(id="c1", label="依赖倒置原则 (DIP)", type="core", x=260, y=140),
                GraphNode(id="p1", label="抽象契约接口 (IKnowledgeStorage)", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="依赖注入解耦 (DI/IoC)", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="坏味道: if-else破坏OCP", type="trap", x=130, y=240),
                GraphNode(id="t2", label="坏味道: 乱继承破坏LSP", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="面向接口编程"),
                GraphEdge(from_node="p2", to_node="c1", label="控制反转实现"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (业务与底层技术硬绑定)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (为了复用代码滥用继承)"),
            ]
        ),
        socratic_prompt="请同学想象一下家里的电源插座：国标三孔插座定义了一套抽象规范（接口），无论是台灯、电脑还是电冰箱（实现类），只要符合插头规范就能插上工作。如果每买一台新电器，我们都得把墙砸开重新接线（修改业务代码），这样的设计能持续吗？"
    ),

    QuizItem(
        id="se_3",
        subject="se",
        difficulty="★★★★☆",
        tag="软件质量保证 · 边界值分析与变异测试 (Mutation Testing)",
        stem="在开发学生成绩管理系统的GPA计算模块时，某函数要求输入单门课程学分必须落在有效区间 [0.5, 10.0] 之间。关于该模块的黑盒测试用例设计以及自动化测试套件的充分性度量，下列说法完全正确的是？",
        options=[
            OptionItem(key="A", text="只要测试套件在代码行覆盖率（Line Coverage）上达到了 100%，就足以证明所有边界值缺陷已被完全消除，无需进一步质量检验", is_correct=False, trap_id="trap_se_3_1"),
            OptionItem(key="B", text="边界值分析（BVA）不仅应选取边界上及边界内的值（如 0.5, 0.6, 9.9, 10.0），还必须选取边界外紧邻的无效输入（如 0.4, 10.1）检验防御性拦截；变异测试通过在源代码中植入变异体（Mutant）来客观度量测试用例的真正杀伤力", is_correct=True),
            OptionItem(key="C", text="边界值分析法要求测试人员只能输入合法范围内的有效数据，严禁输入任何负向或越界的无效数据", is_correct=False, trap_id="trap_se_3_2"),
            OptionItem(key="D", text="变异测试是一种专门用于测量系统在 10 万人并发选课时服务器 CPU 占用率的白盒压力测试工具", is_correct=False, trap_id="trap_se_3_3"),
        ],
        explanation="【权威考点解析 · 边界值测试与变异测试杀灭率】：① 绝大多数程序 Bug 发生在输入输出边界处，边界值分析（BVA）必须包含正向与负向邻界值（如 0.4 与 10.1 阻断拦截）；② 覆盖率幻觉（Coverage Illusion）：100% 语句覆盖完全可能包含大量'无断言弱测试'（Assertion-free Tests）！变异测试通过自动把 `>=` 改为 `>`、`+` 改为 `-` 等方式产生代码变异体，唯有测试用例能令变异体报错失败（Killed），才能证明测试套件具备真正的缺陷捕获能力！",
        traps={
            "trap_se_3_1": TrapDetail(
                title="🚨 虚假覆盖率安全感陷阱：高行覆盖率 ≠ 高检错能力",
                desc="这是软件工程质量门禁中最危险的盲区！测试代码执行了每一行，并不代表它断言了每一行的逻辑正确性！如果测试用例中没有任何 assert，覆盖率依然可以显示 100%，但变异测试杀伤率将直降为 0！",
                prereq="先修定理前置：测试充分性准则与变异分数（Mutation Score）定义",
                radar_hit="trapDefense"
            ),
            "trap_se_3_2": TrapDetail(
                title="🚨 负向测试缺失陷阱：忽略边界外拦截测试直接导致生产崩溃",
                desc="只测试合法数据（Positive Testing）是脆弱软件的典型征兆。健壮性测试必须覆盖紧邻边界外的无效等价类，确保异常被安全捕获并抛出受控错误，而非直接抛出未捕获异常导致系统崩溃！",
                prereq="先修定理前置：等价类划分与健壮性边界值分析矩阵",
                radar_hit="boundary"
            ),
            "trap_se_3_3": TrapDetail(
                title="🚨 测试类型概念错配陷阱：把'变异测试'误判为'性能压测'",
                desc="变异测试是著名的'测试你的测试（Testing the Tests）'的高级元测试技术，属于缺陷注入（Fault Injection）和测试集能力评价领域，与性能压测完全无关！",
                prereq="先修定理前置：故障注入机制与自动化变异算子（Mutator）分类",
                radar_hit="recall"
            )
        },
        graph=GraphData(
            title="质量保证·边界值分析与变异测试杀伤力拓扑图",
            nodes=[
                GraphNode(id="c1", label="变异测试 (Mutation Testing)", type="core", x=260, y=140),
                GraphNode(id="p1", label="BVA: 跨越正负边界取样", type="prereq", x=120, y=60),
                GraphNode(id="p2", label="破除弱断言: 杀灭率评价", type="prereq", x=400, y=60),
                GraphNode(id="t1", label="虚荣陷阱: 迷信100%行覆盖率", type="trap", x=130, y=240),
                GraphNode(id="t2", label="概念陷阱: 误判变异测试为压测", type="trap", x=390, y=240),
            ],
            edges=[
                GraphEdge(from_node="p1", to_node="c1", label="高危边界敏感度"),
                GraphEdge(from_node="p2", to_node="c1", label="测试用例质量度量"),
                GraphEdge(from_node="c1", to_node="t1", label="易错于 (忽略断言有效性)"),
                GraphEdge(from_node="c1", to_node="t2", label="易错于 (测试类型概念混同)"),
            ]
        ),
        socratic_prompt="请同学思考：如果一个保安只是把公司的每一个房间门推开看了一眼（代码行覆盖率 100%），但他根本不认识谁是小偷（没有写判断断言 assert），那么当真正有小偷把房间里的电脑搬走时（变异体引入），这个保安能发出警报吗？"
    ),
]


def get_seed_questions() -> List[QuizItem]:
    """Return all seed quiz items."""
    return list(SEED_QUESTIONS)
