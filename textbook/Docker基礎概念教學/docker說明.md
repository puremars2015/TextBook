### CHAPTER 01: Docker介紹

---

#### 1.1 Docker的誕生

Docker的誕生源於2013年，由一間名為DotCloud的公司推出。這家公司最初是一家平台即服務（PaaS）提供商，致力於為開發者提供簡單而強大的工具，讓應用程式能夠快速而高效地部署和運行。在這個過程中，他們發現市場缺乏一種工具，能夠將應用程式的依賴環境完整封裝，讓開發、測試和部署過程更加一致。Docker的出現為解決這個痛點提供了全新的方案：它能夠將應用程式及其依賴項封裝成一個“容器”，並可以在任何平台上運行，從而解決了傳統環境中“在我電腦上沒問題”的困境。

#### 1.2 軟體產業的變革

軟體產業在近幾年發生了巨大的變革。隨著雲計算技術的發展，以及微服務架構的廣泛應用，軟體部署和維護的需求已經變得越來越複雜。傳統的部署方式需要依賴具體的操作系統環境和依賴庫，不僅耗時，還容易產生不兼容的問題。Docker的誕生，讓“容器化”概念迅速崛起，解決了軟體部署中的許多難題。透過Docker的技術，開發人員可以在開發環境中創建一個完整的應用程式環境，並確保該環境可以在生產環境中無縫運行，從而提高了開發和運營的協作效率（DevOps），並促進了持續集成和交付（CI/CD）的實現。

#### 1.3 Docker是什麼？

Docker是一個開放源碼的容器平台，它允許開發人員封裝、分發和運行應用程式及其所有依賴環境。與虛擬機不同，Docker利用操作系統層的隔離技術，將應用程式及其依賴環境封裝成獨立的單位（容器），從而讓這些容器可以在不同的系統和雲平台上運行。這使得應用程式變得高度可移植，可以在開發環境、測試環境甚至是生產環境中保持一致的行為表現。

#### 1.4 我可以用Docker做些什麼？

Docker可以在多種場景中應用，包括但不限於：

- **開發與測試環境的統一**：開發人員可以使用Docker建立一個標準化的開發環境，從而減少環境不一致導致的問題。
- **應用程式的快速部署**：利用Docker容器，應用程式可以在幾秒內完成部署，並可在不同環境間快速移植。
- **微服務架構**：Docker特別適合用於微服務架構，每個微服務都可以在單獨的容器中運行，保持獨立且彼此隔離。
- **多雲和混合雲部署**：Docker容器的高可移植性，讓企業可以輕鬆將應用程式部署在不同的雲平台上。
- **持續集成和持續交付**：利用Docker構建、測試和部署流程，使得持續交付的流程更加順暢和高效。

#### 1.5 Docker的基礎架構

Docker的基礎架構包含以下幾個主要組件：

- **Docker Client**：用戶可以通過Docker命令行與Docker Daemon進行交互，負責發送命令並接收反饋。
- **Docker Daemon**：Docker的核心服務，負責管理容器和鏡像。
- **Docker Image（映像檔）**：應用程式及其依賴環境的靜態文件，類似於只讀模板。用戶可以基於映像檔來創建容器。
- **Docker Container（容器）**：Docker映像檔的運行實例，包含應用程式及其所有依賴項。容器之間相互隔離，每個容器都具有自己的文件系統和網絡。
- **Docker Hub**：Docker官方的映像檔倉庫，用於儲存和分享映像檔。用戶可以從Docker Hub上下載公開的映像檔，也可以上傳自己的映像檔。

#### 1.6 Docker的指令格式

Docker提供了一組簡單而強大的命令來管理容器和映像檔。以下是一些常用的Docker指令格式：

- **docker run**：啟動一個新容器，例如：`docker run hello-world`
- **docker pull**：從Docker Hub或其他倉庫拉取一個映像檔，例如：`docker pull ubuntu`
- **docker build**：基於Dockerfile構建一個新的映像檔，例如：`docker build -t myapp .`
- **docker ps**：查看正在運行的容器，例如：`docker ps`
- **docker stop**：停止一個運行中的容器，例如：`docker stop container_id`
- **docker rm**：刪除一個容器，例如：`docker rm container_id`
- **docker rmi**：刪除一個映像檔，例如：`docker rmi image_id`

