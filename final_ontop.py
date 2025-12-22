import os
import time
import subprocess
import base64
import urllib.request
import jaydebeapi
import socket  # Needed to catch socket.timeout

timeout_seconds = 30 
# ============================================================
# CONFIGURATION
# ============================================================

# H2 setup
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

jdbc_driver = "org.h2.Driver"
jdbc_url = "jdbc:h2:~/pregnancy_db"
jdbc_user = "sa"
jdbc_password = ""
h2_jar_path = "/Users/admin/Downloads/h2/bin/h2-2.4.240.jar"

# Ontop setup 
ONTOP_DIR = "/Users/admin/Downloads/ontop-cli-5.4.0"    
ONTOP_EXISTS = os.path.exists(ONTOP_DIR)

# RDF + AllegroGraph endpoint
username = "admin"
password = "91v1BzU8ac6jzeNkn6jTTa"
endpoint_url = "https://ag1ujtnj93md49vl.allegrograph.cloud/repositories/pregnancy/statements"
rdf_file_path = "/Users/admin/Downloads/ontop-cli-5.4.0/test_output.rdf"

# ============================================================
# DATABASE CONNECTION HELPER
# ============================================================
def get_h2_connection():
    return jaydebeapi.connect(
        jdbc_driver,
        jdbc_url,
        [jdbc_user, jdbc_password],
        h2_jar_path
    )

# ============================================================
# STEP 1: FETCH UNPROCESSED VISITS
# ============================================================
def fetch_unprocessed_visits():
    try:
        conn = get_h2_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                v.visit_id,
                p.patient_id, p.first_name, p.last_name, p.gender,
                p.age_years, p.age_months, p.phone_number, p.country,
                v.visit_date, v.visit_time, v.visit_type, v.priority_status,
                d.diagnosis_id, d.diagnosis_type, d.icd10_code, d.description,
                d.recorded_at
            FROM Diagnosis d
            JOIN Visit v ON d.visit_id = v.visit_id
            JOIN Patient p ON v.patient_id = p.patient_id
            WHERE d.IS_PROCESSED = FALSE
            ORDER BY v.visit_id, d.diagnosis_id
        """)
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            print("No unprocessed visits found.")
            return None
        grouped = {}
        for r in rows:
            visit_id = r[0]
            if visit_id not in grouped:
                grouped[visit_id] = []
            grouped[visit_id].append(r)
        print(f"Found {len(grouped)} unprocessed visits.")
        return grouped
    except Exception as e:
        print(f"[ERROR] fetch_unprocessed_visits(): {e}")
        return None

# ============================================================
# STEP 1B: POPULATE STAGING TABLE
# ============================================================
def populate_staging_table(grouped_data):
    try:
        conn = get_h2_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS STAGING_VISIT_RDF")
        cursor.execute("""
            CREATE TABLE STAGING_VISIT_RDF (
                visit_id VARCHAR(20),
                patient_id VARCHAR(20),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                gender VARCHAR(20),
                age_years INT,
                age_months INT,
                phone_number VARCHAR(20),
                country VARCHAR(50),
                visit_date DATE,
                visit_time TIME,
                visit_type VARCHAR(20),
                priority_status VARCHAR(20),
                diagnosis_list CLOB
            )
        """)
        for visit_id, rows in grouped_data.items():
            first = rows[0]
            diagnosis_text = "\n".join(
                f"[{r[13]}] {r[14]} - {r[15]} - {r[16]}"
                for r in rows
            )
            cursor.execute("""
                INSERT INTO STAGING_VISIT_RDF VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                first[0], first[1], first[2], first[3], first[4],
                first[5], first[6], first[7], first[8],
                first[9], first[10], first[11], first[12],
                diagnosis_text
            ])
        conn.commit()
        conn.close()
        print("Staging table populated.")
        return True
    except Exception as e:
        print(f"[ERROR] populate_staging_table(): {e}")
        return False

# ============================================================
# STEP 2: ONTOP MATERIALIZATION
# ============================================================
# def run_ontop_materialize():
#     if not ONTOP_EXISTS:
#         print("[WARNING] Ontop not installed — skipping materialization.")
#         return False
#     try:
#         command = [
#             os.path.join(ONTOP_DIR, "ontop"),
#             "materialize",
#             "-m", "Second_mapping_1.ttl",
#             "-o", rdf_file_path,
#             "-p", "ontop.properties"
#         ]
#         result = subprocess.run(
#             command,
#             cwd=ONTOP_DIR,
#             check=True,
#             text=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )
#         print(result.stdout)
#         print("Ontop materialization completed.")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Ontop materialize failed: {e}")
#         return False

