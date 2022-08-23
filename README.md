## 怪异炼化词条自动填充

### 目前的问题

目前，配装器已经支持用户输入/导入怪异炼化记录，从而实现带怪异炼化的配装搜索。

然而，很多时候玩家的问题并不是“我如何利用我已经怪异炼化完成的装备”，而是“我想配出一套含有某些技能的配装，为此我需要怪异炼化哪些装备”。目前的解决方案，并不能很好地支持这一需求。如果配装器能够自动生成带有怪异炼化词条的防具，那么对此类玩家将有很大的帮助。

同时，怪异炼化的特殊之处在于它带有强烈的随机要素。如果配装器搜索出一套配装，其上使用了一件非常极限的怪异炼化防具，由于大多数 NS 玩家和没有 mod 的 PC 玩家都不太可能做出这一防具，所以这套配装的指导意义将会非常有限。虽然通过“观星”和“嫁接”的方式可以某种程度上缓解这一问题，但是有指导性的配装中，仍应该使用“出货”概率相对大的怪异炼化防具。

综上所述：

- 配装器需要自动生成带有怪异炼化词条的防具，并用于配装；
- 配装器生成的防具的“出货”概率不能过低。

### 太长不看

目前我们的配装器支持了上述需求。您需要注意的是：

- 您可以在 2%, 0.5% 和 0.01% 三档中，根据您的实际需要选取所需概率；
- 对于每件防具，配装器只会生成“技能等级+1”或者“孔位+n”两类词条之一，且不会同时生成两个词条；
- 配装器会提示每件带有生成词条的防具的“出货”概率。概率的算法详见后文，它的实际意义是，通过单次怪异炼化得到带有生成的词条，且不带有任何“技能等级-1”词条的防具的概率。由于“技能等级-1”词条并不一定会影响配装，因此实际概率可能会略高于配装器提示概率。后续研究可能会得出一个更加精确估计概率的方法；
- 在开启该功能时，“技能可以追加的等级”的准确度将会急剧下降。它提示的可以追加的技能仍然可以追加，但是未提示的技能或者等级追加后也可能有解。后续研究可能会解决该问题；
- 目前的优化水平不高，在开启该功能时，搜索可能会需要数分钟。

### 怪异炼化词条概率

经过大佬们的辛勤研究，目前曙光中新增的怪异炼化的词条生成机制已经被研究得相当透彻了，您可以参考下面的帖子：

https://bbs.nga.cn/read.php?tid=33109101

