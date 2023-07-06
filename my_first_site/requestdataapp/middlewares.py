import time

from django.http import HttpRequest
from django.shortcuts import render


def setup_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        return response
    return middleware

class CountRequestMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.last_request = {}

    def __call__(self, request: HttpRequest):
        # interval = 1
        # if self.last_request:
        #     if (time.time() - self.last_request['time']) < interval and self.last_request['ip-address'] == request.META.get('REMOTE_ADDR'):
        #         return render(request, 'requestdataapp/error-interval.html')

        self.last_request['ip-address'] = request.META.get('REMOTE_ADDR')
        self.last_request['time'] = time.time()

        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


