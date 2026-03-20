from flask import Flask, request, render_template_string, send_file
from docx import Document
import subprocess
import os
import math

app = Flask(__name__)

def compute_skus(num_leases):
    """Return SKUs based on number of leases."""
    try:
        n = int(num_leases)
    except:
        n = 0
    if n < 0:
        n = 0

    skus = []

    # Always include PS-TECH
    skus.append({
        'sku': 'PS-TECH',
        'hours': 16,
        'rate': 275,
        'total': 4400
    })

    # IFM SKU selection
    if n <= 15:
        skus.append({
            'sku': 'IFM-LEASE-BASE',
            'description': '
