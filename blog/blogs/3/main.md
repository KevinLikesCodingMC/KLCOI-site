# CSP2024模拟测试九 D - 树上开花

## 简要题意

对于 $1\le k \le n$ 的每一个 $k$，求出有多少大小为 $k$ 的点集，满足其点集内任意两个点的距离不超过 $x$。

答案对 $998244353$ 取模。

## 题解

### 主要思路

对于这类点集方案数的题，一种套路的方法就是枚举中心点。  
对于 $x$ 为奇数的情况，可以将原有的点作为关键点，并在每一条边上加上一个额外点，这样 $x$ 就翻了一倍成为了偶数，这样中心一定在点上。

然后对于一个中心点 $i$，其能取到的点必须与 $i$ 的距离不超过 $\frac{x}{2}$，
然后设与 $i$ 点距离小于 $\frac{x}{2}$ 的点有 $u_i$ 个，
那么粗略的统计，若子集大小为 $k$，则有 $\binom{u_i}{k} $ 种选法。  

但是警惕！这样算算重很多，譬如一个子集会被多个中心点计算到。  

怎么解决呢？观察提供贡献的中心点，不难发现这个点一定会组成一个联通块。

这有什么用吗？注意到，一个联通快的边的个数等于点的个数减一。到这里方法应该显然易见了，
再以边为中心点，然后合法的点是距离这条边的两个端点的距离都不超过 $\frac{x}{2}$，定义边 $i$ 的合法点的数量为 $e_i$，
那么以边来选即为 $\binom{e_i}{k} $，然后两者相减即可做道不重不漏。

得出最后的式子：

$$ Ans_i=\sum_{j\in V}\binom{u_j}{i} -\sum_{j\in E}\binom{e_j}{i} $$

### 实现

#### 求 $u_i$ 与 $e_i$

这里考虑淀粉质（点分治）实现。考虑一个点或边所在的子树被分割时，
这是这颗子树外的节点以后就不会对该点或边产生贡献，所以在分割前把其他子树的点的贡献统计一下。

实现也是非常的简单，考虑先前缀和记录每一种深度内的节点数，然后容斥，把同子树的方案减掉。

时间复杂度可以做道 $O(n\log n)$。

#### 求 $Ans$ 数组

上面已经求出了式子：

$$ Ans_i=\sum_{j\in V}\binom{u_j}{i} -\sum_{j\in E}\binom{e_j}{i} $$

这个 $u_j$ 和 $e_j$ 不难想到用出现次数来代替，其中 $u_i$ 出现则次数加一，若是 $e_i$ 则次数减一，原式即可变为：

$$ Ans_i=\sum_{j=i}^{n}c_j\binom{j}{i} $$

然后组合数展开一下：

$$ Ans_i=\sum_{j=i}^{n}c_j\frac{j!}{i!(j-i)!} $$

把与 $j$ 没有关系的 $i$ 提出来：

$$ Ans_i=\frac{1}{i!}\sum_{j=i}^{n}\frac{c_j\cdot j!}{(j-i)!} $$

这里发现这个式子不能直接做卷积，回顾一下卷积基本式子：

$$H_i=\sum_{j=0}^{i}F_jG_{i-j}$$

一个函数必须关于 $j$，另一个必须关于 $i-j$，上面的式子把 $j$ 移动后就不符合了。

这里考虑反转下标，设 $Ans_i=\frac{1}{i!}H_{n-i}$，接下来只需求出 $H_i$，直接带入：

$$
\begin{aligned}
H_i & = \sum_{j = n-i}^{n}\frac{c_j\cdot j!}{(j-n+i)!} \\\\
& = \sum_{j = 0}^{i}\frac{c_{n-j}\cdot (n-j)!}{({n-j}-n+i)!} \\\\
& = \sum_{j = 0}^{i}(c_{n-j}\cdot (n-j)!) \cdot\frac{1}{(i-j)!} \\\\
\end{aligned}
$$

左边关于 $j$ 右边关于 $i-j$，完全胜利！

