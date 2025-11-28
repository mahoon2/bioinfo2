#include <iostream>
#include <vector>
#include <algorithm>

#define vi vector<int>
#define pii pair<int,int>

using namespace std;

vector<vi> dp;
vector<vector<pii>> back;

void solve(string& seq1, string& seq2)
{
    for(int i = 1; i < seq1.size() + 1; i++) {
        for(int j = 1; j < seq2.size() + 1; j++) {
            dp[i][j] = max(
                dp[i-1][j] - 1,
                max(
                    dp[i][j-1] - 1,
                    dp[i-1][j-1] + (seq1[i-1] == seq2[j-1]? 1 : -1)
                )
            );

            if(dp[i][j] == dp[i-1][j] - 1) {
                back[i][j] = pii(i-1, j);
            } else if(dp[i][j] == dp[i][j-1] - 1) {
                back[i][j] = pii(i, j-1);
            } else {
                back[i][j] = pii(i-1, j-1);
            }
        }
    }
}

void backtrack(string& seq1, string& seq2)
{
    int starti, startj = seq2.size(), maxval = -987654321;
    for(int i = 0; i < seq1.size() + 1; i++) {
        if(maxval < dp[i][startj]) {
            maxval = dp[i][startj];
            starti = i;
        }
    }

    cout << dp[starti][startj] << '\n';
    int nexti, nextj;
    string out1, out2;

    while(startj > 0) {
        nexti = back[starti][startj].first;
        nextj = back[starti][startj].second;

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

    dp = vector<vector<int>> (seq1.size() + 1, vector<int>(seq2.size() + 1, 0));
    back = vector<vector<pii>> (seq1.size() + 1, vector<pii>(seq2.size() + 1));
    for(int j = 1; j < seq2.size() + 1; j++) {
        dp[0][j] = dp[0][j-1] - 1;
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