def run_ontop_materialize():
    if not ONTOP_EXISTS:
        print("[WARNING] Ontop not installed — skipping materialization.")
        return False
    try:
        command = [
            os.path.join(ONTOP_DIR, "ontop"),
            "materialize",
            "-m", "mapping-dataset01.ttl",
            "-o", rdf_file_path,
            "-p", "ontop.properties"
        ]
        result = subprocess.run(
            command,
            cwd=ONTOP_DIR,
            check=False,     # <- IMPORTANT: allow capture of stderr
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print("=== ONTOP STDOUT ===")
        print(result.stdout)

        print("=== ONTOP STDERR ===")
        print(result.stderr)

        if result.returncode != 0:
            print(f"[ERROR] Ontop exit code: {result.returncode}")
            return False

        print("Ontop materialization completed.")
        return True

    except Exception as e:
        print(f"[ERROR] Ontop materialize crashed: {e}")
        return False


# ============================================================
# STEP 3: UPLOAD RDF TO ALLEGROGRAPH
# ============================================================
# def upload_rdf():
#     if not os.path.exists(rdf_file_path):
#         print(f"[ERROR] RDF not found: {rdf_file_path}")
#         return False
#     try:
#         with open(rdf_file_path, "rb") as f:
#             rdf_data = f.read()
#         request = urllib.request.Request(
#             url=endpoint_url,
#             data=rdf_data,
#             method="POST",
#             headers={
#                 "Content-Type": "application/rdf+xml",
#                 "Authorization": "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
#             }
#         )
#         response = urllib.request.urlopen(request)
#         print("Upload status:", response.status)
#         return response.status in [200, 204]
#     except Exception as e:
#         print(f"[ERROR] upload_rdf(): {e}")
#         return False

def upload_rdf():
    if not os.path.exists(rdf_file_path):
        print(f"[ERROR] RDF file not found: {rdf_file_path}")
        return False

    try:
        with open(rdf_file_path, "rb") as f:
            rdf_data = f.read()

        headers = {
            "Content-Type": "application/rdf+xml",
            "Authorization": "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
        }

        request = urllib.request.Request(
            url=endpoint_url,
            data=rdf_data,
            method="POST",
            headers=headers
        )

        # Set a timeout to avoid hanging
        response = urllib.request.urlopen(request, timeout=timeout_seconds)
        print("Upload status:", response.status)
        if response.status in [200, 204]:
            print("[SUCCESS] RDF uploaded successfully!")
            return True
        else:
            print(f"[WARNING] Unexpected response status: {response.status}")
            return False

    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR] Code: {e.code}, Reason: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"[URL ERROR] Reason: {e.reason}")
        return False
    except socket.timeout:
        print(f"[TIMEOUT ERROR] Upload timed out after {timeout_seconds} seconds")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

# Call the function
upload_rdf()


# ============================================================
# STEP 4: MARK DIAGNOSIS AS PROCESSED
# ============================================================
def mark_diagnoses_processed(grouped_data):
    try:
        conn = get_h2_connection()
        cursor = conn.cursor()
        all_diag_ids = []
        for visit_id, rows in grouped_data.items():
            diag_ids = [r[13] for r in rows]
            all_diag_ids.extend(diag_ids)
        cursor.executemany(
            "UPDATE Diagnosis SET is_processed = TRUE WHERE diagnosis_id = ?",
            [(d,) for d in all_diag_ids]
        )
        conn.commit()
        conn.close()
        print(f"Marked {len(all_diag_ids)} diagnoses as processed.")
    except Exception as e:
        print(f"[ERROR] mark_diagnoses_processed(): {e}")

# ============================================================
# MAIN LOOP
# ============================================================
while True:
    grouped = fetch_unprocessed_visits()
    if grouped:
        if populate_staging_table(grouped):
            if run_ontop_materialize():
                if upload_rdf():
                    mark_diagnoses_processed(grouped)
    time.sleep(60)
