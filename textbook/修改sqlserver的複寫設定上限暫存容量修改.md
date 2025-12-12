# SQL Server 設定複寫 LOB 同步上限（max text repl size）

以下 Script 將 SQL Server 的 LOB 複寫上限（`max text repl size`）從預設 **64 KB** 調整為 **無限制 (-1)**。  
此設定需在 **Publisher** 與 **Distributor**（若為不同伺服器）都執行，並確保執行者具有 `sysadmin` 權限。

---

```sql
/*--------------------------------------------------------------
  設定 SQL Server 複寫 LOB (max text repl size) 同步上限
  將原本的 64 KB 上限調整為「無限制」(-1)
  此設定需在 Publisher 與 Distributor 都執行 (若不同伺服器)
  執行者必須具備 sysadmin 權限
--------------------------------------------------------------*/

-- 1. 開啟進階選項 (sp_configure 需要先啟用才能設定)
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
-- 完成後可開始修改進階項目

-- 2. 將 max text repl size 設為 -1 (無限制)
--   - 預設 = 65536 bytes (64 KB)
--   - -1 表示無限制（只受資料型態實際大小限制）
EXEC sp_configure 'max text repl size', -1;
RECONFIGURE;

-- 3. 檢查設定結果 (config_value 與 run_value 都應為 -1)
EXEC sp_configure 'max text repl size';

---------------------------------------------------------------
-- 執行後注意：
-- 1. 若 run_value 未更新為 -1，請檢查是否具 sysadmin 權限。
-- 2. 若你的 Publisher 與 Distributor 是不同伺服器，
--    請到兩台都執行本 script。
---------------------------------------------------------------
