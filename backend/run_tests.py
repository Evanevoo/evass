import os
import sys
import subprocess
import argparse
import time
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_test_history():
    history_file = Path(__file__).parent / "test_logs" / "test_history.json"
    if history_file.exists():
        with open(history_file, "r") as f:
            return json.load(f)
    return {"runs": [], "stats": defaultdict(int)}

def save_test_history(history):
    history_file = Path(__file__).parent / "test_logs" / "test_history.json"
    history_file.parent.mkdir(exist_ok=True)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

def generate_summary(history):
    if not history["runs"]:
        return "No test history available"
    
    summary = ["\nTest Run Summary:"]
    summary.append("-" * 50)
    
    # Overall stats
    total_runs = len(history["runs"])
    successful_runs = sum(1 for run in history["runs"] if run["status"] == "success")
    success_rate = (successful_runs / total_runs) * 100 if total_runs > 0 else 0
    
    summary.append(f"Total Runs: {total_runs}")
    summary.append(f"Success Rate: {success_rate:.1f}%")
    summary.append(f"Total Tests Run: {history['stats']['total_tests']}")
    summary.append(f"Failed Tests: {history['stats']['failed_tests']}")
    
    # Recent runs
    summary.append("\nRecent Runs:")
    for run in history["runs"][-5:]:
        status = "✅" if run["status"] == "success" else "❌"
        summary.append(
            f"{status} {run['timestamp']}: {run['duration']:.1f}s - "
            f"{run['tests_passed']}/{run['total_tests']} passed"
        )
    
    return "\n".join(summary)

def generate_html_report(history, output_dir="test_reports"):
    """Generate an HTML report from test history."""
    report_dir = Path(__file__).parent / output_dir
    report_dir.mkdir(exist_ok=True)
    
    html_content = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>Test Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 20px; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "th { background-color: #f2f2f2; }",
        "tr:nth-child(even) { background-color: #f9f9f9; }",
        ".success { color: green; }",
        ".failure { color: red; }",
        ".chart { margin: 20px; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Test Report</h1>",
        "<h2>Summary</h2>",
        "<table>",
        "<tr><th>Total Runs</th><td>{}</td></tr>".format(len(history["runs"])),
        "<tr><th>Success Rate</th><td>{:.1f}%</td></tr>".format(
            (sum(1 for run in history["runs"] if run["status"] == "success") / len(history["runs"])) * 100
        ),
        "<tr><th>Total Tests</th><td>{}</td></tr>".format(history["stats"]["total_tests"]),
        "<tr><th>Failed Tests</th><td>{}</td></tr>".format(history["stats"]["failed_tests"]),
        "</table>",
        "<h2>Recent Runs</h2>",
        "<table>",
        "<tr><th>Timestamp</th><th>Status</th><th>Duration</th><th>Tests</th><th>Log File</th></tr>"
    ]
    
    for run in history["runs"][-10:]:
        status_class = "success" if run["status"] == "success" else "failure"
        html_content.append(
            "<tr>"
            f"<td>{run['timestamp']}</td>"
            f"<td class='{status_class}'>{run['status']}</td>"
            f"<td>{run['duration']:.1f}s</td>"
            f"<td>{run['tests_passed']}/{run['total_tests']}</td>"
            f"<td><a href='{run['log_file']}'>View Log</a></td>"
            "</tr>"
        )
    
    html_content.extend([
        "</table>",
        "</body>",
        "</html>"
    ])
    
    report_file = report_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_file, "w") as f:
        f.write("\n".join(html_content))
    
    return report_file

def load_test_config():
    """Load test configuration from YAML file."""
    config_file = Path(__file__).parent / "test_config.yaml"
    if config_file.exists():
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    return {
        "environment": {
            "database": "sqlite:///:memory:",
            "log_level": "INFO"
        },
        "dependencies": {
            "required": [],
            "optional": []
        },
        "test_data": {
            "fixtures": [],
            "seed_data": []
        }
    }

def check_dependencies(dependencies):
    """Check if required dependencies are installed."""
    missing_deps = []
    for dep in dependencies.get("required", []):
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)

def setup_test_environment(config):
    """Set up test environment based on configuration."""
    # Set environment variables
    for key, value in config.get("environment", {}).items():
        os.environ[f"TEST_{key.upper()}"] = str(value)
    
    # Create test data directories
    data_dir = Path(__file__).parent / "test_data"
    data_dir.mkdir(exist_ok=True)
    
    # Load test fixtures
    for fixture in config.get("test_data", {}).get("fixtures", []):
        fixture_path = data_dir / fixture
        if not fixture_path.exists():
            print(f"Warning: Test fixture {fixture} not found")
    
    # Load seed data
    for seed_file in config.get("test_data", {}).get("seed_data", []):
        seed_path = data_dir / seed_file
        if not seed_path.exists():
            print(f"Warning: Seed data file {seed_file} not found")

