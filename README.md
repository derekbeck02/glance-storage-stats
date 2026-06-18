# Glance Storage Stats

A lightweight Docker API that provides storage statistics.

Monitor any mount point, NAS share, RAID array, or mergerFS pool and display the results in Glance using a custom-api widget.

## Screenshot

<img width="314" height="190" alt="storage-stats-screenshot" src="https://github.com/user-attachments/assets/a25a4e39-d572-4c9b-8b20-7cf0556f65eb" />

## Features

* Works with local disks, NAS mounts, mergerFS pools, and network storage
* Configurable display units (B, KB, MB, GB, TB)
* Optional subtitle

## Requirements

- Docker
- Docker Compose

## Quick Start

Clone the repository:

```bash
git clone https://github.com/derekbeck02/glance-storage-stats.git
cd glance-storage-stats
```

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
SUBTITLE=Main Storage
SHOW_SUBTITLE=true

PATH_TO_MONITOR=/path/to/your/storage
UNIT=TB
PORT=3020
```

Replace `/path/to/your/storage` with the directory or mount point you want to monitor and edit any of the other variables as you require.

Start the container:

```bash
docker compose up -d --build
```

Verify:

```bash
curl http://localhost:3020/api/storage
```

## Glance Widget

Add the following widget to your Glance configuration and edit the url:

```yaml
- type: custom-api
  title: Storage
  cache: 1m
  url: http://YOUR_SERVER_IP:3020/api/storage

  template: |
    <div class="flex flex-column gap-10">

      {{ if and (.JSON.Bool "show_subtitle") (.JSON.String "subtitle") }}
      <div class="size-h6 color-subdue">
        {{ .JSON.String "subtitle" }}
      </div>
      {{ end }}

      <div class="flex justify-between">
        <div>
          <div class="size-h5 uppercase">Used</div>
          <div>{{ .JSON.String "used" }}</div>
        </div>

        <div class="text-right">
          <div class="size-h5 uppercase">Free</div>
          <div>{{ .JSON.String "free" }}</div>
        </div>
      </div>

      <div style="height: 12px; border-radius: 999px; border: 1px solid var(--color-text-subdue); background: var(--color-background); overflow: hidden;">
        <div style="height: 100%; width: {{ .JSON.Float "used_percent" }}%; background: var(--color-primary);"></div>
      </div>

      <div class="size-h6 color-subdue">
        Total: {{ .JSON.String "total" }} • {{ .JSON.Float "used_percent" }}% used • {{ .JSON.Float "free_percent" }}% free
      </div>

    </div>
```

## Example API Response

```json
{
  "subtitle": "Main Storage",
  "show_subtitle": true,
  "host_path": "/path/to/your/storage",
  "container_path": "/storage",
  "unit": "TB",
  "used": "2.30 TB",
  "free": "13.70 TB",
  "total": "16.00 TB",
  "used_percent": 14.4,
  "free_percent": 85.6
}
```

## License

MIT
