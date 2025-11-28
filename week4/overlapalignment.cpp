#include <iostream>
#include <vector>
#include <algorithm>

using ll = long long;
using ld = long double;
using namespace std;

#define INF 987654321
#define vi vector<int>
#define pii pair<int,int>
#define fi first
#define se second
#define pb push_back
#define eb emplace_back
#define all(v) (v).begin(), (v).end()
#define sz(v) ((int)v.size())
#define rep(i, n) for(int i=0; i<(n); i++)
#define rrep(i, n) for(int i=1; i<=(n); i++)

int n, m;
int match = 1;
int penalty = -2;
vector<vi> dp;
vector<vector<pii>> back;

void solve(string& seq1, string& seq2)
{
    for(int i = 1; i < n + 1; i++) {
        for(int j = 1; j < m + 1; j++) {
            dp[i][j] = max(
                dp[i-1][j] + penalty,
                max(
                    dp[i][j-1] + penalty,
                    dp[i-1][j-1] + (seq1[i-1] == seq2[j-1]? match : penalty)
                )
            );

            if(dp[i][j] == dp[i-1][j] + penalty) {
                back[i][j] = pii(i-1, j);
            } else if(dp[i][j] == dp[i][j-1] + penalty) {
                back[i][j] = pii(i, j-1);
            } else {
                back[i][j] = pii(i-1, j-1);
            }
        }
    }
}

void backtrack(string& seq1, string& seq2)
{
    int starti = n, startj, maxval = -INF;
    for(int j = 1; j < m + 1; j++) {
        if(maxval < dp[starti][j]) {
            maxval = dp[starti][j];
            startj = j;
        }
    }

    cout << dp[starti][startj] << '\n';
    int nexti, nextj;
    string out1, out2;

    while(startj > 0) {
        nexti = back[starti][startj].fi;
        nextj = back[starti][startj].se;

        if(nexti != starti && nextj != startj) {
            out1 += seq1[nexti];
            out2 += seq2[nextj];
        } else if(nexti != starti) {
            out1 += seq1[nexti];
            out2 += '-';
        } else {
            out1 += '-';
            out2 += seq2[nextj];
        }

        starti = nexti;
        startj = nextj;
    }

    for(auto iter = out1.rbegin(); iter != out1.rend(); iter++) {
        cout << *iter;
    }
    cout << '\n';
    for(auto iter = out2.rbegin(); iter != out2.rend(); iter++) {
        cout << *iter;
    }
}

int main(int argc, char *argv[])
{
    cin.tie(NULL); cout.tie(NULL); ios_base::sync_with_stdio(false);
    freopen("../test.in", "r", stdin);
    freopen("../test.out", "w", stdout);

    string seq1, seq2;
    cin >> seq1 >> seq2;
    n = sz(seq1);
    m = sz(seq2);
    dp = vector<vector<int>> (n + 1, vector<int>(m + 1, 0));
    back = vector<vector<pii>> (n + 1, vector<pii>(m + 1));
    for(int j = 1; j < m + 1; j++) {
        dp[0][j] = dp[0][j-1] + penalty;
    }

#ifdef DEBUG
    cout << '\t';
    for(auto& j: seq2) {
        cout << '\t' << j;
    }
    cout << '\n';
#endif

    solve(seq1, seq2);

#ifdef DEBUG
    for(int i = 0; i < seq1.size() + 1; i++) {
        if(i != 0) {
            cout << seq1[i-1];
        }
        cout << '\t';

        for(int j = 0; j < seq2.size() + 1; j++) {
            cout << dp[i][j] << '\t';
        }
        cout << '\n';
    }
#endif

    backtrack(seq1, seq2);

    return 0;
}