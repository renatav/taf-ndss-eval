# Performance Artifacts

This section evaluates TAF’s repository validation performance across multiple representative partners. The goal is to measure how efficiently TAF processes and verifies large versioned legal repositories under realistic conditions.  

We focus exclusively on validation performance, excluding clone times, since cloning is primarily dependent on external factors such as network throughput and local disk performance, which vary significantly between machines.  

Each test case profiles the execution of `taf repo validate` under controlled conditions. The profiling data is collected using Python’s `cProfile` and analyzed through custom scripts that extract cumulative runtime for the core updater routine (`run_tuf_updater`). These measurements provide a direct indication of TAF's internal efficiency during repository validation.

Due to underlying differences in the `pygit2` library, TAF exhibits different runtime characteristics on Windows versus Unix-based systems. To ensure reproducibility, we provide both `*-windows.prof` and `*-unix.prof` baseline profiles. Users may compare their local results against the corresponding reference for their operating system.  

Please note that performance will naturally vary with hardware specifications (CPU, disk speed, etc.). Our provided numbers serve as indicative baselines rather than fixed benchmarks.

## Running the Performance Evaluation

1. Navigate to the `./performance` directory.  
2. Run the following command:

   ```bash
   python -m run.py
   ```

3. The script will:

   - Execute taf repo validate under profiling for several sample partner repositories.
   - Collect .prof files containing detailed timing statistics.
   - Extract cumulative times for TAF’s updater routine.
   - Compare results against provided baseline profiles (*-unix.prof or *-windows.prof).
   - Output total validation time, difference, and per-commit performance insights.

The results summarize how each partner repository performs relative to the baseline, allowing evaluators to observe scaling behavior and performance consistency across jurisdictions.
