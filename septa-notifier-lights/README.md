To set this up as a service, do:

```bash
sudo nano /lib/systemd/system/fancy_light_notifier.service
```

Paste in the contents of _fancy_light_notifier.service_ and exit. Then:

```bash
sudo chmod 644 /lib/systemd/system/fancy_light_notifier.service
sudo systemctl daemon-reload
sudo systemctl enable fancy_light_notifier.service
```
