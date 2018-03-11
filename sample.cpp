#include <bits/stdc++.h>
using namespace std;

int main(void) {
    int H, W, D;
    cin >> H >> W >> D;

    vector<int> f_x((H + 1) * (W + 1));
    vector<int> f_y((H + 1) * (W + 1));

    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; j++) {
            int num;
            cin >> num;
            f_x[num] = i + 1;
            f_y[num] = j + 1;
        }
    }

    int Q;
    cin >> Q;

    vector<int> VL(Q);
    vector<int> VR(Q);
    for (int i = 0; i < Q; i++) {
        cin >> VL[i] >> VR[i];
    }
    for (int i = 0; i < Q; i++) {
        int L = VL[i], R = VR[i], sum = 0;
        while(L != R) {
            int _L = L + D;
            sum += abs(f_x[_L] - f_x[L]) + abs(f_y[_L] - f_y[L]);
            L += D;
        }
        cout << sum << endl;
    }

    return 0;
}