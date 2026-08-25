# 静态与动态结构因子 $S(k)$

结构因子描述密度涨落在波数空间中的分布。小波数对应大尺度结构，因此 $S(k\to0)$ 常用于判断体系是普通涨落、超均匀，还是具有巨数涨落。本文固定 Fourier 约定，推导 $S(k)$ 与实空间关联函数、窗口内粒子数涨落和动态结构因子之间的关系，并给出周期性模拟中的计算方法。

## 1. 定义与 Fourier 约定

考虑 $d$ 维周期性立方盒，体积为 $V=L^d$，其中有 $N$ 个点粒子，平均数密度为

$$
\rho_0=\frac{N}{V}.
$$

微观密度场定义为

$$
\rho(\mathbf r)=\sum_{j=1}^{N}\delta(\mathbf r-\mathbf r_j).
$$

采用 Fourier 约定

$$
\rho_{\mathbf k}
=\int_V d^d r\,\rho(\mathbf r)e^{-i\mathbf k\cdot\mathbf r}
=\sum_{j=1}^{N}e^{-i\mathbf k\cdot\mathbf r_j},
$$

$$
\rho(\mathbf r)=\frac{1}{V}\sum_{\mathbf k}
\rho_{\mathbf k}e^{i\mathbf k\cdot\mathbf r},
\qquad
\mathbf k=\frac{2\pi}{L}(n_1,\ldots,n_d),
$$

其中 $n_a\in\mathbb Z$。由于 $\rho(\mathbf r)$ 为实场，$\rho_{-\mathbf k}=\rho_{\mathbf k}^{*}$。

令

$$
\delta\rho_{\mathbf k}
=\rho_{\mathbf k}-\langle\rho_{\mathbf k}\rangle.
$$

静态结构因子定义为

$$
S(\mathbf k)
=\frac{1}{N}
\left\langle
\delta\rho_{\mathbf k}\delta\rho_{-\mathbf k}
\right\rangle.
$$

对于平移不变的均匀体系，任意非零允许波矢均满足 $\langle\rho_{\mathbf k}\rangle=0$，因此

$$
\begin{aligned}
S(\mathbf k)
&=\frac{1}{N}\left\langle|\rho_{\mathbf k}|^2\right\rangle\\
&=1+\frac{1}{N}
\left\langle
\sum_{i\ne j}
e^{-i\mathbf k\cdot(\mathbf r_i-\mathbf r_j)}
\right\rangle,
\qquad \mathbf k\ne0.
\end{aligned}
$$

在固定粒子数的系综中，$\delta\rho_{\mathbf0}=0$，所以 $S(\mathbf0)=0$ 是粒子数约束导致的平凡结果。讨论 $k\to0$ 时，应使用一系列非零允许波矢，而不是把零模当作小波数数据点。

若体系各向同性，可对模长相近的波矢作壳平均并记为 $S(k)$，其中 $k=|\mathbf k|$。各向异性体系则应保留完整的 $S(\mathbf k)$。

## 2. 与实空间密度关联函数的关系

定义连通密度关联函数

$$
C(\mathbf r)
=\left\langle
\delta\rho(\mathbf0)\delta\rho(\mathbf r)
\right\rangle,
\qquad
\delta\rho(\mathbf r)=\rho(\mathbf r)-\rho_0.
$$

利用平移不变性，对非零波矢有

