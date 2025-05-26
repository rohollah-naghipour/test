import time
import threading

def download_file(url):
    print(f"Downloading {url}")
    time.sleep(2)  
    print(f"Finished {url}")

urls = [
    "https://example.com/file1",
    "https://example.com/file2",
    "https://example.com/file3",
    "https://example.com/file4"
]

threads = []
for url in urls:
    thread = threading.Thread(target=download_file, args=(url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("All downloads complete")