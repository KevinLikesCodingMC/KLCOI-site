# P7884 【模板】Meissel-Lehmer

一道 Meissel-Lehmer 算法的模板题洛谷题解里没有 Meissel-Lehmer，大悲啊。

这里介绍 Meissel-Lehmer 算法。

先线性筛算出前大于等于 $n^\frac{1}{2}$ 个数内的素数和 $\pi(n)$。

然后对于求 $\pi(n)$，考虑对其产生贡献的素数分治。 
考虑对于 $n^\frac{1}{3}$ 分治，先算出 $(n^\frac{1}{3},n]$ 中对于 $n^\frac{1}{3}$ 以内的素数筛不掉的数，暂定一个 dp，$dp_{i,j}$ 表示 $[1,i]$ 中不会被前 $j$ 个素数筛掉的个数。

接下来不难发现，现在筛剩下的 $(n^\frac{1}{3},n]$ 中的数，如果是合数，则其必定为两个大于 $n^\frac{1}{3}$ 的素数的乘积，其他即为素数。

计算这类由两个素数相乘的数的个数很简单，直接考虑枚举小的素数，去计算另外一个素数的方案数即可，假设当前选取了小素数 $p$，则其筛掉的数就是 $[p,\frac{n}{p}]$ 中的素数的个数，即为 $\pi(\frac{n}{p})-\pi(p)+1$。

结合一下上述，可得出 $\pi(n)$ 的递归公式：  
$$
\pi(n)=dp_{n,\pi(n^\frac{1}{3})}-1+\pi(n^\frac{1}{3})
-\sum_{p\in(n^\frac{1}{3},n^\frac{1}{2}]} \pi(\frac{n}{p})-\pi(p)+1
$$    
公式前面减一是因为 $1$ 是筛不掉的，其中 $p$ 为素数。

然后考虑如何求 dp 数组，考虑转移。考虑计算最后一个素数的贡献，发现其贡献是其倍数中没有被前面素数筛掉的数的个数，发现可以再利用 dp 数组，所以转移为 $dp_{i,j}=dp_{i,j-1}-dp_{\frac{i}{p_j},j-1}$，其中 $p_j$ 表示第 $j$ 个素数。

考虑边界情况，显然的是 $dp_{i,0}=i$。但这样还不够优，考虑 $p_j^2\ge i$ 的情况，这时 $[1,i]$ 中的合数全被筛过，只剩下素数，所以值即为 $\max(0,\pi(i)-j+1)$，加一是为了留下 $1$，与前面同步。

这样一个基础的 Meissel-Lehmer 算法原理讲解就完成了。

接下来是实现，对于 dp 数组，可以预处理出一部分，例如 $i\le 1.8 \times 10^6,j\le 60$ 的情况。然后由于这道题空间有限，前面公式里的 $\pi(\frac{n}{p})$ 会超出预处理的范围，这是要继续递归。

由于不断递归了 $\pi(n)$，这份代码的时间复杂度我分析不出来，但是时间复杂度应该在 $O(n^\frac{2}{3})$ 级别，足以通过。

```cpp
const int N = 8e6 + 10;
const int MI = 1.8e6;
const int MJ = 60;
ll n;
int f[MI + 5][MJ + 5];
int p[N / 10], ip[N], g[N], cnt;
void init() {
	FOR(i, 2, N - 1) {
		if(!ip[i]) {
			p[++cnt] = i;
		}
		for(int j = 1; j <= cnt && p[j] * i < N; j++) {
			ip[i * p[j]] = 1;
			if(i % p[j] == 0) {
				break;
			}
		}
	}
	// 警惕！这里的 g 数组表示的 pi(n) 含有 1，是 pi(n)+1
	FOR(i, 1, N - 1) g[i] = g[i - 1] + !ip[i];
	FOR(i, 1, MI) f[i][0] = i;
	FOR(i, 1, MI) FOR(j, 1, MJ)
		f[i][j] = f[i][j - 1] - f[i / p[j]][j - 1];
}
ll dp(ll i, ll j) {
	if(i <= MI && j <= MJ) return f[i][j];
	if(!i || !j) return i;
	if(i < N && 1ll * p[j] * p[j] >= i) return max(0ll, g[i] - j);
	return dp(i, j - 1) - dp(i / p[j], j - 1);
}
ll pi(ll n) {
	if(n < N) return g[n] - 1;
	ll sn = pow(n, 1. / 3);
	ll m = g[sn] - 1;
	ll res = dp(n, m) + m - 1;
	for(m++; 1ll * p[m] * p[m] <= n; m++)
		res -= pi(n / p[m]) - pi(p[m]) + 1; // 继续递归
	return res;
}
```