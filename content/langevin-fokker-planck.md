# 从一般 Langevin 方程到 Fokker–Planck 方程

Langevin 方程含有白噪声时，$\dot X=a+b\xi$ 只是形式写法。严格的起点应当是随机微分方程（SDE），并且必须指明随机积分的解释。本文先处理一维 Itô 扩散

$$
\mathrm dX_t=a(X_t,t)\,\mathrm dt+b(X_t,t)\,\mathrm dW_t,
$$

其中 $W_t$ 是标准 Wiener 过程，

$$
\mathbb E[\mathrm dW_t]=0,
\qquad
\mathbb E[(\mathrm dW_t)^2]=\mathrm dt.
$$

形式上可以写成 $\xi(t)=\mathrm dW_t/\mathrm dt$，但白噪声 $\xi$ 是广义随机过程，不能按普通时间函数处理。在系数具有足够正则性、SDE 存在适定解且 $X_t$ 具有概率密度 $p(x,t)$ 的条件下，对应的 Fokker–Planck 方程为

$$
\boxed{
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}\bigl[a(x,t)p(x,t)\bigr]
+\frac12\frac{\partial^2}{\partial x^2}
\bigl[b^2(x,t)p(x,t)\bigr].
}
$$

下面给出两种等价的推导。第一种从 Itô 公式出发；第二种通过短时转移矩和 Kramers–Moyal 展开得到同一结果。

---

## 1. Itô 公式与 Delta 函数表示

### 1.1 概率密度的微观表示

定义单条随机轨道对密度的贡献

$$
\rho(x,t)=\delta(x-X_t).
$$

对所有噪声实现取系综平均，得到

$$
p(x,t)=\mathbb E[\rho(x,t)]
=\mathbb E[\delta(x-X_t)].
$$

### 1.2 对微观密度使用 Itô 公式

由于 $X_t$ 的二次变差不为零，这一步不能使用普通链式法则。将 $\rho(x,t)=\delta(x-X_t)$ 视为 $X_t$ 的函数，形式地应用 Itô 公式，

$$
\begin{aligned}
\mathrm d\rho
&=-\frac{\partial\rho}{\partial x}\,\mathrm dX_t
+\frac12\frac{\partial^2\rho}{\partial x^2}(\mathrm dX_t)^2 \\
&=\left[
-a(X_t,t)\frac{\partial\rho}{\partial x}
+\frac12 b^2(X_t,t)\frac{\partial^2\rho}{\partial x^2}
\right]\mathrm dt
-b(X_t,t)\frac{\partial\rho}{\partial x}\,\mathrm dW_t.
\end{aligned}
$$

这里使用了 Itô 乘法表

$$
(\mathrm dW_t)^2=\mathrm dt,
\qquad
\mathrm dt\,\mathrm dW_t=0,
\qquad
(\mathrm dt)^2=0.
$$

上述 Delta 函数计算应当按分布理解。等价的严格做法是先对任意光滑测试函数 $\varphi(X_t)$ 应用 Itô 公式，再对 $x$ 分部积分。

### 1.3 取平均并进行分部积分

在 Itô 解释下，最后一项是 Itô 随机积分。若相应的可积性条件成立，其期望为零。因此

$$
\frac{\partial p}{\partial t}
=-\mathbb E\!\left[
a(X_t,t)\frac{\partial}{\partial x}\delta(x-X_t)
\right]
+\frac12\mathbb E\!\left[
b^2(X_t,t)\frac{\partial^2}{\partial x^2}\delta(x-X_t)
\right].
$$

利用分布恒等式

$$
\mathbb E\!\left[F(X_t,t)\delta(x-X_t)\right]
=F(x,t)p(x,t),
$$

并将对 $x$ 的导数移到整个乘积上，得到

$$
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}\bigl[a(x,t)p(x,t)\bigr]
+\frac12\frac{\partial^2}{\partial x^2}
\bigl[b^2(x,t)p(x,t)\bigr].
$$

关键的二阶导数来自 Itô 二次变差 $(\mathrm dW_t)^2=\mathrm dt$，而不是普通链式法则之后再额外补入的噪声平均。

---

## 2. Chapman–Kolmogorov 方程与 Kramers–Moyal 展开

### 2.1 短时增量

在条件 $X_t=x$ 下，小时间步 $\Delta t$ 内的 Itô 增量为

$$
\Delta X
=a(x,t)\Delta t+b(x,t)\Delta W+o_{\mathrm p}(\sqrt{\Delta t}),
$$

其中 $\Delta W\sim\mathcal N(0,\Delta t)$。在 $b(x,t)\neq0$ 的非退化点，短时转移核在领头阶上是高斯的：

