# THis code works - but I'm annoyed with the way things change in Python all the time
# You have to know how things work - and practice coding yourself - a lot of practice is required

# Yeaaa you literally need to know how those functions and data structures are used
# like the Queue.join and queue.put in this program.... that's something new and not intuitive
# anyone who thinks that's intuitive is probably stupid and makes no sense
# https://docs.python.org/3/library/queue.html

import logging
import multiprocessing
import time
from queue import Queue
from threading import Thread
import requests


class WebsiteDownException(Exception):
    pass

def ping_website(address, timeout=20):
    """
    Check if a website is down. A website is considered down
    if either the status_code >= 400 or if the timeout expires

    Throw a WebsiteDownException if any of the website down conditions are met
    """
    try:
        response = requests.head(address, timeout=timeout)
        if response.status_code >= 400:
            logging.warning("Website %s returned status_code=%s" % (address, response.status_code))
            raise WebsiteDownException()
    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()


def notify_owner(address):
    """
    Send the owner of the address a notification that their website is down

    For now, we're just going to sleep for 0.5 seconds but this is where
    you would send an email, push notification or text-message
    """
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)


def check_website(address):
    """
    Utility function: check if a website is down, if so, notify the user
    """
    try:
        ping_website(address)
    except WebsiteDownException:
        notify_owner(address)


WEBSITE_LIST = [
    'https://envato.com',
    'http://amazon.co.uk',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://google.co.uk',
    'http://internet.org',
    'http://gmail.com',
    'http://stackoverflow.com',
    'http://github.com',
    'http://heroku.com',
    'http://really-cool-available-domain.com',
    'http://djangoproject.com',
    'http://rubyonrails.org',
    'http://basecamp.com',
    'http://trello.com',
    'http://yiiframework.com',
    'http://shopify.com',
    'http://another-really-interesting-domain.co',
    'http://airbnb.com',
    'http://instagram.com',
    'http://snapchat.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
    'http://live.com',
    'http://linkedin.com',
    'http://yandex.ru',
    'http://netflix.com',
    'http://wordpress.com',
    'http://bing.com',
]

# serial_squirrel.py
start_time = time.time()
for address in WEBSITE_LIST:
    check_website(address)
end_time = time.time()
print("Time for SerialSquirrel: %ssecs" % (end_time - start_time))

##############################################################################


NUM_WORKERS = 4
task_queue = Queue()

def worker():
    # Constantly check the queue for addresses
    while True:
        address = task_queue.get()
        check_website(address)

        # Mark the processed task as done
        task_queue.task_done()


start_time = time.time()

# Create the worker threads
threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]

# Add the websites to the task queue
[task_queue.put(item) for item in WEBSITE_LIST]

# Start all the workers
[thread.start() for thread in threads]

# Wait for all the tasks in the queue to be processed
task_queue.join()

end_time = time.time()

print("Time for ThreadedSquirrel: %ssecs" % (end_time - start_time))

##################################################################################


NUM_WORKERS = 4

start_time = time.time()

with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
    results = pool.map_async(check_website, WEBSITE_LIST)
    results.wait()

end_time = time.time()

print("Time for MultiProcessingSquirrel: %ssecs" % (end_time - start_time))

##################################################################################