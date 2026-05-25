# Wazuh → TheHive Integration
## Features

- ✅ Automatic case creation for alerts level ≥ 3
- ✅ Full alert context included
- ✅ Severity mapping (Wazuh level → TheHive severity)
- ✅ Automatic tagging
- ✅ Compatible with TheHive 5.x API

## Installation

### 1. Copy Integration Script

```bash
sudo cp custom-w2thehive.py /var/ossec/integrations/
sudo chmod 640 /var/ossec/integrations/custom-w2thehive.py
sudo chown root:wazuh /var/ossec/integrations/custom-w2thehive.py
```

### 2. Create Wrapper Script

```bash
sudo cat > /var/ossec/integrations/custom-w2thehive << 'WRAPPER'
#!/bin/sh
exec /var/ossec/framework/python/bin/python3 /var/ossec/integrations/custom-w2thehive.py "$@"
WRAPPER

sudo chmod 750 /var/ossec/integrations/custom-w2thehive
sudo chown root:wazuh /var/ossec/integrations/custom-w2thehive
```

### 3. Configure Wazuh

Edit `/var/ossec/etc/ossec.conf` and add inside `<ossec_config>`:

```xml
<integration>
  <name>custom-w2thehive</name>
  <hook_url>http://localhost:9000</hook_url>
  <api_key>YOUR_THEHIVE_API_KEY</api_key>
  <alert_format>json</alert_format>
  <level>3</level>
</integration>
```

### 4. Get TheHive API Key

1. Login to TheHive
2. Click your profile (top-right)
3. Go to **API Keys**
4. Click **"Create API Key"**
5. Copy the generated key
6. Paste it in the `<api_key>` field above

### 5. Restart Wazuh Manager

```bash
sudo systemctl restart wazuh-manager
```

## Testing

### Test 1: Manual Trigger

```bash
# Modify a monitored file
sudo touch /etc/passwd
```

**Expected:** New case appears in TheHive within seconds

### Test 2: Check Integration Logs

```bash
sudo tail -f /var/ossec/logs/integrations.log
```

**Expected output:**
WRAPPER

sudo chmod 750 /var/ossec/integrations/custom-w2thehive
sudo chown root:wazuh /var/ossec/integrations/custom-w2thehive

### 3. Configure Wazuh

Edit `/var/ossec/etc/ossec.conf` and add inside `<ossec_config>`:

```xml
<integration>
  <name>custom-w2thehive</name>
  <hook_url>http://localhost:9000</hook_url>
  <api_key>YOUR_THEHIVE_API_KEY</api_key>
  <alert_format>json</alert_format>
  <level>3</level>
</integration>
```


### 4. Get TheHive API Key

1. Login to TheHive
2. Click your profile (top-right)
3. Go to **API Keys**
4. Click **"Create API Key"**
5. Copy the generated key
6. Paste it in the `<api_key>` field above
### 5. Restart Wazuh Manager

```bash
sudo systemctl restart wazuh-manager
```

**Expected:** New case appears in TheHive within seconds

### Test 2: Check Integration Logs

```bash
sudo tail -f /var/ossec/logs/integrations.log
```

**Expected output:**
### Test 3: Verify Permissions

```bash
ls -la /var/ossec/integrations/custom-w2thehive*
```

**Expected output:**
## Alert Level Mapping

| Wazuh Level | TheHive Severity | Description |
|-------------|------------------|-------------|
| 12-15 | High (3) | Critical alerts |
| 7-11 | Medium (2) | Important alerts |
| 3-6 | Low (1) | Informational alerts |

## Troubleshooting

### No cases appearing in TheHive

1. Check API key is correct
2. Verify TheHive is accessible: `curl http://localhost:9000`
3. Check integration logs: `sudo tail -f /var/ossec/logs/integrations.log`
4. Verify alert level threshold (must be ≥ 3)

### Permission denied errors

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-w2thehive*
sudo chmod 750 /var/ossec/integrations/custom-w2thehive
sudo chmod 640 /var/ossec/integrations/custom-w2thehive.py
```

### Integration script not found

```bash
# Verify files exist
ls -la /var/ossec/integrations/custom-w2thehive*

# If missing, copy again from repository
```

## Configuration Options

You can customize the integration by editing `custom-w2thehive.py`:

- **TLP (Traffic Light Protocol)**: Default is AMBER (2)
- **PAP (Permissible Actions Protocol)**: Default is AMBER (2)
- **Tags**: Add custom tags to categorize alerts
- **Severity mapping**: Adjust thresholds for High/Medium/Low

## Support

For issues with this integration:
1. Check the main repository README troubleshooting section
2. Open an issue on GitHub
3. Check Wazuh and TheHive documentation
