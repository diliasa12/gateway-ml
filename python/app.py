from flask import Flask, request, jsonify

app = Flask(__name__)

def klasifikasi(ph, lembap_udara):
    """
    Logika klasifikasi sederhana berdasarkan pH dan kelembapan udara.
    """
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
        ph = float(data["ph"])
        lembap_udara = float(data["lembap_udara"])
    except (ValueError, TypeError):
        return jsonify({"error": "Nilai 'ph' dan 'lembap_udara' harus berupa angka"}), 400

    hasil, confidence = klasifikasi(ph, lembap_udara)

    return jsonify({
        "prediksi": hasil,
        "nilai_confidence": confidence
    }), 200


if __name__ == '__main__':
    app.run(port=3001, debug=True)