這些命令構成了Docker最基本的操作方式，讓用戶可以輕鬆地管理和操作容器，並將應用程式快速部署至各種環境。

### CHAPTER 02: Docker容器

---

#### 2.1 容器的生命週期

Docker容器的生命週期包括創建、運行、暫停、停止、重啟及刪除等階段。理解容器的生命週期可以幫助我們更有效地管理和控制應用程式的運行環境。

- **創建 (Create)**：當我們使用 `docker create` 指令時，Docker會基於映像檔創建一個新的容器，但並不啟動它。這相當於設置好環境，等待運行的準備階段。
- **運行 (Run)**：容器的運行可以通過 `docker start` 或 `docker run` 指令來實現。在這個階段，應用程式會在容器中啟動並執行。
- **暫停 (Pause)**：可以使用 `docker pause` 將容器內的所有進程暫停，暫時凍結容器的狀態。
- **停止 (Stop)**： `docker stop` 指令可以優雅地停止容器，讓容器內的應用程式結束所有進程並退出。
- **重啟 (Restart)**：容器的重啟是指將已經停止的容器重新啟動。這可以通過 `docker restart` 指令來完成，適用於在保持容器狀態的基礎上快速恢復服務。
- **刪除 (Remove)**：最後，當容器不再需要時，可以使用 `docker rm` 指令將其刪除，以釋放資源。

理解這些階段讓我們能夠根據需求管理容器的生命週期，靈活控制應用程式的部署和回收。

#### 2.2 一探究竟容器內部

進入容器的內部可以讓開發者更好地理解容器內部的文件系統、進程和網絡狀態。通過 `docker exec` 指令，我們可以進入一個正在運行的容器，並直接與容器內部的操作系統進行互動。例如：

```bash
docker exec -it <container_id> /bin/bash
```

這條指令將在指定的容器內開啟一個交互式的Shell，讓我們可以查看容器的文件系統結構、安裝應用程式或進行其他操作。進入容器後，我們可以觀察到容器擁有自己的文件系統，並且只運行與應用程式相關的必要進程。這種隔離性使得Docker容器能夠實現輕量化和高效運行。

#### 2.3 容器與虛擬機

容器和虛擬機（Virtual Machine, VM）都是用來隔離應用程式和運行環境的技術，但它們的運作方式和資源利用率存在顯著差異。

- **架構**：虛擬機是通過在物理主機上安裝Hypervisor來創建和管理的，每個虛擬機都包含完整的操作系統及應用程式，佔用大量系統資源。相對而言，Docker容器直接運行在主機的操作系統內核之上，不需要完整的操作系統，資源佔用更少。
- **啟動速度**：虛擬機通常需要幾分鐘的時間來啟動完整的操作系統，而Docker容器只需幾秒鐘，因為它使用了共享的主機內核。
- **資源利用**：由於容器直接使用主機內核，資源佔用更少、更高效，適合高密度部署。

總的來說，Docker容器的輕量特性使其更適合現代的微服務架構，而虛擬機更適合於需要高隔離性和完全分離操作系統的場景。

#### 2.4 容器的IP位置及Port

每個Docker容器都擁有自己的虛擬網絡接口和IP地址，這使得容器之間可以通過IP地址進行通信。默認情況下，Docker會分配一個內部IP地址給每個容器。用戶可以通過以下指令查看容器的IP地址：

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>
```

此外，Docker容器的端口是容器和外界通信的重要手段。通過端口映射（Port Mapping），我們可以將主機的端口與容器的端口綁定在一起，使得外部可以通過主機的IP地址和指定的端口來訪問容器內的服務。例如：

```bash
docker run -p 8080:80 <image_name>
```

這條指令會將主機的8080端口映射到容器內的80端口，使得主機可以通過 `http://localhost:8080` 訪問容器內的應用服務。這樣的端口映射機制提供了容器與外部網絡的靈活交互方式，方便我們將應用程式公開到網絡上。

