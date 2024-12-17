# Verinin ortalama ve top 3 ortalama hesaplanması
def preprocess_data(data):
    # Ortalama
    mean_value = sum(data) / len(data)

    # En büyük 3 değeri bul
    top_3 = sorted(data, reverse=True)[:3]
    top_3_mean = sum(top_3) / len(top_3)

    return mean_value, top_3_mean  # İki değeri döndürür
