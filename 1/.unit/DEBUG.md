# Debug Nginx Unit

General live configuration, using curl:
```sh
curl -X PUT --data-binary @config.json --unix-socket /var/run/control.unit.sock http://localhost/config
```

Generation of new static stub configuration, remotely:
```sh
mkdir -p /var/www/static && echo "Hello World" > /var/www/static/index.html
cat << EOF > config.json
{
    "listeners": {
        "*:9090": {
            "pass": "routes"
        }
     },
    "routes": [
        {
            "action": {
                "share": "/var/www/static/"
             }
        }
    ],
    "access_log": "/var/log/access.log"
}
EOF
```

Download socat binary with curl:
```sh
curl -LJ -o socat https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true
```

Start socat as a HTTP interceptor [Cloud Foundry:443]->[socat:8080]->[Nginx Unit:9090]:
```sh
./socat -v TCP-LISTEN:8080,reuseaddr TCP-CONNECT:127.0.0.1:9090
```
# Bugs

https://github.com/nginx/unit/issues/422

I haven't managed to enable debug logging yet. It would mean rebuilding the Docker image, as it does not appear to be doable by changing the configuration. Is there another image available which starts this "unitd-debug" binary?

For now, I injected a socat instance in front of Unit, inside a live container:
```sh
root@eac3c01c-2116-4f0a-69cd-1da1:~# ./socat -v TCP-LISTEN:8080,reuseaddr TCP-CONNECT:127.0.0.1:9090
> 2020/04/09 09:47:33.460427  length=1027 from=0 to=1026
GET / HTTP/1.1\r
Host: www.example.com\r
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36\r
$wsis: false\r
$wsra: 77.56.208.204\r
$wssc: http\r
$wssn: www.example.com\r
$wssp: 80\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r
Accept-Encoding: gzip, deflate\r
Accept-Language: en-US,en;q=0.9\r
B3: ab3114a0f3d1da92-ab3114a0f3d1da92\r
Cache-Control: no-transform\r
Dnt: 1\r
Upgrade-Insecure-Requests: 1\r
Via: 1.1 DQAAADtvDEQ-\r
X-B3-Spanid: ab3114a0f3d1da92\r
X-B3-Traceid: ab3114a0f3d1da92\r
X-Cf-Applicationid: 02b6df87-2617-4b4f-8b1e-67abd17984b6\r
X-Cf-Instanceid: eac3c01c-2116-4f0a-69cd-1da1\r
X-Cf-Instanceindex: 0\r
X-Client-Ip: 77.56.208.204\r
X-Forwarded-For: 77.56.208.204, 10.164.95.242\r
X-Forwarded-Proto: http\r
X-Global-Transaction-Id: f28b14df5e8eef35e3be829f\r
X-Request-Start: 1586425653430\r
X-Vcap-Request-Id: 44eb6f3a-bd59-4786-7480-6bce6bfd3ec5\r
\r
< 2020/04/09 09:47:33.497045  length=204 from=0 to=203
HTTP/1.1 400 Bad Request\r
Content-Type: text/html\r
Server: Unit/1.16.0\r
Date: Thu, 09 Apr 2020 09:47:33 GMT\r
Content-Length: 54\r
Connection: close\r
\r
<!DOCTYPE html><title>Error 400</title><p>Error 400.\r
```

Unit is running on port 9090 with a simple "Hello World" static page, socat on 8080 to intercept the requests.

As you can see from the output, Unit is generating the "Error 400" on account of—I presume—one or more headers in the request.

The ones with the '$' characters seemed to be the most likely candidates, and bingo:

```sh
root@eac3c01c-2116-4f0a-69cd-1da1:~# curl localhost:9090
Hello World
root@eac3c01c-2116-4f0a-69cd-1da1:~# curl -H "$wssn: 80" localhost:9090
<!DOCTYPE html><title>Error 400</title><p>Error 400.
```


cat << EOF > config.json
{
    "listeners": {
        "*:8080": {
            "pass": "routes"
        }
     },
    "routes": [
        {
            "action": {
                "share": "/var/www/static/"
             }
        }
    ],
    "access_log": "/var/log/access.log"
}
EOF