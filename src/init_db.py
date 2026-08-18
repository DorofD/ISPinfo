"""Однократная инициализация БД при первом старте контейнера."""
import os

import dbscripts

if not os.path.exists(dbscripts.DB_PATH):
    os.makedirs(os.path.dirname(dbscripts.DB_PATH), exist_ok=True)
    dbscripts.create_db()
    dbscripts.create_admin()
    print('Database initialized, admin user created')
else:
    print('Database already exists, skipping init')
