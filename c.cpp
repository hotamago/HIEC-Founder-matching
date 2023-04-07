// Hoang Son WIBU lolicon codeforces rate 1834 khong cay
#include <bits/stdc++.h>
//#pragma GCC optimize("Ofast")
//#pragma GCC target("popcnt")
//#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
#define F first
#define S second
#define times double stime = clock();
#define gettime cout << "\nTime executed: " << (clock() - stime) / CLOCKS_PER_SEC * 1000 << "ms.\n";
#define M_PI 3.14159265358979323846
#define int long long

using namespace std;
typedef long long ll;
typedef unsigned int ui;
typedef unsigned long long ull;
typedef double dou;
typedef pair<int, int> pii;
typedef pair<pair<int, int>, int> ppiii;
typedef vector<int> vi;
typedef vector<vi> vvi;

ll mod = 998244353ll;
const int ooii = 0x7f7f7f7f;
const ll ooll = 0x7f7f7f7f7f7f7f7f;
// const double epsilon = 1e-8;
// 1000000007ll 998244353ll
bool debug_on = true, debug_test = false;

struct lineinfo {
    int id = -1;
    int time = 0;
    int num_left = 0;
    multiset<int> label;
    multiset<int> label_op;
    lineinfo(int id, int time, int num_left){
        this->id = id;
        this->time = time;
        this->num_left = num_left;
        this->label = multiset<int>();
        this->label_op = multiset<int>();
    }
};
struct user: public lineinfo{
    user(int id, int time, int num_left): lineinfo(id, time, num_left){
    }
};
struct team: lineinfo{
    team(int id, int time, int num_left): lineinfo(id, time, num_left){
    }
};

vector<user> users;
vector<team> teams;

struct edge {
    int point;
    int time_t, time_u;
    team *t = NULL;
    user *u = NULL;
    edge(team *t, user *u){
        this->point = 0;
        this->t = t;
        this->u = u;

        time_t = t->time;
        time_u = u->time;

        { // +2 team match
            bool ok = false;
            for(auto it = t->label_op.begin(); it != t->label_op.end(); it++){
                int val = *it;
                if(u->label.find(val) != u->label.end()){
                    ok = true;
                    break;
                }
            }
            if(ok){
                this->point += 2;
            }
        }
        { // +1 team match
            bool ok = false;
            for(auto it = u->label_op.begin(); it != u->label_op.end(); it++){
                int val = *it;
                if(t->label.find(val) != t->label.end()){
                    ok = true;
                    break;
                }
            }
            if(ok){
                this->point += 1;
            }
        }
    }
};

bool compareEdge(const edge &a, const edge &b)
{
    if (a.point != b.point)
        return a.point > b.point;
    if (a.time_t != b.time_t)
        return a.time_t < b.time_t;
    return a.time_u < b.time_u;
}

vector<edge> edges;
set<int> delNodes;
set<pii> delEdges;

void input_label(lineinfo &newLineinfo){
    { // Label
        int m;
        cin >> m;
        for(int j = 1, u; j<=m; j++){
            cin >> u;
            newLineinfo.label.insert(u);
        }
    }
    { // Label op
        int m;
        cin >> m;
        for(int j = 1, u; j<=m; j++){
            cin >> u;
            newLineinfo.label_op.insert(u);
        }
    }
}

vector<pii> result;
int32_t process()
{
    // srand(time(NULL));
    int tcase = 1;
    // cin >> tcase;
    for (int ttcase = 1; ttcase <= tcase; ttcase++)
    {
      { // User
        int n;
        cin >> n;
        for(int i = 1, id, time, num_left; i<=n; i++){
            cin >> id >> time;
            cin >> num_left;
            user newUser = user(id, time, num_left);
            input_label(newUser);
            users.push_back(newUser);
        }
      }
      { // Team
        int n;
        cin >> n;
        for(int i = 1, id, time, num_left; i<=n; i++){
            cin >> id >> time;
            cin >> num_left;
            team newTeam = team(id, time, num_left);
            input_label(newTeam);
            teams.push_back(newTeam);
        }
      }
      { // Del node
        int n;
        cin >> n;
        for(int i = 1, u; i<=n; i++){
            cin >> u;
            delNodes.insert(u);
        }
      }
      { // Del edge
        int n;
        cin >> n;
        for(int i = 1, u, v; i<=n; i++){
            cin >> u >> v;
            delEdges.insert({u, v});
        }
      }
      { // Preprocess
        for(team &t: teams){
            for(user &u: users){
                edges.push_back(edge(&t, &u));
            }
        }
        sort(edges.begin(), edges.end(), compareEdge);
      }
      { // Process
        for(edge &ed: edges){
            if(ed.point == 0 || ed.t->num_left == 0 || ed.u->num_left == 0) continue;
            if(delNodes.find(ed.t->id) != delNodes.end() || delNodes.find(ed.u->id) != delNodes.end()) continue;
            if(delEdges.find({ed.t->id, ed.u->id}) != delEdges.end()) continue;

            bool ok = false;
            for(auto it = ed.t->label_op.begin(); it != ed.t->label_op.end(); it++) {
                int val = *it;
                if(ed.u->label.find(val) != ed.u->label.end()){
                    ok = true;
                    ed.t->label_op.erase(it);
                    break;
                }
            }
            if(ok){
                ed.t->num_left -= 1;
                ed.u->num_left -= 1;
                result.push_back({ed.t->id, ed.u->id});
            }
        }
      }
      { // Print result
        for(pii &ed: result){
            cout << ed.F << " " << ed.S << "\n";
        }
      }
    }
    // system("pause");
    return 0;
}

//-----------------------------------------------//
//                       Main                    //
//-----------------------------------------------//
// 2 is standard input
// 0, 1 is file input
int online = 0;
int32_t main()
{
    // ios::sync_with_stdio(0);
    // cin.tie(0);
    if (online == 0)
    {
        freopen("temp.inp", "r", stdin);
        freopen("temp.out", "w", stdout);
    }
    else if (online == 1)
    {
        freopen("dothi.txt", "r", stdin);
        freopen("dothitomau.dot", "w", stdout);
    }
    // times
    int error = process();
    // gettime
    return error;
}
