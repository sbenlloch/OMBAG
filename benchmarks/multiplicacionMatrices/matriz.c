#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define min(a, b) ((a) < (b) ? (a) : (b))

const size_t side = 200;

#ifndef __MATRIX__
#define __MATRIX__

#include <stdlib.h>

struct _matrix_;
typedef struct _matrix_ *matrix_t;

matrix_t new_random_matrix(size_t side);

void print_matrix(const matrix_t matrix);

void mm_mult_naive(matrix_t result,
                   const matrix_t left_source,
                   const matrix_t right_source);

void mm_mult_blocked(matrix_t result,
                     const matrix_t left_source,
                     const matrix_t right_source);

void mm_mult_rm_cm(matrix_t result,
                   const matrix_t left_source,
                   const matrix_t right_source);

void mm_mult_blocked_rm_cm(matrix_t result,
                           const matrix_t left_source,
                           const matrix_t right_source);
void mm_mult_blocked_rm_cm_vec(matrix_t result,
                               const matrix_t left_source,
                               const matrix_t right_source);
void mm_mult_blocked_rm_cm_vec_parallel(matrix_t result,
                                        const matrix_t left_source,
                                        const matrix_t right_source);

void free_matrix(matrix_t matrix);

#endif

struct _matrix_
{
    size_t side;
    float *elements;
};

const size_t size_matrix = sizeof(struct _matrix_);

matrix_t new_random_matrix(size_t side)
{
    matrix_t matrix = (matrix_t)malloc(size_matrix);
    matrix->side = side;
    matrix->elements = (float *)malloc(side * side * sizeof(float));
    for (size_t i = 0; i < side * side; i++)
        matrix->elements[i] = 2 * drand48() - 1;
    return matrix;
}

void print_matrix(const matrix_t matrix)
{
    for (size_t row = 0; row < matrix->side; row++)
    {
        for (size_t column = 0; column < matrix->side; column++)
            printf("%7.5f ",
                   matrix->elements[row * matrix->side + column]);
        printf("\n");
    }
}

void mm_mult_naive(matrix_t result,
                   const matrix_t left_source,
                   const matrix_t right_source)
{
    const size_t side = result->side;
    for (size_t i = 0; i < side; i++)
        for (size_t j = 0; j < side; j++)
        {
            float acc = 0.0;
            for (size_t k = 0; k < side; k++)
                acc += left_source->elements[i * side + k] *
                       right_source->elements[k * side + j];
            result->elements[i * side + j] = acc;
        }
}

void mm_mult_blocked(matrix_t result,
                     const matrix_t left_source,
                     const matrix_t right_source)
{
    const size_t side = result->side;
    const size_t block_side = 16;
    const size_t blocks_per_side = (side + side % block_side) / block_side;
    float *res = result->elements;
    const float *lso = left_source->elements;
    const float *rso = right_source->elements;
    for (size_t block_i = 0;
         block_i < blocks_per_side;
         block_i++)
    {
        const size_t i_start = block_i * block_side;
        const size_t i_stop = min((block_i + 1) * block_side, side);
        for (size_t block_j = 0;
             block_j < blocks_per_side;
             block_j++)
        {
            const size_t j_start = block_j * block_side;
            const size_t j_stop =
                min((block_j + 1) * block_side, side);
            for (size_t block_k = 0;
                 block_k < blocks_per_side;
                 block_k++)
            {
                const size_t k_start = block_k * block_side;
                const size_t k_stop =
                    min((block_k + 1) * block_side,
                        side);
                for (size_t i = i_start;
                     i < i_stop;
                     i++)
                    for (size_t j = j_start;
                         j < j_stop;
                         j++)
                    {
                        float acc = res[i * side + j];
                        for (size_t k = k_start;
                             k < k_stop;
                             k++)
                            acc += lso[i * side + k] *
                                   rso[k * side + j];
                        res[i * side + j] = acc;
                    }
            }
        }
    }
}

void mm_mult_rm_cm(matrix_t result,
                   const matrix_t left_source,
                   const matrix_t right_source)
{
    const size_t side = result->side;
    for (size_t i = 0; i < side; i++)
        for (size_t j = 0; j < side; j++)
        {
            float acc = 0.0;
            for (size_t k = 0; k < side; k++)
                acc += left_source->elements[i * side + k] *
                       right_source->elements[j * side + k];
            result->elements[i * side + j] = acc;
        }
}

