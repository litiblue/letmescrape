from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy import log
import time


class RetryMiddlewareWithIncreasingInterval(RetryMiddleware):
    INITIAL_INTERVAL_IN_SECONDS = 10
    MAX_INTERVAL_IN_SECONDS = 30
    INCREASING_RATE = 2

    def _retry(self, request, reason, spider):
        retryreq = super(RetryMiddlewareWithIncreasingInterval, self)._retry(request, reason, spider)
        if retryreq is None:
            return

        previous_retry_interval = request.meta.get('retry_interval', 0)
        retry_interval = previous_retry_interval * 2 or self.INITIAL_INTERVAL_IN_SECONDS

        if retry_interval <= self.MAX_INTERVAL_IN_SECONDS:
            log.msg(format="%(request)s will be retried in %(retry_interval)s",
                    level=log.DEBUG, spider=spider, request=request, retry_interval=retry_interval)

            retryreq.meta['retry_interval'] = retry_interval
            time.sleep(retry_interval)

            log.msg(format="Retrying %(request)s", level=log.DEBUG, spider=spider, request=request)
            return retryreq
        else:
            log.msg(format="Gave up retrying %(request)s "
                           "(%(retry_interval)ss exceeded the maximum value(%(max_retry_interval)s)): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retry_interval=retry_interval,
                    max_retry_interval=self.MAX_INTERVAL_IN_SECONDS)