直接跑 [NTT](https://oi-wiki.org/math/poly/ntt/) 卷积即可，时间复杂度 $O(n\log n)$。

总时间复杂度 $O(n\log n)$，足以通过。

<div class="alert alert-info" role="alert">
  ナイテイタ　ナイテイタカラ  <br>
  （泣いていた　泣いていたから）　<br>
  是因为：还不是因为自己————不够努力。
</div>
<div class="alert alert-success" role="alert">
  だらしなくて弱い僕だって　<br>
  歌い続けるよ　<br>
  続けるよ　<br>
</div>

```cpp
const int N = 6e5 + 5;
const int INF = 1e9 + 7;
const int P = 998244353;
int I, n, X;
int fi[N], ne[N << 1], to[N << 1], ecnt = 1;
int rt, sz[N], mx[N], vis[N];
int a[N], b[N], d[N], s[N], t[N], mxd, mxs;
int fac[N], finv[N];
int r[N << 2], f[N << 2], g[N << 2];
int add(int x, int y) { return (x + y < P ? x + y : x + y - P); }
void Add(int &x, int y) { x = (x + y < P ? x + y : x + y - P); }
int sub(int x, int y) { return (x < y ? x - y + P : x - y); }
int mul(int x, int y) { return (1ll * x * y) % P; }
void Mul(int &x, int y) { x = (1ll * x * y) % P; }
int fp(int x, int y) {
	int res = 1;
	for(; y; y >>= 1) {
		if(y & 1) Mul(res, x);
		Mul(x, x);
	}
	return res;
}
void add_edge(int u, int v) {
	ne[++ecnt] = fi[u];
	to[ecnt] = v;
	fi[u] = ecnt;
}
void fsz(int u, int fa, int sum) {
	sz[u] = 1;
	mx[u] = 0;
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(v == fa || vis[v]) continue;
		fsz(v, u, sum);
		sz[u] += sz[v];
		chmax(mx[u], sz[v]);
	}
	chmax(mx[u], sum - sz[u]);
	if(mx[u] < mx[rt]) rt = u;
}
void dfs1(int u, int fa) {
	chmax(mxd, d[u]);
	if(u <= n) s[d[u]]++;
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(v == fa || vis[v]) continue;
		d[v] = d[u] + 1;
		dfs1(v, u);
	}
}
void dfs2(int u, int fa) {
	chmax(mxs, d[u]);
	if(u <= n) t[d[u]]++;
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(v == fa || vis[v]) continue;
		dfs2(v, u);
	}
}
void dfs3(int u, int fa, int eg) {
	if(d[u] <= X) {
		int val = s[min(mxd, X - d[u])] - t[min(mxs, X - d[u])];
		a[u] += val;
		b[eg / 2] += val;
	} 
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(v == fa || vis[v]) continue;
		dfs3(v, u, i);
	}
}
void slv(int u) {
	mxd = 0;
	if(u <= n) s[0] += 1;
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(vis[v]) continue;
		d[v] = 1;
		dfs1(v, u);
	}
	FOR(i, 1, mxd) s[i] += s[i - 1];
	a[u] += s[min(X, mxd)];
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(vis[v]) continue;
		mxs = 0;
		dfs2(v, u);
		FOR(j, 1, mxs) t[j] += t[j - 1];
		b[i / 2] += t[min(X, mxs)];
		dfs3(v, u, i);
		FOR(j, 1, mxs) t[j] = 0;
	}
	FOR(i, 0, mxd) s[i] = 0;
}
void dfz(int u, int sum) {
	vis[u] = 1;
	slv(u);
	for(int i = fi[u]; i; i = ne[i]) {
		int v = to[i];
		if(vis[v]) continue;
		int siz = sz[v] < sz[u] ? sz[v] : sum - sz[u];
		rt = 0; fsz(v, u, siz);
		dfz(rt, siz);
	}
}
void NTT(int *a, int lim, int o) {
	REP(i, lim) if(i < r[i]) swap(a[i], a[r[i]]);
	for(int i = 1; i < lim; i <<= 1) {
		int wn = fp(o == 1 ? 3 : 332748118, (P - 1) / (i << 1));
		for(int j = 0; j < lim; j += (i << 1)) {
			int w = 1;
			for(int k = 0; k < i; k++, Mul(w, wn)) {
				int x = a[j + k];
				int y = mul(a[j + k + i], w);
				a[j + k] = add(x, y);
				a[j + k + i] = sub(x, y);
			}
		}
	}
	if(o == 1) return;
	int inv = fp(lim, P - 2);
	REP(i, lim) Mul(a[i], inv);
}
void solve() {
	cin >> I >> n >> X;
	FOR(i, 1, n - 1) {
		int u, v;
		cin >> u >> v;
		add_edge(u, n + i), add_edge(n + i, u);
		add_edge(v, n + i), add_edge(n + i, v);
	}
	mx[rt] = INF;
	fsz(1, 0, n * 2 - 1);
	dfz(rt, n * 2 - 1);
	fac[0] = 1;
	FOR(i, 1, n) fac[i] = mul(fac[i - 1], i);
	finv[n] = fp(fac[n], P - 2);
	ROF(i, n - 1, 0) finv[i] = mul(finv[i + 1], i + 1);
	FOR(i, 1, n * 2 - 1) {
		f[n - a[i]]++;
		f[n - b[i]]--;
	}
	FOR(i, 0, n) {
		f[i] = (f[i] + P) % P;
		Mul(f[i], fac[n - i]);
		g[i] = finv[i];
	}
	int lim = 1, l = 0;
	while(lim <= n * 2) lim <<= 1, l++;
	REP(i, lim) r[i] = (r[i >> 1] >> 1) | ((i & 1) << (l - 1));
	NTT(f, lim, 1);
	NTT(g, lim, 1);
	REP(i, lim) Mul(f[i], g[i]);
	NTT(f, lim, -1);
	FOR(i, 1, n) cout << mul(f[n - i], finv[i]) << " ";
	cout << endl;
}
```
