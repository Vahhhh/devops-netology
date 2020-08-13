***1. Установите Hashicorp Vault в виртуальной машине Vagrant/VirtualBox.***

```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

***2. Запустить Vault-сервер в dev-режиме.***

```
vault server -dev

vagrant@vagrant:~$ vault server -dev
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.14.4
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.5.0

WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: BWMxxHEXz062ceR8gB7z3Y/NkVyCw+7l+/sS6WxpdUg=
Root Token: s.Z4d30aeflw8KPNHevss74Cgs

Development mode should NOT be used in production installations!
```

```
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN="s.Z4d30aeflw8KPNHevss74Cgs"

vagrant@vagrant:~$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.5.0
Cluster Name    vault-cluster-c2bda762
Cluster ID      0256ddac-3124-5bbd-d84f-ce275f51f651
HA Enabled      false
```

***3. Используя PKI Secrets Engine, создайте Root CA и Intermediate CA. Обратите внимание на дополнительные материалы по созданию CA в Vault, если с изначальной инструкцией возникнут сложности.***

- Root CA
```
vault secrets enable pki

vault secrets tune -max-lease-ttl=87600h pki

vault write -field=certificate pki/root/generate/internal \
        common_name="example.com" \
        ttl=87600h > CA_cert.crt

vault write pki/config/urls \
        issuing_certificates="http://127.0.0.1:8200/v1/pki/ca" \
        crl_distribution_points="http://127.0.0.1:8200/v1/pki/crl"
```

- Intermediate CA

```
vault secrets enable -path=pki_int pki

vault secrets tune -max-lease-ttl=43800h pki_int

vault write -format=json pki_int/intermediate/generate/internal \
        common_name="example.com Intermediate Authority" \
        | jq -r '.data.csr' > pki_intermediate.csr
        
vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
        format=pem_bundle ttl="43800h" \
        | jq -r '.data.certificate' > intermediate.cert.pem
        
vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem

```

- Создаём роль (хотя не уверен, что именно для наших целей это обязательно - но я стараюсь по документации делать)

```

vault write pki_int/roles/example-dot-com \
        allowed_domains="example.com" \
        allow_subdomains=true \
        max_ttl="720h"

```

***4. Согласно этой же инструкции, подпишите Intermediate CA csr на сертификат для тестового домена (например, netology.example.com если действовали согласно инструкции).***

`vault write pki_int/issue/example-dot-com common_name="netology.example.com" ttl="24h" > netology.out`

Дальше `private_key` я вручную через nano скопировал в `netology.key`
А остальное - в `netology.pem`, причём что важно - первым идёт `ca_chain` - его надо перенести ниже, чтобы первым шёл `certificate`.

Скорее всего, можно сделать через `-format=json` и `jq` - как один сертификат оттуда выцепить я понял, а вот необходимы ли `ca_chain`, `issuing_ca` - не смог найти.
Сейчас попробую...

```
vault write -format=json pki_int/issue/example-dot-com common_name="test.example.com" ttl="24h" > test.json
cat test.json | jq -r '.data.private_key' > test.key
cat test.json | jq -r '.data.certificate' > test.pem && cat test.json | jq -r '.data.issuing_ca' >> test.pem
```
РАБОТАЕТ! :)

***5. Поднимите на localhost nginx, сконфигурируйте default vhost для использования подписанного Vault Intermediate CA сертификата и выбранного вами домена. Сертификат из Vault подложить в nginx руками.***

```
sudo nano /etc/nginx/sites-enabled/default

