# 使用 JWT 進行身份驗證的 Flask 應用程序

此專案是一個最基本的 Flask web app 的 api，包括用戶註冊、登錄和用戶管理等功能。它利用 Flask-SQLAlchemy ORM 進行數據庫(SQLite)的操作 mapping，Flask-JWT-Extended 進行 JSON Web Token (JWT) 基於身份驗證。

## 功能

- **用戶註冊**：允許新用戶使用名稱和密碼註冊。
- **用戶登錄**：驗證現有用戶並為安全 API 訪問生成 JWT。
- **用戶管理**：提供端點來獲取用戶詳細信息和更新用戶角色。
- **後台管理**：一個僅對後台用戶身分可訪問的端點，用於管理其他用戶。

## 開始使用

要在本地運行此應用程序，請按照以下步驟操作：

1. 確保您的系統上已經安裝了 Python 3.x。
2. 使用 pip 安裝所需的套件：

pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-Login

3. clone 此 repo 的專案到本地。
4. 在 terminal 中移動到該專案目錄下。
5. terminal 中輸入 $python -m venv virtual 並接著$.\virtual\Scripts\activate 來設置 python 虛擬環境
6. terminal 中輸入 $python create_db.py 先設置資料庫
7. 然後 terminal 中輸入 $ python app.py 來啟動 Flask web app。
8. 打開 postman 以訪問應用程序 api。

## api 端點

### 用戶註冊

- **URL**：`/api/register`
- **方法**：POST
- **描述**：用戶名稱和密碼註冊新用戶。

### 用戶登錄

- **URL**：`/api/login`
- **方法**：POST
- **描述**：登錄現有用戶並返回 JWT token。

### 獲取當前用戶

- **URL**：`/api/user`
- **方法**：GET
- **要求**：JWT token 在 Authorization 標頭中
- **描述**：返回目前驗證的用戶的詳細信息。

### 更改用戶角色

- **URL**：`/api/users/<int:user_id>/role`
- **方法**：PUT
- **要求**：JWT token 在 Authorization 標頭中
- **描述**：將用戶的角色更新為管理員。

### 後台管理

- **URL**：`/api/admin`
- **要求**：JWT token 在 Authorization 標頭中
- **描述**：顯示所有用戶列表，只對管理員用戶可訪問。

## 安全性注意事項

在此範例中使用的 JWT 秘鑰（`"my-secret"`）,可自行更改，以確保應用程序的安全性。

## 備註

1. 目前本專案僅供 api 串接，template 部分尚未串接，因此無法在 web 上顯示渲染。
