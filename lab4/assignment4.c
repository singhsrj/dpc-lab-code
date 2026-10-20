#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define N 12

int is_sorted(int arr[], int n) {
    for (int i = 1; i < n; i++)
        if (arr[i - 1] > arr[i])
            return 0;
    return 1;
}

/* Windows-safe shuffle (no rand_r) */
void shuffle(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        int j = rand() % n;
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void copy_array(int src[], int dest[], int n) {
    for (int i = 0; i < n; i++)
        dest[i] = src[i];
}

void print_array(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {

    int original[N];
    int result[N];

    
    for (int i = 0; i < N; i++)
        original[i] = i + 1;

    // Shuffle initial array 
    srand((unsigned int)time(NULL));
    for (int i = 0; i < N; i++) {
        int j = rand() % N;
        int temp = original[i];
        original[i] = original[j];
        original[j] = temp;
    }

    printf("Original Array: ");
    print_array(original, N);


    int seq_arr[N];
    copy_array(original, seq_arr, N);

    long long seq_shuffles = 0;

    double start = omp_get_wtime();

    while (!is_sorted(seq_arr, N)) {
        shuffle(seq_arr, N);
        seq_shuffles++;
    }

    double seq_time = omp_get_wtime() - start;

    printf("\nSequential Run:\n");
    printf("Sorted Array: ");
    print_array(seq_arr, N);
    printf("Time Taken: %.4f sec\n", seq_time);
    printf("Total Shuffles: %lld\n", seq_shuffles);

    /* ================= PARALLEL ================= */

    int thread_counts[] = {2, 4, 8};

    printf("\nSummary Table:\n");
    printf("Threads\tTime(sec)\tShuffles\tSpeedup\n");

    for (int t = 0; t < 3; t++) {

        int T = thread_counts[t];
        int found = 0;
        long long total_shuffles = 0;

        start = omp_get_wtime();

        #pragma omp parallel num_threads(T) shared(found, result, total_shuffles)
        {
            int local[N];
            copy_array(original, local, N);

            long long local_shuffles = 0;

            /* Unique seed per thread */
            srand((unsigned int)time(NULL) + omp_get_thread_num());

            while (!found) {

                shuffle(local, N);
                local_shuffles++;

                if (is_sorted(local, N)) {

                    #pragma omp critical
                    {
                        if (!found) {
                            copy_array(local, result, N);
                            found = 1;
                            printf("Thread %d found the sorted array!\n",
                                   omp_get_thread_num());
                        }
                    }
                }
            }

            #pragma omp atomic
            total_shuffles += local_shuffles;
        }

        double par_time = omp_get_wtime() - start;

        printf("%d\t%.4f\t\t%lld\t\t%.2f\n",
               T,
               par_time,
               total_shuffles,
               seq_time / par_time);
    }

    printf("\nFinal Sorted Array: ");
    print_array(result, N);

    return 0;
}
