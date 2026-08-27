# Martin–Siggia–Rose formalism

本文从一般 Langevin 方程出发，将噪声平均改写为关于原变量和响应场的函数积分。推导依次使用运动方程的泛函数 Delta 约束、Delta 泛函数的 Fourier 表示以及高斯噪声积分，得到 Martin–Siggia–Rose/Janssen–De Dominicis（MSRJD）动作量。文末用 Ornstein–Uhlenbeck 过程显式计算生成泛函数、二点相关函数和线性响应函数。

> **转写与修正约定。** 原 PDF 共 3 页，其中第 1 页为空白页，手写推导位于第 2–3 页。本文保留原稿的实响应变量 $\widetilde x$ 和显式因子 $\ii$，并统一使用 $D$ 表示白噪声强度。原稿省略的泛函数 Jacobian、边界条件和随机积分解释在正文中补全。本文默认采用 Itô 离散化；乘性噪声的其他离散化需要另行处理漂移和 Jacobian。文中的泛函数积分均按标准形式意义理解，归一化常数与必要的积分路径变形默认包含在测度中。

## 问题与约定

先考虑一个实随机变量 $x(t)$，其动力学为

$$
  \dot x(t)=F[x;t]+\eta(t).
$$
<p class="equation-number" id="equation-eq:langevin-additive">(1)</p>

这里 $F[x;t]$ 可以是 $x(t)$ 的非线性函数。噪声取零均值高斯过程，

