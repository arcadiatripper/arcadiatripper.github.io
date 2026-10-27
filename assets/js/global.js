(() => {
  // A visitor whose browser is in English sees a small "English version →" band on a Korean page (never a redirect).
  const hint = document.querySelector('[data-lang-hint]');
  if (!hint) return;

  let dismissed = false;
  try {
    dismissed = localStorage.getItem('lang-hint-dismissed') === '1';
  } catch (error) {
    dismissed = false;
  }

  const prefersEnglish = (navigator.languages || [navigator.language || ''])
    .some((language) => /^en\b/i.test(language)) && !/^ko\b/i.test(navigator.language || '');

  if (prefersEnglish && !dismissed) hint.classList.add('is-shown');

  hint.querySelector('button')?.addEventListener('click', () => {
    hint.classList.remove('is-shown');
    try {
      localStorage.setItem('lang-hint-dismissed', '1');
    } catch (error) {
      // nothing to keep
    }
  });
})();
