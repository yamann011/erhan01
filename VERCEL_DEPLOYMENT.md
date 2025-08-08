# ERHAN Ziyaretçi Sistemi - Vercel Deployment Rehberi

## 1. Gereksinimler

- GitHub hesabı
- Vercel hesabı (ücretsiz)
- PostgreSQL veritabanı (Neon Database öneriliyor)

## 2. Proje Hazırlığı

### 2.1 Vercel Konfigürasyon Dosyası Oluştur
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "server/index.ts",
      "use": "@vercel/node"
    },
    {
      "src": "client/**/*",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server/index.ts"
    },
    {
      "src": "/(.*)",
      "dest": "/client/dist/index.html"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

### 2.2 Package.json Build Scripts Güncelle
```json
{
  "scripts": {
    "build": "npm run build:client && npm run build:server",
    "build:client": "cd client && vite build",
    "build:server": "cd server && tsc",
    "vercel-build": "npm run build"
  }
}
```

## 3. Veritabanı Kurulumu (Neon)

1. [Neon Console](https://console.neon.tech/) git
2. "Create Project" tıkla
3. Proje adı: `erhan-visitor-system`
4. Connection string'i kopyala (postgresql://...)

## 4. GitHub'a Yükleme

```bash
# 1. Git repository oluştur
git init
git add .
git commit -m "Initial commit"

# 2. GitHub'da yeni repository oluştur: erhan-visitor-system

# 3. Remote ekle ve push yap
git remote add origin https://github.com/USERNAME/erhan-visitor-system.git
git branch -M main
git push -u origin main
```

## 5. Vercel Deployment

### 5.1 Vercel'e Git
1. [Vercel Dashboard](https://vercel.com/dashboard) git
2. "New Project" tıkla
3. GitHub repository'yi seç: `erhan-visitor-system`

### 5.2 Environment Variables Ayarla
Vercel dashboard'da "Settings" > "Environment Variables":

```
DATABASE_URL = postgresql://username:password@hostname:port/database
SESSION_SECRET = your-super-secret-key-here
NODE_ENV = production
```

### 5.3 Build Settings
- **Build Command**: `npm run vercel-build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

## 6. Deploy

1. "Deploy" butonuna tıkla
2. Build işlemi tamamlanması bekle (2-3 dakika)
3. Domain adresini al: `https://erhan-visitor-system.vercel.app`

## 7. Veritabanı Tabloları Oluştur

Deploy'dan sonra Neon Console'da SQL Editor'ü açıp şu komutları çalıştır:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Visitors table
CREATE TABLE visitors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(200),
    visit_date TIMESTAMP NOT NULL,
    entry_time TIMESTAMP NOT NULL,
    exit_time TIMESTAMP,
    visit_type VARCHAR(20) NOT NULL,
    description TEXT,
    registered_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Default users
INSERT INTO users (username, password, first_name, last_name, role) VALUES 
('superadmin', '$2b$10$4d3P7.depGozt60vzBg8T.IaPGlui3DZRrH5vU8eVYWEQTxxH61Ya', 'Super', 'Admin', 'superadmin'),
('erhan', '$2b$10$4d3P7.depGozt60vzBg8T.IaPGlui3DZRrH5vU8eVYWEQTxxH61Ya', 'Erhan', 'Yaman', 'user');
```

## 8. Test

1. Deployed URL'i aç
2. `erhan` / `yaman` ile giriş yap
3. Ziyaretçi kaydı dene
4. Dashboard'u kontrol et

## 9. Domain Ayarları (Opsiyonel)

Vercel'de "Settings" > "Domains" bölümünden kendi domain'ini ekleyebilirsin.

## 10. Sorun Giderme

### Build Hatası
- `package.json` scripts'lerin doğru olduğunu kontrol et
- Dependencies eksik olabilir, `npm install` çalıştır

### Database Connection Hatası
- `DATABASE_URL` doğru format: `postgresql://user:pass@host:port/db`
- Neon'da connection string'in güncel olduğunu kontrol et

### 500 Server Error
- Vercel Functions logs'unu kontrol et
- Environment variables'ların doğru set edildiğini kontrol et

## Önemli Notlar

- Vercel'in ücretsiz planı ayda 100GB bandwidth sınırı var
- PostgreSQL bağlantı sayısını optimum tutmak için connection pooling kullanılıyor
- Session'lar artık memory yerine veritabanında saklanıyor (production için)

## Güvenlik

- Production'da güçlü `SESSION_SECRET` kullan
- Database şifresini güvenli tut
- HTTPS otomatik aktif (Vercel tarafından)

---
*Bu rehber ERHAN Ziyaretçi Kayıt Sistemi'ni Vercel'e deploy etmek için hazırlanmıştır.*