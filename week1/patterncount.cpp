#include <iostream>
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
    freopen("patterncount.out", "w", stdout);

    string text, pattern;
    cin >> text >> pattern;

    int patterni = 0;
    for(char& nt: pattern) {
        patterni = (patterni << 2) | nt_to_bit(nt);
    }

    int texti = 0;
    for(int i = 0; i < pattern.length() - 1; i++) {
        texti = (texti << 2) | nt_to_bit(text[i]);
    }

    int cnt = 0;
    int mask = (1 << (2 * pattern.length())) - 1;
    for(int i = pattern.length() - 1; i < text.length(); i++) {
        texti = (texti << 2) | nt_to_bit(text[i]);
        texti &= mask;

        if (texti == patterni) {
            cnt++;
        }
    }

    cout << cnt;

    return 0;
}