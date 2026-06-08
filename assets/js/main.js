const WHATSAPP_PHONE = document.querySelector('meta[name="whatsapp-phone"]')?.content || '595973232127';
const PLACEHOLDER_SVG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300'%3E%3Crect fill='%231a1a1a' width='300' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='system-ui' font-size='14' fill='%23555'%3ESin imagen%3C/text%3E%3C/svg%3E";

function openProductModal(product) {
    const modal = document.getElementById('product-modal');
    if (!modal) return;

    const finalPrice = "$" + parseFloat(product.price_with_margin).toFixed(2);
    const message = encodeURIComponent(`Hola, vi en la página el producto ${product.name} por ${finalPrice} y me interesa`);
    const waLink = `https://wa.me/${WHATSAPP_PHONE}?text=${message}`;

    document.getElementById('modal-category').textContent = product.category;
    document.getElementById('modal-name').textContent = product.name;
    document.getElementById('modal-specs').textContent = product.specs;
    document.getElementById('modal-price').textContent = finalPrice;
    document.getElementById('modal-image').src = product.image;
    document.getElementById('modal-image').alt = product.name;
    document.getElementById('modal-wa-link').href = waLink;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeProductModal() {
    const modal = document.getElementById('product-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

async function loadProducts(filter = 'Todos') {
    const productGrid = document.getElementById('product-grid');
    if (!productGrid) return;

    try {
        const response = await fetch('data/productos.json');
        const products = await response.json();

        if (products && products.length > 0) {
            productGrid.innerHTML = '';

            const filteredProducts = filter === 'Todos'
                ? products
                : products.filter(p => p.category === filter);

            if (filteredProducts.length === 0) {
                productGrid.innerHTML = '<div class="col-span-full text-center text-on-surface-variant py-10">No hay productos en esta categoría.</div>';
                return;
            }

            filteredProducts.forEach(product => {
                const finalPrice = "$" + parseFloat(product.price_with_margin).toFixed(2);

                const message = encodeURIComponent(`Hola, vi en la página el producto ${product.name} por ${finalPrice} y me interesa`);
                const waLink = `https://wa.me/${WHATSAPP_PHONE}?text=${message}`;

                const card = document.createElement('div');
                card.className = 'glass-panel p-2 md:p-4 rounded-xl flex flex-col justify-between border-t border-white/5 hover:-translate-y-2 transition-transform duration-300 cursor-pointer';
                card.innerHTML = `
                    <div class="flex flex-col h-full">
                        <div class="w-full h-32 md:h-48 bg-white/5 rounded-lg mb-4 overflow-hidden flex items-center justify-center">
                            <img src="${product.image}" alt="${product.name}" class="w-full h-full object-cover" loading="lazy" onerror="this.src='${PLACEHOLDER_SVG}'">
                        </div>
                        <div class="flex-grow">
                            <h4 class="font-headline-md text-on-surface text-sm md:text-lg mb-2 line-clamp-2">${product.name}</h4>
                            <p class="text-on-surface-variant text-[10px] md:text-xs mb-4 italic">${product.specs}</p>
                        </div>
                        <div class="mt-4">
                            <p class="text-primary-container font-bold text-base md:text-xl mb-4">${finalPrice}</p>
                            <a href="${waLink}" target="_blank" class="btn-primary w-full py-2.5 rounded-lg font-label-md flex justify-center items-center gap-2 neon-glow hover:neon-glow-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background" onclick="event.stopPropagation()">
                                <span class="material-symbols-outlined text-[18px]">shopping_cart</span>
                                Comprar
                            </a>
                        </div>
                    </div>
                `;

                card.addEventListener('click', () => openProductModal(product));
                productGrid.appendChild(card);
            });
        } else {
            productGrid.innerHTML = '<div class="col-span-full text-center text-on-surface-variant py-10">No hay productos disponibles en este momento.</div>';
        }
    } catch (error) {
        console.error("Error loading products:", error);
        productGrid.innerHTML = '<div class="col-span-full text-center text-error py-10">Error al cargar la tienda. Intente nuevamente más tarde.</div>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();

    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterButtons.forEach(b => b.classList.remove('bg-primary-container', 'text-white'));
            btn.classList.add('bg-primary-container', 'text-white');

            const category = btn.getAttribute('data-category');
            loadProducts(category);
        });

        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    });

    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.toggle('hidden');
            mobileMenuBtn.setAttribute('aria-expanded', !isHidden);
            mobileMenuBtn.querySelector('.material-symbols-outlined').textContent = isHidden ? 'menu' : 'close';
        });
    }

    const closeModalBtn = document.getElementById('close-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeProductModal);
    }

    const modalOverlay = document.getElementById('product-modal');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeProductModal();
            }
        });
    }
});
