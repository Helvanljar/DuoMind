// DuoMind base_lang.js — preload language selection before i18n.js runs
(function () {
  const COOKIE = "duomind_lang";
  const SUP = ["en","de","fr","es","pt","tr","ru","ja","ko","zh","th","id","vi","ar"];

  function getCookie(k) {
    const m = document.cookie.match(new RegExp("(?:^|; )" + k + "=([^;]+)"));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function pickLang() {
    const saved = getCookie(COOKIE);
    if (saved && SUP.includes(saved)) return saved;
    const nav = (navigator.language || "en").split("-")[0].toLowerCase();
    return SUP.includes(nav) ? nav : "en";
  }

  const lang = pickLang();
  document.documentElement.setAttribute("lang", lang);
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");

  document.addEventListener("DOMContentLoaded", function () {
    const dd = document.querySelector(".lang-dropdown .lang-current");
    const btn = document.querySelector('.lang-dropdown [data-lang="' + lang + '"]');
    if (dd && btn) dd.textContent = btn.textContent.trim();
  });
})();
