#include <iostream>
#include <vector>

using namespace std;

int dp[100000];
vector<int> coins;

int solve(int money)
{
    if(dp[money] != -1) return dp[money];

    int ret = 987654321;
    for(auto &c: coins) {
        int left = money - c;
        if(left >= 0) {
            ret = min(ret, solve(left) + 1);
        }
    }

    return dp[money] = ret;
}

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    freopen("../test.in", "r", stdin);
    freopen("mincoin.out", "w", stdout);

    int money, c;
    cin >> money >> c;

    for(int i = 0; i <= money; i++) {
        dp[i] = -1;
    }

    dp[0] = 0;
    coins = vector<int>(c);
    for(auto &coin: coins) {
        cin >> coin;
        dp[coin] = 1;
    }

    cout << solve(money) << '\n';

    return 0;
}