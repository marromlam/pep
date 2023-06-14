void parallel_quicksort( T* first, T* last ) {
    tbb::task_group g;
    while( last-first>QUICKSORT_CUTOFF ) {
        // Divide
        T* middle = divide(first,last);
        if( !middle ) {
            g.wait();
            return;
        }

        // Now have two subproblems: [first..middle) and [middle+1..last)

            // Left problem (first..middle) is smaller, so spawn it.

            // Solve right subproblem in next iteration.

        } else {
            // Right problem (middle..last) is smaller, so spawn it.

            // Solve left subproblem in next iteration.
        }
    }
    // Base case
    std::sort(first,last);
    g.wait();
 }
