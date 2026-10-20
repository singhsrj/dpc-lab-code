#include <stdio.h>
#include <omp.h>

#define N 100000

int main() {

    unsigned int A[N];

    // Initialize array
    for (int i = 0; i < N; i++) {
        A[i] = i + 1;
    }

    unsigned long long sum = 0;
    unsigned int maxVal = 0;
    unsigned int minVal = A[0];

    #pragma omp parallel sections
    {
        #pragma omp section
        {
            printf("Thread %d computing SUM\n", omp_get_thread_num());
            for (int i = 0; i < N; i++) {
                sum += A[i];
            }
        }

        #pragma omp section
        {
            printf("Thread %d computing MAX\n", omp_get_thread_num());
            unsigned int localMax = A[0];
            for (int i = 0; i < N; i++) {
                if (A[i] > localMax)
                    localMax = A[i];
            }
            maxVal = localMax;
        }

        #pragma omp section
        {
            printf("Thread %d computing MIN\n", omp_get_thread_num());
            unsigned int localMin = A[0];
            for (int i = 0; i < N; i++) {
                if (A[i] < localMin)
                    localMin = A[i];
            }
            minVal = localMin;
        }
    }

    printf("\nFinal Results:\n");
    printf("Sum = %llu\n", sum);
    printf("Max = %u\n", maxVal);
    printf("Min = %u\n", minVal);

    return 0;
}
