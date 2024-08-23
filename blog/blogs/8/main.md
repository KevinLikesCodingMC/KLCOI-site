# CSP2024模拟测试八 D - plane

## 简要题意
在坐标系中有一矩形，矩形中有 $n$ 条平行于 $x$ 轴或 $y$ 轴的线段，会对矩形进行分割，求矩形分割后的连通块个数。  
$n \le 2 \times 10 ^ 5$。
## 题解
考虑从下到上扫描线，考虑竖线和横线，而竖线需要拆成插入竖线和删除竖线。  
不难发现，若只有竖线的插入和删除，块会一直连通，而时刻块劈开的方法只有插入横线。  
若用平衡树维护插入的竖线，这样就能维护出一些段，然后对于横线就新增并查集，然后在竖线插入和删除时维护并查集合并。  
这样就能过掉大部分联通块数量有限的点。  
但是可以构造出一个网格，使得新增的并查集过多。  
不难发现这个网格的大部分并查集都没有用到，考虑懒惰新增并查集，被迫新增并查集的数量只有 $O(n)$，  
这样就可以在平衡树上打 tag，表示有多少新的但没动过的并查集，然后加入横线时直接查询即可。

Treap 的具体实现就是在 split 和 merge 的时候都 pushdown 一下，pushdown 时若当前节点有 tag，那么下传并清空 tag，然后新增并查集节点即可。

时间复杂度 $O(n\log n)$。

<div class="alert alert-success" role="alert">
世界中の記憶がいつか <br>
砂のように消えてしまっても <br>
空と海と風と君がそこにあれば <br>
青春は終わんない <br>
守るべき理由はいつも単純明快 <br>
この場所が私たちの <br>
決して手放したくない <br>
お金じゃ買えやしない <br>
たったひとつの居場所だから
</div>

```cpp
const int N = 4e5 + 50;
const int M = 1e7 + 50;
const int INF = 1e9 + 7;
int n, h, w, m;
struct Node {
	int o, x, l, r;
	bool operator < (const Node &A) const {
		if(x == A.x) return o < A.o;
		return x < A.x;
	}
} a[N];
int f[M], cnt;
int find(int u) {
	if(f[u] == u) return u;
	return f[u] = find(f[u]);
}
int add() {
	cnt++;
	f[cnt] = cnt;
	return cnt;
}
void mrg(int u, int v) {
	u = find(u); v = find(v);
	if(u != v) f[u] = v;
}
mt19937 rng(time(0));
int rt, tot, ls[N], rs[N], sz[N], vl[N], id[N], F[N];
uint rnd[N];
bool t[N];
ll ans;
void pushup(int u) {
	sz[u] = sz[ls[u]] + sz[rs[u]] + 1;
	F[u] = F[ls[u]] + F[rs[u]];
}
void push(int u) {
	if(u) {
		F[u] = sz[u];
		t[u] = 1;
	}
}
void pushdown(int u) {
	if(t[u]) {
		push(ls[u]);
		push(rs[u]);
		F[u]--;
		id[u] = add();
		t[u] = 0;
	}
}
void split(int u, int p, int &x, int &y) {
	if(!u) {
		x = y = 0;
		return;
	}
	pushdown(u);
	if(vl[u] <= p) {
		x = u;
		split(rs[u], p, rs[u], y);
	}
	else {
		y = u;
		split(ls[u], p, x, ls[u]);
	}
	pushup(u);
}
int merge(int u, int v) {
	if(!u || !v) return u | v;
	pushdown(u);
	pushdown(v);
	if(rnd[u] > rnd[v]) {
		rs[u] = merge(rs[u], v);
		pushup(u);
		return u;
	}
	else {
		ls[v] = merge(u, ls[v]);
		pushup(v);
		return v;
	}
}
int nxt(int u) {
	while(rs[u]) u = rs[u];
	return u;
}
void insert(int p) {
	int x, y;
	split(rt, p, x, y);
	int u = nxt(x);
	tot++;
	vl[tot] = p;
	id[tot] = id[u];
	sz[tot] = 1;
	rt = merge(merge(x, tot), y);
}
void modify(int l, int r) {
	int x, y, z;
	split(rt, l - 1, x, y);
	split(y, r, y, z);
	if(!y) {
		rt = merge(x, z);
		return;
	}
	int u = nxt(y);
	split(y, vl[u] - 1, y, u);
	if(!y) {
		rt = merge(merge(x, u), z);
		return;
	}
	ans += F[y];
	push(y);
	rt = merge(merge(x, merge(y, u)), z);
}
void del(int p) {
	int x, y, z;
	split(rt, p - 1, x, y);
	split(y, p, y, z);
	int u = nxt(x);
	mrg(id[u], id[y]);
	rt = merge(x, z);
}
void solve() {
	cin >> n >> w >> h;
	REP(i, n) rnd[i] = rng();
	FOR(i, 1, n) {
		int x1, y1, x2, y2;
		cin >> x1 >> y1 >> x2 >> y2;
		if(x1 == x2) {
			if(y1 > y2) swap(y1, y2);
			a[++m] = {1, y1, x1, 0};
			a[++m] = {3, y2, x1, 0};
		}
		else {
			if(x1 > x2) swap(x1, x2);
			a[++m] = {2, y1, x1, x2};
		}
	}
	a[++m] = {2, 0, 0, w};
	a[++m] = {2, h, 0, w};
	a[++m] = {1, 0, 0, 0};
	a[++m] = {1, 0, w, 0};
	a[++m] = {3, h, 0, 0};
	a[++m] = {3, h, w, 0};
	sort(a + 1, a + m + 1);
	rt = tot = 1;
	vl[1] = -INF;
	id[1] = add();
	sz[1] = 1;  
	FOR(i, 1, m) {
		if(a[i].o == 1) insert(a[i].l);
		if(a[i].o == 2) modify(a[i].l, a[i].r);
		if(a[i].o == 3) del(a[i].l);
	}
	FOR(i, 1, cnt) if(find(i) == i) ans++;
	cout << ans - 1 << endl;
}
```