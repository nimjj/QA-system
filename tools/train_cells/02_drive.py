# CELL 2: mount Google Drive and create the folders.
# EXPECT: Colab asks you to allow Drive access, then "Mounted at /content/drive" and "DRIVE_OK [...]".
# If it prints DRIVE_MOUNT_FAILED, stop and paste the message.
try:
    from google.colab import drive
    drive.mount("/content/drive")
    for sub in ("checkpoints", "data", "runs"):
        os.makedirs(f"{DRIVE}/{sub}", exist_ok=True)
    print("DRIVE_OK", sorted(os.listdir(DRIVE)))
except Exception as e:
    print("DRIVE_MOUNT_FAILED:", repr(e))
    raise
