# mitmproxy-cache
Simple mitmproxy HTTPS web cache.
## How to install
Clone the repo:
`git clone https://github.com/matfyzacek/mitmproxy-cache/`
`cd mmitmproxy-cache`
`mkdir cache`
Download mitmproxy, and setup your browser to trust mitmproxy certificate.
Then run:
`mitmproxy -s cache.py`
Final step is to setup system to use mitmproxy as proxy.
## !!warning!!
It may break some websites. Please be craful
