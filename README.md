# Odoo Server Framework 101 - Learning Project

Project ini adalah sarana pembelajaran Odoo 17 Server Framework. Materi utama diambil dari dokumentasi resmi Odoo dan diimplementasikan bertahap dalam bentuk module custom.

## Learning Source
Sumber materi resmi:
- https://www.odoo.com/documentation/17.0/th/developer/tutorials/server_framework_101.html

## Commit Strategy
Setiap commit merepresentasikan satu sub bab materi pada tutorial.

Format commit yang digunakan:
- `Chapter <N>: <Topic>`

Contoh cek progress pembelajaran:
```bash
git log --oneline
```

## Project Structure
- `docker-compose.yaml`: definisi service Odoo dan PostgreSQL untuk local development.
- `odoo.conf`: konfigurasi Odoo (addons path, database, workers).
- `customize/estate_property`: module utama hasil pembelajaran.
- `customize/estate_account`: module turunan untuk integrasi accounting.

## Minimal Setup (Docker Compose)
### Prerequisites
- Docker Engine
- Docker Compose plugin
- Port `8069` dan `5433` tidak dipakai process lain

### Setup Steps
1. Clone repository ini.
2. Masuk ke folder project.
3. Pastikan file `docker-compose.yaml` dan `odoo.conf` tersedia di root.
4. Jalankan service:

```bash
docker compose up -d
```

5. Buka Odoo di browser:
- `http://localhost:8069`

## Docker Compose Commands
- Jalankan service:

```bash
docker compose up -d
```

- Restart service:

```bash
docker compose restart
```

- Stop dan hapus container/network:

```bash
docker compose down
```

- Lihat log Odoo (opsional):

```bash
docker compose logs -f odoo-demo
```

## Update Module Saat Development
Setelah mengubah model/view, update module dari dalam container:

```bash
docker compose exec odoo-demo odoo -c /etc/odoo/odoo.conf -u estate_property -d <db_name> --stop-after-init
```

```bash
docker compose exec odoo-demo odoo -c /etc/odoo/odoo.conf -u estate_account -d <db_name> --stop-after-init
```

## Testing
Perubahan terakhir menambahkan comprehensive test suite untuk module `estate_property` serta perbaikan flow state saat create offer pertama.

Komponen yang dicakup test:
- `estate.property` (constraints, compute, onchange, action button, write/unlink, report action)
- `estate.property.offer` (price constraint, compute/inverse deadline, accept/refuse action, create rule)
- `estate.property.tag` (required + unique constraint)
- `estate.property.type` (unique constraint, compute offer count, action domain)

Jalankan full test module `estate_property`:

```bash
docker compose exec odoo-demo odoo -c /etc/odoo/odoo.conf -d BELAJAR_ODOO17 -u estate_property --test-enable --test-tags /estate_property --stop-after-init
```

Catatan:
- Log `bad query` saat test negatif constraint bisa muncul dan tetap normal selama summary akhir menunjukkan `0 failed, 0 error(s)`.

## Notes
Project ini ditujukan untuk pembelajaran lokal. Konfigurasi saat ini bukan baseline untuk environment production.
