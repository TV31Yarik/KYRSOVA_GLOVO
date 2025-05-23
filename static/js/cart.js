document.addEventListener('DOMContentLoaded', function () {
  const cartSidebar = document.getElementById('cart-sidebar');
  const openCartBtn = document.getElementById('open-cart');

  function loadCartSidebar() {
    fetch('/cart/sidebar/')
      .then(response => response.json())
      .then(data => {
        cartSidebar.innerHTML = data.html;
        cartSidebar.style.display = 'block';
        cartSidebar.classList.add('show');
        attachCartEvents();
        attachCloseEvent();  
      });
  }

  function attachCartEvents() {
    document.querySelectorAll('.change-qty').forEach(btn => {
      btn.onclick = function () {
        const id = this.dataset.id;
        const op = this.dataset.op;
        const csrfToken = getCSRFToken();

        fetch('/cart/change-quantity/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
          },
          body: new URLSearchParams({ id, op })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) loadCartSidebar();
        });
      };
    });

    document.querySelectorAll('.delete-item').forEach(btn => {
      btn.onclick = function () {
        const id = this.dataset.id;
        const csrfToken = getCSRFToken();

        fetch('/cart/delete-item/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
          },
          body: new URLSearchParams({ id })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) loadCartSidebar();
        });
      };
    });
  }

 
  function attachCloseEvent() {
  const closeBtn = cartSidebar.querySelector('.close-cart-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      cartSidebar.classList.remove('show');
      cartSidebar.classList.add('hide');

      
      setTimeout(() => {
        cartSidebar.style.display = 'none';
        cartSidebar.classList.remove('hide');
      }, 300);
    });
  }
}

  function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  }

  openCartBtn.addEventListener('click', function () {
    loadCartSidebar();
  });
});
