# Email 驗證碼生成 API

這是一個用於生成電子郵件驗證碼的 Web API，配有一個測試用的網頁界面，方便進行集成與測試。驗證碼可以設置有效期，提供更靈活的驗證方式。

## 功能

- 生成電子郵件驗證碼。
- 配置驗證碼的有效期（默認為 15 分鐘）。
- 驗證用戶提交的驗證碼。
- 提供測試用網頁界面，方便快速測試與集成。

## 快速開始

### 需求

- Python 3.x
- Flask
- SMTP 設定（例如 Gmail）

### 安裝

1. 克隆這個倉庫：

   ```bash
   git clone https://github.com/your-username/email-verification-api.git
   cd email-verification-api
   ```

2. 安裝所需的依賴：

   ```bash
   pip install -r requirements.txt
   ```

3. 配置環境變量（如 `.env` 文件）：

   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=你的電子郵件地址
   EMAIL_PASSWORD=你的應用程式密碼
   VERIFICATION_CODE_EXPIRY=900  # 驗證碼有效期（以秒為單位），默認為 15 分鐘
   ```

4. 啟動服務：

   ```bash
   python app.py
   ```

5. 在瀏覽器中訪問 `http://localhost:5000` 來使用測試界面。

## API 文檔

### 1. 發送驗證碼

**端點：** `POST /send_verification_email`

**請求體：**

```json
{
  "email": "user@example.com"
}
```

**響應：**

```json
{
  "success": true,
  "message": "Verification email sent"
}
```

### 2. 驗證驗證碼

**端點：** `POST /verify_code`

**請求體：**

```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**成功響應：**

```json
{
  "success": true,
  "message": "Verification successful"
}
```

**失敗響應（驗證碼錯誤或過期）：**

```json
{
  "success": false,
  "message": "Invalid verification code" 或 "Verification code expired"
}
```

## 配置驗證碼有效期

你可以通過 `.env` 文件中的 `VERIFICATION_CODE_EXPIRY` 變量來配置驗證碼的有效期（以秒為單位）。默認設置為 **15 分鐘**。

## 測試界面

本 API 附帶一個簡單的網頁界面，用於測試驗證碼的生成與驗證。只需啟動服務並訪問 `http://localhost:5000`，即可使用該界面來進行測試。

## 開發

### 運行開發模式

使用以下命令以開發模式運行服務器，支持熱加載：

```bash
flask run --reload
```

## 貢獻

1. Fork 本倉庫。
2. 創建你的功能分支：`git checkout -b feature-name`。
3. 提交變更：`git commit -m 'Add feature'`。
4. 推送到分支：`git push origin feature-name`。
5. 發送 Pull Request。

## 授權

本項目基於 MIT 許可證進行授權。詳情請參見 [LICENSE](LICENSE) 文件。

