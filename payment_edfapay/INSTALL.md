# EdfaPay Payment Gateway - Installation Guide

## Prerequisites

Before installing this module, ensure you have:

1. **Odoo v19** installed and running
2. **EdfaPay Merchant Account** with:
   - Merchant Key (UUID format)
   - Password
   - Access to EdfaPay merchant dashboard

3. **Server Requirements**:
   - HTTPS enabled (required for payment processing)
   - Public IP or domain name accessible from the internet
   - Firewall configured to allow incoming webhooks from EdfaPay

## Installation Steps

### Step 1: Module Installation

#### Option A: Using Odoo Apps Interface
1. Copy the `payment_edfapay` folder to your Odoo addons directory:
   ```bash
   cp -r payment_edfapay /path/to/odoo/addons/
   ```

2. Restart Odoo server:
   ```bash
   sudo systemctl restart odoo
   ```

3. Update the Apps List:
   - Login to Odoo as Administrator
   - Go to **Apps** menu
   - Click **Update Apps List**
   - Click **Update** in the confirmation dialog

4. Install the Module:
   - Search for "EdfaPay"
   - Click **Install**

#### Option B: Using Command Line
```bash
# Copy module to addons directory
cp -r payment_edfapay /path/to/odoo/addons/

# Install using odoo-bin
/path/to/odoo-bin -d your_database -i payment_edfapay --stop-after-init
```

### Step 2: EdfaPay Dashboard Configuration

1. Login to your EdfaPay merchant dashboard

2. Navigate to Settings or Integration section

3. Configure the following URLs:

   **Return URL (3DS):**
   ```
   https://yourdomain.com/payment/edfapay/return
   ```

   **Webhook/Callback URL:**
   ```
   https://yourdomain.com/payment/edfapay/webhook
   ```

   **Note**: Replace `yourdomain.com` with your actual domain

4. Note down your credentials:
   - Merchant Key (UUID format, e.g., xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
   - Password

### Step 3: Odoo Configuration

1. Navigate to **Accounting → Configuration → Payment Providers**

2. Find and click on **EdfaPay**

3. **Credentials Tab**:
   - **Merchant Key**: Enter your EdfaPay Merchant Key
   - **Password**: Enter your EdfaPay Password

4. **Configuration Tab**:
   - **State**: 
     - Select **Test Mode** for testing with sandbox
     - Select **Enabled** for production
   - **Published**: Check this box to make it available on your website

5. **Payment Form Tab**:
   - Review and customize the pre-payment message if needed

6. Click **Save**

### Step 4: Testing

#### Test in Sandbox Mode

1. Ensure **State** is set to **Test Mode**

2. Use test card numbers provided by EdfaPay:
   - **Successful Payment**: 4111111111111111 (Exp: 01/2025, CVV: Any 3 digits)
   - **3DS Test**: 2223000000000007 (Exp: 01/2039)

3. Create a test order in your Odoo e-commerce:
   - Add products to cart
   - Proceed to checkout
   - Select EdfaPay as payment method
   - Complete the payment

4. Verify:
   - Payment redirects to EdfaPay
   - Payment processes successfully
   - Returns to Odoo with correct status
   - Order status updates correctly

#### Verify Webhook Delivery

1. Check Odoo logs for webhook receipts:
   ```bash
   tail -f /var/log/odoo/odoo.log | grep -i edfapay
   ```

2. Verify transaction status updates automatically

### Step 5: Going Live

1. **Production Checklist**:
   - [ ] HTTPS is properly configured with valid SSL certificate
   - [ ] Production Merchant Key and Password obtained from EdfaPay
   - [ ] Callback URLs verified in EdfaPay production dashboard
   - [ ] Test transactions completed successfully in sandbox
   - [ ] Webhook delivery confirmed
   - [ ] Refund process tested (if applicable)

2. **Switch to Production**:
   - Go to **Accounting → Configuration → Payment Providers**
   - Open **EdfaPay** provider
   - Update **Merchant Key** and **Password** with production credentials
   - Change **State** to **Enabled**
   - Click **Save**

3. **Final Verification**:
   - Process a small real transaction
   - Verify payment success
   - Verify webhook delivery
   - Check order status update

## Troubleshooting

### Module Not Appearing

**Problem**: Module doesn't appear in Apps list

**Solution**:
1. Verify the module is in the addons path
2. Check file permissions:
   ```bash
   chmod -R 755 /path/to/odoo/addons/payment_edfapay
   ```
3. Update apps list in Odoo
4. Check Odoo logs for errors

### Payment Not Processing

**Problem**: Payment button doesn't redirect to EdfaPay

**Solution**:
1. Check Odoo logs for errors:
   ```bash
   tail -f /var/log/odoo/odoo.log
   ```
2. Verify credentials are correct
3. Check if provider is published
4. Verify currency is supported

### Webhook Not Received

**Problem**: Payments complete but order status doesn't update

**Solution**:
1. Verify callback URL in EdfaPay dashboard
2. Check firewall settings
3. Verify HTTPS is working
4. Check Odoo logs for incoming webhooks
5. Test webhook URL manually:
   ```bash
   curl -X POST https://yourdomain.com/payment/edfapay/webhook
   ```

### Hash Validation Errors

**Problem**: "Hash mismatch" or validation errors

**Solution**:
1. Verify password is correct (no extra spaces)
2. Check that credentials match EdfaPay dashboard
3. Review Odoo logs for detailed hash comparison

## Security Recommendations

1. **Always use HTTPS** in production
2. **Restrict access** to payment provider settings (admin only)
3. **Regularly update** Odoo and the module
4. **Monitor logs** for suspicious activity
5. **Backup** your database before major changes
6. **Use strong passwords** for Odoo admin accounts

## Uninstallation

If you need to uninstall the module:

1. Go to **Apps**
2. Search for "EdfaPay"
3. Click **Uninstall**
4. Confirm the action

**Warning**: This will remove all EdfaPay payment provider records and configurations.

## Support

For support:
- **Module Issues**: Contact your Odoo partner or developer
- **EdfaPay API**: Contact EdfaPay support
- **Account Setup**: Contact EdfaPay merchant services

## Additional Resources

- **EdfaPay API Documentation**: https://sandbox.edfapay.com/pgapi/EdfapayCheckout_Developer-API.html
- **Odoo Payment Documentation**: https://www.odoo.com/documentation/19.0/developer/reference/backend/payment.html

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Author**: Arabian Admas Ltd Co