### CHAPTER 03: Docker虛擬網路

---

#### 3.1 Docker的虛擬網路概念

Docker的虛擬網路系統是一套用於實現容器之間通信的網絡架構。Docker虛擬網路的主要目的是讓容器之間能夠在同一主機上或跨主機之間互相通信，並且能夠與外部網絡互聯互通。這種虛擬網路技術利用網橋、網卡和端口轉發等技術來隔離容器之間的網絡流量，實現應用程式在容器內的高度隔離性和靈活性。

Docker的虛擬網路可以劃分為以下幾種模式：

- **Bridge（橋接）模式**：這是Docker的默認網路模式。當容器啟動時，它會被連接到一個虛擬網橋上（通常是`docker0`），這樣容器之間可以直接通信。這種模式適合單主機上的容器互聯。
- **Host（主機）模式**：在這種模式下，容器直接使用主機的網絡堆疊，沒有虛擬網橋的隔離。這樣容器可以更高效地使用網絡資源，但缺乏容器內網絡的隔離性。
- **Overlay（覆蓋）模式**：這是Docker為多主機集群設計的網絡模式。Overlay網路允許不同主機上的容器通過同一虛擬網絡通信，適合Swarm模式下的容器集群環境。
- **None模式**：在這種模式下，容器沒有任何網絡配置，完全隔離網絡，用於需要手動管理網絡的情況。

透過這些網絡模式，Docker提供了一套靈活的網絡配置方案，使得容器的網絡連接可以根據不同的需求進行適應性調整。

#### 3.2 操作Docker虛擬網路

Docker提供了一組命令來創建和管理虛擬網路，讓用戶可以靈活地配置網絡結構。以下是一些常見的操作：

- **查看現有網路**：
  使用 `docker network ls` 指令來查看Docker中所有可用的網路。例如：

  ```bash
  docker network ls
  ```

  此指令將列出當前主機上的所有Docker網路，包括預設的`bridge`、`host`和`none`網路。

- **創建新網路**：
  可以使用 `docker network create` 創建自定義網路。例如：

  ```bash
  docker network create my_custom_network
  ```

  這將創建一個名為`my_custom_network`的虛擬網路，容器之間可以加入此網路來進行通信。

- **連接容器到指定網路**：
  使用 `docker network connect` 指令可以將一個容器連接到指定的網路。例如：

  ```bash
  docker network connect my_custom_network <container_id>
  ```

  這樣該容器就可以與其他在`my_custom_network`上的容器互相通信。

- **移除網路**：
  若不再需要某個網路，可以使用 `docker network rm` 將其刪除。例如：

  ```bash
  docker network rm my_custom_network
  ```

這些操作讓Docker網絡管理變得非常直觀，我們可以根據應用需求靈活地配置容器之間的網絡結構。

#### 3.3 Docker的DNS

Docker提供了內建的DNS功能，以便容器可以根據名稱解析IP地址，這對於跨容器的通信非常便利。當一個容器加入Docker網路後，Docker會自動為該容器分配一個IP地址，並將該容器的名稱註冊到內部的DNS服務中。這樣，其他容器可以使用容器名稱直接進行通信，而不需要手動查找IP地址。

例如，在同一網路中的容器A和容器B中，容器A可以通過名稱`containerB`來訪問容器B，這樣的DNS解析大大簡化了容器之間的網絡通信配置。

此外，Docker還允許配置外部的DNS服務，以便容器能夠訪問外部網絡。例如，在運行容器時可以指定自定義的DNS服務器：

```bash
docker run --dns 8.8.8.8 <image_name>
```

這樣，容器內部的DNS解析會優先使用指定的DNS服務器（如Google的`8.8.8.8`），確保容器可以正常訪問外部網絡資源。

### CHAPTER 04: Docker映像檔

---

#### 4.1 什麼是映像檔？

