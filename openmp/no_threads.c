#include <stdio.h>
#include <omp.h>
int main() {
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();        // thread ID
        int total = omp_get_num_threads();     // total threads
        printf("Hello from thread %d out of %d\n", tid, total);
    }
    return 0;
}