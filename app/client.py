import time

import httpx

if __name__ == "__main__":
    url = "http://localhost:8001/"
    files = {'file': open('./app/test.txt', 'rb')}

    # Wait for server startup
    time.sleep(10)

    with httpx.Client() as client:
        for i in range(100):
            r = client.post(url, timeout=None, files=files)
            print(r.status_code)
            assert r.status_code == 200
