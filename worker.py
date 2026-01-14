"""
Vast.ai PyWorker Configuration for Piper TTS

This file configures the PyWorker to proxy requests to the Piper TTS model server.
The model server runs on port 18000 and this pyworker handles routing on port 8000.

Following Vast.ai recommended structure:
- worker.py in public git repo
- PYWORKER_REPO env var points to this repo
- start_server.sh bootstrap script handles environment setup
"""
import os

from vastai import Worker, WorkerConfig, HandlerConfig, LogActionConfig, BenchmarkConfig

# Model server configuration
MODEL_SERVER_URL = "http://127.0.0.1"
MODEL_SERVER_PORT = int(os.environ.get("MODEL_SERVER_PORT", 18000))
MODEL_LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/workspace/model.log")

# Log patterns for PyWorker detection
# CRITICAL: These patterns are PREFIX-based (must match START of log line)
MODEL_LOAD_LOG_MSGS = [
    "PIPER_READY",  # Our model server prints this when ready
]

MODEL_ERROR_LOG_MSGS = [
    "Traceback",
    "Error:",
    "Exception:",
    "RuntimeError:",
]

MODEL_INFO_LOG_MSGS = [
    "Starting",
    "Loading",
    "Voice model found",
]


def benchmark_generator() -> dict:
    """Generate benchmark request payload.

    CRITICAL: This must match the TTSRequest model in model_server.py:
    - text: str (required)
    - voice: str (optional, defaults to en_US-lessac-medium)
    """
    return {
        "text": "Hello, this is a benchmark test for Piper TTS.",
        "voice": "en_US-lessac-medium"
    }


# PyWorker configuration
worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url="/health",
    handlers=[
        HandlerConfig(
            route="/generate",
            allow_parallel_requests=True,
            max_queue_time=60.0,
            benchmark_config=BenchmarkConfig(
                generator=benchmark_generator,
                runs=1,
                concurrency=1,
            ),
        ),
        HandlerConfig(
            route="/health",
            allow_parallel_requests=True,
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=MODEL_LOAD_LOG_MSGS,
        on_error=MODEL_ERROR_LOG_MSGS,
        on_info=MODEL_INFO_LOG_MSGS,
    ),
)

# Run PyWorker (blocks forever)
Worker(worker_config).run()
