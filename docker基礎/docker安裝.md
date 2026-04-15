# Docker 安裝

## 大綱

1. [Windows 安裝](#1-windows-安裝)
2. [Linux 安裝](#2-linux-安裝)
3. [macOS 安裝](#3-macos-安裝)
4. [安裝後驗證](#4-安裝後驗證)
5. [Docker Engine 與 Docker Desktop](#5-docker-engine-與-docker-desktop)

---

## 1. Windows 安裝

### 1.1 系統需求

- Windows 10 64-bit（專業版、企業版、教育版）或 Windows 11
- 必須啟用 **WSL 2**（Windows Subsystem for Linux 2）
- 至少 4GB RAM
- 必須在 BIOS 啟用虛擬化（Virtualization）

### 1.2 安裝步驟

#### 方式一：Docker Desktop for Windows（推薦）

1. 前往 [Docker Desktop 官網](https://www.docker.com/products/docker-desktop) 下載安裝程式

2. 執行 `Docker Desktop Installer.exe`

3. 勾選「Use WSL 2 instead of Hyper-V」（建議）

4. 完成後點擊「Close」

5. 啟動 Docker Desktop，等待 Docker 圖示顯示為「Running」

#### 方式二：手動啟用 WSL 2

```powershell
# 以系統管理員身份開啟 PowerShell

# 啟用 WSL 功能
dism.exe /online /enable-norification /all /featurename:Microsoft-Windows-Subsystem-Linux /all /norestore

# 啟用虛擬機器平台
dism.exe /online /enable-norification /all /featurename:VirtualMachinePlatform /all /norestore

# 設定 WSL 2 為預設版本
wsl --set-default-version 2
```

### 1.3 常見問題

| 問題 | 解決方案 |
|------|----------|
| WSL 2 未正確安裝 | 安裝 Ubuntu 或其他 Linux 發行版 |
| 虛擬化未啟用 | 進入 BIOS 啟用 Virtualization Technology |
| Docker 啟動失敗 | 確認 WSL 2 更新至最新版本 |

---

## 2. Linux 安裝

### 2.1 Ubuntu / Debian

```bash
# 更新套件索引
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# 新增 Docker GPG 金鑰
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 新增 Docker 套件庫
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安裝 Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 將目前使用者加入 docker 群組（免 root 執行）
sudo usermod -aG docker $USER
newgrp docker
```

### 2.2 CentOS / RHEL / Fedora

```bash
# 移除舊版 Docker
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 安裝必要套件
sudo yum install -y yum-utils

# 新增 Docker 套件庫
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安裝 Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 啟動 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 2.3 快速安裝脚本

```bash
curl -fsSL https://get.docker.com | sh
```

---

## 3. macOS 安裝

### 3.1 Docker Desktop for Mac（推薦）

1. 前往 [Docker Desktop 官網](https://www.docker.com/products/docker-desktop) 下載 `Docker.dmg`

2. 雙擊下載的檔案，將 Docker 圖示拖曳至 Applications 資料夾

3. 啟動 Docker Desktop

4. 等待系統列顯示 Docker 圖示為「Running」

### 3.2 系統需求

- macOS 11 (Big Sur) 或更新版本
- 至少 4GB RAM
- 支援 Apple M1/M2/M3 晶片或 Intel 處理器

---

## 4. 安裝後驗證

### 4.1 確認 Docker 版本

```bash
docker --version
docker-compose --version
docker version
```

### 4.2 執行 Hello World 容器

```bash
docker run hello-world
```

成功輸出：

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 4.3 確認 Docker 服務狀態

```bash
# Linux
sudo systemctl status docker

# Windows/macOS（透過 Docker Desktop）
# 確認 Docker Desktop UI 顯示 Running 狀態
```

---

## 5. Docker Engine 與 Docker Desktop

### 5.1 Docker Engine

- 核心元件：dockerd（Daemon）、docker CLI、containerd
- 負責容器生命週期管理
- 適用於 Linux 伺服器環境

### 5.2 Docker Desktop

- 包含 Docker Engine + Docker CLI + Docker Compose + Kubernetes
- 內建 GUI 管理介面
- 適用於開發者本機環境（Windows / macOS）
- 支援容器化開發與測試

### 5.3 兩者差異

| 功能 | Docker Engine | Docker Desktop |
|------|---------------|----------------|
| 跨平台支援 | Linux only | Windows/macOS |
| 內建 Kubernetes | 需額外安裝 | 內建（可選） |
| GUI 管理工具 | 無 | 有 |
| 體積 | 輕量 | 較大 |

---

## 總結

- **Windows/macOS**：使用 Docker Desktop（推薦）
- **Linux 伺服器**：使用 Docker Engine
- 安裝後務必執行 `docker run hello-world` 驗證