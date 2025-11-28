#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

inline int nt_to_bit(char nt)
{
    switch(nt)
    {
    case 'A': return 0;
    case 'C': return 1;
    case 'G': return 2;
    case 'T': return 3;
    }

    return -1;
}

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    freopen(argv[1], "r", stdin);
    freopen("motifenum.out", "w", stdout);

    int k, d;
    cin >> k >> d;

    string text;
    vector<string> texts;
    while(cin >> text) {
        texts.push_back(text);
    }



    return 0;
}