from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


db_config = {
    "host":     "localhost",
    "user":     "mahasiswa",
    "password": "akucintafik",
    "database": "2410511078_ml_service"
}


def klasifikasi(ph, lembap_udara):
    if ph < 5.5:
        return "Terlalu Asam", 0.92
    elif ph > 7.5:
        return "Terlalu Basa", 0.90
    elif lembap_udara < 60:
        return "Kering", 0.88
    elif lembap_udara > 90:
        return "Terlalu Lembap", 0.87
    else:
        return "Ideal", 0.85



@app.route('/prediksi', methods=['POST'])
def prediksi():
    data = request.get_json()

    # Validasi input
    if not data:
        return jsonify({"error": "Body JSON tidak ditemukan"}), 400

    if "ph" not in data or "lembap_udara" not in data:
        return jsonify({"error": "Field 'ph' dan 'lembap_udara' wajib diisi"}), 400

    try:
        ph           = float(data["ph"])
        lembap_udara = float(data["lembap_udara"])
    except (ValueError, TypeError):
        return jsonify({"error": "Nilai 'ph' dan 'lembap_udara' harus berupa angka"}), 400

    # Klasifikasi
    hasil, confidence = klasifikasi(ph, lembap_udara)

   
    try:
        conn   = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO hasil_prediksi (ph, lembap_udara, prediksi, nilai_confidence, created_at)
               VALUES (%s, %s, %s, %s, NOW())""",
            (ph, lembap_udara, hasil, confidence)
        )

        conn.commit()
        inserted_id = cursor.lastrowid

    except mysql.connector.Error as e:
        return jsonify({"error": "Gagal menyimpan ke database", "detail": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

    return jsonify({
        "id":               inserted_id,
        "prediksi":         hasil,
        "nilai_confidence": confidence
    }), 200


if __name__ == '__main__':
    app.run(port=3001, debug=True)