# 统计计算 R 脚本索引

这组脚本来自原桌面目录“学习笔记临时/统计计算”，现按原课程章节保存在仓库中，并与[统计计算总复习](../../stat-computing-review.md)建立对应关系。

导入时保留了 `.R`、`.csv` 和 `.txt` 源文件；`.RData`、`.Rhistory`、课程 PDF、截图及运行生成的图像没有纳入版本控制。两处本机绝对路径也已移除。

## 章节对应

| 课程代码 | 总复习位置 | 主要内容 | 代表脚本 |
|---|---|---|---|
| Ch1 | §1 | R 数据结构、文件读写、绘图与基础统计 | [R 基础总例](Ch1_R语言基础/Ch11_Basics/Ch11_Basics.r) |
| Ch2 | §2-§4 | 均匀随机数、逆变换、接受-拒绝、变换法、混合分布与多元正态 | [逆变换](ch2/Ch22_IT.r)、[接受-拒绝](ch2/Ch23_AR.r)、[多元正态](ch2/Ch25_MNorm.r) |
| Ch3 | §5-§6 | Monte Carlo 积分、对偶变量、控制变量、重要抽样与分层抽样 | [估计 $\pi$](<Ch3 蒙特卡罗积分和方差缩减/Ch31_pi.r>)、[MC 积分](<Ch3 蒙特卡罗积分和方差缩减/Ch32_MCint.r>)、[方差缩减](<Ch3 蒙特卡罗积分和方差缩减/Ch33_VR.r>) |
| Ch4 | §7 | MSE、置信区间覆盖率、第一类错误率与检验功效模拟 | [估计量模拟](Ch4_Monte-Carlo/Ch41_Est.r)、[置信区间](Ch4_Monte-Carlo/Ch42_CI.r)、[检验模拟](Ch4_Monte-Carlo/Ch43_Test.r) |
| Ch5 | §8 | Bootstrap、Jackknife 与多种 Bootstrap 置信区间 | [Bootstrap](Ch5/Ch51_Bootstrap.r)、[Jackknife](Ch5/Ch52_Jackknife.r)、[Bootstrap CI](Ch5/Ch53_BCI.r) |
| Ch6 | §9 | 二分法、Newton 法、数值优化与极大似然估计 | [数值求根](<Ch6 R中的数值方法/Ch61_Root.r>)、[MLE](<Ch6 R中的数值方法/Ch62_MLE.r>)、[Cauchy MLE](<Ch6 R中的数值方法/Ch6newton4CauchyMLE.R>) |
| Ch7 | §10 | Metropolis-Hastings、随机游走 Metropolis 与独立 MH | [一般 MH](<Ch7 马尔科夫链蒙特卡罗方法/Ch71_MH.r>)、[Metropolis](<Ch7 马尔科夫链蒙特卡罗方法/Ch72_Metropolis.r>)、[独立 MH](<Ch7 马尔科夫链蒙特卡罗方法/Ch73_Independence.r>) |

## 综合脚本

- [`stats_review.R`](stats_review.R)：按课程顺序汇集主要算法的复习草稿，适合与总复习文档对照阅读；它包含多个相互独立的代码段，不应假定整文件一次运行。
- [`Stats_Compute.R`](Stats_Compute.R)：Cauchy 位置参数的 Newton 估计，以及 Bootstrap、Jackknife 误差估计。
- [`T6.R`](T6.R)：数值方法补充练习。

## 运行方式

代码主要采用 base R，部分例子需要额外软件包：

```r
install.packages(c(
  "VGAM", "bootstrap", "boot", "Hmisc", "nortest", "energy",
  "MASS", "mvtnorm", "vcd", "survival", "aplpack",
  "factoextra", "ggplot2", "igraph"
))
```

含相对数据文件的示例应从脚本所在目录运行。例如：

```bash
cd docs/computation/code/stat-computing/Ch1_R语言基础/Ch11_Basics/Ex_read
Rscript main.r
```

许多课程脚本会绘图、打开图形设备或打印中间结果，定位更接近“可交互实验”而非无输出的自动化程序。建议先单独运行表格中的代表脚本，再阅读同章的练习文件。

## 已知边界

- 原始脚本保留了课程学习过程中的命名和写法，没有做大规模风格重构。
- `stats_review.R` 中若干段落复用同名变量或函数，按章节分段运行更安全。
- 当前环境未安装 R，因此本次只完成静态路径、文件依赖和敏感信息检查；尚未声明所有脚本都能无警告运行。