$$
  \avg{\eta(t)}=0,
  \qquad
  \avg{\eta(t)\eta(t')}=G(t,t').
$$
<p class="equation-number" id="equation-eq:noise-covariance">(2)</p>

假设核 $G$ 可逆，噪声的泛函数概率测度可写成

$$
  \mathcal P[\eta]
  =\frac{1}{\mathcal N_\eta}
   \exp\!\left[
   -\frac12\int\dd t\,\dd t'\,
   \eta(t)G^{-1}(t,t')\eta(t')
   \right].
$$
<p class="equation-number" id="equation-eq:noise-measure">(3)</p>

其中 $G^{-1}$ 满足

$$
  \int\dd s\,G(t,s)G^{-1}(s,t')=\delta(t-t').
$$
<p class="equation-number">(4)</p>

我们的目标是计算轨道可观测量 $\mathcal O[x]$ 的噪声平均，

$$
  \avg{\mathcal O[x]}_\eta
  =\int\D\eta\,\mathcal P[\eta]\,\mathcal O[x_\eta],
$$
<p class="equation-number" id="equation-eq:observable-noise-average">(5)</p>

其中 $x_\eta$ 是给定噪声实现下式 [(1)](#equation-eq:langevin-additive) 的解。MSR 形式主义的核心是把对 $\eta$ 的平均改写为对动力学轨道 $x$ 的路径积分。

## 从噪声平均到 MSRJD 动作量

### 运动方程作为泛函数约束

定义运动方程算子

$$
  \E[x](t)\equiv \dot x(t)-F[x;t].
$$
<p class="equation-number">(6)</p>

在给定初始条件且解唯一时，可插入泛函数恒等式

$$
  1=\int\D x\;\Jdet[x]\,
  \delta\!\left[\E[x]-\eta\right],
$$
<p class="equation-number" id="equation-eq:delta-identity">(7)</p>

其中

$$
  \Jdet[x]
  =\left|\det\!\left[
    \frac{\delta \E[x](t)}{\delta x(t')}
  \right]\right|
  =\left|\det\!\left[
    \partial_t\delta(t-t')
    -\frac{\delta F[x;t]}{\delta x(t')}
  \right]\right|
$$
<p class="equation-number" id="equation-eq:jacobian">(8)</p>

是映射 $x\mapsto\eta=\E[x]$ 的泛函数 Jacobian。这个因子在手写稿中被省略，但一般情况下不能在写出离散化之前直接丢弃。

### 引入响应场

用 Fourier 表示泛函数 Delta 约束，

$$
  \delta[A]
  =\mathcal N_\delta
   \int\D\widetilde x\,
   \exp\!\left[-\ii\int\dd t\,
   \widetilde x(t)A(t)\right].
$$
<p class="equation-number" id="equation-eq:delta-fourier">(9)</p>

$\widetilde x(t)$ 称为响应场或辅助场。将式 [(7)](#equation-eq:delta-identity) 和 [(9)](#equation-eq:delta-fourier) 代入式 [(5)](#equation-eq:observable-noise-average)，得

$$
\begin{aligned}
  \avg{\mathcal O[x]}_\eta
  ={}&\mathcal N
  \int\D x\,\D\widetilde x\,\D\eta\;
  \Jdet[x]\,\mathcal O[x]
  \exp\!\left[-\frac12\eta G^{-1}\eta\right]
  \\
  &\times
  \exp\!\left[
  -\ii\int\dd t\,\widetilde x(t)
  \bigl(\E[x](t)-\eta(t)\bigr)
  \right].
\end{aligned}
$$
<p class="equation-number" id="equation-eq:before-noise-integration">(10)</p>

在上式中使用了紧凑记号

$$
  \eta G^{-1}\eta
  \equiv\int\dd t\,\dd t'\,
  \eta(t)G^{-1}(t,t')\eta(t').
$$

### 积掉高斯噪声

对 $\eta$ 配方，或直接使用高斯泛函数积分恒等式，

$$
  \int\D\eta\,
  \exp\!\left[
  -\frac12\eta G^{-1}\eta
  +\ii\widetilde x\eta
  \right]
  =\mathcal N_G
  \exp\!\left[-\frac12\widetilde xG\widetilde x\right],
$$
<p class="equation-number" id="equation-eq:gaussian-noise-integration">(11)</p>

其中

$$
  \widetilde xG\widetilde x
  \equiv\int\dd t\,\dd t'\,
  \widetilde x(t)G(t,t')\widetilde x(t').
$$

因此

$$
  \boxed{
  \avg{\mathcal O[x]}_\eta
  =\mathcal N
  \int\D x\,\D\widetilde x\;
  \mathcal O[x]\,\ee^{-S[x,\widetilde x]}
  }
$$
<p class="equation-number" id="equation-eq:msr-average">(12)</p>

其中 MSRJD 动作量为

$$
  \boxed{
  S[x,\widetilde x]
  =\ii\int\dd t\,\widetilde x(t)
  \bigl[\dot x(t)-F[x;t]\bigr]
  +\frac12\int\dd t\,\dd t'\,
  \widetilde x(t)G(t,t')\widetilde x(t')
  -\ln\Jdet[x].
  }
$$
<p class="equation-number" id="equation-eq:general-msr-action">(13)</p>

> 动作量第一项强制原变量满足确定性运动算子；第二项记录噪声协方差；第三项来自变量替换。对因果的 Itô 前点离散化，$\Jdet$ 是与场无关的上/下三角行列式，可吸收进归一化常数。若使用 Stratonovich 或其他离散化，这个结论一般不再自动成立。

## 白噪声与乘性噪声

### 加性高斯白噪声

对白噪声

$$
  \avg{\eta(t)\eta(t')}=2D\,\delta(t-t'),
  \qquad D>0,
$$
<p class="equation-number" id="equation-eq:white-noise">(14)</p>

有 $G(t,t')=2D\delta(t-t')$。在 Itô 离散化下吸收常数 Jacobian 后，式 [(13)](#equation-eq:general-msr-action) 化为

$$
  \boxed{
  S[x,\widetilde x]
  =\int\dd t\,
  \left\{
  \ii\widetilde x(t)\bigl[\dot x(t)-F[x;t]\bigr]
  +D\widetilde x^2(t)
  \right\}.
  }
$$
<p class="equation-number" id="equation-eq:additive-white-action">(15)</p>

### Itô 乘性高斯白噪声

原手写稿还考虑了

$$
  \dot x(t)=F[x(t)]+H[x(t)]\eta(t),
  \qquad
  \avg{\eta(t)\eta(t')}=2D\delta(t-t').
$$
<p class="equation-number" id="equation-eq:multiplicative-langevin">(16)</p>

在 Itô 前点离散化下，高斯平均中的源变为 $H(x)\widetilde x$，因此

$$
  \boxed{
  S_{\mathrm{It\hat{o}}}[x,\widetilde x]
  =\int\dd t\,
  \left\{
  \ii\widetilde x(t)\bigl[\dot x(t)-F(x(t))\bigr]
  +D H^2(x(t))\widetilde x^2(t)
  \right\}.
  }
$$
<p class="equation-number" id="equation-eq:multiplicative-action">(17)</p>

这就是手写稿第 2 页给出的特殊形式。式 [(17)](#equation-eq:multiplicative-action) 不能在不加修改的情况下解释为 Stratonovich 结果：后者需要同时跟踪等价的 Itô 漂移修正与离散化相关的 Jacobian。

### 时空相关的噪声场

若噪声本身是高斯随机场 $\eta(\bm r,t)$，其协方差为

$$
  \avg{\eta(\bm r,t)\eta(\bm r',t')}
  =G(\bm r,t;\bm r',t'),
$$
<p class="equation-number">(18)</p>

而动力学沿轨道取样 $\eta(x(t),t)$，则积掉噪声后出现

$$
  \frac12\int\dd t\,\dd t'\,
  \widetilde x(t)
  G\bigl(x(t),t;x(t'),t'\bigr)
  \widetilde x(t').
$$
<p class="equation-number" id="equation-eq:trajectory-noise-kernel">(19)</p>

这是原稿首个动作量公式中噪声项的含义；完整动作量仍需包含运动方程约束和相应的 Jacobian。由于协方差核沿未知轨道取值，式 [(19)](#equation-eq:trajectory-noise-kernel) 一般会产生非局域且非线性的动作量。

## 生成泛函数、相关函数与响应

引入与 $x$ 和 $\ii\widetilde x$ 耦合的源 $J$ 与 $\widetilde J$，

$$
  Z[J,\widetilde J]
  =\int\D x\,\D\widetilde x\,
  \exp\!\left[
  -S[x,\widetilde x]
  +\int\dd t\,
  \bigl(Jx+\widetilde J\,\ii\widetilde x\bigr)
  \right].
$$
<p class="equation-number" id="equation-eq:generating-functional">(20)</p>

并选择归一化 $Z[0,0]=1$。例如，

$$
\begin{aligned}
  \avg{x(t_1)x(t_2)}
  &=\left.
    \frac{\delta^2 Z}{\delta J(t_1)\delta J(t_2)}
    \right|_{J=\widetilde J=0},
  \\
  \avg{x(t)\,\ii\widetilde x(t')}
  &=\left.
    \frac{\delta^2 Z}{\delta J(t)\delta\widetilde J(t')}
    \right|_{J=\widetilde J=0}.
\end{aligned}
$$
<p class="equation-number">(21)</p>

若在 Langevin 方程中加入外力 $h(t)$，

$$
  \dot x=F[x;t]+h(t)+\eta(t),
$$
<p class="equation-number">(22)</p>

则动作量增加 $-\ii\int\dd t\,\widetilde xh$。因此线性响应函数为

$$
  R(t,t')
  \equiv\left.
  \frac{\delta\avg{x(t)}}{\delta h(t')}
  \right|_{h=0}
  =\avg{x(t)\,\ii\widetilde x(t')}.
$$
<p class="equation-number" id="equation-eq:response-field-meaning">(23)</p>

这说明辅助场并非另一个独立的物理自由度；它生成了系统对外部扰动的因果响应。

## Ornstein–Uhlenbeck 过程

### 模型与动作量

考虑原稿中的 Ornstein–Uhlenbeck（OU）过程

$$
  \dot x(t)=-\alpha x(t)+\eta(t),
  \qquad
  \alpha>0,
  \qquad
  \avg{\eta(t)\eta(t')}=2D\delta(t-t').
$$
<p class="equation-number" id="equation-eq:ou-process">(24)</p>

取稳态极限，即把初始时刻送到 $-\infty$。对应的自由 MSRJD 动作量为

$$
  S_0[x,\widetilde x]
  =\int_{-\infty}^{\infty}\dd t\,
  \left[
  \ii\widetilde x(t)(\partial_t+\alpha)x(t)
  +D\widetilde x^2(t)
  \right].
$$
<p class="equation-number" id="equation-eq:ou-action">(25)</p>

### 积掉 x 并解响应场约束

只引入与 $x$ 耦合的源 $J$，

$$
  Z[J]
  =\mathcal N\int\D x\,\D\widetilde x\,
  \exp\!\left[-S_0[x,\widetilde x]
  +\int\dd t\,J(t)x(t)\right].
$$
<p class="equation-number" id="equation-eq:ou-generating-functional">(26)</p>

对含 $\partial_t x$ 的项分部积分，并假设时间边界项消失，得到所有与 $x$ 相关的项

$$
  \int\dd t\,x(t)
  \left[
  \ii(\partial_t-\alpha)\widetilde x(t)+J(t)
  \right].
$$
<p class="equation-number">(27)</p>

因此对 $x$ 的泛函数积分产生 Delta 泛函数

$$
  \delta\!\left[
  \ii(\partial_t-\alpha)\widetilde x+J
  \right].
$$
<p class="equation-number" id="equation-eq:ou-response-delta">(28)</p>

选择与因果问题对应的终端条件 $\widetilde x(+\infty)=0$，约束方程的解为

$$
  \boxed{
  \widetilde x_J(t)
  =-\ii\int_t^\infty\dd s\,
  \ee^{-\alpha(s-t)}J(s).
  }
$$
<p class="equation-number" id="equation-eq:ou-response-field-solution">(29)</p>

这一“向后积分”不表示物理响应是超前的；它来自对原变量 $x$ 积分后得到的共轭算子 $(-\partial_t+\alpha)$。物理响应仍由退迟 Green 函数给出。

### 计算高斯核

将式 [(29)](#equation-eq:ou-response-field-solution) 代入式 [(26)](#equation-eq:ou-generating-functional)中的二次项，

$$
\begin{aligned}
  \int\dd t\,\widetilde x_J^2(t)
  ={}&-\int\dd s_1\,\dd s_2\,
  J(s_1)J(s_2)
  \int_{-\infty}^{\min(s_1,s_2)}\dd t
  \\
  &\hspace{3.3cm}\times
  \ee^{-\alpha(s_1-t)}
  \ee^{-\alpha(s_2-t)}.
\end{aligned}
$$
<p class="equation-number" id="equation-eq:ou-kernel-before-integral">(30)</p>

时间积分为

$$
  \int_{-\infty}^{\min(s_1,s_2)}\dd t\,
  \ee^{-\alpha(s_1+s_2-2t)}
  =\frac{1}{2\alpha}
  \ee^{-\alpha|s_1-s_2|}.
$$
<p class="equation-number" id="equation-eq:ou-kernel-identity">(31)</p>

从而得到归一化生成泛函数

$$
  \boxed{
  Z[J]
  =\exp\!\left[
  \frac{D}{2\alpha}
  \int\dd s_1\,\dd s_2\,
  J(s_1)\ee^{-\alpha|s_1-s_2|}J(s_2)
  \right].
  }
$$
<p class="equation-number" id="equation-eq:ou-final-generating-functional">(32)</p>

### 相关函数和响应函数

将式 [(32)](#equation-eq:ou-final-generating-functional) 与标准高斯形式

$$
  Z[J]=\exp\!\left[
  \frac12\int\dd t\,\dd t'\,
  J(t)C(t,t')J(t')
  \right]
$$

比较，读出

$$
  \boxed{
  C(t,t')=\avg{x(t)x(t')}
  =\frac{D}{\alpha}\,
  \ee^{-\alpha|t-t'|}.
  }
$$
<p class="equation-number" id="equation-eq:ou-correlation">(33)</p>

特别地，稳态方差为 $\avg{x^2}=D/\alpha$。直接对带外力的 OU 方程求解，或者求自由响应传播子，可得

$$
  \boxed{
  R(t,t')
  =\avg{x(t)\,\ii\widetilde x(t')}
  =\Theta(t-t')\,
  \ee^{-\alpha(t-t')}.
  }
$$
<p class="equation-number" id="equation-eq:ou-response">(34)</p>

式 [(34)](#equation-eq:ou-response) 在 $t<t'$ 时为零，明确表明物理响应具有因果性。

## 两个一致性检验

### 积掉响应场

对加性白噪声，从式 [(15)](#equation-eq:additive-white-action) 积掉 $\widetilde x$ 可得形式上的 Onsager–Machlup 权重

$$
  \int\D\widetilde x\,
  \ee^{-S[x,\widetilde x]}
  \propto
  \exp\!\left[
  -\frac{1}{4D}
  \int\dd t\,
  \bigl(\dot x-F[x;t]\bigr)^2
  \right],
$$
<p class="equation-number" id="equation-eq:onsager-machlup-check">(35)</p>

其中仍要保留与离散化相容的 Jacobian 和初始分布。这一结果反映了噪声实现 $\eta=\dot x-F$ 的高斯概率权重。

### OU 结果的直接检验

OU 方程的稳态解可直接写成

$$
  x(t)=\int_{-\infty}^{t}\dd s\,
  \ee^{-\alpha(t-s)}\eta(s).
$$
<p class="equation-number">(36)</p>

使用噪声协方差式 [(24)](#equation-eq:ou-process)，立即得到

$$
  \avg{x(t)x(t')}
  =2D\int_{-\infty}^{\min(t,t')}\dd s\,
  \ee^{-\alpha(t-s)}\ee^{-\alpha(t'-s)}
  =\frac{D}{\alpha}\ee^{-\alpha|t-t'|},
$$
<p class="equation-number">(37)</p>

与 MSRJD 生成泛函数给出的式 [(33)](#equation-eq:ou-correlation) 完全相同。

## 多分量和场论形式

对多分量场 $\phi_a(\bm r,t)$，设动力学方程为

$$
  \partial_t\phi_a(\bm r,t)
  =F_a[\phi;\bm r,t]+\eta_a(\bm r,t),
$$
<p class="equation-number">(38)</p>

噪声协方差为

$$
  \avg{\eta_a(\bm r,t)\eta_b(\bm r',t')}
  =G_{ab}(\bm r,t;\bm r',t').
$$
<p class="equation-number">(39)</p>

在 Itô 离散化下省略场无关 Jacobian 后，MSRJD 动作量为

$$
\begin{aligned}
  S[\phi,\widetilde\phi]
  ={}&\ii\sum_a\int\dd t\,\dd^d r\,
  \widetilde\phi_a
  \bigl(\partial_t\phi_a-F_a[\phi]\bigr)
  \\
  &+\frac12\sum_{a,b}
  \int\dd t\,\dd t'\,\dd^d r\,\dd^d r'\,
  \widetilde\phi_a(\bm r,t)
  G_{ab}(\bm r,t;\bm r',t')
  \widetilde\phi_b(\bm r',t').
\end{aligned}
$$
<p class="equation-number" id="equation-eq:field-msr-action">(40)</p>

非线性动力学 $F_a[\phi]$ 在式 [(40)](#equation-eq:field-msr-action) 中产生响应场与原场的相互作用顶角，从而可以使用场论的图形展开和重整化群方法研究非线性随机动力学。

## 结论

MSRJD 推导的逻辑链可概括为

$$
\text{Langevin SDE}
\longrightarrow
\delta[\E[x]-\eta]
\longrightarrow
\widetilde x
\longrightarrow
\text{Gaussian average}
\longrightarrow
S_{\mathrm{MSRJD}}.
$$

这个变换没有消除随机性，而是将噪声统计编码进响应场的二次项中。原场的关联函数和系统的因果响应因此可以在同一个生成泛函数中计算。在应用到乘性噪声时，必须同时指明随机积分解释并处理相应 Jacobian；这是从形式推导走向可计算场论时不能省略的条件。

## 参考文献

1. P. C. Martin, E. D. Siggia, and H. A. Rose,
“Statistical Dynamics of Classical Systems,” *Physical Review A* **8**, 423–437 (1973), [doi:10.1103/PhysRevA.8.423](https://doi.org/10.1103/PhysRevA.8.423).

1. H.-K. Janssen,
“On a Lagrangean for Classical Field Dynamics and Renormalization Group Calculations of Dynamical Critical Properties,” *Zeitschrift für Physik B* **23**, 377–380 (1976), [doi:10.1007/BF01316547](https://doi.org/10.1007/BF01316547).

1. C. De Dominicis,
“Techniques de renormalisation de la théorie des champs et dynamique des phénomènes critiques,” *Journal de Physique Colloques* **37**, C1-247–C1-253 (1976), [doi:10.1051/jphyscol:1976138](https://doi.org/10.1051/jphyscol:1976138).
