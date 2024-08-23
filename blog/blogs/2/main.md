# P10637 BZOJ4262 Sum 题解

题目链接：[P10637 BZOJ4262 Sum](https://www.luogu.com.cn/problem/P10637)

非常简单的一道题。

同样是 SgT Beats，隔壁 [P10639 BZOJ4695 最佳女选手](https://www.luogu.com.cn/problem/P10639) 做的人好多，这里就没什么人做，差评。

本质和 [P3246 [HNOI2016] 序列](https://www.luogu.com.cn/problem/P3246) 没有区别，都是离线询问然后扫描线，然后在线段树上进行区间最值操作和区间查询历史和。具体的，在时刻 $i$，将区间 $[1,i]$ 对 $a_i$ 进行最值操作，那么此时线段树上 $[1,i]$ 的值就是 $\max_{j=p}^{i}a_j$ 或者 $\min_{j=p}^{i}a_j$ 的值，那么求一段子区间的答案就是求区间的历史和，这个很好理解。这道题由于左右端点都有范围，所以需要两段历史和前缀相减，要把询问拆成 $r_2$ 时刻的 $[l_1,r_1]$ 历史和减去 $l_2-1$ 时刻的 $[l_1,r_1]$ 历史和。

然后就是经典问题，线段树区间最值操作与区间历史和。

对于最值操作，考虑 Beats。以计算 $\min$ 为例，维护最大值，次大值和最大值出现次数，最值操作时不断递归，知道等下最值修改的是小于最大值，大于次大值，这样最值操作只会影响最大值，这样就只用处理一种数了，非常方便，然后时间复杂度是对的，是 $O(n \log n)$。

对于历史和，需要记录一些 tag，例如当前区间修改的次数和修改历史和的值的 tag。注意，对于修改次数的 tag，即使区间操作没有对某区间产生影响，如最值修改的数大于最大值，这时候没有影响，但是也要推一个值的一的修改次数 tag，为了能正确维护历史和。

对与如何更新历史和有疑问的可以观察代码，这还是比较简单的。

时间复杂度 $O(n \log n)$。

```cpp
const int N = 1e5 + 5;
const int P = 1e9;
const int INF = 2.2e9;
int n, m, a[N];
vector<array<int, 4>> e[N];
ll ans[N];
void init() {
	ll fst = 1023, sec = 1025;
	n = 1e5;
	FOR(i, 1, n) {
		a[i] = fst ^ sec;
		fst = fst * 1023 % P;
		sec = sec * 1025 % P;
	}
}
struct SgT {
	int le[N << 2], ri[N << 2];
	int F[N << 2][2], G[N << 2][2], C[N << 2][2], T[N << 2][2], TC[N << 2][2];
	// F 为最大值和次大值，G 为最小值与次小值，C 为最大最小出现次数，
	// T 为最值操作值的 tag，TC 为区间操作次数的 tag
	ll S[N << 2][2], H[N << 2][2], TH[N << 2][2];
	// S 为区间和，H 为区间历史和，TH 为区间历史和的 tag
	void pushup(int u) {
		S[u][0] = S[u << 1][0] + S[u << 1 | 1][0];
		S[u][1] = S[u << 1][1] + S[u << 1 | 1][1];
		F[u][0] = max(F[u << 1][0], F[u << 1 | 1][0]);
		G[u][0] = min(G[u << 1][0], G[u << 1 | 1][0]);
		H[u][0] = H[u << 1][0] + H[u << 1 | 1][0];
		H[u][1] = H[u << 1][1] + H[u << 1 | 1][1];
		if(F[u << 1][0] > F[u << 1 | 1][0]) {
			F[u][1] = max(F[u << 1][1], F[u << 1 | 1][0]);
			C[u][0] = C[u << 1][0];
		}
		else if(F[u << 1][0] < F[u << 1 | 1][0]) {
			F[u][1] = max(F[u << 1][0], F[u << 1 | 1][1]);
			C[u][0] = C[u << 1 | 1][0];
		}
		else {
			F[u][1] = max(F[u << 1][1], F[u << 1 | 1][1]);
			C[u][0] = C[u << 1][0] + C[u << 1 | 1][0];
		}
		if(G[u << 1][0] < G[u << 1 | 1][0]) {
			G[u][1] = min(G[u << 1][1], G[u << 1 | 1][0]);
			C[u][1] = C[u << 1][1];
		}
		else if(G[u << 1][0] > G[u << 1 | 1][0]) {
			G[u][1] = min(G[u << 1][0], G[u << 1 | 1][1]);
			C[u][1] = C[u << 1 | 1][1];
		}
		else {
			G[u][1] = min(G[u << 1][1], G[u << 1 | 1][1]);
			C[u][1] = C[u << 1][1] + C[u << 1 | 1][1];
		}
	}
	void push_max(int u, int x, int c, ll h) {
		H[u][0] += 1ll * c * S[u][0] + h * C[u][0];
		// 操作时旧的和加上历史和修改的和
		TH[u][0] += 1ll * T[u][0] * c + h;
		// 历史和修改的 tag 需要加上当前的最值 tag
		F[u][0] += x;
		T[u][0] += x;
		S[u][0] += 1ll * x * C[u][0];
		TC[u][0] += c; 
	}
	void push_min(int u, int x, int c, ll h) {
		H[u][1] += 1ll * c * S[u][1] + h * C[u][1];
		TH[u][1] += 1ll * T[u][1] * c + h;
		G[u][0] += x;
		T[u][1] += x;
		S[u][1] += 1ll * x * C[u][1];
		TC[u][1] += c; 
	}
	void pushdown(int u) {
		if(TC[u][0]) {
			int val = max(F[u << 1][0], F[u << 1 | 1][0]);
			// 判断对哪边有影响
			if(F[u << 1][0] == val) push_max(u << 1, T[u][0], TC[u][0], TH[u][0]);
			else push_max(u << 1, 0, TC[u][0], 0); // 注意没有影响也要更新操作次数，维护历史和
			if(F[u << 1 | 1][0] == val) push_max(u << 1 | 1, T[u][0], TC[u][0], TH[u][0]);
			else push_max(u << 1 | 1, 0, TC[u][0], 0);
			TH[u][0] = T[u][0] = TC[u][0] = 0;
		}
		if(TC[u][1]) {
			int val = min(G[u << 1][0], G[u << 1 | 1][0]);
			if(G[u << 1][0] == val) push_min(u << 1, T[u][1], TC[u][1], TH[u][1]);
			else push_min(u << 1, 0, TC[u][1], 0);
			if(G[u << 1 | 1][0] == val) push_min(u << 1 | 1, T[u][1], TC[u][1], TH[u][1]);
			else push_min(u << 1 | 1, 0, TC[u][1], 0);
			TH[u][1] = T[u][1] = TC[u][1] = 0;
		}
	}
	void build(int u, int l, int r) {
		le[u] = l, ri[u] = r;
		if(l == r) {
			F[u][0] = G[u][0] = S[u][0] = S[u][1] = a[l];
			F[u][1] = -INF, G[u][1] = INF;
			C[u][0] = C[u][1] = 1;
			return;
		}
		int mid = l + r >> 1;
		build(u << 1, l, mid);
		build(u << 1 | 1, mid + 1, r);
		pushup(u);
	}
	void modify_max(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r && F[u][0] <= x) { // 这里也要更新操作次数
			push_max(u, 0, 1, 0);
			return;
		}
		if(l <= le[u] && ri[u] <= r && F[u][1] < x && x < F[u][0]) { // 进行最值操作
			push_max(u, x - F[u][0], 1, x - F[u][0]);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify_max(u << 1, l, r, x);
		if(mid < r) modify_max(u << 1 | 1, l, r, x);
		pushup(u);
	}
	void modify_min(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r && G[u][0] >= x) {
			push_min(u, 0, 1, 0);
			return;
		}
		if(l <= le[u] && ri[u] <= r && G[u][1] > x && x > G[u][0]) {
			push_min(u, x - G[u][0], 1, x - G[u][0]);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify_min(u << 1, l, r, x);
		if(mid < r) modify_min(u << 1 | 1, l, r, x);
		pushup(u);
	}
	ll query_max(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return H[u][0];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(r <= mid) return query_max(u << 1, l, r);
		if(mid < l) return query_max(u << 1 | 1, l, r);
		return query_max(u << 1, l, r) + query_max(u << 1 | 1, l, r);
	}
	ll query_min(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return H[u][1];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(r <= mid) return query_min(u << 1, l, r);
		if(mid < l) return query_min(u << 1 | 1, l, r);
		return query_min(u << 1, l, r) + query_min(u << 1 | 1, l, r);
	}
} t;
void solve() {
	init();
	t.build(1, 1, n);
	cin >> m;
	FOR(i, 1, m) {
		int l1, r1, l2, r2;
		cin >> l1 >> r1 >> l2 >> r2;
		// 前缀拆分一下
		e[l2 - 1].push_back({l1, r1, i, -1});
		e[r2].push_back({l1, r1, i, 1});
	}
	FOR(i, 1, n) { // 扫描线
		t.modify_max(1, 1, i, a[i]); // 更新最值
		t.modify_min(1, 1, i, a[i]);
		for(auto h : e[i]) { // 查询历史和
			ans[h[2]] += h[3] * (t.query_min(1, h[0], h[1]) - t.query_max(1, h[0], h[1]));
		}
	}
	FOR(i, 1, m) cout << ans[i] << endl;
}
```
