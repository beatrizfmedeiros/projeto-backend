import os
import time
import threading
from backend.infra.storage.sqlite.sqlite_pedido_repository import SqlitePedidoRepository

# Configurable interval (seconds) via environment variable, default 7 seconds
INTERVAL = int(os.getenv('STATUS_UPDATE_INTERVAL', '7'))

# Global repository instance (reuse the same as in routes)
pedido_repo = SqlitePedidoRepository()

def _status_updater_loop():
    """Loop that advances order statuses at the configured interval."""
    while True:
        try:
            active_orders = pedido_repo.list_active_orders()
            for pedido in active_orders:
                # Advance only if there is a next status
                pedido_repo.advance_status(pedido.id)
        except Exception as e:
            # In production you'd log this; for now we just print
            print(f"[status_updater] Error while updating statuses: {e}")
        time.sleep(INTERVAL)

def start_background_updater():
    """Start the daemon thread that runs the status updater.
    Called from the Flask app factory during startup.
    """
    thread = threading.Thread(target=_status_updater_loop, daemon=True)
    thread.start()
    return thread
