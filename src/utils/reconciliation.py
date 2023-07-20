"""
Utility functions for secret updates to reduce duplication
"""

from src.config import ConfigLoader
import time

def reconcile_secret(secret_name: str, age: int):
    
    outcome = ""
    if (time.time() - age) > 60:
        outcome = f"Secret {secret_name} has not been changed since last reconciliation."
    else:
        outcome = f"Secret {secret_name} has been changed since last reconciliation. Adding to update queue."
        # Add secret and config to queue
        # Add message for each config? Or add one message with all relevant config?
    return outcome
