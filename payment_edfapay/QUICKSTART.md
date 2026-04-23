# Quick Start Guide - EdfaPay Payment Gateway

## 5-Minute Setup

### Step 1: Install Module (2 min)
```bash
# Copy module to Odoo addons
cp -r payment_edfapay /path/to/odoo/addons/

# Restart Odoo
sudo systemctl restart odoo

# In Odoo: Apps → Update Apps List → Search "EdfaPay" → Install
```

### Step 2: Configure EdfaPay Dashboard (1 min)
Login to EdfaPay dashboard and set:
- **Return URL**: `https://yourdomain.com/payment/edfapay/return`
- **Webhook URL**: `https://yourdomain.com/payment/edfapay/webhook`

### Step 3: Configure Odoo (2 min)
1. Go to: **Accounting → Configuration → Payment Providers → EdfaPay**
2. Enter:
   - **Merchant Key**: Your EdfaPay Merchant Key
   - **Password**: Your EdfaPay Password
   - **State**: Test Mode (for testing) or Enabled (for production)
3. Check **Published**
4. Save

### Step 4: Test Payment
1. Add product to cart
2. Checkout
3. Select EdfaPay
4. Use test card: **4111111111111111** (Exp: 01/2025)
5. Complete payment

## Test Card Numbers

| Card Number | Expiry | Result |
|-------------|--------|---------|
| 4111111111111111 | 01/2025 | Success |
| 2223000000000007 | 01/2039 | 3DS Redirect |

## URLs to Configure

Replace `yourdomain.com` with your actual domain:

- **Return URL**: `https://yourdomain.com/payment/edfapay/return`
- **Webhook**: `https://yourdomain.com/payment/edfapay/webhook`

## Supported Currencies

SAR • AED • USD • EUR • GBP • KWD • OMR • QAR • BHD • JOD • EGP

## Troubleshooting

### Payment Not Working?
1. Check credentials are correct
2. Verify URLs in EdfaPay dashboard
3. Ensure HTTPS is enabled
4. Check Odoo logs: `tail -f /var/log/odoo/odoo.log | grep -i edfapay`

### Webhook Not Received?
1. Verify webhook URL in EdfaPay dashboard
2. Check firewall allows incoming connections
3. Test: `curl -X POST https://yourdomain.com/payment/edfapay/webhook`

## Going Live

1. Get production credentials from EdfaPay
2. Update Merchant Key and Password in Odoo
3. Change State to **Enabled**
4. Test with small real transaction
5. Monitor first few transactions closely

## Support

- **Module**: See INSTALL.md for detailed guide
- **API**: https://sandbox.edfapay.com/pgapi/EdfapayCheckout_Developer-API.html
- **Security**: See SECURITY.md for best practices

## Files Included

- `README.md` - Full documentation
- `INSTALL.md` - Detailed installation guide
- `CHANGELOG.md` - Version history
- `SECURITY.md` - Security best practices
- `LICENSE` - License information

---

**Ready to start?** See INSTALL.md for complete setup instructions.
