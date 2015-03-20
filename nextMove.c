// This file depends on there being 5 ships to a board

// USAGE:
// <progname> <num_correct_guesses> [<correct_1> ...] <num_incorrect_guesses> [<incorrect_1> ...]
// This program brute-forces a board sufficiently close to being solved; takes time if there aren't many incorrect guesses
//
// Also, please compile it with the following command: gcc -o nextMove nextMove.c

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 100
#define ROWS 10
#define COLS 10

int illegal(int *known, int ship, int direction, int length) {
    if (direction == 1) {
        if (ship/COLS + length > ROWS) {
            return 1;
        }
    }
    if (direction == 0) {
        if (ship%COLS + length > COLS) {
            return 1;
        }
    }
    return conflict(known, ship, direction, length);
}

int conflict(int *known, int ship, int direction, int length) {
    int i;
    if (direction == 0) {
        for (i = 0; i < length; ++i) {
            if (known[ship + i] == 1) {
                return 1;
            }
        }
    }
    if (direction == 1) {
        for (i = 0; i < length; ++i) {
            if (known[ship + COLS*i] == 1) {
                return 1;
            }
        }
    }
    return 0;
}

int collision(int ship1, int ship1D, int l1, int ship2, int ship2D, int l2) {
    if (ship1 == ship2)
        return 1;
    if (ship1D == 0 && ship2D == 0 && ship1/COLS == ship2/COLS) {
        if (ship1 < ship2 && ship1 + l1 > ship2)
            return 1;
        if (ship1 > ship2 && ship2 + l2 > ship1)
            return 1;
        return 0;
    }
    if (ship1D == 0 && ship2D == 1) {
        if (ship1%COLS <= ship2%COLS && ship1%COLS + l1 > ship2%COLS && ship2/COLS <= ship1/COLS && ship2/COLS + l2 > ship1/COLS)
            return 1;
        return 0;
    }
    if (ship1D == 1 && ship2D == 0) {
        if (ship2%COLS <= ship1%COLS && ship2%COLS + l2 > ship1%COLS && ship1/COLS <= ship2/COLS && ship1/COLS + l1 > ship2/COLS)
            return 1;
        return 0;
    }
    if (ship1D == 1 && ship2D == 1 && ship1%COLS == ship2%COLS) {
        if (ship1/COLS < ship2/COLS && ship1/COLS + l1 > ship2/COLS)
            return 1;
        if (ship1/COLS > ship2/COLS && ship2/COLS + l2 > ship1/COLS)
            return 1;
    }
    return 0;
}

int requirements_met(int *known, int number, int *positions, int *directions, int *lengths) {
    int i, j;
    for (i = 0; i < SIZE; ++i) {
        if (*(known+i) == 2) {
            int found = 0;
            for (j = 0; j < number; ++j) {
                if (collision(*(positions+j), *(directions+j), *(lengths+j), i, 0, 1)) {
                    found = 1;
                    break;
                }
            }
            if (!found) {
                return 0;
            }
        }
    }
    return 1;
}

void increment(int *known, long *array, int ship, int direction, int length) {
    int c;
    if (direction == 0) {
        for (c = 0; c < length; ++c) {
            if (*(known + ship + c) == 0) {
                *(array + ship + c) += 1;
            }
        }
    }
    if (direction == 1) {
        for (c = 0; c < length; ++c) {
            if (*(known + ship + COLS*c) == 0) {
                *(array + ship + COLS*c) += 1;
            }
        }
    }
}

void recordStats(char **args, int *known) {
    int i;
    int right = atoi(*(args + 1));
    for (i = 0; i < right; ++i) {
        int index = atoi(*(args + 1+ i + 1));
        *(known+index) = 2;
    }
    int wrong = atoi(*(args + 1 + right + 1));
    for (i = 0; i < wrong; ++i) {
        int index = atoi(*(args + 1 + right + 1 + i + 1));
        *(known+index) = 1;
    }
    return;
}

int main(int argc, char *argv[]) {
    long total = 0;
    long count[SIZE];
    int *known = (int*)calloc(SIZE, sizeof(int));
    int i, j;
    recordStats(argv, known);
    for (i=0; i<SIZE; ++i)
        count[i] = 0;
    int ships[5];
    int directions[5];
    int lengths[5] = {5, 4, 3, 3, 2};
    for (ships[0] = 0; ships[0] < SIZE; ++ships[0]) {
    for (directions[0] = 0; directions[0] < 2; ++directions[0]) {
        if (illegal(known, ships[0], directions[0], lengths[0]))
            continue;
        for (ships[1] = 0; ships[1] < SIZE; ++ships[1]) {
        for (directions[1] = 0; directions[1] < 2; ++directions[1]) {
            if (illegal(known, ships[1], directions[1], lengths[1]))
                continue;
            if (collision(ships[0], directions[0], lengths[0], ships[1], directions[1], lengths[1]))
                continue;
            for (ships[2] = 0; ships[2] < SIZE; ++ships[2]) {
            for (directions[2] = 0; directions[2] < 2; ++directions[2]) {
                if (illegal(known, ships[2], directions[2], lengths[2]))
                    continue;
                if (collision(ships[0], directions[0], lengths[0], ships[2], directions[2], lengths[2]) ||
                    collision(ships[1], directions[1], lengths[0], ships[2], directions[2], lengths[2]))
                    continue;
                for (ships[3] = 0; ships[3] < SIZE; ++ships[3]) {
                for (directions[3] = 0; directions[3] < 2; ++directions[3]) {
                    if (illegal(known, ships[3], directions[3], lengths[3]))
                        continue;
                    if (collision(ships[0], directions[0], lengths[0], ships[3], directions[3], lengths[3]) ||
                        collision(ships[1], directions[1], lengths[1], ships[3], directions[3], lengths[3]) ||
                        collision(ships[2], directions[2], lengths[2], ships[3], directions[3], lengths[3]))
                        continue;
                    for (ships[4] = 0; ships[4] < SIZE; ++ships[4]) {
                    for (directions[4] = 0; directions[4] < 2; ++directions[4]) {
                        if (illegal(known, ships[4], directions[4], lengths[4]))
                            continue;
                        if (collision(ships[0], directions[0], lengths[0], ships[4], directions[4], lengths[4]) ||
                            collision(ships[1], directions[1], lengths[1], ships[4], directions[4], lengths[4]) ||
                            collision(ships[2], directions[2], lengths[2], ships[4], directions[4], lengths[4]) ||
                            collision(ships[3], directions[3], lengths[3], ships[4], directions[4], lengths[4]))
                            continue;
                        if (!requirements_met(known, 5, ships, directions, lengths)) {
                            continue;
                        }
                        increment(known, count, ships[4], directions[4], lengths[4]);
                        increment(known, count, ships[3], directions[3], lengths[3]);
                        increment(known, count, ships[2], directions[2], lengths[2]);
                        increment(known, count, ships[1], directions[1], lengths[1]);
                        increment(known, count, ships[0], directions[0], lengths[0]);
                        ++total;
                    }
                    }
                }
                }
            }
            }
        }
        }
    }
    }
    free( (void*) known);
    int max_index = 0;
    for (i = 1; i < SIZE; ++i) {
        if (count[i] > count[max_index]) {
            max_index = i;
        }
    }
    return max_index;
}