Docker映像檔是一種輕量化、獨立且可執行的軟體包，包含了應用程式的運行環境及其所有依賴。每個Docker容器都是基於一個映像檔運行的，而映像檔本身可以看作是容器的靜態模板。映像檔分層存儲了應用程式所需的文件、環境變數和配置，讓應用程式可以在各種環境中一致地運行。

#### 4.2 從DockerHub開始認識映像檔

Docker Hub是一個公共的映像檔倉庫，用戶可以在此下載和分享映像檔。許多流行的軟體（例如Nginx、MySQL、Python）都有官方映像檔，讓我們能夠快速部署並使用這些軟體。可以使用以下命令從Docker Hub下載映像檔：

```bash
docker pull <image_name>
```

例如，`docker pull nginx`會下載最新版本的Nginx映像檔到本地。

#### 4.3 映像檔的標籤

Docker映像檔的標籤（Tag）是用來區分映像檔版本的標識。默認情況下，拉取的映像檔是最新的（通常標記為`latest`），但我們也可以指定其他標籤來拉取特定版本的映像檔。例如：

```bash
docker pull nginx:1.19
```

這將下載標籤為`1.19`的Nginx映像檔。

#### 4.4 層層堆疊的映像檔

Docker映像檔是通過分層技術構建的，每一層都包含了一部分變更，如添加文件或運行命令。這些層是不可變的且可以被多個映像檔共享，從而減少了磁碟空間的使用。Docker使用聯合文件系統（UnionFS）將這些層堆疊起來，最終構成一個完整的映像檔。

#### 4.5 映像檔快取的秘密

在構建映像檔時，Docker會自動使用快取來提高建構速度。每次執行Dockerfile中的指令時，Docker會檢查是否有已存在的快取可以復用，從而避免重複執行相同的指令。這樣，快取可以大大加快構建速度，特別是在修改文件時。

#### 4.6 映像檔的唯讀性

Docker映像檔是唯讀的，這意味著我們無法直接修改映像檔內的內容。當一個容器基於映像檔啟動時，Docker會創建一個可寫層來保存運行時的變更。這種唯讀設計增加了映像檔的安全性，同時保證了每次啟動容器時的一致性。

#### 4.7 推送映像檔到DockerHub

當我們創建了自定義映像檔後，可以將其推送到Docker Hub上，方便其他人下載和使用。首先，使用 `docker login` 登錄Docker Hub，然後使用 `docker push` 將映像檔上傳。例如：

```bash
docker push username/myimage:tag
```

#### 4.8 本地建立映像檔儲存庫

除了Docker Hub，也可以在本地創建私有的映像檔儲存庫，適合內部開發環境使用。Docker Registry是一個開源項目，可以用來搭建本地的映像檔倉庫，從而不依賴於互聯網。

#### 4.9 Dockerfile內容解析

Dockerfile是用來構建Docker映像檔的腳本文件。它包含了一系列指令，如 `FROM`、`COPY`、`RUN` 等，來描述如何生成映像檔。Dockerfile的每一行指令通常會創建一個新的層，並記錄映像檔構建的步驟。

#### 4.10 建置映像檔

可以使用以下指令來基於Dockerfile構建映像檔：

```bash
docker build -t myimage:tag .
```

這條命令將根據當前目錄下的Dockerfile構建映像檔，並命名為`myimage:tag`。

#### 4.11 重新整理Dockerfile的執行順序

在編寫Dockerfile時，指令的執行順序會影響映像檔的大小和構建速度。將常變更的指令放在文件後面可以提高快取利用率，並且減少每次構建的時間。

#### 4.12 多階段建置映像檔

多階段構建允許我們在同一個Dockerfile中使用多個`FROM`指令，以減少映像檔的最終大小。例如，可以在第一階段構建應用程式，在第二階段中只保留所需的可執行文件，從而生成更精簡的映像檔。

#### 4.13 Golang應用程式的多階段建置

在Golang應用程式中，多階段構建特別適用於編譯二進位文件，並在最終階段中只保留運行所需的文件，減少映像檔的大小。

#### 4.14 Express.js應用程式的多階段建置