void mm_mult_blocked_rm_cm(matrix_t result,
                           const matrix_t left_source,
                           const matrix_t right_source)
{
    const size_t side = result->side;
    const size_t block_side = 16;
    const size_t blocks_per_side = (side + side % block_side) / block_side;
    float *res = result->elements;
    const float *lso = left_source->elements;
    const float *rso = right_source->elements;
    for (size_t block_i = 0;
         block_i < blocks_per_side;
         block_i++)
    {
        const size_t i_start = block_i * block_side;
        const size_t i_stop = min((block_i + 1) * block_side, side);
        for (size_t block_j = 0;
             block_j < blocks_per_side;
             block_j++)
        {
            const size_t j_start = block_j * block_side;
            const size_t j_stop =
                min((block_j + 1) * block_side, side);
            for (size_t block_k = 0;
                 block_k < blocks_per_side;
                 block_k++)
            {
                const size_t k_start = block_k * block_side;
                const size_t k_stop =
                    min((block_k + 1) * block_side,
                        side);
                for (size_t i = i_start;
                     i < i_stop;
                     i++)
                    for (size_t j = j_start;
                         j < j_stop;
                         j++)
                    {
                        float acc = res[i * side + j];
                        for (size_t k = k_start;
                             k < k_stop;
                             k++)
                            acc += lso[i * side + k] *
                                   rso[j * side + k];
                        res[i * side + j] = acc;
                    }
            }
        }
    }
}

typedef float vec4 __attribute__((vector_size(16)));

void mm_mult_blocked_rm_cm_vec(matrix_t result,
                               const matrix_t left_source,
                               const matrix_t right_source)
{
    const size_t side = result->side;
    const size_t block_side = 16;
    const size_t blocks_per_side = (side + side % block_side) / block_side;
    float *res = result->elements;
    const float *lso = left_source->elements;
    const float *rso = right_source->elements;
    for (size_t block_i = 0;
         block_i < blocks_per_side;
         block_i++)
    {
        const size_t i_start = block_i * block_side;
        const size_t i_stop = min((block_i + 1) * block_side, side);
        for (size_t block_j = 0;
             block_j < blocks_per_side;
             block_j++)
        {
            const size_t j_start = block_j * block_side;
            const size_t j_stop =
                min((block_j + 1) * block_side, side);
            for (size_t block_k = 0;
                 block_k < blocks_per_side;
                 block_k++)
            {
                const size_t k_start = block_k * block_side;
                const size_t k_stop =
                    min((block_k + 1) * block_side,
                        side);
                for (size_t i = i_start;
                     i < i_stop;
                     i++)
                    for (size_t j = j_start;
                         j < j_stop;
                         j++)
                    {
                        vec4 accv = {0.0, 0.0, 0.0, 0.0};
                        const float *lpso = lso + i * side +
                                            k_start;
                        const vec4 *lvso =
                            (vec4 *)(lpso);
                        const float *rpso =
                            rso + j * side +
                            k_start;
                        const vec4 *rvso =
                            (vec4 *)(rpso);
                        size_t num_k =
                            (k_stop - k_start);
                        size_t num_vk = num_k / 4;
                        for (size_t k = 0;
                             k < num_vk;
                             k++)
                            accv += lvso[k] *
                                    rvso[k];
                        float acc = accv[0] +
                                    accv[1] +
                                    accv[2] +
                                    accv[3];
                        for (size_t k = num_vk * 4;
                             k < num_k;
                             k++)
                            acc += lpso[k] + rpso[k];
                        res[i * side + j] += acc;
                    }
            }
        }
    }
}

void free_matrix(matrix_t matrix)
{
    free(matrix->elements);
    free(matrix);
}

typedef void (*mm_mult_t)(matrix_t result,
                          const matrix_t left_source,
                          const matrix_t right_source);
void time_mm_mult(mm_mult_t multiplication,
                  matrix_t result,
                  matrix_t left_source,
                  matrix_t right_source,
                  size_t num_tests);

int main()
{
    srand48(time(0));
    matrix_t A = new_random_matrix(side);
    matrix_t B = new_random_matrix(side);
    matrix_t C = new_random_matrix(side);
    printf("Naive matrix matrix multiplication\n");
    time_mm_mult(mm_mult_naive, C, A, B, 1);
    printf("Blocked matrix matrix multiplication\n");
    time_mm_mult(mm_mult_blocked, C, A, B, 1);
    printf("Row major column major matrix multiplication\n");
    time_mm_mult(mm_mult_rm_cm, C, A, B, 1);
    printf("Blocked row major column major matrix matrix multiplication\n");
    time_mm_mult(mm_mult_blocked_rm_cm, C, A, B, 1);
    printf("Blocked vectorized row major column major matrix matrix multiplication\n");
    time_mm_mult(mm_mult_blocked_rm_cm_vec, C, A, B, 1);
    free_matrix(A);
    free_matrix(B);
    free_matrix(C);
    return EXIT_SUCCESS;
}

void time_mm_mult(mm_mult_t multiplication,
                  matrix_t result,
                  matrix_t left_source,
                  matrix_t right_source,
                  size_t num_tests)
{
    for (size_t i = 0; i < num_tests; i++)
    {
        printf("Test %lu:", i + 1);
        fflush(stdout);
        struct timespec t_start, t_end;
        clock_gettime(CLOCK_REALTIME, &t_start);
        multiplication(result, left_source, right_source);
        clock_gettime(CLOCK_REALTIME, &t_end);
        double elapsed_time =
            (t_end.tv_sec - t_start.tv_sec) * 1e6 +
            (t_end.tv_nsec - t_start.tv_nsec) * 1e-3;
        printf(" %10.3lf µs\n", elapsed_time);
    }
}