server {
        # SSL configuration
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
        ssl_certificate /home/vagrant/netology.pem;
        ssl_certificate_key /home/vagrant/netology.key;

sudo systemctl restart nginx
```

***6. Модифицировав /etc/hosts и системный trust-store, добейтесь безошибочной с точки зрения HTTPS работы curl на ваш тестовый домен (отдающийся с localhost).***

```
sudo cp /home/vagrant/intermediate.cert.pem /usr/local/share/ca-certificates/intermediate.cert.crt
(можно было ln -s - но пусть в нормальном месте лежит)

sudo update-ca-certificates

sudo nano /etc/hosts
127.0.0.1       localhost netology.example.com


vagrant@vagrant:~$ curl https://netology.example.com
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

***7. Ознакомьтесь с протоколом ACME и CA Let's encrypt. Если у вас есть во владении доменное имя с платным TLS-сертификатом, который возможно заменить на LE, или же без HTTPS вообще, попробуйте воспользоваться одним из предложенных клиентов, чтобы сделать веб-сайт безопасным (или перестать платить за коммерческий сертификат).***

У меня в управлении есть CISCO ASA, на которой я через Certbot периодически обновляю сертификаты.
Правда чтобы закачать их на ASA, приходится поколдовать, но вот со стороны LINUX'а проблем нет.

Чтобы показать сертификат клиент не захотел подключаться (видимо несекьюрно) - пришлось сделать вот что.

```
vagrant@vagrant:~$ cat openssl.conf
openssl_conf = default_conf

[ default_conf ]

ssl_conf = ssl_sect

[ssl_sect]

system_default = ssl_default_sect

[ssl_default_sect]
MinProtocol = TLSv1
CipherString = DEFAULT:@SECLEVEL=1
```
`export OPENSSL_CONF=/home/vagrant/openssl.conf`

А вот и доказательство работы моего сертификата ;)

```
vagrant@vagrant:~$ openssl s_client -servername vpn.inteco.ru -connect vpn.inteco.ru:443
CONNECTED(00000003)
depth=2 O = Digital Signature Trust Co., CN = DST Root CA X3
verify return:1
depth=1 C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3
verify return:1
depth=0 CN = vpn.inteco.ru
verify return:1
---
Certificate chain
 0 s:CN = vpn.inteco.ru
   i:C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3
 1 s:C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3
   i:O = Digital Signature Trust Co., CN = DST Root CA X3
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIFUjCCBDqgAwIBAgISA5va+c/nDGf7W3sGchquAv8hMA0GCSqGSIb3DQEBCwUA
MEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD
ExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0yMDA2MjYxNDAzMzZaFw0y
MDA5MjQxNDAzMzZaMBgxFjAUBgNVBAMTDXZwbi5pbnRlY28ucnUwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQDXOxsScts72SZ6PPJc3TrUfX0Xn78WV/u6
Qc3HeP4HbyO8una9UXYITckeusvpXLvV3xc2dIdvi9stSQQJNL+QoiYLpP1MuCji
n1ZWODEpAjukauJYHcKlv8vdMV+9RaulPP7lySLCN115kTSiSAY0KPBAksY2ghFC
ZyfvfBaGJYmLGDV8sOOJsHdZTIW3eLkCHbP0PqSGZ/AZLJroMj7pleqazcLghNqu
DkrCZ2WErFdqIYv1Qkx7G22gmcNcwQ8EEJ+83Iealup19T0c0olPxTM5uONlRUmh
/ZNlloLq1MCQb04qEhgQlvtPHK739oo2YGEsbGaBaTqy7aEsLwdnAgMBAAGjggJi
MIICXjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUF
BwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFC2FbTSUW2pUXeq7FfE1iXZBF3XL
MB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMG8GCCsGAQUFBwEBBGMw
YTAuBggrBgEFBQcwAYYiaHR0cDovL29jc3AuaW50LXgzLmxldHNlbmNyeXB0Lm9y
ZzAvBggrBgEFBQcwAoYjaHR0cDovL2NlcnQuaW50LXgzLmxldHNlbmNyeXB0Lm9y
Zy8wGAYDVR0RBBEwD4INdnBuLmludGVjby5ydTBMBgNVHSAERTBDMAgGBmeBDAEC
ATA3BgsrBgEEAYLfEwEBATAoMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNl
bmNyeXB0Lm9yZzCCAQQGCisGAQQB1nkCBAIEgfUEgfIA8AB3AOcS8rA3fhpi+47J
DGGE8ep7N8tWHREmW/Pg80vyQVRuAAABcvEny8MAAAQDAEgwRgIhAOLuHB89iZTN
ogTnkQBp8VvBjK2DQk1L64X2rEV1vqPEAiEAvh1zTBDQJarFFExBFdu/LTp7W3q9
D9i6JvNIrEPCr18AdQAHt1wb5X1o//Gwxh0jFce65ld8V5S3au68YToaadOiHAAA
AXLxJ8v1AAAEAwBGMEQCIANcUN+lZyFUUuGBcJBPn8O8eKuT1MmJDgMdijZOydob
AiBC58j1NlpWy21aBkwNyVe+ub8eBqqezz4i2CdZGf56ajANBgkqhkiG9w0BAQsF
AAOCAQEAmhEtl5pkWJvBvOM92FJlCEM6AP+DEawsXAIcMIQASMx8N2x0N1KCiHbW
ea2EzEgbg3ONP/TJYPz1QiqDvJn5Zd0KK1aghGRfAdMKplXVbS2fYZYu8zuG1bR2
yJoiWZaVkk0xNQ6EPRwzajuFRpUpIC0iKKXBFygHlXwUsCMOxBNIsorcPikGSfK6
/Vu3SDNDiyiprwPXDb/OyVO4BQdhaq9kMFobRADmzEXTSsxRdpJvGe49CIHdr+Fb
3g4bp/pN03nwpzwpLIOU9sPZULHYSmDpgNaMt76SjlIKaXVz/yTsoWLIq/viWnMS
Wf9q2hfYu+9n3kz3yKhywAXalpikKA==
-----END CERTIFICATE-----
subject=CN = vpn.inteco.ru

issuer=C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3

---
No client certificate CA names sent
Peer signing digest: MD5-SHA1
Peer signature type: RSA
Server Temp Key: DH, 1024 bits
---
SSL handshake has read 3235 bytes and written 513 bytes
Verification: OK
---
New, SSLv3, Cipher is DHE-RSA-AES256-SHA
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1
    Cipher    : DHE-RSA-AES256-SHA
    Session-ID: F1A19CB4E148BABA75351D5B204C6CAF3F649102D771356DE75E781A85A73EB9
    Session-ID-ctx:
    Master-Key: 03E3EA4F89D59C597DEC8CEAE0A28D9D7EEAA166C899C6C10A6B18EF97ABF0CD75587C77DF632A6860B1999B0FFB3E0F
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    Start Time: 1597332939
    Timeout   : 7200 (sec)
    Verify return code: 0 (ok)
    Extended master secret: no
---
```

