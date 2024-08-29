from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient


key_vault_url = "https://artiekeyvault.vault.azure.net/"

# 32바이트(256비트) 키 생성 또는 지정
key = b'0123456789abcdef0123456789abcdef'  # 예제에서는 고정된 32바이트 키를 사용

def encrypt_file(input_file, output_file):
    # 파일 읽기
    with open(input_file, 'rb') as f:
        data = f.read()

    # 16바이트(128비트) IV 생성
    iv = get_random_bytes(16)

    # AES 암호화 설정 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 데이터 패딩 및 암호화
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # 암호화된 데이터와 IV를 함께 파일에 저장
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

def decrypt_file(input_file, output_file):
    # 암호화된 파일 읽기
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # 첫 16바이트는 IV
        encrypted_data = f.read()

    # AES 복호화 설정 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 복호화 및 패딩 제거
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # 복호화된 데이터 저장
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

# 테스트 실행
# 암호화
encrypt_file('240829_운영 파이프라인 검수 결과.pptx', '240829_운영 파이프라인 검수 결과_crypto.pptx')

# 복호화
decrypt_file('240829_운영 파이프라인 검수 결과_crypto.pptx', '240829_운영 파이프라인 검수 결과_after.pptx')

# 'decrypted_blob_file.bin'은 원래 파일과 동일해야 합니다.
