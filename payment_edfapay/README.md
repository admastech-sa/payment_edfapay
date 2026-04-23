# EdfaPay Payment Gateway for Odoo v19

This module integrates EdfaPay payment gateway with Odoo v19, allowing your customers to make secure online payments through EdfaPay's platform.

## Features

- Complete integration with EdfaPay Payment Gateway API
- Support for multiple currencies (SAR, AED, USD, EUR, GBP, etc.)
- Secure payment processing with 3D Secure support
- Automatic transaction status updates
- Webhook support for real-time payment notifications
- Test and production environment support
- Partial refund support

## Installation

1. Copy the `payment_edfapay` folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the "EdfaPay Payment Gateway" module

## Configuration

### 1. EdfaPay Account Setup

Before configuring the module, ensure you have:
- An active EdfaPay merchant account
- Your Merchant Key (UUID format)
- Your Password

**Important**: You must also provide EdfaPay with your:
- **Callback URL**: `https://yourdomain.com/payment/edfapay/webhook`
- **Return URL**: `https://yourdomain.com/payment/edfapay/return`

### 2. Odoo Configuration

1. Navigate to **Accounting > Configuration > Payment Providers**
2. Find and open the **EdfaPay** provider
3. Configure the following settings:

   **Credentials Tab:**
   - **Merchant Key**: Enter your EdfaPay Merchant Key (UUID format)
   - **Password**: Enter your EdfaPay Password
   
   **Configuration Tab:**
   - **State**: Select "Test Mode" for testing or "Enabled" for production
   - **Website Published**: Check to make it available on your website
   
   **Payment Form Tab:**
   - Customize the pre-payment message if needed
   
4. Save the configuration

### 3. Testing

For testing, use the following test credentials:

**API Endpoint (Sandbox):** `https://sandbox.edfapay.com/api/payment/initiate`

**Test Cards:**
- **Successful Payment**: 4111111111111111 (Exp: 01/2025)
- **3DS Redirect Test**: 2223000000000007 (Exp: 01/2039)

**Expected Responses:**
- Successful SALE: `{action: SALE, result: SUCCESS, status: SETTLED}`
- 3DS Redirect: `{action: SALE, result: REDIRECT, status: REDIRECT}`

### 4. Going Live

1. Change the **State** to "Enabled"
2. Ensure you're using production credentials
3. The module will automatically use: `https://api.edfapay.com/payment/initiate`

## API Endpoints

The module uses the following EdfaPay API endpoints:

- **Payment Initiation**: `POST https://api.edfapay.com/payment/initiate`
- **Refund**: `POST https://api.edfapay.com/payment/refund`
- **Status Check**: `POST https://api.edfapay.com/payment/status`

## Callback URLs

Make sure the following URLs are accessible and configured in your EdfaPay account:

- **Return URL**: `https://yourdomain.com/payment/edfapay/return`
- **Webhook URL**: `https://yourdomain.com/payment/edfapay/webhook`

## Hash Calculation

The module uses EdfaPay's signature formula:
```
SHA1(MD5(order_id.order_amount.order_currency.order_description.password))
```

All hash strings are converted to uppercase before hashing.

## Supported Transaction Types

- **SALE**: Immediate authorization and capture
- **REFUND**: Full or partial refund of completed transactions
- **STATUS**: Check transaction status

## Troubleshooting

### Payment not processing
1. Check that credentials are correct
2. Verify the callback URLs are configured in EdfaPay dashboard
3. Check Odoo logs for detailed error messages

### Callback not received
1. Ensure your Odoo instance is accessible from the internet
2. Verify the webhook URL is configured correctly in EdfaPay
3. Check firewall settings

### Hash mismatch errors
1. Verify the password is correct
2. Ensure no extra spaces in credentials
3. Check that the order amount format is correct (2 decimal places)

## Support

For issues related to:
- **Module functionality**: Contact your Odoo partner or developer
- **EdfaPay API**: Contact EdfaPay support
- **Account setup**: Contact EdfaPay merchant support

## Security Notes

- All credentials are stored encrypted in Odoo
- Password fields are masked in the UI
- Communication with EdfaPay uses HTTPS
- Hash validation ensures request authenticity

## Version History

### 1.0 (Current)
- Initial release
- Support for SALE transactions
- Webhook integration
- 3D Secure support
- Partial refund support
- Test and production modes

## License

LGPL-3

## Author

Arabian Admas Ltd Co
Principal Architect & Solutions Expert

## Credits

Based on the payment provider framework of Odoo v19
EdfaPay API Documentation: https://sandbox.edfapay.com/pgapi/EdfapayCheckout_Developer-API.html