***8.Вместо ручного подкладывания сертификата в nginx, воспользуйтесь Consul для автоматического подтягивания сертификата из Vault.***

Сделал. Одно напрягает, что это всё почти копипастом... :)
Но работает - огонь!!

```
watch -n 5 "curl --cacert /home/vagrant/CA_cert.crt --insecure -v https://new.example.com 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }'"

Every 5.0s: curl --cacert /home/vagrant/CA_cert.crt --insecure -v https://new.exam...  vagrant: Thu Aug 13 16:52:15 2020

* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server accepted to use http/1.1
* Server certificate:
*  subject: CN=new.example.com
*  start date: Aug 13 16:50:21 2020 GMT
*  expire date: Aug 13 16:52:50 2020 GMT
*  issuer: CN=example.com Intermediate Authority
*  SSL certificate verify ok.
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
* Mark bundle as not supporting multiuse
* Connection #0 to host new.example.com left intact


Every 5.0s: curl --cacert /home/vagrant/CA_cert.crt --insecure -v https://new.exam...  vagrant: Thu Aug 13 16:53:09 2020

* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server accepted to use http/1.1
* Server certificate:
*  subject: CN=new.example.com
*  start date: Aug 13 16:50:21 2020 GMT
*  expire date: Aug 13 16:52:50 2020 GMT
*  issuer: CN=example.com Intermediate Authority
*  SSL certificate verify result: certificate has expired (10), continuing anyway.
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
* Mark bundle as not supporting multiuse
* Connection #0 to host new.example.com left intact
```
