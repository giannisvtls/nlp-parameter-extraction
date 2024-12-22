import { useCallback, useRef } from 'react';

/**
 * A custom React hook that returns a debounced version of a callback function.
 *
 * This hook delays the execution of the provided callback function until
 * after a specified delay in milliseconds has passed since the last time
 * the debounced function was invoked.
 * If the debounced function is called again before the delay period has expired,
 * the previous timeout is cleared and a new one is set.
 *
 * @param {function} callback - The callback function to be debounced.
 * @param {number} [delay=500] - The amount of time in milliseconds to wait before invoking the callback.
 *
 * @returns {function} A debounced version of the callback function that can be called with any arguments.
 * The returned function also clears the timeout when called.
 */
const useDebouncedCallback = (callback, delay = 500) => {
  const timeoutRef = useRef();

  return useCallback((...args) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, delay);

    return () => clearTimeout(timeoutRef.current);
  }, [callback, delay]);

};

export default useDebouncedCallback;
