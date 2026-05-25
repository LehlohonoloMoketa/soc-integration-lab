#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wazuh → TheHive Integration Script
Automatically creates TheHive cases from Wazuh alerts

Compatible with TheHive 5.x API
"""

import sys
import json
import requests
from datetime import datetime

# Configuration
THEHIVE_URL = None
API_KEY = None

def send_to_thehive(alert_data):
    """Send alert to TheHive and create a case"""
    
    # Extract alert details
    rule_description = alert_data.get('rule', {}).get('description', 'Unknown')
    rule_level = alert_data.get('rule', {}).get('level', 0)
    agent_name = alert_data.get('agent', {}).get('name', 'Unknown')
    
    # Build TheHive case
    case = {
        "title": f"Wazuh Alert: {rule_description}",
        "description": json.dumps(alert_data, indent=2),
        "severity": get_severity(rule_level),
        "tags": ["wazuh", f"level-{rule_level}"],
        "tlp": 2,  # TLP:AMBER
        "pap": 2   # PAP:AMBER
    }
    
    # Send to TheHive
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{THEHIVE_URL}/api/v1/alert",
        headers=headers,
        json=case,
        verify=False
    )
    
    return response.status_code == 201

def get_severity(level):
    """Map Wazuh alert level to TheHive severity"""
    if level >= 12:
        return 3  # High
    elif level >= 7:
        return 2  # Medium
    else:
        return 1  # Low

if __name__ == "__main__":
    # Read configuration from command line
    THEHIVE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:9000"
    API_KEY = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Read alert from stdin
    alert_json = sys.stdin.read()
    alert = json.loads(alert_json)
    
    # Send to TheHive
    if send_to_thehive(alert):
        sys.exit(0)
    else:
        sys.exit(1)
