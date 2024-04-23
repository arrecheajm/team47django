# quick'n' dirty script to improve productivity, feel free to delete
current_datetime=$(date +"%Y%m%d_%H%M%S")
cp db.sqlite3 "backup_db/backupdb_$current_datetime"
python3 manage.py migrate