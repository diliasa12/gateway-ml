import express from "express";
import axios from "axios";
import { rateLimit } from "express-rate-limit";
const app = express();
app.use(express.json());
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // Jendela waktu 15 menit
  max: 10, // Maksimal 10 permintaan per IP dalam 15 menit
  message: "Terlalu banyak permintaan, coba lagi setelah 15 menit.", // Pesan jika limit terlampaui
  standardHeaders: true, // Menambahkan header RateLimit-* ke response
  legacyHeaders: false, // Menonaktifkan X-RateLimit-* header
});
// URL Python ML Service
const ML_SERVICE_URL = "http://localhost:3001/prediksi";
app.use(apiLimiter);
app.post("/klasifikasi", async (req, res) => {
  const { ph, lembap_udara } = req.body;

  if (ph === undefined || lembap_udara === undefined) {
    return res.status(400).json({
      error: "Field 'ph' dan 'lembap_udara' wajib diisi",
    });
  }

  try {
    const response = await axios.post(ML_SERVICE_URL, {
      ph,
      lembap_udara,
    });

    const { prediksi, nilai_confidence } = response.data;

    return res.status(200).json({
      input: {
        ph,
        lembap_udara,
      },
      prediksi,
      model_confidence: nilai_confidence,
    });
  } catch (error) {
    console.error("Error menghubungi ML Service:", error.message);
    return res.status(502).json({
      error: "Gagal menghubungi ML Service",
      detail: error.message,
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`API Gateway berjalan di http://localhost:${PORT}`);
});
