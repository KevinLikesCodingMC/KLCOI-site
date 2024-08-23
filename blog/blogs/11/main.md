# 2024“钉耙编程”中国大学生算法设计超级联赛三 E - 数论

非常简单的一道题

## 题意

## 题解


时间复杂度 $O(n \log n \log V)$

```cpp
const int P = 998244353;
typedef Modint<P> mint;
const int N = 1e5 + 5;
const int M = 1e5 * 20 + 5;
int n, a[N];
int gcd(int x, int y) {
	if(!y) return x;
	return gcd(y, x % y);
}
int lg[N], g[N][20];
void build() {
	FOR(i, 2, n) lg[i] = lg[i >> 1] + 1;
	FOR(i, 1, n) g[i][0] = a[i];
	FOR(j, 1, lg[n]) {
		FOR(i, 1, n - (1 << j) + 1) {
			g[i][j] = gcd(g[i][j - 1], g[i + (1 << j - 1)][j - 1]);
		}
	}
}
int query(int l, int r) {
	int len = lg[r - l + 1];
	return gcd(g[l][len], g[r - (1 << len) + 1][len]);
}
struct Node {
	int i; mint x, s;
};
vector<Node> s[M][2];
unordered_map<int, int> mp; int tot;
unordered_set<int> S[N];
int get(int val) {
	if(mp.count(val)) return mp[val];
	mp[val] = ++tot;
	s[tot][0].push_back({0, 1, 1});
	s[tot][1].push_back({n + 1, 1, 1});
	return tot;
}
Node getl(int u, int p) {
	int L = 0, R = SZ(s[u][0]) - 1, res = 0;
	while(L <= R) {
		int mid = L + R >> 1;
		if(s[u][0][mid].i <= p) {
			res = mid;
			L = mid + 1;
		}
		else {
			R = mid - 1;
		}
	}
	return s[u][0][res];
}
Node getr(int u, int p) {
	int L = 0, R = SZ(s[u][1]) - 1, res = 0;
	while(L <= R) {
		int mid = L + R >> 1;
		if(p <= s[u][1][mid].i) {
			res = mid;
			L = mid + 1;
		}
		else {
			R = mid - 1;
		}
	}
	return s[u][1][res];
}
mint ssuml(int u, int p) {
	if(p < 0) return 0;
	auto h = getl(u, p);
	return h.s + h.x * (p - h.i);
}
mint suml(int u, int p) {
	if(p < 0) return 0;
	auto h = getl(u, p);
	return h.x;
}
mint ssumr(int u, int p) {
	if(p > n + 1) return 0;
	auto h = getr(u, p);
	return h.s + h.x * (h.i - p);
}
mint sumr(int u, int p) {
	if(p > n + 1) return 0;
	auto h = getr(u, p);
	return h.x;
}
void insertl(int u, int i, mint x) {
	auto h = s[u][0].back();
	int len = i - h.i - 1;
	s[u][0].push_back({i, h.x + x, h.s + h.x + x + h.x * len});
}
void insertr(int u, int i, mint x) {
	auto h = s[u][1].back();
	int len = h.i - i - 1;
	s[u][1].push_back({i, h.x + x, h.s + h.x + x + h.x * len});
}
struct SgT {
	int le[N << 2], ri[N << 2];
	unordered_set<int> e[N << 2];
	void build(int u, int l, int r) {
		le[u] = l, ri[u] = r;
		if(l == r) {
			return;
		}
		int mid = l + r >> 1;
		build(u << 1, l, mid);
		build(u << 1 | 1, mid + 1, r);
	}
	void modify(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r) {
			e[u].insert(x);
			return;
		}
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify(u << 1, l, r, x);
		if(mid < r) modify(u << 1 | 1, l, r, x);
	}
	void query(int u, int p) {
		for(int x : e[u]) S[p].insert(x);
		if(le[u] == ri[u]) {
			return;
		}
		int mid = le[u] + ri[u] >> 1;
		if(p <= mid) query(u << 1, p);
		else query(u << 1 | 1, p);
	}
} t;
void solve() {
	cin >> n;
	FOR(i, 1, n) cin >> a[i];
	build();
	t.build(1, 1, n);
	FOR(i, 1, n) {
		int r = i;
		while(r) {
			int val = query(r, i);
			int L = 1, R = r, l = r;
			while(L <= R) {
				int mid = L + R >> 1;
				if(query(mid, i) == val) {
					l = mid;
					R = mid - 1;
				}
				else {
					L = mid + 1;
				}
			}
			int u = get(val);
			mint sum = ssuml(u, r - 1) - ssuml(u, l - 2);
			insertl(u, i, sum);
			t.modify(1, l, i, val);
			r = l - 1;
		}
	}
	ROF(i, n, 1) {
		int r = i;
		while(r <= n) {
			int val = query(i, r);
			int L = r, R = n, l = r;
			while(L <= R) {
				int mid = L + R >> 1;
				if(query(i, mid) == val) {
					l = mid;
					L = mid + 1;
				}
				else {
					R = mid - 1;
				}
			}
			int u = get(val);
			mint sum = ssumr(u, r + 1) - ssumr(u, l + 2);
			insertr(u, i, sum);
			t.modify(1, i, r, val);
			r = l + 1;
		}
	}
	FOR(i, 1, n) t.query(1, i);
	FOR(i, 1, n) {
		mint ans = 0;
		for(int x : S[i]) {
			int u = get(x);
			ans += suml(u, n);
			ans -= suml(u, i - 1) * sumr(u, i + 1);
		}
		cout << ans << " ";
	}
	cout << endl;
}
```
