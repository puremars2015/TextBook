# docker 網站與反向代理設定教學

## app.py
這是一個sample網站,只顯示了hello world,但代表一個網頁應用程式的原始檔,用來作為第一個docker的容器資料來源

## 



## 建立image
docker build -t [image name] .

docker build -t hello-world-web .


## 從image執行
docker run -d --name [container name] -p 443:443 [image name]

### 從image執行
docker run -d --name [container name] -p 80:80 [image name]

docker run -d --name hello-web -p 80:80 hello-world-web
