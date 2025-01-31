`pip install python-decouple`

`Create an Environment File: Create a .env file in the root directory of your project.`

#### Example .env settings

```
SECRET_KEY=Key
DEBUG=True
```

#### SMTP settings

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com  # Replace with your SMTP server
EMAIL_PORT=587  # Or the appropriate port for your provider
EMAIL_USE_TLS=True  # Use TLS if required by your provider
EMAIL_HOST_USER=your_email@example.com  # sender's email-id
EMAIL_HOST_PASSWORD=your_password  #password associated with above email-id
```

#### Remember to remove comment in front of value definitions