在Express.js應用程式中，可以使用多階段構建來安裝依賴項並構建應用程式，然後僅將最小的依賴和代碼拷貝到最終的映像中，減少了不必要的開發依賴。

#### 4.15 .dockerignore

`.dockerignore` 文件類似於 `.gitignore`，用於指定哪些文件或目錄在構建映像檔時需要忽略，從而減少映像檔的大小和構建時間。

#### 4.16 清理本機容量

隨著時間的推移，Docker會在本地存儲大量的映像檔、容器和網路，佔用大量空間。我們可以使用以下命令清理不需要的資源：

```bash
docker system prune
```

這條指令會刪除所有不使用的容器、網路和未標記的映像檔。

### CHAPTER 05: Docker Volume

---

#### 5.1 有 / 無狀態的應用程式

應用程式可以分為有狀態和無狀態兩種。無狀態應用程式（Stateless Application）不需要保存任何用戶或操作數據，應用程序重啟後不會受到影響。相反，有狀態應用程式（Stateful Application）則需要持久化數據，這些數據在應用程式重啟後依然存在。舉例來說，Web伺服器通常是無狀態的，而數據庫服務則是有狀態的。

在Docker中，容器本身是短暫的，默認情況下任何數據都會在容器刪除後消失。因此，如果需要持久化數據，通常會用到Volume來實現數據的長期存儲。Volume是Docker推薦的持久化數據存儲方式，它允許將數據從容器內分離出來，保存在主機或其他存儲設備上。

#### 5.2 從DockerHub看Volume

在Docker Hub上許多官方映像檔都支持Volume，讓應用程式可以方便地實現數據持久化。比如，MySQL、MongoDB等數據庫映像檔通常會自帶Volume設定，將數據保存到特定的目錄中。當我們運行這些容器時，可以指定一個Volume，這樣無論容器如何重啟，數據都能保持不變。

#### 5.3 執行帶有Volume指令的映像檔

運行容器時，可以通過`-v`或`--mount`指令來指定Volume。例如：

```bash
docker run -d -v myvolume:/var/lib/mysql mysql
```

這條指令會將名為`myvolume`的Volume掛載到容器內的`/var/lib/mysql`目錄，這樣MySQL的數據就會持久化到這個Volume中。當容器刪除後，數據依然保存在Volume中，不會丟失。

#### 5.4 為你的Volume命名

命名Volume有助於組織和管理持久化數據，特別是在多容器環境中。使用以下指令可以創建並命名一個Volume：

```bash
docker volume create myvolume
```

接著，可以在運行容器時引用這個Volume：

```bash
docker run -d --name mycontainer -v myvolume:/app/data myimage
```

這樣，我們可以通過Volume名稱來訪問並管理數據。命名Volume還有助於共享數據，允許多個容器掛載同一個Volume，實現數據共享。

#### 5.5 另一種方式：Bind Mount

除了Volume，Docker還提供了另一種數據持久化方式：Bind Mount。與Volume不同，Bind Mount允許將主機上的特定目錄直接掛載到容器中。這意味著，主機和容器可以直接共享數據，而不需要經過Docker的Volume管理。例如：

```bash
docker run -d -v /host/data:/app/data myimage
```

這條指令將主機上的`/host/data`目錄掛載到容器內的`/app/data`目錄。這種方式在開發和測試階段非常有用，因為它可以讓容器直接訪問主機上的文件。

然而，Bind Mount與Volume相比有一些限制。Bind Mount的數據是存儲在主機文件系統中的具體路徑，當主機文件系統變更時，數據可能會受到影響。而Volume則是由Docker管理的，可以跨平台和跨主機環境使用，更加靈活。

### CHAPTER 06: Docker Compose

---

#### 6.1 什麼是Docker Compose？

Docker Compose是一種用於定義和管理多容器應用程式的工具。當我們的應用程式需要多個容器協同工作時（例如一個Web伺服器與數據庫服務），手動啟動和配置每個容器會變得繁瑣。Docker Compose通過一個名為`docker-compose.yml`的文件，讓我們可以在單一文件中定義應用程式所需的所有服務，並通過一條指令來啟動或管理它們。

