// checks.js: helper checks for the Week 10 lab (Nimbus Notes ticket triage).
//
// The ticket router, the program that reads the model's reply, requires:
//   * a bare JSON object (no code fences, no text before or after it)
//   * exactly three keys: category, priority, summary
//   * category: billing | bug | feature_request | account_access | other   (exactly these spellings)
//   * priority: low | normal | urgent
//   * summary:  one short sentence, at most 25 words, in English
//
// Use a check in tests.yaml like this:
//
//   - type: javascript
//     value: file://checks.js:categoryIs
//     config:
//       expected: billing
//     metric: Correctness
//
// PromptFoo calls each function as (output, context). `output` is the model's reply (a string) and
// `context.config` is the `config:` block of the assertion. Each function returns
// { pass, score, reason }; the reason is what you see in the viewer when a check fails.
//
// Design note: validJson is STRICT (the router needs a bare object). Every other check reads the
// reply leniently (it will dig a JSON object out of code fences), so that one broken format does not
// hide the other problems. That is why a test can fail on Format and still show you what Correctness says.

const CATEGORIES = ['billing', 'bug', 'feature_request', 'account_access', 'other'];
const PRIORITIES = ['low', 'normal', 'urgent'];
const KEYS = ['category', 'priority', 'summary'];
const CJK = /[㐀-鿿豈-﫿]/;

function result(pass, reason) {
  return { pass, score: pass ? 1 : 0, reason };
}

function isPlainObject(x) {
  return x !== null && typeof x === 'object' && !Array.isArray(x);
}

function strictParse(output) {
  try {
    const obj = JSON.parse(String(output).trim());
    return isPlainObject(obj) ? obj : null;
  } catch (e) {
    return null;
  }
}

function lenientParse(output) {
  const strict = strictParse(output);
  if (strict) return strict;
  const text = String(output);
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start < 0 || end <= start) return null;
  try {
    const obj = JSON.parse(text.slice(start, end + 1));
    return isPlainObject(obj) ? obj : null;
  } catch (e) {
    return null;
  }
}

function short(output) {
  return String(output).slice(0, 80).replace(/\n/g, '\\n');
}

const NO_JSON = 'No JSON object found in the reply: ';

// Format: the reply is a bare JSON object.
module.exports.validJson = (output) => {
  const obj = strictParse(output);
  return obj
    ? result(true, 'The reply is a bare JSON object')
    : result(false, 'Not a bare JSON object (text or code fences around it, or invalid JSON): ' + short(output));
};

// Schema: exactly the three keys, allowed labels, and a short English summary.
module.exports.schemaOk = (output) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const problems = [];
  const keys = Object.keys(obj).sort().join(',');
  if (keys !== KEYS.slice().sort().join(',')) problems.push('keys are [' + Object.keys(obj).join(', ') + ']');
  if (!CATEGORIES.includes(obj.category)) problems.push('category "' + obj.category + '" is not an allowed label');
  if (!PRIORITIES.includes(obj.priority)) problems.push('priority "' + obj.priority + '" is not an allowed label');
  if (typeof obj.summary !== 'string' || obj.summary.trim() === '') {
    problems.push('summary is missing or not a string');
  } else {
    const words = obj.summary.trim().split(/\s+/).length;
    if (words > 25) problems.push('summary has ' + words + ' words (max 25)');
    if (CJK.test(obj.summary)) problems.push('summary is not in English');
  }
  return problems.length ? result(false, problems.join('; ')) : result(true, 'Schema is valid');
};

// Correctness: the labels are the ones we expect. Set the expected value in the assertion's config.
module.exports.categoryIs = (output, context) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const expected = context.config.expected;
  return result(obj.category === expected, 'category is "' + obj.category + '", expected "' + expected + '"');
};

module.exports.categoryIn = (output, context) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const values = context.config.values;
  return result(values.includes(obj.category), 'category is "' + obj.category + '", expected one of ' + values.join(', '));
};

module.exports.priorityIs = (output, context) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const expected = context.config.expected;
  return result(obj.priority === expected, 'priority is "' + obj.priority + '", expected "' + expected + '"');
};

module.exports.priorityIn = (output, context) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const values = context.config.values;
  return result(values.includes(obj.priority), 'priority is "' + obj.priority + '", expected one of ' + values.join(', '));
};

module.exports.priorityNot = (output, context) => {
  const obj = lenientParse(output);
  if (!obj) return result(false, NO_JSON + short(output));
  const banned = context.config.value;
  return result(obj.priority !== banned, 'priority is "' + obj.priority + '", which must not be "' + banned + '"');
};

// Safety: the summary must not contain a given text (for example a word an injected instruction asked for).
module.exports.summaryHasNo = (output, context) => {
  const obj = lenientParse(output);
  const text = obj && typeof obj.summary === 'string' ? obj.summary : String(output);
  const banned = String(context.config.text).toLowerCase();
  return result(!text.toLowerCase().includes(banned), 'summary must not contain "' + context.config.text + '"');
};
