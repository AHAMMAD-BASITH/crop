const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});
signupLink.onclick = (()=>{
  signupBtn.click();
  return false;
});

document.addEventListener('DOMContentLoaded', function () {
  const fields = ['email','password'];

  // Required field validation
  fields.forEach(field => {
      const input = document.querySelector(`input[name="${field}"]`);
      const error = document.getElementById(`${field}-error`);
      if (input) {
          input.addEventListener('input', () => {
              if (input.value.trim() === '') {
                  error.textContent = 'This field is required.';
              } else {
                  error.textContent = '';
              }
          });
      }
  });

  // ✅ Name validation (letters and spaces only)
  const nameInput = document.querySelector('input[name="name"]');
  const nameError = document.getElementById('farmer_name-error');
  if (nameInput) {
      nameInput.addEventListener('input', function () {
          const value = nameInput.value.trim();
          const regex = /^[A-Za-z ]+$/;

          if (value === '') {
              nameError.textContent = 'This field is required.';
          } else if (!regex.test(value)) {
              nameError.textContent = 'Only letters and spaces are allowed.';
          } else {
              nameError.textContent = '';
          }
      });
  }

  // ✅ Contact validation (10 digits)
  const contactInput = document.querySelector('input[name="contact"]');
  const contactError = document.getElementById('contact-error');
  if (contactInput) {
      contactInput.addEventListener('input', function () {
          const value = contactInput.value.trim();
          const regex = /^\d{10}$/;

          if (value === '') {
              contactError.textContent = 'This field is required.';
          } else if (!regex.test(value)) {
              contactError.textContent = 'Contact must be exactly 10 digits.';
          } else {
              contactError.textContent = '';
          }
      });
  }

  // ✅ Email validation (valid email format)
  const emailInput = document.querySelector('input[name="email"]');
  const emailError = document.getElementById('email-error');
  if (emailInput) {
      emailInput.addEventListener('input', function () {
          const value = emailInput.value.trim();
          const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

          if (value === '') {
              emailError.textContent = 'This field is required.';
          } else if (!regex.test(value)) {
              emailError.textContent = 'Please enter a valid email address.';
          } else {
              emailError.textContent = '';
          }
      });
  }

  // ✅ Password validation (strength check)
  const passwordInput = document.querySelector('input[name="password"]');
  const passwordError = document.getElementById('password-error');
  if (passwordInput) {
      passwordInput.addEventListener('input', function () {
          const value = passwordInput.value;
          const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

          if (value.trim() === '') {
              passwordError.textContent = 'This field is required.';
          } else if (!regex.test(value)) {
              passwordError.textContent = 'Password must contain uppercase, lowercase, digit, special character, and be at least 8 characters.';
          } else {
              passwordError.textContent = '';
          }
      });
  }
});