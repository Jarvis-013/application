import random
import datetime
# import datetime
import hashlib
from database import get_db_connection

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def send_otp(user_id: str, phone_number: str, user_type: str) -> str | None:
    otp = str(random.randint(100000, 999999))
    otp_hash = hash_otp(otp)
    now = datetime.datetime.now()
    expires_at = now + datetime.timedelta(minutes=2)

    conn = get_db_connection()
    if not conn:
        print("[ERROR] Cannot send OTP, DB connection failed.")
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE OTPs
            SET expires_at = ?
            WHERE user_id = ? AND user_type = ? AND expires_at > ?
        """, (now, user_id, user_type, now))

        cursor.execute("""
            INSERT INTO OTPs (user_id, otp_hash, created_at, expires_at, user_type, used)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (user_id, otp_hash, now, expires_at, user_type))

        conn.commit()
        print(f"[INFO] OTP for {user_type} {user_id}: {otp}")
        return otp

    except Exception as e:
        print(f"[ERROR] Failed to insert OTP: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def verify_otp_code(user_id: str, otp_input: str, user_type: str) -> bool:
    print(f"[INFO] Starting OTP verification for {user_type} ID: {user_id}")

    conn = get_db_connection()
    if conn is None:
        print("[ERROR] DB connection failed.")
        return False

    try:
        cursor = conn.cursor()

        # Remove expired OTPs
        cursor.execute("DELETE FROM OTPs WHERE expires_at < GETDATE()")

        # Get the latest valid OTP
        cursor.execute("""
            SELECT TOP 1 id, otp_hash FROM OTPs
            WHERE user_id = ? AND user_type = ? AND expires_at > GETDATE() AND used = 0
            ORDER BY created_at DESC
        """, (user_id, user_type))
        row = cursor.fetchone()

        if row:
            otp_hash_input = hash_otp(otp_input)
            print(f"[DEBUG] Input Hash: {otp_hash_input}, Stored Hash: {row.otp_hash if hasattr(row, 'otp_hash') else row[1]}")

            if otp_hash_input == row[1]:
                cursor.execute("UPDATE OTPs SET used = 1 WHERE id = ?", (row[0],))
                conn.commit()
                print("[INFO] OTP verified and marked as used.")
                return True
            else:
                print("[WARN] OTP mismatch.")
        else:
            print("[WARN] No valid OTP found for given user.")

        return False

    except Exception as e:
        print("[ERROR] OTP verification failed:", e)
        return False

    finally:
        cursor.close()
        conn.close()
