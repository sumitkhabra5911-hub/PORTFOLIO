/* ==========================================================================
   SUMIT CHAUHAN - PORTFOLIO JAVASCRIPT
   Lightweight, clean, and dependency-free
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      navToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
    });

    // Close mobile menu when clicking any nav link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.textContent = '☰';
      });
    });
  }

  // 2. Active Navigation Link on Scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;

    sections.forEach(sec => {
      const sectionHeight = sec.offsetHeight;
      const sectionTop = sec.offsetTop - 100;
      const sectionId = sec.getAttribute('id');
      const currentLink = document.querySelector(`.nav-link[href*="#${sectionId}"]`);

      if (currentLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          currentLink.classList.add('active');
        } else {
          currentLink.classList.remove('active');
        }
      }
    });
  });

  // 3. Contact Form Submission Feedback
  const contactForm = document.getElementById('contact-form');
  const formStatus = document.getElementById('form-status');

  if (contactForm && formStatus) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Show immediate feedback to the user
      formStatus.textContent = 'Thank you, Sumit received your message! (Demo feedback)';
      formStatus.style.display = 'block';
      formStatus.style.color = '#00ffb2';
      formStatus.style.marginTop = '12px';
      formStatus.style.fontSize = '0.9rem';

      // Reset form fields
      contactForm.reset();

      // Clear status after 5 seconds
      setTimeout(() => {
        formStatus.style.display = 'none';
      }, 5000);
    });
  }
});
