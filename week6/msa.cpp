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

vector<vector<vi>> dp;

int main(int argc, char *argv[])
{
    cin.tie(NULL); cout.tie(NULL); ios_base::sync_with_stdio(false);
    freopen("../test.in", "r", stdin);
    freopen("../test.out", "w", stdout);

    string seq1, seq2, seq3;
    cin >> seq1 >> seq2 >> seq3;

    dp = vector<vector<vi>> (sz(seq1) + 1, vector<vi>(sz(seq2) + 1, vi(sz(seq3) + 1, 0)));
    int match, previ, prevj, prevk;

    for(int i = 0; i < sz(seq1) + 1; i++) {
        previ = max(0, i - 1);

        for(int j = 0; j < sz(seq2) + 1; j++) {
            prevj = max(0, j - 1);

            for(int k = 0; k < sz(seq3) + 1; k++) {
                prevk = max(0, k - 1);
                match = 0;

                if(i != 0 && j != 0 && k != 0 && seq1[i - 1] == seq2[j - 1] && seq2[j - 1] == seq3[k - 1]) {
                    match = 1;
                }

                dp[i][j][k] = dp[previ][prevj][prevk] + match;
                dp[i][j][k] = max(dp[i][j][k], dp[previ][j][k]);
                dp[i][j][k] = max(dp[i][j][k], dp[i][prevj][k]);
                dp[i][j][k] = max(dp[i][j][k], dp[i][j][prevk]);

                dp[i][j][k] = max(dp[i][j][k], dp[previ][prevj][k]);
                dp[i][j][k] = max(dp[i][j][k], dp[i][prevj][prevk]);
                dp[i][j][k] = max(dp[i][j][k], dp[previ][j][prevk]);
            }
        }
    }

    int i = sz(seq1);
    int j = sz(seq2);
    int k = sz(seq3);

    string out1, out2, out3;
    cout << dp[i][j][k] << '\n';
    while(i > 0 && j > 0 && k > 0) {
        if(dp[i - 1][j - 1][k - 1] + 1 == dp[i][j][k] && seq1[i - 1] == seq2[j - 1] && seq2[j - 1] == seq3[k - 1]) {
            out1 += seq1[i - 1];
            out2 += seq2[j - 1];
            out3 += seq3[k - 1];
            i--; j--; k--;
        } else {
            previ = max(0, i - 1);
            prevj = max(0, j - 1);
            prevk = max(0, k - 1);

            if(dp[i][j][k] == dp[previ][j][k]) {
                out1 += seq1[i - 1];
                out2 += '-';
                out3 += '-';
                i--;
            } else if(dp[i][j][k] == dp[i][prevj][k]) {
                out1 += '-';
                out2 += seq2[j-1];
                out3 += '-';
                j--;
            } else if(dp[i][j][k] == dp[i][j][prevk]) {
                out1 += '-';
                out2 += '-';
                out3 += seq3[k-1];
                k--;
            } else if(dp[i][j][k] == dp[previ][prevj][k]) {
                out1 += seq1[i - 1];
                out2 += seq2[j - 1];
                out3 += '-';
                i--; j--;
            } else if(dp[i][j][k] == dp[i][prevj][prevk]) {
                out1 += '-';
                out2 += seq2[j - 1];
                out3 += seq3[k - 1];
                j--; k--;
            } else if(dp[i][j][k] == dp[previ][j][prevk]) {
                out1 += seq1[i - 1];
                out2 += '-';
                out3 += seq3[k - 1];
                i--; k--;
            }
        }
    }

    int left = max(max(i, j), k);

    int templeft = left - i;
    for(; i > 0; i--) {
        out1 += seq1[i - 1];
    }
    for(; templeft > 0; templeft--) {
        out1 += '-';
    }

    templeft = left - j;
    for(; j > 0; j--) {
        out2 += seq2[j - 1];
    }
    for(; templeft > 0; templeft--) {
        out2 += '-';
    }

    templeft = left - k;
    for(; k > 0; k--) {
        out3 += seq3[k - 1];
    }
    for(; templeft > 0; templeft--) {
        out3 += '-';
    }

    for(auto iter = out1.rbegin(); iter != out1.rend(); iter++) {
        cout << *iter;
    }
    cout << '\n';

    for(auto iter = out2.rbegin(); iter != out2.rend(); iter++) {
        cout << *iter;
    }
    cout << '\n';

    for(auto iter = out3.rbegin(); iter != out3.rend(); iter++) {
        cout << *iter;
    }
    cout << '\n';

    return 0;
}