# 🚀 Guía de DF Multiservicios - Publicación y Gestión del E-commerce

Esta carpeta contiene todo lo necesario para desplegar tu sitio web en **GitHub Pages** y administrar tu inventario de productos. La página ha sido personalizada con la paleta de colores corporativa: **Negro profundo y Naranja brillante**.

---

## 📂 Estructura del Proyecto

```text
/GITHUB
├── .github/workflows/actualizar-inventario.yml # Actualización automática diaria
├── assets/
│   ├── css/style.css                          # Estilos de fondo y efectos (Negro/Naranja)
│   └── js/main.js                             # Catálogo interactivo y filtros de la tienda
├── data/
│   ├── productos.json                          # Catálogo final compilado (Generado automáticamente)
│   ├── productos_manuales.json                 # Tus productos personalizados (¡Agrégalos aquí!)
│   └── precios_manuales.json                   # Excepciones de precios para el scraper
├── images/
│   ├── logo.jpeg                              # Logotipo de la empresa (DF Multiservicios)
│   └── ...                                    # Fotos de los servicios y productos
├── index.html                                 # Página web principal (Negro y Naranja)
├── scraper.py                                 # Script de Python que extrae productos de la web
└── README.md                                  # Esta guía de uso
```

---

## ☁️ 1. Cómo subir la página a GitHub y activar la Web Gratis

Sigue estos pasos para publicar tu sitio web en internet utilizando **GitHub Pages**:

