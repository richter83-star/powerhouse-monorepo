
// Internationalization (i18n) Configuration
// Supports multiple languages with dynamic loading

export type Locale = 'en' | 'es' | 'fr' | 'de' | 'ja' | 'zh';

export interface Translation {
  [key: string]: string | Translation;
}

const translations: Record<Locale, () => Promise<Translation>> = {
  en: () => import('@/locales/en.json').then(m => m.default),
  es: () => import('@/locales/es.json').then(m => m.default),
  fr: () => import('@/locales/fr.json').then(m => m.default),
  de: () => import('@/locales/de.json').then(m => m.default),
  ja: () => import('@/locales/ja.json').then(m => m.default),
  zh: () => import('@/locales/zh.json').then(m => m.default),
};

let currentLocale: Locale = 'en';
let currentTranslations: Translation = {};

export async function setLocale(locale: Locale): Promise<void> {
  currentLocale = locale;
  currentTranslations = await translations[locale]();
  if (typeof window !== 'undefined') {
    localStorage.setItem('preferred-locale', locale);
    document.documentElement.lang = locale;
  }
}

export function getLocale(): Locale {
  return currentLocale;
}

export function t(key: string, params?: Record<string, string>): string {
  const keys = key.split('.');
  let value: any = currentTranslations;
  
  for (const k of keys) {
    value = value?.[k];
    if (value === undefined) return key;
  }
  
  let result = String(value);
  
  if (params) {
    Object.entries(params).forEach(([paramKey, paramValue]) => {
      result = result.replace(`{{${paramKey}}}`, paramValue);
    });
  }
  
  return result;
}

export async function initI18n(): Promise<void> {
  if (typeof window !== 'undefined') {
    const savedLocale = localStorage.getItem('preferred-locale') as Locale;
    const browserLocale = navigator.language.split('-')[0] as Locale;
    const locale = savedLocale || (translations[browserLocale] ? browserLocale : 'en');
    await setLocale(locale);
  } else {
    await setLocale('en');
  }
}