Compose不僅能夠簡化容器的啟動，還支持跨容器的網絡設置、環境變數配置、Volume掛載等，讓我們可以輕鬆地構建和運行多容器應用程式。

#### 6.2 啟動WordPress

Docker Compose非常適合用來搭建需要多個服務的應用程式。以下是一個簡單的`docker-compose.yml`文件，用於啟動WordPress和MySQL數據庫：

```yaml
version: '3.8'
services:
  wordpress:
    image: wordpress
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: user
      WORDPRESS_DB_PASSWORD: password
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

這個文件定義了兩個服務：`wordpress` 和 `db`。`wordpress` 服務基於官方WordPress映像檔，並將HTTP端口8080映射到容器內的80端口。`db` 服務則基於MySQL映像檔，並且通過環境變數設置了數據庫用戶和密碼。最後，`volumes`字段用於指定數據庫的持久化存儲，確保數據不會隨著容器刪除而丟失。

要啟動這個WordPress服務，只需在文件所在的目錄運行以下命令：

```bash
docker-compose up -d
```

這條指令會根據`docker-compose.yml`文件啟動所有的服務並使其在後台運行。

#### 6.3 深入Docker Compose

Docker Compose支持多種配置選項，用戶可以在`docker-compose.yml`中設置容器的資源限制、網絡設置、環境變數等。以下是一些常用的配置選項：

- **volumes**: 持久化存儲，用於保存數據。例如`- db_data:/var/lib/mysql`。
- **ports**: 端口映射，將主機端口和容器端口進行綁定。例如`- "8080:80"`。
- **environment**: 環境變數，用於在容器內設置特定的變量值。
- **depends_on**: 設置容器之間的依賴順序。例如`depends_on`可以確保MySQL在WordPress之前啟動。
- **networks**: 指定容器所屬的網絡，方便容器間通信。

Docker Compose通過這些配置選項，可以滿足多種複雜的應用場景，實現靈活的多容器管理。

#### 6.4 Docker Compose的擴充欄位

Docker Compose還提供了一些擴充欄位，用來細化容器的配置和運行方式，例如：

- **restart**: 定義容器的重啟策略，例如`restart: always`，這樣容器在崩潰後會自動重啟。
- **build**: 支持從Dockerfile構建映像檔。例如`build: ./app`，可以從當前目錄的`app`文件夾中構建應用程式。
- **command**: 覆蓋默認的啟動命令。例如，`command: ["npm", "start"]`。
- **depends_on**: 用於設置容器之間的啟動順序，確保依賴服務先於其他服務啟動。
- **healthcheck**: 定義容器的健康檢查條件，確保容器在服務正常時才被認為“健康”。

這些擴充欄位可以進一步提高Compose文件的靈活性和可用性，使得我們可以精確控制容器的行為。

#### 6.5 範例一二三

以下是幾個使用Docker Compose的範例，展示不同的應用場景：

**範例一：多容器應用程式**

一個典型的Web應用程式包括Web伺服器、應用程式伺服器和數據庫。可以通過以下Compose文件來定義這些服務：

```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"

  app:
    image: myapp_image
    depends_on:
      - db
    environment:
      DATABASE_URL: mysql://user:password@db/mydatabase

  db:
    image: mysql
    environment:
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: root_password
```

**範例二：本地開發環境**

在本地開發環境中，我們可以將應用程式的源代碼掛載到容器中，以便於實時更新代碼。以下範例將源代碼掛載到Node.js容器中，方便開發者測試和調試：

```yaml
version: '3.8'
services:
  node:
    image: node:14
    volumes:
      - ./src:/app/src
    ports:
      - "3000:3000"
    command: ["npm", "run", "dev"]
