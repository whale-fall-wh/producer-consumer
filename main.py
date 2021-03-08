import schedule
import time
import consumers
import producers


class Producer:
    def __init__(self):
        self.producers = producers.producers

    def start(self):
        for producer in self.producers:
            producer()
        # schedule.every(1).seconds.do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)


class Consumer:

    def __init__(self):
        self.consumers = consumers.consumer

    def yield_consumer(self):
        for consumer in self.consumers:
            yield consumer

    def start(self):
        for consumer in self.yield_consumer():
            t = consumer()
            t.setDaemon(False)
            t.start()


if __name__ == '__main__':
    Consumer().start()
    Producer().start()
