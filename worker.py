import os

from vastai import Worker, WorkerConfig, HandlerConfig, LogActionConfig, BenchmarkConfig

# Configuration
MODEL_SERVER_PORT = int(os.environ.get("MODEL_SERVER_PORT", 18000))
MODEL_LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/workspace/model.log")

def benchmark_generator():
    """Generate benchmark request payload."""
    return {
        "text": "Hello, this is a benchmark test.",
        "voice": "en_US-lessac-medium"
    }

config = WorkerConfig(
    model_server_url="http://127.0.0.1",
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    handlers=[
        HandlerConfig(
            route="/generate",
            allow_parallel_requests=True,
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
        on_load=["PIPER_READY"],
        on_error=["Traceback", "Error:", "Exception:", "CUDA out of memory", "RuntimeError"],
        on_info=["Starting", "Loading", "Voice model found"],
    ),
)

Worker(config).run()
