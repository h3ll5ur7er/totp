//! #Example module
//! example module for demonstraton purposes
//!
//! ## Example
//! ```
//! use rust_template::operations::add;
//! let result = add(2, 3);
//! assert_eq!(result, 5);
//! ```
//!

/// Adds two numbers
///
/// # Example
/// ```
/// use rust_template::operations::add;
/// let result = add(1, 2);
/// assert_eq!(result, 3);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
