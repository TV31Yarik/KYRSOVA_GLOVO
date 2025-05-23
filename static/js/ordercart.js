document.addEventListener('DOMContentLoaded', function() {
  const addToCartBtn = document.querySelector('button.btn-primary[data-product-id]');
  const modalContent = document.getElementById('productModalContent');
  const productModal = new bootstrap.Modal(document.getElementById('productModal'));

  addToCartBtn.addEventListener('click', function() {
    const modalUrl = this.dataset.productModalUrl;

    fetch(modalUrl)
      .then(response => response.text())
      .then(html => {
        modalContent.innerHTML = html;
        productModal.show();
        setupQuantityButtons();
      })
      .catch(err => {
        modalContent.innerHTML = '<p>Помилка завантаження.</p>';
        console.error(err);
      });
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
});
