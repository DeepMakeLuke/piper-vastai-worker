import os

from vastai import Worker, WorkerConfig, HandlerConfig, LogActionConfig, BenchmarkConfig

# Piper TTS model server configuration
MODEL_SERVER_URL = "http://127.0.0.1"
MODEL_SERVER_PORT = int(os.environ.get("MODEL_SERVER_PORT", 18000))
MODEL_LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/workspace/model.log")
MODEL_HEALTHCHECK_ENDPOINT = "/health"

# Piper-specific log messages
MODEL_LOAD_LOG_MSG = ["PIPER_READY"]
MODEL_ERROR_LOG_MSGS = [
    "Traceback",
    "Error:",
    "Exception:",
    "CUDA out of memory",
    "RuntimeError",
]
MODEL_INFO_LOG_MSGS = [
    "Starting",
    "Loading",
    "Voice model found",
]


def benchmark_generator():
    """Generate benchmark request payload for Piper TTS."""
    return {
        "text": "Hello, this is a benchmark test for the text to speech system.",
        "voice": "en_US-lessac-medium"
    }


worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url=MODEL_HEALTHCHECK_ENDPOINT,
    handlers=[
        HandlerConfig(
            route="/generate",
            allow_parallel_requests=True,
            max_queue_time=600.0,
            benchmark_config=BenchmarkConfig(
                generator=benchmark_generator,
                concurrency=1,
                runs=1,
            ),
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=MODEL_LOAD_LOG_MSG,
        on_error=MODEL_ERROR_LOG_MSGS,
        on_info=MODEL_INFO_LOG_MSGS,
    ),
)

Worker(worker_config).run()
