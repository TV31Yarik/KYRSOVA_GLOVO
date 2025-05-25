document.addEventListener('DOMContentLoaded', function () {
  const isAuthenticated = document.body.dataset.isAuthenticated === 'true';
  const addToCartBtn = document.querySelector('button.btn-primary[data-product-id]');
  const modalContent = document.getElementById('productModalContent');
  const productModalElement = document.getElementById('productModal');
  const productModal = new bootstrap.Modal(productModalElement);

  addToCartBtn.addEventListener('click', function () {
     if (!isAuthenticated) {
      window.location.href = '/login/'; 
      return; 
    }
    const modalUrl = this.dataset.productModalUrl;

    fetch(modalUrl)
      .then(response => response.text())
      .then(html => {
        modalContent.innerHTML = html;
        productModal.show();
        setupQuantityButtons();
        setupAddToCartHandler();
      })
      .catch(err => {
        modalContent.innerHTML = '<p>Помилка завантаження.</p>';
        console.error(err);
      });
  });

  productModalElement.addEventListener('hidden.bs.modal', function () {
    const backdrops = document.getElementsByClassName('modal-backdrop');
    while(backdrops.length > 0) {
      backdrops[0].parentNode.removeChild(backdrops[0]);
    }
    document.body.classList.remove('modal-open');
    document.body.style.overflow = 'auto';
    document.documentElement.style.overflow = 'auto';
  });

  function setupQuantityButtons() {
    const decreaseBtn = document.getElementById('decreaseQty');
    const increaseBtn = document.getElementById('increaseQty');
    const qtyInput = document.getElementById('product-quantity');

    if (!decreaseBtn || !increaseBtn || !qtyInput) return;

    decreaseBtn.addEventListener('click', () => {
      let val = parseInt(qtyInput.value);
      if (val > 1) qtyInput.value = val - 1;
    });

    increaseBtn.addEventListener('click', () => {
      let val = parseInt(qtyInput.value);
      qtyInput.value = val + 1;
    });
  }

  function setupAddToCartHandler() {
    const addToCartBtn = document.getElementById('addToCartBtn');
    const qtyInput = document.getElementById('product-quantity');
    const modal = document.getElementById('productModal');

    if (!addToCartBtn || !qtyInput) return;

    addToCartBtn.addEventListener('click', function () {
      const productId = this.dataset.productId;
      const quantity = qtyInput.value;

      fetch('/cart/add_ajax/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
          product_id: productId,
          quantity: quantity
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const modalInstance = bootstrap.Modal.getInstance(modal);
          if (modalInstance) {
            modalInstance.hide();
          }
          const backdrops = document.getElementsByClassName('modal-backdrop');
          while(backdrops.length > 0) {
            backdrops[0].parentNode.removeChild(backdrops[0]);
          }
          document.body.classList.remove('modal-open');
          document.body.style.overflow = 'auto';
          document.documentElement.style.overflow = 'auto';

          showToast(data.message);
        } else {
          showToast(data.message || 'Не вдалося додати до кошика', true);
        }
      })
      .catch(() => {
        showToast('Помилка з’єднання із сервером', true);
      });
    });
  }

  function showToast(message, isError = false) {
    const existingToast = document.querySelector('.custom-toast');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.className = 'custom-toast';
    toast.textContent = message;
    if (isError) toast.classList.add('error');

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('visible');
    }, 100);

    setTimeout(() => {
      toast.classList.remove('visible');
      setTimeout(() => toast.remove(), 300);
    }, 3100);
  }
});
