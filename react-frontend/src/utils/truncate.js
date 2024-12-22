/**
 * Truncates a string to a specified character count, optionally appending a delimiter.
 *
 * This function takes a string and limits its length to the specified character count.
 * If the character count exceeds the length of the string, the original string is returned.
 * The function also handles trailing spaces by removing them and appending a specified delimiter.
 *
 * @param {string} subjectString - The string to be truncated.
 * @param {number} characterCount - The maximum number of characters to retain from the beginning of the string.
 * @param {string} [delimiter=''] - An optional string to append to the truncated string.
 * @returns {string} The truncated string with the delimiter appended, or the original string if the character count exceeds its length.
 *
 * @throws {TypeError} If the first argument is not a string or the second argument is not a number.
 */
export const truncate = (subjectString, characterCount, delimiter) => {
  var regex, truncated;

  if (typeof subjectString !== 'string') {
    throw new TypeError('Expected a string for first argument');
  }

  if (typeof characterCount !== 'number') {
    throw new TypeError('Expected a number for second argument');
  }

  characterCount = Math.floor(characterCount);

  if (
    characterCount > subjectString.length
        || characterCount < 0
  ) {
    return subjectString;
  }

  regex = new RegExp('^.{0,' + characterCount + '}[S]*', 'g');
  truncated = subjectString.match(regex);
  delimiter = delimiter || '';
  truncated = truncated[0].replace(/\s$/, '');
  truncated = truncated + delimiter;

  return truncated;
};
