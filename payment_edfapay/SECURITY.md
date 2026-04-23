# Security Documentation

## Overview

The EdfaPay Payment Gateway module implements multiple security layers to ensure safe payment processing and protect sensitive merchant and customer data.

## Security Features

### 1. Credential Protection

**Encrypted Storage**:
- All merchant credentials (Merchant Key and Password) are stored encrypted in the Odoo database
- Passwords are never logged or displayed in plain text
- UI fields use `password="True"` attribute to mask sensitive data

**Access Control**:
- Credential fields restricted to `base.group_system` (System administrators)
- Only authorized users can view/modify payment provider settings

### 2. Request Signature Validation

**Hash Calculation**:
```python
# All requests to EdfaPay are signed with SHA1(MD5(data))
hash_string = f"{order_id}{amount}{currency}{description}{password}"
hash_md5 = hashlib.md5(hash_string.upper().encode('utf-8')).hexdigest()
hash_value = hashlib.sha1(hash_md5.encode('utf-8')).hexdigest()
```

**Protection Against**:
- Request tampering
- Man-in-the-middle attacks
- Replay attacks
- Unauthorized API access

### 3. HTTPS Communication

**Requirements**:
- All communication with EdfaPay uses HTTPS
- SSL/TLS certificates must be valid
- Production URLs enforce HTTPS

**Endpoints**:
- Production: `https://api.edfapay.com`
- Sandbox: `https://sandbox.edfapay.com`

### 4. Webhook Security

**Validation**:
- Incoming webhooks validated against expected signature
- Only POST requests accepted
- CSRF protection disabled for webhook endpoint (required for external calls)
- Session not saved for webhook calls

**Endpoint Security**:
```python
@http.route('/payment/edfapay/webhook',
    type='http',
    auth='public',
    methods=['POST'],
    csrf=False,
    save_session=False
)
```

### 5. Data Sanitization

**Input Validation**:
- All user inputs validated before processing
- Amount format enforced (2 decimal places)
- Currency codes validated against supported list
- Order IDs sanitized to prevent injection

**Output Encoding**:
- HTML entities escaped in templates
- SQL injection prevented through ORM usage
- No raw SQL queries

### 6. Transaction State Management

**State Validation**:
- Transaction states follow defined workflow
- State transitions validated
- Duplicate transaction prevention

**States**:
- draft → pending → done/canceled/error
- Invalid state transitions blocked

## Security Best Practices

### For Administrators

1. **Credential Management**:
   ```
   ✓ Use strong, unique passwords
   ✓ Rotate credentials periodically
   ✓ Never share credentials via email/chat
   ✓ Store credentials in password manager
   ✗ Don't reuse passwords across systems
   ✗ Don't store credentials in plain text files
   ```

2. **Access Control**:
   ```
   ✓ Limit admin access to necessary personnel
   ✓ Use separate accounts (no shared logins)
   ✓ Enable two-factor authentication for Odoo
   ✓ Regularly review user access
   ✗ Don't use generic admin accounts
   ✗ Don't grant unnecessary system access
   ```

3. **Environment Separation**:
   ```
   ✓ Use different credentials for test/production
   ✓ Test in sandbox before going live
   ✓ Keep test and production data separate
   ✗ Don't use production credentials in test
   ✗ Don't test with real payment data
   ```

### For Developers

1. **Code Security**:
   ```python
   # ✓ Good: Use ORM
   transactions = self.env['payment.transaction'].search([
       ('reference', '=', reference)
   ])
   
   # ✗ Bad: Raw SQL
   self.env.cr.execute("SELECT * FROM payment_transaction WHERE reference = '%s'" % reference)
   ```

2. **Logging**:
   ```python
   # ✓ Good: Log without sensitive data
   _logger.info("Processing transaction %s", self.reference)
   
   # ✗ Bad: Log sensitive data
   _logger.info("Transaction: %s, Password: %s", self.reference, self.provider_id.edfapay_password)
   ```

3. **Error Handling**:
   ```python
   # ✓ Good: Generic error messages
   raise ValidationError(_("Payment processing failed. Please try again."))
   
   # ✗ Bad: Expose internal details
   raise ValidationError(_("Hash mismatch: expected %s, got %s") % (hash1, hash2))
   ```

### For Merchants

1. **SSL/TLS Configuration**:
   - Use valid SSL certificates (not self-signed)
   - Keep certificates up to date
   - Use TLS 1.2 or higher
   - Configure HSTS headers

2. **Server Security**:
   - Keep Odoo and OS updated
   - Configure firewall properly
   - Use fail2ban or similar
   - Regular security audits
   - Monitor logs for suspicious activity

3. **Network Security**:
   - Restrict database access
   - Use VPN for remote administration
   - Disable unnecessary services
   - Implement intrusion detection

## Compliance Considerations

### PCI DSS

**What This Module Does**:
- ✓ Never stores full card numbers
- ✓ Never stores CVV/CVC codes
- ✓ Redirects to PCI-compliant gateway
- ✓ Uses secure communication (HTTPS)
- ✓ Implements access controls

**Merchant Responsibilities**:
- Maintain PCI DSS compliance for Odoo environment
- Conduct regular security scans
- Complete SAQ (Self-Assessment Questionnaire)
- Maintain security policies
- Train staff on security practices

### GDPR

**Data Processing**:
- Customer data processed for payment only
- Data retention follows Odoo's policies
- Customers can request data deletion
- Transaction logs include necessary data only

**Merchant Responsibilities**:
- Maintain privacy policy
- Obtain customer consent
- Handle data subject requests
- Implement data protection measures
- Appoint DPO if required

## Incident Response

### Security Incident Checklist

1. **Detection**:
   - Monitor logs for anomalies
   - Set up alerts for failed transactions
   - Review webhook delivery failures

2. **Containment**:
   - Disable provider if breach suspected
   - Rotate credentials immediately
   - Block suspicious IP addresses

3. **Investigation**:
   - Review transaction logs
   - Check access logs
   - Identify affected transactions
   - Document findings

4. **Recovery**:
   - Restore from backup if needed
   - Update security measures
   - Re-enable with new credentials

5. **Notification**:
   - Notify EdfaPay if their system involved
   - Inform affected customers if required
   - Report to authorities if mandated

## Security Audit Checklist

### Monthly
- [ ] Review failed transaction logs
- [ ] Check webhook delivery rates
- [ ] Verify SSL certificate validity
- [ ] Review user access logs

### Quarterly
- [ ] Rotate payment credentials
- [ ] Update dependencies
- [ ] Security patch review
- [ ] Access control audit

### Annually
- [ ] Full security audit
- [ ] Penetration testing
- [ ] PCI DSS compliance review
- [ ] Update security policies

## Known Security Limitations

1. **Callback URL Authentication**:
   - Webhooks use public endpoint
   - Rely on signature validation
   - Consider IP whitelisting if EdfaPay provides static IPs

2. **Rate Limiting**:
   - Not implemented in module
   - Should be configured at nginx/Apache level
   - Prevents brute force attacks

3. **Session Management**:
   - Standard Odoo session management
   - Consider additional authentication for payment settings

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. Email security details to: [your security contact]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

4. Allow reasonable time for fix before public disclosure

## Security Resources

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **PCI DSS**: https://www.pcisecuritystandards.org/
- **Odoo Security**: https://www.odoo.com/page/security
- **EdfaPay Security**: Contact EdfaPay support

---

**Last Updated**: November 2025  
**Version**: 1.0.0
