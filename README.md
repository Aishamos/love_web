# LOVE Web（OUR STORY）

情侣纪念网站：照片墙、相册、TodoList、纪念日倒计时。前端 Vue 3 + Vite + TypeScript，后端 Flask + MySQL，通过 nginx 反向代理部署。

---

## 目录

- [技术栈与组件版本](#技术栈与组件版本)
- [目录结构](#目录结构)
- [本地开发](#本地开发)
- [环境变量](#环境变量)
- [账户与密码说明](#账户与密码说明)
- [生产部署（Ubuntu / Debian）](#生产部署ubuntu--debian)
- [增量更新部署](#增量更新部署)
- [备份建议](#备份建议)
- [常见问题](#常见问题)
- [API 接口一览](#api-接口一览)
- [安全说明](#安全说明)

---

## 技术栈与组件版本

| 层 | 技术 | 版本 |
| --- | --- | --- |
| 前端框架 | Vue | ^3.5.13 |
| 路由 | vue-router | ^4.5.0 |
| 构建工具 | Vite | ^6.2.4 |
| 语言 | TypeScript | ~5.7.3 |
| 样式 | Tailwind CSS | ^3.4.17 |
| 动画 | GSAP | ^3.12.7 |
| 图片 EXIF | exifr | ^7.1.3 |
| 后端框架 | Flask | 3.1.0 |
| ORM | Flask-SQLAlchemy | 3.1.1 |
| 数据库驱动 | PyMySQL | 1.1.1 |
| 图片处理 | Pillow | 11.1.0 |
| WSGI 服务器 | gunicorn | 23.0.0 |
| 数据库 | MySQL | 5.7+ / 8.0 |
| 反向代理 | Nginx | 1.18+ |
| 进程管理 | systemd | 系统自带 |

完整依赖见 [package.json](package.json) 与 [backend/requirements.txt](backend/requirements.txt)。

**运行环境要求：**

- Node.js ≥ 18（仅构建前端需要；服务器只部署 `dist/` 时不需要）
- Python ≥ 3.10（推荐 3.12 / 3.13）
- MySQL 5.7 或 8.0

---

## 目录结构

```text
LOVE_web/
├── src/                    # 前端源码
│   ├── api/                # API 封装（含 CSRF token 管理）
│   ├── components/         # 布局 / 区块 / 通用组件
│   ├── composables/        # Vue 组合式函数（认证、图片查看器、纪念日、Todo、动画等）
│   ├── pages/              # 页面（首页 / 登录 / 上传）
│   ├── router/             # 路由与滚动行为
│   ├── types/              # TypeScript 类型
│   └── utils/              # 工具（图片兜底等）
├── backend/                # Flask 后端
│   ├── app/
│   │   ├── api/            # 接口（photos / albums / hero / todos / upload）
│   │   ├── models/         # 数据模型
│   │   └── utils/          # 图片处理 / 时间 / CSRF
│   ├── migrations/         # 手动 SQL 迁移脚本
│   ├── seed_db.py          # 初始化数据库种子数据（示例相册，清空照片/相册及上传图片）
│   ├── init_admin.py       # 初始化/重置管理员账号密码（需显式确认）
│   ├── wsgi.py             # gunicorn 入口
│   └── requirements.txt
├── dist/                   # 前端构建产物（不纳入 git，部署时上传）
├── nginx.conf              # nginx 参考配置
└── _backup/                # 本地代码备份（不纳入 git）
```

---

## 本地开发

### 1. 前端

```bash
npm install
npm run dev          # 开发服务器 http://localhost:3000
npm run build        # 类型检查 + 生产构建，输出 dist/
```

### 2. 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 本地需要可用的 MySQL，并按下方"数据库准备"建库建用户
flask --app wsgi run --debug --port 5000
```

### 3. 数据库准备（本地 / 服务器通用）

```sql
CREATE DATABASE love_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'love'@'localhost' IDENTIFIED BY 'love123';
GRANT ALL PRIVILEGES ON love_web.* TO 'love'@'localhost';
FLUSH PRIVILEGES;
```

数据库表由后端启动时自动创建（`db.create_all()`）；如需初始化示例相册或管理员账号，分别执行：

```bash
cd backend
python seed_db.py --yes              # 初始化示例相册（清空照片/相册及上传图片后重建）
ADMIN_PASSWORD=你的密码 python init_admin.py --yes   # 创建/重置管理员账号
```

> ⚠️ `seed_db.py` 会**清空** photos / albums 两张表、**删除上传目录中的图片**，再重建示例相册；`init_admin.py` 只创建/重置账号，不影响照片与相册。两者都必须加 `--yes` 或设 `SEED_CONFIRM=1` 才会执行。

---

## 环境变量

| 变量 | 说明 | 默认值 | 必填 |
| --- | --- | --- | --- |
| `SECRET_KEY` | 会话签名密钥，生产必须为强随机值 | 开发: `dev-secret-change-in-production`；生产: 无（缺省拒绝启动） | 生产必填 |
| `DATABASE_URL` | SQLAlchemy 连接串 | `mysql+pymysql://love:love123@localhost:3306/love_web?charset=utf8mb4` | 否 |
| `UPLOAD_FOLDER` | 图片存储目录 | `/var/www/love_web/uploads` | 否 |
| `FLASK_ENV` | `development` / `production`；production 时 cookie 强制 HTTPS | `development` | 否 |
| `ALLOWED_ORIGINS` | CORS 允许来源，逗号分隔 | `http://localhost:3000,http://127.0.0.1:3000` | 否 |
| `ADMIN_USERNAME` | init_admin.py 创建的管理员用户名 | `0609` | 否 |
| `ADMIN_PASSWORD` | init_admin.py 创建/重置的管理员密码；不设则随机生成并打印一次 | 无 | 建议设置 |
| `SEED_CONFIRM` | 置为 `1` 等效于脚本 `--yes`（seed_db.py / init_admin.py） | 无 | 否 |

生成强随机密钥：

```bash
openssl rand -hex 32
```

---

## 纪念日与见面日期配置

首页（桌面导航栏与移动端）显示的"在一起天数""纪念日倒计时""距离见面天数"来自配置文件 [public/anniversary.json](public/anniversary.json)。构建时该文件会原样复制到 `dist/anniversary.json`，前端运行时读取它，因此**改日期不需要重新编译**：

```json
{
  "anniversaryStart": "2026-06-09",
  "anniversaryMonth": 6,
  "anniversaryDay": 9,
  "meetingDate": "2026-11-14"
}
```

| 配置项 | 作用 | 显示位置 |
| --- | --- | --- |
| `anniversaryStart` | 在一起的起始日期（`YYYY-MM-DD`），计算"在一起 X 天"（只显示总天数，不折算成年） | 桌面导航栏 / 移动端首页 |
| `anniversaryMonth` / `anniversaryDay` | 每年的纪念日月日（与真实在一起的月日一致），计算"距离纪念日还有 X 天" | 同上 |
| `meetingDate` | 距离见面的目标日期（`YYYY-MM-DD`），计算"距离见面还有 X 天"（日期已过则显示"已见面"） | 同上 |

**改日期的正确方式**：直接在服务器上编辑 `dist/anniversary.json`，保存后浏览器刷新即可生效，无需编译、无需重启。

> ⚠️ 重新构建并上传 `dist` 时，会覆盖服务器上改过的 `anniversary.json`（恢复成 `public/anniversary.json` 里的值）。所以改日期时记得把本地 `public/anniversary.json` 同步成相同值，两边保持一致。

---

## 账户与密码说明

本项目的"账户"只有两类，均无内置默认密码（开发默认值仅限本地，生产必须覆盖）：

### 数据库账户

- 用户：`love`，默认密码：`love123`（来自 `config.py` 默认连接串）
- **生产建议**：改为随机密码，并通过 `DATABASE_URL` 环境变量传入，不要沿用默认值

### 网站管理员

- 由 `init_admin.py` 创建，用户名默认 `0609`，密码由 `ADMIN_PASSWORD` 指定或随机生成（随机时会打印到终端，请注意保存）
- 重置管理员密码：`ADMIN_PASSWORD=新密码 python init_admin.py --yes`（不影响照片与相册数据）
- 登录页地址：`/login`

### 会话密钥

- `SECRET_KEY` 不是登录密码，但泄露等同于会话可被伪造，生产必须用 `openssl rand -hex 32` 生成并妥善保管

> 🔒 **不要**把任何真实密码写入本 README 或提交到 git。所有密码通过环境变量 / systemd `Environment` 注入。

---

## 生产部署（Ubuntu / Debian）

以下命令均在服务器执行，`用户名@服务器IP` 处替换为你的 SSH 信息。

### 1. 安装基础软件

```bash
sudo apt update
sudo apt install -y nginx mysql-server python3 python3-venv python3-pip
```

### 2. 上传代码

```bash
sudo mkdir -p /var/www/love_web
sudo chown -R $USER:$USER /var/www/love_web
```

在本地 Windows 上传（`dist/` 已从 git 移除，必须单独传）：

```powershell
scp -r dist 用户名@服务器IP:/var/www/love_web/
scp -r backend 用户名@服务器IP:/var/www/love_web/
```

### 3. 准备数据库

```bash
sudo mysql
```

```sql
CREATE DATABASE love_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'love'@'localhost' IDENTIFIED BY 'love123';
GRANT ALL PRIVILEGES ON love_web.* TO 'love'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. 安装后端依赖

```bash
cd /var/www/love_web/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. 初始化示例相册与管理员账号（仅首次）

```bash
cd /var/www/love_web/backend
export SECRET_KEY="用 openssl rand -hex 32 生成的值"
python seed_db.py --yes
export ADMIN_PASSWORD="你的管理员密码"
python init_admin.py --yes
```

### 6. 配置 systemd 服务

```bash
sudo nano /etc/systemd/system/love-web.service
```

```ini
[Unit]
Description=LOVE Web Flask Backend
After=network.target mysql.service

[Service]
User=root
WorkingDirectory=/var/www/love_web/backend
Environment=SECRET_KEY=你的密钥
Environment=FLASK_ENV=development
ExecStart=/var/www/love_web/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now love-web
sudo systemctl status love-web
```

> 关于 `FLASK_ENV`：先保持 `development` 跑通；接入 HTTPS 后再改为 `production`（production 下 cookie 强制 `Secure`，http 访问会导致登录失效）。

### 7. 配置 nginx

```bash
sudo nano /etc/nginx/sites-available/love-web
```

```nginx
server {
    listen 8081 default_server;
    listen [::]:8081;

    root /var/www/love_web/dist;
    index index.html;

    server_name _;

    location /api/ {
        client_max_body_size 20m;
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/uploads/ {
        alias /var/www/love_web/uploads/;
        expires 7d;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

启用并重载：

```bash
sudo ln -s /etc/nginx/sites-available/love-web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 8. 创建上传目录

```bash
sudo mkdir -p /var/www/love_web/uploads
sudo chown -R root:root /var/www/love_web/uploads
sudo chmod 755 /var/www/love_web/uploads
```

### 9. 验证

```bash
curl http://127.0.0.1:5000/api/auth/csrf   # 应返回 token
curl http://127.0.0.1:5000/api/hero         # 应返回图片信息
```

浏览器访问 `http://服务器IP:8081`，测试：登录 → 上传图片 → 添加/勾选 Todo。

防火墙需放行 8081 端口（云服务器在安全组开放，本地 `sudo ufw allow 8081`）。

---

## 增量更新部署

仅更新代码时，无需重装依赖、无需动数据库：

1. 本地重新构建前端（`npm run build`），上传覆盖：

   ```powershell
   scp -r dist 用户名@服务器IP:/var/www/love_web/
   scp -r backend 用户名@服务器IP:/var/www/love_web/
   ```

2. 服务器重启后端：

   ```bash
   sudo systemctl restart love-web
   ```

3. 浏览器强制刷新（Ctrl+F5）验证。

> 前后端必须**一起更新**：后端 CSRF 校验与前端 token 是配套的，只更新一边会导致登录/上传/Todo 报 403。

---

## 设置 MySQL 远程连接

如需用 Navicat / DataGrip 等图形化工具远程管理数据库，需要让 MySQL 监听所有网卡、授权远程用户、放行防火墙端口。项目提供了脚本 [setup_mysql_remote.sh](backend/setup_mysql_remote.sh) 一次性完成前两步并提示防火墙命令：

```bash
cd /var/www/love_web/backend
sudo bash setup_mysql_remote.sh <远程来源IP|%> [数据库用户] [数据库名]
# 例：sudo bash setup_mysql_remote.sh 1.2.3.4 love love_web
```

脚本会：把 `bind-address` 改为 `0.0.0.0` 并重启 MySQL；创建/更新远程用户并授权；最后提示防火墙放行命令。远程密码会在运行时交互输入，不写入脚本。

> ⚠️ 用 `%` 表示允许任意主机，存在安全风险，建议填固定公网 IP。3306 端口仅对可信来源放行。

---

## 备份建议

照片和数据库是站点唯一资产，建议配置每日定时备份：

```bash
sudo crontab -e
```

```cron
0 3 * * * mysqldump love_web > /backup/love_web_$(date +\%F).sql && find /backup -name '*.sql' -mtime +7 -delete
0 4 * * * rsync -a /var/www/love_web/uploads/ /backup/uploads/
```

首次执行先手动创建 `/backup` 目录并验证备份文件可读。

---

## 常见问题

| 现象 | 原因与处理 |
| --- | --- |
| 登录报 "CSRF 校验失败" | 浏览器缓存了旧前端。清缓存 / 无痕窗口重试；确认前端与后端已同步更新 |
| 登录后跳回登录页 / 一直未登录 | `FLASK_ENV=production` 但没有 HTTPS。改为 `development` 或先接证书 |
| 上传报 413 | 超过 16MB 大小限制，压缩图片；nginx `client_max_body_size` 与 Flask 限制已对齐为 20m / 16MB |
| 页面能开但图片全裂 | 确认 `/var/www/love_web/uploads` 存在且 nginx 可读（部署第 8 步） |
| 登录后不能跳到 TodoList 位置 | 已修复（跨页面导航的锚点滚动由首页数据加载后统一执行）。若仍异常，先强制刷新 |
| 首页无数据 | 后端未启动或数据库未就绪；查看 `sudo systemctl status love-web` 日志 |

---

## API 接口一览

所有接口前缀 `/api`，响应统一为 `{ code, message, data }`，`code === 0` 表示成功。写请求需携带 `X-CSRF-Token` 请求头（由 `GET /api/auth/csrf` 获取）。

| 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- |
| GET | `/auth/csrf` | 获取 CSRF token | 否 |
| POST | `/auth/login` | 登录 | 否 |
| POST | `/auth/logout` | 登出 | 否 |
| GET | `/auth/check` | 检查登录态 | 否 |
| GET | `/hero` | 首页大图（随机照片） | 否 |
| GET | `/photos` | 照片分页（`albumId` / `page` / `pageSize`，pageSize ≤ 50） | 否 |
| GET | `/photos/latest` | 最新照片（`count` ≤ 50） | 否 |
| GET | `/albums` | 相册列表 | 否 |
| GET | `/todos` | Todo 列表 | 否 |
| POST | `/todos` | 新建 Todo | 是 |
| PATCH | `/todos/<id>` | 更新完成状态（`done` 必须为布尔值） | 是 |
| POST | `/upload` | 上传图片（multipart，`files` / `remark` / `region` / `photoDate` / `albumId`） | 是 |

---

## 安全说明

- 生产环境必须设置强随机 `SECRET_KEY`，否则后端拒绝启动
- 写接口均有 CSRF 校验（`X-CSRF-Token`），CORS 仅允许白名单来源
- 上传仅接受 jpg / jpeg / png / webp，文件名随机化，Pillow 处理失败会拒绝并清理文件
- 建议尽快配置 HTTPS 并将 `FLASK_ENV` 切为 `production`
- 建议将 systemd 服务从 `User=root` 改为专用低权限用户
- `dist/`、`_backup/`、`node_modules/` 不纳入 git；勿将真实密码写入仓库
