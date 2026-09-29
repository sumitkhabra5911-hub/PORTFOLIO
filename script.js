/* ==========================================================================
   SUMIT CHAUHAN - PORTFOLIO JAVASCRIPT
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // ── 1. Mobile Menu Toggle ──────────────────────────────────────────────────
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      navToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.textContent = '☰';
      });
    });
  }

  // ── 2. Active Navigation Link on Scroll ────────────────────────────────────
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

  // ── 3. Contact Form Controller ─────────────────────────────────────────────
  const contactForm = document.getElementById('contact-form');
  const nameInput = document.getElementById('name');
  const emailInput = document.getElementById('email');
  const messageInput = document.getElementById('message');
  const subjectInput = document.getElementById('subject');
  const messageCharCount = document.getElementById('message-char-count');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnIcon = document.getElementById('btn-icon');

  const alertBox = document.getElementById('form-status-alert');
  const alertIcon = document.getElementById('alert-icon');
  const alertTitle = document.getElementById('alert-title');
  const alertDesc = document.getElementById('alert-desc');
  const alertAction = document.getElementById('alert-action');
  const alertClose = document.getElementById('alert-close');

  const backendBadge = document.getElementById('backend-status-badge');
  const statusText = document.getElementById('status-text');
  const topicPills = document.querySelectorAll('.topic-pill');

  // Topic pill selector
  if (topicPills.length && subjectInput) {
    topicPills.forEach(pill => {
      pill.addEventListener('click', () => {
        topicPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        subjectInput.value = pill.getAttribute('data-topic') || 'General Inquiry';
      });
    });
  }

  // Character counter for message textarea
  if (messageInput && messageCharCount) {
    messageInput.addEventListener('input', () => {
      const len = messageInput.value.length;
      messageCharCount.textContent = `${len} / 5000`;
      if (len > 4800) {
        messageCharCount.className = 'char-count limit';
      } else if (len > 4000) {
        messageCharCount.className = 'char-count warn';
      } else {
        messageCharCount.className = 'char-count';
      }
    });
  }

  // Validation functions
  const validators = {
    name: (val) => {
      const trimmed = (val || '').trim();
      if (!trimmed) return 'Please enter your name.';
      if (trimmed.length < 2) return 'Name must be at least 2 characters long.';
      if (trimmed.length > 100) return 'Name cannot exceed 100 characters.';
      return null;
    },
    email: (val) => {
      const trimmed = (val || '').trim();
      if (!trimmed) return 'Please enter your email address.';
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
      if (!emailRegex.test(trimmed)) return 'Please provide a valid email address (e.g. name@domain.com).';
      return null;
    },
    message: (val) => {
      const trimmed = (val || '').trim();
      if (!trimmed) return 'Please enter your message.';
      if (trimmed.length < 10) return 'Message is too short. Please provide at least 10 characters.';
      if (trimmed.length > 5000) return 'Message cannot exceed 5000 characters.';
      return null;
    }
  };

  function setFieldState(inputEl, feedbackEl, errorMsg) {
    if (!inputEl || !feedbackEl) return;
    if (errorMsg) {
      inputEl.classList.add('is-invalid');
      inputEl.classList.remove('is-valid');
      feedbackEl.textContent = errorMsg;
      feedbackEl.style.opacity = '1';
    } else if (inputEl.value.trim().length > 0) {
      inputEl.classList.remove('is-invalid');
      inputEl.classList.add('is-valid');
      feedbackEl.textContent = '';
      feedbackEl.style.opacity = '0';
    } else {
      inputEl.classList.remove('is-invalid');
      inputEl.classList.remove('is-valid');
      feedbackEl.textContent = '';
      feedbackEl.style.opacity = '0';
    }
  }

  // Real-time input validation on blur and input
  if (nameInput) {
    const feedback = document.getElementById('name-feedback');
    nameInput.addEventListener('blur', () => setFieldState(nameInput, feedback, validators.name(nameInput.value)));
    nameInput.addEventListener('input', () => {
      if (nameInput.classList.contains('is-invalid')) {
        setFieldState(nameInput, feedback, validators.name(nameInput.value));
      }
    });
  }

  if (emailInput) {
    const feedback = document.getElementById('email-feedback');
    emailInput.addEventListener('blur', () => setFieldState(emailInput, feedback, validators.email(emailInput.value)));
    emailInput.addEventListener('input', () => {
      if (emailInput.classList.contains('is-invalid')) {
        setFieldState(emailInput, feedback, validators.email(emailInput.value));
      }
    });
  }

  if (messageInput) {
    const feedback = document.getElementById('message-feedback');
    messageInput.addEventListener('blur', () => setFieldState(messageInput, feedback, validators.message(messageInput.value)));
    messageInput.addEventListener('input', () => {
      if (messageInput.classList.contains('is-invalid')) {
        setFieldState(messageInput, feedback, validators.message(messageInput.value));
      }
    });
  }

  // Alert Box functions
  function showAlert(type, title, desc, actionHtml = null) {
    if (!alertBox) return;
    alertBox.className = `form-status-alert alert-${type}`;
    alertIcon.textContent = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : '❌';
    alertTitle.textContent = title;
    alertDesc.textContent = desc;

    if (actionHtml && alertAction) {
      alertAction.innerHTML = actionHtml;
      alertAction.style.display = 'block';
    } else if (alertAction) {
      alertAction.style.display = 'none';
      alertAction.innerHTML = '';
    }

    alertBox.style.display = 'flex';
  }

  function hideAlert() {
    if (alertBox) alertBox.style.display = 'none';
  }

  if (alertClose) {
    alertClose.addEventListener('click', hideAlert);
  }

  // Contact Form Submission
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const nameVal = nameInput ? nameInput.value.trim() : '';
      const emailVal = emailInput ? emailInput.value.trim() : '';
      const messageVal = messageInput ? messageInput.value.trim() : '';
      const subjectVal = subjectInput ? subjectInput.value.trim() : 'General Inquiry';

      // 1. Validate all fields
      const nameErr = validators.name(nameVal);
      const emailErr = validators.email(emailVal);
      const messageErr = validators.message(messageVal);

      setFieldState(nameInput, document.getElementById('name-feedback'), nameErr);
      setFieldState(emailInput, document.getElementById('email-feedback'), emailErr);
      setFieldState(messageInput, document.getElementById('message-feedback'), messageErr);

      if (nameErr || emailErr || messageErr) {
        const firstInvalid = nameErr ? nameInput : emailErr ? emailInput : messageInput;
        if (firstInvalid) firstInvalid.focus();
        showAlert('warning', 'Please Review Your Details', 'Make sure your name, a valid email address, and a message (10+ characters) are entered.');
        return;
      }

      // 2. Set button loading state
      if (submitBtn) {
        submitBtn.disabled = true;
        if (btnText) btnText.textContent = 'Sending Message...';
        if (btnIcon) btnIcon.innerHTML = '<span class="btn-spinner"></span>';
      }

      // 3. Post to Formsubmit API
      try {
        const response = await fetch(`https://formsubmit.co/ajax/sumitkhabra5911@gmail.com`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            name: nameVal,
            email: emailVal,
            _subject: subjectVal,
            message: messageVal
          })
        });

        if (response.ok) {
          showAlert(
            'success',
            'Message Sent Successfully!',
            `Thank you, ${nameVal}! Your message has been delivered to sumitkhabra5911@gmail.com. You will receive a response soon.`
          );

          // Reset form fields
          contactForm.reset();
          if (messageCharCount) messageCharCount.textContent = '0 / 5000';
          if (nameInput) nameInput.classList.remove('is-valid');
          if (emailInput) emailInput.classList.remove('is-valid');
          if (messageInput) messageInput.classList.remove('is-valid');

          // Reset topic pills to default
          if (topicPills.length) {
            topicPills.forEach(p => p.classList.remove('active'));
            topicPills[topicPills.length - 1].classList.add('active');
            if (subjectInput) subjectInput.value = '👋 General Message';
          }
        } else {
          // Server returned an error
          const fallbackMailto = `mailto:sumitkhabra5911@gmail.com?subject=${encodeURIComponent(subjectVal + ' from ' + nameVal)}&body=${encodeURIComponent(messageVal + '\n\n— ' + nameVal + ' (' + emailVal + ')')}`;
          showAlert(
            'error',
            'Server Temporarily Unavailable',
            'The contact API encountered an issue. You can send your message directly via email to sumitkhabra5911@gmail.com:',
            `<a href="${fallbackMailto}" class="btn btn-secondary btn-sm" style="display:inline-flex; align-items:center; gap:6px; margin-top:4px; text-decoration:none;">✉️ Open in Email Client</a>`
          );
        }
      } catch (networkError) {
        // Network failed
        const fallbackMailto = `mailto:sumitkhabra5911@gmail.com?subject=${encodeURIComponent(subjectVal + ' from ' + nameVal)}&body=${encodeURIComponent(messageVal + '\n\n— ' + nameVal + ' (' + emailVal + ')')}`;
        showAlert(
          'error',
          'Network Error',
          'We could not connect to the server. Please check your internet connection or email Sumit directly:',
          `<a href="${fallbackMailto}" class="btn btn-secondary btn-sm" style="display:inline-flex; align-items:center; gap:6px; margin-top:6px; text-decoration:none;">✉️ Send via Email to sumitkhabra5911@gmail.com</a>`
        );
      } finally {
        // Restore button state
        if (submitBtn) {
          submitBtn.disabled = false;
          if (btnText) btnText.textContent = 'Send Message';
          if (btnIcon) btnIcon.textContent = '🚀';
        }
      }
    });
  }
});
