/**
 * Creates a query string from an object of parameters.
 *
 * This function takes an object containing key-value pairs and converts it into a URL query string format.
 * Each key-value pair is represented as `key=value`, and pairs are joined with the `&` character.
 *
 * @param {Object} params - An object containing key-value pairs to be converted into URL parameters.
 * @returns {string} The constructed query string in the format "key1=value1&key2=value2&...".
 */
export const createUrlParams = (params) => {
  let urlParams = [];
  Object.entries(params).forEach(([key, value]) => {
    urlParams.push(`${key}=${value}`);
  });

  const queryParam = urlParams.join('&')
  return queryParam
}
