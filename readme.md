Cấu trúc tài liệu
1. Elliptic Curve Cryptography (ECC) Fundamentals
1.1. Định nghĩa đường cong elliptic
1.2. Phép cộng điểm trên đường cong elliptic
1.3. Phép nhân vô hướng (Scalar Multiplication)
1.4. Bài toán Discrete Logarithm trên ECC (ECDLP)
1.5. Các tham số domain (curve parameters)
2. ECDSA (Elliptic Curve Digital Signature Algorithm)
2.1. Tổng quan về chữ ký số
2.2. Quy trình tạo khóa (Key Generation)
2.3. Quy trình ký (Signature Generation)
2.4. Quy trình xác minh (Signature Verification)
3. Vai trò của Nonce trong ECDSA
3.1. Nonce là gì và tại sao cần nonce?
3.2. Yêu cầu bảo mật của nonce
3.3. Các phương pháp sinh nonce (RFC 6979)
4. Nonce Reuse Attack
4.1. Mô tả lỗ hổng
4.2. Phân tích toán học của attack
4.3. Khôi phục private key từ hai chữ ký
4.4. Case studies thực tế (Sony PS3, Bitcoin wallets)
5. Demonstration
5.1. Triển khai attack trên Python
5.2. Ví dụ với curve cụ thể (secp256k1)
6. Biện pháp phòng chống
6.1. Deterministic nonce generation (RFC 6979)
6.2. Best practices trong implementation


resource:
https://curves.xargs.org/




1. AES-GCM Fundamentals
1.1. AES Block Cipher
1.2. Counter Mode (CTR)
1.3. GHASH và Galois Field $GF(2^{128})$
1.4. Cấu trúc AES-GCM (Encryption + Authentication)
2. Vai trò của Nonce trong AES-GCM
2.1. Nonce là gì và yêu cầu bảo mật
2.2. Tại sao nonce phải unique?
3. Forbidden Attack
3.1. Mô tả lỗ hổng
3.2. Khôi phục Authentication Key $H$
3.3. Giải mã plaintext (XOR attack)
3.4. Forgery - Tạo ciphertext giả mạo
4. Case Studies
4.1. TLS 1.2 với AES-GCM
4.2. Các lỗi implementation thực tế
5. Demonstration
Challenge: Decrypt và forge message
6. Biện pháp phòng chống
6.1. Nonce construction (counter-based vs random)
6.2. AES-GCM-SIV (nonce-misuse resistant)

resources
https://frereit.de/aes_gcm/