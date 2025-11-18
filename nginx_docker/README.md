
1. 取得憑證
docker run -it --rm -p 80:80 -v ./certs:/etc/letsencrypt certbot/certbot certonly --standalone -d pc1.thetainformation.com

2. 啟動nginx服務
docker compose up -d


netsh advfirewall firewall add rule name="Docker HTTP" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="Docker HTTPS" dir=in action=allow protocol=TCP localport=443
 