$$
\begin{aligned}
S(\mathbf k)
&=\frac{1}{N}
\int_V d^d r\,d^d r'\,
e^{-i\mathbf k\cdot(\mathbf r-\mathbf r')}
\left\langle
\delta\rho(\mathbf r)\delta\rho(\mathbf r')
\right\rangle\\
&=\frac{V}{N}
\int d^d r\,e^{-i\mathbf k\cdot\mathbf r}C(\mathbf r)\\
&=\frac{1}{\rho_0}\widetilde C(\mathbf k).
\end{aligned}
$$

若以径向分布函数 $g_2(\mathbf r)$ 表示二体关联，并定义总关联函数 $h(\mathbf r)=g_2(\mathbf r)-1$，则

$$
C(\mathbf r)
=\rho_0\delta(\mathbf r)+\rho_0^2h(\mathbf r),
$$

从而

$$
S(\mathbf k)=1+\rho_0\widetilde h(\mathbf k).
$$

自关联产生常数项 $1$；粒子间关联决定 $S(\mathbf k)$ 相对于泊松分布的偏离。理想泊松点过程满足 $h(\mathbf r)=0$，所以

$$
S(\mathbf k)=1.
$$

### 2.1 两个常见的 Fourier 渐近例子

若关联函数具有不可积的长程幂律尾部

$$
C(r)\sim r^{-\gamma},
\qquad 0<\gamma<d,
$$

则其小波数非解析部分满足

$$
S(k)\sim k^{\gamma-d}.
$$

由于 $\gamma-d<0$，这种长程正关联对应小波数发散，而不是超均匀性。

作为短程关联的简单例子，若某一关联贡献按 $e^{-r/\xi}$ 衰减，则

$$
\int d^d r\,e^{-i\mathbf k\cdot\mathbf r}e^{-r/\xi}
\propto
\xi^d\left[1+(k\xi)^2\right]^{-(d+1)/2}.
$$

因此它在 $k\xi\ll1$ 时是解析的，首个修正为 $O(k^2)$；在 $k\xi\gg1$ 时按 $k^{-(d+1)}$ 衰减。这里讨论的是单个指数关联贡献，完整结构因子还可能包含自关联和其他关联项。

## 3. 超均匀、普通涨落与巨数涨落

若非零波矢的结构因子满足

$$
S(k)\sim A k^{\alpha},
\qquad k\to0,
$$

则可按指数 $\alpha$ 区分三种大尺度行为：

- $\alpha>0$：$S(k\to0)=0$，体系是超均匀的；
- $\alpha=0$：$S(k\to0)$ 趋于非零常数，对应普通体积标度涨落；
- $-d<\alpha<0$：$S(k\to0)$ 发散，对应巨数涨落。

超均匀性要求长波密度涨落被抑制。由

$$
S(\mathbf0)=1+\rho_0\int d^d r\,h(\mathbf r)
$$

可见，在热力学极限下，超均匀点过程满足总和规则

$$
\rho_0\int d^d r\,h(\mathbf r)=-1.
$$

这个负的积分表示粒子间反关联恰好抵消自关联在零波数处的贡献。由 $S(k)\sim k^{\alpha}$ 直接推断 $h(r)$ 的尾部需要额外正则性条件；不能对任意 $\alpha$ 无条件写成同一个实空间幂律。

## 4. 窗口内粒子数涨落

设 $w_R(\mathbf r)$ 是尺度为 $R$ 的观察窗口指标函数：窗口内取 $1$，窗口外取 $0$。窗口内粒子数为

$$
N_R=\int d^d r\,w_R(\mathbf r)\rho(\mathbf r).
$$

定义窗口重叠核

$$
\alpha_R(\mathbf r)
=\int d^d R'\,
w_R(\mathbf R')w_R(\mathbf R'+\mathbf r).
$$

粒子数方差在实空间中为

$$
\operatorname{Var}(N_R)
=\int d^d r\,C(\mathbf r)\alpha_R(\mathbf r),
$$

在 Fourier 空间中为

$$
\operatorname{Var}(N_R)
=\frac{\rho_0}{(2\pi)^d}
\int d^d k\,S(\mathbf k)
\left|\widetilde w_R(\mathbf k)\right|^2.
$$

若 $w_R(\mathbf r)=w_1(\mathbf r/R)$，则

$$
\widetilde w_R(\mathbf k)
=R^d\widetilde w_1(R\mathbf k).
$$

对球形或具有足够规则边界的窗口，若 $S(k)\sim k^{\alpha}$，则大 $R$ 渐近行为为

$$
\operatorname{Var}(N_R)\sim
\begin{cases}
R^{d-\alpha}, & -d<\alpha<1,\\[1mm]
R^{d-1}\ln R, & \alpha=1,\\[1mm]
R^{d-1}, & \alpha>1.
\end{cases}
$$

其中 $\alpha<0$ 对应巨数涨落，$\alpha=0$ 给出泊松型体积标度，$0<\alpha<1$ 对应超均匀但仍大于表面积标度的方差。$\alpha\ge1$ 时，窗口边界主导渐近行为。

由于平均粒子数满足 $\langle N_R\rangle\propto R^d$，若忽略 $\alpha=1$ 的对数修正并写成

$$
\operatorname{Var}(N_R)
\propto\langle N_R\rangle^{\beta},
$$

则

$$
\beta=
\begin{cases}
1-\dfrac{\alpha}{d}, & -d<\alpha<1,\\[2mm]
1-\dfrac{1}{d}, & \alpha>1.
\end{cases}
$$

在 $\alpha=1$ 时还要乘以 $\ln R$，因此不能仅用一个纯幂指数完整描述。对于与晶格方向锁定的非球形窗口，数目方差还可能依赖窗口形状和取向。

## 5. 独立随机位移是否破坏超均匀性

在吸收态模型中，常用“自然初态”构造是：先让体系进入吸收态，再对每个粒子施加小位移以重新激活体系。设

$$
\mathbf R_i' = \mathbf R_i+\mathbf u_i,
$$

其中位移 $\mathbf u_i$ 独立同分布，并与原始粒子构型独立。定义位移分布的特征函数

$$
\Phi(\mathbf k)
=\left\langle e^{-i\mathbf k\cdot\mathbf u}\right\rangle.
$$

对任意非零波矢，位移后的结构因子精确满足

$$
S'(\mathbf k)
=1-|\Phi(\mathbf k)|^2
+|\Phi(\mathbf k)|^2S(\mathbf k).
$$

推导的关键是区分 $i=j$ 的自关联项和 $i\ne j$ 的粒子间关联项：前者恒为 $1$，后者被 $|\Phi(\mathbf k)|^2$ 乘法修正。

若位移分布均值为零、各向同性且具有有限四阶矩，并定义单个笛卡尔分量的方差为

$$
\langle u_a u_b\rangle=\sigma_u^2\delta_{ab},
$$

则

$$
\Phi(\mathbf k)
=1-\frac{1}{2}\sigma_u^2k^2+O(k^4),
$$

$$
|\Phi(\mathbf k)|^2
=1-\sigma_u^2k^2+O(k^4).
$$

因此

$$
S'(k)
=S(k)+\sigma_u^2k^2[1-S(k)]+O(k^4).
$$

若原体系满足 $S(k)\sim A k^{\alpha}$ 且 $\alpha>0$，则位移后的小波数指数为

$$
\alpha'=\min(\alpha,2).
$$

具体地：

- $0<\alpha<2$ 时，原来的 $k^{\alpha}$ 项占主导，指数不变；
- $\alpha=2$ 时，位移改变 $k^2$ 项的系数；
- $\alpha>2$ 时，独立有限方差位移生成 $k^2$ 项，将指数降为 $2$。

因此这类位移不会把超均匀体系变成普通泊松体系，但会把强于 $k^2$ 的小波数抑制截断到 $k^2$。若位移具有空间关联、重尾分布或与初始构型相关，上述结论需要重新推导。

## 6. 吸收态转变中的超均匀指数

守恒有向渗流（conserved directed percolation, C-DP）、Manna 模型和随机组织模型的临界吸收态可以出现超均匀性，但其指数关系仍涉及活跃研究。

较早的工作基于 C-DP 与 quenched Edwards–Wilkinson depinning 的映射，提出过

$$
\alpha_{\mathrm{HU}}
\stackrel{\text{conjecture}}{=}
4-d-2\zeta_{\mathrm{dep}},
$$

其中 $\zeta_{\mathrm{dep}}$ 是 depinning 粗糙度指数。这个关系应标记为历史猜想，而不是确定标度律。

后续 Doi–Peliti 场论指出，C-DP 在 $d=4-\epsilon$ 附近的超均匀指数为

$$
\alpha_{\mathrm{HU}}
=\frac{2\epsilon}{9}+O(\epsilon^2),
$$

并明确否定了上述简单 depinning 标度关系。更新的随机组织场论进一步指出，守恒噪声可能是危险无关变量，使随机组织与 C-DP 共享若干临界指数，却具有不同的超均匀指数。因此，分析具体模型时应说明模型、噪声结构、维数和所采用的理论或数值估计，不能把单一公式普遍用于所有吸收态模型。

## 7. 动态结构因子 $S(k,\omega)$

对时间平移不变的稳态，定义中间散射函数

$$
F(\mathbf k,t)
=\frac{1}{N}
\left\langle
\delta\rho_{\mathbf k}(t)
\delta\rho_{-\mathbf k}(0)
\right\rangle.
$$

动态结构因子定义为

$$
S(\mathbf k,\omega)
=\int_{-\infty}^{\infty}dt\,
e^{i\omega t}F(\mathbf k,t).
$$

静态结构因子是等时关联

$$
S(\mathbf k)=F(\mathbf k,0),
$$

并满足频率总和规则

$$
S(\mathbf k)
=\frac{1}{2\pi}
\int_{-\infty}^{\infty}d\omega\,
S(\mathbf k,\omega).
$$

若体系在小波数下只有一个特征频率尺度 $\omega_k\sim k^z$，则与总和规则一致的动态标度形式是

$$
S(k,\omega)
=S(k)k^{-z}
f\!\left(\frac{\omega}{k^z}\right),
$$

其中标度函数归一化为

$$
\frac{1}{2\pi}\int_{-\infty}^{\infty}dx\,f(x)=1.
$$

### 7.1 扩散密度模

对线性扩散模，若

$$
F(k,t)=S(k)e^{-Dk^2|t|},
$$

则

$$
S(k,\omega)
=\frac{2S(k)Dk^2}
{\omega^2+(Dk^2)^2}.
$$

若静态结构因子满足 $S(k)\sim k^{\alpha}$，零频附近谱峰的宽度按 $k^2$ 缩小，而峰高按 $k^{\alpha-2}$ 标度。

### 7.2 热扩散峰与声峰

简单流体同时具有位于 $\omega=0$ 的 Rayleigh 热扩散峰和位于 $\omega=\pm c_s k$ 的 Brillouin 声峰。忽略更高阶修正时，可写成归一化的示意形式

$$
\begin{aligned}
S(k,\omega)\simeq S(k)\Bigg[
&A_R\frac{2D_Tk^2}{\omega^2+(D_Tk^2)^2}\\
&+\frac{A_B}{2}\sum_{\pm}
\frac{2\Gamma k^2}
{(\omega\mp c_s k)^2+(\Gamma k^2)^2}
\Bigg],
\end{aligned}
$$

其中 $A_R+A_B=1$。$A_R$、$A_B$ 的具体热力学权重以及 $D_T$、$c_s$、$\Gamma$ 取决于模型。这个谱同时含有传播尺度 $\omega\sim k$ 和衰减尺度 $\omega\sim k^2$，因此不能用单一动态指数完整描述。

静态 $S(k)$ 回答“每个尺度上有多少密度涨落”，动态 $S(k,\omega)$ 进一步区分这些涨落是扩散、传播还是弛豫，以及相应的时间尺度。

非稳态体系不具备时间平移不变性，应使用双时间关联 $F(\mathbf k;t,t')$，而不能直接套用只依赖时间差的 $S(k,\omega)$。

## 8. 周期性粒子模拟中如何计算 $S(k)$

### 8.1 单个构型

对边长为 $L$ 的二维周期性方盒，允许波矢为

$$
\mathbf k=\frac{2\pi}{L}(n_x,n_y),
\qquad n_x,n_y\in\mathbb Z.
$$

对每个非零波矢计算

$$
\rho_{\mathbf k}
=\sum_{j=1}^{N}
e^{-i\mathbf k\cdot\mathbf r_j}
=\sum_j\cos(\mathbf k\cdot\mathbf r_j)
-i\sum_j\sin(\mathbf k\cdot\mathbf r_j),
$$

以及单构型散射强度

$$
\widehat S(\mathbf k)=\frac{|\rho_{\mathbf k}|^2}{N}.
$$

平移不变体系的 $S(\mathbf k)$ 是 $\widehat S(\mathbf k)$ 的系综平均。实际模拟通常用多个充分间隔的稳态快照估计该平均；若样本在时间上相关，应估计有效独立样本数和误差。

### 8.2 壳平均

只有在体系预期各向同性时，才将 $|\mathbf k|$ 落入同一窄区间的模式平均成 $S(k)$。建议同时记录每个壳内的平均 $k$、模式数和跨快照误差。正方盒不禁止按照模长分箱，但原始采样点必须来自笛卡尔倒格矢，不能把任意连续极坐标波矢当作周期边界下的允许模式。

下面的 C++ 示例同时对独立波矢和快照累加，并显式跳过零模：

```cpp
#include <cmath>
#include <complex>
#include <cstddef>
#include <vector>

struct Particle {
    double x;
    double y;
};

void accumulate_radial_sk(
    const std::vector<Particle>& particles,
    double box_length,
    int n_max,
    double delta_k,
    std::vector<double>& k_sum,
    std::vector<double>& sk_sum,
    std::vector<std::size_t>& sample_count
) {
    if (particles.empty() || box_length <= 0.0 || delta_k <= 0.0) {
        return;
    }

    constexpr double PI = 3.14159265358979323846;
    const double k_min = 2.0 * PI / box_length;
    const double inv_n = 1.0 / static_cast<double>(particles.size());

    for (int n_x = -n_max; n_x <= n_max; ++n_x) {
        for (int n_y = -n_max; n_y <= n_max; ++n_y) {
            // 跳过零模，并只保留 ±k 中的一个，避免重复计数。
            if (n_x < 0 || (n_x == 0 && n_y <= 0)) {
                continue;
            }

            const double k_x = k_min * static_cast<double>(n_x);
            const double k_y = k_min * static_cast<double>(n_y);
            const double k = std::hypot(k_x, k_y);
            const std::size_t bin =
                static_cast<std::size_t>(std::floor(k / delta_k));

            if (bin >= sk_sum.size() ||
                bin >= k_sum.size() ||
                bin >= sample_count.size()) {
                continue;
            }

            std::complex<double> rho_k{0.0, 0.0};
            for (const Particle& particle : particles) {
                const double phase = k_x * particle.x + k_y * particle.y;
                rho_k += std::complex<double>{
                    std::cos(phase), -std::sin(phase)
                };
            }

            const double sk = std::norm(rho_k) * inv_n;
            k_sum[bin] += k;
            sk_sum[bin] += sk;
            sample_count[bin] += 1;
        }
    }
}
```

完成所有快照后，对每个非空分箱输出

$$
k_{\mathrm{bin}}
=\frac{k_{\mathrm{sum}}}{n_{\mathrm{bin}}},
\qquad
S(k_{\mathrm{bin}})
=\frac{S_{\mathrm{sum}}}{n_{\mathrm{bin}}}.
$$

这里的 $n_{\mathrm{bin}}$ 同时计入壳内模式和快照。若要估计统计误差，不应把同一快照中的不同波矢或 $\pm\mathbf k$ 简单当作完全独立样本；更稳妥的做法是先对每个快照完成壳平均，再对快照平均并进行阻塞分析。

### 8.3 使用 Type-1 NUFFT 加速

直接求和需要对每个粒子和每个波矢计算复指数。若共有 $N$ 个粒子和 $M$ 个 Fourier 模式，其计算量为 $O(NM)$。当粒子坐标是连续值、但目标波矢仍是周期盒允许的规则倒格矢时，可以使用 Type-1 非均匀快速 Fourier 变换（nonuniform fast Fourier transform, NUFFT）。

定义缩放后的周期坐标

$$
\mathbf x_j
=\frac{2\pi}{L}\mathbf r_j
\pmod{2\pi}.
$$

Type-1 NUFFT 一次计算所有整数模式

$$
\rho_{\mathbf n}
=\sum_{j=1}^{N}
e^{-i\mathbf n\cdot\mathbf x_j},
\qquad
\mathbf n=(n_x,n_y),
$$

它们正好对应物理波矢

$$
\mathbf k=\frac{2\pi}{L}\mathbf n.
$$

因此 NUFFT 只替换 $\rho_{\mathbf k}$ 的计算步骤；随后仍按

$$
S(\mathbf k)=\frac{|\rho_{\mathbf k}|^2}{N}
$$

计算结构因子，并使用与直接算法完全相同的壳划分。典型 NUFFT 将粒子扩散到过采样网格，执行普通 FFT，再在 Fourier 空间去卷积。若扩散核宽度为 $w$，其成本近似为

$$
O(Nw^d)+O(M\log M),
$$

其中 $w$ 随目标精度提高而缓慢增加。

下面使用 FINUFFT 的二维 Type-1 接口。`modeord=0` 指定以零模为中心的输出顺序，因此数组中心 `[n_max, n_max]` 对应 $\mathbf k=0$。

```python
import finufft
import numpy as np


def structure_factor_nufft(
    positions: np.ndarray,
    box_length: float,
    n_max: int,
    eps: float = 1.0e-12,
    nthreads: int = 1,
) -> np.ndarray:
    """Return S(k_x, k_y) for modes -n_max, ..., n_max."""
    positions = np.asarray(positions, dtype=np.float64)
    if positions.ndim != 2 or positions.shape[1] != 2 or positions.shape[0] == 0:
        raise ValueError("positions must have shape (N, 2) with N > 0")
    if box_length <= 0.0 or n_max < 0 or nthreads < 1:
        raise ValueError("box_length and nthreads must be positive; n_max must be nonnegative")
    particle_count = positions.shape[0]

    # FINUFFT recommends periodic coordinates in [-pi, pi).
    scaled = 2.0 * np.pi * positions / box_length
    scaled = (scaled + np.pi) % (2.0 * np.pi) - np.pi
    x = np.ascontiguousarray(scaled[:, 0])
    y = np.ascontiguousarray(scaled[:, 1])
    strengths = np.ones(particle_count, dtype=np.complex128)
    mode_count = 2 * n_max + 1

    rho_k = finufft.nufft2d1(
        x,
        y,
        strengths,
        (mode_count, mode_count),
        eps=eps,
        isign=-1,
        modeord=0,
        nthreads=nthreads,
    )
    sk = np.abs(rho_k) ** 2 / particle_count
    sk[n_max, n_max] = np.nan  # 固定粒子数下不使用零模。
    return sk
```

把坐标平移到 $[-\pi,\pi)$ 只会给 $\rho_{\mathbf k}$ 乘上依赖于模式的相位，不改变 $|\rho_{\mathbf k}|^2$。若需要逐复数振幅比较，直接求和与 NUFFT 必须使用同一个坐标原点和 Fourier 符号。

#### 与直接求和的数值对比

为了比较随体系尺寸的变化，以下测试固定二维数密度 $\rho=N/L^2=1$，并固定每个 Cartesian 分量的物理截止波数 $k_{\max}\simeq1.42$。因此增大 $N$ 时有 $L\propto N^{1/2}$、$n_{\max}\propto L$，所需 Fourier 模式数 $M=(2n_{\max}+1)^2\propto N$。这比“固定模式数”更接近在不同体系中保持同一空间分辨率的生产计算。两种算法使用同一批粒子、同一组模式和同一壳划分。

##### 速度与复杂度

![固定密度、固定物理截止波数下两种算法随体系尺寸的耗时](assets/sk-runtime-scaling.png)

直接算法采用分块 NumPy 求和，每个尺寸重复三次；FINUFFT 2.5.1 使用双精度、`eps=1e-12`、单线程，预热后重复七次。图中的点是中位数，误差棒覆盖最小值到最大值。对 $N=4{,}000$ 到 $32{,}000$ 的后四点作 log--log 拟合，直接求和为 $t\propto N^{1.90}$，接近本协议下的理论标度 $O(NM)\sim O(N^2)$；NUFFT 为 $t\propto N^{0.82}$。后者的有限区间指数受固定开销影响，不应解释为渐近复杂度；理论成本仍近似为 $O(N+M\log M)\sim O(N\log N)$。

| $N$ | 模式数 $M$ | 直接求和 | Type-1 NUFFT | 加速比 |
|---:|---:|---:|---:|---:|
| 1,000 | 225 | 8.21 ms | 0.357 ms | $23.0$ |
| 2,000 | 441 | 32.0 ms | 0.473 ms | $67.7$ |
| 4,000 | 841 | 0.123 s | 0.698 ms | $176$ |
| 8,000 | 1,681 | 0.446 s | 1.07 ms | $418$ |
| 16,000 | 3,249 | 1.69 s | 1.85 ms | $913$ |
| 32,000 | 6,561 | 6.33 s | 3.86 ms | $1.64\times10^3$ |

在这个固定物理分辨率的扫描中，体系从 $N=1{,}000$ 增至 $32{,}000$ 时，直接求和耗时增加约 770 倍，而 NUFFT 只增加约 10.8 倍；相应加速比从约 23 增至约 1,641。具体耗时和交叉尺度仍依赖硬件与实现。

##### 准确度

准确度不能用“NUFFT 与直接求和之差”完全定义，因为这会预先把直接求和当作精确答案。下面改用单位间距的完美方格点阵作为解析基准。对于图中选取的全部非零模式，波数都低于第一组倒格矢峰，因而精确结果是 $S(\mathbf k)=0$。纵轴画的是全部非零模式中的最大绝对误差；数值越低，算法越准确。

![两种算法相对于完美方格点阵解析零谱的误差](assets/sk-accuracy-scaling.png)

| $N$ | 直接求和最大 $\lvert\Delta S(\mathbf k)\rvert$ | NUFFT 最大 $\lvert\Delta S(\mathbf k)\rvert$ |
|---:|---:|---:|
| 1,024 | $8.38\times10^{-29}$ | $1.30\times10^{-23}$ |
| 2,025 | $2.42\times10^{-28}$ | $5.25\times10^{-23}$ |
| 4,096 | $2.88\times10^{-28}$ | $5.20\times10^{-23}$ |
| 8,281 | $9.71\times10^{-27}$ | $2.72\times10^{-23}$ |
| 16,384 | $3.99\times10^{-26}$ | $2.09\times10^{-22}$ |
| 32,761 | $1.13\times10^{-25}$ | $1.62\times10^{-21}$ |

在这个严格的解析零信号测试中，直接求和的残差比 `eps=1e-12` 的 NUFFT 小约四至六个数量级；这是 NUFFT 以可控近似换取速度的体现。尽管误差随体系尺寸有波动并总体增大，即使在最大体系中，NUFFT 的最大伪结构因子仍只有 $1.62\times10^{-21}$。对于随机点体系，两种算法的最大壳平均差始终低于 $8.0\times10^{-12}$，全部尺寸中的最大壳平均 RMS 相对差为 $6.9\times10^{-13}$。

精度随 FINUFFT 容差的收敛如下：

| `eps` | 最大逐模 $\lvert\Delta S(\mathbf k)\rvert$ | 最大壳平均 $\lvert\Delta S(k)\rvert$ | 壳平均 RMS 相对差 |
|---:|---:|---:|---:|
| $10^{-6}$ | $7.88\times10^{-6}$ | $4.16\times10^{-7}$ | $1.23\times10^{-7}$ |
| $10^{-8}$ | $1.72\times10^{-8}$ | $1.78\times10^{-9}$ | $4.65\times10^{-10}$ |
| $10^{-10}$ | $5.09\times10^{-10}$ | $4.71\times10^{-11}$ | $1.56\times10^{-11}$ |
| $10^{-12}$ | $7.90\times10^{-12}$ | $6.81\times10^{-13}$ | $1.24\times10^{-13}$ |

`eps` 控制的是 Fourier 变换误差，不保证超均匀指数的统计误差或有限尺寸误差。生产计算中应采用以下验证门槛：

1. 使用双精度和 `eps=1e-12` 计算完整谱。
2. 对进入小 $k$ 拟合的最低若干壳，用直接求和逐模复核。
3. 比较至少 `eps=1e-8, 1e-10, 1e-12` 三档结果，要求壳平均和拟合指数在目标误差内不再变化。
4. 独立改变系统尺寸、快照间隔和拟合窗口；NUFFT 收敛不能替代这些物理与统计收敛检查。

普通“粒子沉积到网格再 FFT”还会引入质量分配窗函数和 aliasing。高阶粒子分配、交错网格和去卷积可以显著减小这些误差，但若目标是连续粒子坐标上的高精度 $S(\mathbf k)$，Type-1 NUFFT 提供了更直接、容差可控的路径。

### 8.4 有限尺寸与拟合注意事项

1. 最小非零波数是 $k_{\min}=2\pi/L$。判断 $k\to0$ 标度必须比较多个系统尺寸。
2. 不要把固定粒子数导致的 $S(0)=0$ 纳入幂律拟合。
3. 拟合区间应同时避开有限尺寸区和粒子尺度附近的高波数区。
4. 应报告分箱宽度、每个壳的模式数、快照间隔、样本数和误差估计。
5. 若 $S(\mathbf k)$ 显示明显角向结构，应报告二维谱，而不是只展示径向平均。

## 附录：$d$ 维球形窗口的形状因子

对半径为 $R$ 的 $d$ 维球形窗口，令 $q=kR$。归一化形状因子为

$$
F_d(q)
=\frac{|\widetilde w_R(k)|^2}{V_R^2}
=\left[
\frac{2^{d/2}\Gamma(1+d/2)}{q^{d/2}}
J_{d/2}(q)
\right]^2,
$$

其中 $J_{\nu}$ 是第一类 Bessel 函数。前三个维数分别为

$$
F_1(q)=\left(\frac{\sin q}{q}\right)^2,
$$

$$
F_2(q)=\left(\frac{2J_1(q)}{q}\right)^2,
$$

$$
F_3(q)=\left[
\frac{3(\sin q-q\cos q)}{q^3}
\right]^2.
$$

在大 $q$ 下，其振荡包络满足 $F_d(q)\sim q^{-(d+1)}$。正是这一慢衰减使 $\alpha\ge1$ 时窗口边界控制粒子数方差的主导标度。

## 参考资料

- [Torquato and Stillinger, *Local Density Fluctuations, Hyperuniformity, and Order Metrics*](https://arxiv.org/abs/cond-mat/0311532)
- [Gabrielli, *Point processes and stochastic displacement fields*](https://arxiv.org/abs/cond-mat/0409594)
- [Hexner and Levine, *Hyperuniformity of critical absorbing states*](https://arxiv.org/abs/1407.0146)
- [Ma, Pausch, and Cates, *Theory of Hyperuniformity at the Absorbing State Transition*](https://arxiv.org/abs/2310.17391)
- [Ma, Pausch, Pruessner, and Cates, *Hyperuniformity at the Absorbing State Transition: Perturbative RG for Random Organization*](https://arxiv.org/abs/2507.07793)
- [Hawat et al., *On estimating the structure factor of a point process, with applications to hyperuniformity*](https://arxiv.org/abs/2203.08749)
- [Barnett, Magland, and af Klinteberg, *A parallel non-uniform fast Fourier transform library based on an exponential of semicircle kernel*](https://arxiv.org/abs/1808.06736)
- [Barnett, *Aliasing error of the exponential-of-semicircle kernel in the nonuniform fast Fourier transform*](https://arxiv.org/abs/2001.09405)
- [Sefusatti et al., *Accurate Estimators of Correlation Functions in Fourier Space*](https://arxiv.org/abs/1512.07295)
