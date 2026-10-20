#include <stdio.h>
#include <omp.h>

int main() {
    int i;
    int sum = 0;

    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Thread %d starting...\n", thread_id);
        // for(i = 1; i <= 10000; i++) {
        //     sum += i;
        //     printf("Thread %d adding %d\n", thread_id, i);
        // }
    }
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Thread %d starting...\n", thread_id);
        // for(i = 1; i <= 10000; i++) {
        //     sum += i;
        //     printf("Thread %d adding %d\n", thread_id, i);
        // }
    }
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Thread %d starting...\n", thread_id);
        // for(i = 1; i <= 10000; i++) {
        //     sum += i;
        //     printf("Thread %d adding %d\n", thread_id, i);
        // }
    }
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Thread %d starting...\n", thread_id);
        // for(i = 1; i <= 10000; i++) {
        //     sum += i;
        //     printf("Thread %d adding %d\n", thread_id, i);
        // }
    }
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Thread %d starting...\n", thread_id);
        // for(i = 1; i <= 10000; i++) {
        //     sum += i;
        //     printf("Thread %d adding %d\n", thread_id, i);
        // }
    }
    


    printf("Final Sum = %d\n", sum);
    return 0;
}