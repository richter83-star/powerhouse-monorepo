
// Accessibility utilities

/**
 * Generate a unique ID for form elements
 */
export function generateId(prefix: string = 'id'): string {
  return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Announce to screen readers
 */
export function announceToScreenReader(message: string, priority: 'polite' | 'assertive' = 'polite') {
  if (typeof window === 'undefined') return;
  
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;
  
  document.body.appendChild(announcement);
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}

/**
 * Trap focus within a modal or dialog
 */
export function trapFocus(element: HTMLElement) {
  const focusableElements = element.querySelectorAll<HTMLElement>(
    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );
  
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  function handleTabKey(e: KeyboardEvent) {
    if (e.key !== 'Tab') return;
    
    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    }
  }
  
  element.addEventListener('keydown', handleTabKey);
  
  return () => {
    element.removeEventListener('keydown', handleTabKey);
  };
}

/**
 * Get contrast ratio between two colors
 */
export function getContrastRatio(color1: string, color2: string): number {
  const getLuminance = (color: string) => {
    // This is a simplified version - in production, use a proper color library
    const rgb = color.match(/\d+/g)?.map(Number) || [0, 0, 0];
    const [r, g, b] = rgb.map(val => {
      const normalized = val / 255;
      return normalized <= 0.03928
        ? normalized / 12.92
        : Math.pow((normalized + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if element is visible to assistive technologies
 */
export function isAccessible(element: HTMLElement): boolean {
  const style = window.getComputedStyle(element);
  
  return (
    style.display !== 'none' &&
    style.visibility !== 'hidden' &&
    style.opacity !== '0' &&
    element.getAttribute('aria-hidden') !== 'true'
  );
}

/**
 * Keyboard navigation helper
 */
export function handleArrowNavigation(
  event: React.KeyboardEvent,
  items: HTMLElement[],
  currentIndex: number,
  options?: {
    loop?: boolean;
    horizontal?: boolean;
  }
) {
  const { loop = true, horizontal = false } = options || {};
  const maxIndex = items.length - 1;
  
  let newIndex = currentIndex;
  
  if (horizontal) {
    if (event.key === 'ArrowLeft') newIndex--;
    if (event.key === 'ArrowRight') newIndex++;
  } else {
    if (event.key === 'ArrowUp') newIndex--;
    if (event.key === 'ArrowDown') newIndex++;
  }
  
  if (event.key === 'Home') newIndex = 0;
  if (event.key === 'End') newIndex = maxIndex;
  
  if (newIndex < 0) {
    newIndex = loop ? maxIndex : 0;
  } else if (newIndex > maxIndex) {
    newIndex = loop ? 0 : maxIndex;
  }
  
  if (newIndex !== currentIndex) {
    event.preventDefault();
    items[newIndex]?.focus();
  }
  
  return newIndex;
}
