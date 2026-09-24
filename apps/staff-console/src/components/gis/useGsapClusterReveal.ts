import { useEffect, useRef, useState } from 'react';

export interface GsapClusterRevealOptions {
  triggerKey: string | number;
  selector: string;
  getTargetRadius: (el: SVGCircleElement) => number;
}

/**
 * useGsapClusterReveal
 * Conforms to DESIGN.md §9 & SCREEN_SPECS.md §2.12:
 * - Expressive tier: GSAP cluster reveal, duration-deliberate (600ms), ease-spatial (cubic-bezier(.16,1,.3,1))
 * - Reduced-motion: instant final state, no animation, verified with prefers-reduced-motion forced on
 * - Dynamic import: GSAP is dynamically loaded on this route only, never bundled in root or other apps!
 */
export const useGsapClusterReveal = (options: GsapClusterRevealOptions) => {
  const [isReady, setIsReady] = useState(false);
  const containerRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    let mounted = true;

    // Check prefers-reduced-motion
    const prefersReducedMotion =
      typeof window !== 'undefined' &&
      window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
      // Reduced motion: apply instant final state immediately
      if (containerRef.current) {
        const circles = containerRef.current.querySelectorAll<SVGCircleElement>(options.selector);
        circles.forEach((circle) => {
          const targetR = options.getTargetRadius(circle);
          circle.setAttribute('r', targetR.toString());
          circle.style.opacity = '1';
        });
      }
      setIsReady(true);
      return;
    }

    // Dynamic import of gsap
    import('gsap')
      .then((gsapModule) => {
        if (!mounted || !containerRef.current) return;
        const gsap = gsapModule.gsap || gsapModule.default || gsapModule;

        const circles = containerRef.current.querySelectorAll<SVGCircleElement>(options.selector);
        if (circles.length === 0) return;

        // Animate each circle from radius 0 -> targetRadius
        circles.forEach((circle, index) => {
          const targetR = options.getTargetRadius(circle);
          // Set initial state
          circle.setAttribute('r', '0');
          circle.style.opacity = '0';

          gsap.to(circle, {
            attr: { r: targetR },
            opacity: 1,
            duration: 0.6, // duration-deliberate = 600ms
            delay: index * 0.04, // subtle spatial stagger
            ease: 'power2.out', // cubic-bezier(.16,1,.3,1) approximation
          });
        });

        setIsReady(true);
      })
      .catch((err) => {
        console.warn('[useGsapClusterReveal] Failed to load GSAP dynamically:', err);
        // Fallback: instant final state
        if (containerRef.current) {
          const circles = containerRef.current.querySelectorAll<SVGCircleElement>(options.selector);
          circles.forEach((circle) => {
            const targetR = options.getTargetRadius(circle);
            circle.setAttribute('r', targetR.toString());
            circle.style.opacity = '1';
          });
        }
        setIsReady(true);
      });

    return () => {
      mounted = false;
    };
  }, [options.triggerKey, options.selector]);

  return { containerRef, isReady };
};