$$
P(x',t+\Delta t\mid x,t)
\simeq
\frac{1}{\sqrt{2\pi b^2(x,t)\Delta t}}
\exp\!\left[
-\frac{[x'-x-a(x,t)\Delta t]^2}
{2b^2(x,t)\Delta t}
\right].
$$

当 $a$ 或 $b$ 依赖于状态时，这只是冻结短时系数得到的渐近转移核，不是有限 $\Delta t$ 下的精确解。

### 2.2 条件矩与 Kramers–Moyal 系数

定义

$$
D^{(n)}(x,t)
=\frac{1}{n!}\lim_{\Delta t\to0}
\frac{\mathbb E[(\Delta X)^n\mid X_t=x]}{\Delta t}.
$$

利用 $\mathbb E[\Delta W]=0$ 和 $\mathbb E[(\Delta W)^2]=\Delta t$，可得

$$
D^{(1)}(x,t)=a(x,t),
\qquad
D^{(2)}(x,t)=\frac12 b^2(x,t).
$$

对 $n\geq3$，高阶条件矩本身在有限 $\Delta t$ 下并非都等于零；正确的说法是

$$
\mathbb E[(\Delta X)^n\mid X_t=x]=o(\Delta t),
$$

因而它们对应的 Kramers–Moyal 系数 $D^{(n)}$ 为零。

### 2.3 概率密度的演化

Chapman–Kolmogorov 方程给出

$$
p(x',t+\Delta t)
=\int_{-\infty}^{\infty}
P(x',t+\Delta t\mid x,t)p(x,t)\,\mathrm dx.
$$

将短时转移矩代入 Kramers–Moyal 展开，

$$
\frac{\partial p}{\partial t}
=\sum_{n=1}^{\infty}
\left(-\frac{\partial}{\partial x}\right)^n
\bigl[D^{(n)}(x,t)p(x,t)\bigr].
$$

对连续高斯扩散，只有 $D^{(1)}$ 和 $D^{(2)}$ 存活，所以

$$
\boxed{
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}\bigl[a(x,t)p(x,t)\bigr]
+\frac12\frac{\partial^2}{\partial x^2}
\bigl[b^2(x,t)p(x,t)\bigr].
}
$$

---

## 3. Itô 与 Stratonovich 解释

对加性噪声（$b$ 与 $x$ 无关），Itô 与 Stratonovich 解释给出相同的 Fokker–Planck 方程。对乘性噪声，两者的漂移项不同。若 Langevin 方程以 Stratonovich 形式给出，

$$
\mathrm dX_t
=a_{\mathrm S}(X_t,t)\,\mathrm dt
+b(X_t,t)\circ\mathrm dW_t,
$$

则等价的 Itô 漂移为

$$
a_{\mathrm I}(x,t)
=a_{\mathrm S}(x,t)
+\frac12 b(x,t)\frac{\partial b(x,t)}{\partial x}.
$$

因此对应的 Fokker–Planck 方程是

$$
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}
\left[\left(a_{\mathrm S}
+\frac12 b\,\partial_x b\right)p\right]
+\frac12\frac{\partial^2}{\partial x^2}(b^2p).
$$

它也可以写成

$$
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}(a_{\mathrm S}p)
+\frac12\frac{\partial}{\partial x}
\left[b\frac{\partial}{\partial x}(bp)\right].
$$

因此，只写 $\dot X=a+b\xi$ 而不指定随机积分解释，并不足以唯一确定乘性噪声下的 Fokker–Planck 方程。

---

## 4. 概率流、边界条件与归一化

定义 Itô 扩散的概率流

$$
J(x,t)
=a(x,t)p(x,t)
-\frac12\frac{\partial}{\partial x}
\bigl[b^2(x,t)p(x,t)\bigr],
$$

则 Fokker–Planck 方程具有连续性方程的形式

$$
\frac{\partial p}{\partial t}=-\frac{\partial J}{\partial x}.
$$

在无穷区间上，若 $J(\pm\infty,t)=0$；或在有限区间上采用无流边界条件，则

$$
\frac{\mathrm d}{\mathrm dt}
\int p(x,t)\,\mathrm dx=0,
$$

所以概率归一化得以保持。吸收边界则允许概率通过边界流出所考察的状态区域。

---

## 5. 两个极限检验

- 当 $b=0$ 时，方程化为

  $$
  \frac{\partial p}{\partial t}
  =-\frac{\partial}{\partial x}(ap),
  $$

  即确定性动力学 $\dot X=a(X,t)$ 对应的 Liouville 连续性方程。

- 当 $a=0$ 且 $b=\sqrt{2D}$ 为常数时，方程化为

  $$
  \frac{\partial p}{\partial t}
  =D\frac{\partial^2p}{\partial x^2},
  $$

  即普通扩散方程。这一极限也检验了二阶项中的因子 $1/2$。

---

## 6. 多维推广

对 $d$ 维 Itô 扩散（$i,j=1,\ldots,d$）

$$
\mathrm dX_i
=a_i(\boldsymbol X,t)\,\mathrm dt
+\sum_{\alpha=1}^{m}
B_{i\alpha}(\boldsymbol X,t)\,\mathrm dW_\alpha,
$$

其中

$$
\mathbb E[\mathrm dW_\alpha\,\mathrm dW_\beta]
=\delta_{\alpha\beta}\,\mathrm dt,
$$

定义扩散矩阵

$$
D_{ij}(\boldsymbol x,t)
=\sum_{\alpha=1}^{m}
B_{i\alpha}(\boldsymbol x,t)B_{j\alpha}(\boldsymbol x,t).
$$

则 Fokker–Planck 方程为

$$
\boxed{
\frac{\partial p}{\partial t}
=-\sum_i\frac{\partial}{\partial x_i}(a_i p)
+\frac12\sum_{i,j}
\frac{\partial^2}{\partial x_i\partial x_j}(D_{ij}p).
}
$$

这是有限维连续 Itô 扩散的一般形式，但仍不是所有随机动力学的“最一般”形式。含跳跃的 Markov 过程需要主方程中的非局域转移项；有色噪声通常需要扩大状态空间或采用近似闭合；非 Markov 过程也不一定满足局域的 Fokker–Planck 方程。

---

## 7. 结论与适用范围

从一维 Itô SDE

$$
\mathrm dX_t=a(X_t,t)\,\mathrm dt+b(X_t,t)\,\mathrm dW_t
$$

出发，可以通过 Itô 公式或 Kramers–Moyal 展开得到

$$
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}(ap)
+\frac12\frac{\partial^2}{\partial x^2}(b^2p).
$$

这一结论依赖于三个关键前提：过程是 Markov 的连续扩散；噪声是 Wiener 白噪声；已明确指定 Itô 或与之等价的随机积分解释。对乘性噪声，改变随机积分解释会改变有效漂移，不能省略这一约定。
