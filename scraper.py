import requests
from bs4 import BeautifulSoup
import json
import os
import re

# --- CONFIGURATION ---
TARGET_URL = "https://www.visaovip.com/es/"
MANUAL_PRICES_FILE = "data/precios_manuales.json"
MANUAL_PRODUCTS_FILE = "data/productos_manuales.json"
OUTPUT_FILE = "data/productos.json"
MARKUP = 1.20  # 20% increase

def get_manual_products():
    if os.path.exists(MANUAL_PRODUCTS_FILE):
        try:
            with open(MANUAL_PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception as e:
            print(f"[WARNING] Error al leer productos manuales: {e}")
    return []

def get_manual_prices():
    if os.path.exists(MANUAL_PRICES_FILE):
        try:
            with open(MANUAL_PRICES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Intento obtener precios de "descripciones_manuales"
                manual_data = data.get("descripciones_manuales", {})

                # Si "descripciones_manuales" está vacío, buscamos precios en la raíz del JSON
                if not manual_data:
                    manual_data = {k: v for k, v in data.items() if k != "descripciones_manuales" and isinstance(v, (int, float))}

                return {k.strip().lower(): v for k, v in manual_data.items()}
        except Exception as e:
            print(f"[WARNING] Error al leer precios manuales: {e}")
    return {}

def clean_price(price_text):
    if not price_text:
        return 0.0
    try:
        price_text = price_text.replace('U$', '').strip()
        # Handle comma as decimal separator (e.g. 555,00 -> 555.00)
        if ',' in price_text and '.' not in price_text:
            price_text = price_text.replace(',', '.')
        # Handle dot as thousand separator and comma as decimal (e.g. 1.200,00 -> 1200.00)
        elif '.' in price_text and ',' in price_text:
            price_text = price_text.replace('.', '').replace(',', '.')
        return float(re.sub(r'[^0-9.]', '', price_text))
    except Exception:
        return 0.0

def calculate_final_price(name, current_price, manual_prices):
    name_normalized = name.strip().lower()
    # Priority: Manual Price > Current Price * MARKUP
    if name_normalized in manual_prices:
        return float(manual_prices[name_normalized])

    # Búsqueda por subcadena para facilitar la coincidencia manual
    for key, val in manual_prices.items():
        if key in name_normalized and len(key) >= 5:
            return float(val)

    return current_price * MARKUP

def scrape_products():
    print(f"[INFO] Iniciando scraping de {TARGET_URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari(537.36"
    }

    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Error al acceder a la web: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products_data = []
    manual_prices = get_manual_prices()

    links = soup.find_all('a', href=re.compile(r'/es/prod/'))

    for link in links:
        try:
            name_el = link.find('p', class_=re.compile(r'text-black-alpha-90'))
            if not name_el:
                continue
            name = name_el.get_text(strip=True)

            orig_el = link.find('p', class_=re.compile(r'text-line-through'))
            dest_el = link.find('p', class_=re.compile(r'PrecoDestacado'))

            orig_price_text = orig_el.get_text(strip=True) if orig_el else ""
            dest_price_text = dest_el.get_text(strip=True) if dest_el else ""

            if not orig_price_text and dest_price_text:
                orig_price_text = dest_price_text

            original_price = clean_price(orig_price_text)
            price_val = clean_price(dest_price_text)

            if price_val == 0.0:
                continue

            img_tag = link.find('img')
            img_url = img_tag['src'] if img_tag else "https://via.placeholder.com/300"
            if img_url.startswith('/'):
                img_url = "https://www.visaovip.com" + img_url

            category = "Otros"
            name_lower = name.lower()
            if any(k in name_lower for k in ["iphone", "ipad", "apple watch", "icloud", "macbook"]):
                category = "Dispositivos Apple"
            elif any(k in name_lower for k in ["ram", "ssd", "disco", "almacenamiento"]):
                category = "Almacenamiento"
            elif any(k in name_lower for k in ["gpu", "cpu", "procesador", "placa", "fuente", "gabinete"]):
                category = "Componentes"
            elif any(k in name_lower for k in ["teclado", "mouse", "monitor", "periferico"]):
                category = "Periféricos"
            elif any(k in name_lower for k in ["auricular", "headset", "cascos", "buds"]):
                category = "Auriculares"
            elif any(k in name_lower for k in ["celular", "smartphone", "teléfono"]):
                category = "Celulares"
            elif any(k in name_lower for k in ["notebook", "laptop", "portátil"]):
                category = "Notebooks"
            elif any(k in name_lower for k in ["pc armada", "estacion", "gamer pc"]):
                category = "PCs Armadas"

            specs = name
            spec_match = re.search(r'(\d+GB|\d+TB|DDR\d|MHz|GHz).*', name)
            if spec_match:
                specs = name[spec_match.start():]

            # Use the new pricing helper
            final_price = calculate_final_price(name, price_val, manual_prices)

            products_data.append({
                "name": name,
                "original_price": original_price,
                "price_with_margin": final_price,
                "image": img_url,
                "category": category,
                "specs": specs
            })
        except Exception as e:
            print(f"[WARNING] Error procesando producto: {e}")

    return products_data

def main():
    products = scrape_products()
    manual_products = get_manual_products()
    manual_prices = get_manual_prices()

    if manual_products:
        print(f"[INFO] Agregando {len(manual_products)} productos manuales...")
        # Evitar duplicados por nombre
        manual_names = {p['name'].lower() for p in manual_products}
        products = [p for p in products if p['name'].lower() not in manual_names]

        # Apply manual prices to manual products as well
        for p in manual_products:
            p['price_with_margin'] = calculate_final_price(p['name'], p['price_with_margin'] / MARKUP if 'price_with_margin' in p else p['original_price'], manual_prices)

        products.extend(manual_products)

    if products:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"[OK] Proceso completado. {len(products)} productos guardados en {OUTPUT_FILE}")
    else:
        print("[ERROR] No se pudieron extraer productos o no hay productos configurados.")

if __name__ == "__main__":
    main()
