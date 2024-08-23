# P9989 [Ynoi Easy Round 2023] TEST_69 题解

首先观察一下性质，

一个数 $a_i$ 操作后一定是不增的，

每次操作要么不变，要么变成原来的数的约数，

所以一个数减小次数最多只有 $\log V$ 次。

按照 [P4145 上帝造题的七分钟 2 / 花神游历各国](https://www.luogu.com.cn/problem/P4145) 的思路，

用一颗线段树去维护，每次操作暴力递归到叶子节点更新，

同时到一个节点，如果当前操作对这个节点所代表的区间中的数没有变化，就直接跳过。

然后考虑什么时候没有变化，也就是在此节点代表的区间内的 $a_i$ 都是 $x$ 的约数，

也就是区间内所有 $a_i$ 的最小公倍数是 $x$ 的约数。

因此线段树维护总和于最小公倍数即可。

```cpp
const int N = 2e5 + 5;
const ll P = 1ll << 32;
int n, m;
ll a[N];
ll gcd(ll x, ll y) {
	if(!y) return x;
	return gcd(y, x % y);
}
ll lcm(ll x, ll y) {
	__int128 val = (__int128)x * y / gcd(x, y);
	return val > LNF ? LNF : val;
}
struct Sgt {
	ll f[N << 2], g[N << 2];
	int le[N << 2], ri[N << 2];
	void pushup(int u) {
		f[u] = (f[u << 1] + f[u << 1 | 1]) % P;
		g[u] = lcm(g[u << 1], g[u << 1 | 1]);
	}
	void build(int u, int l, int r) {
		le[u] = l; ri[u] = r;
		if(l == r) {
			f[u] = g[u] = a[l];
			return;
		}
		int mid = l + r >> 1;
		build(u << 1, l, mid);
		build(u << 1 | 1, mid + 1, r);
		pushup(u);
	}
	void modify(int u, int l, int r, ll x) {
		if(g[u] != LNF && x % g[u] == 0) return;
		if(le[u] == ri[u]) {
			ll val = f[u];
			val = gcd(val, x);
			f[u] = g[u] = val;
			return;
		}
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify(u << 1, l, r, x);
		if(mid < r) modify(u << 1 | 1, l, r, x);
		pushup(u);
	}
	ll query(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return f[u];
		}
		int mid = le[u] + ri[u] >> 1;
		ll res = 0;
		if(l <= mid) res += query(u << 1, l, r);
		if(mid < r) res += query(u << 1 | 1, l, r);
		res %= P;
		return res;
	}
} t;
void solve() {
	cin >> n >> m;
	FOR(i, 1, n) cin >> a[i];
	t.build(1, 1, n);
	REP(_, m) {
		int opt;
		cin >> opt;
		if(opt == 1) {
			int l, r; ll x;
			cin >> l >> r >> x;
			t.modify(1, l, r, x);
		}
		else {
			int l, r;
			cin >> l >> r;
			cout << t.query(1, l, r) << endl;
		}
	}
}
```