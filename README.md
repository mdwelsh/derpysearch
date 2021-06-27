# derpysearch

It's search. But derpy.

Use these commands to run locally:
```bash
pip install -r requirements.txt
gcloud components install cloud-datastore-emulator
gcloud beta emulators datastore start

# In another terminal:
$(gcloud beta emulators datastore env-init)
python main.py
```


