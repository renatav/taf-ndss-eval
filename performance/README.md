# Performance Artifacts

This section evaluates TAF’s repository validation performance across multiple representative partners. The goal is to measure how efficiently TAF processes and verifies large, versioned legal repositories under realistic conditions.

In practice, TAF’s updater is used to securely clone and update repositories, as well as to validate local repositories when needed. Since cloning speed depends on network conditions and is not a reliable benchmark, this evaluation focuses on validating local repositories, which does not require network access.

The test setup begins by cloning the repositories without running validation. After cloning, the repositories are reset to the exact  states used during our original evaluation. This ensures consistency, as the source repositories are active production repositories and may change over time.

 Validation is then executed and profiled using Python’s `cProfile`, with analysis performed by custom scripts that extract cumulative runtime for the core updater routine (`run_tuf_updater`). These measurements provide a direct indication of TAF’s internal efficiency during validation.

Performance naturally varies based on hardware (e.g., CPU, disk speed), so the results should be viewed as indicative baselines, not fixed benchmarks. Additionally, due to implementation differences in the `pygit2` library, TAF exhibits different runtime characteristics on Windows and Unix-based systems. It is also well known that Git operations are slower on Windows. To ensure reproducibility, we provide both `*-windows.prof` and `*-unix.prof` baseline profiles so users can compare their local results against the appropriate reference.ofiles. Users may compare their local results against the corresponding reference for their operating system. Is it known that git is slower on Windows.

## Running the Performance Evaluation

1. Navigate to the `./performance` directory.  
2. Run the following command:

   ```bash
   python -m run.py
   ```

3. The script will:

   - Execute taf repo validate under profiling for several sample partner repositories.
   - Collect `.prof` files containing detailed timing statistics.
   - Extract cumulative times for TAF’s updater routine.
   - Compare results against provided baseline profiles (`*-unix.prof` or `*-windows.prof`).
   - Output total validation time, difference, and per-commit performance insights.

The results summarize how each partner repository performs relative to the baseline.
The tests were conducted on a machine more powerful than an average laptop, so slower performance should be expected on less capable hardware.
