#include <iostream>
#include <vector>
#include <algorithm>

#define pii pair<int, int>

using namespace std;

vector<vector<pii>> adj;
vector<int> dp;
vector<int> last;

void dfs(int here)
{
    for(auto& next: adj[here]) {
        int there = next.first;
        int weight = next.second;

        if(dp[there] < dp[here] + weight) {
            dp[there] = dp[here] + weight;
            last[there] = here;
        }
        dfs(there);
    }
}

int main(int argc, char *argv[])
{
    cin.tie(NULL); cout.tie(NULL); ios_base::sync_with_stdio(false);
    freopen("../parsed.in", "r", stdin);
    freopen("../test.out", "w", stdout);

    int source, sink;
    cin >> source >> sink;

    adj = vector<vector<pii>>(100 + 1, vector<pii>());
    dp = vector<int>(100 + 1, -1);
    last = vector<int>(100 + 1, -1);

    int m, from, to, weight;
    cin >> m;
    for(int i = 0; i < m; i++) {
        cin >> from >> to >> weight;
        adj[from].push_back(pii(to, weight));
    }

    dp[source] = 0;
    dfs(source);

    cout << dp[sink] << '\n';

    vector<int> path;
    int here = sink;
    while(here != source) {
        path.push_back(here);
        here = last[here];
    }

    cout << source;
    for(auto here = path.rbegin(); here != path.rend(); here++) {
        cout << "->" << *here;
    }
    cout << '\n';

    return 0;
}