import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS  # 為了支持跨域請求
import random
import string
import time

app = Flask(__name__)

# 啟用 CORS（允許所有來源）
CORS(app, resources={r"/*": {"origins": "*"}})

# 配置郵件服務
SMTP_SERVER = "smtp.gmail.com"  # 使用 Gmail
SMTP_PORT = 587
EMAIL_ADDRESS = "{email}"  # 你的信箱
EMAIL_PASSWORD = "{password}"  # 信箱密碼（建議使用應用程式密碼）

# 驗證碼存儲和有效期配置
verification_codes = {}
VERIFICATION_CODE_EXPIRY = 15 * 60  # 驗證碼有效期為 15 分鐘

# 生成隨機驗證碼
def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# 發送驗證郵件
def send_verification_email(email, code):
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # 啟用 TLS 加密
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # 登入郵件伺服器
            server.sendmail(EMAIL_ADDRESS, email, message)  # 發送郵件
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# 發送驗證碼的 API
@app.route('/send_verification_email', methods=['POST'])
def send_email():
    try:
        # 獲取請求數據
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"success": False, "message": "No email provided"}), 400

        email = data['email']

        # 生成驗證碼並記錄時間戳
        verification_code = generate_verification_code()
        verification_codes[email] = {
            "code": verification_code,
            "timestamp": time.time()
        }

        # 發送郵件
        if send_verification_email(email, verification_code):
            return jsonify({"success": True, "message": "Verification email sent"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to send email"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 驗證驗證碼的 API
@app.route('/verify_code', methods=['POST'])
def verify_code():
    try:
        # 獲取請求數據
        data = request.get_json()
        if not data or 'email' not in data or 'code' not in data:
            return jsonify({"success": False, "message": "Email and code are required"}), 400

        email = data['email']
        code = data['code']

        # 驗證碼是否存在
        if email not in verification_codes:
            return jsonify({"success": False, "message": "No verification code found for this email"}), 400

        stored_code_data = verification_codes[email]
        stored_code = stored_code_data["code"]
        stored_timestamp = stored_code_data["timestamp"]

        # 驗證碼是否正確
        if stored_code != code:
            return jsonify({"success": False, "message": "Invalid verification code"}), 400

        # 驗證碼是否過期
        if time.time() - stored_timestamp > VERIFICATION_CODE_EXPIRY:
            del verification_codes[email]  # 刪除過期的驗證碼
            return jsonify({"success": False, "message": "Verification code expired"}), 400

        # 驗證成功
        del verification_codes[email]  # 刪除已驗證的驗證碼
        return jsonify({"success": True, "message": "Verification successful"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
