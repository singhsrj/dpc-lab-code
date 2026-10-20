#include <mpi.h>
#include <iostream>
#include <random>
#include <chrono>
#include <thread>
#include <iomanip>

using namespace std;

int main() {
    MPI_Init(NULL, NULL);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0 || rank == 1) {
        int principal;
        char node_name;
        int partner_rank;
        
        if (rank == 0) {
            principal = 4321;
            node_name = 'A';
            partner_rank = 1;
        } else {
            principal = 8765;
            node_name = 'B';
            partner_rank = 0;
        }

        int years = 1;
        int total_days = years * 365;
        double amount = principal;

        mt19937 gen(principal);
        uniform_real_distribution<double> dist(0.001, 0.009);

        for (int i = 0; i < total_days; ++i) {
            double r = 0.07;
            double b = dist(gen);
            double rate_daily = (r + b) / 365.0;
            amount *= (1.0 + rate_daily);
            
            this_thread::sleep_for(chrono::milliseconds(1));
        }

        double partner_amount = 0.0;

        MPI_Send(&amount, 1, MPI_DOUBLE, partner_rank, 0, MPI_COMM_WORLD);
        MPI_Recv(&partner_amount, 1, MPI_DOUBLE, partner_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        double final_total = amount + partner_amount;

        cout << fixed << setprecision(2);
        cout << "Node " << node_name << " calculated its maturity as: " << amount << "\n";
        cout << "Node " << node_name << " consensus total: " << final_total << "\n";
    }

    MPI_Finalize();
    return 0;
}