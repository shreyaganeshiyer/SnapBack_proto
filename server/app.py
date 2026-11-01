from pathlib import Path
from flask import Flask, jsonify
import config


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def home():
        return jsonify(
            {
                "project": "SnapBack",
                "status": "running",
                "message": "SnapBack backend is running.",
            }
        )

    @app.get("/api/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.get("/api/status")
    def status():
        shared_drive = Path(config.SHARED_DIR)
        snapshot_dir = Path(config.SNAPSHOT_DIR)

        file_count = 0
        
        if shared_drive.exists():
            file_count = sum(
                1 for path in shared_drive.rglob("*") if path.is_file()
            )

        snapshot_exists = snapshot_dir.exists()

        return jsonify(
            {
                "shared_drive_exists": shared_drive.exists(),
                "files_in_shared_drive": file_count,
                "snapshot_vault_exists": snapshot_exists,
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)