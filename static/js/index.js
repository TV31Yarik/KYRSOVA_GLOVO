 document.addEventListener("DOMContentLoaded", function () {
    const fadeElements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show'); 
          observer.unobserve(entry.target); 
        }
      });
    }, {
      threshold: 0.2  
    });

    fadeElements.forEach(el => observer.observe(el));
  });