```

**範例三：多階段建置**

在應用程式構建和運行時，可能需要多階段建置。以下範例展示了如何在多階段構建中使用Compose：

```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
```

在此範例中，`app`服務將從Dockerfile中構建，並將應用程式的埠5000映射到主機的5000埠上。

### CHAPTER 07: Docker Swarm

---

#### 7.1 Docker Swarm模式

Docker Swarm是Docker的原生集群管理工具，用於將多台Docker主機組成一個叢集。Swarm模式允許我們在多主機環境中管理和編排容器，實現應用程式的高可用性和負載平衡。透過Swarm模式，我們可以輕鬆將多個容器分布到多個節點上，並利用Swarm的自動修復功能來確保服務的穩定性。

#### 7.2 Swarm模式下的容器

在Swarm模式下，容器被組織成“服務”（Service）。每個服務由一組容器副本組成，這些副本會自動分布在集群中的不同節點上。這種方式允許應用程式在多個節點上運行，實現負載平衡和高可用性。Swarm還提供了滾動更新的功能，允許我們逐步更新容器，而不會影響整體服務的運行。

#### 7.3 Docker Swarm指令

Docker Swarm提供了一組指令，用於管理叢集和服務。以下是一些常用指令：

- **docker swarm init**：初始化一個新的Swarm叢集並將當前節點設為管理節點（Manager）。
- **docker swarm join**：將一個Docker主機加入到已有的Swarm叢集中，成為工作節點（Worker）。
- **docker service create**：在Swarm模式下創建一個新的服務。
- **docker service ls**：列出所有服務。
- **docker node ls**：列出Swarm叢集中的所有節點。
- **docker service scale**：調整服務的容器副本數量，例如 `docker service scale myservice=3`。

這些指令讓我們能夠靈活地管理和擴展Swarm叢集中的容器和服務。

#### 7.4 正式建立叢集

要建立一個Swarm叢集，我們首先需要在主節點（Manager）上初始化Swarm模式：

```bash
docker swarm init
```

此命令會返回一條`docker swarm join`指令，讓其他Docker主機可以加入叢集。然後，我們可以在其他主機上運行該指令，將它們添加到Swarm中。加入後，這些節點可以被分配到不同的服務，使得整個叢集擁有負載平衡和高可用性。

#### 7.5 Overlay虛擬網路

在Swarm模式下，Docker支持Overlay網路，這是一種虛擬網路技術，允許不同主機上的容器進行跨節點通信。Overlay網路將不同主機的容器組織到同一虛擬網路中，這樣無論容器在哪個節點上運行，都可以使用內部IP進行通信。要創建Overlay網路，可以使用以下指令：

```bash
docker network create -d overlay my_overlay_network
```

在創建服務時，我們可以指定該服務加入這個Overlay網路，從而實現跨節點的容器通信。

#### 7.6 如何在Swarm中儲存資料

在Swarm中，我們可以使用Volume來實現數據的持久化。Volume允許服務的數據即使在容器重啟或遷移後也能保持不變。可以在創建服務時指定Volume掛載。例如：

```bash
docker service create --name myservice --mount type=volume,source=myvolume,target=/app/data myimage
```

這樣，Swarm會在每個節點上創建名為`myvolume`的Volume，並將它掛載到服務容器的指定目錄中，實現數據的持久化存儲。

#### 7.7 如何在Swarm中傳遞敏感資料

Swarm提供了Secrets管理功能，用於存儲和傳遞敏感資料（如API密鑰、密碼等）。Secrets會被加密存儲，並且僅在需要的容器中解密，確保資料安全。

首先，我們可以創建一個Secret：

```bash
echo "my_secret_password" | docker secret create my_secret -
```

然後在創建服務時指定該Secret：

```bash
docker service create --name myservice --secret my_secret myimage
```

服務可以通過指定的路徑訪問該Secret，例如 `/run/secrets/my_secret`，從而安全地使用敏感資料。

#### 7.8 打包所有服務

Swarm支持堆疊（Stack）功能，允許我們將多個服務的配置打包到一個`docker-compose.yml`文件中，然後在Swarm中整體部署。使用以下命令可以部署一個Stack：

```bash
docker stack deploy -c docker-compose.yml mystack
```

這樣，Swarm會根據Compose文件中的配置啟動所有服務，並自動管理它們之間的網絡連接、依賴關係等。這種打包方式適合複雜應用程式的部署，讓我們可以輕鬆地在多節點上管理多個服務。

### CHAPTER 08: 部署Web應用程式

---

#### 8.1 購買屬於你的網域

在部署Web應用程式之前，首先需要一個網域名稱，這樣用戶可以通過網域訪問你的應用程式。可以通過各種網域註冊商（如GoDaddy、Namecheap等）購買網域，並根據需求選擇合適的頂級網域（如`.com`、`.net`等）。購買後，還需要配置DNS，以便網域可以指向你的伺服器IP地址，讓用戶可以訪問你的應用程式。

DNS配置主要包括A記錄（指向IP地址）、CNAME記錄（指向另一個域名）和其他服務所需的記錄。將網域與伺服器正確綁定後，就可以使用這個網域來提供Web服務。

#### 8.2 利用Traefik部署自己的映像檔儲存庫

Traefik是一個用於處理反向代理和負載平衡的開源工具，支持動態配置和多種協議。利用Traefik，我們可以輕鬆地配置HTTPS、自動生成SSL證書，並管理多個應用程式的路由。這對於多服務架構特別有用，例如當我們想要將不同的Web應用程式部署在同一伺服器上時。

Traefik可以作為Docker的反向代理，通過簡單的配置將多個服務公開到網絡上。例如，如果我們有一個映像檔儲存庫和幾個Web服務，可以用以下方式配置Traefik來管理這些服務的路由：

```yaml
version: '3.8'
services:
  traefik:
    image: traefik:v2.5
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=you@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./letsencrypt:/letsencrypt"

  registry:
    image: registry:2
    labels:
      - "traefik.http.routers.registry.rule=Host(`registry.example.com`)"
      - "traefik.http.routers.registry.entrypoints=websecure"
      - "traefik.http.routers.registry.tls.certresolver=myresolver"
    volumes:
      - "registry_data:/var/lib/registry"

