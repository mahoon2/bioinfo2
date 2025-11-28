#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> d, r, ret;

int solve(int y, int x)
{
    if(y == 0 || x == 0) return ret[y][x];
    if(ret[y][x] != -1) return ret[y][x];

    return ret[y][x] = max(solve(y-1, x) + d[y][x], solve(y, x-1) + r[y][x]);
}

int main(int argc, char *argv[])
{
    cin.tie(NULL); cout.tie(NULL); ios_base::sync_with_stdio(false);
    freopen("../test.in", "r", stdin);
    freopen("../test.out", "w", stdout);

    int n, m;
    cin >> n >> m;

    d = vector<vector<int>>(n + 1);
    for(auto& arr: d) {
        arr = vector<int>(m + 1);
    }

    r = vector<vector<int>>(n + 1);
    for(auto& arr: r) {
        arr = vector<int>(m + 1);
    }

    ret = vector<vector<int>>(n + 1);
    for(auto& arr: ret) {
        arr = vector<int>(m + 1, -1);
    }


    for(int i = 1; i < n + 1; i++) {
        for(int j = 0; j < m + 1; j++) {
            cin >> d[i][j];
        }
    }

    char c;
    cin >> c;

    for(int i = 0; i < n + 1; i++) {
        for(int j = 1; j < m + 1; j++) {
            cin >> r[i][j];
        }
    }


    ret[0][0] = 0;
    for(int i = 1; i < n + 1; i++) {
        ret[i][0] = ret[i-1][0] + d[i][0];
    }
    for(int j = 1; j < m + 1; j++) {
        ret[0][j] = ret[0][j-1] + r[0][j];
    }

    cout << solve(n, m) << '\n';

    return 0;
}