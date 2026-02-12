// DuoMind i18n.js — full multilingual support (14 languages)
// - Uses data-i18n* attributes where present
// - Safe fuzzy mapping for fixed English phrases
// - Keeps layout stable; RTL for Arabic only affects text direction, not layout

(function () {
  const COOKIE = "duomind_lang";
  const SUP = ["en", "de", "fr", "es", "pt", "tr", "ru", "ja", "ko", "zh", "th", "id", "vi", "ar"];
  const RTL_CODE = "ar";

  function getCookie(k, d) {
    const m = document.cookie.match(new RegExp("(?:^|; )" + k + "=([^;]+)"));
    return m ? decodeURIComponent(m[1]) : d;
  }

  function setCookie(k, v) {
    document.cookie = k + "=" + encodeURIComponent(v) + ";path=/;max-age=31536000";
  }

  function htmlLang() {
    return (document.documentElement.getAttribute("lang") || "").toLowerCase();
  }

  function pickInitialLang() {
    const fromCookie = getCookie(COOKIE, "");
    if (SUP.includes(fromCookie)) return fromCookie;
    const fromHtml = htmlLang();
    if (SUP.includes(fromHtml)) return fromHtml;
    const nav = (navigator.language || "en").split("-")[0].toLowerCase();
    return SUP.includes(nav) ? nav : "en";
  }

  // ================== DICTIONARY ==================
  const T = {
    // ---------- English ----------
    en: {
      nav: {
        home: "Home",
      hello: "Hello",
        settings: "Settings",
        history: "History",
        login: "Login",
        register: "Register",
        logout: "Logout",
        language: "Language",
        theme: "Theme"
      },
      theme: { system: "System", light: "Light", dark: "Dark" },
      footer: { text: "AI Research Copilot • © 2025" },
      home: {
        title: "Welcome to DuoMind",
        subtitle: "A dual-LLM research copilot. Log in, set your keys, and start exploring.",
        search: "Ask DuoMind to compare GPT and Gemini on a topic…",
        searchbtn: "Search",
        guestNote: "Guest mode: 5 requests/day. Add your API keys to continue without limits.",
        dual: "Dual LLM",
        "dual.desc": "Run GPT + Gemini together and compare perspectives.",
        byok: "BYOK",
        "byok.desc": "Bring your own API keys for full power and privacy.",
        history: "History",
        "history.desc": "See your recent research sessions at a glance.",
        guest: ""
      },
      login: {
        title: "Login",
        subtitle: "Log in to access your settings and history.",
        email: "Email",
        password: "Password",
        button: "Login",
        noaccount: "No account yet?",
        registerlink: "Register"
      },
      register: {
        title: "Create Account",
        subtitle: "Username will be shown in the top right after login.",
        username: "Username",
        email: "Email",
        password: "Password",
        confirm: "Confirm password",
        rules: "Password must be at least 8 characters, contain 2 digits, 1 special character, and 1 uppercase letter.",
        button: "Register",
        already: "Already have an account?",
        loginlink: "Login",
        alertMismatch: "Passwords do not match.",
        alertWeak: "Password must be ≥8 chars, ≥2 digits, ≥1 special, ≥1 uppercase."
      },
      settings: {
        title: "Settings",
        needlogin: "You need to be logged in to edit your OpenAI / Gemini keys.",
        desc: "Provide your own keys (BYOK) and preferred model.",
        openai: "OpenAI API Key",
        gemini: "Gemini API Key",
        anthropic: "Anthropic (Claude) API Key",
        openrouter: "OpenRouter API Key",
        mistral: "Mistral API Key",
        tip: "Tip: Your keys are stored encrypted and only used for your requests.",
        preferred: "Preferred LLM",
        save: "Save",
        keyValid: "{provider} key valid",
        keyInvalid: "{provider} key invalid",
        saved: "Settings saved.",
        error: "Could not save settings.",
        opt: {
          auto: "Auto (GPT → Gemini)",
          openai: "OpenAI first",
          gemini: "Gemini first"
        ,
          anthropic: "Claude first"
        ,
          openrouter: "OpenRouter first"
        ,
          mistral: "Mistral first"
        }
      },
      history: {
        title: "History",
        empty: "No research sessions yet.",
        loadMore: "Load more",
        needlogin: "You must be logged in to view your research history.",
        cta: { login: "Login", register: "Register" },
        search: "Search history…"
      },
      research: {
        title: "Research session",
        run: "Run",
        search: "Type a query…",
        models: "Models",
        tipPrefix: "Tip: Add your own keys in",
        tipSuffix: "to unlock higher limits.",
        explainer: "Both models responded. Agreements show overlap; disagreements show nuance.",
        agreements: "Agreements",
        disagreements: "Disagreements",
        guest: "Guest mode: using GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Answer (LLM A)",
        answerB: "Answer (LLM B)",
        synthesis: "Comparison / Synthesis",
        compare: "Compare & reconcile",
        recommendation: "Recommendation",
        openQuestions: "Open questions",
        comparedBy: "Compared by"
      },
      toasts: {
        keysSaved: "Settings saved.",
        keysError: "Could not save settings.",
        guestLimit:
          "Daily guest limit reached (5 requests). Please register or add API keys to continue.",
        needLogin: "You must be logged in to perform this action.",
        invalidKeyOpenAI: "Invalid OpenAI API key.",
        invalidKeyGemini: "Invalid Gemini API key.",
        missingKey: "Missing API key.",
        genericError: "Something went wrong. Please try again."
      },
      common: { ok: "OK", cancel: "Cancel", save: "Save" }
    },

    // ---------- German ----------
    de: {
      nav: {
        home: "Start",
      hello: "Hallo",
        settings: "Einstellungen",
        history: "Verlauf",
        login: "Anmelden",
        register: "Registrieren",
        logout: "Abmelden",
        language: "Sprache",
        theme: "Thema"
      },
      theme: { system: "System", light: "Hell", dark: "Dunkel" },
      footer: { text: "KI-Forschungsassistent • © 2025" },
      home: {
        title: "Willkommen bei DuoMind",
        subtitle:
          "Ein Forschungs-Copilot mit zwei LLMs. Melde dich an, hinterlege deine Schlüssel und lege los.",
        search: "Bitte Thema für den Vergleich von GPT und Gemini eingeben…",
        searchbtn: "Suchen",
        guestNote:
          "Gastmodus: 5 Anfragen/Tag. Füge API-Schlüssel hinzu, um ohne Limit weiterzumachen.",
        dual: "Dual LLM",
        "dual.desc":
          "GPT und Gemini gemeinsam ausführen und Perspektiven vergleichen.",
        byok: "BYOK",
        "byok.desc": "Eigene API-Schlüssel für volle Leistung und Datenschutz.",
        history: "Verlauf",
        "history.desc": "Sieh dir deine letzten Recherchen auf einen Blick an.",
        guest: ""
      },
      login: {
        title: "Anmelden",
        subtitle: "Melde dich an, um Einstellungen und Verlauf zu sehen.",
        email: "E-Mail",
        password: "Passwort",
        button: "Anmelden",
        noaccount: "Noch kein Konto?",
        registerlink: "Registrieren"
      },
      register: {
        title: "Konto erstellen",
        subtitle: "Der Benutzername wird oben rechts angezeigt.",
        username: "Benutzername",
        email: "E-Mail",
        password: "Passwort",
        confirm: "Passwort bestätigen",
        rules:
          "Passwort: mind. 8 Zeichen, 2 Ziffern, 1 Sonderzeichen und 1 Großbuchstabe.",
        button: "Registrieren",
        already: "Schon ein Konto?",
        loginlink: "Anmelden",
        alertMismatch: "Passwörter stimmen nicht überein.",
        alertWeak: "Passwort zu schwach."
      },
      settings: {
        title: "Einstellungen",
        needlogin:
          "Zum Bearbeiten der OpenAI/Gemini-Schlüssel musst du angemeldet sein.",
        desc:
          "Hinterlege eigene Schlüssel (BYOK) und wähle ein bevorzugtes Modell.",
        openai: "OpenAI-API-Schlüssel",
        gemini: "Gemini-API-Schlüssel",
        anthropic: "Anthropic (Claude) API Key",
        openrouter: "OpenRouter API Key",
        mistral: "Mistral API Key",
        tip: "Tipp: Deine Schlüssel werden verschlüsselt gespeichert und nur für deine Anfragen verwendet.",
        preferred: "Bevorzugtes LLM",
        save: "Speichern",
        keyValid: "{provider}-Schlüssel gültig",
        keyInvalid: "{provider}-Schlüssel ungültig",
        saved: "Einstellungen gespeichert.",
        error: "Einstellungen konnten nicht gespeichert werden.",
        opt: {
          auto: "Auto (GPT → Gemini)",
          openai: "OpenAI zuerst",
          gemini: "Gemini zuerst"
        ,
          anthropic: "Claude zuerst"
        ,
          openrouter: "OpenRouter zuerst"
        ,
          mistral: "Mistral zuerst"
        }
      },
      history: {
        title: "Verlauf",
        empty: "Noch keine Recherchen.",
        loadMore: "Mehr laden",
        needlogin: "Du musst angemeldet sein, um deinen Verlauf zu sehen.",
        cta: { login: "Anmelden", register: "Registrieren" },
        search: "Verlauf durchsuchen…"
      },
      research: {
        title: "Recherche-Sitzung",
        run: "Ausführen",
        search: "Gib eine Abfrage ein…",
        models: "Modelle",
        tipPrefix: "Tipp: Hinterlege deine Schlüssel in",
        tipSuffix: "um höhere Limits freizuschalten.",
        explainer:
          "Beide Modelle haben geantwortet. Übereinstimmungen zeigen Überschneidungen; Unterschiede zeigen Nuancen.",
        agreements: "Übereinstimmungen",
        disagreements: "Unterschiede",
        guest: "Gastmodus: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Antwort (LLM A)",
        answerB: "Antwort (LLM B)",
        synthesis: "Vergleich / Synthese",
        compare: "Vergleichen & zusammenführen",
        recommendation: "Empfehlung",
        openQuestions: "Offene Fragen",
        comparedBy: "Verglichen von"
      },
      toasts: {
        keysSaved: "Einstellungen gespeichert.",
        keysError: "Einstellungen konnten nicht gespeichert werden.",
        guestLimit:
          "Tageslimit im Gastmodus erreicht (5 Anfragen). Bitte registrieren oder API-Schlüssel hinzufügen.",
        needLogin:
          "Du musst angemeldet sein, um diese Aktion auszuführen.",
        invalidKeyOpenAI: "Ungültiger OpenAI-API-Schlüssel.",
        invalidKeyGemini: "Ungültiger Gemini-API-Schlüssel.",
        missingKey: "API-Schlüssel fehlt.",
        genericError:
          "Etwas ist schief gelaufen. Bitte erneut versuchen."
      },
      common: { ok: "OK", cancel: "Abbrechen", save: "Speichern" }
    },

    // ---------- French ----------
    fr: {
      nav: {
        home: "Accueil",
      hello: "Bonjour",
        settings: "Paramètres",
        history: "Historique",
        login: "Connexion",
        register: "Inscription",
        logout: "Déconnexion",
        language: "Langue",
        theme: "Thème"
      },
      theme: { system: "Système", light: "Clair", dark: "Sombre" },
      footer: { text: "Copilote de recherche IA • © 2025" },
      home: {
        title: "Bienvenue sur DuoMind",
        subtitle:
          "Copilote de recherche à deux LLM. Connectez-vous, ajoutez vos clés et commencez.",
        search: "Demandez à DuoMind de comparer GPT et Gemini…",
        searchbtn: "Rechercher",
        guestNote:
          "Mode invité : 5 requêtes/jour. Ajoutez vos clés pour continuer sans limite.",
        dual: "Double LLM",
        "dual.desc": "Exécutez GPT + Gemini ensemble et comparez.",
        byok: "BYOK",
        "byok.desc":
          "Apportez vos propres clés API pour plus de puissance et de confidentialité.",
        history: "Historique",
        "history.desc":
          "Consultez rapidement vos recherches récentes.",
        guest: ""
      },
      login: {
        title: "Connexion",
        subtitle: "Accédez à vos paramètres et à l’historique.",
        email: "E-mail",
        password: "Mot de passe",
        button: "Connexion",
        noaccount: "Pas encore de compte ?",
        registerlink: "S’inscrire"
      },
      register: {
        title: "Créer un compte",
        subtitle: "Le nom d’utilisateur sera visible en haut à droite.",
        username: "Nom d’utilisateur",
        email: "E-mail",
        password: "Mot de passe",
        confirm: "Confirmer le mot de passe",
        rules: "≥ 8 caractères, 2 chiffres, 1 caractère spécial et 1 majuscule.",
        button: "S’inscrire",
        already: "Déjà un compte ?",
        loginlink: "Connexion",
        alertMismatch: "Les mots de passe ne correspondent pas.",
        alertWeak: "Mot de passe trop faible."
      },
      settings: {
        title: "Paramètres",
        needlogin: "Connectez-vous pour modifier vos clés OpenAI / Gemini.",
        desc: "Ajoutez vos clés (BYOK) et le modèle préféré.",
        openai: "Clé API OpenAI",
        gemini: "Clé API Gemini",
        anthropic: "Clé API Anthropic (Claude)",
        openrouter: "Clé API OpenRouter",
        mistral: "Clé API Mistral",
        tip: "Astuce : vos clés sont stockées chiffrées et utilisées uniquement pour vos requêtes.",
        preferred: "LLM préféré",
        save: "Enregistrer",
        keyValid: "Clé {provider} valide",
        keyInvalid: "Clé {provider} invalide",
        saved: "Paramètres enregistrés.",
        error: "Impossible d’enregistrer.",
        opt: {
          auto: "Auto (GPT → Gemini)",
          openai: "OpenAI d’abord",
          gemini: "Gemini d’abord"
        ,
          anthropic: "Claude d’abord"
        ,
          openrouter: "OpenRouter d’abord"
        ,
          mistral: "Mistral d’abord"
        }
      },
      history: {
        title: "Historique",
        empty: "Aucune recherche pour l’instant.",
        loadMore: "Charger plus",
        needlogin: "Connectez-vous pour voir l’historique.",
        cta: { login: "Connexion", register: "Inscription" },
        search: "Rechercher dans l’historique…"
      },
      research: {
        title: "Session de recherche",
        run: "Exécuter",
        search: "Saisissez une requête…",
        models: "Modèles",
        tipPrefix: "Astuce : ajoutez vos clés dans",
        tipSuffix: "pour débloquer des limites plus élevées.",
        explainer:
          "Les deux modèles ont répondu. Les accords montrent les recoupements ; les désaccords montrent les nuances.",
        agreements: "Accords",
        disagreements: "Désaccords",
        guest: "Mode invité : GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Réponse (LLM A)",
        answerB: "Réponse (LLM B)",
        synthesis: "Comparaison / Synthèse",
        compare: "Comparer & réconcilier",
        recommendation: "Recommandation",
        openQuestions: "Questions ouvertes",
        comparedBy: "Comparé par"
      },
      toasts: {
        keysSaved: "Paramètres enregistrés.",
        keysError: "Impossible d’enregistrer les paramètres.",
        guestLimit:
          "Limite quotidienne en mode invité atteinte (5 requêtes). Inscrivez-vous ou ajoutez des clés API.",
        needLogin:
          "Vous devez être connecté pour effectuer cette action.",
        invalidKeyOpenAI: "Clé API OpenAI invalide.",
        invalidKeyGemini: "Clé API Gemini invalide.",
        missingKey: "Clé API manquante.",
        genericError: "Une erreur s’est produite. Réessayez."
      },
      common: { ok: "OK", cancel: "Annuler", save: "Enregistrer" }
    },

    // ---------- Spanish ----------
    es: {
      nav: {
        home: "Inicio",
      hello: "Hola",
        settings: "Ajustes",
        history: "Historial",
        login: "Iniciar sesión",
        register: "Registrarse",
        logout: "Cerrar sesión",
        language: "Idioma",
        theme: "Tema"
      },
      theme: { system: "Sistema", light: "Claro", dark: "Oscuro" },
      footer: { text: "Copiloto de investigación IA • © 2025" },
      home: {
        title: "Bienvenido a DuoMind",
        subtitle:
          "Copiloto de investigación con dos LLM. Inicia sesión, agrega tus claves y comienza.",
        search: "Pide a DuoMind comparar GPT y Gemini…",
        searchbtn: "Buscar",
        guestNote:
          "Modo invitado: 5 solicitudes/día. Añade tus claves para continuar sin límites.",
        dual: "Doble LLM",
        "dual.desc": "Ejecuta GPT + Gemini juntos y compara.",
        byok: "BYOK",
        "byok.desc": "Usa tus propias claves API para mayor potencia y privacidad.",
        history: "Historial",
        "history.desc": "Mira tus sesiones recientes.",
        guest: ""
      },
      login: {
        title: "Iniciar sesión",
        subtitle: "Accede a ajustes e historial.",
        email: "Correo",
        password: "Contraseña",
        button: "Entrar",
        noaccount: "¿Sin cuenta?",
        registerlink: "Regístrate"
      },
      register: {
        title: "Crear cuenta",
        subtitle: "El nombre de usuario se mostrará arriba a la derecha.",
        username: "Usuario",
        email: "Correo",
        password: "Contraseña",
        confirm: "Confirmar contraseña",
        rules: "≥ 8 caracteres, 2 dígitos, 1 especial y 1 mayúscula.",
        button: "Registrarse",
        already: "¿Ya tienes cuenta?",
        loginlink: "Entrar",
        alertMismatch: "Las contraseñas no coinciden.",
        alertWeak: "Contraseña débil."
      },
      settings: {
        title: "Ajustes",
        needlogin: "Debes iniciar sesión para editar tus claves.",
        desc: "Añade tus claves (BYOK) y el modelo preferido.",
        openai: "Clave API de OpenAI",
        gemini: "Clave API de Gemini",
        anthropic: "Clave API de Anthropic (Claude)",
        openrouter: "Clave API de OpenRouter",
        mistral: "Clave API de Mistral",
        tip: "Consejo: tus claves se almacenan cifradas y solo se usan para tus solicitudes.",
        preferred: "LLM preferido",
        save: "Guardar",
        keyValid: "Clave de {provider} válida",
        keyInvalid: "Clave de {provider} no válida",
        saved: "Ajustes guardados.",
        error: "No se pudieron guardar los ajustes.",
        opt: {
          auto: "Auto (GPT → Gemini)",
          openai: "OpenAI primero",
          gemini: "Gemini primero"
        ,
          anthropic: "Claude primero"
        ,
          openrouter: "OpenRouter primero"
        ,
          mistral: "Mistral primero"
        }
      },
      history: {
        title: "Historial",
        empty: "Aún no hay investigaciones.",
        loadMore: "Cargar más",
        needlogin: "Debes iniciar sesión para ver el historial.",
        cta: { login: "Iniciar sesión", register: "Registrarse" },
        search: "Buscar en el historial…"
      },
      research: {
        title: "Sesión de investigación",
        run: "Ejecutar",
        search: "Escribe una consulta…",
        models: "Modelos",
        tipPrefix: "Consejo: añade tus claves en",
        tipSuffix: "para desbloquear límites más altos.",
        explainer:
          "Ambos modelos respondieron. Los acuerdos muestran coincidencias; los desacuerdos muestran matices.",
        agreements: "Acuerdos",
        disagreements: "Desacuerdos",
        guest: "Modo invitado: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Respuesta (LLM A)",
        answerB: "Respuesta (LLM B)",
        synthesis: "Comparación / Síntesis",
        compare: "Comparar y reconciliar",
        recommendation: "Recomendación",
        openQuestions: "Preguntas abiertas",
        comparedBy: "Comparado por"
      },
      toasts: {
        keysSaved: "Ajustes guardados.",
        keysError: "No se pudieron guardar los ajustes.",
        guestLimit:
          "Se alcanzó el límite diario de invitado (5). Regístrate o agrega claves API.",
        needLogin: "Debes iniciar sesión para realizar esta acción.",
        invalidKeyOpenAI: "Clave de API de OpenAI no válida.",
        invalidKeyGemini: "Clave de API de Gemini no válida.",
        missingKey: "Falta la clave de API.",
        genericError: "Ocurrió un error. Inténtalo de nuevo."
      },
      common: { ok: "OK", cancel: "Cancelar", save: "Guardar" }
    },

    // ---------- Portuguese ----------
    pt: {
      nav: {
        home: "Início",
        settings: "Configurações",
        history: "Histórico",
        login: "Entrar",
        register: "Registrar",
        logout: "Sair",
        language: "Idioma",
        theme: "Tema"
      },
      theme: { system: "Sistema", light: "Claro", dark: "Escuro" },
      footer: { text: "Copiloto de pesquisa IA • © 2025" },
      home: {
        title: "Bem-vindo ao DuoMind",
        subtitle:
          "Copiloto de pesquisa com dois LLMs. Faça login, adicione suas chaves e comece.",
        search: "Peça ao DuoMind para comparar o GPT e o Gemini…",
        searchbtn: "Buscar",
        guestNote:
          "Modo convidado: 5 solicitações/dia. Adicione suas chaves para continuar sem limites.",
        dual: "LLM Duplo",
        "dual.desc": "Execute GPT + Gemini juntos e compare.",
        byok: "BYOK",
        "byok.desc": "Use suas próprias chaves API para mais potência e privacidade.",
        history: "Histórico",
        "history.desc": "Veja suas sessões recentes rapidamente.",
        guest: ""
      },
      login: {
        title: "Entrar",
        subtitle: "Acesse configurações e histórico.",
        email: "E-mail",
        password: "Senha",
        button: "Entrar",
        noaccount: "Ainda não tem conta?",
        registerlink: "Registrar"
      },
      register: {
        title: "Criar conta",
        subtitle: "O nome de usuário aparecerá no canto superior direito.",
        username: "Usuário",
        email: "E-mail",
        password: "Senha",
        confirm: "Confirmar senha",
        rules:
          "A senha deve ter pelo menos 8 caracteres, conter 2 dígitos, 1 símbolo e 1 maiúscula.",
        button: "Registrar",
        already: "Já tem conta?",
        loginlink: "Entrar",
        alertMismatch: "As senhas não coincidem.",
        alertWeak: "Senha fraca."
      },
      settings: {
        title: "Configurações",
        needlogin: "Faça login para editar suas chaves.",
        desc: "Adicione suas chaves (BYOK) e modelo preferido.",
        openai: "Chave API OpenAI",
        gemini: "Chave API Gemini",
        preferred: "LLM preferido",
        save: "Salvar",
        keyValid: "Chave {provider} válida",
        keyInvalid: "Chave {provider} inválida",
        saved: "Configurações salvas.",
        error: "Não foi possível salvar as configurações.",
        opt: {
          auto: "Auto (GPT → Gemini)",
          openai: "OpenAI primeiro",
          gemini: "Gemini primeiro"
        }
      },
      history: {
        title: "Histórico",
        empty: "Ainda sem pesquisas.",
        loadMore: "Carregar mais",
        needlogin: "É preciso entrar para ver o histórico.",
        cta: { login: "Entrar", register: "Registrar" },
        search: "Pesquisar no histórico…"
      },
      research: {
        title: "Sessão de pesquisa",
        run: "Executar",
        search: "Digite uma consulta…",
        models: "Modelos",
        tipPrefix: "Dica: adicione suas chaves em",
        tipSuffix: "para liberar limites mais altos.",
        explainer:
          "Ambos os modelos responderam. Os acordos mostram sobreposição; os desacordos mostram nuances.",
        agreements: "Concordâncias",
        disagreements: "Discordâncias",
        guest: "Modo convidado: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Resposta (LLM A)",
        answerB: "Resposta (LLM B)",
        synthesis: "Comparação / Síntese",
        compare: "Comparar e reconciliar",
        recommendation: "Recomendação",
        openQuestions: "Perguntas em aberto",
        comparedBy: "Comparado por"
      },
      toasts: {
        keysSaved: "Configurações salvas.",
        keysError: "Não foi possível salvar as configurações.",
        guestLimit:
          "Limite diário de convidado atingido (5 solicitações). Registre-se ou adicione chaves de API.",
        needLogin: "Você precisa entrar para executar esta ação.",
        invalidKeyOpenAI: "Chave de API OpenAI inválida.",
        invalidKeyGemini: "Chave de API Gemini inválida.",
        missingKey: "Falta a chave de API.",
        genericError: "Algo deu errado. Tente novamente."
      },
      common: { ok: "OK", cancel: "Cancelar", save: "Salvar" }
    },

    // ---------- Turkish ----------
    tr: {
      nav: {
        home: "Ana Sayfa",
      hello: "Merhaba",
        settings: "Ayarlar",
        history: "Geçmiş",
        login: "Giriş",
        register: "Kayıt ol",
        logout: "Çıkış",
        language: "Dil",
        theme: "Tema"
      },
      theme: { system: "Sistem", light: "Açık", dark: "Koyu" },
      footer: { text: "Yapay Zekâ Araştırma Asistanı • © 2025" },
      home: {
        title: "DuoMind’e Hoş Geldiniz",
        subtitle:
          "Çift LLM araştırma copilotu. Giriş yapın, anahtarlarınızı kaydedin ve başlayın.",
        search: "DuoMind’dan GPT ve Gemini karşılaştırması isteyin…",
        searchbtn: "Ara",
        guestNote:
          "Misafir modu: günde 5 istek. Limitsiz devam için API anahtarınızı ekleyin.",
        dual: "Çift LLM",
        "dual.desc": "GPT + Gemini birlikte çalışsın, bakış açılarını karşılaştırın.",
        byok: "BYOK",
        "byok.desc": "Tam güç ve gizlilik için kendi API anahtarınızı kullanın.",
        history: "Geçmiş",
        "history.desc": "Son araştırma oturumlarınızı görün.",
        guest: ""
      },
      login: {
        title: "Giriş",
        subtitle: "Ayarlar ve geçmişe erişin.",
        email: "E-posta",
        password: "Şifre",
        button: "Giriş",
        noaccount: "Hesabınız yok mu?",
        registerlink: "Kayıt ol"
      },
      register: {
        title: "Hesap oluştur",
        subtitle: "Kullanıcı adı girişten sonra sağ üstte görünür.",
        username: "Kullanıcı adı",
        email: "E-posta",
        password: "Şifre",
        confirm: "Şifreyi doğrula",
        rules:
          "Şifre en az 8 karakter olmalı; 2 rakam, 1 özel karakter ve 1 büyük harf içermeli.",
        button: "Kayıt ol",
        already: "Zaten hesabınız var mı?",
        loginlink: "Giriş",
        alertMismatch: "Şifreler eşleşmiyor.",
        alertWeak: "Zayıf şifre."
      },
      settings: {
        title: "Ayarlar",
        needlogin: "OpenAI / Gemini anahtarlarını düzenlemek için giriş yapın.",
        desc: "Kendi anahtarlarınızı (BYOK) ekleyin ve tercih edilen modeli seçin.",
        openai: "OpenAI API Anahtarı",
        gemini: "Gemini API Anahtarı",
        anthropic: "Anthropic (Claude) API Anahtarı",
        openrouter: "OpenRouter API Anahtarı",
        mistral: "Mistral API Anahtarı",
        tip: "İpucu: Anahtarlarınız şifreli saklanır ve yalnızca istekleriniz için kullanılır.",
        preferred: "Tercih edilen LLM",
        save: "Kaydet",
        keyValid: "{provider} anahtarı geçerli",
        keyInvalid: "{provider} anahtarı geçersiz",
        saved: "Ayarlar kaydedildi.",
        error: "Ayarlar kaydedilemedi.",
        opt: {
          auto: "Otomatik (GPT → Gemini)",
          openai: "Önce OpenAI",
          gemini: "Önce Gemini"
        ,
          anthropic: "Önce Claude"
        ,
          openrouter: "Önce OpenRouter"
        ,
          mistral: "Önce Mistral"
        }
      },
      history: {
        title: "Geçmiş",
        empty: "Henüz araştırma yok.",
        loadMore: "Daha fazla yükle",
        needlogin: "Geçmişi görmek için giriş yapın.",
        cta: { login: "Giriş", register: "Kayıt ol" },
        search: "Geçmişte ara…"
      },
      research: {
        title: "Araştırma oturumu",
        run: "Çalıştır",
        search: "Bir sorgu yazın…",
        models: "Modeller",
        tipPrefix: "İpucu: anahtarlarınızı şuraya ekleyin:",
        tipSuffix: "daha yüksek limitlerin kilidini açmak için.",
        explainer:
          "Her iki model de yanıt verdi. Benzerlikler örtüşmeyi; farklılıklar nüansı gösterir.",
        agreements: "Benzerlikler",
        disagreements: "Farklılıklar",
        guest: "Misafir modu: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Yanıt (LLM A)",
        answerB: "Yanıt (LLM B)",
        synthesis: "Karşılaştırma / Özet",
        compare: "Karşılaştır ve uzlaştır",
        recommendation: "Öneri",
        openQuestions: "Açık sorular",
        comparedBy: "Karşılaştıran"
      },
      toasts: {
        keysSaved: "Ayarlar kaydedildi.",
        keysError: "Ayarlar kaydedilemedi.",
        guestLimit:
          "Misafir günlük sınırı aşıldı (5 istek). Lütfen kayıt olun veya API anahtarı ekleyin.",
        needLogin: "Bu işlemi yapmak için giriş yapmalısınız.",
        invalidKeyOpenAI: "Geçersiz OpenAI API anahtarı.",
        invalidKeyGemini: "Geçersiz Gemini API anahtarı.",
        missingKey: "API anahtarı eksik.",
        genericError: "Bir şeyler ters gitti. Lütfen tekrar deneyin."
      },
      common: { ok: "Tamam", cancel: "İptal", save: "Kaydet" }
    },

    // ---------- Russian ----------
    ru: {
      nav: {
        home: "Главная",
      hello: "Привет",
        settings: "Настройки",
        history: "История",
        login: "Войти",
        register: "Регистрация",
        logout: "Выйти",
        language: "Язык",
        theme: "Тема"
      },
      theme: { system: "Системная", light: "Светлая", dark: "Тёмная" },
      footer: { text: "ИИ-помощник для исследований • © 2025" },
      home: {
        title: "Добро пожаловать в DuoMind",
        subtitle:
          "Копилот для исследований с двумя LLM. Войдите, добавьте ключи и начните.",
        search: "Попросите DuoMind сравнить GPT и Gemini…",
        searchbtn: "Поиск",
        guestNote:
          "Гостевой режим: 5 запросов в день. Добавьте ключи для продолжения без ограничений.",
        dual: "Двойной LLM",
        "dual.desc": "Запускайте GPT и Gemini вместе и сравнивайте.",
        byok: "BYOK",
        "byok.desc": "Используйте свои API-ключи для мощности и приватности.",
        history: "История",
        "history.desc": "Ваши недавние сессии исследования.",
        guest: ""
      },
      login: {
        title: "Вход",
        subtitle: "Доступ к настройкам и истории.",
        email: "Email",
        password: "Пароль",
        button: "Войти",
        noaccount: "Нет аккаунта?",
        registerlink: "Зарегистрироваться"
      },
      register: {
        title: "Создать аккаунт",
        subtitle: "Имя пользователя показывается справа вверху.",
        username: "Имя пользователя",
        email: "Email",
        password: "Пароль",
        confirm: "Подтвердите пароль",
        rules:
          "Пароль: не менее 8 символов, 2 цифры, 1 спецсимвол и 1 заглавная буква.",
        button: "Зарегистрироваться",
        already: "Уже есть аккаунт?",
        loginlink: "Войти",
        alertMismatch: "Пароли не совпадают.",
        alertWeak: "Слабый пароль."
      },
      settings: {
        title: "Настройки",
        needlogin: "Войдите, чтобы редактировать ключи OpenAI / Gemini.",
        desc: "Добавьте ключи (BYOK) и выберите предпочитаемую модель.",
        openai: "Ключ API OpenAI",
        gemini: "Ключ API Gemini",
        anthropic: "Ключ API Anthropic (Claude)",
        openrouter: "Ключ API OpenRouter",
        mistral: "Ключ API Mistral",
        tip: "Совет: ваши ключи хранятся в зашифрованном виде и используются только для ваших запросов.",
        preferred: "Предпочитаемая LLM",
        save: "Сохранить",
        keyValid: "Ключ {provider} действителен",
        keyInvalid: "Ключ {provider} недействителен",
        saved: "Сохранено.",
        error: "Не удалось сохранить.",
        opt: {
          auto: "Авто (GPT → Gemini)",
          openai: "Сначала OpenAI",
          gemini: "Сначала Gemini"
        ,
          anthropic: "Сначала Claude"
        ,
          openrouter: "Сначала OpenRouter"
        ,
          mistral: "Сначала Mistral"
        }
      },
      history: {
        title: "История",
        empty: "Пока нет исследований.",
        loadMore: "Показать ещё",
        needlogin: "Войдите, чтобы увидеть историю.",
        cta: { login: "Войти", register: "Регистрация" },
        search: "Поиск по истории…"
      },
      research: {
        title: "Сессия исследования",
        run: "Запуск",
        search: "Введите запрос…",
        models: "Модели",
        tipPrefix: "Совет: добавьте свои ключи в",
        tipSuffix: "чтобы увеличить лимиты.",
        explainer:
          "Ответили обе модели. Совпадения показывают пересечения; расхождения — нюансы.",
        agreements: "Совпадения",
        disagreements: "Расхождения",
        guest: "Гостевой режим: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Ответ (LLM A)",
        answerB: "Ответ (LLM B)",
        synthesis: "Сравнение / Сводка",
        compare: "Сравнить и согласовать",
        recommendation: "Рекомендация",
        openQuestions: "Открытые вопросы",
        comparedBy: "Сравнил"
      },
      toasts: {
        keysSaved: "Настройки сохранены.",
        keysError: "Не удалось сохранить настройки.",
        guestLimit:
          "Достигнут дневной лимит гостя (5 запросов). Зарегистрируйтесь или добавьте API-ключи.",
        needLogin: "Необходимо войти в систему для выполнения действия.",
        invalidKeyOpenAI: "Неверный API-ключ OpenAI.",
        invalidKeyGemini: "Неверный API-ключ Gemini.",
        missingKey: "Отсутствует API-ключ.",
        genericError: "Что-то пошло не так. Попробуйте снова."
      },
      common: { ok: "ОК", cancel: "Отмена", save: "Сохранить" }
    },

    // ---------- Japanese ----------
    ja: {
      nav: {
        home: "ホーム",
      hello: "こんにちは",
        settings: "設定",
        history: "履歴",
        login: "ログイン",
        register: "登録",
        logout: "ログアウト",
        language: "言語",
        theme: "テーマ"
      },
      theme: { system: "システム", light: "ライト", dark: "ダーク" },
      footer: { text: "AI リサーチコパイロット • © 2025" },
      home: {
        title: "DuoMind へようこそ",
        subtitle:
          "2つの LLM を使う研究コパイロット。ログインしキーを設定して始めましょう。",
        search: "GPT と Gemini を比較するよう DuoMind に依頼…",
        searchbtn: "検索",
        guestNote:
          "ゲストモード：1日5回。API キーを追加してください。",
        dual: "デュアル LLM",
        "dual.desc": "GPT と Gemini を同時に実行し比較します。",
        byok: "BYOK",
        "byok.desc": "独自の API キーでパワーとプライバシーを確保。",
        history: "履歴",
        "history.desc": "最近のセッションを一目で確認。",
        guest: ""
      },
      login: {
        title: "ログイン",
        subtitle: "設定と履歴にアクセスします。",
        email: "メール",
        password: "パスワード",
        button: "ログイン",
        noaccount: "アカウント未作成？",
        registerlink: "登録"
      },
      register: {
        title: "アカウント作成",
        subtitle: "ログイン後、ユーザー名は右上に表示されます。",
        username: "ユーザー名",
        email: "メール",
        password: "パスワード",
        confirm: "パスワード確認",
        rules:
          "8文字以上、数字2つ、記号1つ、大文字1つを含めてください。",
        button: "登録",
        already: "既にアカウントがありますか？",
        loginlink: "ログイン",
        alertMismatch: "パスワードが一致しません。",
        alertWeak: "パスワードが弱すぎます。"
      },
      settings: {
        title: "設定",
        needlogin: "OpenAI / Gemini キーを編集するにはログインしてください。",
        desc: "自分のキー (BYOK) と優先モデルを設定します。",
        openai: "OpenAI API キー",
        gemini: "Gemini API キー",
        anthropic: "Anthropic (Claude) API キー",
        openrouter: "OpenRouter API キー",
        mistral: "Mistral API キー",
        tip: "ヒント：キーは暗号化して保存され、あなたのリクエストにのみ使用されます。",
        preferred: "優先 LLM",
        save: "保存",
        keyValid: "{provider}キーは有効です",
        keyInvalid: "{provider}キーは無効です",
        saved: "設定を保存しました。",
        error: "設定を保存できませんでした。",
        opt: {
          auto: "自動 (GPT → Gemini)",
          openai: "OpenAI を優先",
          gemini: "Gemini を優先"
        ,
          anthropic: "Claude を優先"
        ,
          openrouter: "OpenRouter を優先"
        ,
          mistral: "Mistral を優先"
        }
      },
      history: {
        title: "履歴",
        empty: "まだ研究履歴はありません。",
        loadMore: "さらに表示",
        needlogin: "履歴を見るにはログインが必要です。",
        cta: { login: "ログイン", register: "登録" },
        search: "履歴を検索…"
      },
      research: {
        title: "リサーチセッション",
        run: "実行",
        search: "クエリを入力…",
        models: "モデル",
        tipPrefix: "ヒント：キーは",
        tipSuffix: "で追加すると上限が上がります。",
        explainer:
          "両モデルが回答しました。一致は共通点を、相違はニュアンスを示します。",
        agreements: "合意点",
        disagreements: "相違点",
        guest: "ゲストモード：GPT-4o mini + Gemini 1.5 Flash。",
        answerA: "回答 (LLM A)",
        answerB: "回答 (LLM B)",
        synthesis: "比較 / 要約",
        compare: "比較して統合",
        recommendation: "推奨",
        openQuestions: "未解決の質問",
        comparedBy: "比較者"
      },
      toasts: {
        keysSaved: "設定を保存しました。",
        keysError: "設定を保存できませんでした。",
        guestLimit:
          "ゲストの1日上限（5回）に達しました。登録するか API キーを追加してください。",
        needLogin: "この操作を行うにはログインが必要です。",
        invalidKeyOpenAI: "OpenAI の API キーが無効です。",
        invalidKeyGemini: "Gemini の API キーが無効です。",
        missingKey: "API キーがありません。",
        genericError: "エラーが発生しました。もう一度お試しください。"
      },
      common: { ok: "OK", cancel: "キャンセル", save: "保存" }
    },

    // ---------- Korean ----------
    ko: {
      nav: {
        home: "홈",
      hello: "안녕하세요",
        settings: "설정",
        history: "기록",
        login: "로그인",
        register: "가입",
        logout: "로그아웃",
        language: "언어",
        theme: "테마"
      },
      theme: { system: "시스템", light: "라이트", dark: "다크" },
      footer: { text: "AI 연구 코파일럿 • © 2025" },
      home: {
        title: "DuoMind에 오신 것을 환영합니다",
        subtitle:
          "이중 LLM 연구 코파일럿. 로그인하고 키를 설정한 후 시작하세요.",
        search: "GPT와 Gemini 비교 질문을 입력하세요…",
        searchbtn: "검색",
        guestNote:
          "게스트 모드: 하루 5회. API 키를 추가하면 제한 없이 사용 가능합니다.",
        dual: "듀얼 LLM",
        "dual.desc": "GPT와 Gemini를 함께 실행하고 관점을 비교하세요.",
        byok: "BYOK",
        "byok.desc": "자신의 API 키로 더 강력하고 안전하게.",
        history: "기록",
        "history.desc": "최근 연구 세션을 한눈에 확인.",
        guest: ""
      },
      login: {
        title: "로그인",
        subtitle: "설정과 기록에 접근합니다.",
        email: "이메일",
        password: "비밀번호",
        button: "로그인",
        noaccount: "계정이 없으신가요?",
        registerlink: "가입"
      },
      register: {
        title: "계정 만들기",
        subtitle: "로그인 후 사용자 이름이 오른쪽 상단에 표시됩니다.",
        username: "사용자 이름",
        email: "이메일",
        password: "비밀번호",
        confirm: "비밀번호 확인",
        rules: "8자 이상, 숫자 2개, 특수문자 1개, 대문자 1개 포함.",
        button: "가입",
        already: "이미 계정이 있나요?",
        loginlink: "로그인",
        alertMismatch: "비밀번호가 일치하지 않습니다.",
        alertWeak: "비밀번호가 너무 약합니다."
      },
      settings: {
        title: "설정",
        needlogin: "OpenAI / Gemini 키를 수정하려면 로그인하세요.",
        desc: "자신의 키(BYOK)와 선호 LLM을 설정하세요.",
        openai: "OpenAI API 키",
        gemini: "Gemini API 키",
        anthropic: "Anthropic (Claude) API 키",
        openrouter: "OpenRouter API 키",
        mistral: "Mistral API 키",
        tip: "팁: 키는 암호화되어 저장되며 요청에만 사용됩니다.",
        preferred: "선호 LLM",
        save: "저장",
        keyValid: "{provider} 키가 유효함",
        keyInvalid: "{provider} 키가 유효하지 않음",
        saved: "설정이 저장되었습니다.",
        error: "설정을 저장할 수 없습니다.",
        opt: {
          auto: "자동 (GPT → Gemini)",
          openai: "OpenAI 우선",
          gemini: "Gemini 우선"
        ,
          anthropic: "Claude 우선"
        ,
          openrouter: "OpenRouter 우선"
        ,
          mistral: "Mistral 우선"
        }
      },
      history: {
        title: "기록",
        empty: "아직 연구 기록이 없습니다.",
        loadMore: "더 보기",
        needlogin: "기록을 보려면 로그인해야 합니다.",
        cta: { login: "로그인", register: "가입" },
        search: "기록 검색…"
      },
      research: {
        title: "리서치 세션",
        run: "실행",
        search: "질문을 입력하세요…",
        models: "모델",
        tipPrefix: "팁: 키를",
        tipSuffix: "에서 추가하면 더 높은 한도를 사용할 수 있습니다.",
        explainer:
          "두 모델이 응답했습니다. 일치점은 공통점을, 불일치는 뉘앙스를 보여줍니다.",
        agreements: "일치점",
        disagreements: "불일치",
        guest: "게스트 모드: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "답변 (LLM A)",
        answerB: "답변 (LLM B)",
        synthesis: "비교 / 요약",
        compare: "비교 및 통합",
        recommendation: "권장사항",
        openQuestions: "열린 질문",
        comparedBy: "비교 모델"
      },
      toasts: {
        keysSaved: "설정이 저장되었습니다.",
        keysError: "설정을 저장할 수 없습니다.",
        guestLimit:
          "게스트 일일 한도(5회)에 도달했습니다. 회원가입 또는 API 키를 추가하세요.",
        needLogin: "이 작업을 하려면 로그인해야 합니다.",
        invalidKeyOpenAI: "잘못된 OpenAI API 키입니다.",
        invalidKeyGemini: "잘못된 Gemini API 키입니다.",
        missingKey: "API 키가 없습니다.",
        genericError: "문제가 발생했습니다. 다시 시도하세요."
      },
      common: { ok: "확인", cancel: "취소", save: "저장" }
    },

    // ---------- Chinese ----------
    zh: {
      nav: {
        home: "首页",
      hello: "你好",
        settings: "设置",
        history: "历史",
        login: "登录",
        register: "注册",
        logout: "退出",
        language: "语言",
        theme: "主题"
      },
      theme: { system: "系统", light: "浅色", dark: "深色" },
      footer: { text: "AI 研究副驾 • © 2025" },
      home: {
        title: "欢迎使用 DuoMind",
        subtitle: "双 LLM 研究副驾。登录、设置密钥并开始探索。",
        search: "让 DuoMind 比较 GPT 和 Gemini…",
        searchbtn: "搜索",
        guestNote: "访客模式：每天 5 次请求。添加 API 密钥可继续无限使用。",
        dual: "双 LLM",
        "dual.desc": "同时运行 GPT 和 Gemini 并比较观点。",
        byok: "BYOK",
        "byok.desc": "使用你自己的 API 密钥，更强更私密。",
        history: "历史",
        "history.desc": "快速查看最近会话。",
        guest: ""
      },
      login: {
        title: "登录",
        subtitle: "访问设置和历史记录。",
        email: "邮箱",
        password: "密码",
        button: "登录",
        noaccount: "还没有账号？",
        registerlink: "注册"
      },
      register: {
        title: "创建账户",
        subtitle: "登录后用户名显示在右上角。",
        username: "用户名",
        email: "邮箱",
        password: "密码",
        confirm: "确认密码",
        rules: "至少 8 位，包含 2 个数字、1 个特殊字符和 1 个大写字母。",
        button: "注册",
        already: "已有账号？",
        loginlink: "登录",
        alertMismatch: "两次密码不一致。",
        alertWeak: "密码太弱。"
      },
      settings: {
        title: "设置",
        needlogin: "登录后才能编辑 OpenAI / Gemini 密钥。",
        desc: "添加你的密钥（BYOK）并选择首选模型。",
        openai: "OpenAI API 密钥",
        gemini: "Gemini API 密钥",
        anthropic: "Anthropic（Claude）API 密钥",
        openrouter: "OpenRouter API 密钥",
        mistral: "Mistral API 密钥",
        tip: "提示：你的密钥将加密存储，仅用于你的请求。",
        preferred: "首选 LLM",
        save: "保存",
        keyValid: "{provider} 密钥有效",
        keyInvalid: "{provider} 密钥无效",
        saved: "已保存设置。",
        error: "无法保存设置。",
        opt: {
          auto: "自动 (GPT → Gemini)",
          openai: "优先 OpenAI",
          gemini: "优先 Gemini"
        ,
          anthropic: "优先 Claude"
        ,
          openrouter: "优先 OpenRouter"
        ,
          mistral: "优先 Mistral"
        }
      },
      history: {
        title: "历史",
        empty: "暂无研究记录。",
        loadMore: "加载更多",
        needlogin: "登录后查看研究历史。",
        cta: { login: "登录", register: "注册" },
        search: "搜索历史…"
      },
      research: {
        title: "研究会话",
        run: "运行",
        search: "输入查询…",
        models: "模型",
        tipPrefix: "提示：在",
        tipSuffix: "中添加你的密钥以解锁更高额度。",
        explainer: "两个模型均已响应。共识显示重叠；分歧体现差异与细节。",
        agreements: "共识",
        disagreements: "分歧",
        guest: "访客模式：GPT-4o mini + Gemini 1.5 Flash。",
        answerA: "回答（LLM A）",
        answerB: "回答（LLM B）",
        synthesis: "比较 / 综合",
        compare: "对比并整合",
        recommendation: "建议",
        openQuestions: "开放问题",
        comparedBy: "对比模型"
      },
      toasts: {
        keysSaved: "已保存设置。",
        keysError: "无法保存设置。",
        guestLimit:
          "已达到访客每日上限（5 次）。请注册或添加 API 密钥继续使用。",
        needLogin: "执行此操作需要登录。",
        invalidKeyOpenAI: "无效的 OpenAI API 密钥。",
        invalidKeyGemini: "无效的 Gemini API 密钥。",
        missingKey: "缺少 API 密钥。",
        genericError: "发生错误，请重试。"
      },
      common: { ok: "确定", cancel: "取消", save: "保存" }
    },

    // ---------- Thai ----------
    th: {
      nav: {
        home: "หน้าแรก",
      hello: "สวัสดี",
        settings: "การตั้งค่า",
        history: "ประวัติ",
        login: "เข้าสู่ระบบ",
        register: "สมัคร",
        logout: "ออกจากระบบ",
        language: "ภาษา",
        theme: "ธีม"
      },
      theme: { system: "ระบบ", light: "สว่าง", dark: "มืด" },
      footer: { text: "ผู้ช่วยวิจัย AI • © 2025" },
      home: {
        title: "ยินดีต้อนรับสู่ DuoMind",
        subtitle: "โคไพลอตวิจัยแบบสอง LLM ลงชื่อเข้าใช้ ตั้งค่าคีย์ แล้วเริ่มต้นได้เลย",
        search: "ให้ DuoMind เปรียบเทียบ GPT กับ Gemini…",
        searchbtn: "ค้นหา",
        guestNote: "โหมดผู้เยี่ยมชม: วันละ 5 ครั้ง เพิ่มคีย์ API เพื่อใช้งานต่อโดยไม่จำกัด",
        dual: "LLM คู่",
        "dual.desc": "รัน GPT + Gemini พร้อมกันแล้วเปรียบเทียบมุมมอง",
        byok: "BYOK",
        "byok.desc": "ใช้คีย์ของคุณเองเพื่อพลังและความเป็นส่วนตัว",
        history: "ประวัติ",
        "history.desc": "ดูเซสชันวิจัยล่าสุดของคุณได้ทันที",
        guest: ""
      },
      login: {
        title: "เข้าสู่ระบบ",
        subtitle: "เข้าถึงการตั้งค่าและประวัติของคุณ",
        email: "อีเมล",
        password: "รหัสผ่าน",
        button: "เข้าสู่ระบบ",
        noaccount: "ยังไม่มีบัญชี?",
        registerlink: "สมัคร"
      },
      register: {
        title: "สร้างบัญชี",
        subtitle: "ชื่อผู้ใช้จะแสดงที่มุมขวาบนหลังเข้าสู่ระบบ",
        username: "ชื่อผู้ใช้",
        email: "อีเมล",
        password: "รหัสผ่าน",
        confirm: "ยืนยันรหัสผ่าน",
        rules: "รหัสผ่านอย่างน้อย 8 ตัว มีตัวเลข 2 ตัว อักขระพิเศษ 1 ตัว และตัวพิมพ์ใหญ่ 1 ตัว",
        button: "สมัคร",
        already: "มีบัญชีอยู่แล้ว?",
        loginlink: "เข้าสู่ระบบ",
        alertMismatch: "รหัสผ่านไม่ตรงกัน",
        alertWeak: "รหัสผ่านไม่ปลอดภัย"
      },
      settings: {
        title: "การตั้งค่า",
        needlogin: "ต้องเข้าสู่ระบบเพื่อแก้ไขคีย์ OpenAI / Gemini",
        desc: "เพิ่มคีย์ของคุณ (BYOK) และเลือก LLM ที่ต้องการ",
        openai: "คีย์ API OpenAI",
        gemini: "คีย์ API Gemini",
        anthropic: "คีย์ API Anthropic (Claude)",
        openrouter: "คีย์ API OpenRouter",
        mistral: "คีย์ API Mistral",
        tip: "ทิป: คีย์ของคุณจะถูกจัดเก็บแบบเข้ารหัสและใช้เฉพาะกับคำขอของคุณเท่านั้น",
        preferred: "LLM ที่ต้องการ",
        save: "บันทึก",
        keyValid: "คีย์ {provider} ใช้ได้",
        keyInvalid: "คีย์ {provider} ใช้ไม่ได้",
        saved: "บันทึกการตั้งค่าแล้ว",
        error: "ไม่สามารถบันทึกการตั้งค่าได้",
        opt: {
          auto: "อัตโนมัติ (GPT → Gemini)",
          openai: "OpenAI ก่อน",
          gemini: "Gemini ก่อน"
        ,
          anthropic: "Claude ก่อน"
        ,
          openrouter: "OpenRouter ก่อน"
        ,
          mistral: "Mistral ก่อน"
        }
      },
      history: {
        title: "ประวัติ",
        empty: "ยังไม่มีการค้นคว้า",
        loadMore: "โหลดเพิ่มเติม",
        needlogin: "ต้องเข้าสู่ระบบเพื่อดูประวัติ",
        cta: { login: "เข้าสู่ระบบ", register: "สมัคร" },
        search: "ค้นหาประวัติ…"
      },
      research: {
        title: "เซสชันการค้นคว้า",
        run: "รัน",
        search: "พิมพ์คำค้น…",
        models: "โมเดล",
        tipPrefix: "ทิป: เพิ่มคีย์ของคุณใน",
        tipSuffix: "เพื่อปลดล็อกขีดจำกัดที่สูงขึ้น",
        explainer:
          "ทั้งสองโมเดลตอบกลับแล้ว จุดที่ตรงกันแสดงส่วนที่ซ้อนทับกัน; จุดที่ต่างกันแสดงมุมมองเพิ่มเติม",
        agreements: "จุดที่ตรงกัน",
        disagreements: "จุดที่ต่างกัน",
        guest: "โหมดผู้เยี่ยมชม: GPT-4o mini + Gemini 1.5 Flash",
        answerA: "คำตอบ (LLM A)",
        answerB: "คำตอบ (LLM B)",
        synthesis: "การเปรียบเทียบ / สรุป",
        compare: "เปรียบเทียบและผสาน",
        recommendation: "คำแนะนำ",
        openQuestions: "คำถามที่ยังค้าง",
        comparedBy: "เปรียบเทียบโดย"
      },
      toasts: {
        keysSaved: "บันทึกการตั้งค่าแล้ว",
        keysError: "ไม่สามารถบันทึกการตั้งค่าได้",
        guestLimit:
          "ถึงขีดจำกัดโหมดผู้เยี่ยมชมต่อวัน (5 ครั้ง) โปรดสมัครหรือเพิ่มคีย์ API",
        needLogin: "ต้องเข้าสู่ระบบเพื่อดำเนินการนี้",
        invalidKeyOpenAI: "คีย์ API ของ OpenAI ไม่ถูกต้อง",
        invalidKeyGemini: "คีย์ API ของ Gemini ไม่ถูกต้อง",
        missingKey: "ไม่มีคีย์ API",
        genericError: "เกิดข้อผิดพลาด โปรดลองอีกครั้ง"
      },
      common: { ok: "ตกลง", cancel: "ยกเลิก", save: "บันทึก" }
    },

    // ---------- Indonesian ----------
    id: {
      nav: {
        home: "Beranda",
      hello: "Halo",
        settings: "Pengaturan",
        history: "Riwayat",
        login: "Masuk",
        register: "Daftar",
        logout: "Keluar",
        language: "Bahasa",
        theme: "Tema"
      },
      theme: { system: "Sistem", light: "Terang", dark: "Gelap" },
      footer: { text: "Kopilot riset AI • © 2025" },
      home: {
        title: "Selamat datang di DuoMind",
        subtitle: "Kopilot riset dengan dua LLM. Masuk, atur kunci Anda, lalu mulai.",
        search: "Minta DuoMind membandingkan GPT dan Gemini…",
        searchbtn: "Cari",
        guestNote: "Mode tamu: 5 permintaan/hari. Tambahkan kunci API untuk tanpa batas.",
        dual: "LLM Ganda",
        "dual.desc": "Jalankan GPT + Gemini bersama dan bandingkan sudut pandang.",
        byok: "BYOK",
        "byok.desc": "Gunakan kunci API sendiri demi daya dan privasi.",
        history: "Riwayat",
        "history.desc": "Lihat sesi riset terbaru Anda dengan cepat.",
        guest: ""
      },
      login: {
        title: "Masuk",
        subtitle: "Akses pengaturan dan riwayat Anda.",
        email: "Email",
        password: "Kata sandi",
        button: "Masuk",
        noaccount: "Belum punya akun?",
        registerlink: "Daftar"
      },
      register: {
        title: "Buat akun",
        subtitle: "Nama pengguna akan tampil di kanan atas setelah login.",
        username: "Nama pengguna",
        email: "Email",
        password: "Kata sandi",
        confirm: "Konfirmasi kata sandi",
        rules: "Minimal 8 karakter, 2 digit, 1 simbol, dan 1 huruf besar.",
        button: "Daftar",
        already: "Sudah punya akun?",
        loginlink: "Masuk",
        alertMismatch: "Kata sandi tidak cocok.",
        alertWeak: "Kata sandi lemah."
      },
      settings: {
        title: "Pengaturan",
        needlogin: "Masuk untuk mengedit kunci OpenAI / Gemini.",
        desc: "Tambahkan kunci Anda (BYOK) dan pilih LLM favorit.",
        openai: "Kunci API OpenAI",
        gemini: "Kunci API Gemini",
        anthropic: "Kunci API Anthropic (Claude)",
        openrouter: "Kunci API OpenRouter",
        mistral: "Kunci API Mistral",
        tip: "Tip: kunci Anda disimpan terenkripsi dan hanya digunakan untuk permintaan Anda.",
        preferred: "LLM pilihan",
        save: "Simpan",
        keyValid: "Kunci {provider} valid",
        keyInvalid: "Kunci {provider} tidak valid",
        saved: "Pengaturan disimpan.",
        error: "Tidak dapat menyimpan pengaturan.",
        opt: {
          auto: "Otomatis (GPT → Gemini)",
          openai: "OpenAI dulu",
          gemini: "Gemini dulu"
        ,
          anthropic: "Claude dulu"
        ,
          openrouter: "OpenRouter dulu"
        ,
          mistral: "Mistral dulu"
        }
      },
      history: {
        title: "Riwayat",
        empty: "Belum ada sesi riset.",
        loadMore: "Muat lagi",
        needlogin: "Masuk untuk melihat riwayat.",
        cta: { login: "Masuk", register: "Daftar" },
        search: "Cari riwayat…"
      },
      research: {
        title: "Sesi riset",
        run: "Jalankan",
        search: "Ketik kueri…",
        models: "Model",
        tipPrefix: "Tips: tambahkan kunci Anda di",
        tipSuffix: "untuk membuka batas yang lebih tinggi.",
        explainer:
          "Kedua model merespons. Kesepakatan menunjukkan tumpang tindih; perbedaan menunjukkan nuansa.",
        agreements: "Kesepakatan",
        disagreements: "Perbedaan",
        guest: "Mode tamu: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Jawaban (LLM A)",
        answerB: "Jawaban (LLM B)",
        synthesis: "Perbandingan / Sintesis",
        compare: "Bandingkan & satukan",
        recommendation: "Rekomendasi",
        openQuestions: "Pertanyaan terbuka",
        comparedBy: "Dibandingkan oleh"
      },
      toasts: {
        keysSaved: "Pengaturan disimpan.",
        keysError: "Tidak dapat menyimpan pengaturan.",
        guestLimit:
          "Batas harian tamu tercapai (5 permintaan). Daftar atau tambahkan kunci API.",
        needLogin: "Anda harus masuk untuk melakukan tindakan ini.",
        invalidKeyOpenAI: "Kunci API OpenAI tidak valid.",
        invalidKeyGemini: "Kunci API Gemini tidak valid.",
        missingKey: "Kunci API hilang.",
        genericError: "Terjadi kesalahan. Coba lagi."
      },
      common: { ok: "OK", cancel: "Batal", save: "Simpan" }
    },

    // ---------- Vietnamese ----------
    vi: {
      nav: {
        home: "Trang chủ",
      hello: "Xin chào",
        settings: "Cài đặt",
        history: "Lịch sử",
        login: "Đăng nhập",
        register: "Đăng ký",
        logout: "Đăng xuất",
        language: "Ngôn ngữ",
        theme: "Chủ đề"
      },
      theme: { system: "Hệ thống", light: "Sáng", dark: "Tối" },
      footer: { text: "Trợ lý nghiên cứu AI • © 2025" },
      home: {
        title: "Chào mừng đến với DuoMind",
        subtitle: "Trợ lý nghiên cứu với 2 LLM. Đăng nhập, đặt khóa và bắt đầu.",
        search: "Yêu cầu DuoMind so sánh GPT và Gemini…",
        searchbtn: "Tìm kiếm",
        guestNote: "Chế độ khách: 5 lượt/ngày. Thêm khóa API để dùng không giới hạn.",
        dual: "LLM Kép",
        "dual.desc": "Chạy GPT + Gemini cùng lúc và so sánh.",
        byok: "BYOK",
        "byok.desc": "Dùng khóa API riêng để mạnh mẽ và riêng tư.",
        history: "Lịch sử",
        "history.desc": "Xem nhanh các phiên gần đây.",
        guest: ""
      },
      login: {
        title: "Đăng nhập",
        subtitle: "Truy cập cài đặt và lịch sử.",
        email: "Email",
        password: "Mật khẩu",
        button: "Đăng nhập",
        noaccount: "Chưa có tài khoản?",
        registerlink: "Đăng ký"
      },
      register: {
        title: "Tạo tài khoản",
        subtitle: "Tên người dùng hiển thị ở góc phải trên sau khi đăng nhập.",
        username: "Tên người dùng",
        email: "Email",
        password: "Mật khẩu",
        confirm: "Xác nhận mật khẩu",
        rules: "Tối thiểu 8 ký tự, gồm 2 số, 1 ký tự đặc biệt và 1 chữ hoa.",
        button: "Đăng ký",
        already: "Đã có tài khoản?",
        loginlink: "Đăng nhập",
        alertMismatch: "Mật khẩu không khớp.",
        alertWeak: "Mật khẩu yếu."
      },
      settings: {
        title: "Cài đặt",
        needlogin: "Hãy đăng nhập để sửa khóa OpenAI / Gemini.",
        desc: "Thêm khóa (BYOK) và chọn mô hình ưa thích.",
        openai: "Khóa API OpenAI",
        gemini: "Khóa API Gemini",
        anthropic: "Khóa API Anthropic (Claude)",
        openrouter: "Khóa API OpenRouter",
        mistral: "Khóa API Mistral",
        tip: "Mẹo: khóa của bạn được lưu mã hóa và chỉ dùng cho các yêu cầu của bạn.",
        preferred: "LLM ưa thích",
        save: "Lưu",
        keyValid: "Khóa {provider} hợp lệ",
        keyInvalid: "Khóa {provider} không hợp lệ",
        saved: "Đã lưu cài đặt.",
        error: "Không thể lưu cài đặt.",
        opt: {
          auto: "Tự động (GPT → Gemini)",
          openai: "Ưu tiên OpenAI",
          gemini: "Ưu tiên Gemini"
        ,
          anthropic: "Ưu tiên Claude"
        ,
          openrouter: "Ưu tiên OpenRouter"
        ,
          mistral: "Ưu tiên Mistral"
        }
      },
      history: {
        title: "Lịch sử",
        empty: "Chưa có phiên nghiên cứu nào.",
        loadMore: "Tải thêm",
        needlogin: "Đăng nhập để xem lịch sử.",
        cta: { login: "Đăng nhập", register: "Đăng ký" },
        search: "Tìm trong lịch sử…"
      },
      research: {
        title: "Phiên nghiên cứu",
        run: "Chạy",
        search: "Nhập truy vấn…",
        models: "Mô hình",
        tipPrefix: "Mẹo: thêm khóa của bạn trong",
        tipSuffix: "để mở khóa giới hạn cao hơn.",
        explainer:
          "Cả hai mô hình đã phản hồi. Điểm đồng cho thấy phần giao; điểm khác thể hiện sắc thái.",
        agreements: "Điểm đồng",
        disagreements: "Điểm khác",
        guest: "Chế độ khách: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "Câu trả lời (LLM A)",
        answerB: "Câu trả lời (LLM B)",
        synthesis: "So sánh / Tổng hợp",
        compare: "So sánh & hòa giải",
        recommendation: "Khuyến nghị",
        openQuestions: "Câu hỏi mở",
        comparedBy: "So sánh bởi"
      },
      toasts: {
        keysSaved: "Đã lưu cài đặt.",
        keysError: "Không thể lưu cài đặt.",
        guestLimit:
          "Đã đạt giới hạn khách mỗi ngày (5 lượt). Vui lòng đăng ký hoặc thêm khóa API.",
        needLogin: "Bạn phải đăng nhập để thực hiện thao tác này.",
        invalidKeyOpenAI: "Khoá API OpenAI không hợp lệ.",
        invalidKeyGemini: "Khoá API Gemini không hợp lệ.",
        missingKey: "Thiếu khoá API.",
        genericError: "Đã xảy ra lỗi. Vui lòng thử lại."
      },
      common: { ok: "OK", cancel: "Hủy", save: "Lưu" }
    },

    // ---------- Arabic ----------
    ar: {
      nav: {
        home: "الرئيسية",
      hello: "مرحباً",
        settings: "الإعدادات",
        history: "السجل",
        login: "تسجيل الدخول",
        register: "إنشاء حساب",
        logout: "تسجيل الخروج",
        language: "اللغة",
        theme: "السمة"
      },
      theme: { system: "النظام", light: "فاتح", dark: "داكن" },
      footer: { text: "مساعد أبحاث بالذكاء الاصطناعي • © 2025" },
      home: {
        title: "مرحبًا بك في DuoMind",
        subtitle: "مساعد أبحاث ثنائي النماذج. سجّل الدخول وأضف مفاتيحك وابدأ.",
        search: "اطلب من DuoMind مقارنة GPT وGemini…",
        searchbtn: "بحث",
        guestNote: "وضع الزائر: 5 طلبات يوميًا. أضف مفاتيح API للمتابعة دون حدود.",
        dual: "نماذج مزدوجة",
        "dual.desc": "شغّل GPT وGemini معًا وقارن النتائج.",
        byok: "BYOK",
        "byok.desc": "استخدم مفاتيحك الخاصة لمزيد من القوة والخصوصية.",
        history: "السجل",
        "history.desc": "اعرض جلساتك الأخيرة بسرعة.",
        guest: ""
      },
      login: {
        title: "تسجيل الدخول",
        subtitle: "الوصول إلى الإعدادات والسجل.",
        email: "البريد الإلكتروني",
        password: "كلمة المرور",
        button: "تسجيل الدخول",
        noaccount: "لا تملك حسابًا؟",
        registerlink: "إنشاء حساب"
      },
      register: {
        title: "إنشاء حساب",
        subtitle: "سيظهر اسم المستخدم في الأعلى بعد تسجيل الدخول.",
        username: "اسم المستخدم",
        email: "البريد الإلكتروني",
        password: "كلمة المرور",
        confirm: "تأكيد كلمة المرور",
        rules:
          "كلمة المرور: 8 أحرف على الأقل، تحتوي على رقمين، ورمز خاص، وحرف كبير واحد.",
        button: "إنشاء حساب",
        already: "لديك حساب؟",
        loginlink: "تسجيل الدخول",
        alertMismatch: "كلمتا المرور غير متطابقتين.",
        alertWeak: "كلمة المرور ضعيفة."
      },
      settings: {
        title: "الإعدادات",
        needlogin: "يلزم تسجيل الدخول لتعديل مفاتيح OpenAI / Gemini.",
        desc: "أضف مفاتيحك (BYOK) واختر النموذج المفضل.",
        openai: "مفتاح OpenAI",
        gemini: "مفتاح Gemini",
        anthropic: "مفتاح Anthropic (Claude)",
        openrouter: "مفتاح OpenRouter",
        mistral: "مفتاح Mistral",
        tip: "معلومة: تُحفظ مفاتيحك مشفّرة وتُستخدم فقط لطلباتك.",
        preferred: "النموذج المفضل",
        save: "حفظ",
        keyValid: "مفتاح {provider} صالح",
        keyInvalid: "مفتاح {provider} غير صالح",
        saved: "تم حفظ الإعدادات.",
        error: "تعذر حفظ الإعدادات.",
        opt: {
          auto: "تلقائي (GPT → Gemini)",
          openai: "أولوية OpenAI",
          gemini: "أولوية Gemini"
        ,
          anthropic: "Claude أولاً"
        ,
          openrouter: "OpenRouter أولاً"
        ,
          mistral: "Mistral أولاً"
        }
      },
      history: {
        title: "السجل",
        empty: "لا توجد جلسات حتى الآن.",
        loadMore: "تحميل المزيد",
        needlogin: "سجّل الدخول للاطلاع على السجل.",
        cta: { login: "تسجيل الدخول", register: "إنشاء حساب" },
        search: "ابحث في السجل…"
      },
      research: {
        title: "جلسة بحث",
        run: "تشغيل",
        search: "اكتب استعلامًا…",
        models: "النماذج",
        tipPrefix: "نصيحة: أضف مفاتيحك في",
        tipSuffix: "لفتح حدود أعلى.",
        explainer:
          "استجاب النموذجان. تُظهر نقاط الاتفاق التداخل؛ ونقاط الاختلاف تُظهر الفروق الدقيقة.",
        agreements: "نقاط الاتفاق",
        disagreements: "نقاط الاختلاف",
        guest: "وضع الزائر: GPT-4o mini + Gemini 1.5 Flash.",
        answerA: "إجابة (LLM A)",
        answerB: "إجابة (LLM B)",
        synthesis: "مقارنة / تلخيص",
        compare: "قارن ووفّق",
        recommendation: "التوصية",
        openQuestions: "أسئلة مفتوحة",
        comparedBy: "تمت المقارنة بواسطة"
      },
      toasts: {
        keysSaved: "تم حفظ الإعدادات.",
        keysError: "تعذر حفظ الإعدادات.",
        guestLimit:
          "تم بلوغ حد الزائر اليومي (5 طلبات). يُرجى التسجيل أو إضافة مفاتيح API للمتابعة.",
        needLogin: "يلزم تسجيل الدخول لتنفيذ هذا الإجراء.",
        invalidKeyOpenAI: "مفتاح OpenAI غير صالح.",
        invalidKeyGemini: "مفتاح Gemini غير صالح.",
        missingKey: "مفتاح API مفقود.",
        genericError: "حدث خطأ ما. حاول مرة أخرى."
      },
      common: { ok: "حسنًا", cancel: "إلغاء", save: "حفظ" }
    }
  };

  // Ensure home.guest always defined
  Object.keys(T).forEach((lang) => {
    const L = T[lang];
    if (!L.home) L.home = {};
    if (!L.home.guest) {
      L.home.guest = (L.research && L.research.guest) || L.home.guestNote || "";
    }
  });

  // ================== AUTO i18n key helpers (FIXED) ==================
  function slugifyForKey(str) {
    return String(str)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .slice(0, 40);
  }

  function bootstrapAutoKeys(root, lang, dict) {
    // create base keys only from English
    if ((lang || "en") !== "en") return;

    root.querySelectorAll("[data-i18n-auto]").forEach((el) => {
      if (el.getAttribute("data-i18n")) return;

      const base = (el.textContent || "").trim();
      if (!base) return;

      const slug = slugifyForKey(base) || "text";
      const key = "auto." + slug;

      el.setAttribute("data-i18n", key);

      if (!dict.en.auto) dict.en.auto = {};
      if (!dict.en.auto[slug]) dict.en.auto[slug] = base;
    });
  }
  // ================== END AUTO HELPERS ==================

  // ================== FUZZY MAPPINGS ==================
  function normSpaces(s) {
    return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function canon(s) {
    return normSpaces(s)
      .replace(/[＋+]/g, " plus ")
      .replace(/[^a-z0-9\s]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  const LIT_EQ = {
    "login": "login.title",
    "create account": "register.title",
    "email": "login.email",
    "password": "login.password",
    "username": "register.username",
    "confirm password": "register.confirm",
    "no account yet?": "login.noaccount",
    "register": "login.registerlink",
    "theme": "nav.theme",
    "system": "theme.system",
    "light": "theme.light",
    "dark": "theme.dark",
    "dual llm": "home.dual",
    "byok": "home.byok",
    "history": "home.history",
    "research session": "research.title",
    "run": "research.run",
    "agreements": "research.agreements",
    "disagreements": "research.disagreements",
    "load more": "history.loadMore",
    "no research sessions yet.": "history.empty",
    "settings": "settings.title",
    "save": "common.save"
  };

  const LIT_CONTAINS = [
    { needle: "run gpt plus gemini together and compare perspectives", key: "home.dual.desc" },
    { needle: "bring your own api keys for full power and privacy", key: "home.byok.desc" },
    { needle: "see your recent research sessions at a glance", key: "home.history.desc" },
    { needle: "you are currently in guest mode", key: "home.guest" },
    { needle: "gpt 4o mini plus gemini 1 5 flash", key: "home.guest" },
    { needle: "log in to access your settings and history", key: "login.subtitle" },
    { needle: "username will be shown in the top right after login", key: "register.subtitle" },
    {
      needle:
        "password must be at least 8 characters contain 2 digits 1 special character and 1 uppercase letter",
      key: "register.rules"
    },
    { needle: "already have an account", key: "register.already" },
    {
      needle:
        "both models responded agreements show overlap disagreements show nuance",
      key: "research.explainer"
    },
    { needle: "settings saved", key: "toasts.keysSaved" },
    { needle: "could not save settings", key: "toasts.keysError" },
    { needle: "daily guest limit reached", key: "toasts.guestLimit" },
    {
      needle: "you must be logged in to view your research history",
      key: "history.needlogin"
    },
    {
      needle: "you must be logged in to perform this action",
      key: "toasts.needLogin"
    },
    { needle: "invalid openai api key", key: "toasts.invalidKeyOpenAI" },
    { needle: "invalid gemini api key", key: "toasts.invalidKeyGemini" },
    { needle: "missing api key", key: "toasts.missingKey" },
    {
      needle: "something went wrong please try again",
      key: "toasts.genericError"
    }
  ];

  function byPath(lang, path) {
    const root = T[lang] || T.en;
    if (!path) return "";
    const parts = String(path).split(".");

    // direct nested lookup
    let obj = root;
    let ok = true;
    for (const k of parts) {
      if (obj && typeof obj === "object" && Object.prototype.hasOwnProperty.call(obj, k)) {
        obj = obj[k];
      } else {
        ok = false;
        break;
      }
    }
    if (ok && (typeof obj === "string" || typeof obj === "number")) {
      return String(obj);
    }

    // tail lookup
    let base = root;
    for (let i = 0; i < parts.length; i++) {
      if (!base || typeof base !== "object") break;
      const tail = parts.slice(i).join(".");
      if (Object.prototype.hasOwnProperty.call(base, tail)) {
        const v = base[tail];
        if (typeof v === "string" || typeof v === "number") return String(v);
      }
      const key = parts[i];
      if (Object.prototype.hasOwnProperty.call(base, key)) {
        base = base[key];
      } else {
        break;
      }
    }
    return "";
  }

  function replaceLiterals(root, lang) {
    const nodes = root.querySelectorAll(
      "h1,h2,h3,h4,p,span,button,a,li,label,small,strong,em"
    );
    nodes.forEach((el) => {
      if (el.hasAttribute("data-i18n")) return;
      if (el.children && el.children.length > 0) return;
      const raw = el.textContent || "";
      const n = normSpaces(raw);
      if (!n) return;
      const c = canon(raw);

      if (LIT_EQ[n]) {
        const v = byPath(lang, LIT_EQ[n]);
        if (v) el.textContent = v;
        return;
      }
      for (const m of LIT_CONTAINS) {
        if (c.includes(m.needle)) {
          const v = byPath(lang, m.key);
          if (v) el.textContent = v;
          break;
        }
      }
    });
  }

  // ================== RTL GUARD ==================
  const RTL_CSS = `
  html[dir="rtl"] body,
  html[dir="rtl"] .navbar,
  html[dir="rtl"] .container,
  html[dir="rtl"] .card-row,
  html[dir="rtl"] .card,
  html[dir="rtl"] .search-group {
    direction: ltr !important;
  }
  html[dir="rtl"] h1,
  html[dir="rtl"] h2,
  html[dir="rtl"] h3,
  html[dir="rtl"] p,
  html[dir="rtl"] label,
  html[dir="rtl"] .modal,
  html[dir="rtl"] .card-body {
    direction: rtl !important;
    text-align: right !important;
  }
  html[dir="rtl"] input,
  html[dir="rtl"] textarea {
    direction: rtl !important;
    text-align: right !important;
  }`;

  function ensureRtlGuard(enabled) {
    let tag = document.getElementById("duomind-rtl-guard");
    if (enabled) {
      if (!tag) {
        tag = document.createElement("style");
        tag.id = "duomind-rtl-guard";
        tag.type = "text/css";
        tag.appendChild(document.createTextNode(RTL_CSS));
        document.head.appendChild(tag);
      }
    } else if (tag) {
      tag.remove();
    }
  }

  // ================== CORE APPLY ==================
  let CUR = pickInitialLang();

  function applyTranslations(root) {
    const lang = CUR;

    // ✅ fixed: auto-keys now receives lang+dict, no global CUR reference
    bootstrapAutoKeys(root, lang, T);

    // data-i18n text
    root.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const v = byPath(lang, key);
      if (v) el.textContent = v;
    });

    // attributes
    root.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      const key = el.getAttribute("data-i18n-placeholder");
      const v = byPath(lang, key);
      if (v) el.setAttribute("placeholder", v);
    });
    root.querySelectorAll("[data-i18n-title]").forEach((el) => {
      const key = el.getAttribute("data-i18n-title");
      const v = byPath(lang, key);
      if (v) el.setAttribute("title", v);
    });
    root.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const key = el.getAttribute("data-i18n-aria");
      const v = byPath(lang, key);
      if (v) el.setAttribute("aria-label", v);
    });

    // fuzzy for leftover literals
    replaceLiterals(root, lang);

    // dropdown label
    const dd = document.querySelector(".lang-dropdown .lang-current");
    const btn = document.querySelector('.lang-dropdown [data-lang="' + lang + '"]');
    if (dd && btn) dd.textContent = btn.textContent.trim();

    // lang/dir + RTL
    document.documentElement.setAttribute("lang", lang);
    const isRtl = lang === RTL_CODE;
    document.documentElement.setAttribute("dir", isRtl ? "rtl" : "ltr");
    ensureRtlGuard(isRtl);
  }

  function setLang(code) {
    if (!code) return;
    code = String(code).toLowerCase();
    const alias = {
      "zh-cn": "zh",
      "zh-hans": "zh",
      "zh-hant": "zh",
      "zh-tw": "zh",
      "pt-br": "pt",
      "pt-pt": "pt"
    };
    if (code.includes("-")) code = code.split("-")[0];
    code = alias[code] || code;
    if (!SUP.includes(code)) return;
    CUR = code;
    setCookie(COOKIE, code);
    applyTranslations(document);
    const ev = new CustomEvent("duomind:langchange", { detail: { lang: code } });
    window.dispatchEvent(ev);
  }

  // public
  window.DuoMindI18N = {
    get lang() {
      return CUR;
    },
    // Translate a key in the current language, falling back to English.
    t(key) {
      return byPath(CUR, key) || byPath("en", key) || "";
    },
    setLang
  };

  // dropdown click handler (scoped to .lang-dropdown)
  document.addEventListener("click", (e) => {
    const el = e.target.closest(".lang-dropdown [data-lang]");
    if (!el) return;
    e.preventDefault();
    const code = el.getAttribute("data-lang");
    setLang(code);
  });

  // observe DOM for modals / injected content
  let timer = null;
  const obs = new MutationObserver(() => {
    clearTimeout(timer);
    timer = setTimeout(() => applyTranslations(document), 30);
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });

  // initial apply
  applyTranslations(document);
})();