def run_tests(test_path=None, coverage=False, html_report=False, parallel=False, 
             failfast=False, markers=None, verbose=1, timeout=None, retries=0,
             cache_results=False, profile=False, slow_threshold=None, generate_report=False,
             config_file=None, skip_deps=False):
    """
    Run tests with optional coverage reporting and additional features.
    
    Args:
        test_path (str, optional): Specific test file or directory to run
        coverage (bool): Whether to run with coverage
        html_report (bool): Whether to generate HTML coverage report
        parallel (bool): Whether to run tests in parallel
        failfast (bool): Stop on first failure
        markers (str): pytest markers to run
        verbose (int): Verbosity level (0-2)
        timeout (int): Test timeout in seconds
        retries (int): Number of retries for failed tests
        cache_results (bool): Whether to cache test results
        profile (bool): Whether to profile test execution
        slow_threshold (float): Threshold for slow tests in seconds
        generate_report (bool): Whether to generate HTML report
        config_file (str): Path to test configuration file
        skip_deps (bool): Skip dependency checking
    """
    # Load test configuration
    config = load_test_config()
    if config_file:
        with open(config_file, "r") as f:
            config.update(yaml.safe_load(f))
    
    # Check dependencies
    if not skip_deps:
        check_dependencies(config.get("dependencies", {}))
    
    # Set up test environment
    setup_test_environment(config)
    
    # Get the backend directory path
    backend_dir = Path(__file__).parent
    
    # Load test history if caching
    history = load_test_history() if cache_results else {"runs": [], "stats": defaultdict(int)}
    
    # Construct the pytest command
    cmd = ["pytest"]
    
    # Add coverage options
    if coverage:
        cmd.extend([
            "--cov=.",
            "--cov-report=term",
            "--cov-config=.coveragerc"
        ])
        if html_report:
            cmd.append("--cov-report=html")
    
    # Add parallel testing
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add failfast
    if failfast:
        cmd.append("-x")
    
    # Add markers
    if markers:
        cmd.extend(["-m", markers])
    
    # Add verbosity
    if verbose == 0:
        cmd.append("-q")
    elif verbose == 2:
        cmd.append("-vv")
    
    # Add timeout
    if timeout:
        cmd.extend(["--timeout", str(timeout)])
    
    # Add retries
    if retries > 0:
        cmd.extend(["--reruns", str(retries)])
    
    # Add profiling
    if profile:
        cmd.extend(["--profile", "--profile-svg"])
    
    # Add slow test threshold
    if slow_threshold:
        cmd.extend(["--durations", str(slow_threshold)])
    
    # Add test path
    if test_path:
        cmd.append(str(test_path))
    else:
        cmd.append("tests/")
    
    # Add timestamp for logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = backend_dir / "test_logs" / f"test_results_{timestamp}.log"
    log_file.parent.mkdir(exist_ok=True)
    
    # Run the tests
    start_time = time.time()
    try:
        with open(log_file, "w") as f:
            process = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            output = process.stdout
            f.write(output)
        
        duration = time.time() - start_time
        
        # Parse test results
        tests_passed = output.count("PASSED")
        tests_failed = output.count("FAILED")
        total_tests = tests_passed + tests_failed
        
        # Update history
        if cache_results:
            history["runs"].append({
                "timestamp": timestamp,
                "duration": duration,
                "status": "success" if tests_failed == 0 else "failure",
                "tests_passed": tests_passed,
                "total_tests": total_tests,
                "log_file": str(log_file)
            })
            history["stats"]["total_tests"] += total_tests
            history["stats"]["failed_tests"] += tests_failed
            save_test_history(history)
        
        print(f"\nTests completed in {duration:.2f} seconds")
        print(f"Passed: {tests_passed}, Failed: {tests_failed}, Total: {total_tests}")
        print(f"Log file: {log_file}")
        
        if cache_results:
            print(generate_summary(history))
        
        # Generate HTML report if requested
        if generate_report and cache_results:
            report_file = generate_html_report(history)
            print(f"\nHTML report generated: {report_file}")
        
    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        output = e.stdout if hasattr(e, 'stdout') else ""
        
        # Update history
        if cache_results:
            history["runs"].append({
                "timestamp": timestamp,
                "duration": duration,
                "status": "failure",
                "tests_passed": output.count("PASSED"),
                "total_tests": output.count("PASSED") + output.count("FAILED"),
                "log_file": str(log_file)
            })
            save_test_history(history)
        
        print(f"\nTests failed after {duration:.2f} seconds")
        print(f"Exit code: {e.returncode}")
        print(f"Log file: {log_file}")
        
        if cache_results:
            print(generate_summary(history))
        
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests with optional coverage reporting")
    parser.add_argument("test_path", nargs="?", help="Specific test file or directory to run")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--failfast", action="store_true", help="Stop on first failure")
    parser.add_argument("--markers", help="Run only tests with specified markers")
    parser.add_argument("--verbose", type=int, choices=[0, 1, 2], default=1,
                      help="Verbosity level (0=quiet, 1=normal, 2=verbose)")
    parser.add_argument("--timeout", type=int, help="Test timeout in seconds")
    parser.add_argument("--retries", type=int, default=0, help="Number of retries for failed tests")
    parser.add_argument("--cache", action="store_true", help="Cache test results and generate summary")
    parser.add_argument("--profile", action="store_true", help="Profile test execution")
    parser.add_argument("--slow", type=float, help="Threshold for slow tests in seconds")
    parser.add_argument("--report", action="store_true", help="Generate HTML test report")
    parser.add_argument("--config", help="Path to test configuration file")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency checking")
    
    args = parser.parse_args()
    
    run_tests(
        test_path=args.test_path,
        coverage=args.coverage,
        html_report=args.html,
        parallel=args.parallel,
        failfast=args.failfast,
        markers=args.markers,
        verbose=args.verbose,
        timeout=args.timeout,
        retries=args.retries,
        cache_results=args.cache,
        profile=args.profile,
        slow_threshold=args.slow,
        generate_report=args.report,
        config_file=args.config,
        skip_deps=args.skip_deps
    ) 