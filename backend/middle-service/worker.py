from app.service.queue_worker import QueueWorker
import threading

if __name__ == "__main__":
    worker = QueueWorker()

    t1 = threading.Thread(target=worker.run_market_queue)
    t2 = threading.Thread(target=worker.run_market_retry_queue)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
