TOKEN_BOT = '5921929527:AAFCgDQoUS8yBA77PlDA8CnIXb0OkIIiiJU'
SECRET_OPENAI = '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'

DB_HOST = "95.163.237.220"
DB_USER = "root"
DB_PASSWORD = "iW7kH8tG3zfZ"
DB_NAME = "dalle"

WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN_BOT)