volumes:
  registry_data:
```

這樣配置後，Traefik會將 `registry.example.com` 路由到映像檔儲存庫服務，並自動管理HTTPS證書。

#### 8.3 服務間的相依性

在構建和部署應用程式時，通常會有服務間的相依性。例如，後端API可能依賴於數據庫服務，前端應用則依賴於API服務。Docker Compose的`depends_on`指令可以指定服務間的啟動順序，確保數據庫先於API服務啟動，從而避免因服務未準備就緒而導致的錯誤。

然而，僅依賴`depends_on`可能不足以確保服務可用，因為`depends_on`僅控制啟動順序，並不能保證服務完全準備就緒。為此，可以使用健康檢查（Healthcheck）功能來確保服務的健康狀態。例如，API服務可以檢查數據庫連線狀態，在數據庫準備好後再啟動業務邏輯。

#### 8.4 部署前後端分離應用程式

在現代Web開發中，前後端分離架構非常普遍。通常，前端（如Vue.js、React等）用於處理用戶界面，而後端（如Node.js、Python Flask等）則負責處理業務邏輯和數據管理。這樣的應用程式可以通過Docker進行打包和部署。

以下是一個示例的`docker-compose.yml`文件，展示如何部署前後端分離的應用程式：

```yaml
version: '3.8'
services:
  frontend:
    image: myfrontend:latest
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    labels:
      - "traefik.http.routers.frontend.rule=Host(`frontend.example.com`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"
  
  backend:
    image: mybackend:latest
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    labels:
      - "traefik.http.routers.backend.rule=Host(`api.example.com`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=myresolver"
    environment:
      DATABASE_URL: mongodb://mongo:27017/mydb
    depends_on:
      - mongo

  mongo:
    image: mongo:4.4
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

這個配置文件包含了前端服務（`frontend`）、後端服務（`backend`）和數據庫（`mongo`）。前端和後端分別有各自的路由配置，通過Traefik將`frontend.example.com`指向前端應用，`api.example.com`指向後端API。後端依賴於MongoDB，並使用`depends_on`確保數據庫優先啟動。