（与此同时，再次感谢 [@yohasakura](https://bbs.nga.cn/nuke.php?func=ucp&uid=51032) 版主大大，[@dtlnor](https://space.bilibili.com/1887638) 大佬，[@少年A](https://space.bilibili.com/359203633) 大佬等为怪异炼化研究做出卓越贡献的各位）

根据帖子中描述的原理，可以很简单地写出模拟程序 (见本 repo 中的 [qurious_entry_monte_carlo.py](https://github.com/applepi-icpc/qurious-filling-introduction/blob/master/qurious_entry_monte_carlo.py))，使用蒙特卡洛方法估计不同装备实际出不同词条的概率。

程序在一开始定义了两个参数：

```python
MONTE_CARLO_LOOPS = 5000000
CONSIDER_DROP_SKILL = True
```

其中 `MONTE_CARLO_LOOPS` 表示针对每类装备进行模拟的次数；`CONSIDER_DROP_SKILL` 表示是否考虑丢弃技能这一情况，具体含义会在后面详述。

实际运行这个程序，可以得到如下结果 (由于蒙特卡洛方法的原理，多次运行结果会略有不同)：

|   COST | SKILL_1   | SKILL_2   | SKILL_3   | SKILL_4   | SKILL_5   | DECO_1   | DECO_2   | DECO_3   | DECO_4+   |
|--------|-----------|-----------|-----------|-----------|-----------|----------|----------|----------|-----------|
|     20 | 1.244 %   | 0.868 %   | 0.999 %   | 0.803 %   | 0.341 %   | 13.711 % | 2.678 %  | 0.271 %  | 0.007 %   |
|     18 | 1.232 %   | 0.836 %   | 0.796 %   | 0.753 %   | 0.310 %   | 12.709 % | 2.053 %  | 0.141 %  | 0.002 %   |
|     16 | 1.223 %   | 0.820 %   | 0.758 %   | 0.539 %   | 0.185 %   | 11.915 % | 1.530 %  | 0.065 %  | 0.000 %   |
|     14 | 1.208 %   | 0.788 %   | 0.554 %   | 0.501 %   | 0.123 %   | 10.678 % | 1.092 %  | 0.037 %  | 0.000 %   |
|     12 | 1.145 %   | 0.641 %   | 0.522 %   | 0.218 %   | 0.061 %   | 9.352 %  | 0.734 %  | 0.021 %  | 0.000 %   |
|     10 | 1.101 %   | 0.622 %   | 0.331 %   | 0.202 %   | 0.003 %   | 8.441 %  | 0.484 %  | 0.010 %  | 0.000 %   |

其中，`COST` 列代表防具的初始 COST。您可以在 [这里](https://docs.qq.com/sheet/DRlJVTWpwUkVRallz?tab=lpncye) 查看防具与初始 COST 的对应关系 (**注意**：目前不考虑风雷神装备)。

`SKILL_n` 列表示该防具经过一次炼化，得到“某 n 类技能等级+1”效果的概率。其中 1, 2, 3, 4, 5 类技能分别对应 [这里](https://docs.qq.com/sheet/DRlJVTWpwUkVRallz?tab=gbypuk) 所描述的 COST 为 3, 6, 9, 12, 15 的技能。

`DECO_n` 列表示防具经过一次炼化，得到“孔位+n”效果的概率。

这里有三点值得注意：
- 计算上表时，`CONSIDER_DROP_SKILL` 设置为了 `True`，它的含义是，只要装备炼化出了“技能等级-1”词条，就将此装备视为无用，不计入上表的概率。在实践中，带有“技能等级-1”词条的装备不一定会损失有效技能，因此实际的出率会略高于该表；
- “某 n 类技能等级+1”的概率指得到具体某一个技能的概率，而不是得到任一个该类技能的概率。在计算时，我们假定技能都是在对应类的表中等概率抽选的；
- 上表中“某 n 类技能等级+1”与“孔位+n”这两个事件不独立。因此，用两个概率相乘来估计同时发生这两个事件的概率可能有误差。

从中我们可以发现，“某 n 类技能等级+1”属于低概率事件。如要在怪异炼化中同时获得两个确定的技能，或者获取一个确定的技能外加孔位扩张的话，虽然由于事件不独立，将概率简单相乘会有误差，但是仍然可以定性地认为“这是十分困难的” (概率估计在千分之一以下)。因此，从现实角度出发，我们决定让配装器最多追加一个词条。

此外，我们现在直接忽略了带有“技能等级-1”词条的装备的概率。即使将带有“技能等级-1”词条的装备也纳入计算，概率的提升也不明显（例如，初始 COST 为 20 的防具，得到“孔位+1”词条的概率从现在的 13.7% 提高到了约 18.0%）。在今后的研究中，会尝试得出一种根据配装和装备，将这一部分概率修正的方法。

在实际的配装器中，为了数值“好看”，以及程序编写方便，我们使用下面的概率表：


|   COST | SKILL_1   | SKILL_2   | SKILL_3   | SKILL_4   | SKILL_5   | DECO_1   | DECO_2   | DECO_3   | DECO_4+   |
|--------|-----------|-----------|-----------|-----------|-----------|----------|----------|----------|-----------|
|     20 | 1.25 %    | 0.85 %    | 1.00 %    | 0.80 %    | 0.35 %    | 13.70 %  | 2.70 %   | 0.25 %   | 0.00 %    |
|     18 | 1.25 %    | 0.80 %    | 0.80 %    | 0.75 %    | 0.30 %    | 12.70 %  | 2.05 %   | 0.15 %   | 0.00 %    |
|     16 | 1.25 %    | 0.80 %    | 0.75 %    | 0.55 %    | 0.20 %    | 11.90 %  | 1.55 %   | 0.07 %   | 0.00 %    |
|     14 | 1.20 %    | 0.80 %    | 0.55 %    | 0.50 %    | 0.10 %    | 10.70 %  | 1.05 %   | 0.04 %   | 0.00 %    |
|     12 | 1.15 %    | 0.65 %    | 0.50 %    | 0.20 %    | 0.06 %    | 9.35 %   | 0.75 %   | 0.02 %   | 0.00 %    |
|     10 | 1.10 %    | 0.60 %    | 0.35 %    | 0.20 %    | 0.00 %    | 8.45 %   | 0.50 %   | 0.01 %   | 0.00 %    |

### 结果展示

在结果展示方面，我们面临一个显著的问题：对于某件防具来说，如果它在填充某个怪异炼化词条时有解，那么填充比它更加“上位”的词条时，也一定有解。这一性质将导致搜索结果中，包含大量意义重复的条目。例如，某装备“孔位+1”时有解，那么“孔位+2”和“孔位+3”也一定会出现在搜索结果中，但是它对于玩家的意义并不大，反而会使得搜索结果难以阅读。

为此，对于一套配装，我们定义它的“肝度”为：

$$ \sum_{k \in \textrm{armors}} (\frac{1}{p_k} - 1) $$

其中，$\textrm{armors}$ 代表全身的防具集合 (头、胸、手、腰、腿)，$k$ 代表某件防具，$p_k$ 表示这件防具的“出货”概率。如果某件防具 $k$ 上不带有填充的怪异词条 (例如普通防具，或者用户通过怪异炼化记录导入的已有的带怪异炼化条目的防具)，定义 $p_k = 1$。

“肝度”在物理上可以理解为“为了获得这套配装，怪异炼化需要重试的次数的期望”。

之后，如果两套配装有相同的防具/护石组合，我们令配装器只输出“肝度”最低的配装，就可以解决这一问题了。如果有多套配装“肝度”都最低，则同时展示。

在最终搜索结果中，您也可以按“肝度”排序，选取最容易获得的配装。

### 关于“技能可以追加的等级”功能

这一功能的实现，目前基于搜索结果和一些数学事实以贪心算法得出。

在开启怪异炼化词条生成之后，由于“肝度”过高的配装会被筛除，“技能可以追加的等级”功能的准确度将会大受影响。该功能提示的可以追加的技能仍然可以追加，但是未提示的技能或者等级追加后也可能有解。

这一问题将在后续研究中尝试解决。

### 联系我们

如果对概率表或蒙特卡洛模拟程序有疑问，或者对算法有建议/指导，欢迎您发送邮件至 gamecat@aliyun.com。
