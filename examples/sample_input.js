/**
 * Calculates the factorial of a number.
 * @param {number} n The number to calculate the factorial of.
 * @returns {number} The factorial of n.
 */
function calculateFactorial(n) {
  if (n < 0) {
    return -1; // Or throw an error
  }
  if (n === 0) {
    return 1;
  }
  return n * calculateFactorial(n - 1);
}

// Another simple function for testing
function greet(name) {
  return `Hello, ${name}!`;
}

module.exports = { calculateFactorial, greet };