### Paso A: Subir los archivos a un repositorio de GitHub
1. Abre tu navegador e inicia sesión en [GitHub](https://github.com).
2. Haz clic en el botón **"New"** (Nuevo) para crear un repositorio.
3. Escribe un nombre para tu repositorio (por ejemplo: `tienda-df`).
4. Selecciona la opción **Public** (Público) y deja las demás opciones sin marcar. Haz clic en **Create repository**.
5. Abre la consola de comandos (**Git Bash**, **CMD** o **PowerShell**) en esta carpeta (`C:\Users\PC\Desktop\GITHUB`) y ejecuta los siguientes comandos ordenadamente:
   ```bash
   # 1. Inicializar el control de versiones en esta carpeta
   git init

   # 2. Agregar todos los archivos para subirlos
   git add .

   # 3. Guardar el estado inicial
   git commit -m "Despliegue inicial de tienda negra y naranja"

   # 4. Cambiar el nombre de la rama principal a 'main'
   git branch -M main

   # 5. Conectar tu carpeta local con tu repositorio en GitHub
   # (Reemplaza 'tu-usuario' y 'tienda-df' por los datos de tu repositorio creado en GitHub)
   git remote add origin https://github.com/tu-usuario/tienda-df.git

   # 6. Subir tus archivos a GitHub
   git push -u origin main -f
   ```

### Paso B: Activar GitHub Pages (Web en Línea)
Una vez subidos los archivos:
1. En la página de tu repositorio en GitHub, ve a la pestaña **Settings** (Configuración) en el menú superior.
2. En el menú lateral izquierdo, haz clic en **Pages** (Páginas).
3. En la sección **Build and deployment**:
   - Bajo **Source**, asegúrate de que esté seleccionado **Deploy from a branch**.
   - Bajo **Branch**, selecciona la rama **`main`** y la carpeta **`/ (root)`**.
   - Haz clic en **Save** (Guardar).
4. Espera 1 o 2 minutos. GitHub te mostrará arriba un enlace similar a:
   `https://tu-usuario.github.io/tienda-df/`
   ¡Esta será la dirección pública de tu tienda en internet!

---

## 🛍️ 2. Cómo Subir y Modificar Productos

Tienes dos formas de administrar tus productos en la tienda:

### 🔹 Método Manual (Para productos propios, combos y servicios)
Si quieres agregar productos que no provienen del proveedor (por ejemplo: la antena Starlink configurada, soporte técnico, armado de PCs personalizadas, etc.), utiliza el archivo de productos manuales:
1. Abre el archivo [data/productos_manuales.json](file:///C:/Users/PC/Desktop/GITHUB/data/productos_manuales.json) con un editor de texto (como Bloc de Notas, VS Code u OpenCode).
2. Agrega o modifica tus productos siguiendo este formato:
   ```json
   {
     "name": "Nombre de tu producto o servicio",
     "original_price": 100.00,
     "price_with_margin": 120.00,
     "image": "images/tu-imagen.jpeg", 
     "category": "Componentes",
     "specs": "Especificaciones técnicas del producto"
   }
   ```
   *Nota: Las categorías disponibles para usar son: `"Componentes"`, `"Almacenamiento"`, `"Periféricos"`, `"PCs Armadas"`.*
3. Guarda el archivo y ejecuta el scraper (Paso C) para que se actualice la base de datos de la web.

### 🤖 Método Automático (Scraper desde la web del proveedor)
El script `scraper.py` descarga automáticamente los últimos productos del proveedor, les aplica un margen de ganancia del 20% y los combina con tus productos manuales.

*   **Para cambiar el margen de ganancia**: Abre `scraper.py` y modifica el valor de `MARKUP = 1.20` (por ejemplo, `1.30` representa un 30% de ganancia).
*   **Para fijar el precio de un producto scrapeado**: Si un producto específico del proveedor tiene un precio que quieres fijar a mano (sin aplicar el 20%), abre el archivo [data/precios_manuales.json](file:///C:/Users/PC/Desktop/GITHUB/data/precios_manuales.json) y agrega el nombre exacto del producto y su precio deseado:
    ```json
    {
      "descripciones_manuales": {
        "Nombre Exacto del Producto Proveedor": 99.99
      }
    }
    ```

### Paso C: Ejecutar el actualizador (Scraper)
Cada vez que edites los productos manuales o quieras sincronizar con el proveedor, debes actualizar el archivo definitivo `productos.json`. Puedes hacerlo de dos formas:

1. **De forma automática (Diaria)**: GitHub Actions ya está configurado en el archivo `.github/workflows/actualizar-inventario.yml`. Cada día a medianoche, ejecutará el script por ti, unirá tus productos manuales y actualizará la web de forma automática en internet.
   > ⚠️ **IMPORTANTE**: Para que esto funcione, en GitHub ve a **Settings ➔ Actions ➔ General ➔ Workflow permissions**, selecciona la opción **Read and write permissions** (Permisos de lectura y escritura) y presiona **Save**.
2. **De forma manual en tu PC**: Abre una terminal en esta carpeta y ejecuta:
   ```bash
   pip install requests beautifulsoup4
   python scraper.py
   ```
   Esto generará el catálogo actualizado localmente. Luego, sube los cambios a GitHub para actualizar la web online:
   ```bash
   git add .
   git commit -m "Actualizar inventario"
   git push origin main
   ```

---

## 🖼️ 3. Cómo Elegir y Cambiar las Imágenes (como el Logo)

Todas las imágenes locales se guardan en la carpeta `images/`.

### Cambiar el Logotipo de la Empresa
1. Consigue tu logotipo en formato `.jpeg` (o `.jpg`).
2. Cámbiale el nombre a `logo.jpeg`.
3. Pégalo dentro de la carpeta `images/`, reemplazando el archivo `logo.jpeg` existente.
4. Si tu logotipo está en formato `.png` o tiene otro nombre, reemplázalo en la carpeta y edita la línea **245** y **606** de `index.html` para actualizar la extensión o el nombre del archivo.

### Cambiar las imágenes de los Servicios y Portafolio
Si realizaste un nuevo trabajo y deseas cambiar las imágenes de la sección de servicios o trabajos recientes:
1. Pega tu foto dentro de la carpeta `images/` (por ejemplo: `nueva-antena.jpeg`).
2. Abre `index.html` y busca la sección del servicio correspondiente (por ejemplo, busca `images/instalacion-de-antena-starlink.jpeg` en el código).
3. Cambia esa ruta por el nombre de tu nuevo archivo (ejemplo: `images/nueva-antena.jpeg`).

---

## 🎨 4. Personalización del Color (Negro y Naranja)

El sitio web está diseñado con un fondo negro profundo y detalles naranja neón. Si deseas hacer ajustes visuales adicionales:

1. **Estilos y Efectos de Brillo**: Se administran en el archivo [assets/css/style.css](file:///C:/Users/PC/Desktop/GITHUB/assets/css/style.css). Aquí puedes controlar la intensidad del brillo naranja en la clase `.neon-glow` y los botones.
2. **Colores generales del sitio**: Están configurados dinámicamente mediante Tailwind CSS en la cabecera de [index.html](file:///C:/Users/PC/Desktop/GITHUB/index.html) (dentro del script `tailwind-config` entre las líneas 18 y 66). Si deseas cambiar los tonos de naranja o gris, modifica esos valores hexadecimales.
