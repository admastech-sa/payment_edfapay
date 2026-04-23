# Changelog

All notable changes to the EdfaPay Payment Gateway module will be documented in this file.

## [1.0.1] - 2025-11-16

### Fixed
- **CRITICAL**: Added missing payment method definitions
- Payment Methods section now displays "Credit/Debit Card"
- Provider now accessible on website checkout
- Default payment method properly configured

### Added
- Payment method record for Credit/Debit Card
- `_get_default_payment_method_id()` method in payment provider model
- Payment method linking in data file

### Technical Changes
- File: `data/payment_provider_data.xml`
  - Added `payment_method_edfapay_card` record
  - Added `payment_method_ids` field to provider
- File: `models/payment_provider.py`
  - Added `_get_default_payment_method_id()` override

### Migration Notes
- **Breaking Change**: Requires uninstall and reinstall (or upgrade)
- Configuration will be preserved during upgrade
- Fresh installations will have payment methods included

## [1.0.0] - 2025-11-15

### Added
- Initial release of EdfaPay Payment Gateway integration for Odoo v19
- Complete payment initiation via REST API
- Support for SALE transactions
- 3D Secure redirect handling
- Webhook integration for payment callbacks
- Return URL handling for customer redirects
- Multi-currency support (SAR, AED, USD, EUR, GBP, etc.)
- Test and production environment support
- SHA1-MD5 hash signature validation
- Partial refund support
- Real-time transaction status updates
- Comprehensive error handling and logging
- Security features:
  - Encrypted credential storage
  - Password masking in UI
  - HTTPS communication
  - Request signature validation

### Supported Features
- Payment Methods: Credit/Debit Cards
- Transaction Types: SALE
- Refunds: Full and Partial
- 3D Secure: Yes
- Tokenization: Framework ready (future enhancement)
- Recurring Payments: Framework ready (future enhancement)

### API Endpoints
- Payment Initiate: `/payment/initiate`
- Return URL: `/payment/edfapay/return`
- Webhook: `/payment/edfapay/webhook`

### Configuration Requirements
- Odoo 19.0
- EdfaPay Merchant Account
- Valid Merchant Key (UUID format)
- Valid Password
- Accessible callback URLs

### Known Limitations (v1.0.0)
- ⚠️ Payment methods not included (FIXED in v1.0.1)
- Tokenization not yet implemented (planned for v1.2)
- Recurring payments not yet implemented (planned for v1.2)
- AUTH-only transactions not implemented (SALE only)

## Future Enhancements (Roadmap)

### [1.1.0] - Planned
- Enhanced error handling
- Additional logging
- Performance optimizations
- UI improvements

### [1.2.0] - Planned
- Card tokenization support
- Recurring payment implementation
- AUTH and CAPTURE workflow
- Advanced refund management

### [1.3.0] - Planned
- Apple Pay integration
- Additional payment method support
- Transaction analytics dashboard
- Enhanced reporting features

---

For detailed API documentation, see: https://sandbox.edfapay.com/pgapi/EdfapayCheckout_Developer-API.html
