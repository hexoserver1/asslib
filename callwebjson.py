from .disp import disp


def callwebjson(url, method="GET", data=None, headers=None, retry=1, delay=2, max_delay=10, warn=True, authtoken=None):
    """
    callwebjson(url, [method, data], [retry], [delay] [max_delay] [warn])
    where url    is the URL to call
          method    is the HTTP method to use
          data      is dict to send as JSON (if using PUT or POST)
          headers   is a dict representing HTTP header values
          retry     is the number of attempts to make the call in the event of a failed call(s)
          delay     is the base delay in number of seconds between retry attempts
          max_delay is the maximum individual delay value in seconds
          warn      is a boolean to enable warnings display. Defaults to True

    callwebjson makes a HTTP call to send and/or receive JSON with retry functionality


      title - callwebjson vr - 1.2 author - fakas date - 20190509

      mods  - 1.1 Adjustment to default arguments to better conform to Python conventions,
                  enabled usage of neglected 'warn' argument and added noinspetion comments
                  where appropriate                                         (fakas20190708)

            - 1.2 Added authtoken parameter to method which takes the auth access token as a string. If auth
                  token exists then it is appended to the header in key:value format.  (roje20190711)

    """
    from urllib import request as http
    from urllib import parse

    from json import loads
    import traceback
    from time import sleep

    if headers is None:
        headers = {}

    if authtoken is not None:
        auth = {"Authorization": "Bearer " + authtoken}  # Set authorization key: value
        headers.update(auth)  # Append authorization key: value to header

    suppress = not warn  # For simplicity's sake

    # Upper-case method is preferred by documentation and enforced here for consistency
    method = method.upper()
    attempt = 1

    while attempt <= retry:
        if attempt > 1:
            # Wait for given delay if we're retrying
            sleep(min(delay * attempt, max_delay))  # Only sleep for up to max delay
            disp("Retrying...")

        # noinspection PyBroadException
        try:
            if data is not None:
                # Request with embedded data, encode to JSON
                jdata = parse.urlencode(data).encode('utf-8')
            else:
                # Request without embedded data
                jdata = None
            response = http.urlopen(http.Request(url, data=jdata, method=method, headers=headers))
        except Exception:
            disp("Unexpected error in request to " + url + " ("+method+"): " + traceback.format_exc())
            attempt += 1
            continue
        if response.getcode() != 200:
            disp(url + "Returned a non-200 response code: " + str(response.getcode()))
            attempt += 1
            continue

        # noinspection PyBroadException
        try:
            data = response.read().decode("utf-8")
        except Exception:
            data = ''

        if len(data) == 0:
            if method == "GET":
                # We can only assume response data with GET
                disp("Call to " + url + "("+method+") returned no data...")
                attempt += 1
                continue
            else:
                # Don't waste time retrying for non-GET methods
                disp("Warning: Call to " + url + "(" + method + ") returned no " +
                     "data, best practice is to return an empty JSON object!", suppress=suppress)
                return None

        # noinspection PyBroadException
        try:
            # Decode returned data and load into JSON dict object
            jobj = loads(data)

        except Exception:
            disp("Unexpected error resolving JSON: " + traceback.format_exc())
            attempt += 1
            continue

        return jobj
    raise Exception("No valid response received after " + str(retry) + " attempts! URL: \n" +
                    url)
