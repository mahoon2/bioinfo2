#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

vector<vector<int>> dp;

int main(int argc, char *argv[])
{
    cin.tie(NULL); cout.tie(NULL); ios_base::sync_with_stdio(false);
    freopen("../test.in", "r", stdin);
    freopen("../test.out", "w", stdout);

    string a, b;
    cin >> a >> b;

    int n, m;
    n = a.length();
    m = b.length();

    dp = vector<vector<int>>(n + 1);
    for(auto& arr: dp) {
        arr = vector<int>(m + 1);
    }

    for(int i = 1; i < n + 1; i++) {
        for(int j = 1; j < m + 1; j++) {
            if(a[i-1] == b[j-1]) dp[i][j] = dp[i-1][j-1] + 1;
            else dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
        }
    }

    cout << dp[n][m] << '\n';

    int i = n;
    int j = m;
    while(i > 0 && j > 0) {
        if(a[i-1] == b[j-1]) {
            cout << a[i-1];
            i--;
            j--;
        } else {
            if(dp[i][j] == dp[i-1][j]) {
                i--;
            } else {
                j--;
            }
        }
    }

    cout << '\n';

    return 0;
}