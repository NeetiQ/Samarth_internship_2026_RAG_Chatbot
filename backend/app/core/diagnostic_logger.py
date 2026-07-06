import time
import os
import logging

logger = logging.getLogger("legal-rag-diagnostics")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

def get_rss_mb():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        try:
            with open('/proc/self/status') as f:
                for line in f:
                    if line.startswith('VmRSS:'):
                        return int(line.split()[1]) / 1024
        except Exception:
            pass
    return 0.0

class Profiler:
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = 0
        self.start_rss = 0

    def __enter__(self):
        self.start_rss = get_rss_mb()
        self.start_time = time.time()
        logger.info(f"START [{self.operation_name}] | PID: {os.getpid()} | RSS: {self.start_rss:.2f} MB")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        end_rss = get_rss_mb()
        elapsed_ms = (end_time - self.start_time) * 1000
        status = "ERROR" if exc_type else "SUCCESS"
        logger.info(f"END [{self.operation_name}] | Status: {status} | Elapsed: {elapsed_ms:.2f} ms | RSS Before: {self.start_rss:.2f} MB | RSS After: {end_rss:.2f} MB | Delta: {end_rss - self.start_rss:.2f} MB")
        if exc_type:
            logger.exception(f"Exception during [{self.operation_name}]: {exc_val}")
