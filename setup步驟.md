# openclaw新建立步驟

## 第一步：建立telegram機器人

1. 準備好telegram
2. telegram尋找bot father,找到後輸入/newbot，然後按照指示輸入機器人名稱和用戶名稱，最後會得到一個token，記得保存好這個token，後面會用到。
3. telegram尋找User Info,然後輸入/start，會達到你的user id，記得保存好這個user id，後面會用到。
4. 將這兩組id提供給openclaw的開發者，讓他們將你的telegram帳號加入到openclaw的系統中。
5. 等待開發者完成設定後，你就可以開始使用openclaw了。

## 第二步：setup google cloud platform

1. 前往[Google Cloud Platform](https://cloud.google.com/)並註冊一個帳號。(同gmail帳號)
2. 進入GCP，建立新的專案，命名為openclaw。
3. 在專案中，左上角漢堡選單->API和服務->程式庫->啟用Google Drive API和Google Sheets API。
4. 在專案中，左上角漢堡選單->API和服務->憑證->建立憑證->服務帳戶，命名為openclaw，選擇角色為專案->編輯者，然後點擊完成。到這邊會取得cliendt id跟client token，記得保存好這兩組資訊，後面會用到。
5. 在服務帳戶中，點擊剛剛建立的openclaw
6. 切到OAuth同意畫面->目標對象->發布狀態選發布。

到此為止，接下來的步驟會由openclaw協助完成，請將google cloud platform的client id和client token提供給openclaw，讓他完成後續的設定。

核心關鍵在於，正常使用OAuth登入，會有一個登入的動作，但openclaw執行這一段會比較複雜，所以通常會叫openclaw去產生一段URL，然後你用瀏覽器去打這個URL，會跳轉到Google的登入頁面，登入後會有一個授權的動作，授權完成後拿這個token貼回openclaw讓他儲存，這樣就完成了OAuth的流程。
