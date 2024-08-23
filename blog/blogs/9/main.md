# CSP2024模拟测试十 C - Talulah

## 简要题意
给出长度为 $n$ 的排列 $a$，定义集合 $S_i = \left \\{ x \mid \max_{j=i}^{x}a_j=a_x \right \\} $。   
对于 $q$ 个询问，给出 $l$ 和 $r$，求出 $\sum_{l\le x,y\le r}|S_x\cup S_y|$。  
$n,q \le 2.5 \times 10^5$。

## 题解
考虑这个集合是什么，发现是从右往左，依次加入一个递增单调栈，集合即为此时单调栈的状态。  
然后考虑并集不是很好求，考虑容斥后求交集。不难发现两单调栈集合的并即为最长公共后缀。  
转化这个问题，发现若把单调栈持久化一下，所有单调栈就会构成一颗树，一个点到根的路径即为当前的单调栈。  
然后最长公共后缀就变为了最近公共祖先 lca。然后比较套路，因为两个点必须在不同子树，直接总子树减同子树容斥。  
但是不难发现对于 $v\in son(u)$，$u$ 子树加上了 $d_u$ 的贡献，$v$ 子树减掉上了 $d_u$ 的贡献，  
然后在统计 $v$ 的贡献时，$v$ 子树又要加上 $d_v$ 的贡献，总贡献等于 $d_v-d_u=1$。  
每个点的子树大小即为该点前面的可选点，这样就和树没有关系了，再用一个单调栈求出。  
然后统计贡献，可以转化成一个二维数点问题，一个点对对应了坐标系的一个点，  
这样两个都在 $[l,r]$ 的点代表了一个 $(l,r,l,r)$ 的矩形，加贡献相当于矩形加，同样的询问相当于矩形查询。  


### 实现
对于静态的矩形加和矩形求和，考虑扫描线维护历史和线段树。  

具体的，对于 $y$ 轴做扫描线，那么对于修改操作，就需要在 $l_2$ 时刻在线段树上 $[l_1,r_1]$ 加上 $x$，在 $r_2+1$ 时刻就在 $[l_1,r_1]$ 减去 $x$。   
然后对于查询操作，把查询按照 $y$ 轴拆成两前缀相减，相当于 $r_2$ 时刻的 $[l_1,r_1]$ 历史和减去 $l_2-1$ 时刻的。

然后是历史和线段树。考虑维护区间和 $F$ 的同时，维护当前的区间历史和 $H$。  
然后除了区间加的 tag $T$ 外，还需要历史区间加的 tag $TH$ 与上次下传操作的时间差 tag $TC$。  
然后考虑如和下传：  
设下传的三个 tag 依次是 $x,h,c$。  
对于区间和，直接对于 $F$ 加上 $x\cdot len$，$T$ 加上 $x$，然后时间差也很简单，$TC$ 直接加上 $c$。  
然后是复杂的历史信息：  
对于历史和 tag $TH$，其有 $c$ 的时间还是用了旧区间和 tag $T$，所以加上 $c \cdot T$，然后再加上新 tag $h$。  
对于区间历史和 $H$，先加上 $c$ 时间用的旧区间和 $F$，即加上 $c \cdot F \cdot$，然后加上新值 $h\cdot len$。  
然后注意一下信息更新的顺序，一定是历史和先更新。

时间复杂度 $O(n \log n)$。

<div class="alert alert-info" role="alert">
(The sky blue) でも君の笑顔も <br>
(Archive) 砂の一粒さえ <br>
何ひとつ失いたくないんだ <br>
それがそれ全部が <br>
私たちの青春だから <br>
誰にも渡さない <br>
さあ一緒に帰ろう
</div>

```cpp
const int N = 2.5e5 + 5;
int I, n, q, a[N], stk[N], tp;
int nxt[N], d[N], sz[N], f[N];
ll s[N], ans[N];
vector<array<int, 3>> e[N];
vector<array<int, 4>> qs[N];
struct SgT {
	int le[N << 2], ri[N << 2];
	ll F[N << 2], H[N << 2];
	ll T[N << 2], TH[N << 2], TC[N << 2];
	void pushup(int u) {
		F[u] = F[u << 1] + F[u << 1 | 1];
		H[u] = H[u << 1] + H[u << 1 | 1];
	}
	void push(int u, ll x, ll h, ll c) {
		H[u] += F[u] * c + (ri[u] - le[u] + 1) * h;
		F[u] += (ri[u] - le[u] + 1) * x;
		TH[u] += h + T[u] * c;
		T[u] += x;
		TC[u] += c;
	}
	void pushdown(int u) {
		if(T[u] || TH[u] || TC[u]) {
			push(u << 1, T[u], TH[u], TC[u]);
			push(u << 1 | 1, T[u], TH[u], TC[u]);
			T[u] = TH[u] = TC[u] = 0;
		}
	}
	void build(int u, int l, int r) {
		le[u] = l, ri[u] = r;
		if(l == r) {
			return;
		}
		int mid = le[u] + ri[u] >> 1;
		build(u << 1, l, mid);
		build(u << 1 | 1, mid + 1, r);
	}
	void modify(int u, int l, int r, int x) {
		if(l <= le[u] && ri[u] <= r) {
			push(u, x, 0, 0);
			return;
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		if(l <= mid) modify(u << 1, l, r, x);
		if(mid < r) modify(u << 1 | 1, l, r, x);
		pushup(u);
	}
	ll query(int u, int l, int r) {
		if(l <= le[u] && ri[u] <= r) {
			return H[u];
		}
		pushdown(u);
		int mid = le[u] + ri[u] >> 1;
		ll res = 0;
		if(l <= mid) res += query(u << 1, l, r);
		if(mid < r) res += query(u << 1 | 1, l, r);
		return res;
	}
} t;
void solve() {
	cin >> n >> q >> I;
	FOR(i, 1, n) cin >> a[i];
	tp = 0; stk[tp] = 0;
	FOR(i, 1, n) {
		while(tp && a[stk[tp]] < a[i]) tp--;
		sz[i] = i - stk[tp];
		stk[++tp] = i;
	}
	tp = 0; stk[tp] = 0;
	ROF(i, n, 1) {
		while(tp && a[stk[tp]] < a[i]) tp--;
		stk[++tp] = i;
		d[i] = tp;
	}
	FOR(i, 1, n) s[i] = s[i - 1] + d[i];
	FOR(u, 1, n) {
		int l = u - sz[u] + 1; 
		e[l].push_back({l, u, 1});
		e[u + 1].push_back({l, u, -1});
	}
	FOR(i, 1, q) {
		int l, r;
		cin >> l >> r;
		ans[i] = 2 * (s[r] - s[l - 1]) * (r - l + 1);
		qs[l - 1].push_back({l, r, i, -1});
		qs[r].push_back({l, r, i, 1});
	}
	t.build(1, 1, n);
	FOR(i, 0, n) {
		for(auto h : e[i]) 
			t.modify(1, h[0], h[1], h[2]);
		t.push(1, 0, 0, 1);
		for(auto h : qs[i]) 
			ans[h[2]] -= h[3] * t.query(1, h[0], h[1]);
	}
	FOR(i, 1, q) cout << ans[i] << endl;
}
```