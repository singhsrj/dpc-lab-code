#include <stdio.h>
#include <omp.h>

#define N 100000

int main() {

    unsigned int v[N];

    // Initialize array
    for (int i = 0; i < N; i++) {
        v[i] = i + 1;
    }

    unsigned long long evenSum = 0;
    unsigned long long oddSum = 0;

    printf("---- Incorrect Version (Race Condition) ----\n");

    evenSum = 0;
    oddSum = 0;

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        if (v[i] % 2 == 0)
            evenSum += v[i];   // Race condition
        else
            oddSum += v[i];    // Race condition
    }

    printf("Even Sum = %llu\n", evenSum);
    printf("Odd Sum = %llu\n", oddSum);

    printf("\n---- Correct Version (Using Atomic) ----\n");

    evenSum = 0;
    oddSum = 0;

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        if (v[i] % 2 == 0) {
            #pragma omp atomic
            evenSum += v[i];
        } else {
            #pragma omp atomic
            oddSum += v[i];
        }
    }

    printf("Even Sum = %llu\n", evenSum);
    printf("Odd Sum = %llu\n", oddSum);

    return 0;
}
