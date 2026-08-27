# C/C++ 数值模拟注意点

优化前先保证结果正确，再用性能分析工具定位瓶颈。每次只改一项，便于判断收益和回退。

1. **数据对齐**
   
   需要 SIMD 或避免伪共享时，可使用标准 C++ 的 `alignas(bytes)`。对齐和填充过多也会浪费内存，应通过测试决定。

2. **连续内存**
   
   规则数组尽量使用连续存储，并使循环顺序与存储顺序一致，以提高缓存命中率。二维数据可用一维 `std::vector<T>` 存储。

3. **内存分配**
   
   先减少热循环中的反复分配，例如预留容量和复用缓冲区。只有确认分配器是瓶颈时，才考虑其他内存池或分配器。

4. **矩阵计算**
   
   大矩阵运算可使用分块提高缓存利用率。Strassen 算法只适合经过基准测试和误差检查的特定大规模问题，不是默认选择。

5. **数学库**
   
   矩阵乘法、分解和线性方程求解应优先使用经过优化的 BLAS/LAPACK 库。同时检查库内部线程是否与外层并行重叠。

6. **SIMD 向量化**
   
   先尝试编译器自动向量化，再考虑 SSE/AVX intrinsic。手写 SIMD 需要处理 CPU 支持、数据对齐、尾部元素和可移植性。

7. **循环优化**
   
   将不随循环变化的计算移到循环外，并避免在热循环中分配内存或重复调用高开销函数。

8. **编译优化**
   
   通常先比较 `-O2` 和 `-O3`。`-Ofast` 可能改变浮点语义，只有在数值误差和性能都经过验证后才使用。

9. **多线程并行**
   
   可使用 C++ 线程、TBB 或 OpenMP 并行处理独立任务。需要检查数据竞争、同步开销、伪共享和浮点求和顺序的变化。

10. **任务划分**
    
    任务应尽量负载均衡，同时保证单个任务足够大，避免调度开销超过并行收益。

11. **性能分析**
    
    使用 `perf`、gprof、Cachegrind 或 Intel VTune 定位热点。Valgrind Memcheck 和 sanitizer 主要用于检查正确性，不应用它们的运行时间作为正常性能结果。

12. **优化后验证**
    
    每次优化后都要复测墙钟时间，并检查误差、守恒量、统计分布和收敛趋势。只有结果正确且稳定加速时，才能保留改动。

## 参考

[GCC 优化选项](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) · [OpenMP 循环调度](https://www.openmp.org/spec-html/5.2/openmpse66.html) · [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html) · [Valgrind Cachegrind](https://valgrind.org/docs/manual/cg-manual.html)
