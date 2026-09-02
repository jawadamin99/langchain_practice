import random
import string
from config.db_connector import db_conn


class AssignmentHelper:
    thread_id = ""

    def generate_thread_id(self):
        while True:
            random_part = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=5)
            )

            thread_id = "JWD_" + random_part

            if not self.thread_exists(thread_id):
                self.thread_id = thread_id

                db_conn.execute(
                    "INSERT INTO thread_list (thread_id) VALUES (?)",
                    (thread_id,)
                )
                db_conn.commit()
                return thread_id

    def thread_exists(self, thread_id):
        cursor = db_conn.cursor()

        cursor.execute(
            "SELECT thread_id FROM thread_list WHERE thread_id = ?",
            (thread_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return False

        return True

    def save_message(self, thread_id,app_code, role, content):
        db_conn.execute(
            "INSERT INTO conversations (thread_id,app_code, role, content) VALUES (?, ?, ?, ?)",
            (thread_id, app_code, role, content)
        )
        db_conn.commit()
