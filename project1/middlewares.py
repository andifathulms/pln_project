from django.db import connection
from time import time
from operator import add
import re
from functools import reduce

class StatsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        '''
        In your base template, put this:
        <div id="stats">
        <!-- STATS: Total: %(total_time).2fs Python: %(python_time).2fs DB: %(db_time).2fs Queries: %(db_queries)d ENDSTATS -->
        </div>
        '''

        # Uncomment the following if you want to get stats on DEBUG=True only
        #if not settings.DEBUG:
        #    return None

        # get number of db queries before we do anything
        n = len(connection.queries)

        # time the view
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        total_time = time() - start

        # compute the db time for the queries just run
        db_queries = len(connection.queries) - n
        if db_queries:
            db_time = reduce(add, [float(q['time'])
                                   for q in connection.queries[n:]])
        else:
            db_time = 0.0

        # and backout python time
        python_time = total_time - db_time

        stats = {
            'total_time': total_time,
            'python_time': python_time,
            'db_time': db_time,
            'db_queries': db_queries,
        }

        # replace the comment if found
        if response and response.content:
            s = response.content.decode('utf-8')
            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)ENDSTATS\s*-->)')
            match = regexp.search(s)
            if match:
                s = (s[:match.start('cmt')] +
                     match.group('fmt') % stats +
                     s[match.end('cmt'):])
                response.content = s

        return response