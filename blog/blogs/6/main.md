# P10639 BZOJ4695 最佳女选手

非常好 SgT Beats 使我线段树能力提升。

前置知识：[Segment Tree Beats P6242 【模板】线段树 3（区间最值操作、区间历史最值）](https://www.luogu.com.cn/problem/P6242)。

对于最值操作，很容易想到这个 Beats 来维护，然后这个有取大取小两种最值操作，那么就能想到这个同时记录线段树节点区间的最大最小，次大次小，最大值与最小值的出现次数，然后最值基本思路就是当操作的最值在当前区间的最大和次大值之间的时候进行处理，这样只会对最大值有操作，这样就会很方便，而且时间复杂度是 $O(n \log n)$ 的。

然后肯定会维护一个 tag 表示当前节点取最值操作的值，然后在打加法 tag 的时候，如果加上 $x$，同时最值 tag 也需要加上 $x$ 来保证正确性，然后 pushdown 的时候先处理加法然后处理最值即可保证正确。

然后就是最关键的部分！就是打取最小的最值 tag 的时候可能会影响另外一边的信息，这里需要特判。一共有两种情况：一种是这个区间就一种数，还有一种就是区间只有两种数，这种情况更新最值的之后同时也需要将另一边也进行更改，这里不难。

对于有两种最值操作和加操作的 Beats，时间复杂度可证明上界为 $O(n\log^2n)$，常数可能较大，本篇题解作者加上快读即可卡过。

具体可以看代码。

```cpp
const int N = 5e5 + 5;
const int INF = 2e9 + 5;
int n, m, a[N];
int read() {
	int res = 0, v = 1;
	char c = getchar();
	while(c < '0' || c > '9') { if(c == '-') v = -1; c = getchar();}
	while('0' <= c && c <= '9') res = res * 10 + c - '0', c = getchar();
	return res * v;
}
struct SgT {
	int le[N << 2], ri[N << 2];
	ll S[N << 2]; // 区间和
	int F[N << 2][2], G[N << 2][2], C[N << 2][2]; // 最大，次大，最大出现次数，以及最小等同理
	int T[N << 2], TV[N << 2][2]; // T 为加法 tag，TV 为两种最值 tag
	inline void pushup(int u) {
		S[u] = S[u << 1] + S[u << 1 | 1];
		F[u][0] = max(F[u << 1][0], F[u << 1 | 1][0]);
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
		G[u][0] = min(G[u << 1][0], G[u << 1 | 1][0]);
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
	inline void push_add(int u, int x) { // 加法 tag
		S[u] += 1ll * x * (ri[u] - le[u] + 1);
		F[u][0] += x;
		if(F[u][1] != -INF) F[u][1] += x;
		G[u][0] += x;
		if(G[u][1] != INF) G[u][1] += x;
		if(TV[u][0] != INF) TV[u][0] += x; // 这里最值 tag 也需要更改
		if(TV[u][1] != -INF) TV[u][1] += x;
		T[u] += x;
	}
	inline void push_max(int u, int x) { // 取最小最值 tag
		S[u] -= 1ll * (F[u][0] - x) * C[u][0];
		if(F[u][0] == G[u][1]) G[u][1] = x; // 只有两种数
		F[u][0] = x;
		TV[u][0] = x;
		if(F[u][1] == -INF) G[u][0] = x, TV[u][1] = -INF; // 只有一种数
	}
	inline void push_min(int u, int x) { // 同理
		S[u] += 1ll * (x - G[u][0]) * C[u][1];
		if(F[u][1] == G[u][0]) F[u][1] = x;
		G[u][0] = x;
		TV[u][1] = x;
		if(G[u][1] == INF) F[u][0] = x, TV[u][0] = INF;
	}
	inline void pushdown(int u) {
		if(T[u]) { // 先打加法 tag
			push_add(u << 1, T[u]);
			push_add(u << 1 | 1, T[u]);
			T[u] = 0;
		}
		if(TV[u][0] != INF) {
			int val = max(F[u << 1][0], F[u << 1 | 1][0]); // 需要判断往哪边下传
			if(F[u << 1][0] == val) push_max(u << 1, TV[u][0]);
			if(F[u << 1 | 1][0] == val) push_max(u << 1 | 1, TV[u][0]);
			TV[u][0] = INF;
		}
		if(TV[u][1] != -INF) {
			int val = min(G[u << 1][0], G[u << 1 | 1][0]);
			if(G[u << 1][0] == val) push_min(u << 1, TV[u][1]);
			if(G[u << 1 | 1][0] == val) push_min(u << 1 | 1, TV[u][1]);
			TV[u][1] = -INF;
		}
	}
	void build(int u, int l, int r) {
		le[u] = l, ri[u] = r;
		TV[u][0] = INF, TV[u][1] = -INF;
		if(l == r) {
			F[u][0] = G[u][0] = S[u] = a[l];
			F[u][1] = -INF, G[u][1] = INF;
			C[u][0] = C[u][1] = 1;
			return;
		}
		int mid = l + r >> 1;
		build(u << 1, l, mid);
		build(u << 1 | 1, mid + 1, r);
		pushup(u);
	}
	ll query_sum(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return S[u];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(r <= mid) return query_sum(u << 1, l, r);
		if(mid < l) return query_sum(u << 1 | 1, l, r);
		return query_sum(u << 1, l, r) + query_sum(u << 1 | 1, l, r);
	}
	int query_max(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return F[u][0];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(r <= mid) return query_max(u << 1, l, r);
		if(mid < l) return query_max(u << 1 | 1, l, r);
		return max(query_max(u << 1, l, r), query_max(u << 1 | 1, l, r));
	}
	int query_min(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return G[u][0];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(r <= mid) return query_min(u << 1, l, r);
		if(mid < l) return query_min(u << 1 | 1, l, r);
		return min(query_min(u << 1, l, r), query_min(u << 1 | 1, l, r));
	}
	void modify_add(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r) {
			push_add(u, x);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify_add(u << 1, l, r, x);
		if(mid < r) modify_add(u << 1 | 1, l, r, x);
		pushup(u);
	}
	void modify_max(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r && F[u][0] <= x) return;
		if(l <= le[u] && ri[u] <= r && F[u][1] < x && x < F[u][0]) { // 当修改的数小于最大值大于次大值时进行处理
			push_max(u, x);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify_max(u << 1, l, r, x);
		if(mid < r) modify_max(u << 1 | 1, l, r, x);
		pushup(u);
	}
	void modify_min(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r && G[u][0] >= x) return;
		if(l <= le[u] && ri[u] <= r && G[u][1] > x && x > G[u][0]) {
			push_min(u, x);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify_min(u << 1, l, r, x);
		if(mid < r) modify_min(u << 1 | 1, l, r, x);
		pushup(u);
	}
} t;
void solve() {
	n = read();
	FOR(i, 1, n) a[i] = read();
	t.build(1, 1, n);
	m = read();
	REP(_, m) {
		int opt;
		opt = read();
		if(opt == 1) {
			int l, r, x;
			l = read(); r = read(); x = read();
			t.modify_add(1, l, r, x);
		}
		if(opt == 2) {
			int l, r, x;
			l = read(); r = read(); x = read();
			t.modify_min(1, l, r, x);
		}
		if(opt == 3) {
			int l, r, x;
			l = read(); r = read(); x = read();
			t.modify_max(1, l, r, x);
		}
		if(opt == 4) {
			int l, r;
			l = read(); r = read();
			cout << t.query_sum(1, l, r) << endl;
		}
		if(opt == 5) {
			int l, r;
			l = read(); r = read();
			cout << t.query_max(1, l, r) << endl;
		}
		if(opt == 6) {
			int l, r;
			l = read(); r = read();
			cout << t.query_min(1, l, r) << endl;
		}
	}
}
```