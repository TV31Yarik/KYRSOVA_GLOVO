 document.addEventListener("DOMContentLoaded", function () {
    // Отримуємо всі елементи з класом .fade-in
    const fadeElements = document.querySelectorAll('.fade-in');

    // Створюємо спостерігача для IntersectionObserver
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        // Якщо елемент потрапив в область видимості
        if (entry.isIntersecting) {
          entry.target.classList.add('show'); // додаємо клас для анімації
          observer.unobserve(entry.target); // припиняємо спостереження за елементом
        }
      });
    }, {
      threshold: 0.2  // Активуємо анімацію, коли 20% елемента видно
    });

    // Спостерігаємо за кожним елементом з класом .fade-in
    fadeElements.forEach(el => observer.observe(el));
  });